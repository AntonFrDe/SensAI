"""CLI checks: run main.py as a real subprocess against a fake Ollama and the real MCP server. Run: python3 test_cli.py"""
import json
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

from fake_ollama import FakeOllama, start

ROOT = Path(__file__).parent
OLLAMA = f"http://127.0.0.1:{start(FakeOllama)}"


def cli(stdin, *args):
    return subprocess.run(
        [sys.executable, str(ROOT / "main.py"), *args], input=stdin, capture_output=True, text=True, timeout=30, cwd=ROOT
    )


POKER_TOOLS = {"poker": {"command": [sys.executable, "mcp_server.py"]}}


def chat(stdin, *args, model="ok", url=OLLAMA, servers=None, tool_call=None, mode="--libre", profiles=None):
    """Run the CLI with a throwaway config pointing at the fake Ollama (and at MCP servers, if any).

    The plain chat (--libre) by default; mode=None runs the trainer.
    """
    FakeOllama.reset()
    FakeOllama.tool_call = tool_call
    with tempfile.TemporaryDirectory() as tmp:
        config = Path(tmp) / "config.json"
        config.write_text(json.dumps({"model": model, "ollama_url": url, "num_ctx": 1024,
                                      "system_prompt_file": "prompts/system.txt", "mcp_servers": servers or {},
                                      "banque_file": str(Path(tmp) / "banque.jsonl"),
                                      "profiles_dir": profiles or str(Path(tmp) / "profiles")}))
        return cli(stdin, "--config", str(config), *filter(None, [mode]), *args)


def roles(request):
    return [m["role"] for m in request["messages"]]


def test_streams_the_answer_and_shows_stats():
    p = chat("salut\n/quit\n")
    assert p.returncode == 0
    assert "Hello" in p.stdout                       # "Hel" + "lo" arrive as two chunks
    assert "[réflexion…]" in p.stdout                # the model's thinking is signalled, not printed
    assert "hmm" not in p.stdout
    assert "20 tokens · 10.0 tok/s" in p.stdout


def test_history_is_kept_within_the_session():
    chat("salut\nsuite\n/quit\n")
    first, second = FakeOllama.requests
    assert roles(first) == ["system", "user"]        # the system prompt comes from the file
    assert roles(second) == ["system", "user", "assistant", "user"]
    assert [m["content"] for m in second["messages"][1:]] == ["salut", "Hello", "suite"]


def test_reset_forgets_the_conversation():
    chat("a\n/reset\nb\n/quit\n")
    assert [m["content"] for m in FakeOllama.requests[1]["messages"][1:]] == ["b"]


def test_empty_input_is_refused_and_never_sent():
    p = chat("\n   \n/quit\n")
    assert p.returncode == 0 and "Message vide" in p.stdout
    assert FakeOllama.requests == []


def test_end_of_input_quits_cleanly():
    p = chat("salut\n")                              # no /quit: stdin just ends (Ctrl-D)
    assert p.returncode == 0 and len(FakeOllama.requests) == 1


def test_model_argument_overrides_the_config():
    chat("hi\n/quit\n", "--model", "a", model="ok")
    assert FakeOllama.requests[0]["model"] == "a"


def test_unknown_model_stops_with_a_useful_message():
    p = chat("hi\n", model="ghost")
    assert p.returncode == 1
    assert "ghost" in p.stderr and "ollama pull ghost" in p.stderr and "ok" in p.stderr   # lists what is installed
    assert FakeOllama.requests == []


def test_ollama_down_stops_with_a_clear_message():
    p = chat("hi\n", url="http://127.0.0.1:1")
    assert p.returncode == 1 and "Cannot reach Ollama" in p.stderr


def test_a_failed_turn_keeps_the_session_alive_and_out_of_the_history():
    p = chat("hi\nagain\n/quit\n", model="missing")   # installed as far as the tags go, but chatting fails (404)
    assert p.returncode == 0 and p.stderr.count("ollama pull missing") == 2
    assert [m["content"] for m in FakeOllama.requests[1]["messages"][1:]] == ["again"]


def test_ctrl_c_stops_the_answer_and_keeps_the_session():
    FakeOllama.reset()
    with tempfile.TemporaryDirectory() as tmp:
        config = Path(tmp) / "config.json"
        config.write_text(json.dumps({"model": "slow1", "ollama_url": OLLAMA, "num_ctx": 1024,
                                      "system_prompt_file": "prompts/system.txt"}))
        p = subprocess.Popen([sys.executable, str(ROOT / "main.py"), "--config", str(config), "--libre"], cwd=ROOT,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        p.stdin.write("hi\n")
        p.stdin.flush()
        while "réflexion" not in p.stdout.readline():   # the answer is streaming: now interrupt it
            pass
        p.send_signal(signal.SIGINT)
        out, err = p.communicate("again\n/quit\n", timeout=30)
    assert p.returncode == 0 and "(interrompu)" in out and "Traceback" not in err
    assert [m["content"] for m in FakeOllama.requests[1]["messages"][1:]] == ["again"]   # the cut turn is forgotten


def test_bad_config_is_reported():
    p = cli("", "--config", "/nonexistent/config.json")
    assert p.returncode == 1 and "Configuration" in p.stderr


def test_model_calls_an_mcp_tool_then_answers_with_its_result():
    p = chat("AhKh sur Qh 7h 2c ?\n/quit\n", servers=POKER_TOOLS,
             tool_call={"name": "hand_odds", "arguments": {"hand": "Ah Kh", "board": "Qh 7h 2c"}})

    assert p.returncode == 0 and "[outil] hand_odds" in p.stdout and "Hello" in p.stdout
    first, second = FakeOllama.requests
    assert {t["function"]["name"] for t in first["tools"]} == {"hand_odds", "define_term", "preflop_open", "hand_rankings"}
    assert roles(second) == ["system", "user", "assistant", "tool"]
    assert second["messages"][2]["tool_calls"][0]["function"]["name"] == "hand_odds"
    tool = second["messages"][3]
    assert tool["tool_name"] == "hand_odds" and "Outs : 15" in tool["content"]   # computed by mcp_server.py


def test_tool_turns_stay_in_the_history():
    chat("AhKh ?\nmerci\n/quit\n", servers=POKER_TOOLS, tool_call={"name": "hand_rankings", "arguments": {}})
    third = FakeOllama.requests[2]   # the 2nd question: after the tool round and the answer of the 1st
    assert roles(third) == ["system", "user", "assistant", "tool", "assistant", "user"]


def test_tool_errors_reach_the_model_instead_of_crashing():
    chat("hi\n/quit\n", servers=POKER_TOOLS, tool_call={"name": "hand_odds", "arguments": {"hand": "Ah Ah"}})
    assert FakeOllama.requests[1]["messages"][-1]["content"].startswith("Erreur : Arguments invalides")


def test_broken_tool_server_is_reported_and_the_chat_goes_on():
    p = chat("hi\n/quit\n", servers={"ghost": {"command": ["/nonexistent/server"]}})
    assert p.returncode == 0 and "ghost" in p.stderr and "Hello" in p.stdout
    assert "tools" not in FakeOllama.requests[0]


def test_no_tools_flag_starts_no_server():
    chat("hi\n/quit\n", "--no-tools", servers=POKER_TOOLS)
    assert "tools" not in FakeOllama.requests[0]


def test_trainer_asks_the_level_then_deals_a_situation():
    p = chat("4\n1\n/quit\n", mode=None)
    assert p.returncode == 0 and "Quel est ton niveau" in p.stdout
    assert "Réponds par un numéro de 1 à 3." in p.stdout
    assert "Situation 1 · Table 6 joueurs, 100 blindes" in p.stdout and "[f] se coucher   [r] relancer" in p.stdout
    assert FakeOllama.requests == []   # the situation comes from the code, not from the model


def test_a_free_answer_off_schema_falls_back_to_the_numbered_choice():
    p = chat("je joue un peu le vendredi\n2\n/quit\n", mode=None)
    assert "Je n'ai pas compris. Réponds par un numéro de 1 à 3." in p.stdout   # the fake model answers off schema
    assert "Situation 1 ·" in p.stdout and "format" in FakeOllama.requests[0]


def test_trainer_grades_the_decision_then_the_coach_debriefs_it():
    p = chat("1\nsalut\nf\npourquoi ?\n/quit\n", mode=None)
    assert "Choisis une action : [f] se coucher   [r] relancer" in p.stdout   # no debrief before the decision
    assert any(v in p.stdout for v in ("✅ Bon :", "🟡 Acceptable :", "❌ Erreur :"))
    assert "- Référence : ranges d'ouverture 6-max, 100 blindes." in p.stdout and "Hello" in p.stdout
    (request,) = FakeOllama.requests
    assert roles(request) == ["system", "user"]
    system = request["messages"][0]["content"]
    cards = next(line for line in p.stdout.splitlines() if " Tu as " in line).split(" Tu as ")[1]
    assert f"Tu as {cards}" in system and "Décision du joueur : se coucher. Verdict :" in system


def test_exercice_deals_the_next_situation_with_a_fresh_debrief():
    p = chat("1\nf\nq1\n/exercice\nf\nq2\n/quit\n", mode=None)
    assert "Situation 2 ·" in p.stdout
    assert [m["content"] for m in FakeOllama.requests[1]["messages"][1:]] == ["q2"]


def test_niveau_changes_the_level_and_its_themes():
    p = chat("1\n/niveau\n3\n/quit\n", mode=None)
    second = p.stdout.split("Situation 2 ·")[1]
    assert "Board :" in second and "[c] suivre" in second   # the advanced level plays draws on the flop or turn


def test_seed_replays_the_same_situations():
    first, second, other = (chat("2\n/exercice\n/exercice\n/quit\n", "--seed", seed, mode=None).stdout
                            for seed in ("7", "7", "8"))
    assert first == second and first != other


def test_fiche_off_schema_is_reported_and_the_session_goes_on():
    p = chat("1\n/fiche\nf\n/fiche\n/quit\n", mode=None)
    assert p.returncode == 0 and "Fiche impossible : décide d'abord" in p.stdout
    assert "Fiche impossible : champ manquant ou vide : a_retenir." in p.stdout   # the fake model answers off schema


def test_the_coach_question_shows_numbered_choices():
    p = chat("1\nf\npourquoi ?\n2\n/quit\n", mode=None,
             tool_call={"name": "poser_question", "arguments": {"question": "Outs ?", "choix": ["9", "15"]}})
    assert "Outs ?\n  1. 9\n  2. 15" in p.stdout
    assert FakeOllama.requests[-1]["messages"][-1]["content"] == "Je réponds : 15"


def test_pseudo_remembers_the_level_and_resumes_the_debrief():
    with tempfile.TemporaryDirectory() as profiles:
        first = chat("1\nf\npourquoi ?\n/quit\n", "--pseudo", "amine", mode=None, profiles=profiles)
        assert "Quel est ton niveau" in first.stdout

        again = chat("/reprendre\net au bouton ?\n/quit\n", "--pseudo", "Amine", mode=None, profiles=profiles)
    assert "Quel est ton niveau" not in again.stdout
    assert "Re-bonjour amine · niveau : Je découvre" in again.stdout
    assert "Dernière situation ·" in again.stdout and "Coach : Hello" in again.stdout
    assert [m["content"] for m in FakeOllama.requests[-1]["messages"][1:]] == ["pourquoi ?", "Hello", "et au bouton ?"]


def test_reprendre_without_a_profile_says_there_is_nothing():
    p = chat("1\n/reprendre\n/quit\n", mode=None)
    assert "Rien à reprendre" in p.stdout


def test_a_bad_pseudo_is_refused():
    p = chat("", "--pseudo", "../x", mode=None)
    assert p.returncode == 1 and "pseudo" in p.stderr


def test_end_of_input_leaves_the_trainer_at_any_step():
    assert chat("", mode=None).returncode == 0
    assert chat("2\n", mode=None).returncode == 0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)

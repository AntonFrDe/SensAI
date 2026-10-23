"""SensAI in the terminal: a poker trainer. It asks your level, deals a situation, grades your decision against a
reference computed by the code, then the coach (a local Ollama model) debriefs it, answers streamed as written.

    python3 main.py [--model M] [--config config.json] [--no-tools] [--seed N] [--pseudo P] [--libre]

Commands: /exercice deals the next situation, /fiche writes what to remember, /niveau changes the level,
/reprendre brings back the last debrief of the profile, /reset forgets the debrief, /tools lists the tools,
/quit (or Ctrl-D) leaves, Ctrl-C stops an answer. --pseudo keeps the level and the results in
profiles/<pseudo>.json. --libre is the plain chat.
The model can call the tools of the MCP servers listed under "mcp_servers" in the config (see mcp_client.py).
"""
import argparse
import json
import random
import sys
from collections.abc import Iterator
from contextlib import closing

import ai
import coach
import generation
import profils
import trainer
from llm import ROOT, LLMError, list_models, load_config
from mcp_client import Toolbox

DIM, RED, RESET = "\033[2m", "\033[31m", "\033[0m"
KEYS = {"fold": "f", "call": "c", "raise": "r", "moi": "m", "adversaire": "a", "egalite": "e"}
ICONS = {"bon": "✅", "acceptable": "🟡", "erreur": "❌"}
CHARS_PER_TOKEN = 3   # ponytail: rough estimate, use Ollama's prompt_eval_count if the context still overflows


def with_context(text: str, history: list[dict]) -> str:
    """The question, preceded by the glossary entries not already in the history and the question's own data.

    Keywords never miss a term written in the question, embeddings add the ones close in meaning, the tools
    catch the rest.
    """
    given = "\n".join(m["content"] for m in history if m["role"] == "user")
    new = [e for e in ai.glossary_entries_for(text) if f"\n- {e.term}" not in given]
    parts = (ai.glossary_context(entries=new), ai.preflop_context(text), ai.situation_context(text))
    context = "\n\n".join(p for p in parts if p)
    return f"Contexte :\n{context}\n\nQuestion : {text}" if context else text


def trim(history: list[dict], cfg: dict) -> list[dict]:
    """Forget the oldest whole turns while the history would overflow the model's context."""
    fixed = len(cfg["system_prompt"]) + len(json.dumps(cfg.get("tools", [])))
    budget = cfg["num_ctx"] * 3 // 4 * CHARS_PER_TOKEN - fixed  # a quarter left free for the answer
    while any(m["role"] == "user" for m in history[1:]) and sum(len(m["content"]) for m in history) > budget:
        history = history[1:]
        while history and history[0]["role"] != "user":  # never start on an orphan answer or tool result
            history = history[1:]
    return history


def style(text: str, code: str, stream) -> str:
    """Colour only when writing to a terminal, so pipes and files stay clean."""
    return f"{code}{text}{RESET}" if stream.isatty() else text


def fail(message: str) -> None:
    print(style(f"Erreur : {message}", RED, sys.stderr), file=sys.stderr)


def note(message: str) -> None:
    print(style(message, DIM, sys.stdout), flush=True)


def ensure_model(cfg: dict) -> None:
    """Stop early, with a useful message, if Ollama is down or the model is not installed."""
    names = [m["name"] for m in list_models(cfg)]
    accepted = {cfg["model"], cfg["model"] + ":latest"}  # Ollama resolves a bare name to :latest
    if not accepted & set(names):
        raise LLMError(
            f"Modèle \"{cfg['model']}\" introuvable. Installés : {', '.join(names) or 'aucun'}. "
            f"Pour l'installer : ollama pull {cfg['model']}"
        )


def answer(history: list[dict], text: str, cfg: dict, toolbox: Toolbox) -> list[dict] | None:
    """Print the reply to `text` as it streams, with the tools it runs on the way."""
    return show(coach.repondre(history, text, cfg, toolbox))


def show(events: Iterator[tuple[str, object]]) -> list[dict] | None:
    """Print the events of coach.repondre as they come.

    Returns the turn's messages (user, tool calls and results, final answer), or None if it failed or was cut.
    """
    turn, stats, thinking, line = None, None, False, ""
    try:
        with closing(events) as events:  # closing stops Ollama's generation
            for kind, data in events:
                if kind == "thinking" and not thinking:
                    thinking = True
                    note("[réflexion…]")
                elif kind == "token":
                    line += data
                    print(data, end="", flush=True)
                elif kind == "question":
                    if line:
                        print()
                    line = ""
                    print(f"\n{data['question']}")
                    for number, choice in enumerate(data["choix"], 1):
                        print(f"  {number}. {choice}")
                    note("(réponds par un numéro, ou écris ta réponse)")
                elif kind == "outil":
                    if line:
                        print()
                    thinking, line = False, ""
                    name, arguments = data
                    note(f"[outil] {name}({json.dumps(arguments, ensure_ascii=False)})")
                elif kind == "fin":
                    turn, stats = data
    except LLMError as e:
        print()  # end a half-printed answer's line
        fail(str(e))
        return None
    except KeyboardInterrupt:
        print("\n(interrompu)")
        return None
    if not turn[-1]["content"]:
        fail("le modèle n'a rien répondu.")
        return None
    speed = f" · {stats['tok_s']} tok/s" if stats and stats["tok_s"] else ""
    print("\n" + style(f"({stats['tokens'] if stats else '?'} tokens{speed})", DIM, sys.stdout))
    return turn


def read_line() -> str | None:
    """The next line typed, stripped; None at the end of the input (Ctrl-D). Ctrl-C asks again."""
    while True:
        try:
            return input("> ").strip()
        except EOFError:
            print()
            return None
        except KeyboardInterrupt:
            print("\n(Ctrl-D ou /quit pour quitter)")


def list_tools(toolbox: Toolbox) -> None:
    for spec in toolbox.specs:
        print(f"- {spec['function']['name']} ({toolbox.routes[spec['function']['name']].name})")
    if not toolbox.specs:
        print("Aucun outil.")


def chat_loop(cfg: dict, toolbox: Toolbox) -> int:
    history: list[dict] = []  # replaced, never edited in place
    tools = f" · {len(toolbox.specs)} outils (/tools)" if toolbox.specs else ""
    print(f"SensAI · {cfg['model']}{tools} · /reset : oublier la conversation · /quit : quitter")
    while True:
        text = read_line()
        if text is None:
            return 0
        if not text:
            print("Message vide : écris quelque chose.")
        elif text in ("/quit", "/exit"):
            return 0
        elif text == "/reset":
            history = []
            print("Conversation oubliée.")
        elif text == "/tools":
            list_tools(toolbox)
        elif (turn := answer(history, with_context(text, history), cfg, toolbox)) is not None:
            history = trim([*history, *turn], cfg)


def ask_level(session: trainer.Session) -> bool:
    """Ask the level until the answer is one, by number or in plain words; False if the player leaves instead."""
    print("Quel est ton niveau au poker ? (un numéro, ou dis-le avec tes mots)")
    for number, label in enumerate(trainer.NIVEAUX.values(), 1):
        print(f"  {number}. {label}")
    while True:
        text = read_line()
        if text is None or text in ("/quit", "/exit"):
            return False
        try:
            session.choisir_niveau(text)
            return True
        except ValueError:
            pass
        if text.isdigit():
            print(f"Réponds par un numéro de 1 à {len(trainer.NIVEAUX)}.")
            continue
        note("[classement de ta réponse…]")
        try:
            level = session.niveau_libre(text)
        except (ValueError, LLMError):
            print(f"Je n'ai pas compris. Réponds par un numéro de 1 à {len(trainer.NIVEAUX)}.")
            continue
        print(f"Niveau retenu : {trainer.NIVEAUX[level['niveau']]}. {level['raison']}")
        return True


def choices(situation: dict) -> str:
    return "   ".join(f"[{KEYS[a]}] {generation.LIBELLES[a]}" for a in situation["actions"])


def deal(session: trainer.Session) -> None:
    situation = session.nouvelle_situation()
    print(f"\nSituation {session.numero} · {generation.decrire(situation)}")
    print(f"{generation.QUESTIONS.get(situation['theme'], 'Que fais-tu ?')}  {choices(situation)}")


def or_list(actions: list[str]) -> str:
    return " ou ".join(generation.LIBELLES[a] for a in actions)


def decide(session: trainer.Session, text: str) -> None:
    """Grade the action of the key typed, then show the reference it was graded against."""
    action = {KEYS[a]: a for a in session.situation["actions"]}.get(text.lower())
    if action is None:
        print(f"Choisis une action : {choices(session.situation)}")
        return
    verdict = session.decider(action)
    reference = session.situation["reference"]
    if verdict == "bon":
        print(f"{ICONS[verdict]} Bon : {generation.LIBELLES[action]}, c'est la bonne réponse.")
    elif verdict == "acceptable":
        print(f"{ICONS[verdict]} Acceptable : situation limite, {or_list(reference['acceptables'])} se défendent.")
    else:
        best = reference["bonnes"] or reference["acceptables"]
        print(f"{ICONS[verdict]} Erreur : la bonne réponse était {or_list(best)}.")
    for fact in reference["faits"]:
        print(f"- {fact}")
    note("Pose tes questions au coach · /fiche : ce qu'il faut retenir · /exercice : situation suivante")


def greet(profil: dict) -> None:
    """Welcome back a known player: level, themes to work on, how to resume."""
    done = profils.nombre_exercices(profil)
    print(f"Re-bonjour {profil['pseudo']} · niveau : {trainer.NIVEAUX[profil['niveau']]} (/niveau pour changer)")
    print(f"{done} exercice{'s' if done > 1 else ''} fait{'s' if done > 1 else ''} jusqu'ici.")
    if weak := profils.themes_faibles(profil):
        print(f"Thèmes à revoir : {', '.join(weak)}. Ils reviendront plus souvent.")
    if profil["dernier_debrief"]:
        note("/reprendre : reprendre le dernier débrief")


def resume(session: trainer.Session) -> None:
    """Show the debrief brought back from the profile: the situation, the decision and the last answer."""
    try:
        last = session.reprendre()
    except ValueError as e:
        print(f"Rien à reprendre : {e}.")
        return
    print(f"\nDernière situation · {generation.decrire(last['situation'])}")
    print(f"Ta décision : {generation.LIBELLES[last['action']]} ({ICONS[last['verdict']]} {last['verdict']}).")
    answers = [m["content"] for m in last["debrief"] if m["role"] == "assistant" and m["content"]]
    if answers:
        print(f"Coach : {answers[-1]}")
    note("Continue le débrief, ou /exercice pour une nouvelle situation")


def card(session: trainer.Session) -> None:
    """Print the end-of-exercise card written by the model."""
    note("[fiche de fin d'exercice…]")
    try:
        fiche = session.ecrire_fiche()
    except (ValueError, LLMError) as e:
        print(f"Fiche impossible : {e}.")
        return
    print(f"À retenir : {fiche['a_retenir']}")
    print(f"Thème à revoir : {fiche['theme_a_revoir']}")


def trainer_loop(cfg: dict, toolbox: Toolbox, rng: random.Random | None = None, profil: dict | None = None) -> int:
    session = trainer.Session(cfg, toolbox, rng, profil)
    tools = f" · {len(toolbox.specs)} outils (/tools)" if toolbox.specs else ""
    print(f"SensAI · {cfg['model']}{tools} · /exercice · /fiche · /niveau · /reprendre · /reset · /quit")
    if session.niveau:
        greet(session.profil)
    elif not ask_level(session):
        return 0
    deal(session)
    while True:
        text = read_line()
        if text is None or text in ("/quit", "/exit"):
            return 0
        if not text:
            print("Message vide : écris quelque chose.")
        elif text == "/tools":
            list_tools(toolbox)
        elif text == "/exercice":
            deal(session)
        elif text == "/niveau":
            if not ask_level(session):
                return 0
            deal(session)
        elif text == "/reprendre":
            resume(session)
        elif text == "/fiche":
            card(session)
        elif text == "/reset":
            session.oublier()
            print("Débrief oublié.")
        elif session.action is None:
            decide(session, text)
        else:
            show(session.discuter(session.reponse(text)))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="SensAI : entraîneur de poker en ligne de commande, avec un modèle Ollama local")
    ap.add_argument("--model", help="modèle à utiliser (sinon celui de la config)")
    ap.add_argument("--config", default=str(ROOT / "config.json"), help="fichier de configuration (défaut : config.json)")
    ap.add_argument("--no-tools", action="store_true", help="ne lancer aucun serveur MCP")
    ap.add_argument("--seed", type=int, help="graine du tirage des situations, pour rejouer la même session")
    ap.add_argument("--pseudo", help="garder le niveau et les résultats dans profiles/<pseudo>.json")
    ap.add_argument("--libre", action="store_true", help="chat libre avec le modèle, sans le parcours d'exercices")
    args = ap.parse_args()
    try:
        if args.pseudo:
            profils.valider_pseudo(args.pseudo)
    except ValueError as e:
        fail(str(e))
        return 1

    try:
        cfg = load_config(args.config)
        if args.model:
            cfg = {**cfg, "model": args.model}
        profil = profils.charger(args.pseudo, cfg) if args.pseudo else None
        ensure_model(cfg)
    except (OSError, ValueError, KeyError) as e:
        fail(f"Configuration illisible ({args.config}) : {e!r}")
        return 1
    except LLMError as e:
        fail(str(e))
        return 1

    toolbox = Toolbox({} if args.no_tools else cfg.get("mcp_servers", {}))
    try:
        for warning in toolbox.warnings:  # a broken tool server must not stop the chat
            fail(f"outils indisponibles, {warning}")
        cfg = {**cfg, "tools": toolbox.specs}
        if args.libre:
            system = f"{cfg['system_prompt']}\n\n{ai.hand_rankings_context()}"
            return chat_loop({**cfg, "system_prompt": system}, toolbox)
        return trainer_loop(cfg, toolbox, random.Random(args.seed), profil)
    finally:
        toolbox.close()


if __name__ == "__main__":
    sys.exit(main())

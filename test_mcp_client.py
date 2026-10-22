"""MCP client checks against the real poker server, started as a subprocess. Run: python3 test_mcp_client.py"""
import sys
import threading

from mcp_client import Toolbox

POKER = {"poker": {"command": [sys.executable, "mcp_server.py"]}}


def test_threads_sharing_a_server_each_get_their_own_answer():
    hands = ["K9s", "72o", "AA", "QJo"] * 5
    toolbox = Toolbox(POKER)
    answers = {}

    def ask(i, hand):
        answers[i] = toolbox.call("preflop_open", {"hand": hand})

    try:
        threads = [threading.Thread(target=ask, args=(i, hand)) for i, hand in enumerate(hands)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        alone = {hand: toolbox.call("preflop_open", {"hand": hand}) for hand in set(hands)}
    finally:
        toolbox.close()
    assert all(answers[i] == alone[hand] for i, hand in enumerate(hands))   # no answer went to the wrong call


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)

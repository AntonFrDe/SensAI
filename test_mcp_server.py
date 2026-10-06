"""MCP server protocol checks, no subprocess needed. Run: python3 test_mcp_server.py"""
import mcp_server


def call(method, params=None, msg_id=1):
    return mcp_server.handle({"jsonrpc": "2.0", "id": msg_id, "method": method, "params": params or {}})


def test_initialize_answers_with_a_version_both_sides_speak():
    assert call("initialize", {"protocolVersion": "2025-03-26"})["result"]["protocolVersion"] == "2025-03-26"
    result = call("initialize", {"protocolVersion": "1999-01-01"})["result"]
    assert result["protocolVersion"] == mcp_server.PROTOCOL_VERSIONS[0] and "tools" in result["capabilities"]


def test_notifications_get_no_answer():
    assert mcp_server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}) is None


def test_every_tool_has_a_schema_and_unknown_things_are_json_rpc_errors():
    tools = call("tools/list")["result"]["tools"]
    assert all(t["inputSchema"]["type"] == "object" and t["description"] for t in tools)
    assert call("tools/call", {"name": "nope"})["error"]["code"] == -32602
    assert call("resources/list")["error"]["code"] == -32601


def test_bad_arguments_are_a_tool_error_the_model_can_read():
    result = call("tools/call", {"name": "preflop_open", "arguments": {"hand": "ZZ"}})["result"]
    assert result["isError"] and "Arguments invalides" in result["content"][0]["text"]
    assert call("tools/call", {"name": "define_term", "arguments": {"term": "check-raise"}})["result"]["isError"] is False


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
            print("ok", name)

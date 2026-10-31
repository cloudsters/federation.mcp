"""mcp_http.py — the transport of federation.mcp: MCP's Streamable HTTP, JSON-RPC over POST, answered with JSON.

It hands every call to the released pipeline, `serve_mcp.call` of the installed Commons Essentials, and adds nothing to
its semantics: the grant, the cut, the envelope and the offer are serve_mcp's (mcp R1, R2, R22, R28). Pure Python, so
the same code runs in the Worker and in a local test.

What it does not do yet: sign-in. It reads no token, so every caller is no user and holds ROAM's `public` grant (R3),
which is what R24 asks of federation.mcp; a shell further in waits for the protocol's authorisation (R22).
"""
import base64
import io
import json
import os
import sys
import tempfile
import zipfile

import core_bundle

CORE = os.path.join(tempfile.gettempdir(), "federation-mcp", "core")       # the served CORE, unpacked at start
STATE = os.path.join(tempfile.gettempdir(), "federation-mcp", "state")
TOOLS = os.path.join(CORE, "extensions", "commons-engineering", "commons-essentials", "specs", "tools")
PATH = "/federation"
VERSIONS = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]   # the protocol revisions it answers, newest first


def restore():
    """unpack the served CORE that deploy/build.py packed, once per instance, into its memory"""
    if not os.path.isdir(CORE):
        zipfile.ZipFile(io.BytesIO(base64.b64decode(core_bundle.ZIP))).extractall(CORE)


restore()
sys.path.insert(0, TOOLS)

import answer_graph  # noqa: E402
import serve_mcp  # noqa: E402

# The served CORE is a bundle, not a git checkout: the reader then reads the working files and stamps `read_at`, as it
# does wherever git is absent. A Worker cannot start a process, so git is not asked.
answer_graph.git = lambda *a, **k: None

SPECS = {
    "answer": ("Answer a question from the canon of the Commons, within the caller's cut (mcp R2).",
               {"question": {"type": "string", "description": "context and problem, in plain words"}}, ["question"]),
    "node": ("One node of the graph by its id, with its relations, within the caller's cut (mcp R2).",
             {"id": {"type": "string", "description": "a node id, e.g. `mcp#R24`"}}, ["id"]),
    "propose": ("Propose a change as one item on a board (mcp R12). At ROAM nothing may be written, so it is refused.",
                {k: {"type": "string"} for k in sorted(serve_mcp.PAYLOAD)}, ["text"]),
}


def tools():
    return [{"name": n, "description": d, "inputSchema": {"type": "object", "properties": p, "required": r}}
            for n, (d, p, r) in SPECS.items()]


def result(i, r):
    return {"jsonrpc": "2.0", "id": i, "result": r}


def error(i, code, msg):
    return {"jsonrpc": "2.0", "id": i, "error": {"code": code, "message": msg}}


def rpc(m):
    """one JSON-RPC message; None for a notification"""
    if not isinstance(m, dict) or m.get("jsonrpc") != "2.0" or not isinstance(m.get("method"), str):
        return error(m.get("id") if isinstance(m, dict) else None, -32600, "not a JSON-RPC 2.0 request")
    i, method, p = m.get("id"), m["method"], m.get("params") or {}
    if "id" not in m:
        return None
    if method == "initialize":
        asked = p.get("protocolVersion")
        return result(i, {"protocolVersion": asked if asked in VERSIONS else VERSIONS[0],
                          "capabilities": {"tools": {"listChanged": False}},
                          "serverInfo": {"name": "federation.mcp", "version": "commons-essentials 0.2.0"},
                          "instructions": "The Federation's MCP: the canon of the Commons at ROAM, free, with no named user. "
                                          "Every envelope carries the offer per shell (mcp R24, R28)."})
    if method == "ping":
        return result(i, {})
    if method == "tools/list":
        return result(i, {"tools": tools()})
    if method == "tools/call":
        name, args = p.get("name"), p.get("arguments") or {}
        if name not in SPECS:
            return error(i, -32602, f"`{name}` is no tool of this MCP")
        env = serve_mcp.call(CORE, "", name, {k: str(v) for k, v in args.items()}, STATE)
        return result(i, {"content": [{"type": "text", "text": json.dumps(env, ensure_ascii=False)}],
                          "structuredContent": env, "isError": "refused" in env})
    return error(i, -32601, f"`{method}` is not served")


def handle(method, path, body):
    """an HTTP request at the route; returns (status, headers, text)"""
    js = {"Content-Type": "application/json"}
    if path.rstrip("/") != PATH:
        return 404, js, json.dumps({"error": "not found"})
    if method != "POST":
        return 405, {**js, "Allow": "POST"}, json.dumps({"error": "POST a JSON-RPC message"})
    try:
        m = json.loads(body or "")
    except ValueError:
        return 400, js, json.dumps(error(None, -32700, "not JSON"))
    if isinstance(m, list):
        return 400, js, json.dumps(error(None, -32600, "one message per request"))
    out = rpc(m)
    return (202, {}, "") if out is None else (200, js, json.dumps(out, ensure_ascii=False))

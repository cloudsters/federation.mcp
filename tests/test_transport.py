#!/usr/bin/env python3
"""test_transport.py — the Worker's transport over the built CORE, in CPython: the calls a session makes, and what
each must give. Run after deploy/build.py:  python -B tests/test_transport.py"""
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "worker", "src"))
shutil.rmtree(os.path.join(tempfile.gettempdir(), "federation-mcp"), ignore_errors=True)
import mcp_http  # noqa: E402

FAIL = []


def post(m):
    s, _, b = mcp_http.handle("POST", "/federation", json.dumps(m))
    return s, json.loads(b) if b else None


def call(i, name, args):
    s, r = post({"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": name, "arguments": args}})
    return r["result"]


def expect(what, ok):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        FAIL.append(what)


s, r = post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}}})
expect("initialize answers the revision asked", s == 200 and r["result"]["protocolVersion"] == "2025-06-18")
expect("a notification is accepted with 202", mcp_http.handle("POST", "/federation", '{"jsonrpc":"2.0","method":"notifications/initialized"}')[0] == 202)
s, r = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
expect("three tools: answer, node, propose", [t["name"] for t in r["result"]["tools"]] == ["answer", "node", "propose"])
env = call(3, "answer", {"question": "who may read the canon without signing in"})["structuredContent"]
expect("answer: a caller with no sign-in holds the public grant at ROAM", env.get("grant") == "public")
expect("answer: candidates from the canon", bool(env.get("answer", {}).get("candidates")))
expect("answer: the envelope carries the offer of every shell (R28)", set(env.get("offer") or {}) >= {"SEED", "CORE", "PEER", "OPEN", "DOCK", "ROAM"})
expect("answer: ROAM reads public only", (env.get("gets") or {}).get("reads") == ["public"])
env = call(4, "node", {"id": "mcp#R24"})["structuredContent"]
expect("node: mcp#R24 is found", (env.get("node") or {}).get("id") == "mcp#R24")
r = call(5, "propose", {"text": "a proposal"})
expect("propose: refused at ROAM, nothing written", r["isError"] and "refused" in r["structuredContent"])
expect("GET is 405, another path 404", mcp_http.handle("GET", "/federation", "")[0] == 405 and mcp_http.handle("POST", "/x", "{}")[0] == 404)
print(f"# transport: {len(FAIL)} fail")
sys.exit(1 if FAIL else 0)

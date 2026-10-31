#!/usr/bin/env python3
"""check_mcp.py — a commons' MCP serves each caller within its grant and says what it rests on (mcp.md). Read-only on
the CORE: the reference pipeline reads it in place and keeps its operational state in a temporary folder.

Reports each finding as fail (a MUST), should (a SHOULD) or gap (missing or unverifiable, not wrong), and exits with
1 only on a fail. The check ids are those of mcp.md part 6:

  access  pipeline  projection  envelope  budget  write  state  setup

`access` reads `.commons/access.yml` against the graph's register: every class CORE's or further out, every user in
one shell and no wider than it, and every technical user and entry by pattern no wider than the human accountable for
it. The others run serve_mcp.py as every user of `access.yml`, as an account each entry by pattern admits, and as a
caller that is no user, each call in a period of its own: an answer to one question, nodes of the caller's cut and their edges, a node of a source the
caller may not see beside one that does not exist, a write sent twice by one user and once by another of the same
shell under the same request id, the use records the calls left, and the teams and ruleset the set-up generates.

Usage:  check_mcp.py CORE [--question TEXT] [--today YYYY-MM-DD]
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import tempfile

import jsonschema

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answer_graph  # noqa: E402
import serve_mcp  # noqa: E402
from check_core import Report  # noqa: E402

SCHEMA = json.load(open(os.path.join(HERE, "..", "schemas", "mcp.schema.json"), encoding="utf-8"))
GRAPH = json.load(open(os.path.join(HERE, "..", "schemas", "graph.schema.json"), encoding="utf-8"))
SPECS = {"mcp": ["access", "pipeline", "projection", "envelope", "budget", "write", "state", "setup"]}


def errors(sch, doc):
    return [f"{'/'.join(str(p) for p in e.path) or 'root'}: {e.message}" for e in jsonschema.Draft202012Validator(sch).iter_errors(doc)]


def of(name, schema=SCHEMA):
    return {**schema["$defs"][name], "$defs": schema["$defs"]}


def check_access(r, core, acc, today):
    for e in errors(SCHEMA, acc):
        r.fail("access", f"`.commons/access.yml`: {e} (R3, R4, R24, R27)")
    if not acc.get("federation"):
        r.fail("access", "`access.yml` does not name `federation.mcp` (R24)")
    classes = serve_mcp.classes_of(acc)
    if classes.get("public") != "ROAM":
        r.fail("access", f"the class `public` is everyone's, ROAM's, and `access.yml` maps it to {classes.get('public')} (R4)")
    for c in sorted(c for c, s in classes.items() if s == "SEED"):
        r.fail("access", f"the class `{c}` is SEED's alone; SEED and CORE read the whole repository, so a class is CORE's or further out (R4)")
    for e in answer_graph.register_of(core):
        if e["class"] not in classes:
            r.fail("access", f"the source `{e['id']}` has the class `{e['class']}`, which `access.yml` maps to no shell (R4)")
    seen = [str(u.get("account") or u.get("match", "")).lower() for u in serve_mcp.users_of(acc)]
    for x in sorted({x for x in seen if seen.count(x) > 1}):
        r.fail("access", f"`{x}` stands more than once; a user, or a domain, belongs to one entry (R3, R27)")
    for u in serve_mcp.users_of(acc):
        name = u.get("account") or u.get("match")
        if u.get("expires") is not None and serve_mcp.day(u["expires"]) is None:
            r.fail("access", f"`{name}` expires on `{u['expires']}`, which is no calendar date (R3, R27)")
            continue
        if serve_mcp.expired(u, today):
            r.gap("access", f"`{name}` expired on {u['expires']} and grants nothing (R3)")
            continue
        why = serve_mcp.standing(acc, u, today)
        if why and "grants nothing now" in why:
            r.gap("access", f"`{name}`: {why} (R3)")
        elif why:
            r.fail("access", f"`{name}`: {why} (R3, R27)")


def check_setup(r, acc, today):
    """the generated teams hold each platform account that grants something in its shell's team and in no other, and
    no key or entry by pattern; each repository's ruleset lets only its inner shell's team, or one further in, merge
    into `main`, by a pull request whose checks have passed and with no exception, and SEED's team has someone in it
    (R26)"""
    gen = serve_mcp.setup(acc, today)
    t, repos = gen["teams"], gen["repositories"]
    members = [a for m in t.values() for a in m]
    for a in sorted({a for a in members if members.count(a) > 1}):
        r.fail("setup", f"`{a}` is in more than one team (R26)")
    want = {}
    for u in serve_mcp.users_of(acc):
        a = str(u.get("account", ""))
        if a.startswith("account:") and u["shell"] in serve_mcp.SHELLS[:4] and not serve_mcp.expired(u, today) and not serve_mcp.standing(acc, u, today):
            want.setdefault(u["shell"], set()).add(a.split(":", 1)[1])
    if {s: set(m) for s, m in t.items()} != want:
        r.fail("setup", "the teams differ from the users of `access.yml` and their shells (R26)")
    if set(repos) != {f"{i}|{o}" for i, o in serve_mcp.PAIRS}:
        r.fail("setup", "the set-up does not generate one ruleset per pair of shells, SEED|CORE and PEER|OPEN (R26)")
    for name, rules in repos.items():
        inner, outer = name.split("|")
        if (rules.get("branch"), rules.get("change"), rules.get("bypass")) != ("main", "pull request", "none") or not rules.get("checks") \
                or rules.get("merge") != serve_mcp.SHELLS[:serve_mcp.SHELLS.index(inner) + 1] or outer not in (rules.get("push") or []):
            r.fail("setup", f"the ruleset of {name} does not keep `main` to pull requests, with no exception, that {inner} or a shell "
                            f"further in merges once the checks have passed, {outer} pushing branches (R26)")
    if not t.get("SEED"):
        r.fail("setup", "SEED's team is empty, and nobody may merge into `main` (R26)")


def ends(edge):
    """the two node ids of an edge as `show()` prints it: `<from> -<kind>-> <to> (...)`"""
    head, _, tail = edge.partition("-> ")
    return head.rsplit(" -", 1)[0], tail.split(" (", 1)[0]


def check(core, question=None, today=None):
    r = Report()
    today = today or datetime.date.today().isoformat()
    acc = serve_mcp.access_of(core)
    if acc is None:
        r.gap("access", "no `.commons/access.yml`: the MCP serves nothing (R3)")
        return r
    check_access(r, core, acc, today)
    if any(o == "fail" for o, c, _ in r.items if c == "access"):
        return r
    check_setup(r, acc, today)
    full = answer_graph.read(core)
    source_of = {n: v["source"] for n, v in full.nodes.items()}
    register = {e["id"]: e for e in full.register}
    if not question:
        question = " ".join(str(v.get("text") or "")[:60] for v in list(full.nodes.values())[:3]) or "what"
    tmp = tempfile.mkdtemp(prefix="check_mcp-")
    try:
        state = os.path.join(tmp, "state")
        clock = [datetime.datetime.fromisoformat(f"{today}T00:00:00+00:00")]

        def run(who, tool, args, at=None):
            clock[0] += datetime.timedelta(hours=1)  # each probe in a period of its own: a small budget never starves them (R8)
            return serve_mcp.call(core, who, tool, args, state, today, now=clock[0], address=at)

        callers = []
        for u in serve_mcp.users_of(acc):
            if not serve_mcp.expired(u, today) and not serve_mcp.standing(acc, u, today):
                who, at = (u["account"], None) if u.get("account") else ("account:check-partner", "check" + u["match"][1:])
                callers.append((who, at, {"id": u["shell"], "user": who, **serve_mcp.grant_of(acc, u)}))
        pub = acc.get("public", "none")                # an opened public cut is checked like any grant (R3, R6)
        callers.append(("", None, {"id": "public", "shell": "ROAM", "user": None, **pub, "writes": []} if isinstance(pub, dict) else None))
        accounts = {a for a, _, _ in callers if a}
        envs = []
        for who, at, g in callers:
            cid = who or "a caller that is no user"
            env = run(who, "answer", {"question": question}, at)
            envs.append((cid, env))
            if g is None:
                if acc.get("public", "none") == "none" and not env.get("refused"):
                    r.fail("pipeline", "a caller that is no user was served, and nothing is public (R3)")
                continue
            if set(env.get("offer") or {}) != set(serve_mcp.SHELLS) or (env.get("gets") or {}).get("reads") != serve_mcp.visible(acc, g["shell"]):
                r.fail("envelope", f"as `{cid}`: the envelope does not carry the offer of every shell and what this caller gets (R28)")
            ans = env.get("answer")
            if ans is None:
                r.fail("pipeline", f"as `{cid}`: no answer: {env.get('refused')} (R2)")
                continue
            for e in errors(of("answer", GRAPH), ans):
                r.fail("envelope", f"as `{cid}`: the answer: {e} (R7; graph R12)")
            allowed = {s for s, e in register.items() if e["class"] in serve_mcp.visible(acc, g["shell"])
                       and (not g.get("sources") or s in g["sources"])}
            shown = {c["source"] for c in ans["cut"]} | {source_of.get(c["id"]) for c in ans["candidates"]} - {None}
            for s in sorted(shown - allowed):
                r.fail("projection", f"as `{cid}`: the answer shows the source `{s}`, which its grant does not see (R6)")
            if allowed < set(register) and not ans["silences"]["unsighted"]:
                r.fail("projection", f"as `{cid}`: sources were withheld, and the answer does not say so (R6)")
            budget = serve_mcp.budget_of(acc, g)
            if len(ans["candidates"]) > budget["nodes"]:
                r.fail("budget", f"as `{cid}`: {len(ans['candidates'])} nodes in an answer, above its budget of {budget['nodes']} (R8)")
            for nid in sorted(n for n in source_of if source_of[n] in allowed):
                nd = run(who, "node", {"id": nid}, at).get("node") or {}
                if any(x in source_of and source_of[x] not in allowed for e in nd.get("edges") or [] for x in ends(e)):
                    r.fail("projection", f"as `{cid}`: `node {nid}` shows an edge to a node outside its grant (R6)")
                if len(nd.get("edges") or []) > budget["nodes"] or (budget["depth"] < 1 and nd.get("edges")):
                    r.fail("budget", f"as `{cid}`: `node {nid}` shows more edges than its budget allows (R8)")
            hidden = sorted(n for n, s in source_of.items() if s not in allowed)
            if hidden:
                a, b = (run(who, "node", {"id": i}, at) for i in (hidden[0], "no-such:node"))
                envs += [(cid, a), (cid, b)]
                if {**a.get("node", {}), "id": ""} != {**b.get("node", {}), "id": ""}:
                    r.fail("projection", f"as `{cid}`: a withheld node is answered otherwise than a missing one (R6)")
        writers = [(w, g) for w, at, g in callers if g and at is None and "commons" in g["writes"]]
        pair = next(((x, y) for x in writers for y in writers if x[0] != y[0] and x[1]["shell"] == y[1]["shell"]), None)
        if not writers:
            r.gap("write", "no user may write a proposal; the writes are untested (R12)")
        else:
            one_w, g = pair[0] if pair else writers[0]
            args = {"to": "commons", "anchor": "graph", "scope": "a check", "text": "a proposal sent twice", "request": "check-1"}
            w = lambda who, a: run(who, "propose", a)
            one, two = w(one_w, args), w(one_w, args)
            reuse = w(one_w, {**args, "text": "another operation"})
            forged = w(one_w, {**args, "request": "check-3", "state": "accepted"})
            envs += [(one_w, x) for x in (one, two, reuse, forged)]
            if not one.get("receipt") or one.get("receipt") != two.get("receipt"):
                r.fail("write", "a proposal sent twice by one user with one request id did not return one receipt (R13)")
            if pair:
                other = w(pair[1][0], {**args, "text": "another user's proposal"})
                envs.append((pair[1][0], other))
                items = os.listdir(os.path.join(state, "outbox")) if os.path.isdir(os.path.join(state, "outbox")) else []
                if not other.get("receipt") or other.get("receipt") == one.get("receipt") or len(items) != 2:
                    r.fail("write", "two users of one shell under one request id did not get an item each (R13)")
            else:
                r.gap("write", "no shell has two users who may write; that two are never one is untested (R13)")
            if not reuse.get("refused"):
                r.fail("write", "a request id its user reused for another operation was not refused (R13)")
            if not forged.get("refused"):
                r.fail("write", "a write carrying `state`, a field the server builds, was not refused (R12)")
            if (one.get("receipt") or {}).get("state") != "sent":
                r.fail("write", "a new receipt is not `sent`; a write is `sent` until the board says more (R13)")
        narrow = next(((who, g) for who, at, g in callers if who and g and at is None and "model" not in g["writes"]), None)
        if narrow is not None:
            m = run(narrow[0], "propose", {"to": "model", "text": "x", "request": "check-4"})
            envs.append((narrow[0], m))
            if not m.get("refused"):
                r.fail("write", f"`{narrow[0]}` may not write to the Model Workshop, and a proposal there was taken (R12)")
        for cid, env in envs:
            for e in errors(of("envelope"), env):
                r.fail("envelope", f"as `{cid}`: {e} (R7)")
            if any(a in json.dumps(env) for a in accounts):
                r.fail("envelope", f"as `{cid}`: the result names a user; it names the grant by its shell (R7)")
        uses = [json.loads(l) for l in open(os.path.join(state, "use.jsonl"), encoding="utf-8") if l.strip()]
        for u in uses:
            for e in errors(of("use"), u):
                r.fail("state", f"a use record: {e} (R21)")
            if any(a in json.dumps(u) for a in accounts) or question in json.dumps(u):
                r.fail("state", "a use record names a user or the question (R21)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return r


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("core")
    ap.add_argument("--question")
    ap.add_argument("--today")
    a = ap.parse_args()
    r = check(a.core, a.question, a.today)
    n = {o: sum(1 for i in r.items if i[0] == o) for o in ("fail", "should", "gap")}
    print(f"# {a.core}: {n['fail']} fail · {n['should']} should · {n['gap']} gap")
    for o, c, t in r.items:
        print(f"{o}: {c}: {t}")
    return 1 if n["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""propose_adoption.py — selecting a value stream prepares one coherent adoption proposal (extension.md R34).

The proposal holds, from the installed release of the commons' primary extension:
- **required:** the stream, the capabilities its steps bind with their parent chain up to L0, and the entities its
  steps reference;
- **reused:** what of that the commons already holds, by its origin or by its slug, so that nothing is adopted twice;
- **optional:** what the stream relates to without binding it: journeys that mirror it, touchpoints on its steps,
  and the records its own fields refer to, as a kind's specification declares them (`x-refers`);
- **unresolved:** what the stream binds and the release does not offer.

A person accepts the package deliberately. `--accept` writes every required record that is not reused as the
commons' own complete record with `adopted_from`, and a `decision` event that names what was adopted, what was
reused and, under `open`, every required record left open on purpose (`--open`) and every unresolved binding, so
that a dependency left open stays visible (check_extension `adopt`). Optional records are adopted only when named
with `--with`. Nothing is written into a record the commons already holds.

Usage:  propose_adoption.py CORE STREAM [--with kind:slug ...] [--open kind:slug ...] [--accept --by person:P_nnnn]
"""
import argparse
import copy
import datetime
import glob
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_model  # noqa: E402

FOLDER = {"value-stream": "value-streams", "capability": "capabilities", "entity": "entities", "stakeholder": "stakeholders",
          "journey": "journeys", "touchpoint": "touchpoints", "value-exchange": "value-exchanges", "solution": "solutions",
          "body": "bodies", "post": "posts"}


def yml(p):
    return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def dump(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(d, f, sort_keys=False, allow_unicode=True, width=120)


def records(reg):
    out = {}
    for f in sorted(glob.glob(os.path.join(reg, "*", "*.y*ml"))):
        rec = yml(f) or {}
        if isinstance(rec, dict) and rec.get("kind") and rec.get("slug"):
            out[f"{rec['kind']}:{rec['slug']}"] = rec
    return out


def declared(root):
    out = {}
    for p in glob.glob(os.path.join(root, "**", "*.schema.json"), recursive=True):
        for kind, d in (json.load(open(p, encoding="utf-8")).get("$defs") or {}).items():
            if isinstance(d, dict) and isinstance(d.get("x-refers"), dict):
                out.setdefault(kind, {}).update(d["x-refers"])
    return out


def proposal(core, stream):
    cfg = yml(os.path.join(core, ".commons", "commons.yml")) or {}
    prim = next((x for x in cfg.get("extensions") or [] if isinstance(x, dict) and x.get("primary") and "/" in str(x.get("id"))), None)
    if prim is None:
        sys.exit("the CORE pins no extension of its kind as its primary")
    ref, version = prim["id"], str(prim["version"])
    at = os.path.join(core, "extensions", *ref.split("/"))
    offered, local = records(os.path.join(at, "registry")), records(os.path.join(core, "registry"))
    origins = {str(r.get("adopted_from")).split("#", 1)[1]: k for k, r in local.items() if r.get("adopted_from") and "#" in str(r.get("adopted_from"))}
    key = f"value-stream:{stream}"
    if key not in offered:
        sys.exit(f"`{ref}@{version}` offers no `{key}`")
    required, unresolved = [key], []

    def need(k):
        if k in required:
            return
        if k not in offered:
            if k not in unresolved:
                unresolved.append(k)
            return
        required.append(k)
        if k.startswith("capability:") and offered[k].get("parent"):
            need(f"capability:{offered[k]['parent']}")

    for st in offered[key].get("steps") or []:
        for c in st.get("capabilities") or []:
            need(f"capability:{c}")
        for e in st.get("entities") or []:
            need(f"entity:{e}")
    optional = []
    steps = {f"{stream}/{st.get('slug')}" for st in offered[key].get("steps") or []}
    for k, rec in offered.items():
        if k.startswith("journey:") and rec.get("mirrors") == stream:
            optional.append(k)
        if k.startswith("touchpoint:") and steps & set(rec.get("steps") or []):
            optional.append(k)
    for field, target in declared(at).get("value-stream", {}).items():
        for v in offered[key].get(field) or []:
            if f"{target}:{v}" in offered and f"{target}:{v}" not in optional:
                optional.append(f"{target}:{v}")
    # reused only where the commons holds a record adopted from that origin; an own record of the same kind and
    # slug, or a file in the record's place, is a collision for the commons to decide, never reused or overwritten
    reused = [k for k in required + optional if k in origins]

    def place(k):
        kind, slug = k.split(":", 1)
        return os.path.join(core, "registry", FOLDER[kind], f"{slug}.yml")
    collisions = [k for k in required + optional if k not in reused and (k in local or os.path.exists(place(k)))]
    declined = []
    for f in sorted(glob.glob(os.path.join(core, "lifecycle", "events", "*.y*ml"))):
        ev = yml(f) or {}
        if ev.get("kind") == "not-selected" and "#" in str(ev.get("archetype")):
            declined.append(str(ev["archetype"]).split("#", 1)[1])
    declined = [k for k in required if k in declined and k not in reused]
    return {"extension": f"{ref}@{version}", "stream": key,
            "required": [k for k in required if k not in reused and k not in declined], "reused": reused,
            "declined": declined, "optional": [k for k in optional if k not in reused],
            "collisions": collisions, "unresolved": unresolved}, offered, at


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("core")
    ap.add_argument("stream")
    ap.add_argument("--with", dest="with_", nargs="*", default=[])
    ap.add_argument("--open", nargs="*", default=[])
    ap.add_argument("--accept", action="store_true")
    ap.add_argument("--by")
    a = ap.parse_args()
    p, offered, _ = proposal(a.core, a.stream)
    for k in a.open:
        if k not in p["required"]:
            sys.exit(f"`{k}` is not a required record of this proposal")
    for k in a.with_:
        if k not in p["optional"]:
            sys.exit(f"`{k}` is not an optional record of this proposal")
    print(yaml.safe_dump(p, sort_keys=False, allow_unicode=True, width=120), end="")
    if not a.accept:
        return 0
    if not a.by:
        sys.exit("--accept needs --by: a person accepts the package")
    take = [k for k in p["required"] if k not in a.open] + list(a.with_)
    day = datetime.date.today().isoformat()
    # preflight: every target, and the event, before anything is written; all or nothing, the event last
    clash = [k for k in take if k in p["collisions"]]
    if clash:
        print(f"# nothing written: {', '.join(clash)} collide with what the commons holds; decide them first "
              f"(adopt under another slug, or leave them open with --open)")
        return 2
    writes = []
    for k in take:
        rec = copy.deepcopy(offered[k])
        rec.pop("start", None)
        rec["adopted_from"] = f"{p['extension']}#{k}"
        kind, slug = k.split(":", 1)
        writes.append((os.path.join(a.core, "registry", FOLDER[kind], f"{slug}.yml"), rec))
    event_path = os.path.join(a.core, "lifecycle", "events", f"{day}-adopt-{a.stream}.yml")
    taken = [t for t, _ in writes if os.path.exists(t)] + ([event_path] if os.path.exists(event_path) else [])
    if taken:
        print(f"# nothing written: {', '.join(os.path.relpath(t, a.core) for t in taken)} exist")
        return 2
    for target, rec in writes:
        dump(target, rec)
    ev = {"id": f"{day}-adopt-{a.stream}", "date": day,
          "recorded": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
          "kind": "decision", "subject": "model",
          "decision": f"adopt {p['stream']} from {p['extension']} as one package",
          "title": f"The commons adopts the stream {a.stream} with what it binds",
          "by": [a.by], "adopted": take, "reused": p["reused"], "open": list(a.open) + p["declined"] + p["unresolved"]}
    dump(os.path.join(a.core, "lifecycle", "events", f"{ev['id']}.yml"), ev)
    print(f"# accepted: {len(take)} adopted, {len(p['reused'])} reused, {len(ev['open'])} open")
    return 0


if __name__ == "__main__":
    sys.exit(main())

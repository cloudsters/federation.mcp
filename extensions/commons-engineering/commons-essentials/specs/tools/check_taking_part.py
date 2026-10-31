#!/usr/bin/env python3
"""check_taking_part.py — Offices and taking part, as element 9 and the records of work state them. DRAFT.

Body D4 of Commons Engineering, 24 October 2026, for commons.o#81: OF.1–OF.4 (Holger), on D1's
`office-taking-part.md`. Read-only: it reports, it never writes.

  O1  an Office's steward is a human; its number is unique in the CORE and never 0          breach
  O2  a Post whose accountable has no Office is fine                                          —
  O3  an Office claims no mandate and lists no Posts                                          breach
  T1  every serving entry names `function`; an agent entry names `lineage`                   breach
      (a serving entry without `client` is reported)
  T2  one entry never executes and verifies the same work                                     breach
  T3  execute and verify of the same work from the same lineage                               reported
  T4  a record of work names handle, lineage and client                                       reported
  L   lineage and client are labels (`L1`, `C2`; `human` for a person), never names (OF.4)    breach

Serving entries are a Post's `held_by` and an Office's `served_by`. A record of work is any YAML file
given with --records that carries `executor:` and, where the work was checked, `verifier:` — each
{handle, lineage, client}. Legacy records with other executor shapes are reported under T4, not failed.

With --mapping (a local file outside git that maps labels to what they stand for: a name, or {name, model,
sessions} as check_lineage.py reads it), every mapped name or model
found in a record is a breach: it should have been a label. The mapping is read, never printed.

Usage:
    check_taking_part.py --registry DIR [--records PATH ...] [--mapping FILE]
Exit 0 when there is no breach (reports may remain), 1 otherwise.
"""
import argparse
import glob
import os
import re
import sys

import yaml

HUMAN = re.compile(r"^(github|party):")
LINEAGE = re.compile(r"^(L[1-9][0-9]*|human)$")
CLIENT = re.compile(r"^C[1-9][0-9]*$")
OFFICE = re.compile(r"^o([1-9][0-9]*)$")
FUNCTIONS = {"execute", "verify"}


def load(paths):
    out = []
    for p in paths:
        files = sorted(glob.glob(os.path.join(p, "**", "*.yml"), recursive=True)) if os.path.isdir(p) else [p]
        for f in files:
            try:
                doc = yaml.safe_load(open(f, encoding="utf-8"))
            except (OSError, yaml.YAMLError) as e:
                out.append((f, None, str(e)))
                continue
            out.append((f, doc, None))
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True, help="element 9's folder (registry/bodies/, or 9_bodies/)")
    ap.add_argument("--records", nargs="*", default=[], help="records of work: files or folders (e.g. operations/loops/_state/)")
    ap.add_argument("--mapping", help="local label mapping, outside git: {lineage: {L1: …}, client: {C1: …}}")
    a = ap.parse_args()

    breach, report = [], []
    name = lambda f: os.path.relpath(f, a.registry) if f.startswith(a.registry) else f

    reg = load([a.registry])
    offices = {}
    for f, doc, err in reg:
        if err or not isinstance(doc, dict):
            breach.append(f"{name(f)}: cannot read ({err or 'not a mapping'})")
            continue
        kind = doc.get("kind")
        if kind == "office":
            slug = str(doc.get("slug", ""))
            m = OFFICE.match(slug)
            if not m:
                breach.append(f"O1 {name(f)}: number '{slug}' is not o1, o2, … (there is no o0)")
            elif slug in offices:
                breach.append(f"O1 {name(f)}: number {slug} is already used by {offices[slug]}")
            offices.setdefault(slug, name(f))
            if not HUMAN.match(str(doc.get("steward", ""))):
                breach.append(f"O1 {name(f)}: steward '{doc.get('steward')}' does not resolve to a human")
            for key in ("mandate", "under", "posts", "serves"):
                if key in doc:
                    breach.append(f"O3 {name(f)}: an Office holds no `{key}`; its Posts are derived and its authority comes from their mandates")
            entries = doc.get("served_by") or []
        elif kind == "post":
            entries = doc.get("held_by") or []
        else:
            continue
        seen = {}
        lineages = {"execute": set(), "verify": set()}
        for i, e in enumerate(entries):
            if not isinstance(e, dict):
                continue
            where = f"{name(f)} {'served_by' if kind == 'office' else 'held_by'}[{i}] {e.get('id')}"
            if e.get("until"):
                continue                                       # an ended entry stays as history
            fn = e.get("function")
            if fn not in FUNCTIONS:
                breach.append(f"T1 {where}: no `function` (execute or verify)")
            lin = e.get("lineage", "human" if e.get("kind") == "human" else None)
            if e.get("kind") == "agent" and not e.get("lineage"):
                breach.append(f"T1 {where}: an agent entry names no `lineage`")
            elif lin and not LINEAGE.match(str(lin)):
                breach.append(f"L {where}: lineage '{lin}' is not a label (L1, L2 … or human)")
            if e.get("kind") == "agent" and not e.get("client"):
                report.append(f"T1 {where}: no `client`")
            elif e.get("client") and not CLIENT.match(str(e["client"])):
                breach.append(f"L {where}: client '{e['client']}' is not a label (C1, C2 …)")
            if fn in FUNCTIONS:
                if e.get("id") in seen and seen[e.get("id")] != fn:
                    breach.append(f"T2 {where}: the same entry both executes and verifies")
                seen[e.get("id")] = fn
                if lin:
                    lineages[fn].add(lin)
        shared = sorted((lineages["execute"] & lineages["verify"]) - {"human"})
        if shared:
            report.append(f"T3 {name(f)}: execute and verify share lineage {', '.join(shared)}")

    mapping = {}
    if a.mapping:
        m = yaml.safe_load(open(a.mapping, encoding="utf-8")) or {}
        for group in ("lineage", "client"):
            for label, real in (m.get(group) or {}).items():
                names = [real] if isinstance(real, str) else [v for k, v in (real or {}).items() if k in ("name", "model") and v]
                for n in names:
                    mapping[str(n).lower()] = f"{group} {label}"

    for f, doc, err in load(a.records):
        if err or not isinstance(doc, dict):
            report.append(f"T4 {f}: cannot read as a record ({err or 'not a mapping'})")
            continue
        ex, ve = doc.get("executor"), doc.get("verifier")
        if ex is None:
            continue                                           # not a record of work
        for role, who in (("executor", ex), ("verifier", ve)):
            if who is None:
                continue
            if not isinstance(who, dict) or not all(who.get(k) for k in ("handle", "lineage", "client")):
                report.append(f"T4 {f}: {role} does not name handle, lineage and client")
                continue
            if not LINEAGE.match(str(who["lineage"])) or not CLIENT.match(str(who["client"])):
                breach.append(f"L {f}: {role} names lineage '{who['lineage']}' and client '{who['client']}', not labels")
        if isinstance(ex, dict) and isinstance(ve, dict):
            if ex.get("handle") and ex.get("handle") == ve.get("handle"):
                breach.append(f"T2 {f}: the same handle executes and verifies ({ex['handle']})")
            if ex.get("lineage") and ex.get("lineage") == ve.get("lineage") and ex.get("lineage") != "human":
                report.append(f"T3 {f}: executor and verifier share lineage {ex['lineage']}")
        if mapping:
            text = open(f, encoding="utf-8").read().lower()
            for real, label in mapping.items():
                if real in text:
                    breach.append(f"L {f}: names what {label} stands for; write the label instead")

    for b in breach:
        print(f"breach: {b}")
    for r in report:
        print(f"report: {r}")
    print(f"{len(breach)} breach(es), {len(report)} report(s); Offices: {len(offices)}")
    return 1 if breach else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""check_lineage.py — is a declared lineage corroborated by the client's own session record? Local, read-only. DRAFT.

Body D4 of Commons Engineering, 24 October 2026, for commons.o#81 (O3; OF.3, OF.4). A record of work declares
who executed and who verified: {handle, lineage, client, session}. A declaration is one source. The second
is the session record the client keeps on the machine where the work ran. A lineage counts as corroborated
when that record exists in the declared client's store, names the declared lineage's model, and — where the
record gives `evidence:` — contains it. Otherwise it is unconfirmed, and an unconfirmed verifier is never
counted as a second opinion (E3).

What it proves: two processes of the declared lineages did the work. Not: that authority was independent.

The mapping is local and outside git (OF.4). It is the only place where labels meet what they stand for:

    lineage: {L1: {model: <text that identifies the model in a session record>}, …}
    client:  {C1: {sessions: <glob of the client's session files, ~ allowed>}, …}

Nothing from the mapping is printed; the report speaks in labels only.

Usage:
    check_lineage.py --mapping FILE RECORD [RECORD ...] [--strict]
Exit 0; with --strict, 1 when a verifier is unconfirmed or shares the executor's lineage.
"""
import argparse
import glob
import os
import sys

import yaml


def session_file(store, session):
    for f in glob.glob(os.path.expanduser(store), recursive=True):
        if session in os.path.basename(f):
            return f
    return None


def judge(who, mapping, base):
    """Return (verdict, reason) for one declared participant."""
    if not isinstance(who, dict):
        return "unconfirmed", "no declaration"
    lin, cli, ses = who.get("lineage"), who.get("client"), who.get("session")
    if lin == "human":
        return "human", "a person; no session record applies"
    if not (lin and cli and ses):
        return "unconfirmed", "the declaration names no lineage, client or session"
    store = ((mapping.get("client") or {}).get(cli) or {}).get("sessions")
    model = ((mapping.get("lineage") or {}).get(lin) or {}).get("model")
    if not store or not model:
        return "unconfirmed", f"the mapping has no session store for {cli} or no model for {lin}"
    if not os.path.isabs(os.path.expanduser(store)):
        store = os.path.join(base, store)
    f = session_file(store, str(ses))
    if not f:
        return "unconfirmed", f"no session {ses} in the store of {cli}"
    text = open(f, encoding="utf-8", errors="replace").read()
    if model not in text:
        return "unconfirmed", f"session {ses} in {cli} does not name the model of {lin}"
    ev = who.get("evidence")
    if ev and ev not in text:
        return "unconfirmed", f"session {ses} does not contain the stated evidence"
    return "corroborated", f"session {ses} found in {cli}, model of {lin} named" + (", evidence present" if ev else "")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--mapping", required=True)
    ap.add_argument("records", nargs="+")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    mapping = yaml.safe_load(open(a.mapping, encoding="utf-8")) or {}
    base = os.path.dirname(os.path.abspath(a.mapping))
    failed = False
    for r in a.records:
        doc = yaml.safe_load(open(r, encoding="utf-8")) or {}
        ex, ve = doc.get("executor"), doc.get("verifier")
        print(f"# {r}")
        verdicts = {}
        for role, who in (("executor", ex), ("verifier", ve)):
            if who is None:
                continue
            v, why = judge(who, mapping, base)
            verdicts[role] = v
            print(f"{role}: {who.get('handle') if isinstance(who, dict) else '?'} · {who.get('lineage') if isinstance(who, dict) else '?'} · {v} — {why}")
        if ve is not None:
            same = isinstance(ex, dict) and isinstance(ve, dict) and ex.get("lineage") == ve.get("lineage") != "human"
            counts = verdicts.get("verifier") in ("corroborated", "human") and not same
            print("second opinion: " + ("counts" if counts else "does not count" + (" (same lineage, reported)" if same else " (verifier unconfirmed)")))
            failed |= not counts
        print()
    return 1 if (a.strict and failed) else 0


if __name__ == "__main__":
    sys.exit(main())

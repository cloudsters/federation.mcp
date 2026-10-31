#!/usr/bin/env python3
"""check_names.py — no client name appears in the discipline's text (commons.o#85, K4). Read-only.

The names are never written to a file of a repository. They are read at run time:
  * from the platform: the subject of every instance repository (`<slug>.d`, `.g…`, `.w…`, `.i`, `.core`, with or
    without a `-legacy` tail) and every organisation that is not the discipline's or the federation's own;
  * and from --names FILE, a list kept outside git, one name per line.
The discipline's own words (STOP) and every name given with --allow are never flagged. A name is matched as a whole
word, case-insensitive, with a hyphen, a space or nothing between its parts; a name that is also an ordinary word
(WORDS) only where it is written with a capital.

Scans the files git tracks under PATH (default: this repository), and with --issues owner/repo every item body and
comment of that repository. A finding names the place and the name; the place is what the owner changes.

Exit 0 when clean, 1 with findings.

Usage:  check_names.py [PATH] [--rev REV] [--orgs org1,org2 | --no-platform] [--names FILE] [--allow name,…]
                        [--issues owner/repo]
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
INSTANCE = re.compile(r"^(?P<slug>[a-z0-9-]+?)(\.(d|i|core|g\d*|w\d*|\d+\.core))?(-legacy)?$")
SUFFIXED = re.compile(r"\.(d|i|core|g\d*|w\d*)(-legacy)?$|\.\d+\.core$")
STOP = {"commons", "cloudsters", "commons-engineering", "commons-os", "singular", "singular-z", "vector", "vector-n",
        "workshop", "europe", "americas", "africa", "mena", "asia-pacific", "core", "example", "synthetic-a",
        "synthetic-b"}
WORDS = {"cursor", "gore", "junge"}     # also ordinary words: flagged only where written with a capital


def gh(*args):
    out = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        sys.exit(f"gh {' '.join(args[:2])}: {out.stderr.strip()[:200]}")
    return out.stdout


def platform_names(orgs):
    """the subjects of instance repositories, and the organisations that are not the discipline's or the federation's"""
    names = set()
    for o in orgs:
        if not o.lower().startswith(("cloudsters", "commons-")) and o.lower() not in STOP:
            names.add(o.lower())
        for r in json.loads(gh("repo", "list", o, "--limit", "1000", "--json", "name")):
            if SUFFIXED.search(r["name"]):
                names.add(INSTANCE.match(r["name"]).group("slug") if INSTANCE.match(r["name"]) else r["name"].split(".")[0])
    return names


def lines(out):
    return [json.loads(l) for l in out.splitlines() if l.strip()]


def pattern(names):
    alts = sorted({re.escape(n).replace(r"\-", "-").replace("-", r"[-\s_]?") for n in names}, key=len, reverse=True)
    return re.compile(r"(?<![\w-])(" + "|".join(alts) + r")(?![\w-])", re.I) if alts else None


def scan(text, rx):
    for i, line in enumerate(text.splitlines(), 1):
        for m in rx.finditer(line):
            if not (m.group(1).lower() in WORDS and m.group(1).islower()):
                yield i, m.group(1)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=os.path.join(HERE, "..", ".."))
    ap.add_argument("--orgs", help="organisations to read names from; default: all the user can see")
    ap.add_argument("--no-platform", action="store_true", help="read names only from --names")
    ap.add_argument("--names", help="a list kept outside git, one name per line")
    ap.add_argument("--allow", default="", help="names never flagged, comma-separated")
    ap.add_argument("--issues", help="also scan the items of owner/repo")
    ap.add_argument("--rev", help="scan the files at this revision of PATH instead of the working tree")
    a = ap.parse_args()

    names = set()
    if not a.no_platform:
        orgs = a.orgs.split(",") if a.orgs else gh("api", "user/orgs", "--paginate", "--jq", ".[].login").split()
        names |= platform_names(orgs)
    if a.names:
        names |= {l.strip().lower() for l in open(a.names, encoding="utf-8") if l.strip() and not l.startswith("#")}
    names -= STOP | {n.strip().lower() for n in a.allow.split(",") if n.strip()}
    rx = pattern(names)
    if rx is None:
        sys.exit("no names to check against")

    findings = []
    git = lambda *x: subprocess.run(["git", "-C", a.path, *x], capture_output=True).stdout
    if a.rev:                                                   # one archive of the revision, read in memory
        tar = tarfile.open(fileobj=io.BytesIO(git("archive", "--format=tar", a.rev)))
        blobs = ((m.name, tar.extractfile(m).read()) for m in tar if m.isfile())
    else:
        blobs = ((f, open(os.path.join(a.path, f), "rb").read()) for f in git("ls-files", "-z").decode("utf-8").split("\0")
                 if f and os.path.isfile(os.path.join(a.path, f)))
    for f, raw in blobs:
        try:
            text = raw.decode("utf-8") if len(raw) <= 2_000_000 else ""
        except UnicodeDecodeError:
            continue
        findings += [(f, i, n) for i, n in scan(text, rx)]
        findings += [(f, 0, n) for _, n in scan(f.replace("/", " "), rx)]
    if a.issues:
        for it in lines(gh("api", f"repos/{a.issues}/issues?state=all&per_page=100", "--paginate", "--jq", ".[] | tojson")):
            where = f"{a.issues}#{it['number']}"
            findings += [(where, i, n) for i, n in scan((it.get("title") or "") + "\n" + (it.get("body") or ""), rx)]
        for c in lines(gh("api", f"repos/{a.issues}/issues/comments?per_page=100", "--paginate", "--jq", ".[] | tojson")):
            where = f"{a.issues}#{c['issue_url'].rsplit('/', 1)[1]} comment {c['id']}"
            findings += [(where, i, n) for i, n in scan(c.get("body") or "", rx)]
    print(f"# {len(names)} names · {len(findings)} findings")
    for where, i, n in findings:
        print(f"{where}{':' + str(i) if i else ''}: {n}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

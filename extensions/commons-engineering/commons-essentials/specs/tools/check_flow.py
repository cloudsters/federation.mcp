#!/usr/bin/env python3
"""check_flow.py — a board, or an item, is well-formed and anchored by Commons FLOW. Read-only.

Body D2 of Commons Engineering, for commons.o#83 (deliverable D3). It implements part 6 of `flow.md` and of
`flow-bodies.md`: each finding is reported as

    fail    a MUST is not met                       → exit 1
    should  a SHOULD is not met                     → reported, exit 0
    gap     something is absent and no MUST needs it → reported, exit 0

Input is a board as `schemas/flow.schema.json` describes it: one workshop of a commons and its items, exported
from the platform. `--export` writes such a file from a GitHub project, read-only.

Check ids, flow.md:           type fields comments stroke parent done labels assignee status taken-up accepted
                              decision-record escalation loop matrix export wip
Check ids, flow-workshops.md: workshop setup
Check ids, flow-graph.md:     edges resolve
Check ids, flow-bodies.md:    signature handles labels-only office-word start-files taking-part

The edges of an item (core, anchors, stroke, writes_model, raised_by, carried_by, delivered_by, observed_by) are read
as the board states them, else derived from its body and comments, the way the export derives them. Every target
resolves in the item's definite CORE (its own, its parent's, or the workshop's): what does not resolve, and what
cannot be read here, is a gap, never invented; a malformed edge is a fail. Acceptance and an Office's word are checked
as records (who, what, the mandate or a link to it; quote, date, session, CORE, Post, link), and where not every comment
could be read, a missing record is a gap, not a fail.

Usage:
    check_flow.py BOARD.yml [--mapping FILE] [--bodies DIR] [--model DIR] [--project OWNER/NUMBER] [--core OWNER/REPO=DIR]
    check_flow.py --export OWNER NUMBER KIND COMMONS > BOARD.yml
--mapping  the commons' private label mapping (lineage and client names); without it, labels-only is a gap
--bodies   the folder holding start/ and handover/; without it, start-files is a gap
--model    a model folder for check_taking_part.py; without it, taking-part is a gap
--project  runs the workshop's setup check (check_workshop.py); without it, setup is a gap
A green check describes the work. It grants no authority to act.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

import yaml

try:
    import jsonschema
except ImportError:
    jsonschema = None

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(HERE, "..", "schemas", "flow.schema.json")
SETUP = os.path.join(HERE, "..", "schemas", "flow-workshop.yml")
WORKSHOP_TOOL = os.path.join(HERE, "check_workshop.py")
TAKING_PART_TOOL = os.path.join(HERE, "check_taking_part.py")
sys.path.insert(0, HERE)
from check_spec import local_checkout, git, parts_of, split, table  # noqa: E402

FOUR = ["Goal", "Approach", "Deliverables", "Definition of Done"]
FIELDS = {                                                     # flow.md R6, R20, R21, R22
    "Epic": FOUR, "Story": FOUR, "Task": FOUR, "Bug": FOUR,
    "Decision": ["Outcome", "Scope", "Decided", "Statement"],
    "Escalation": ["Raised by", "Asked", "Question", "Definition of Done"],
    "Loop": ["Definition", "Node", "Carried by"],
}
KINDS = ("delivery", "position", "decision")
ELEMENTS = ("stakeholder|journey|touchpoint|value-exchange|value-stream|capability|entity|"
            "solution|body|post|dimension|family|step")         # MODEL R18, part 5
ANCHOR = re.compile(r"anchor:?\**\s*`?(?P<ref>[a-z0-9-]+#R\d+|(?:" + ELEMENTS + r"):[a-z0-9/._-]+(?:#[a-z_]+:[a-z0-9/._-]+)?)`?"
                    r"(?P<rest>.*)$", re.I)
STROKE = re.compile(r"\b(changes|fulfils|fulfills)\b", re.I)
BODY_LABEL = re.compile(r"^[DFS]\d+$")
TAKEN = re.compile(r"taken up\s*:", re.I)
LOOP_KEY = re.compile(r"^\W*loop:\s*([\w.-]+)\s*·\s*id:\s*([\w.-]+)", re.I)
HANDLE = re.compile(r"@([A-Za-z0-9][A-Za-z0-9_-]*)")
ROLE = re.compile(r"^([DFSO])(\d+)(?:-([A-Z]{2}))?$")         # flow-bodies.md R5
LABELS = re.compile(r"\bL\d+\b.*\bC\d+\b")
SECTION = re.compile(r"^##\s+(.+?)\s*$")
# the edges of work (flow-graph): the forms a target may take
REQ = re.compile(r"^(?P<spec>[a-z0-9-]+)#(?P<rid>R\d+)$")
ADDR = re.compile(r"^(?P<kind>" + ELEMENTS + r"):(?P<slug>[a-z0-9][a-z0-9/._-]*)(?:#(?P<field>[a-z_]+):(?P<to>[a-z0-9][a-z0-9/._-]*))?$")
EDGES = {"core": re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$"),          # the CORE's id (CORE R2), never a repository
         "raised_by": re.compile(r"^loop:[A-Za-z0-9_.-]+$"),
         "carried_by": re.compile(r"^(body|post):[a-z0-9][a-z0-9._-]*$"),
         "delivered_by": re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(@[0-9a-f]{7,40}|#[0-9]+)$"),
         "observed_by": re.compile(r"^claim:[A-Za-z0-9_.-]+$")}
CORE_LINE = re.compile(r"^\W*CORE:\s*`?([a-z0-9]+(?:-[a-z0-9]+)*)`?", re.I | re.M)
LOCATION = re.compile(r"^(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@(?P<rev>[^\s:@]+)(?::(?P<path>\S+))?$")
OBSERVATIONS = {"fact", "measure", "signal"}                      # core-knowledge R3, R5
WRITES_LINE = re.compile(r"^\W*Writes:\s*(.+)$", re.I | re.M)
CARRIED_LINE = re.compile(r"^\W*Carried by:\s*`?((?:body|post):[a-z0-9][a-z0-9._-]*)`?", re.I | re.M)
COMMIT = re.compile(r"\b([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@([0-9a-f]{7,40})\b")
PULL = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/pull/(\d+)")
CLAIM = re.compile(r"\bclaim:([A-Za-z0-9_.-]+)")
# a record, not a word (flow.md R20, flow-bodies.md R7)
WHAT = re.compile(r"\b(accept(?:ed|s)?|stop(?:s|ped)?)\b", re.I)
REASON = re.compile(r"\bstop(?:s|ped)?\b[^.\n]*?\b(?:because|since|as|for)\b|\bstop(?:s|ped)?\s*:\s*\S", re.I)
MANDATE = re.compile(r"\bmandate\b", re.I)
RECORDED = re.compile(r"https?://\S+|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#\d+|(?<![\w/])#\d+|\bcomment \d{4,}")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2} (January|February|March|April|May|June|July|August|September|"
                  r"October|November|December)\b", re.I)
SESSION = re.compile(r"\bsession\b", re.I)
POST = re.compile(r"\bpost:[a-z0-9][a-z0-9._-]*|\bPost\b")
CORE_WORD = re.compile(r"\bCORE\b|\b[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.core\b")
ALL = {"Backlog", "Ready", "In Progress", "Validate", "Done"}
MATRIX = {                                                     # flow.md part 5: statuses, Stage, workshops, parent
    "Loop": ({"Backlog", "In Progress", "Done"}, False, {"model"}, set()),
    "Epic": (ALL, True, {"model", "commons", "project"}, set()),
    "Story": (ALL, False, {"model", "project"}, {"Epic"}),
    "Task": (ALL, False, {"model", "commons", "project"}, {"Story", "Epic"}),
    "Bug": (ALL, False, {"model", "commons", "project"}, {"Epic"}),
    "Decision": ({"In Progress", "Done"}, False, {"model", "commons", "project"}, set()),
    "Escalation": ({"Backlog", "In Progress", "Done"}, False, {"model", "commons", "project"}, set()),
}
FOLDERS = {"stakeholder": "stakeholders", "journey": "journeys", "touchpoint": "touchpoints",
           "value-exchange": "value-exchanges", "value-stream": "value-streams", "capability": "capabilities",
           "entity": "entities", "solution": "solutions", "body": "bodies", "post": "bodies"}


class Report:
    def __init__(self):
        self.items = []

    def add(self, o, c, t):
        if (o, c, t) not in self.items:
            self.items.append((o, c, t))

    def fail(self, c, t): self.add("fail", c, t)
    def should(self, c, t): self.add("should", c, t)
    def gap(self, c, t): self.add("gap", c, t)


def sections(body):
    """the level-2 headings of a body in order, and the text under each"""
    order, text, cur = [], {}, None
    for line in (body or "").splitlines():
        m = SECTION.match(line)
        if m:
            cur = m.group(1).strip().rstrip(":")
            order.append(cur)
            text[cur] = []
        elif cur is not None:
            text[cur].append(line)
    return order, {k: "\n".join(v).strip() for k, v in text.items()}


def first_line(text):
    for line in (text or "").splitlines():
        if line.strip():
            return line.strip()
    return ""


def kind_of(comment):
    head = first_line(comment.get("body", "")).lower()
    found = [k for k in KINDS if re.search(r"\b" + k + r"\b", head)]
    return found[0] if found else None


def handles_in(line):
    return HANDLE.findall(line)


def derive(i):
    """the edges of an item: as the board states them, else as its body and comments write them (flow-graph).
    The export derives them the same way, so a board written by hand and an exported one are read alike."""
    _, text = sections(i.get("body"))
    goal = next((v for k, v in text.items() if k.lower().startswith("goal")), "")
    lines = [l for l in goal.splitlines() if ANCHOR.search(l.strip().lstrip("-* "))]
    notes = [c.get("body", "") for c in i.get("comments") or [] if kind_of(c) in ("delivery", "decision")]
    e = {"anchors": [ANCHOR.search(l.strip().lstrip("-* ")).group("ref") for l in lines],
         "stroke": (STROKE.search(lines[0]).group(1).lower().replace("fulfills", "fulfils") if lines and STROKE.search(lines[0]) else None),
         "writes_model": [w.strip(" `") for m in WRITES_LINE.findall(i.get("body") or "") for w in m.split(",") if w.strip(" `")],
         "core": (CORE_LINE.search(i.get("body") or "") or [None, None])[1],
         "carried_by": (CARRIED_LINE.search(i.get("body") or "") or [None, None])[1]
                       or next((f"body:{l.lower()}" for l in i.get("labels") or [] if BODY_LABEL.match(l)), None),
         "raised_by": (lambda m: f"loop:{m.group(1)}" if m else None)(LOOP_KEY.match(first_line(i.get("body")))),
         "delivered_by": sorted({f"{r}@{s}" for n in notes for r, s in COMMIT.findall(n)}
                                | {f"{r}#{p}" for n in notes for r, p in PULL.findall(n)}),
         "observed_by": sorted({f"claim:{c}" for n in notes for c in CLAIM.findall(n)}),
         "part_of": i.get("parent")}
    for k in e:
        if k in i and k != "part_of":
            e[k] = i[k]
    return e


class Cores:
    """the definite COREs a board's targets resolve in, each named by its id (CORE R2).

    A CORE is found where it is given (`--core <id>=DIR`), or where the CORE of the workshop (`--core DIR`, or the
    given CORE whose id the workshop names) declares it in the `sources` of its commons.yml as owner/repo@rev[:path],
    read from a local checkout at that revision. A CORE found there whose commons.yml names another id contradicts
    the board. Read-only; what is not at hand is unverified, never passed."""

    def __init__(self, given=None):
        self.given = dict(given or {})
        self.cache = {}
        self.tmp = None

    @staticmethod
    def id_of(d):
        f = os.path.join(d, ".commons", "commons.yml")
        doc = yaml.safe_load(open(f, encoding="utf-8")) if os.path.exists(f) else None
        return (doc or {}).get("id") if isinstance(doc, dict) else None

    def home(self):
        return self.given.get("*")

    def locate(self, core):
        """the folder of the CORE `core`, or None, and why"""
        if ("loc", core) in self.cache:
            return self.cache[("loc", core)]
        d, why = None, f"the CORE `{core}` is not at hand (no `--core {core}=DIR`, no source of the workshop's CORE)"
        if core in self.given:
            d, why = self.given[core], ""
        else:
            homes = [h for h in [self.home()] + list(self.given.values()) if h]
            for h in homes:
                if self.id_of(h) == core:
                    d, why = h, ""
                    break
            for h in homes if d is None else []:
                f = os.path.join(h, ".commons", "commons.yml")
                for src in ((yaml.safe_load(open(f, encoding="utf-8")) or {}).get("sources") or []) if os.path.exists(f) else []:
                    m = LOCATION.match(str(src))
                    if not m:
                        continue
                    owner, repo = m["repo"].split("/", 1)
                    c = local_checkout(h, owner, repo)
                    if not c:
                        continue
                    base = (m["path"] or "").strip("/")
                    shown = git(c, "show", f"{m['rev']}:{(base + '/') if base else ''}.commons/commons.yml")
                    if shown.returncode or (yaml.safe_load(shown.stdout) or {}).get("id") != core:
                        continue
                    import tarfile, tempfile, io as _io
                    self.tmp = self.tmp or tempfile.mkdtemp(prefix="check_flow-")
                    out = subprocess.run(["git", "-C", c, "archive", "--format=tar", m["rev"]] + ([base] if base else []),
                                         capture_output=True)
                    if out.returncode == 0:
                        dest = os.path.join(self.tmp, core)
                        tarfile.open(fileobj=_io.BytesIO(out.stdout)).extractall(dest)
                        d, why = os.path.join(dest, base) if base else dest, ""
                        break
                if d:
                    break
        if d and not os.path.isdir(d):
            d, why = None, f"`{d}`, given for `{core}`, is no folder"
        self.cache[("loc", core)] = (d, why)
        return d, why

    def model(self, d):
        key = ("model", d)
        if key not in self.cache:
            recs = {}
            for f in glob.glob(os.path.join(d, "registry", "**", "*.y*ml"), recursive=True):
                doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
                for x in (doc.get("records") or [doc]) if isinstance(doc, dict) else []:
                    if isinstance(x, dict) and x.get("kind") and x.get("slug"):
                        recs[(x["kind"], str(x["slug"]))] = x
            self.cache[key] = recs
        return self.cache[key]

    def claims(self, d):
        f = os.path.join(d, "knowledge", "claims.yml")
        doc = yaml.safe_load(open(f, encoding="utf-8")) if os.path.exists(f) else None
        cl = (doc or {}).get("claims") if isinstance(doc, dict) else doc
        return {str(c.get("id")): c for c in cl or [] if isinstance(c, dict)}

    def resolve(self, core, target):
        """found · missing · unverified · contradicts, and a reason (flow-graph R2, R4)"""
        if not core:
            return "unverified", "no CORE is named for it"
        d, why = self.locate(core)
        if not d:
            return "unverified", why
        found = self.id_of(d)
        if found != core:
            return "contradicts", f"the CORE found for `{core}` names itself `{found}`"
        if m := REQ.match(target):
            specs = [x for base in ("specs", "commons-as-code") for x in [os.path.join(d, base, f"{m['spec']}.md")]
                     if os.path.exists(x)] or glob.glob(os.path.join(d, "**", f"{m['spec']}.md"), recursive=True)
            if not specs:
                return "missing", f"no specification `{m['spec']}` in `{core}`"
            _, lines = split(open(specs[0], encoding="utf-8").read())
            _, rows = table(parts_of(lines)[0].get(4, ("", []))[1])
            return ("found", "") if any(r and r[0] == m["rid"] for r in rows) else ("missing", f"`{m['spec']}` has no {m['rid']}")
        if m := ADDR.match(target):
            kind, slug = m["kind"], m["slug"]
            if kind == "dimension":
                return ("found", "") if re.fullmatch(r"d[0-4]", slug) else ("missing", f"`{slug}` is no dimension")
            recs = self.model(d)
            if kind == "family":
                ok = any(r.get("family") == slug for (k, _), r in recs.items() if k == "value-stream")
                return ("found", "") if ok else ("missing", f"no value stream of `{core}` runs in the family `{slug}`")
            if kind == "step" or (kind == "value-stream" and "/" in slug):
                stream, _, step = slug.partition("/")
                vs = recs.get(("value-stream", stream))
                rec = next((x for x in (vs or {}).get("steps") or [] if isinstance(x, dict) and x.get("slug") == step), None)
                if rec is None:
                    return "missing", f"`{core}` holds no step `{stream}/{step}`"
            else:
                rec = recs.get((kind, slug))
                if rec is None:
                    return "missing", f"`{core}` holds no {kind} `{slug}`"
            if m["field"]:
                v = rec.get(m["field"])
                vals = [str(x) for x in (v if isinstance(v, list) else [v])] if v is not None else []
                if m["to"] not in vals and not any(str(x).endswith(m["to"]) for x in vals):
                    return "missing", f"`{kind}:{slug}` does not bind `{m['field']}: {m['to']}`"
            return "found", ""
        if target.startswith(("body:", "post:")):
            kind, slug = target.split(":", 1)
            return ("found", "") if (kind, slug) in self.model(d) else ("missing", f"`{core}` holds no {kind} `{slug}` in element 9")
        if target.startswith("claim:"):
            return ("found", "") if target[6:] in self.claims(d) else ("missing", f"`{core}` holds no claim `{target[6:]}`")
        if target.startswith("loop:"):
            ok = any(os.path.exists(os.path.join(d, p, f"{target[5:]}.loop.yml"))
                     for p in ("operations/loops", "instance/operations/loops"))
            return ("found", "") if ok else ("missing", f"`{core}` defines no loop `{target[5:]}`")
        if m := COMMIT.fullmatch(target):
            owner, repo = m.group(1).split("/", 1)
            c = local_checkout(d, owner, repo) or local_checkout(HERE, owner, repo)
            if not c:
                return "unverified", f"no checkout of `{m.group(1)}` is at hand"
            return ("found", "") if git(c, "cat-file", "-e", f"{m.group(2)}^{{commit}}").returncode == 0 \
                else ("unverified", f"`{m.group(2)}` is not in the local checkout of `{m.group(1)}`")
        return "unverified", "a pull request is not read here"

    def claim_kind(self, core, cid):
        d, _ = self.locate(core) if core else (None, "")
        c = self.claims(d).get(cid) if d else None
        return (c.get("kind") or "fact") if c else None


def core_of(i, by_ref, board, seen=()):
    """the definite CORE of an item: its own, else its parent's, else the workshop's (flow-graph R2)"""
    e = derive(i)
    if e["core"]:
        return e["core"]
    p = i.get("parent")
    if p in by_ref and p not in seen:
        return core_of(by_ref[p], by_ref, board, seen + (i["ref"],))
    return (board.get("workshop") or {}).get("core")


def anchors_of(i, by_ref, seen=()):
    """an item's anchors: its own, else inherited from its parent (a Task inherits its aim)"""
    own = derive(i)["anchors"]
    p = i.get("parent")
    return own or (anchors_of(by_ref[p], by_ref, seen + (i["ref"],)) if p in by_ref and p not in seen else [])


def accepted_record(c, humans):
    """what a decision comment lacks to be an acceptance record (flow.md R20): who, what and under which mandate,
    or a link to where that is recorded; and whether its authority can be established from the inputs"""
    b = c.get("body", "")
    who = handles_in(first_line(b))
    lack = [] if who else ["who"]
    if not WHAT.search(b):
        lack.append("accepted or stops")
    elif re.search(r"\bstop", b, re.I) and not re.search(r"\baccept", b, re.I) and not REASON.search(b):
        lack.append("why it stops")
    if not (MANDATE.search(b) or RECORDED.search(b)):
        lack.append("the mandate, or a link to where it is recorded")
    known = bool(who) and (who[0] in humans or (ROLE.match(who[0]) and ROLE.match(who[0]).group(1) == "O"))
    return lack, known


def office_record(b):
    """what an Office's recorded word lacks (flow-bodies.md R7)"""
    need = {"a verbatim quote": re.search(r"^\s*>", b, re.M), "the date": DATE.search(b),
            "the session": SESSION.search(b), "the CORE": CORE_WORD.search(b), "the Post": POST.search(b),
            "a link to its record": RECORDED.search(b)}
    return [k for k, v in need.items() if not v]


def triples(board):
    """every edge of a board as (item, edge, target), the work's side of the graph (flow-graph R1)"""
    by_ref = {i["ref"]: i for i in board.get("items") or []}
    out = []
    for i in board.get("items") or []:
        e = derive(i)
        e["core"] = core_of(i, by_ref, board)
        for k in ("core", "part_of", "raised_by", "carried_by", "stroke"):
            if e.get(k):
                out.append((i["ref"], k, e[k]))
        for k in ("anchors", "writes_model", "delivered_by", "observed_by"):
            out += [(i["ref"], k, x) for x in e[k] or []]
        out += [(i["ref"], "member_of", m.get("kind") or "unknown") for m in i.get("memberships") or []]
    return out


def check_board(board, r, mapping=None, bodies=None, model=None, project=None, cores=None):
    cores = cores if isinstance(cores, Cores) else Cores(cores)
    if jsonschema is None:
        r.fail("schema", "the jsonschema package is required for this check")
        return
    schema = json.load(open(SCHEMA, encoding="utf-8"))
    errs = list(jsonschema.Draft202012Validator(schema).iter_errors(board))
    for e in errs:
        r.fail("schema", f"{'/'.join(map(str, e.path)) or '(root)'}: {e.message}")
    if errs:
        return
    kind = board["workshop"]["kind"]
    items = board["items"]
    by_ref = {i["ref"]: i for i in items}
    humans = set(board.get("humans") or [])
    seen_handles = set()
    loop_keys = {}

    if not (board.get("workshop") or {}).get("core"):
        r.fail("workshop", "the board names no CORE for its workshop (flow-workshops R1)")

    for i in items:
        ref, typ, open_ = i["ref"], i["type"], i["state"] == "open"
        order, text = sections(i["body"])
        complete = i.get("comments_complete", True)
        e = derive(i)

        # type (flow.md R6): an export never invents a type
        if typ == "unknown":
            r.fail("type", f"{ref}: its type is none of the seven work objects; its fields cannot be checked")
            continue

        # edges (flow-graph): the form of every edge, as stated or as derived from the body
        for t in e["anchors"]:
            if not (REQ.match(t) or ADDR.match(t)):
                r.fail("edges", f"{ref}: the anchor `{t}` is neither a MODEL address nor `<spec>#R<n>`")
        for k in ("core", "raised_by", "carried_by"):
            if e[k] and not EDGES[k].match(e[k]):
                r.fail("edges", f"{ref}: `{k}` is `{e[k]}`, not of the form of that edge")
        for k in ("delivered_by", "observed_by"):
            for t in e[k] or []:
                if not EDGES[k].match(t):
                    r.fail("edges", f"{ref}: `{k}` holds `{t}`, not of the form of that edge")
        if typ in ("Epic", "Story", "Task", "Bug", "Loop") and not e["carried_by"]:
            r.fail("edges", f"{ref}: carried by no Body or Post (no `carried_by`, no Body label)")

        # resolve (flow-graph R2–R9): every target in the item's definite CORE; unresolvable is a gap, never invented
        core = core_of(i, by_ref, board)
        if e["carried_by"] and "carried_by" not in i and not CARRIED_LINE.search(i.get("body") or ""):
            r.gap("edges", f"{ref}: `carried_by` {e['carried_by']} is read from the label, a convenience (flow-graph R6)")
        for t in [x for x in e["anchors"] if REQ.match(x) or ADDR.match(x)] + [x for x in (
                [e["carried_by"], e["raised_by"]] + list(e["observed_by"] or [])) if x and (
                x.startswith(("body:", "post:", "loop:", "claim:")))] + list(e["delivered_by"] or []):
            state, why = cores.resolve(core, t)
            if state == "contradicts":
                r.fail("resolve", f"{ref}: {why}")
            elif state == "missing":
                r.gap("resolve", f"{ref}: `{t}` does not resolve: {why}")
            elif state == "unverified":
                r.gap("resolve", f"{ref}: `{t}` is unverified: {why}")
            elif t.startswith("claim:") and t in (e["observed_by"] or []):
                k = cores.claim_kind(core, t[6:])
                if k not in OBSERVATIONS:
                    r.should("resolve", f"{ref}: `{t}` is a {k}, not an observation (fact, measure, signal)")

        # fields (flow.md R6, R20, R21, R22)
        want = FIELDS[typ]
        got = [h for h in order if any(h.lower().startswith(w.lower()) for w in want)]
        missing = [w for w in want if not any(h.lower().startswith(w.lower()) for h in order)]
        if missing:
            r.fail("fields", f"{ref}: a {typ} lacks the field(s) {missing}")
        else:
            idx = [next(n for n, h in enumerate(order) if h.lower().startswith(w.lower())) for w in want]
            if idx != sorted(idx):
                r.fail("fields", f"{ref}: the fields are not in the order {want}")
        get = lambda w: next((v for k, v in text.items() if k.lower().startswith(w.lower())), "")

        # comments (R8, R9) and the signature of agents (flow-bodies R4, R5, R7)
        for c in i.get("comments") or []:
            head = first_line(c.get("body", ""))
            k = kind_of(c)
            hs = handles_in(head)
            if TAKEN.search(head) and not k:
                k = "delivery"                                   # a taken-up line is a delivery note
            if not k:
                r.fail("comments", f"{ref}: a comment does not say in its first line whether it is a delivery, a position or a decision: {head[:60]}")
            if not hs:
                r.fail("comments", f"{ref}: a comment's first line names no handle: {head[:60]}")
            if k == "position" and not any(f.lower() in c.get("body", "").lower() for f in FOUR):
                r.fail("comments", f"{ref}: a position names none of the four fields it would change")
            for h in hs:
                m = ROLE.match(h)
                if m:
                    seen_handles.add(h)
                    if not m.group(3):
                        r.fail("handles", f"{ref}: `@{h}` lacks the commons' code (`@{m.group(1)}{m.group(2)}-XX`)")
                    if not LABELS.search(head):
                        r.fail("signature", f"{ref}: `@{h}` signs without lineage and client labels (L…, C…)")
                    if m.group(1) == "O" and k == "decision":
                        lack = office_record(c.get("body", ""))
                        if lack:
                            r.fail("office-word", f"{ref}: an Office records a word without {', '.join(lack)}")

        # edges: the anchor (flow-graph R3) and stroke (flow.md R11)
        if typ in ("Epic", "Story", "Bug"):
            if not e["anchors"]:
                r.fail("edges", f"{ref}: no anchor (`Anchor: <spec>#R<n>` or a MODEL address in the Goal, or `anchors`)")
            elif not e["stroke"]:
                r.fail("stroke", f"{ref}: the anchor does not say whether the work changes an orientation or fulfils one")
        elif typ == "Task" and not anchors_of(i, by_ref) and not i.get("parent"):
            r.fail("edges", f"{ref}: a Task with neither a parent nor an anchor of its own")
        stated = [(t, x) for t in ("anchors", "delivered_by", "observed_by", "writes_model") for x in e[t] or []]
        for t, x in sorted({(t, x) for t, x in stated if stated.count((t, x)) > 1}):
            r.fail("edges", f"{ref}: the edge `{t}` → `{x}` is stated twice")

        # matrix (flow.md R35, part 5)
        statuses, stage, places, parents = MATRIX[typ]
        if i["status"] not in statuses:
            r.fail("matrix", f"{ref}: a {typ} takes the statuses {sorted(statuses)}, not {i['status']}")
        if stage and open_ and not i.get("stage"):
            r.fail("matrix", f"{ref}: an open Epic states no Stage")
        if not stage and i.get("stage"):
            r.fail("matrix", f"{ref}: a {typ} has no Stage, and states `{i['stage']}`")
        for k in sorted(({m.get("kind") for m in i.get("memberships") or []} | {kind}) - places - {None}):
            r.fail("matrix", f"{ref}: a {typ} is in no {k} workshop")
        p = i.get("parent")
        pt = by_ref[p]["type"] if p in by_ref else None
        if p and not parents:
            r.fail("matrix", f"{ref}: a {typ} hangs under nothing, and here under {p}")
        elif pt and parents and pt not in parents:
            r.fail("matrix", f"{ref}: a {typ} hangs under {' or '.join(sorted(parents))}, not under a {pt}")

        # export (flow.md R36): a board declares what it could not read
        if "comments_complete" not in i:
            r.gap("export", f"{ref}: the board does not declare whether every comment was read")
        elif not complete:
            r.gap("export", f"{ref}: not every comment was read; checks that need the history report gaps")

        # parent (R12)
        p = i.get("parent")
        if typ in ("Story", "Task") and not p:
            r.fail("parent", f"{ref}: a {typ} hangs under no {'Epic' if typ == 'Story' else 'Story or Epic'}")
        elif p in by_ref:
            pt = by_ref[p]["type"]
            if typ == "Story" and pt != "Epic":
                r.fail("parent", f"{ref}: a Story hangs under a {pt}, not an Epic")
            if typ == "Task" and pt not in ("Story", "Epic"):
                r.fail("parent", f"{ref}: a Task hangs under a {pt}")

        # done (R13, R14)
        if "Definition of Done" in want:
            dod = get("Definition of Done")
            if not re.search(r"^\s*(?:[-*]|\d+\.)\s+\S", dod, re.M):
                r.fail("done", f"{ref}: the Definition of Done lists no condition that can be checked")
            if typ == "Story" and not re.search(r"observ", dod, re.I):
                r.should("done", f"{ref}: the Story's Definition of Done names no one who observes its effect")

        # labels (R15)
        if open_:
            body_labels = [l for l in i["labels"] if BODY_LABEL.match(l)]
            others = [l for l in i["labels"] if not BODY_LABEL.match(l)]
            if not body_labels:
                r.fail("labels", f"{ref}: an open item carries no Body label")
            if others:
                r.fail("labels", f"{ref}: an open item carries labels other than Body labels: {others}")

        # assignee (R16) and wip (R24)
        a = i.get("assignees") or []
        if i["status"] == "Validate" and not a:
            r.fail("assignee", f"{ref}: in Validate, and no human is named to act next")
        if not open_ and a:
            r.fail("assignee", f"{ref}: closed, and still assigned to {a}")
        if humans:
            for x in a:
                if x not in humans:
                    r.fail("assignee", f"{ref}: the assignee `{x}` is not a human of this commons")

        # status (R17)
        if open_ and i["status"] == "Done":
            r.fail("status", f"{ref}: open, but its status is Done")
        if not open_ and i["status"] != "Done":
            r.fail("status", f"{ref}: closed, but its status is {i['status']}")

        # taken-up (R18)
        if typ in ("Epic", "Story", "Task", "Bug") and i["status"] in ("In Progress", "Validate") and not any(
                TAKEN.search(c.get("body", "")) for c in i.get("comments") or []) and not TAKEN.search(i["body"]):
            if complete:
                r.fail("taken-up", f"{ref}: {i['status']}, and nobody has written `taken up:`")
            else:
                r.gap("taken-up", f"{ref}: no `taken up:` among the comments read, and not every comment was read")

        # accepted (R19) and decision-record (R20): a record, not a word
        decisions = [c for c in i.get("comments") or [] if kind_of(c) == "decision"]
        if not open_ and typ != "Decision":
            if not decisions:
                if complete:
                    r.fail("accepted", f"{ref}: closed without a decision comment that records who accepted it or why it stops")
                else:
                    r.gap("accepted", f"{ref}: no decision comment among the comments read, and not every comment was read")
            else:
                records = [accepted_record(c, humans) for c in decisions]
                full = [known for lack, known in records if not lack]
                if not full:
                    r.fail("accepted", f"{ref}: the decision comment lacks {', '.join(records[-1][0])}")
                elif not any(full):
                    r.gap("accepted", f"{ref}: who accepted is no human of this commons and no Office: the authority is unverified")
        if typ == "Decision":
            decided = get("Decided")
            if decided and not (handles_in(decided) or re.search(r"\bby\b", decided, re.I)):
                r.fail("decision-record", f"{ref}: the Decision does not name the human who decided")
            if decided and not re.search(r"mandate|under", decided, re.I):
                r.fail("decision-record", f"{ref}: the Decision does not name the mandate it was taken under")

        # escalation (R21)
        if typ == "Escalation":
            asked = get("Asked")
            if not get("Raised by"):
                r.fail("escalation", f"{ref}: the Escalation does not name the loop or Body that raises it")
            for h in handles_in(asked):
                if h in humans and h not in a:
                    r.fail("escalation", f"{ref}: `{h}` is asked, but is not the assignee")

        # loop (R22, R23)
        if typ == "Loop" and not re.search(r"\.loop\.ya?ml", get("Definition")):
            r.fail("loop", f"{ref}: a Loop item does not link its definition file")
        m = LOOP_KEY.match(first_line(i["body"]))
        if m and open_:
            key = (m.group(1), m.group(2))
            if key in loop_keys:
                r.fail("loop", f"{ref}: loop {key[0]} has already opened {loop_keys[key]} for id {key[1]}")
            loop_keys[key] = ref

        # workshop (flow-workshops R1–R4)
        if kind == "commons" and typ == "Story":
            r.fail("workshop", f"{ref}: a Commons Workshop holds a Story")
        if kind == "commons" and e["writes_model"]:
            r.fail("workshop", f"{ref}: a Commons Workshop holds work that writes the model")
        # what the work writes, not the word it uses, decides whether it is an item of the Model Workshop (R3)
        kinds = {m.get("kind") for m in i.get("memberships") or []} | {kind}
        if e["writes_model"] and "model" not in kinds:
            r.fail("workshop", f"{ref}: it writes the model ({', '.join(e['writes_model'][:3])}), and it is no item of the Model Workshop")

    # wip (R24)
    limits = board.get("limits") or {}
    if limits:
        load = {}
        for i in items:
            if i["state"] == "open":
                for x in i.get("assignees") or []:
                    load[x] = load.get(x, 0) + 1
        for h, n in load.items():
            if h in limits and n > limits[h]:
                r.fail("wip", f"`{h}` has {n} open items to act on, above the stated limit of {limits[h]}")
    else:
        r.gap("wip", "the board states no limits for humans")

    # labels-only (flow-bodies R3)
    if mapping:
        m = yaml.safe_load(open(mapping, encoding="utf-8")) or {}
        names = set()
        for group in ("lineage", "client"):
            for _, v in (m.get(group) or {}).items():
                names |= {str(x) for x in (v.values() if isinstance(v, dict) else [v]) if isinstance(x, str) and len(x) > 2}
        blob = json.dumps(board, ensure_ascii=False).lower()
        for n in sorted(names):
            if n.lower() in blob:
                r.fail("labels-only", f"a mapped name appears in the work: `{n}`")
    else:
        r.gap("labels-only", "no private label mapping given (--mapping)")

    # start-files (flow-bodies R11)
    if bodies:
        for h in sorted(seen_handles):
            label = ROLE.match(h).group(1) + ROLE.match(h).group(2)
            for folder in ("start", "handover"):
                if not any(os.path.exists(os.path.join(bodies, folder, f"{x}.md")) for x in (h, label)):
                    r.fail("start-files", f"`@{h}` has no {folder} file in `{bodies}`")
    else:
        r.gap("start-files", "no bodies folder given (--bodies)")

    # taking-part (flow-bodies R1, R2)
    if model and os.path.exists(TAKING_PART_TOOL):
        out = subprocess.run([sys.executable, TAKING_PART_TOOL, model], capture_output=True, text=True)
        if out.returncode:
            r.fail("taking-part", f"check_taking_part.py: {(out.stdout or out.stderr).strip().splitlines()[-1][:120]}")
    else:
        r.gap("taking-part", "no model folder given (--model)")

    # setup (R4)
    if project and os.path.exists(WORKSHOP_TOOL):
        owner, number = project.split("/")
        out = subprocess.run([sys.executable, WORKSHOP_TOOL, SETUP, owner, number, "--kind", f"{kind}-workshop"],
                             capture_output=True, text=True)
        if out.returncode:
            r.fail("setup", f"the workshop's setup shows something missing or differing ({owner} #{number})")
    else:
        r.gap("setup", "no project given (--project); the workshop's setup is not checked here")


Q = """query($o:String!,$n:Int!,$c:String){organization(login:$o){projectV2(number:$n){
 items(first:50,after:$c){pageInfo{hasNextPage endCursor} nodes{
  status:fieldValueByName(name:"Status"){... on ProjectV2ItemFieldSingleSelectValue{name}}
  stage:fieldValueByName(name:"Stage"){... on ProjectV2ItemFieldSingleSelectValue{name}}
  content{... on Issue{number title body state stateReason repository{nameWithOwner} issueType{name}
   labels(first:50){nodes{name}} assignees(first:20){nodes{login}} parent{number repository{nameWithOwner}}
   projectItems(first:20){nodes{project{title number owner{... on Organization{login} ... on User{login}}}}}
   comments(first:100){totalCount pageInfo{hasNextPage endCursor} nodes{author{login} createdAt body}}}}}}}}}"""
QC = """query($o:String!,$r:String!,$n:Int!,$c:String){repository(owner:$o,name:$r){issue(number:$n){
 comments(first:100,after:$c){pageInfo{hasNextPage endCursor} nodes{author{login} createdAt body}}}}}"""
OBJECTS = ("Loop", "Epic", "Story", "Task", "Bug", "Decision", "Escalation")
WORKSHOP_KINDS = (("model workshop", "model"), ("commons workshop", "commons"), ("project workshop", "project"))


def type_of(name):
    """the platform's type as a work object, or `unknown`: never invented (flow.md R6)"""
    t = re.sub(r"^\d+\s*", "", name or "").strip()
    return next((o for o in OBJECTS if o.lower() == t.lower()), "unknown")


def kind_of_workshop(title):
    t = (title or "").lower()
    return next((k for w, k in WORKSHOP_KINDS if w in t), None)


def comment(c):
    return {"author": (c.get("author") or {}).get("login", ""), "date": c["createdAt"], "body": c["body"]}


def item_of(node, more_comments=None):
    """one exported item: what the platform holds, faithfully; edges derived the way the checker derives them"""
    x = node.get("content") or {}
    cs = x.get("comments") or {}
    comments = [comment(c) for c in cs.get("nodes") or []] + [comment(c) for c in more_comments or []]
    i = {"ref": f"{x['repository']['nameWithOwner']}#{x['number']}",
         "type": type_of((x.get("issueType") or {}).get("name")), "title": x["title"],
         "state": x["state"].lower(), **({"closed_as": "not_planned"} if x.get("stateReason") == "NOT_PLANNED" else {}),
         "status": (node.get("status") or {}).get("name") or "Backlog",
         "labels": [l["name"] for l in x["labels"]["nodes"]],
         "assignees": [a["login"] for a in x["assignees"]["nodes"]],
         "parent": f"{x['parent']['repository']['nameWithOwner']}#{x['parent']['number']}" if x.get("parent") else None,
         "body": x.get("body") or "",
         "comments": comments,
         "comments_complete": len(comments) >= (cs.get("totalCount") or 0)}
    if (node.get("stage") or {}).get("name"):
        i["stage"] = node["stage"]["name"]
    ms = []
    for p in ((x.get("projectItems") or {}).get("nodes") or []):
        pr = p.get("project") or {}
        k = kind_of_workshop(pr.get("title"))
        ms.append({"kind": k or "unknown", "name": f"{(pr.get('owner') or {}).get('login', '')} #{pr.get('number')} {pr.get('title', '')}".strip()})
    if ms:
        i["memberships"] = ms
    e = derive(i)
    for k in ("core", "stroke", "raised_by", "carried_by"):
        if e[k]:
            i[k] = e[k]
    for k in ("anchors", "writes_model", "delivered_by", "observed_by"):
        if e[k]:
            i[k] = e[k]
    return i


def board_of(pages, owner, number, kind, commons, more=None):
    """a board from the raw pages of the project query, and from the further comment pages of each item"""
    items = []
    for d in pages:
        for n in d["data"]["organization"]["projectV2"]["items"]["nodes"]:
            x = n.get("content") or {}
            if x.get("number"):
                items.append(item_of(n, (more or {}).get(f"{x['repository']['nameWithOwner']}#{x['number']}")))
    return {"commons": commons, "workshop": {"kind": kind, "name": f"{owner} #{number}"}, "items": items}


def graphql(query, **v):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, val in v.items():
        if val is not None:
            args += ["-F" if isinstance(val, int) else "-f", f"{k}={val}"]
    out = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        sys.exit(f"export: {out.stderr.strip()[:200]}")
    return json.loads(out.stdout)


def export(owner, number, kind, commons):
    """read-only: every item of the project, with every comment, every membership and its own type"""
    pages, cursor, more = [], None, {}
    while True:
        d = graphql(Q, o=owner, n=int(number), c=cursor)
        pages.append(d)
        page = d["data"]["organization"]["projectV2"]["items"]
        for n in page["nodes"]:
            x = n.get("content") or {}
            cs = (x.get("comments") or {}).get("pageInfo") or {}
            c, extra = cs.get("endCursor"), []
            while cs.get("hasNextPage"):
                o, r = x["repository"]["nameWithOwner"].split("/")
                q = graphql(QC, o=o, r=r, n=x["number"], c=c)["data"]["repository"]["issue"]["comments"]
                extra += q["nodes"]
                cs, c = q["pageInfo"], q["pageInfo"]["endCursor"]
            if extra:
                more[f"{x['repository']['nameWithOwner']}#{x['number']}"] = extra
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return board_of(pages, owner, number, kind, commons, more)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("board", nargs="?")
    ap.add_argument("--mapping")
    ap.add_argument("--bodies")
    ap.add_argument("--model")
    ap.add_argument("--project")
    ap.add_argument("--core", action="append", default=[], metavar="[ID=]DIR",
                    help="a CORE by its id, or the workshop's CORE, whose sources locate the others; without it, a gap")
    ap.add_argument("--edges", action="store_true", help="print every edge of the board as a triple, one per line")
    ap.add_argument("--export", nargs=4, metavar=("OWNER", "NUMBER", "KIND", "COMMONS"))
    a = ap.parse_args()
    if a.export:
        if sys.platform == "win32":
            sys.stdout.reconfigure(encoding="utf-8")
        yaml.safe_dump(export(*a.export), sys.stdout, allow_unicode=True, sort_keys=False, width=120)
        return 0
    if not a.board:
        ap.error("a board file is needed")
    board = yaml.safe_load(open(a.board, encoding="utf-8")) or {}
    r = Report()
    if a.edges:
        if sys.platform == "win32":
            sys.stdout.reconfigure(encoding="utf-8")
        for t in triples(board):
            print("\t".join(t))
        return 0
    check_board(board, r, a.mapping, a.bodies, a.model, a.project,
                dict(c.split("=", 1) if "=" in c else ("*", c) for c in a.core))
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    for o, c, t in r.items:
        print(f"{o:6} {c:16} {t}")
    n = {o: sum(1 for x in r.items if x[0] == o) for o in ("fail", "should", "gap")}
    print(f"\n{a.board}: {n['fail']} fail · {n['should']} should · {n['gap']} gap")
    return 1 if n["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())

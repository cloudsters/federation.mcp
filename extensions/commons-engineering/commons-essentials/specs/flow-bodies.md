---
id: flow-bodies
title: Commons FLOW — Bodies, Posts and Offices at work
status: decided
lang: en
touches: [specification, flow, flow-workshops, flow-graph, model, core, extension]
terms: [commons, body, post, office, decision, escalation, commons-core]
schema: schemas/flow.schema.json
check: tools/check_flow.py
supersedes:
  - ../instance/workshop/bodies/HOW_BODIES_WORK.md
  - ../instance/workshop/bodies/D2/steward-model.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md
  - ../instance/workshop/bodies/D1/element-9-posts.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md
---

# Commons FLOW — Bodies, Posts and Offices at work

*Who takes part in the work of a commons, and how, from one human with agents to many thousands.*

## 1 · Goal

Work stays aimed only if it is clear who answers for it, who does it and who checks it, and if that stays clear when people and agents change, leave or multiply. This specification states how Bodies, Posts and Offices take part in the work of any commons: four functions held apart in every Body, lineage and client as labels, one Office per accountable human, care for the whole while accountability stays with each Body, start and handover by file, git as the record of who did what, and how Bodies form and the commons boots. It decides one thing for its reader: **whether those taking part in a piece of work are recorded so that accountability resolves to a human and execution stays distinguishable from it**. It is the companion of [flow](flow.md), which states the work itself, of [flow-workshops](flow-workshops.md) and of [flow-graph](flow-graph.md).

## 2 · Boundary

**Belongs here:** the four functions; lineage and client; handles; Offices and their recorded word; the duties of every Body toward the whole; start, handover, stand-down; git practice, with branches and pull requests in `flow` R37; how Bodies form; boot.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| the work objects, workshops, anchor, status and rhythm | `flow` |
| the records of Bodies and Posts, their serving entries and accountability chain | `model` |
| where element 9 lives, the party register, the identity file | `core` |
| which Posts and roles a domain proposes | `extension` |

**Touches** `specification`, `flow`, `model`, `core` and `extension`. **Rests on** the Steward's decisions: element 9 the Body with Posts (18 October 2026); A1–A4, S1; the Bodies of the discipline (20 October, commons.o#55); the push and worktree rules (19 and 23 October); the steward model E1–E6 and OF.1–OF.4 (24–25 October, commons.o#81); the handle rule (24 October).

## 3 · Terms

All terms resolve in the glossary. One is new with this specification and is added in the same change: [office](glossary/terms/office.yml).

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | Every Body holds four functions apart, accountable, execute, verify and record, the accountable is always a human, and no one executes and verifies the same work. | Only a person carries legal and moral responsibility, and the maker is not the checker. | taking-part |
| R2 | MUST | A verifier is of another lineage than the executor or a human who did not execute, and a verification within one lineage is recorded as such. | A second opinion from the same lineage is not a second opinion, and hiding that would be worse than having it. | taking-part |
| R3 | MUST | Lineage and client are recorded as labels such as `L1` and `C2`, mapped once in the commons' private settings, and no vendor or client name appears in any record, file or item. | The work must stay traceable to its executor without tying the commons to any vendor in its public record. | labels-only |
| R4 | MUST | Every comment written for a Body or an Office opens with its handle, its lineage label and its client label. | Every agent writes through its human's account, so the first line is where execution becomes distinguishable. | signature |
| R5 | MUST | The handle of a Body is `@Dn-<code>`, of an Office `@On-<code>`, where the code is the commons' two-letter code from its identity file, and a role that works across commons keeps its name. | One handle rule lets people and agents tell which commons a Body speaks for. | handles |
| R6 | MUST | Every accountable human has one Office, which serves all their Posts, holds no mandate of its own and is recorded as a record of kind office in element 9. | Offices multiply with stewards and never divide, so that each human's word has one place. | review |
| R7 | MUST | A steward's word recorded by their Office counts for the Body it names only when it is quoted verbatim with its date, session, CORE and Post and links to the recoverable record, and an Office never creates or enlarges an approval. | The record is the safeguard that lets a steward's word reach many Bodies without being invented on the way. | office-word |
| R8 | MUST | Accountability stays with each Body, and every Body decides with the whole in view, discloses effects on other Bodies, reports harm in another's sphere there without intervening, and reports to D0 what belongs to no Body. | Care for the whole is carried by every Body, while decisions stay where the mandate is. | review |
| R9 | MUST | D0 is the empty centre, which no person, Body or agent owns or speaks for, and its steward function convenes and routes without deciding for the circles. | Identity sits at the centre and is not a fifth agent. | review |
| R10 | MUST | An escalation goes to the circle of the next wider node and at the top to D0 as the circle, and a matter reserved to a steward goes to that steward directly. | Circles, not triangles: the top is the circle of the whole, not one person. | review |
| R11 | MUST | Every role has a start file and a handover note in its commons, named by its handle or its label, and a new session resumes from the note, the mandate and the open items before it writes anything. | A role must survive a change of session, client or person without its work being lost. | start-files |
| R12 | MUST | No role lives in a tool's memory or a client's session, and a change of session is written into the handover note before anything else. | What lives in one tool is invisible to every other and lost with it. | review |
| R13 | MUST | Every role works on a branch and through pull requests as `flow` R37 states, and a worktree serves only parallel writers and is removed in the same session. | One shared checkout between runs, clients and machines loses work, and stale copies mislead. | review |
| R14 | MUST | Every commit, item and comment names the human responsible, no vendor or tool appears as author, co-author or trailer, and no check is bypassed to get a change through. | Every change must stay traceable to the person who answers for it. | review |
| R15 | MUST | One accountable human may delegate bounded execution at any time, and an independent second signature needs a second human. | Delegation scales one person's work, and only another person adds independent accountability. | review |
| R16 | MUST | A planned departure is handed over to a named human or the wider Body, and an unexpected absence is shown as a gap with temporary coverage or suspended decisions. | Leaving must not break the work, and an absence must be visible rather than silent. | review |
| R17 | MUST | The accountable human can stand an agent down at any time without a reason, its open work is handed over, and the Body keeps its mandate. | The Body persists when every agent has left. | review |
| R18 | MUST | An agent never creates accounts, enters secrets, takes a governance decision, chooses the purpose or merges into `main` without the accountable human's word. | Some acts commit the commons and are a human's alone. | review |
| R19 | MUST | A commons states whether a Post may be served by agents only, and where it states nothing, an agent-only Post is not allowed. | A Post without a human serving it is a choice the commons makes explicitly, never by default. | review |
| R20 | MUST | A Post with a duty between Bodies names the Body it sits in and the Body that sends it. | A link between circles is held by someone who belongs to both. | review |
| R21 | MUST | Every serving names the mandate it rests on, a Supplier serves in a Post with an outcome mandate and decides its own method, and every decision names the accountable human. | Authority must resolve to a mandate and a person, and a Supplier is held to results, not to methods. | review |
| R22 | MUST | A Body below a dimension forms by gravitation, from recurring work, a rhythm of its own and an accountable human, inherits its slice of the wider mandate and folds back when the gravitation ends, recorded both times. | Bodies arise where work draws together and do not outlive it. | review |
| R23 | MUST | A commons boots in a conversation between its first human and an agent, needs nobody's approval to begin, and nothing the conversation produces enters the CORE without that human's review. | Any commons can begin on its own terms, and its first record is its human's. | review |
| R24 | MUST | Any role starts in any client from one line, `You take part as <handle>; read <start file>.`, and the start file holds everything else the session needs. | A role that needs a client's features or memory to start belongs to that client, not to the commons. | review |
| R25 | SHOULD | A session is titled `D<n> · <code> — <Body>` for a Body and `· O<n> · <code> — Office · <name>` for an Office, so that Offices sort first. | One title rule lets a person find any role's session at a glance, whatever the client. | review |

## 5 · Structure

The schema is `schemas/flow.schema.json`, the board of `flow`: these requirements are read from its comments and from the records of element 9. Taking part itself, with `function`, `lineage`, `client` and `under` on every serving entry, is recorded as `model` states it.

| Where | What this specification reads |
|---|---|
| a comment's first line | the handle, the lineage label and the client label (R4, R5) |
| an Office's decision comment | the verbatim quote and the link to its record (R7) |
| `start/` and `handover/` of the commons' bodies folder | one file each per handle or label (R11) |
| element 9 | the functions, lineages and clients of serving entries (R1, R2) |
| the commons' private settings | the mapping of labels to names, never in a record or item (R3) |

## 6 · Checks

`tools/check_flow.py <board>` runs these checks as well as those of `flow`. Each needs its input, and without it reports a gap.

| Check | Tests |
|---|---|
| `taking-part` | with `--model`, the serving entries pass `check_taking_part.py`: functions, lineage, an executor that does not verify itself (R1, R2) |
| `labels-only` | with `--mapping`, no mapped name appears anywhere in the board (R3) |
| `signature` | a comment by a Body or an Office handle carries lineage and client labels (R4) |
| `handles` | a Body or Office handle carries the commons' code (R5) |
| `office-word` | an Office's decision comment holds a verbatim quote, its date, the session, the CORE and the Post, and a link to its record; what the input cannot establish is a gap, unverified (R7) |
| `start-files` | with `--bodies`, every Body or Office handle seen has a start file and a handover note (R11) |
| `review` | a reading by the human accountable, or by an agent that has only this file, of R6, R8–R10, R12–R25 |

## 7 · Example

**Minimal:** a comment of the desk Body of the tool library, and an Office's recorded word, in a board of `flow`:

```yaml
commons: tool-library
workshop: {kind: model, name: Tool library}
items:
- ref: tool-library/tool-library.core#5
  type: Decision
  title: "Decision: the desk may log returns without Ana present"
  state: closed
  status: Done
  labels: [D0]
  body: |
    ## Outcome
    Accepted.
    ## Scope
    Returns only.
    ## Decided
    By @ana, under the D4 mandate, in the Office session of 26 October.
    ## Statement
    The desk logs returns on its own.
  comments:
  - author: ana
    body: |
      @O1-TL · L1 · C1 — decision: Ana's word, 2026-10-26, in the Office session, for tool-library/tool-library.core, Post d4.steward
      > The desk may log returns without me.
      Recorded at tool-library/tool-library.core#5, comment 1234567
```

**Complete:** [`examples/flow/complete.yml`](examples/flow/complete.yml), the complete board of `flow`, signed by a Body and an Office throughout.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | Bodies, Posts and Offices at work, as the companion of FLOW, split along its boundary (SPECIFICATION R17) | Holger, commons.o#83, comment 6411242517 |
| 2026-10-26 | revised | The Office's recorded word and an acceptance are checked as records, with what the input cannot establish reported as unverified (the EA's second point) | Holger, commons.o#83, comment 6417155833 |
| 2026-10-26 | adopted | Adopted with the start line (R24) and the session titles (R25) | Holger, commons.o#83, comment 6418348686 |
| 2026-10-28 | revised | H2: R13 binds the Bodies of the discipline and the federation; a commons may choose, for its own CORE, to work on `main` with its topics in items, recorded in its agent file's own guidance | Holger, commons.o#95, comment 6465255055 |
| 2026-10-29 | revised | R13 keeps the worktree rule and points to `flow` R37 for branches and pull requests, and the choice to work on `main` (H2) is struck (6496414850); R19 says *agent-only*, after MODEL's kind `machine` became `agent` (F4). Written for adoption; not yet adopted | Holger, commons.o#100, comment 6495768947 (A7) |
| 2026-10-29 | adopted | Adopted 29 October 2026 | Holger, [commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412) |
| 2026-10-30 | revised | R3 and part 5: the mapping of labels to names lives in the commons' private *settings*, since the glossary keeps *configuration* for the selection of parts (the EA's G) | Holger, [commons.o#98, comment 6522766676](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6522766676) |
| 2026-10-30 | adopted | Adopted 30 October 2026: R3 | Holger, [commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766) |

**Supersedes**

| Text | On adoption |
|---|---|
| `HOW_BODIES_WORK.md` of the discipline, `D2/steward-model.md` | marked; superseded together with `flow` |
| the MODEL and CORE texts, `element-9-posts.md` | superseded for the rules carried below; the rest as `model` and `core` say |

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | a worktree only for parallel writers, removed in the same session (§1, P4) | carried | R13 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | a steward's word recorded by the Office counts, quoted, dated, linked (§1) | carried | R7 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | Body handles are `@Dn-<code>`; cross-commons roles keep their names (§2) | carried | R5 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | every Body cares for the whole; accountability stays with each (§5, E6) | carried | R8 |  |  |
| `../instance/workshop/bodies/D2/steward-model.md` | four functions in every Body (§1) | carried | R1 |  |  |
| `../instance/workshop/bodies/D2/steward-model.md` | verify from another lineage; same lineage written down (§1) | carried | R2 |  |  |
| `../instance/workshop/bodies/D2/steward-model.md` | one Office per accountable human; multiply, never divide (§3) | carried | R6 |  |  |
| `../instance/workshop/bodies/D2/steward-model.md` | bounded delegation needs no second human; a second signature does (§2, I1) | carried | R15 |  |  |
| `../instance/workshop/bodies/D2/steward-model.md` | a planned departure is a handover; an unexpected absence a gap (§2, I2) | carried | R16 |  |  |
| `../instance/workshop/bodies/D2/steward-model.md` | Bodies divide by gravitation, three signs, fold back (§4) | carried | R22 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | a seat with a duty between bodies names where it sits and who sends it (§3.2) | carried | R20 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | D0 is not a fifth agent; identity lives at the centre (§3.3) | carried | R9 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | the default *machine-only Posts not allowed*, adopted or adapted by each commons (§4, E4) | carried | R19 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | `under`, the mandate a serving rests on; Supplier Posts; the accountable human named in every decision (E8, E10, E11, §3) | carried | R21 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | humans decide, agents research and implement (§2.5, §3.1) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | every commons has four core agents, non-negotiable (§3.1) | dropped |  | every commons is worked by five Bodies D0–D4, and D0 is the empty centre | Holger, 20 October 2026 (commons.o#55) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | the Purpose Agent guards D0 and supervises all agents (§3.1–§3.3) | dropped |  | D1 coordinates as a service, not as a hierarchy; the steward function of D0 routes without deciding | Holger, 19 October 2026 (cloudsters.o#55: `HOW_BODIES_WORK` §0) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | a commons needs no application or gatekeeper to begin (§10) | carried | R23 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | maker is not checker; checks run on every change (§1a.1) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | agent files never name an AI product (§3) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | boot is a local conversation; the founder reviews and commits (§6.1) | carried | R23 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | the agent never creates accounts, enters passwords, decides governance, chooses the purpose or commits without review (§6.5) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | secrets, the domain and invitations stay human steps (§2.4) | carried | R18 |  |  |

**Not superseded here**: these rules stay in force in their text until the specification or decision named carries them.

| Text | Rule | Stays until |
|---|---|---|
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | engines under D4, product agents under D3, persona agents under D2; families boot after purpose; the phases Fork to Mature (§3.2–§3.4, §10.1) | the role model of a commons |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | private-first via template; the setup script and guide; the agents' reading order (§2.3, §2.4, §3.1) | core, or a setup text by the rule |

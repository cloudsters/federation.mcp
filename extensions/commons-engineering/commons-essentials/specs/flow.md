---
id: flow
title: Commons FLOW
status: decided
lang: en
touches: [specification, model, core, flow-workshops, flow-graph, flow-bodies, extension, library, graph, mcp]
terms: [commons, model-workshop, commons-workshop, loop, epic, story, task, bug, decision, escalation, body, requirement, branch, pull-request]
schema: schemas/flow.schema.json
check: tools/check_flow.py
supersedes:
  - Commons-Engineering/commons-core@main:.github/ISSUE_TEMPLATE/build.md
  - Commons-Engineering/commons-core@main:.github/ISSUE_TEMPLATE/decision.md
  - Commons-Engineering/commons-core@main:.github/ISSUE_TEMPLATE/deliberation.md
  - ../.github/labels.yml
  - Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_LOOPS_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md
  - ../instance/workshop/bodies/HOW_BODIES_WORK.md
---

# Commons FLOW

*How a commons works on itself: people and machines carry work from a need to a result that orients.*

## 1 · Goal

A commons is worked on by people and machines, from one person to many thousands, and their work loses its aim when it is not tied to what the commons is and wants. This specification is the agile practice of humans and machines for any commons: the work objects with their fields, statuses and templates, the comments, the states from *sent* to *done*, acceptance, loops at work, and the rhythm where human cuts meet machine flow. It decides one thing for its reader: **whether a piece of work is well-formed and anchored**, so that it stays aimed. It draws, as the CORE does, with as few strokes as needed: a work object justifies itself by the orientation it changes or the decided value it fulfils. Three companions hold the rest: [flow-workshops](flow-workshops.md) the three workshops, [flow-graph](flow-graph.md) the edges by which every item is a node of the graph, and [flow-bodies](flow-bodies.md) how Bodies, Posts and Offices take part.

## 2 · Boundary

**Belongs here:** the work objects and their matrix; comments; status and assignee; acceptance and the Decision record; branches and pull requests; loops as they meet the work; rhythm and cuts; the export of a board; how rules of the practice change.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| the three workshops: purpose, who works there, objects, views, rhythm, setup | `flow-workshops` |
| the edges of work: anchors, part of, raised by, carried by, delivered by, observed by | `flow-graph` |
| who takes part and how: the four functions, lineage, client, Offices, handles, start and handover, worktrees | `flow-bodies` |
| the grammar the anchor points into: elements, bindings, addresses | `model` |
| where records live, how they are versioned, the near future on `main` | `core` |
| the form of this text | `specification` |

**Touches** `specification`, `model`, `core`, `flow-workshops`, `flow-graph`, `flow-bodies`, `extension`, `library`, `graph` and `mcp`. **Rests on** the Steward's decisions: the two archetype workshops (21 October 2026), the flow rules and types (23 October), the steward model (24–25 October), the item rule (26 October), FLOW itself, the near future and few strokes (26 October).

## 3 · Terms

All terms resolve in the glossary. One is new with this specification and is added in the same change: [escalation](glossary/terms/escalation.yml).

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | Every piece of work is one item in a workshop of the commons, and what exists only in a message, a session or a local channel is not yet work. | Whatever matters must be findable later by anyone, person or agent. | review |
| R6 | MUST | Every item has one type of Loop, Epic, Story, Task, Bug, Decision and Escalation, and a type the platform holds outside these is reported, never replaced. | The type tells people and agents what kind of work an item is before they read it, and an invented type hides what is really there. | type |
| R7 | MUST | The body of an Epic, Story, Task or Bug holds four fields as level-2 headings in this order: Goal, Approach, Deliverables, Definition of Done. | Four fields are enough to say what is wanted, how, what comes out and when it is done. | fields |
| R8 | MUST | The body is the item's one current state, and a change to a field is made in the body itself. | Whoever opens an item reads where it stands without reading its history. | review |
| R9 | MUST | Every comment is a delivery, a position or a decision, and its first line names its author's handle and its kind. | Three kinds keep a thread short, and the first line tells a reader whether to act. | comments |
| R10 | MUST | A position names the field it would change and gives its reasons. | A position is a proposal to change the state, not an opinion beside it. | comments |
| R11 | MUST | The Goal of an Epic, Story or Bug says in its anchor line whether the work changes an orientation or fulfils one already decided. | Work justifies its stroke by the orientation it changes or the decided value it fulfils, and writing the model is a separate question. | stroke |
| R13 | MUST | A Story hangs under an Epic, and a Task under a Story or an Epic, as a sub-issue on the platform. | A parent named only in text is invisible to people's views and to agents' queries. | parent |
| R14 | MUST | A Definition of Done holds at least one condition that can be checked. | Done that cannot be checked is decided by mood. | done |
| R15 | SHOULD | A Story's Definition of Done names who observes its effect after it is accepted. | Accepting a delivery and observing its effect are two steps, and the second needs an owner. | done |
| R16 | MUST | Every open item carries at least one Body label and no other label. | The Body label is the work address, and every other label blurs it. | labels |
| R17 | MUST | The assignee is the human who must act next, set by whoever hands the item over and removed by whoever completes the step, and an item in Validate always has one. | One field tells every human what waits for them, across all workshops. | assignee |
| R18 | MUST | The status is Backlog when worth doing, Ready when the next verifiable result is clear, In Progress when taken up, Validate when a result is checked against evidence, and Done when closed. | One meaning per status lets every Body read every board the same way. | status |
| R19 | MUST | An item enters In Progress only with a line `taken up:` naming who took it up, and an item sent or delivered is never read as taken up. | Work that was sent but not taken up is the commonest silent loss. | taken-up |
| R20 | MUST | An item is closed only after a decision comment records who accepted it or why it stops, and under which mandate, or links to the record where that stands. | Closing is housekeeping, and the acceptance or the reason to stop is the decision. A word whose authority the record cannot establish is unverified, not accepted. | accepted |
| R21 | MUST | A Decision records the outcome, the scope, the human who decided and the mandate, the statement and where the word was given, and it is closed once recorded. | A decision is relied on because it is recorded once and can be traced to the human who took it. | decision-record |
| R22 | MUST | An Escalation names the loop or Body that raises it and the circle or human it asks, and a human asked is its assignee. | A request for a decision is not the decision, and it waits for someone named. | escalation |
| R23 | MUST | A loop is a contract file of its CORE, bound to one node and carried by one Body, and every run commits a record, a run that finds nothing included. | A loop exists when it leaves its record, and silence must be told apart from absence. | review |
| R24 | MUST | A loop delivers each proposal and escalation as one item whose first line reads `loop: <loop> · id: <id>`, opens no second item for an id, and closes none. | A finding becomes work in one place, and the people it is addressed to decide what happens to it. | loop |
| R25 | MUST | A rhythm is stated by what brings the work back, and a clock may follow from a rhythm but never defines it. | Work that returns by the calendar runs when the date says so, not when the commons needs it. | review |
| R26 | MUST | Humans meet machine work at cuts, selecting at Ready and accepting at Validate, and the machine hands no human more open items than the limit that human states. | Preparation never waits and acceptance never rushes, and human attention is finite. | wip |
| R27 | SHOULD | A change to how people work is bundled into an increment, announced beforehand with what changes for whom, and can be reverted at the next increment. | People take change in at a human pace, and a way back makes change safe. | review |
| R28 | MUST | A decision on purpose, principles or mandates is taken in the annual cycle or in a recorded extraordinary one, with the outside view on record before it. | The weightiest decisions get the slowest rhythm and the outside view. | review |
| R29 | MUST | What a Commons or Project Workshop learns returns as a proposal item in the Model Workshop, which adopts it or refuses it with reasons. | The direction of writing turns learning into silence unless the return has a place and an answer. | review |
| R30 | MUST | A machine finding that needs a human or a change becomes an item with its criterion, place and revision, and a finding that recurs across commons becomes one item on what they share. | Findings printed and thrown away are work lost, and a defect of the form is not a defect of each commons. | review |
| R31 | MUST | An item is cut at the grain at which a human selects or accepts it, and a step an agent takes inside it leaves a commit, not an item. | Items at the grain of agent actions bury the decisions people have to make. | review |
| R32 | SHOULD | Work is cut so that every item ends in a consistent state and can rest at any point. | Work that cannot rest breaks whenever attention moves elsewhere. | review |
| R33 | MUST | A rule of FLOW changes in this specification or in the commons' stated deviation from it, and an item or message only links to it. | Rules changed by message cannot be found where the work happens. | review |
| R34 | SHOULD | The lead of a round consolidates as soon as two contributions are in, and whoever posts a contribution tells the lead and the Office. | Rounds stall when the lead waits for everyone, and contributions in an item go unnoticed. | review |
| R35 | MUST | Every item follows the matrix of part 5: its fields, the statuses it may take, its Stage, the workshops it may be in and its parent. | One matrix lets people and agents read every object the same way in every commons. | matrix |
| R36 | MUST | A board exported from the platform keeps every item's type, memberships and comments as they are, leaves an unknown type unknown and declares any input it could not read completely. | A check judges only what it is given, so an export that drops or invents makes the check lie. | export |
| R37 | MUST | A change to a CORE comes as a pull request from a branch named `<body>/<item>-<topic>` that names its item, whose checks run on it, which only SEED merges (`flow-workshops` R12) and whose branch is deleted after the merge, while the item stays the record of the decision and may have several pull requests, and `main` changes in no other way, SEED's own changes included. | The item says what was decided and why, the pull request how it was made and checked, and a branch that outlives its merge misleads. | review |
| R38 | MUST | Where a task needs more access than its agent's own user holds, the agent names the need and offers to make it a request in the Commons Workshop through `propose` (`mcp` R12), drafting it offline and filing it at the next contact, whoever holds that access takes it up, and no register of others' access is kept beyond the commons' own `access.yml` and Posts. | An agent can know only its own user's access, so the need travels to whoever can meet it, and a register of others' access could be kept only by SEED and CORE and would go stale. | review |

## 5 · Structure

The schema `schemas/flow.schema.json` decides the structure of a **board**: one workshop of a commons and its items, as exported from the platform. Where prose and schema disagree, the schema holds.

| Field | Holds |
|---|---|
| `commons` | the id of the commons |
| `humans` | the handles of the humans who may be assignees |
| `limits` | per human, the most open items assigned at once (R26) |
| `items` | the items, each with `ref` (`owner/repo#n`), `type`, `title`, `state`, `closed_as`, `status`, `stage`, `labels`, `assignees`, `memberships`, `body`, `comments` and `comments_complete`, and the edges and their reading fields of `flow-graph`: `core`, `anchors`, `stroke`, `writes_model`, `parent` (part of), `raised_by`, `carried_by`, `delivered_by`, `observed_by` |

**The matrix of the work objects** (R35). The fields are the item's template, as level-2 headings in this order.

| Object | Fields | Statuses | Stage | Workshops | Parent |
|---|---|---|---|---|---|
| Loop | Definition · Node · Carried by | Backlog, In Progress, Done (retired) | — | model | none |
| Epic | Goal · Approach · Deliverables · Definition of Done | all five | required while open | model, commons, project | none |
| Story | Goal · Approach · Deliverables · Definition of Done | all five | — | model, project | an Epic |
| Task | Goal · Approach · Deliverables · Definition of Done | all five | — | model, commons, project | a Story or an Epic |
| Bug | Goal · Approach · Deliverables · Definition of Done | all five | — | model, commons, project | an Epic, or none |
| Decision | Outcome · Scope · Decided · Statement | In Progress, Done | — | model, commons, project | none |
| Escalation | Raised by · Asked · Question · Definition of Done | Backlog, In Progress, Done | — | model, commons, project | none |

**The anchor line** sits in the Goal: `Anchor: <target> · changes <orientation>` or `· fulfils <decided value>`. Its target, and what the work writes in the model, are edges of [flow-graph](flow-graph.md).

**A comment's first line** names the handle and the kind (`delivery`, `position`, `decision`). A line `taken up: <what> — <who>` is a delivery. An acceptance names who accepted, or why the work stops, and the mandate, or links to where that is recorded.

**An export** (R36) reads every comment and every workshop an item is in. Where it cannot, it sets `comments_complete: false`, and checks that need the history report a gap.

## 6 · Checks

`tools/check_flow.py <board>` reads a board and reports each finding as fail, should or gap; it runs the checks of all four FLOW specifications. `--export OWNER NUMBER KIND COMMONS` writes a board from a project, read-only. Its fixtures are in `tools/tests/flow/`: each probe in `bad/` must fail the check it names.

| Check | Tests |
|---|---|
| `type` | the type is one of the seven; an unknown type is a finding, never a Story (R6) |
| `fields` | the fields of the item's type are there, in order (R7) |
| `comments` | each comment's first line names a handle and its kind; a position names a field (R9, R10) |
| `stroke` | the anchor line of an Epic, Story or Bug says changes or fulfils (R11) |
| `parent` | a Story under an Epic, a Task under a Story or an Epic (R13) |
| `done` | the Definition of Done lists a condition; a Story's names an observer, else should (R14, R15) |
| `labels` | an open item has a Body label and no other (R16) |
| `assignee` | an item in Validate has an assignee; a closed one has none; assignees are humans of the commons (R17) |
| `status` | open is never Done, closed is always Done (R18) |
| `taken-up` | an item In Progress or in Validate has a `taken up:` line (R19) |
| `accepted` | a closed item has a decision comment that names who accepted or why it stops, and the mandate, or links to that record; authority the input cannot establish is a gap, unverified (R20) |
| `decision-record` | a Decision names who decided and under which mandate (R21) |
| `escalation` | an Escalation names who raises it, and a human asked is its assignee (R22) |
| `loop` | a Loop item links its definition; no two open items for one loop id (R24) |
| `matrix` | fields, statuses, Stage, workshops and parent follow part 5 (R35) |
| `export` | the board declares incomplete input; with `--export`, memberships, types and all comments are read (R36) |
| `wip` | no human holds more open items than their stated limit; no limits is a gap (R26) |
| `review` | a reading by the human accountable, or by an agent that has only this file, of R1, R8, R23, R25, R27–R34, R37 and R38 |

**Gap:** the ruleset that lets only SEED merge and the checks on a pull request (R37) are generated by the setup of `flow-workshops` R10 and not yet built; `check_flow` reads no pull requests. Until `propose` runs (`mcp` R12), a member files the request of R38.

## 7 · Example

**Minimal:** a tool library run by one person, with one Epic and one Story in its Model Workshop. In full, [`examples/flow/minimal.yml`](examples/flow/minimal.yml):

```yaml
commons: tool-library
workshop: {kind: model, name: Tool library, core: tool-library}
humans: [ana]
items:
- ref: tool-library/tool-library.core#1
  type: Epic
  title: Lending runs without the founder
  state: open
  status: Ready
  labels: [D4]
  stage: Define
  anchors: ['value-stream:lending']
  stroke: changes
  carried_by: body:d4
  body: |
    ## Goal
    Anchor: `value-stream:lending` · changes who carries lending
    ## Approach
    Hand the lending steps to the desk Body one by one.
    ## Deliverables
    - the desk Body holds `capability:loan-handling`
    ## Definition of Done
    - a month of loans runs with Ana only accepting
```

**Complete:** [`examples/flow/complete.yml`](examples/flow/complete.yml). It holds every work object once, a position, an accepted and closed Task, an Office's recorded word, a loop's escalation and a Loop item.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | Commons FLOW, the agile practice of humans and machines, written by the rule; `[commons]`, never `[org]`; not an operating system | Holger, commons.o#83, comment 6411242517 |
| 2026-10-26 | revised | Extended with a matrix per work object, the workshops per kind and the edges of work in the graph, together with the EA's three points; R2–R5 move to `flow-workshops`, R12 to `flow-graph`; their ids are not reused here | Holger, commons.o#83, comment 6417155833 |
| 2026-10-26 | adopted | Adopted with the matrix, the export, acceptance as a record and the stroke apart from the write; the migration of open items follows the merge | Holger, commons.o#83, comment 6418348686 |
| 2026-10-29 | revised | R37: branches and pull requests embedded in FLOW, from `flow-bodies` R13; `main` changes only by pull request, SEED's own changes included, and the choice to work on `main` (H2) is struck. Written for adoption; not yet adopted | Holger, commons.o#100, comments 6495768947 (A7) and 6496414850 (H2) |
| 2026-10-29 | adopted | Adopted 29 October 2026 | Holger, [commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412) |
| 2026-10-30 | revised | R38: an agent whose task needs more access than its own user holds names the need and offers a request in the Commons Workshop through `propose`, drafted offline and filed at the next contact; whoever holds the access takes it up, and no register of others' access is built (KISS R29) | Holger, [commons.o#98, comment 6524734676](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6524734676), item 3 |
| 2026-10-30 | adopted | Adopted 30 October 2026: R38 | Holger, [commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766) |

**Supersedes**

| Text | On adoption |
|---|---|
| the three issue templates and `../.github/labels.yml` | replaced by the types and the four fields; marked in their repositories |
| the LOOPS manifest and spec, the CORE manifest and spec | superseded for the rules carried below; the rest stays in force as *Not superseded here* says |
| `HOW_BODIES_WORK.md` | superseded together with `flow-workshops` and `flow-bodies` |

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `Commons-Engineering/commons-core@main:.github/ISSUE_TEMPLATE/build.md` | a build task states what, why and acceptance criteria | carried | R7 |  |  |
| `Commons-Engineering/commons-core@main:.github/ISSUE_TEMPLATE/build.md` | its dimension as a label D1–D4 | carried | R16 |  |  |
| `Commons-Engineering/commons-core@main:.github/ISSUE_TEMPLATE/decision.md` | a decision is an issue with decision, context, alternatives, consequences | carried | R21 |  |  |
| `Commons-Engineering/commons-core@main:.github/ISSUE_TEMPLATE/deliberation.md` | a tension before a decision is filed with its options | carried | R22 |  |  |
| `../.github/labels.yml` | dimension, type and priority labels | dropped |  | the Body label is the only label; types are issue types | Holger, 23 October 2026 (commons.o#72: the old labels taken back) |
| `../.github/labels.yml` | the `decision` label | dropped |  | type Decision and the assignee say it | Holger, 23 October 2026 (commons.o#72) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | backlog entries come from deltas loops detected, not from opinion (§11) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | every idea becomes an issue on the board where the commons decides (§11) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | done when the loop that raised the story no longer raises it (§11) | dropped |  | a silent loop may have stopped observing; done is the criterion evidenced, checked, the loop told | Holger, 19 October 2026 (cloudsters.o#55: `HOW_BODIES_WORK` §3) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | priority and acceptance are decided by the commons' own people, never automated (§11) | carried | R20 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | insights reach a commons only as proposals, adopted or refused with reasons (§12) | carried | R29 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_LOOPS_SPEC.md` | a loop exists when it produces its record; a zero-delta run is recorded (§9) | carried | R23 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_LOOPS_SPEC.md` | a loop proposes as issues, never commits to main, never closes issues (§4, §9) | carried | R24 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_LOOPS_SPEC.md` | a loop declares a rhythm; a cadence never defines it (§3) | carried | R25 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_LOOPS_SPEC.md` | a loop lives as one file in the CORE's loop folder with its state (§7.1) | carried | R23 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_LOOPS_SPEC.md` | escalation paths are declared, never improvised (§5) | carried | R22 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | git, issues and the board are the governance layer; work not on the board does not exist (§2.5, §8.3) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | the commit that closes an issue is the decision (§2.5) | dropped |  | closing or merging proves no human decision | Holger, 19 October 2026 (cloudsters.o#55: `HOW_BODIES_WORK` §4) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | labels carry dimension, type and priority (§2.5) | dropped |  | Body labels only | Holger, 23 October 2026 (commons.o#72) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | self-improvement runs as a loop whose output is proposals on the board (§2.6) | carried | R24 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | a change goes issue, review, deliberation, decision, update, propagation (§12) | carried | R33 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | a protected main and a pull-request workflow (§8.3) | carried | R37 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | pre-set labels, the columns Backlog to Done, milestones (§2.2) | dropped |  | Body labels and the status rule replace them | Holger, 23 October 2026 (commons.o#72: flow rules 1–3) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | alignment results go into issues, never back into the rule file (§4) | carried | R30 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | agents propose work as draft issues that humans review and approve (§10.1) | carried | R20 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | the improvement loop proposes through issues and never commits (§10.2) | carried | R24 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | work is reported as a comment in its item (§1) | carried | R9 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | each role commits to its own pushed branch; `main` only by merge on the word (§1, C8) | carried | R37 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | the assignee is the human who must act next (§3, rule 1) | carried | R17 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | the five statuses and their meaning (§3, rule 2) | carried | R18 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | the issue types with exact names, Escalation among them (§4) | carried | R6 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | a Story hangs under its Epic as a sub-issue (§3, rule 3) | carried | R13 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | a Decision is the record; the request is an Escalation (§4) | carried | R22 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | every open item carries a Body label and no other (§4) | carried | R16 |  |  |

**Not superseded here**: these rules stay in force in their text until the specification or decision named carries them.

| Text | Rule | Stays until |
|---|---|---|
| `Commons-Engineering/workshop@main:_manifests/COMMONS_LOOPS_MANIFEST.md` | Story as one delta with its resolution path, Epic as a subgraph; clarification before change; the evaluation formula; cadence sold, scope chosen; the Co-Product Owner (§11–§12) | graph (deltas); a decision on priority; the role model |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_LOOPS_SPEC.md` | the contract keys, levels, classes, directions, adoption, visibility states, retirement and conformance (§2, §4–§8, §10–§12) | a loop contract by the rule |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | priority by board position; experiments private, validated ones shared (§2.5, §2.6) | a decision on priority; library |

**Read, not superseded**: three drafts in `_drafts/werkstatt-bok/` sit in a local repository with no remote, so no other machine can reach them (commons.o#40). Their rules were read; they are held as follows, and the drafts are superseded once they are under version control.

| Text | Rule | Held by |
|---|---|---|
| `_drafts/werkstatt-bok/COMMONS_WORKSHOP_LIFECYCLE_SPEC.md` | a change counts with its binding at a named layer; a change without one is a wish (§4.7) | `flow-graph` R3, R5 |
| `_drafts/werkstatt-bok/COMMONS_WORKSHOP_LIFECYCLE_SPEC.md` | a proposal is adopted, or refused with a reason, and both are recorded (§2.2, §4.8) | R29 |
| `_drafts/werkstatt-bok/COMMONS_WORKSHOP_LIFECYCLE_SPEC.md` | Federation Workshop, the Move and the Mirror (§1, §2, §6) | dropped: the two archetypes are Model and Commons Workshop; the Federation Workshop is legacy (Holger, 21 October 2026 (commons.o#71, W1, W3)) |
| `_drafts/werkstatt-bok/COMMONS_WORKSHOP_LIFECYCLE_SPEC.md` | priority and acceptance never leave the commons and are never automated (§9) | R20 |
| `_drafts/werkstatt-bok/PLAN.md` | new tasks are created as a Story under the matching Epic on the board (header) | R13 |
| `_drafts/werkstatt-bok/PLAN.md` | every package ends consistent and can rest indefinitely (§3.1) | R32 |
| `_drafts/werkstatt-bok/COMMONS_WAYS_OF_WORKING_EPIC_v0.8.md` | no board configuration or operating model is mandatory (status, boundaries) | dropped: FLOW is a deliverable with structure for every commons (Holger, 26 October 2026 (commons.o#83, comment 6411242517)) |
| `_drafts/werkstatt-bok/COMMONS_WAYS_OF_WORKING_EPIC_v0.8.md` | accepted artefacts and observed effects are kept apart; delayed effects get an owner | R15 |
| `_drafts/werkstatt-bok/COMMONS_WAYS_OF_WORKING_EPIC_v0.8.md` | issues at a useful grain, not one per agent action | R31 |
| `_drafts/werkstatt-bok/COMMONS_WORKSHOP_LIFECYCLE_SPEC.md` | the phases and milestones M0–M8, pull not push, the lighthouse, the federation's words (§3–§8, §10–§12) | a federation text |
| `_drafts/werkstatt-bok/COMMONS_WAYS_OF_WORKING_EPIC_v0.8.md` | a baseline and a real-use check before a trial; throughput is never a success measure | iteration of FLOW |

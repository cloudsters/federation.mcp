---
id: flow-workshops
title: Commons FLOW — the workshops
status: decided
lang: en
touches: [specification, flow, flow-graph, flow-bodies, model, core, mcp, library]
terms: [commons, model-workshop, commons-workshop, project-workshop, shell, solution, commons-core]
schema: schemas/flow.schema.json
check: tools/check_flow.py
supersedes:
  - ../instance/workshop/bodies/D4/workshop-definition.yml
  - ../instance/workshop/bodies/D4/workshop-definition.md
  - ../instance/workshop/bodies/HOW_BODIES_WORK.md
---

# Commons FLOW — the workshops

*Where the work of a commons happens: three kinds of workshop, what one does in each, who works there and how.*

## 1 · Goal

A commons works on itself in three kinds of workshop, and people and agents must know without asking where a piece of work belongs, who works there, what it may hold and at what pace it moves. This specification names the Model Workshop, the Commons Workshop and the Project Workshop for any commons: the purpose of each and what one does there, who works in it by the shells of the commons, the views and the rhythm, and how a workshop is set up and recorded. It decides one thing for its reader: **whether a piece of work sits in the workshop it belongs to**, which is where the model is written, used or served by a project. The work objects and their matrix are [flow](flow.md); the edges by which work points into the model are [flow-graph](flow-graph.md).

## 2 · Boundary

**Belongs here:** the three kinds of workshop; their purpose, who works in them, their views and rhythm; the gate by which only the Model Workshop writes the model; setup and record of a workshop.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| the work objects, their fields, statuses and the matrix of where each may be | `flow` |
| what an item writes in the model, as an edge | `flow-graph` |
| who may take part, with which function and mandate | `flow-bodies` |
| the shells themselves | `model` |
| the CORE whose workshop it is | `core` |
| how a platform carries the setup: types, fields, view filters and workflows | its adapter; for GitHub Projects, the reference, `schemas/flow-workshop.yml` |

**Touches** `specification`, `flow`, `flow-graph`, `flow-bodies`, `model` and `core`. **Rests on** the Steward's decisions: the two archetype workshops, with the direction of writing as their boundary (21 October 2026, commons.o#71); Project Workshops alongside (24 October, #84); the views and flow rules (23 October, #72); the shells (24 October, #80); this extension (26 October, #83).

## 3 · Terms

All terms resolve in the glossary. One is new with this specification and is added in the same change: [project-workshop](glossary/terms/project-workshop.yml).

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A commons works in three kinds of workshop, model, commons and project, and every workshop names the CORE whose work it holds by default. | People and agents can tell from a workshop's kind and CORE what may happen in it, and items inherit that CORE (`flow-graph` R2). | workshop |
| R2 | MUST | The Model Workshop is where the commons' model is worked on and released into its CORE, and only an item of the Model Workshop writes the model. | The boundary between workshops is the direction of writing, so every change to the model passes its gate. | workshop |
| R3 | MUST | The Commons Workshop is where people and agents work with the model in their own context, and it holds no Story and nothing that writes the model. | Using the model and writing it are two kinds of work, and the second needs the gate. | workshop |
| R4 | MUST | A Project Workshop serves a purpose of the commons' own with a goal and an end, and an item in it that writes the model is also an item of the Model Workshop. | Work for a project needs a place of its own without a second way into the model. | workshop |
| R5 | MUST | The Model Workshop is worked by the users of SEED and CORE, the pair of the CORE's repository (R12), and from PEER outward a proposal arrives in it only through `propose` of the commons' MCP (`mcp` R12), as an item. | Keeping the model is the work of the innermost shell, and every other shell reaches it by one way in; access comes from a user's shell, never from a Body or Post. | review |
| R6 | MUST | The Commons Workshop is worked by the users of CORE and PEER, and of OPEN where the commons has a repository for PEER and OPEN (R12), and a Project Workshop by whoever its purpose needs, each user within the access of its shell. | Each workshop is open to those whose work it holds, and to no more than their shell grants. | review |
| R7 | SHOULD | Users of DOCK and ROAM, and of OPEN where the commons has no repository for PEER and OPEN, work in no workshop, and what they bring enters as a proposal through `propose` where the commons opens it to them, otherwise carried in by a member. | A low threshold keeps their corrections from being lost. | review |
| R8 | MUST | A workshop has the views Direction, Epics by Stage, Work, the rest by Status, and Workshop, its open items, and a Model Workshop also the view Steward, the open items assigned to whoever reads it, and no view groups by labels. | The same views in every workshop let every person and agent find their next step at once. | setup |
| R9 | MUST | The Model Workshop keeps the rhythm of cuts, increments and the annual cycle, the Commons Workshop follows the pace of its people's own work, and a Project Workshop keeps cuts of its own until its goal is reached or it stops. | The model changes at human cuts, its use flows, and a project ends. | review |
| R10 | MUST | A workshop is set up on a platform that assigns items, shows the views of R8 and holds the statuses of `flow` and the CORE's stage, through an adapter that generates the setup from its CORE, plans it first, applies it on the steward's word and checks it again until nothing is missing and nothing differs, and GitHub Projects with `schemas/flow-workshop.yml` is the reference adapter. | The setup does the same in every commons on any platform, and it never deletes what it does not know. | setup |
| R12 | MUST | A working repository of a commons' workshops serves one pair of shells, whose inner shell merges `main` and whose outer shell pushes branches and proposes by pull request (`flow` R37): SEED and CORE are the pair of the CORE's repository, always, PEER and OPEN have a repository of their own only once the commons grows, which holds the work with the model and never the model, DOCK and ROAM have no repository and reach the commons through its MCP only, and an inner shell reaches every outer repository too, while what a library releases stays readable from a clone of it as `library` R15 keeps it. | Who may write where follows from the pair, so the model stays in the one repository its keepers merge, and the connections between repositories run through users. | review |
| R11 | MUST | Every workshop is recorded in its CORE as a Solution of kind model-workshop, commons-workshop or project-workshop. | A workshop is the system that carries the commons' work on itself, so the model knows it. | review |

## 5 · Structure

The schema is `schemas/flow.schema.json`, the board of `flow`: a board names its workshop's `kind` and `core`, and an item lists its `memberships` and what it `writes_model`. The setup of a workshop is its platform's adapter (R10); the reference is GitHub Projects with `schemas/flow-workshop.yml`, whose `platform: github-projects-v2` and Steward filter `assignee:@me is:open` belong to the adapter, not to R8 or R10.

**The three workshops**, by the shells of the commons. A shell is a group of users, and an agent works under its user's shell:

| Kind | Purpose: what one does there | Who works there | Objects (the matrix of `flow`) | Views | Rhythm |
|---|---|---|---|---|---|
| **Model Workshop** | work on the model and release it into the CORE: proposals are taken in at the entry cut, changes made, checked and graduated | SEED and CORE, in the CORE's repository | all seven | Direction · Work · Workshop · Steward | cuts at Ready and Validate; the increment, at which accepted work graduates; the annual cycle for purpose, principles and mandates |
| **Commons Workshop** | work **with** the model in one's own context: questions, artefacts, services, code; what is learned returns to the Model Workshop as a proposal | CORE and PEER; OPEN where PEER and OPEN have a repository | Epic, Task, Bug, Decision, Escalation: no Story, no Loop | Direction · Work · Workshop | the flow of its people's own work; no cut waits for the Model Workshop |
| **Project Workshop** | a purpose with a goal and an end, such as an engagement, a team effort or a delivery | whoever the purpose needs, within the access of each one's shell | Epic, Story, Task, Bug, Decision, Escalation: no Loop; a Story that writes the model is also in the Model Workshop | Direction · Work · Workshop | its own cuts within its span; it ends when its goal is reached or it stops |

From PEER outward, a proposal to the model enters through `propose` and becomes an item of the Model Workshop (R5). DOCK and ROAM, and OPEN without a repository of its pair, work in no workshop (R7). DOCK is an interface entry into the MCP, not a place of work.

**The working repositories**, one per pair of shells, written SEED|CORE and PEER|OPEN (R12). An inner shell reaches every outer repository too.

| Pair | Repository | Holds | Merges `main` | Pushes branches, proposes by pull request |
|---|---|---|---|---|
| SEED, CORE | the CORE's, always | the model | SEED | CORE |
| PEER, OPEN | its own, only once the commons grows | the work with the model: Commons Workshop items and their artefacts, never the model | PEER | OPEN |
| DOCK, ROAM | none; the MCP only | — | — | — |

**The gate** (R2–R4) is decided by what an item writes, `writes_model` in `flow-graph`, not by the word *changes* in its anchor line. A Story that fulfils a decided change may still write the model, and then it belongs where the gate is.

## 6 · Checks

`tools/check_flow.py <board>` runs these checks with those of `flow`.

| Check | Tests |
|---|---|
| `workshop` | the board names a kind and a CORE; an item that writes the model is in the Model Workshop, or also a member of it; a Commons Workshop holds no Story and nothing that writes the model (R1–R4) |
| `setup` | with `--project`, the setup check of the platform's adapter shows nothing missing or differing, the views of R8 included; without, a gap (R8, R10) |
| `review` | a reading by the human accountable, or by an agent that has only this file, of R5–R7, R9, R11 and R12 |

**Gaps:** `propose` (R5, R7) is specified in the MCP draft and not implemented; until it runs, a proposal from PEER outward is carried in by a member. The teams and rulesets of each repository (R12) are generated from the MCP's `access.yml`, which is drafted and not built. The repository of PEER and OPEN has no check of its own; until it has, `check_flow` is its interim check. GitHub Projects is the only adapter written; a workshop on another platform has no setup check until its adapter is.

## 7 · Example

**Minimal:** a Project Workshop of the tool library, whose one Story writes the model and is therefore also a member of the Model Workshop:

```yaml
commons: tool-library
workshop: {kind: project, name: Repair café, core: tool-library}
items:
- ref: tool-library/repair-cafe#3
  type: Story
  title: The repair café lends tools on Saturdays
  state: open
  status: Backlog
  labels: [D3]
  parent: tool-library/repair-cafe#1
  anchors: ['value-stream:lending']
  stroke: fulfils
  writes_model: ['registry/touchpoints/repair-cafe.yml']
  memberships: [{kind: project, name: Repair café}, {kind: model, name: Tool library}]
  carried_by: body:d3
  body: |
    ## Goal
    Anchor: `value-stream:lending` · fulfils the decided Saturday opening
    ## Approach
    Add the repair café as a touchpoint of lending.
    ## Deliverables
    - `registry/touchpoints/repair-cafe.yml`
    ## Definition of Done
    - the touchpoint is in the model, and the first Saturday is observed
```

**Complete:** [`examples/flow/complete.yml`](examples/flow/complete.yml), a complete Model Workshop of the same commons.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | Per workshop kind: purpose, who works there by shells, objects, views, rhythm; split from `flow` along its boundary | Holger, commons.o#83, comment 6417155833 |
| 2026-10-26 | adopted | Adopted: the three workshops by kind, the gate following the write | Holger, commons.o#83, comment 6418348686 |
| 2026-10-29 | commissioned | Who works where, read by shell as a group of users: SEED and CORE in the Model Workshop, CORE pushing branches and only SEED writing `main`; from PEER outward proposals through `propose` (R5–R7, part 5). Written for adoption; not yet adopted | Holger, commons.o#100 |
| 2026-10-29 | revised | R12: one repository per pair of shells, the inner merging `main`, the outer pushing branches and proposing by pull request; SEED and CORE the CORE's repository, PEER and OPEN one of their own once the commons grows, never holding the model; DOCK and ROAM the MCP only (A6). Written for adoption; not yet adopted | Holger, commons.o#100, comment 6496414850 |
| 2026-10-29 | revised | DOCK belongs to no workshop: an interface entry into the MCP, not a place of work; `check_flow` is the interim check of the repository of PEER and OPEN until it has a check of its own (points 2 and 3). Written for adoption; not yet adopted | Holger, commons.o#100, comment 6500263014 |
| 2026-10-29 | revised | R12 governs the workshops' working repositories; the public release path of a library stays as `library` R15 keeps it, which A6 never meant to remove (the EA's qualifier). Written for adoption; not yet adopted | Holger, commons.o#100, comment 6496414850 (A6) |
| 2026-10-29 | adopted | Adopted 29 October 2026 | Holger, [commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412) |
| 2026-10-30 | revised | R8 and R10 state the function, assignment, the views, the statuses and stage and a checkable setup, and GitHub Projects with `schemas/flow-workshop.yml` is its reference adapter; no second platform is implemented (KISS R29, the EA's E) | Holger, [commons.o#98, comment 6522766676](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6522766676) |
| 2026-10-30 | adopted | Adopted 30 October 2026: R8 and R10 | Holger, [commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766) |

**Supersedes**

| Text | On adoption |
|---|---|
| the workshop definition, `.yml` and `.md` | its content becomes `schemas/flow-workshop.yml`; the files in `bodies/D4/` are marked |
| `HOW_BODIES_WORK.md` | superseded together with `flow` and `flow-bodies` |

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `../instance/workshop/bodies/D4/workshop-definition.yml` | a Model Workshop writes the model; a Commons Workshop never does (kinds) | carried | R2 |  |  |
| `../instance/workshop/bodies/D4/workshop-definition.yml` | a Commons Workshop holds no Story (kinds) | carried | R3 |  |  |
| `../instance/workshop/bodies/D4/workshop-definition.yml` | Project Workshops share types and rules; a model-changing Story is also in the Model Workshop (kinds) | carried | R4 |  |  |
| `../instance/workshop/bodies/D4/workshop-definition.yml` | labels, repository and stage generated from the CORE; plan, apply on the word, check again; never delete (generated_from_core) | carried | R10 |  |  |
| `../instance/workshop/bodies/D4/workshop-definition.yml` | the issue types, labels, fields, workflows and flow checks of a set-up workshop | carried | R10 |  |  |
| `../instance/workshop/bodies/D4/workshop-definition.yml` | the views Direction, Work, Workshop and Steward; never group by labels (views) | carried | R8 |  |  |
| `../instance/workshop/bodies/D4/workshop-definition.md` | a workshop is recorded as a Solution pointing at its project (§2) | carried | R11 |  |  |
| `../instance/workshop/bodies/HOW_BODIES_WORK.md` | the view Steward, `assignee:@me is:open` (§4) | carried | R8 |  |  |

**Not superseded here**

| Text | Rule | Stays until |
|---|---|---|
| `../instance/workshop/bodies/D4/workshop-definition.md` | who runs, supplies and checks the workshops in Commons Engineering | the Bodies' mandates |
| `../instance/workshop/bodies/D4/workshop-definition.md` | one Model Workshop per CORE or per organisation (#84, G2) | the Steward's decision |

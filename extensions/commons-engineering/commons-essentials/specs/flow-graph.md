---
id: flow-graph
title: Commons FLOW — work in the graph
status: decided
lang: en
touches: [specification, flow, flow-workshops, model, core, graph]
terms: [commons, graph, address, requirement, loop, body, post, commons-core]
schema: schemas/flow.schema.json
check: tools/check_flow.py
supersedes: []
---

# Commons FLOW — work in the graph

*Every piece of work is a node of the commons' graph, tied by typed edges to the model it serves and to what it delivers.*

## 1 · Goal

Work stays aimed when it points, in a form a machine can follow, to what in the model it serves, what raised it, who carries it, what delivered it and what showed its effect. FLOW works with the elements of MODEL and the graph that GRAPH serves, so its work has to be part of that graph rather than text beside it. This specification makes every item a node with typed edges, resolved in one definite CORE, and lets views across the model be read from those edges, such as open work per value stream or requirements with no work. It decides one thing for its reader: **whether a piece of work can be found from the model, and the model from the work**. It defines only the edges of work; how the graph is served, stored and queried is GRAPH's.

## 2 · Boundary

**Belongs here:** the node of an item; its six edge types and their targets; the CORE in which targets resolve; what an item writes in the model; the views read from the edges.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| the elements, bindings and addresses the edges point to | `model` |
| where records and claims live, and the near future on `main` | `core` |
| how the graph is stored, served, queried and connected across commons and time | `graph` |
| the work objects and their fields | `flow` |
| which workshop an item that writes the model belongs to | `flow-workshops` |

**Touches** `specification`, `flow`, `flow-workshops`, `model`, `core` and `graph`. **Rests on** the Steward's decision of 26 October 2026 that FLOW needs an understanding of the graph, because it works closely with the elements of GRAPH and MODEL (commons.o#83, comment 6417155833), and on MODEL R18, R22 and R24.

## 3 · Terms

All terms resolve in the glossary. This specification adds none.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | Every item is a node `work:<owner/repo#n>` of the commons' graph, and its edges are typed and point from the work to their target. | Work that is a node can be found from the model it serves, and the model from the work. | edges |
| R2 | MUST | An item resolves its targets in one definite CORE, named by its id as `core` on the item or its workshop and inherited along `part_of`, and a location whose CORE states another id fails. | The same slug can mean different things in different COREs and worlds, and a CORE is referred to by its id, never by where it lives. | resolve |
| R3 | MUST | An Epic, Story or Bug has at least one `anchors` edge to a MODEL address `<kind>:<slug>`, a binding identity `<kind>:<slug>#<field>:<target>` or a requirement `<spec>#R<n>`, and a Task inherits the anchors of its parent. | Work that points nowhere in the model loses its aim, and small work inherits its aim. | edges |
| R4 | MUST | A target the grammar cannot hold fails, a target the CORE does not hold yet is a gap, and no record is invented to resolve it. | A contradiction is an error, an absence is a question, and a check must never be silenced by fiction. | resolve |
| R5 | MUST | An item that writes the model names what it writes in `writes_model`, and only that, not the stroke of its anchor line, decides that it needs the Model Workshop. | Fulfilling a decision can still write the model, and the gate must follow the write. | edges |
| R6 | MUST | Every item has exactly one `carried_by` edge to a Body or a Post of the CORE's element 9, resolved like an anchor, and one taken from the Body label is reported as read from the label. | Every piece of work answers to one carrier, through which accountability resolves to a human, and a label is a work address that grants no authority. | edges |
| R7 | MUST | An item a loop raised has a `raised_by` edge `loop:<id>`, read from its first line. | A finding stays tied to the loop that will observe whether it was resolved. | edges |
| R8 | MUST | A delivery that changes a file names its commit `owner/repo@<sha>` or its pull request `owner/repo#<n>`, which becomes a `delivered_by` edge. | What was delivered must be traceable to the change itself, not to a claim that it happened. | edges |
| R9 | SHOULD | The observation of a Story's effect names a claim `claim:<id>` of kind fact, measure or signal in the CORE's knowledge, which becomes an `observed_by` edge. | An effect is known through an observation the CORE holds, and neither a delivery nor a self-description shows it. | resolve |
| R10 | MUST | An edge is the triple of item, type and target, stated once, and its inverse is never stored. | A fact held in two places drifts, and the graph reads every edge backwards anyway. | edges |
| R11 | MUST | A view across the model, such as open work per value stream, requirements with no work, or elements with neither work nor a loop, is read from these edges and never kept by hand. | A view kept by hand is a second truth that ages. | review |
| R12 | MUST | FLOW defines only the edges of work, and how they are stored, served and queried is GRAPH's. | One specification per concern keeps the edges of work and the graph that carries them from diverging. | review |
| R13 | MUST | An edge the export cannot establish is reported as a gap, never as absent, and an edge read from text names where it was read. | A check must tell what is not there from what it could not see. | resolve |

## 5 · Structure

The schema is `schemas/flow.schema.json`: the edges are fields of an item, and `$defs/target` is the form of an anchor's target.

| Edge (field) | Target | How many | Read from the item |
|---|---|---|---|
| `anchors` | `<kind>:<slug>` (a step `step:<stream>/<step>`), `<kind>:<slug>#<field>:<target>` (MODEL R18, R22) or `<spec>#R<n>` | at least one on Epic, Story and Bug; a Task inherits | the Goal's line `Anchor: <target> · changes … / fulfils …` |
| `part_of` (`parent`) | `owner/repo#n` | 0 or 1 | the platform's sub-issue link |
| `raised_by` | `loop:<id>` | 0 or 1 | the first line `loop: <id> · id: <id>` |
| `carried_by` | `body:<slug>` or `post:<body>.<post>`, a record of element 9 | exactly 1 | the Goal's `Carried by: …`, or else the Body label (`D4` → `body:d4`), reported as read from the label |
| `delivered_by` | `owner/repo@<sha>` or `owner/repo#<n>` | 0 or more | delivery comments naming a commit or pull request |
| `observed_by` | `claim:<id>`, of kind fact, measure or signal | 0 or more | a comment or the Definition of Done naming a claim of the CORE's knowledge |

Two further fields carry no edge and decide its reading. `core` gives the id of the CORE in which targets resolve; the item's Goal may state `CORE: <id>`, and otherwise the workshop's or the parent's holds. Where that CORE lives is a location, declared by the CORE that holds the workshop in its `sources` (`owner/repo@rev`) or given to the check as `--core <id>=DIR`. `writes_model` lists the paths or addresses the work writes, from the Goal's line `Writes: …`; empty when it writes nothing.

**Resolution.** The node kinds are those of MODEL: `dimension`, `family`, `step`, the nine element kinds and `post`. A MODEL address resolves to a record of the CORE's registry by kind and slug, and a binding identity to that record's field naming the target. A dimension resolves to `d0`–`d4`, a family to the thirteen families. A Body or Post of `carried_by` resolves to a record of element 9. A requirement resolves to a row of part 4 of `<spec>.md` in the CORE's specifications folder (`specs/`, CORE). A claim of `observed_by` resolves in the CORE's `knowledge/`, and its kind is read. Unreachable is a gap; malformed is a fail (R4, R13).

**Views read from the edges** (R11), as GRAPH will serve them:

| View | Read as |
|---|---|
| open work per value stream | `anchors` read backwards from each `value-stream:` target, over open items |
| requirements with no work | requirements of the CORE's specifications that no item `anchors` |
| elements with neither work nor a loop | records of the CORE that no open item anchors and no loop is bound to |
| what a Body carries | `carried_by` read backwards |
| delivered but not observed | accepted Stories with `delivered_by` and no `observed_by` |

## 6 · Checks

`tools/check_flow.py <board>` runs these checks with those of `flow`. `--core <id>=DIR` names where the CORE of that id is checked out, and `--edges` prints every edge as a triple, one per line.

| Check | Tests |
|---|---|
| `edges` | each edge has its type's form and count; Epic, Story and Bug anchor, a Task inherits; one `carried_by`; no edge twice (R1, R3, R5–R8, R10) |
| `resolve` | with `--core <id>=DIR`, every target resolves in the item's CORE, `carried_by` in element 9 and `observed_by` in `knowledge/` by its kind; a location whose CORE states another id fails; malformed fails, not held is a gap; a self-description as observation is a should; without a location, a gap; an edge the export could not establish is a gap (R2, R4, R6, R9, R13) |
| `review` | a reading by the human accountable, or by an agent that has only this file, of R11 and R12 |

## 7 · Example

**Minimal:** the Story of the tool library with its edges, in the board of `flow`:

```yaml
commons: tool-library
workshop: {kind: model, name: Tool library, core: tool-library}
items:
- ref: tool-library/tool-library.core#2
  type: Story
  title: Returns are logged by the desk
  state: open
  status: Validate
  labels: [D4]
  assignees: [ana]
  parent: tool-library/tool-library.core#1
  anchors: ['capability:loan-handling']
  stroke: changes
  writes_model: ['registry/bodies/d4.desk.yml']
  carried_by: body:d4
  delivered_by: ['tool-library/tool-library.core@3f2a1c0']
  body: |
    ## Goal
    Anchor: `capability:loan-handling` · changes who logs a returned tool
    Writes: `registry/bodies/d4.desk.yml`
    ## Approach
    The desk agent logs each return.
    ## Deliverables
    - the desk Body holds `capability:loan-handling`
    ## Definition of Done
    - ten returns logged and accepted by Ana
```

**Complete:** [`examples/flow/complete.yml`](examples/flow/complete.yml), where every item carries its edges.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | Work in the graph: every item a node with typed edges (anchors, part of, raised by, carried by, delivered by, observed by), resolved in a definite CORE; views read from the edges; FLOW defines only the edges of work, GRAPH serves them | Holger, commons.o#83, comment 6417155833 |
| 2026-10-26 | adopted | Adopted with D1-CE's four corrections: `core` as the CORE's id with a declared location; the kinds `family` and `step`; `carried_by` resolved in element 9; `observed_by` as an observation | Holger, commons.o#83, comment 6418348686 |

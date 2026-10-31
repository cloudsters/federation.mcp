---
id: model
title: Commons MODEL
status: decided
lang: en
touches: [specification, core, library, graph, mcp, flow, extension]
terms: [commons, scaffold, dimension, value-stream-family, value-stream, value-stream-step, capability, entity, stakeholder, journey, touchpoint, value-exchange, solution, body, post, shell, address, extension, essentials]
schema: schemas/model.schema.json
check: tools/check_model.py
supersedes:
  - Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/ENTITY_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/ADDRESSING_SPEC.md
  - ../instance/workshop/bodies/D1/element-9-posts.md
---

# Commons MODEL

*The grammar of any commons: the kinds of things that exist in it, and how they bind.*

## 1 · Goal

Every commons, and every specification that speaks about one, needs the same words for the same things. Without them, two commons cannot be compared, and an agent cannot tell a sentence about a commons from noise. This specification is that grammar. It names the nine elements of a commons, the five dimensions and thirteen families its value streams belong to, the steps and the capability map they meet at, and the bindings between them. It decides one thing for its reader: **whether a statement about a commons is well-formed in the shared grammar**. It does not decide whether the statement is true. A commons keeps its own words beside the grammar, and extensions add to it without redefining it.

## 2 · Boundary

**Belongs here:**
- the kinds of record: the nine elements, plus the Post within a Body;
- the closed vocabularies: dimensions, families, capability levels;
- the bindings every record must state, even when not yet known;
- the address by which anything outside the model points into it;
- the rules that keep the grammar universal.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| where records live, how they are versioned, how certain a statement is (expected · assumed · claimed · evidenced) | CORE |
| people: the party register, names and contacts | CORE |
| who takes part and how: function, lineage, client, Offices, Supplier Posts, rhythms | FLOW |
| record fields beyond the minimum; which streams, capabilities and entities a domain proposes | EXTENSION, and each extension |
| patterns, and how they come to be addressed | LIBRARY |
| how records connect over time and across commons | GRAPH |

**Touches** the other seven specifications.

**Rests on** the decisions that formed this grammar: the thirteen families 4/3/3/3; D0 named *Perception & Identity* (14 October 2026); element 9 the Body with Posts (18 October 2026); Posts with serving and accountability (22 October 2026, P1–P5); the Body and Post records and the person reference (25 October 2026, S3.1, S3.2); the shell words (24 October 2026).

## 3 · Terms

All terms resolve in the glossary. Two are new with this specification and are added in the same change:
- [shell](glossary/terms/shell.yml);
- [address](glossary/terms/address.yml).

The terms `ring` and `orbit_level` go to the rejected list, in favour of *shell*.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A model is a set of records, each naming its `kind` as one of the nine elements or as a `post` within a Body, and validating against `model.schema.json`. | Every statement about a commons is a statement about one of these kinds, or it is not about the commons' value creation. | schema |
| R2 | MUST | Every record has a `slug`, unique among the records of its kind and never reused, and a `title`. | Bindings, addresses and other commons point at the slug; a reused slug silently changes what they point at. | slugs |
| R3 | MUST | The dimensions are `d0` to `d4` and the families are the thirteen of part 5, and neither a commons nor an extension renames, adds or drops one. | Identical families make every commons comparable with every other, so that no system can be played off against another. | schema |
| R4 | MUST | Every value stream names exactly one family, and a dimension written on it agrees with that family's. | The stream is where a commons is itself; the family is where it stays comparable. | family |
| R5 | MUST | Every value stream has at least one step, and every step states the capabilities it requires and the entities it acts upon. | The step is where the value streams meet the capability map; without it, a capability floats. | schema |
| R6 | MUST | A capability binds to a value stream only through a step, and a step or a solution binds capabilities at L3. | One capability serves many streams; a tree of copies under each stream hides that. | capability-map |
| R7 | MUST | Capabilities form one map from L0 to L5, in which every node below L0 names exactly one parent one level up. | One map lets a commons see the same ability carrying many streams at once. | capability-map |
| R8 | MUST | A capability or an entity states neither a dimension nor a family, because its position is derived from the steps that bind it. | An asserted position drifts from the work; a derived one cannot. | schema |
| R9 | MUST | A journey states its stakeholder and the value stream it mirrors, a touchpoint its journey and the steps it serves, a value exchange its touchpoint with what is offered and what returns, and a solution the capabilities it carries. | Each element is defined by what it binds; a record without its bindings is prose about the commons, not a model of it. | schema |
| R10 | MUST | A binding names a record of the model by slug, a step as `<stream>/<step>`, and a binding that names nothing yet, or an empty list, is a gap. | Missing is a legitimate state and the next question to ask, not an error. | bindings |
| R11 | MUST | The model holds kinds, never individuals: no record holds a person's name, e-mail address or telephone number, and a person enters only by identifier, in a Post. | A model of value creation needs no personal data, so it holds none. | no-persons |
| R12 | MUST | No slug is both a stakeholder and an entity. | A stakeholder stands at the edge and is represented by entities; it is not one of them. | kinds-apart |
| R13 | MUST | A Body states its form, the Body it is part of or `null` for the outermost, and its mandate, has at least one Post held by a human, and is never part of itself through its chain. | The mandate persists while people, agents and work change; the Body carries it, inside a whole that closes, and a council of agents alone answers to no one. | bodies |
| R14 | MUST | A Body holds capabilities only at L0 to L3, and holding a node holds its subtree. | A Body answers for a scope, and an activity is not a scope. | capability-map |
| R15 | MUST | A Post states its Body, its responsibility, who serves it and who is accountable for it, and `accountable` is always set, to a human by identifier or to a Body as `body:<slug>`, which resolves through that Body's steward Post `<body>.steward` and then through `part_of` to a human. | Serving can be shared with machines; accountability is never vacant. | accountable |
| R16 | MUST | Every serving entry names whether a human or an agent serves, by identifier, and an agent entry also names its brief. | Who acts must be visible, and an agent acts only on a written brief. | schema |
| R17 | MUST | A Post served by agents only carries safeguards: its evals, its kill switch, its scope and its review. | Where no human serves, the limits must be stated before anything acts. | safeguards |
| R18 | MUST | Whatever refers to the model from outside it does so by an address that names its source by reference in `from`, one node of the grammar by kind and slug, a weight, a status and the method that produced it. | Recognising a piece of evidence as an element is a mapping with a certainty, and confirmed mappings are what the grammar learns from. | schema |
| R19 | SHOULD | A stakeholder names the one shell it stands in, and only stakeholders, journeys, touchpoints and value exchanges name shells. | A shell is closeness to the model, and only those who meet the commons stand somewhere near it. | shells |
| R20 | SHOULD | An extension adds value streams, steps, capabilities, entities and fields, and redefines no element, dimension or family. | A domain is itself in its streams; it stays comparable in the grammar. | review |
| R21 | MUST | The families and dimensions of part 5 agree with the canon data from which extensions generate their value models, which also holds each family's placement profile and grounding. | Two sources for the same thirteen names drift apart. | canon |
| R22 | MUST | Every binding has the derived identity `<kind>:<slug>#<field>:<target>`, a step's binding `value-stream:<stream>/<step>#<field>:<target>`, and no binding is stated twice. | Moving an ability to another solution or Body is a change of the model, and a loop can only review a change it can name. | binding-ids |
| R23 | MUST | Accountability that ends in a cycle, at an open end or outside the model is a gap, and no check of the model grants authority to act. | Describing a model and permitting an act are two things; a green check is the first only. | accountable |
| R24 | MUST | An address whose target the grammar cannot hold fails, one whose target this model does not hold yet is a gap, and only a ratified address to a held target counts as recognition. | A contradiction is an error, an absence is a question, and recognition must rest on something that is there. | addresses |
| R25 | MUST | A touchpoint's stakeholder is its journey's, and a touchpoint that writes a different one fails. | A touchpoint is where a journey meets the commons; two stakeholders there would be two touchpoints. | coherence |
| R26 | MUST | A family is broad enough to hold all of its value streams across every stakeholder and asset, and a quality the whole embodies is never a family or a dimension. | Families are decided and streams discovered; a family that holds one value is a stream in the wrong place. | review |
| R27 | MUST | A commons' own word for a record is kept beside it in `stated_as`, and the grammar's name is never renamed to match it. | The commons recognises itself in its words, and stays comparable in the grammar's. | review |
| R28 | MUST | In a CORE of `instance_type: extension`, a field missing from a journey, touchpoint, value exchange, solution, Body or Post is a gap, while value streams, steps and capabilities keep the grammar in full. | An archetype offers a kind of record; what it binds to is stated by the commons that adopts it, and the menu's own grammar must still hold. | bindings |

## 5 · Structure

The schema is `schemas/model.schema.json`. A model is `records`, optionally with `addresses`. Each record carries `kind`, `slug` and `title`, plus the bindings of its kind. Extensions may add fields; the schema leaves room for them. A record a commons adopted from an extension names its origin in `adopted_from`, and an extension marks its starting set with `start` (`extension` R23, R24). A commons marks a record that carries it with `essential: true`: its decisive selection, as the views read it.

| # | Element | States (required) | Optional |
|---|---|---|---|
| 1 | **stakeholder** | — | `shell` |
| 2 | **journey** | `stakeholder`, `mirrors` (a value stream) | `shells`, in the order crossed |
| 3 | **touchpoint** | `journey`, `steps` | `stakeholder`, which must be the journey's; `shell` |
| 4 | **value-exchange** | `touchpoint`, `offered`, `returned` | `shell` |
| 5 | **value-stream** | `family`, `steps` (each: `slug`, `title`, `capabilities`, `entities`) | `dimension`, which must agree |
| 6 | **capability** | `level` (L0 to L5), `parent` (`null` at L0) | — |
| 7 | **entity** | — | — |
| 8 | **solution** | `carries` (L3 capabilities) | — |
| 9 | **body** | `form` (`governing-body`, `organisational-unit`), `part_of` (always written, `null` for the outermost Body), `mandate` | `holds` (L0 to L3); absent is the same gap as `[]` |
| 9 | **post** | `of`, `responsibility`, `accountable`, `held_by` (each: `kind`, `id`, and `brief` for an agent) | `safeguards` (`evals`, `kill_switch`, `scope`, `review`) |

**The thirteen families**, by dimension:

| Dimension | Families |
|---|---|
| `d0` Perception & Identity | `perception-to-mandate` |
| `d1` Purpose & System | `purpose-to-portfolio` · `value-to-sustainability` · `portfolio-to-system` |
| `d2` Participation & Relationship | `participant-to-community` · `collaboration-to-automation` · `contributor-to-succession` |
| `d3` Proposition & Exchange | `discovery-to-usage` · `interest-to-relationship` · `proposition-to-audience` |
| `d4` Production & Resilience | `demand-to-fulfillment` · `source-to-alliance` · `acquire-to-retire` |

**A binding** is a field of a record that names another, and its identity is derived, with no catalogue of its own: `solution:lending-ledger#carries:loan-handling`, or for a step `value-stream:lending/hand-out#entities:tool`. **A changed binding** is one identity removed and another added. Moving loan handling to a new solution removes `solution:lending-ledger#carries:loan-handling` and adds `solution:loan-app#carries:loan-handling`. `check_model.py --bindings` lists them, so two revisions can be compared.

**Accountability** set to `body:<slug>` resolves to the `accountable` of that Body's steward Post, `<body>.steward`. Where the Body has none, it resolves to the Body it is `part_of`, until a human is reached. A cycle, an outermost Body without a steward Post, or a Body not in the model is a gap: the accountability is held outside the model, or not yet stated.

**An address** names `from` (a reference to what refers: a path, `owner/repo@rev:path` or a URL), `to` (a node: its `kind` and `slug`, a step as `<stream>/<step>`), a `weight` from 0 to 1, a `status` (`proposed`, `ratified`, `rejected`) and its `source`, meaning the method (`machine`, `curated`, `human`). A target the grammar cannot hold, such as a family that does not exist, is a **contradiction** and fails. A target this model does not hold yet is an **absence** and a gap. Only a ratified address to a held target counts as recognised.

**Two rules keep the families universal.** A family is broad enough to hold all of its streams, across every stakeholder and asset. A family is a function the commons performs, and a quality the whole embodies (resilience, justice, vitality) is never a family or a dimension.

## 6 · Checks

`tools/check_model.py <model>` reads a model, either one file with `records` or a folder of record files. It reports **fail**, **should** or **gap**, and exits with 1 only on a fail. **A green check describes the model; it grants no authority to act.** Its fixtures are in `tools/tests/model/`.

| Check | Tests |
|---|---|
| `schema` | the model validates against the schema (R1, R3, R5, R8, R9, R16, R18) |
| `slugs` | no slug appears twice within a kind (R2) |
| `family` | a stream's written dimension agrees with its family's (R4) |
| `bindings` | every binding resolves; what names nothing yet, an empty list or an absent `holds` is a gap (R10); with `--extension`, so is a field an archetype leaves to the commons (R28) |
| `binding-ids` | no derived binding identity appears twice (R22) |
| `capability-map` | parents one level up; steps and solutions bind L3; Bodies hold L0 to L3; an L3 that no step binds is a gap (R6, R7, R14) |
| `no-persons` | no e-mail address or telephone number anywhere, and identifiers only in a Post (R11) |
| `kinds-apart` | no slug is both a stakeholder and an entity (R12) |
| `bodies` | no Body is part of itself through its `part_of` chain; a Body whose Posts are all held by agents fails, and one with no Post held by a human yet is a gap (R13) |
| `accountable` | a Post's Body resolves, and a `body:` accountability resolves to a human; a cycle, an open end or accountability outside the model is a gap, and so is a Post nobody serves now (R15, R23) |
| `safeguards` | an agent-only Post carries all four safeguards (R17) |
| `addresses` | an address's target resolves to a node of its kind; a contradiction fails and an absence is a gap (R24) |
| `coherence` | a touchpoint's written stakeholder is its journey's (R25) |
| `shells` | shells only where R19 allows them, and on every stakeholder (R19) |
| `canon` | the families equal those of the canon data, when it is at hand (R21) |
| `review` | a reading by the human accountable for this specification's mandate, against the Why of R20, R26 and R27 |

## 7 · Example

**Minimal:** one value stream with one step. Its capabilities, its entities and the journey that mirrors it are not yet known, so the check reports three gaps and no fail:

```yaml
records:
  - kind: value-stream
    slug: grow-and-share
    title: Grow and share
    family: demand-to-fulfillment
    steps:
      - {slug: sow, title: Sow, capabilities: [], entities: []}
```

**Complete:** [a neighbourhood tool library](examples/model/tool-library.yml), with every element, both halves of its exchange, a capability map from L0 to L3, two Bodies (the outermost with `part_of: null`) and three Posts (a steward, and one served by an agent with its safeguards, accountable to its Body), and one address. The check reports 0 fail, 0 should and 0 gaps.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | Commons MODEL, the grammar of any commons, comes second of the eight, after SPECIFICATION; later iteration is expected | commons.o#88, opened on the word of the human accountable |
| 2026-10-26 | adopted | Adopted after six points: derived binding identities, accountability ending in a human, addresses with a source and resolving targets, the step address pattern, an absent `holds` as a gap, `part_of: null` stated and shown; and a green check | Holger, commons.o#88, comment 6414397147 |
| 2026-10-26 | revised | **Draft, contingent on the probe of commons.o#90 and not decided:** the record fields `adopted_from` and `start` (part 5); `essential`, the commons' own mark of a record that carries it, asked for by the Model Engine for Part II (6422822870); R28, the archetypes of an extension leave open what the commons binds (D4-CE's P2 of the probe) | Holger, commons.o#90 (the principle, contingent on the probe 6421206970; not yet decided) |
| 2026-10-29 | revised | R13: a Body is a council with at least one Post held by a human; a Body held by agents only fails, one without a human Post yet is a gap (part 6). Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)) | Holger, commons.o#100 (opening, verbatim: *"ist immer ein Gremium mit mindestens einem human-post"*) |
| 2026-10-29 | revised | The serving kind `machine` is renamed `agent`, in the grammar, its schema, its checks and every fixture (R13, R16, R17, part 5); an address's `source: machine` names a method and stays. Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)) | Holger, commons.o#100, comment 6495768947 (F4: *"ja, agent wird sich vermutlich als gebräuchlich durchsetzen"*) |

**Supersedes**, each text in part: what this specification carries or drops is in the carry-over table, and what it does not supersede stays in force in that text until the specification named for it is adopted. The marks say the same.

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | one architecture: the families are universal, a domain is itself in its value streams (§1, §2, §6) | carried | R20 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | the thirteen families, 4/3/3/3, inherited unchanged by every extension (§3, §6) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | the scope rule (§2.1) | carried | R26 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | families are functions, qualities are properties (§3.1) | carried | R26 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | the agency line: contributors with agency in D2, tools without agency in D4 (§3.2) | carried | R21 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | the standard is not renamed; the commons' word is kept beside it (§5.1) | carried | R27 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | nine elements, in the order a stakeholder meets the commons (§2) | carried | R1 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | a binding has an identity of its own (§2) | carried | R22 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | journey and value stream are one exchange seen from two sides (§2) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | the model holds archetypes, not people (§2.0) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | entities are not stakeholders (§2.1) | carried | R12 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | a seat is held by a stakeholder in the serving stance, `stance` served or serving (§2.2) | dropped |  | element 9 is the Body with Posts; who serves is a Post's `held_by` | Holger, 18 October 2026 (K1–K4, V2; glossary `body`) |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | the gradient D0, VSD, VSF, VS and step (§3) | carried | R4 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | dimensions joined by "&", families named "A to B"; D0 is Perception & Identity (§3, note) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | capabilities are not a level of the gradient (§3) | carried | R6 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | one capability map from L0 to L5, a tree (§3.1) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | a step binds L3 capabilities and the entities it acts upon; a solution carries L3 (§3.2) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | a seat holds capabilities at the level of its scope, L0 to L3, and holding a node holds its subtree (§3.2) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | a capability's position is derived, and one no step binds stands nowhere (§3.3) | carried | R8 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | families are decided, value streams are discovered (§4.0) | carried | R26 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | the scope rule; functions and qualities; thirteen by design (§4) | carried | R26 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | every element carries its own identity and its address in the canon (§5) | carried | R2 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | the extension proposes, the commons fills; element structures are developed in the extensions (§6, §6.1) | carried | R20 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | conformance 6: a value stream without a journey counterpart (§7) | carried | R10 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | conformance 10: a step that binds no L3 capability (§7) | carried | R10 |  |  |
| `Commons-Engineering/workshop@main:_specifications/ENTITY_SPEC.md` | the entity's place: element 7, the nouns the capabilities act upon, apart from stakeholders (§1) | carried | R12 |  |  |
| `Commons-Engineering/workshop@main:_specifications/ENTITY_SPEC.md` | an entity's position across D0–D4 is not asserted (§3) | carried | R8 |  |  |
| `Commons-Engineering/workshop@main:_specifications/ENTITY_SPEC.md` | the Markdown archetype format: frontmatter, body structure and validation (§4–§6) | dropped |  | never built; element structures are developed in the extensions | Holger, 22 September 2026 (COMMONS_MODEL_SPEC §6.1) |
| `Commons-Engineering/workshop@main:_specifications/ENTITY_SPEC.md` | instances filed by dimension in `7_entities/{dimension}/` (§7) | dropped |  | the dimension is derived, and records sit flat in their folder | Holger, 7 October 2026 (COMMONS_MODEL_SPEC §2.3) |
| `Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md` | the model holds archetypes; who holds a seat is evidence beside it (§3) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md` | a seat exists with or without a holder; `holder: null` is never a defect (§4.1, §9.5) | carried | R15 |  |  |
| `Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md` | `stated_as`: the house's word, never translated, never renamed (§4.3) | carried | R27 |  |  |
| `Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md` | no private contact datum, inferred attribute or assessment of a person in the model (§6) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_specifications/ADDRESSING_SPEC.md` | the address: a node, a weight, a status from proposed to ratified or rejected, and a source (§3) | carried | R18 |  |  |
| `Commons-Engineering/workshop@main:_specifications/ADDRESSING_SPEC.md` | only a ratified address counts (§3, §5) | carried | R24 |  |  |
| `Commons-Engineering/workshop@main:_specifications/ADDRESSING_SPEC.md` | principles ground the families: `grounded_in` on every family (§2a) | carried | R21 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | the Body and Post records and their required fields (§1) | carried | R13 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | `accountable` is always set and resolves to a human through the Body's chain (§2, E1) | carried | R15 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | an open end or a cycle in accountability is a gap (§2, E1) | carried | R23 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | a serving entry names kind and id, a machine also its brief (E2) | carried | R16 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | a machine-only Post carries its four safeguards (§4, E3) | carried | R17 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | no personal datum in the records of element 9 (E7) | carried | R11 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | `of`, `part_of` and `mandate` resolve, and an open one is a gap (E8) | carried | R10 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | a vacant Post is a gap, never a defect (E9) | carried | R15 |  |  |
| `../instance/workshop/bodies/D1/element-9-posts.md` | the diagnosis of a model is kept apart from permission to act (§5) | carried | R23 |  |  |

**Not superseded here**: these rules stay in force in their text until the specification named carries them.

| Text | Rule | Stays until |
|---|---|---|
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | the spoken form, seven beats (§3.3) | core |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | naming: enterprise-legible, "A to B" for families, noun phrases for value streams (§5) | extension |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_VALUE_CREATION_MANIFEST.md` | the house-vocabulary table, and the promotion path as the only route by which the canon changes (§5.1) | library |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | the graph is fractal: every stakeholder is a system, coupled at a shared touchpoint (§2) | graph |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | the element folders, and migration as a run with earlier names as fallback (§2.3; conformance 8) | core |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | an extension ships L0–L3 with its essentials and L4–L5 with its enhanced body (§3.1) | extension |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | a seat with a duty between bodies names where it sits and who sends it (§3.2) | flow |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | D0 is not a fifth agent; identity lives at the centre (§3.3) | flow |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_MODEL_SPEC.md` | the model addresses the library; the library never questions the model (§5) | library |
| `Commons-Engineering/workshop@main:_specifications/ENTITY_SPEC.md` | an entity's two lives, definition in the extension and instance in the commons; the four entity types (§2, §3) | extension |
| `Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md` | the register and the harbour: who stands where, apart from what passed between us and them (§3) | core |
| `Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md` | the register's fields and validation: `via`, `source` per assertion, `status`, the three visibilities, the declared exclusions (§4, §6, §9) | core |
| `Commons-Engineering/workshop@main:_specifications/STAKEHOLDER_REGISTER_SPEC.md` | what an extension may shape and may never relax (§11) | core |
| `Commons-Engineering/workshop@main:_specifications/ADDRESSING_SPEC.md` | depth follows generality, the signals, the review gate, curated before machine, and `concerns` for edge observations (§2, §4, §5) | library |
| `../instance/workshop/bodies/D1/element-9-posts.md` | the default *machine-only Posts not allowed*, adopted or adapted by each commons (§4, E4) | flow |
| `../instance/workshop/bodies/D1/element-9-posts.md` | resolving `github:` to its id, and the party register `people.yml` (§2, §3, E5, E6) | core |
| `../instance/workshop/bodies/D1/element-9-posts.md` | `under`, the mandate a serving rests on; Supplier Posts; the accountable human named in every decision (E8, E10, E11, §3) | flow |

The canon data `value-creation-canon.yml` is not superseded. It stays the source from which extensions generate their value models, and R21 keeps the two in agreement.

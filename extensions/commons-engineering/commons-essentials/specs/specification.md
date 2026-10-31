---
id: specification
title: Commons SPECIFICATION
status: decided
lang: en
touches: [model, core, library, graph, mcp, flow, extension]
terms: [commons, specification, requirement, decision, extension, essentials, kiss]
schema: schemas/specification.schema.json
check: tools/check_spec.py
examples: [examples/specification/opening-hours.md]
supersedes: [../commons-as-code/README.md]
---

# Commons SPECIFICATION

*How a commons specifies what it requires, so that people and machines read the same thing, build it and test it.*

## 1 · Goal

A commons states what it requires in specifications. People and agents build, run and apply the commons from the same files. A specification therefore has to be understood, implemented and checked by both of them, without anything said around it. This rule is the form every specification of a commons follows, this one included. It decides one thing for its reader: **whether a text is a specification the commons can rely on**, meaning its requirements are testable, checked and decided. The measure is sufficiency, not depth: a specification says what is needed for that decision, in as few strokes as needed.

## 2 · Boundary

**Belongs here:** the form of any specification of any commons:
- its parts;
- how a requirement is written;
- its schema and its checks;
- its examples;
- its decisions;
- what it supersedes.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| what any specification requires | the specification itself |
| where specifications live in a commons | CORE |
| how work on a specification moves (items, iterations, rounds, reviews) | FLOW |
| the form of a glossary term | the glossary's own schema |
| patterns | LIBRARY |

A specification holds what is required, not the debate about it.

**Touches.** This rule is the first of eight central specifications, and it touches the remaining seven. Each is written from the view of any commons:

| Specification | Answers for a commons |
|---|---|
| **model** | its grammar: dimensions, families, value streams, entity model, the nine elements, their rules |
| **core** | its statements in that grammar, versioned, on the near future |
| **library** | the knowledge it draws on, patterns included |
| **graph** | how its statements connect: within it, over time, with other commons |
| **mcp** | machine access |
| **flow** | how it works on itself: the agile practice of humans and machines |
| **extension** | how it adopts a domain |

This rule is part of the Commons Essentials Extension. A commons adopts it as it stands, and states only where it deviates (R20).

## 3 · Terms

The terms in the front matter resolve in the commons' glossary. Two of them are new with this rule, and they are added to the glossary in the same change:
- [specification](glossary/terms/specification.yml);
- [requirement](glossary/terms/requirement.yml).

Every other word keeps its ordinary meaning.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A specification is one Markdown file named `<id>.md`, whose YAML front matter validates against this rule's schema `specification.schema.json`, while its own `schema` field names the schema of its subject. | People read Markdown; machines read the front matter. One file keeps the two channels together. | front-matter |
| R2 | MUST | The body has eight parts in this order, each a level-2 heading that begins with its number, 1 Goal, 2 Boundary, 3 Terms, 4 Requirements, 5 Structure, 6 Checks, 7 Example and 8 Decision log, and part 1 is one paragraph that names the decision or orientation the specification carries. | Every reader, human or agent, finds the same thing in the same place, in any language, and a specification that carries no decision has no reason to exist. | parts |
| R4 | MUST | Part 2 says what belongs and what does not, and every specification it touches is listed in `touches`. | Boundaries keep two specifications from requiring the same thing differently. | touches |
| R5 | MUST | Every term in `terms` resolves in the commons' glossary; a new term is added to the glossary in the same change and is never defined in the specification alone. | One source per term; a word defined in two places drifts. | terms |
| R6 | MUST | Part 4 holds one table with the columns ID, Level, Requirement, Why and Check, one row per requirement. | A table is read by people and parsed by machines without a second copy. | table |
| R7 | MUST | Requirement ids are unique within the specification and are never reused for a different requirement. | Other specifications, checks and work items cite `<id>#R<n>`; a reused id silently changes what they cite. | ids |
| R8 | MUST | The level is MUST or SHOULD, and a failed MUST fails the check while a failed SHOULD is reported without failing. | Implementers must know what blocks and what only informs. | levels |
| R9 | MUST | A requirement is one testable sentence, and its Why says in one or two sentences which decision it carries. | The machine channel says what holds; the intent channel says why. Agents need both to apply a rule to a case nobody foresaw. | two-channels |
| R10 | MUST | Every requirement names exactly one check: `schema` for validation against its schema, `review` for a judgement no machine can make, or a check id that part 6 lists for the tool named in `check`. | A requirement nobody can test is a wish, and a check that resolves nowhere is one too. | checks |
| R11 | MUST | Part 5 names the schema file that decides the structure; where prose and schema disagree, the schema holds and the disagreement is a defect. | Prose explains; the schema decides. | schema |
| R12 | MUST | An absent optional part, file or relation is reported as a gap and fails only where a MUST requires it. | Missing is a legitimate state of a commons and a question to work on, not a defect by default. | gaps |
| R13 | MUST | Part 7 holds or links one minimal example that passes the specification's own checks. | An example settles what prose leaves open, for people and agents alike, and the minimal one shows the floor every reader builds on. | example |
| R15 | MUST | Part 8 lists each decision and each review result with its date, its kind and the word of the human accountable for the specification's mandate or a link to where that word is recorded, `status: decided` requires a row of kind `adopted`, and a `review` is fulfilled only by an attributable result that names the requirement, the reviewer, the date, the revision reviewed and the outcome, which for the specification itself is a row of kind `reviewed`. | A specification is relied on because the human accountable for it adopted it, in any commons and however many people it has. A judgement no parser can make counts only where someone is named for it. | decisions |
| R17 | MUST | A specification file has at most 400 lines and no heading deeper than level 4, and a larger subject is split along its boundary into specifications that touch each other. | Small, flat units are read whole by people and fit whole into an agent's context without guessing. | size |
| R19 | SHOULD | A specification holds only requirements that change a decision of someone who implements or applies it, can be read without opening another file, and leaves options, open questions and their history to the work items it links. | It draws the needed, not everything that is true, and states what holds while the debate stays where the work is. | review |
| R20 | SHOULD | A commons that deviates from this rule states the deviation in a specification of its own that touches this one and lists only the requirements it changes, adds or drops, by id. | Convention before configuration: what is not stated is adopted. | review |
| R25 | MUST | Every relative link resolves from the specification's folder, and a text in another repository is named as `owner/repo@rev:path`, in `supersedes` and wherever a specification refers outside its repository, so that such a reference that cannot be reached is a gap while a malformed or missing one fails. | A link that leads nowhere fails the reader exactly where the text sends them deeper. A commons' texts live in several repositories, and a lone copy of one must not fail for what it cannot see. | references |
| R26 | MUST | `supersedes` lists every text the specification supersedes, and the file `carry-over/<id>.md` beside it says what happens to each and carries every load-bearing rule of each with the requirement that now holds it or drops it with its reason and the word of the human accountable, so that a superseded text with no row is not examined and blocks adoption, and once the specification is decided each superseded text carries a mark naming it. | Rules written anew beside the old ones get lost exactly where nobody looks. The record of looking is history, which the specification points to and does not carry. | carry-over |
| R27 | MUST | A specification states no measured state of the world and writes nothing that does not exist yet in the present tense: a measurement is produced by a check and dated in its output, a threshold, a limit or a required version stays, and where a requirement's means are not built the gap is named in part 6 or in the work item the specification links. | A number that was true on one day reads as a commitment on every later one. A target written as an inventory leads every reader, person or agent, to act on a capability that is not there. | review |
| R29 | MUST | A specification and its checks pass three tests: leave out, they require nothing they can do without, so the Why of every requirement names the function that breaks without it, a requirement whose Why names none is dropped or folded into the one that holds it, and a structure, field, file or term is added only where a requirement needs it; repair, they require nothing a participant of the commons cannot read, check and repair with plain files in git and the published checks, without a special tool or a particular provider; and robust, they are understood from the files alone, without the history of how they came about, carry a layperson working with an agent and one to many users, work for a while offline and without MCP, and are strict in what a commons generates and tolerant in what it reads, so that a check judges whether a file serves its function, never its wording, and is literal only for ids, digests and schemas. | A design is complete when nothing can be left out without its function breaking (after Antoine de Saint-Exupéry), and built so that those who use it can repair it (after Kelly Johnson); it is used by people nobody here sees, so what nobody needs is still kept by everyone, what only a specialist can repair belongs to the specialist (`core` R21), and what holds only with its history, a live service or one wording fails them. | review |

R3, R14, R16, R18, R21, R22, R23, R24 and R28 are folded into the requirement that now holds them (part 8) and are never reused.

## 5 · Structure

This rule's schema is `schemas/specification.schema.json`. It decides the front matter of every specification, and **every requirement row of part 4 is validated against its `$defs/requirement`**. A specification's own `schema` field names a different schema: the one for its subject.

| Field | Holds |
|---|---|
| `id` | the stable name, in lower case with hyphens; never reused |
| `title` | the name as written |
| `status` | `draft`, `decided` or `retired`; `decided` rests on a row of kind `adopted` in part 8 |
| `lang` | the one language of the file, two letters |
| `touches` | the ids of the specifications it touches |
| `terms` | the glossary ids it uses |
| `schema` | the path of the schema of its subject |
| `check` | the path of its tool, which runs the check ids its part 6 lists. Omitted when every check is `schema` or `review` |
| `examples` | paths of example files, when part 7 links rather than holds them |
| `supersedes` | the texts it supersedes, each a path or `owner/repo@rev:path` (R25); required, and `[]` when nothing is superseded |
| `superseded_by` | the id that replaces it. Required when `status` is `retired` |

**The carry-over file** `carry-over/<id>.md` lies in the specification's folder. For each entry of `supersedes` it says what happens to the text on adoption. Its table follows a line `**Carry-over**` and has the columns Text, Rule, Outcome, Requirement, Reason and Word. Text names one entry of `supersedes` in backticks. Outcome is `carried`, with one requirement id of part 4, or `dropped`, with a reason and the word of the human accountable. A rule that the specification neither carries nor drops is not superseded by it: it stays in force in its text, and the mark on that text says so.

Every path is relative to the specification's own folder. A text in another repository is named as `owner/repo@rev:path`: its owner and repository, a revision (a branch, a tag or a commit), and its path from that repository's root.

## 6 · Checks

`tools/check_spec.py <file>` reads one specification. Part 6 of every specification lists, in the first column of its first table, the check ids its own tool runs. This tool checks that each check named in part 4 resolves there. **Resolving a check is not passing it:** the subject's own tool runs it on the subject's data, and a `review` is passed only by its recorded result (R15). It reports each finding as **fail** (a MUST), **should** (a SHOULD) or **gap** (absent, R12), and exits with 1 only on a fail. The check ids are those named in part 4. The tool follows this part.

| Check | Tests |
|---|---|
| `front-matter` | the front matter validates against the schema (R1) |
| `parts` | the eight parts are there, in order, and part 1 is one paragraph (R2) |
| `touches` | each id resolves to a specification of the commons; an unresolved one is a gap while it is not yet written (R4) |
| `terms` | each term resolves in the glossary, and part 3 defines none of them (R5) |
| `table` | the table has its columns, and every row validates against `$defs/requirement` of this rule's schema (R6) |
| `ids` | ids are unique; with `--since <revision>`, no id is reused (R7) |
| `levels` | each level is MUST or SHOULD; a SHOULD never fails (R8) |
| `two-channels` | each Requirement is one sentence; each Why holds one or two (R9) |
| `checks` | each check is `schema`, `review`, or an id in the first column of part 6, and the tool named in `check` exists (R10) |
| `schema` | the schema file exists and parses (R11) |
| `gaps` | the outcomes are fail, should or gap (R12) |
| `example` | the examples are there, and pass this same check (R13) |
| `decisions` | dates and kinds are valid; with `status: decided`, part 8 has a row of kind `adopted` (R15) |
| `carry-over` | with a non-empty `supersedes`, the carry-over file says what happens to each listed text, which exists; every row names a listed text; a carried row names an existing requirement, a dropped row a reason and a word; a text with no row is a gap while draft and a fail once decided; once decided, each text carries the mark; a table still in part 8 is read and reported as unmigrated (R26) |
| `references` | relative links resolve; a reference to another repository has the form `owner/repo@rev:path` and resolves there; one the check cannot reach is a gap, a malformed or missing one a fail (R25) |
| `size` | at most 400 lines, and no heading below level 4 (R17) |
| `review` | a review by the human accountable for the specification's mandate, or by an agent that has only the file, answering the Why of R19, R20 and R27, and R29 by its three tests, leave out, repair and robust; its result is recorded as R15 says |

**One sentence rule, fixed.** A sentence ends at `.`, `!` or `?` when a space and a capital letter follow, or the cell ends there. Text in code spans does not count. A Requirement or a Why therefore uses no abbreviation that ends in a period. The rule is the same for people and for the tool, so `two-channels` gives no false findings.

## 7 · Example

**Minimal:** [`examples/specification/opening-hours.md`](examples/specification/opening-hours.md). In it, a commons says when it is open, so that people and agents can tell. It has four requirements and a schema file. One of its checks, `no-overlap`, is its own: part 6 lists it, and its small tool runs it. This shows how a specification names checks the generic tool does not know (R10).

**Complete:** this file, which specifies itself by its own rule.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | A new kind of specification for the cognitive age: understandable, implementable and applicable by people and machines; KISS; every commons specifies its requirements this way; part of the Commons Essentials Extension; written from the view of any commons. It comes first of the eight | commons.o#87, opened on the word of the human accountable; the word quoted there |
| 2026-10-26 | adopted | Adopted after four precisions (`supersedes` required, rows validated against `$defs/requirement`, the rule's schema apart from a specification's own, the `decided` object) and a green check | Holger, commons.o#87, comment 6413669417 |
| 2026-10-26 | revised | R25: a text in another repository is named as `owner/repo@rev:path`, in `supersedes` and wherever a specification refers outside its repository; unreachable is a gap, malformed a fail | Holger, commons.o#88, comment 6414185621 |
| 2026-10-26 | revised | R26: a carry-over table for every superseded text; a rule left out counts as not examined and blocks adoption; the 400-line limit is met by splitting along the boundary, never by silent loss | Holger, commons.o#88, comment 6414454881 |
| 2026-10-28 | commissioned | R27: a specification states no measured state; a measurement lives dated in a check's output, while thresholds, limits and required versions stay (proposition 3 of cloudsters.o#33). Written for adoption; not yet adopted | Holger, cloudsters/cloudsters.o#33, comment 6468426138 |
| 2026-10-28 | commissioned | R28: what does not exist yet is never written in the present tense as existing; the gap is named (proposition 4 of cloudsters.o#33). Written for adoption; not yet adopted | Holger, cloudsters/cloudsters.o#33, comment 6468426138 |
| 2026-10-28 | adopted | R27 and R28 adopted after a green second check | Holger, cloudsters/cloudsters.o#33, comment 6468514431 |
| 2026-10-28 | commissioned | KISS pass: the form rules fold into the requirement that now holds them: R3 into R2, R14 into R13 (a complete example is no longer required), R24 into R15, R23 into R17, R18 and R21 into R19, R22 into R25, R16 into R26, R28 into R27; the `decided` object is dropped, since the `adopted` row is the one record of adoption; the carry-over moves to `carry-over/<id>.md` beside each specification, with R26 kept as the rule. Written for adoption; not yet adopted | Holger, commons.o#98 ("Ja, alle") |
| 2026-10-28 | adopted | The KISS revision adopted: the form rules folded, R16 into R26 included; the `decided` object dropped; the carry-over in `carry-over/<id>.md` | Holger, commons.o#98, comment 6474773388 |
| 2026-10-30 | commissioned | R29: leave out and repair, the two tests of keeping a specification simple, for every revision from its adoption on; no pass over the specifications. Adopted 30 October 2026 ([commons.o#98, comment 6520286756](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6520286756)) | Holger, commons.o#98, comment 6519997608 (*"ja, wie vorgeschlagen"*, item 1) |
| 2026-10-30 | adopted | R29 adopted, with the term `kiss`; the EA reads it with the next reading | Holger, commons.o#98, comment 6520286756 (*"A, wie vorgeschlagen"*) |
| 2026-10-30 | revised | Part 6, `review`: the review answers R29 by its tests, leave out, repair and robust, beside the Why of R19, R20 and R27. Adopted 30 October 2026 ([commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766)) | Holger, commons.o#98, comment 6522766676 (*"E–G ja, wie vorgeschlagen"*, item G); the EA, comment 6522117154 |
| 2026-10-30 | revised | R29: the third test, robust, understood from the files alone, for a layperson with an agent and one to many users, a while offline and without MCP, strict in what is generated and tolerant in what is read, a check literal only for ids, digests and schemas; still one requirement and no new term. Adopted 30 October 2026 ([commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766)) | Holger, commons.o#98, comment 6524525898 (*"ja, wie vorgeschlagen"*, item 1) |
| 2026-10-30 | adopted | R29 with its third test, robust, and part 6's review by the three tests adopted with the robustness set | Holger, commons.o#98, comment 6526694766 (on 6526314655: *"1–6 ja, R24 B, wie vorgeschlagen"*) |

The kinds are `commissioned`, `reviewed`, `adopted` and `revised`. A `reviewed` row names the requirements, the revision reviewed and the outcome in the Decision column, and the reviewer in the Word column (R15). The adoption follows as a row of kind `adopted`.

What this specification supersedes, and what it carries of it, is in [`carry-over/specification.md`](carry-over/specification.md).

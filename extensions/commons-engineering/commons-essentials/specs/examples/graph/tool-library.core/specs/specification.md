---
id: specification
title: Commons SPECIFICATION
status: decided
lang: en
touches: [model, core, library, graph, mcp, flow, extension]
terms: [commons, specification, requirement, decision, extension, essentials]
schema: schemas/specification.schema.json
check: tools/check_spec.py
examples: [examples/specification/opening-hours.md]
supersedes: [../commons-as-code/README.md]
decided:
  date: '2026-10-26'
  by: Holger
  where: commons.o#87, comment 6413669417
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
| R2 | MUST | The body has eight parts in this order, each a level-2 heading that begins with its number: 1 Goal, 2 Boundary, 3 Terms, 4 Requirements, 5 Structure, 6 Checks, 7 Example, 8 Decision log. | Every reader, human or agent, finds the same thing in the same place, in any language. | parts |
| R3 | MUST | Part 1 is one paragraph that names the decision or orientation the specification carries. | A specification that carries no decision has no reason to exist. | goal |
| R4 | MUST | Part 2 says what belongs and what does not, and every specification it touches is listed in `touches`. | Boundaries keep two specifications from requiring the same thing differently. | touches |
| R5 | MUST | Every term in `terms` resolves in the commons' glossary; a new term is added to the glossary in the same change and is never defined in the specification alone. | One source per term; a word defined in two places drifts. | terms |
| R6 | MUST | Part 4 holds one table with the columns ID, Level, Requirement, Why and Check, one row per requirement. | A table is read by people and parsed by machines without a second copy. | table |
| R7 | MUST | Requirement ids are unique within the specification and are never reused for a different requirement. | Other specifications, checks and work items cite `<id>#R<n>`; a reused id silently changes what they cite. | ids |
| R8 | MUST | The level is MUST or SHOULD, and a failed MUST fails the check while a failed SHOULD is reported without failing. | Implementers must know what blocks and what only informs. | levels |
| R9 | MUST | A requirement is one testable sentence, and its Why says in one or two sentences which decision it carries. | The machine channel says what holds; the intent channel says why. Agents need both to apply a rule to a case nobody foresaw. | two-channels |
| R10 | MUST | Every requirement names exactly one check: `schema` for validation against its schema, `review` for a judgement no machine can make, or a check id that part 6 lists for the tool named in `check`. | A requirement nobody can test is a wish, and a check that resolves nowhere is one too. | checks |
| R11 | MUST | Part 5 names the schema file that decides the structure; where prose and schema disagree, the schema holds and the disagreement is a defect. | Prose explains; the schema decides. | schema |
| R12 | MUST | An absent optional part, file or relation is reported as a gap and fails only where a MUST requires it. | Missing is a legitimate state of a commons and a question to work on, not a defect by default. | gaps |
| R13 | MUST | Part 7 holds or links one minimal example that passes the specification's own checks. | An example settles what prose leaves open, for people and agents alike. | example |
| R14 | SHOULD | Part 7 also holds or links one complete example. | The minimal example shows the floor; a complete one shows the whole. | example |
| R15 | MUST | Part 8 lists each decision and each review result with its date, its kind and the word of the human accountable for the specification's mandate, or a link to where that word is recorded; `status: decided` requires a row of kind `adopted` and the `decided` object, whose `date`, `by` and `where` give that row's date, the human who adopted it and where the word is recorded. | A specification is relied on because the human accountable for it adopted it, in any commons and however many people it has. | decisions |
| R16 | MUST | `supersedes` lists every text the specification supersedes and part 8 says what happens to each; once it is decided, each carries a mark naming it, and none is kept as current beside it. | Rules written anew beside the old ones, with nothing retired, are why work loses its aim. | superseded |
| R17 | MUST | A specification file has at most 400 lines; a larger subject is split along its boundary into specifications that touch each other. | Small units are read whole by people and fit whole into an agent's context. | size |
| R18 | SHOULD | The body can be read without opening another file: links deepen, and no requirement depends on them. | A reader who must load ten files first does not read. | review |
| R19 | SHOULD | A specification holds only requirements that change a decision of someone who implements or applies it. | It draws the needed, not everything that is true. | review |
| R20 | SHOULD | A commons that deviates from this rule states the deviation in a specification of its own that touches this one and lists only the requirements it changes, adds or drops, by id. | Convention before configuration: what is not stated is adopted. | review |
| R21 | SHOULD | Options, open questions and their history live in the work items the specification links, not in the specification. | A specification states what holds; the debate stays where the work is. | review |
| R22 | MUST | Every relative link resolves from the specification's folder. | A link that leads nowhere fails the reader exactly where the text sends them deeper. | links |
| R23 | MUST | No heading is deeper than level 4. | Flat files are read whole by people and parsed by machines without guessing. | flat |
| R24 | MUST | A `review` is fulfilled only by an attributable result that names the requirement, the reviewer, the date, the revision reviewed and the outcome; for the specification itself, that result is a row of kind `reviewed` in part 8. | Some obligations need judgement, and a structural pass alone never shows that they are met. Making them optional, or pretending a parser decides them, fails the commons either way. | reviews |
| R25 | MUST | A text in another repository is named as `owner/repo@rev:path`, in `supersedes` and wherever a specification refers outside its repository, and such a reference that cannot be reached is a gap while a malformed one fails. | A commons' texts live in several repositories, and a lone copy of one must not fail for what it cannot see. | references |
| R26 | MUST | A specification with a non-empty `supersedes` holds in part 8 a carry-over table, in which every load-bearing rule of each superseded text is carried with the requirement that now holds it or dropped with its reason and the word of the human accountable, and a superseded text with no row is not examined and blocks adoption. | Rules written anew beside the old ones get lost exactly where nobody looks; the table is where looking is recorded. | carry-over |

## 5 · Structure

This rule's schema is `schemas/specification.schema.json`. It decides the front matter of every specification, and **every requirement row of part 4 is validated against its `$defs/requirement`**. A specification's own `schema` field names a different schema: the one for its subject.

| Field | Holds |
|---|---|
| `id` | the stable name, in lower case with hyphens; never reused |
| `title` | the name as written |
| `status` | `draft`, `decided` or `retired` |
| `lang` | the one language of the file, two letters |
| `touches` | the ids of the specifications it touches |
| `terms` | the glossary ids it uses |
| `schema` | the path of the schema of its subject |
| `check` | the path of its tool, which runs the check ids its part 6 lists. Omitted when every check is `schema` or `review` |
| `examples` | paths of example files, when part 7 links rather than holds them |
| `supersedes` | the texts it supersedes, each a path or `owner/repo@rev:path` (R25); required, and `[]` when nothing is superseded |
| `decided` | the object `date`, `by`, `where`: the date of the `adopted` row, the human who adopted it, where the word is recorded. Required when `status` is `decided` |
| `superseded_by` | the id that replaces it. Required when `status` is `retired` |

**The carry-over table** in part 8 follows a line `**Carry-over**` and has the columns Text, Rule, Outcome, Requirement, Reason and Word. Text names one entry of `supersedes` in backticks. Outcome is `carried`, with one requirement id of part 4, or `dropped`, with a reason and the word of the human accountable. A rule that the specification neither carries nor drops is not superseded by it: it stays in force in its text, and the mark on that text says so.

Every path is relative to the specification's own folder. A text in another repository is named as `owner/repo@rev:path`: its owner and repository, a revision (a branch, a tag or a commit), and its path from that repository's root.

## 6 · Checks

`tools/check_spec.py <file>` reads one specification. Part 6 of every specification lists, in the first column of its first table, the check ids its own tool runs. This tool checks that each check named in part 4 resolves there. **Resolving a check is not passing it:** the subject's own tool runs it on the subject's data, and a `review` is passed only by its recorded result (R24). It reports each finding as **fail** (a MUST), **should** (a SHOULD) or **gap** (absent, R12), and exits with 1 only on a fail. The check ids are those named in part 4. The tool follows this part.

| Check | Tests |
|---|---|
| `front-matter` | the front matter validates against the schema (R1) |
| `parts` | the eight parts are there, in order (R2) |
| `goal` | part 1 is one paragraph (R3) |
| `touches` | each id resolves to a specification of the commons; an unresolved one is a gap while it is not yet written (R4) |
| `terms` | each term resolves in the glossary, and part 3 defines none of them (R5) |
| `table` | the table has its columns, and every row validates against `$defs/requirement` of this rule's schema (R6) |
| `ids` | ids are unique; with `--since <revision>`, no id is reused (R7) |
| `levels` | each level is MUST or SHOULD; a SHOULD never fails (R8) |
| `two-channels` | each Requirement is one sentence; each Why holds one or two (R9) |
| `checks` | each check is `schema`, `review`, or an id in the first column of part 6, and the tool named in `check` exists (R10) |
| `schema` | the schema file exists and parses (R11) |
| `gaps` | the outcomes are fail, should or gap (R12) |
| `example` | the examples are there, and pass this same check (R13, R14) |
| `decisions` | dates and kinds are valid; with `status: decided`, the `decided` object is there and its date is that of an `adopted` row (R15) |
| `reviews` | with `status: decided`, every requirement checked by `review` has a `reviewed` row in part 8 that names it (R24) |
| `superseded` | each listed text exists; once decided, each carries the mark (R16) |
| `carry-over` | with a non-empty `supersedes`, the carry-over table is there; every row names a listed text; a carried row names an existing requirement, a dropped row a reason and a word; a text with no row is a gap while draft and a fail once decided (R26) |
| `references` | a reference to another repository has the form `owner/repo@rev:path` and resolves there; one the check cannot reach is a gap, a malformed one a fail (R25) |
| `size` | at most 400 lines (R17) |
| `links` | relative links resolve (R22) |
| `flat` | no heading below level 4 (R23) |
| `review` | a reading by the human accountable for the specification's mandate, or by an agent that has only the file, answering the Why of R18, R19, R20 and R21; its result is recorded as R24 says |

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
| 2026-10-26 | revised | R26: a carry-over table in part 8 for every superseded text; a rule left out counts as not examined and blocks adoption; the 400-line limit is met by splitting along the boundary, never by silent loss | Holger, commons.o#88, comment 6414454881 |

The kinds are `commissioned`, `reviewed`, `adopted` and `revised`. A `reviewed` row names the requirements, the revision reviewed and the outcome in the Decision column, and the reviewer in the Word column (R24). The adoption follows as a row of kind `adopted`, together with the `decided` field.

**Supersedes**

| Text | On adoption |
|---|---|
| `README.md`, the sentence *"There are no manifests or specifications as document kinds"* | revised on 26 October 2026: one normative kind remains, the specification by this rule. Every term remains one object in the glossary |

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `../commons-as-code/README.md` | the sentence *"There are no manifests or specifications as document kinds"* | dropped | | one normative kind remains, the specification by this rule; every term remains one object in the glossary | Holger, commons.o#87, comment 6413669417 |

The manifests and specifications of the archive are not superseded here as a whole. Each of the seven specifications that follow names the texts whose content it supersedes.

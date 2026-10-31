---
id: library
title: Commons LIBRARY
status: decided
lang: en
touches: [specification, core, extension, model, graph, graph-engine, library-patterns, mcp, flow]
terms: [commons, commons-library, extension, essentials, enhanced, pattern, orbit, visibility-class, commons-core, part, where-used]
schema: schemas/library.schema.json
check: tools/check_library.py
supersedes:
  - Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md
  - ../commons/specs/PACK_SPEC.md
  - Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md
  - Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md
  - Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md
  - Commons-Engineering/commons-library@main:README.md
  - Commons-Engineering/commons-patterns@main:README.md
---

# Commons LIBRARY

*What a commons releases for others to install: each release a copy of its own, through one gate, and never changed.*

## 1 · Goal

A commons that has learned something others can use releases it, and a commons that installs it must be able to rely on what it got: that it passed the same checks wherever it came from, that it is the same text tomorrow, and that it says where it came from and what changed. A library is the place that holds such releases, as copies of its own and apart from the CORE they were made in: the released offers of `[domain].core`s, called extensions, and the released extracts of patterns. It publishes; it never authors, because each commons is the source of its own change record. This specification decides two things for its reader: **whether something is releasable**, meaning it passed the one gate and carries its provenance, its licence and no one's private data, and **where a commons finds what it may install, and which versions**.

## 2 · Boundary

**Belongs here:** what a library is and holds; the release record, the one release record of every library; versions, their states and their end; the library's index; the gate; the check at install, the one check every installing commons runs; publication; where answers about a release go.

**Does not belong here:**

| Matter | Where it belongs |
|---|---|
| what an extension is, its offer, its research, installing and adopting | `extension` |
| a pattern's form, orbits, known uses, promotion, the extract's index | `library-patterns` |
| where a CORE keeps what it installed, its lock, its `release` events | `core` |
| the graph run an extract is cut from | `graph-engine` |
| serving, grants, and how a commons sends an answer | `mcp` |
| the change brief a receiving commons computes, its decisions | `flow`, `extension` |
| who operates a library, its hosting, its keys, its staff and what it announces | the operating commons |

**Touches** `specification`, `core`, `extension`, `model`, `graph`, `graph-engine`, `library-patterns`, `mcp` and `flow`. **Rests on** Holger's words: L1, L3, E2 and E5 (commons.o#90, comments 6464648757, 6464676842 and 6464808164); each commons the source of its change record (commons.o#91, comment 6466913268); a library as part of a CORE first and a repository of its own only later (commons.o#89); LIBRARY before MCP (commons.o#91, comment 6468952146); the KISS pass (commons.o#98). The joint position on change communication (commons.o#91, comment 6468978984) gives part 5's release fields.

## 3 · Terms

All terms resolve in the glossary. *Release*, *version*, *source* and *licence* keep their ordinary meaning, made precise by part 5; *library* is the glossary's `commons-library` in general.

## 4 · Requirements

| ID | Level | Requirement | Why | Check |
|---|---|---|---|---|
| R1 | MUST | A library is one repository, or at the first tier a folder of the CORE that holds it, with `library.yml` at its root naming its id, its holder and the releases it withholds, and the same layout at both tiers. | Not every commons needs a repository for what it releases, and moving to one must change a location, never a record. | layout |
| R2 | MUST | A library holds releases of two kinds, the extensions of `[domain].core`s and the extracts of patterns, each as a copy of its own in a folder named by its id and version, and never a pointer into the CORE it was made in, nothing of the copy and no path its record or index names leading outside it, by an absolute path, a step up or a link or junction, so that its pin covers all that it holds. | A private maker is never an origin, what was released must be readable without its maker, and what lies outside the copy is not what was pinned. | layout |
| R3 | MUST | Every release has a record `release.yml`, generated from the `release` event of its source, that names its id, kind, profile and version, the library, the source and commit it was made from with that event, the gate's result with the checker at the commit that ran it, its parts, each with its visibility class and the digest of its files, its licence, where answers about it go and, for a major version, the rename map; a release copy holds its one `public` part, the one a commons installs, and every other part is held only where it is served. | One record says for every library where a release came from, what it passed and what it changed; a part's digest lets each holder verify the part it may hold, without receiving the depth it may not; a rename cannot be derived. | release |
| R4 | MUST | A version is semantic, released once and never changed, so that the files of a released version are the ones first released, and a tag only locates it. | A commons that installed a version must be able to rely on it tomorrow. | immutable |
| R5 | MUST | A released version is never deleted, and its record never leaves the library: it ends by a date in the `retires` of a later release record, from which it is `retired`, still readable and installable by a commons that pins it; apart from its end, a release whose files carry a private datum, an unauthorised part or a licence the library may not give is withheld by an entry in `library.yml` naming it, the date and the reason, after which its files leave the library's current files, its record and its place in the lineage stay, and a commons keeps the copy it installed; a withholding stops the library's distribution and recalls nothing, since earlier commits and every existing clone still hold the files and no history is rewritten (`core` R10). | A commons decides when it moves, and a version that vanishes moves it without its decision; keeping a lineage is no duty to go on distributing what should never have been released. | immutable |
| R6 | MUST | The library's index `index.yml` lists every release by id, kind and version with the path and digest of its release record, its state, `candidate`, `released` or `retired`, and whether it is withheld, and it is generated from the release records and `library.yml`, never kept by hand. | The index is how a commons sees a newer release, by reading it itself, and a state kept by hand would drift from the records. | index |
| R7 | MUST | Only a version that passed the gate is `released`, and a candidate, a version `-rc.n`, is installed only by a commons that pins it by its full version. | A candidate is how a release is proved; it must never arrive by accident. | index |
| R8 | MUST | The gate is one code for every library, the checks of `extension` on an extension's offer, those of `library-patterns` on an extract and those of part 6 on every release; its checks of a release copy are the same code in the library, on a copy alone and at install, read from the copy without its maker, with the mandatory content of the release's profile, a domain's `offer` or Commons Essentials' `specifications`; and no library adds a rule to it or drops one. | The gate decides what may be installed, not the address; a check that is weaker where a commons installs is no check; a library that changed the gate would be another discipline. | release |
| R9 | MUST | A commons installs a release only after running the gate's checks of a release copy again on its own copy, against the record digest its lock took from the library's index at the pinned revision, and a release that fails them there is not installed; what needs the maker, its research and the authority of its event, is checked at the maker's gate and never at install. | A library can be wrong or compromised, and a copy that agrees with itself proves no origin; what a commons installs is checked by the commons, against what it pinned. | release |
| R10 | MUST | A release holds no name of a person or an organisation outside its provenance fields, an extension's attribution list `sources.yml` and a pattern's `contributors`, those who wrote it and never a fixed operator, `sources` and `attribution`, and no contact datum, no credential and no commercial datum; the names it is checked against are the discipline's rejected words and a list kept outside git. | A release is copied into every commons that installs it; what it carries cannot be called back, and provenance that names the wrong author is false. A list finds the names on it and proves no text anonymous, so the reading stays human. | private |
| R11 | MUST | Every release names its licence by an SPDX identifier or by a `LicenseRef-` whose text the release carries in its own `LICENSES/`, and the discipline's own releases stay free. | A commons may only use what it may use, and a licence without its text, wherever the copy went, grants nothing. | licence |
| R12 | MUST | A library publishes and never authors: its release records are generated from the change records of their sources, it holds no research, no workshop, no decision's content beyond its id and nothing of who installed what, and what it makes public becomes public only by an editorial step on the word of its holder, never one to one. | Each commons is the source of its own changes, the library must never learn what a commons adopted, and released is not public. | review |
| R14 | MUST | A commons installs only from a library it names, under the id it gives it, and a library needs no permission to exist, only the gate. | Any commons may release; what it releases is trusted for the gate it passed, not for the address it came from. | layout |
| R15 | MUST | The index, every release record and every file of a release's public part can be read from a clone of the library; a served part is held only by the service that serves it, named in its record by class and digest; and a service holds nothing about the library that only it knows. | A commons must be able to leave its host and keep what it installed, and depth it may not hold must not travel with a clone. | review |
| R17 | MUST | A release names in `answers` the board where answers about it go, its maker's, and an answer arrives there as one item, a commons' through its MCP's `propose` (`mcp` R12), a reader's through whatever door the maker opens. | A release is half of an exchange, and a way back that names no place is none. | release |
| R18 | MUST | A withholding reaches the commons that hold a copy through their own where-used (`graph` R27): each finds the lines of its bill whose release the index marks withheld and decides what follows; the library computes none and recalls nothing (R5). | Only the commons that installed a release can see where it lies, and only it may decide. | where-used |

R13 is folded into R12, and R16 is the operation of the commons that holds a library; neither id is reused.

## 5 · Structure

The schema is `schemas/library.schema.json`. Its root is `library.yml`; its `$defs` hold `index`, `release`, `extract` and `parts`.

```
library.yml                       id, holder, withheld
index.yml                         generated from the release records and library.yml
<extension>/<version>/            an extension's release (EXTENSION part 5): its public part
patterns/<version>/               an extract's release (library-patterns part 5)
<release>/LICENSES/<ref>.txt      the text of a licence the release names by reference
README.md, CONTRIBUTING.md        what the library is
```

| Field of `library.yml` | Holds |
|---|---|
| `id` | the library's id, lowercase with hyphens |
| `holder` | who holds the library, answers for it and gives the editorial word (R12) |
| `withheld` | `[{release, from, reason}]`: a release `<id>@<version>` the library no longer distributes, from a date, for `private-data`, `unauthorised` or `licence` (R5) |

**A release record** (`$defs/release`), the one release record (EXTENSION's release names its offer's fields and refers here):

| Field | Holds |
|---|---|
| `kind` | `extension` or `extract` |
| `profile` | for an extension, `offer` (a domain's offer, the default) or `specifications` (Commons Essentials alone: `specs/` and nothing else) |
| `event` | the source's `release` event, `owner/repo@sha:lifecycle/events/<id>.yml` |
| `gate` | `result`, and `check`, the checker at the commit that ran, `owner/repo@sha:path` |
| `parts` | each part by name with its `class` and its `digest`, `sha256:` over its files but the record, path by path, whatever the line endings; `essentials` (an extract: `patterns`) is the copy and `public`, `enhanced` is served and never in the copy |
| `licence` | an SPDX identifier, or `LicenseRef-<name>` with its text in the release's `LICENSES/` |
| `answers` | the board where answers about the release go, `owner/repo` (R17) |
| `retires` | `[{id, from}]`: an earlier version of this library, `<id>@<version>`, or a record an earlier version offered, and the date `YYYY-MM-DD` from which it is `retired` |

An extract's record (`$defs/extract`) has `kind: extract` and, in place of `made_in`'s offer, the pattern source at its commit, the released graph run, the extractor, the extraction policy, the scope and the digest of its index (`library-patterns` R17).

**A release as a part:** its record is its single-level bill, its `parts` the lines and `made_in` the level below (`graph` R26).

**An index entry** (`$defs/index`): `id` (an extension's id, or `patterns` for an extract), `kind`, `version`, `record` (the path), `digest` (`sha256:` over the record), `state` and, for a withheld release, `withheld: {from, reason}`. The state is derived: `candidate` for `-rc.n`, `retired` from a `retires` date on, else `released`. Being withheld is no state: a withheld version keeps its state and its place in the lineage, and is no longer distributed.

**Installing** (R9): a commons resolves a release from the library's index at a revision and keeps in its lock the release, its origin and `record`, the digest the index gives (CORE R29). At install it runs the gate's checks of a release copy on the copy it received, against that digest: a copy whose files and record were changed together agrees with itself and still fails there.

**What a commons reads of a change:** the index, by reading it itself. Each lifecycle event of a release, `released`, `retired` from its date, or `withheld`, is identified by the release and its record digest, the event, its date and, for an end, the record that set it; a later end of an unchanged record is an event of its own. The change itself is the source's `release` event (CORE), and the brief for a receiving commons is computed by that commons (`extension`, `flow`); the library never reads a commons' lock or `adopted_from`. An answer is the recipient's own; no answer is *unknown*, never agreement, and what came of a release returns to its maker only as the released aggregate of explicit answers.

## 6 · Checks

`tools/check_library.py <library>` reads one library: its `library.yml`, its index and every release in it, with the checks of `library-patterns` for each extract. It reports **fail**, **should** or **gap**, and exits with 1 only on a fail. `--names <file>` reads the list of names R10 checks against, from outside git; without it, that part of `private` is a gap. `--release <folder>` checks one release copy where it lies, as a commons does at install, with `--expect <digest>` the record digest its pin gives; `check_extension.py --core` runs the same code on every installed copy, with the `record` of the lock. A copy's checks are one function in all three places: everything below but `layout`, `index` and `immutable`, which read a library.

| Check | Tests |
|---|---|
| `layout` | `library.yml` validates and every date in `withheld` is a date; the root holds only the entries of part 5; every release folder is `<id>/<version>/` or `patterns/<version>/` (R1, R2, R14) |
| `release` | nothing of a copy leads outside it, links and junctions resolved; every release record validates, names this library, its folder's id and version, a passing gate, a checker at a commit and where answers go; its `public` part is `essentials` or `patterns` and its digest is that of the copy's files, and no other part is `public`; at install, its record has the digest of the lock; every `retires` date is a date and names an earlier version this library holds, or a record an earlier version offered; a withheld release is held by the library and its folder holds its record alone; an extension of the profile `offer` holds `offer.yml` as EXTENSION's schema says, `sources.yml`, a registry with at least one value stream that passes MODEL's checks as an extension, a steering loop for every family it offers streams of, and binds only attributed sources, whose terms it never names; one of the profile `specifications` is `commons-essentials`, holds only `specs/`, and every specification there follows SPECIFICATION but for what only the maker's estate resolves (R3, R5, R8, R9, R17) |
| `immutable` | in git, every file of a released version is the one first released, and no released version has left the library but the files of a withheld one; outside git, a gap (R4, R5) |
| `index` | `index.yml` is the one generated from the release records and `library.yml`, digest by digest, state by state and withholding by withholding; a candidate is never `released` (R6, R7) |
| `private` | no e-mail address, telephone number or credential in any release; no served part, `knowledge/`, `workshop/`, `_authoring/` or `overlays/` in a copy; with `--names`, no listed name outside the provenance fields (R3, R10, R12, R15) |
| `licence` | every release names an SPDX identifier, or a `LicenseRef-` with its text in its own `LICENSES/` (R11) |
| `where-used` | with `--core`, each line of that CORE's bill whose release is withheld is a `should` with its date and reason; a CORE without a bill is a gap with its failures, and each withheld pin its lock declares is named, unverified; nothing is written to the library (R18) |
| `review` | a reading by the human accountable, or by an agent that has only this file, of R10 beyond the list, R12 and R15 |

**Not built yet** (R28): the release tool that makes a release from a source's `release` event, and the verification that a record came from that event and that the event was authorised: until it exists, a well-formed `event` and `gate.result: pass` are the maker's statement, every check reports this as a gap, and E3 made its candidates with a script of its own (commons.o#96), whose records predate `parts`, `record` and `answers`. The first release under this gate is Commons Essentials 0.2.0; what its `specs/` holds of `tools/tests/`, whose fixtures carry contact data by design, is the release tool's to settle.

## 7 · Example

**Minimal:** a library that holds nothing yet. Its `library.yml`:

```yaml
id: tool-library-releases
holder: the tool library
```

**Complete:** [a library with one extension and one extract](examples/library/demo.library/library.yml): the garden extension in two versions, the second retiring a record and renaming another, and an extract of three patterns with its index. `check_library.py` reads it with 0 fail.

## 8 · Decision log

| Date | Kind | Decision | Word |
|---|---|---|---|
| 2026-10-26 | commissioned | LIBRARY: what a commons keeps for reuse and releases; a part of the CORE first, a repository of its own later | Holger, commons.o#91 (*"LIBRARY an D4-CE"*); commons.o#89 |
| 2026-10-28 | revised | Taken up after GRAPH, before MCP, on the decided inputs L1, L3, E2, E5, the change-record principle and E3's account | Holger, commons.o#91, comment 6468952146 |
| 2026-10-28 | revised | `commons-library` public, prepared in four steps (sight, archive the earlier canon, list what becomes public, switch on Holger's word); a note per period (O1) with no adoption counts (O2); one intake with two doors (O3); an extension's release carries no `overlays/` | Holger, commons.o#91, comment 6470680520 |
| 2026-10-28 | revised | KISS: one release record and one check at install for every library (R3, R9); three states and `withheld`; `policy.yml`, the `gate` field of `library.yml` and collections dropped; R13 folded into R12; R14 and R17 written for any commons, a library a commons names (R14), a release naming in `answers` where answers go (R17); R16, the period note, with the intake's staffing and `commons-library`'s publication the operation of the commons that holds it; the ids of folded rules retired, never reused (SPECIFICATION R7) | Holger, commons.o#98 (*"Ja, alle"*) |
| 2026-10-29 | revised | The EA's read of #91: containment, nothing of a copy and no path its index names leading outside it, by an absolute path, `..` or a link or junction, checked by the one check of a copy in its library, alone and at install (R2, R9); withholding stops distribution and recalls nothing, earlier commits and clones keeping the files, no history rewritten (R5); the install description cites CORE R29. Adopted 29 October 2026 ([commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412)) | the EA, commons.o#91; commons.o#98 |
| 2026-10-29 | adopted | Adopted 29 October 2026 | Holger, [commons.o#98, comment 6505618412](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6505618412) |
| 2026-10-30 | revised | Step 2 of the bill of materials: a release record as the release's single-level bill (part 5); a withholding reaches the commons that hold a copy through their own where-used, the library computing none (R18; the check `where-used`). Adopted 30 October 2026 ([commons.o#107, comment 6521463793](https://github.com/Commons-Engineering/commons.o/issues/107#issuecomment-6521463793)) | Holger, commons.o#107 (step 1 adopted, comment 6519835234; D4-CE's reading, comment 6516687963) |
| 2026-10-30 | adopted | Adopted 30 October 2026 | Holger, [commons.o#107, comment 6521463793](https://github.com/Commons-Engineering/commons.o/issues/107#issuecomment-6521463793) |
| 2026-10-30 | revised | The EA's reading of step 2: without a bill, the check `where-used` names the withheld pins the lock declares, unverified, beside the CORE's failures, never certifying them and never making a second bill (R18). Adopted 30 October 2026 ([commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766)) | the EA, commons.o#107, comment 6522100364; Holger, comment 6522699919 |
| 2026-10-30 | adopted | Adopted 30 October 2026 | Holger, [commons.o#98, comment 6526694766](https://github.com/Commons-Engineering/commons.o/issues/98#issuecomment-6526694766) |

**Open for Holger** (proposals, not decided): **O4** the text of `LicenseRef-cloudsters-served` and the licence expression of the Commons extensions (E6; commons.o#69); the EA recommends that an operator's service terms never become the discipline's licence nor make Commons Enhanced proprietary, which no conformance check can decide (commons.o#91, 6470762650); **O5** whether business 2.0.0 keeps `released` while it carries third-party titles (commons.o#69). O1–O3 are decided (6470680520; O1 also 6470576685) and, after the KISS pass, are the operation of the commons that holds a library.

What this specification supersedes, and what it carries of it, is in [`carry-over/library.md`](carry-over/library.md).

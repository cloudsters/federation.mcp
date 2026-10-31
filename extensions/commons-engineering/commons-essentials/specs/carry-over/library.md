# library · carry-over

What [Commons LIBRARY](../library.md) supersedes, and what it carries of each text (SPECIFICATION R26).

**Supersedes**, each text in part. What is not carried or dropped below stays in force in its text until the specification named under *Not superseded here*.

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | a pack is atomic; installed and released locations are fixed, and no tool builds a path itself (§2.1, §2.2) | carried | R2 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | essentials and enhanced as two packs, `{domain}-{half}`, with naming patterns in `pack-naming.yml` (§2.1, §2.2) | dropped |  | one extension per `[domain].core`, one version line, parts by access class | Holger, commons.o#90, comments 6464648757, 6464676842 and 6464808164 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | `_authoring/` is never served or released (§2.2) | carried | R12 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | `draft`, `candidate`, `released`; only `released` passes into the library (§2.3) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | provider names unique, lowercase with hyphens, reserved words (§3.3) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | registration of a provider by a reviewed change (§3.2) | dropped |  | any library under the one gate, needing no permission; a library's id is the one a commons gives it | Holger, commons.o#90, comment 6464648757 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_EXTENSION_SPEC.md` | publishing pre-loaded, direct or by subtree (§4.3) | dropped |  | a commons installs only released extensions from a library, and nothing is pre-loaded | Holger, commons.o#90, comments 6419482445 and 6464648757 |
| `../commons/specs/PACK_SPEC.md` | the provider registry with profiles and status (§3.1) | dropped |  | replaced by `library.yml` and the index; a count of patterns is no field (EXTENSION R1) | Holger, commons.o#90, comment 6464648757 |
| `../commons/specs/PACK_SPEC.md` | registration by pull request to `commons-os`, the reserved name `commons-os` (§3.2, §3.3) | dropped |  | Commons OS is retired | Holger, 28 July 2026 (glossary `rejected.yml`: Commons OS) |
| `../commons/specs/PACK_SPEC.md` | the provider answers for conformance before publication (§5.1) | carried | R8 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | learning returns through the clean room; only validated improvements are published (§2.6) | carried | R12 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | the universal layer is free, stewarded, not owned (§4.1) | carried | R11 |  |  |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_CORE_MANIFEST.md` | every domain's collections pre-loaded in every fork (§4.2, §7.2) | dropped |  | one domain extension per commons, installed by decision | Holger, commons.o#90, comment 6419482445 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_CORE_SPEC.md` | O0 and O1 read-only in forks, updated by upstream sync (§7.1) | dropped |  | a newer release is taken up by decision, never synchronised | Holger, commons.o#95, comment 6438391848 |
| `Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md` | each phase leaves verifiable artefacts before the next (§1, §2) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md` | one pattern form version per release; versions reconciled before generating (§12) | carried | R8 |  |  |
| `Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md` | public pattern files, the computed graph kept back (§15) | carried | R12 |  |  |
| `Commons-Engineering/commons-library@main:README.md` | the library is indexed for install, and its releases are tags | carried | R6 |  |  |
| `Commons-Engineering/commons-library@main:README.md` | the profiles `lean` and `sovereign`, and orbits as folders | dropped |  | every CORE installs the extract of orbits 0–3 pinned by release; the orbit is a field of the index | Holger, commons.o#95, comments 6438391848 and 6438865249 |
| `Commons-Engineering/commons-library@main:README.md` | a change is proposed as an issue | carried | R17 |  |  |
| `Commons-Engineering/commons-patterns@main:README.md` | every release is a tag, and nothing is edited by hand once released | carried | R4 |  |  |
| `Commons-Engineering/commons-patterns@main:README.md` | private, served by ring through the MCP | carried | R12 |  |  |

**Not superseded here:** `COMMONS_EXTENSION_SPEC` §2.4 (collections) and `PACK_SPEC` §2.4, §5.1's pattern form, `PATTERN_PIPELINE_SPEC` §3–§8, §10, §11, §13, §14 go to `library-patterns`; `COMMONS_CORE_MANIFEST` §4.3 (held by `core` R26 and R28) and `COMMONS_CORE_SPEC` §7.3–§7.4 (in `library-patterns`); the Pattern Engine writing `commons-patterns` stays with the engine; `PATTERN_PIPELINE_SPEC`'s operational lessons stay with the Pattern Engine.

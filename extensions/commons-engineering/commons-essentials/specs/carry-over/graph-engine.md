# graph-engine · carry-over

What [Commons GRAPH — the Graph Engine](../graph-engine.md) supersedes, and what it carries of each text (SPECIFICATION R26).

**Supersedes**, each text in part. What is not carried or dropped below stays in force in its text until the specification named under *Not superseded here*.

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | embeddings, vector indexes and rendered projections are not versioned with the graph and are rebuilt (§2) | carried | R15 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | every derived record carries when, from what, under which authority, by which generator, at which revision; one without them is refused (§6) | carried | R5 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | derivation is a loop with its rhythm (§7) | dropped |  | a rhythm is the operating commons' choice, not a rule of the run | Holger, commons.o#98 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | each derivation declares the identity it reads under (§7) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | regeneration is the test; a full regeneration is compared with the incremental state (§7, §12) | carried | R14 |  |  |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | a decided record is never overwritten by a later pass; the writer refuses the ratified (§4a.1) | dropped |  | a run never writes into a source, and that rule is `graph`'s (R4) | Holger, commons.o#98 |
| `Commons-Engineering/workshop@main:_specifications/COMMONS_GRAPH_SPEC.md` | a write reaching the graph from anywhere but a derivation breaks it (§12) | carried | R4 |  |  |
| `Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md` | GraphRAG emulation over all patterns at once: entity extraction, community seeding, relationship inference (§9.1–§9.3) | carried | R2 |  |  |
| `Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md` | inferred relationships are written back into Groups 5 and 6 of each pattern file; `graph_garden` holds machine-written links (§7 Group 6, §9.3, §9.4) | dropped |  | a run delivers a package and never writes into a source; a suggestion is a proposal | Holger, commons.o#95, comment 6438391848 |
| `Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md` | never overwrite manually curated relationships (§9.4) | dropped |  | a run never writes into a source, and that rule is `graph`'s (R4) | Holger, commons.o#98 |
| `Commons-Engineering/workshop@main:_specifications/PATTERN_PIPELINE_SPEC.md` | log every inferred relationship for audit (§9.4) | carried | R5 |  |  |
| `Commons-Engineering/commons-graph@main:README.md` | embeddings and other large reproducible artefacts stay out of the repository and are rebuilt from source | carried | R15 |  |  |
| `Commons-Engineering/commons-graph@main:README.md` | derived structure is marked `generated:` and never hand-edited | carried | R4 |  |  |

**Not superseded here:** `PATTERN_PIPELINE_SPEC.md` §1–§8, §10 (its gates, Gate 3's quotas included) and §11–§14 stay with `library`.

# fabric · carry-over

What [Commons FABRIC](../fabric.md) supersedes, and what it carries of each text (SPECIFICATION R26).

**Supersedes**, each text in part. What is not carried or dropped below stays in force in its text until the specification named under *Not superseded here*.

**Carry-over**

| Text | Rule | Outcome | Requirement | Reason | Word |
|---|---|---|---|---|---|
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | the Fabric is the sensor of the Core; the Core is not a system of record and never becomes one (§1) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | one connection per system of record, n per Core (§1, §2.2) | carried | R2 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | the data stays inside the commons' boundary; no outward data flow (§2.1, §5.4) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | the abstract steps of a value stream are grounded in the commons' actual systems (§2.3, §4.5) | carried | R2 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | three channels, Commons, Blueprint and Fabric MCP (§3.1) | dropped |  | one MCP shape at every level; the Fabric is a component that senses, and the MCP serves what it read | Holger, commons.o#94, comment 6436299151; commons.o#99 |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | a translation layer, the system's protocol inward and MCP tools outward (§3.2) | dropped |  | a connector's implementation; the reading is the contract | Holger, commons.o#98 |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | no persistent store of a system's data; a cache never stands in for the system (§3.3) | carried | R3 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | no aggregation across systems of record (§3.3) | carried | R4 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | the Fabric does not interpret its data; meaning is given elsewhere (§3.3) | carried | R7 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | three deployment shapes, sidecar, bridge and gateway-bridged (§3.4) | dropped |  | where a connector runs is the commons' choice | Holger, commons.o#98 |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | the canonical tool surface: identification, read, aggregate, recent changes, subscriptions (§4.1–§4.3) | dropped |  | a connector's implementation; the register's queries and the reading are the contract | Holger, commons.o#98 |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | the commons authorises who queries which system at which scope, and the Fabric enforces it (§5.1) | carried | R9 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | reads request only the fields needed (§5.2) | carried | R6 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | every call is logged with its identity, a digest of its query and counts rather than values (§5.3) | carried | R4 |  |  |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | reference connectors, custom connectors and their quality contract (§6) | dropped |  | implementations, and their status a measured state | Holger, commons.o#87, comment 6413669417 (SPECIFICATION R27) |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | the activation lifecycle by engagement stage (§7) | dropped |  | a commons reads its systems whenever it registers them; an engagement stage is no condition | Holger, commons.o#93, comment 6424755304 |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | the implementation status and open items (§8, §9) | dropped |  | a dated status, never a requirement | Holger, commons.o#87, comment 6413669417 (SPECIFICATION R27) |
| `Commons-Engineering/workshop@main:_specifications/FABRIC_MCP_SPEC.md` | writes toward a system of record by exception (§3.3, §4.4) | dropped |  | the Fabric reads only (R3); an action on a system of record is the responsible Solution's, under its FLOW mandate | Holger, commons.o#99, comment 6501928492 (F1) |
| `Commons-Engineering/workshop@main:_manifests/COMMONS_SYSTEMS_MANIFEST.md` | an action toward a system of record by exception, per tool and identity (§2) | dropped |  | the Fabric reads only (R3); an action on a system of record is the responsible Solution's, under its FLOW mandate | Holger, commons.o#99, comment 6501928492 (F1) |

**Not superseded here:** `COMMONS_SYSTEMS_MANIFEST` but for its write exception, and `COMMONS_GRAPH_MANIFEST` §5, stay as manifests, read here as the reading that crosses while the record does not.

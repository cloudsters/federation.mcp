# federation.mcp

The Federation's MCP: serves the canon of Commons Engineering at ROAM and the offer per shell; code and deployment.

Content arrives by pull request only; see [cloudsters/cloudsters.o#59](https://github.com/cloudsters/cloudsters.o/issues/59).

It answers at `https://mcp.cloudsters.net/federation` (H3).

| Path | What |
|---|---|
| `.commons/commons.yml` | the pin: `commons-engineering/commons-essentials` 0.2.0, from the library `commons-engineering` in `cloudsters/federation.library` |
| `.commons/lock.yml` | generated at install: origin and record digest, as the library's index gives them (`library` R9) |
| `extensions/commons-engineering/commons-essentials/` | the installed release copy, never edited; the service runs its `specs/tools/serve_mcp.py`, the same code on every level (`mcp` R1, R22) |

**What is never here:**
- `access.yml` and its users. The Federation's access lives in the CORE this MCP serves, `cloudsters/cloudsters.o`, under `.commons/` (`mcp` R1).
- Any credential. The deployment credential is held apart from the code (H4).

Run the tools with `python -B`, so that no bytecode is written into the installed copy.

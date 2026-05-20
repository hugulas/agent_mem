# File-Based vs Database-Based Agent Memory

> Two fundamental paradigms for persisting agent memory: plain text files vs structured databases.

## The Divide

| Dimension | File-Based (OpenClaw, Karpathy Wiki, Codex AGENTS.md) | Database-Based (Mem0, Hindsight, Supermemory) |
|---|---|---|
| **Canonical store** | Markdown files on disk | Vector DB, graph DB, or relational DB |
| **Human readability** | ✅ Native (plain text) | ⚠️ Requires tooling / queries |
| **Version control** | ✅ Git-friendly | ⚠️ Migration scripts needed |
| **Search capability** | ⚠️ Requires indexing layer (FTS5, sqlite-vec) | ✅ Native (vector similarity, graph traversal) |
| **Scalability** | ⚠️ Linear with file count | ✅ Designed for millions of records |
| **Schema enforcement** | ❌ None (free-form Markdown) | ✅ Typed schemas, constraints |
| **Concurrent access** | ⚠️ File locking issues | ✅ ACID transactions |
| **Backup / migration** | ✅ `cp` or `git clone` | ⚠️ Export/import pipelines |
| **Security at rest** | ⚠️ OS-level only | ✅ Can encrypt database files |

## File-Based Advocates

### Arguments
- **Transparency**: You can `cat` your agent's memory. No hidden state.
- **Portability**: `git clone` + config update = full migration.
- **Human editing**: Fix mistakes directly without API calls.
- **Debugging**: `git diff` shows exactly what changed.
- **Longevity**: Text files are the most durable digital format.

### Represented by
- **OpenClaw**: MEMORY.md + daily notes + DREAMS.md
- **Karpathy LLM Wiki**: raw/ + wiki/ + schema/ layers
- **Codex CLI**: AGENTS.md convention

## Database-Based Advocates

### Arguments
- **Query power**: Vector similarity, graph relationships, temporal queries.
- **Performance**: Sub-100ms retrieval at million-record scale.
- **Type safety**: Structured schemas prevent malformed data.
- **Operational maturity**: Backup, replication, monitoring are solved problems.
- **Multi-agent**: Shared memory pools with access control.

### Represented by
- **Mem0**: Vector + optional graph memory
- **Hindsight**: 4-network relational graph
- **Supermemory**: 5-layer RAG pipeline
- **Honcho**: App→User→Session→Message hierarchy

## Hybrid Approaches

Several systems attempt to bridge the gap:

| System | Approach |
|---|---|
| **OpenClaw builtin** | Markdown files (canonical) + SQLite index (derived) |
| **Claude Code** | CLAUDE.md (static file) + disk-cached tool results (structured) |
| **Hermes** | MEMORY.md (static) + external vector provider (dynamic) |

## The Core Tension

> "What's your source of truth?"

- **File-first** (OpenClaw): The Markdown file is canonical. The database serves the file.
- **DB-first** (Mem0): The database is canonical. Files are import/export formats.
- **Dual** (Claude Code): Static instructions in files, dynamic state in structured caches.

## Recommendations by Scale

| Scale | Recommendation |
|---|---|
| **Personal / <1K memories** | File-based (OpenClaw, Karpathy Wiki) |
| **Small team / <100K memories** | Hybrid (Hermes with local provider) |
| **Enterprise / >1M memories** | Database-based (Mem0, Hindsight, Supermemory) |
| **Multi-agent / shared memory** | Database-based with access control (Honcho) |
| **Regulated industries** | File-based with OS-level encryption + audit logging |

## Related
- [[OpenClaw]]
- [[Karpathy LLM Wiki]]
- [[Mem0]]
- [[Hindsight]]
- [[file-based-memory]]
- [S001](sources/S001.md), [S068](sources/S068.md), [S078](sources/S078.md), [S081](sources/S081.md)

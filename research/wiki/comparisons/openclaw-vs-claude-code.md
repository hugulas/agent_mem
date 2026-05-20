# OpenClaw vs Claude Code: Memory Architecture

> Two dominant agent frameworks with fundamentally different memory philosophies.

## At a Glance

| Dimension | OpenClaw | Claude Code |
|---|---|---|
| **Memory philosophy** | Files-as-source-of-truth (Markdown on disk) | Context compaction + persisted tool results |
| **Persistence layer** | Plain Markdown + SQLite (local) | Disk-based tool result caching + CLAUDE.md |
| **Search mechanism** | Hybrid (70% vector + 30% BM25) | LLM-based memory scan + grep |
| **Context management** | Bootstrap file budget + truncation | 5-layer compaction pipeline |
| **User visibility** | Fully transparent, human-editable | Semi-transparent (CLAUDE.md hierarchy) |
| **Security posture** | CVE-2026-25253; plaintext secrets | No known CVEs; memory files user-editable |

## Memory Model

### OpenClaw: File-centric layers
- `MEMORY.md` — curated long-term facts, injected every session
- `memory/YYYY-MM-DD.md` — daily working notes, auto-loaded (today + yesterday)
- `DREAMS.md` — optional dream diary for human review
- Agent expected to **distill** from daily notes into MEMORY.md

### Claude Code: Compaction-centric pipeline
1. **Budget reduction** — cap individual tool outputs (50K/200K chars)
2. **Snip compact** — temporal depth pruning
3. **Microcompact** — `cache_edits` API for incremental updates
4. **Context collapse** — aggressive emergency pruning
5. **Autocompact** — automatic summarization at 13K token threshold

## Retrieval

- **OpenClaw**: `memory_search` (semantic) + `memory_get` (direct read). Hybrid search over all Markdown files with HNSW vector index in SQLite.
- **Claude Code**: No dedicated memory search tool. Relies on context window + CLAUDE.md hierarchy + grep-based scan for relevant prior context.

## Scalability

- **OpenClaw**: MEMORY.md grows unbounded; truncation only affects injected copy. Daily notes accumulate indefinitely unless manually cleaned.
- **Claude Code**: Compaction ensures context window stays within budget, but historical detail is progressively lost through summarization.

## Trade-offs

| Strength | OpenClaw | Claude Code |
|---|---|---|
| **Auditability** | ✅ Plain text, git-friendly | ⚠️ Binary/compiled state |
| **Human editing** | ✅ Direct file edit | ⚠️ Via CLAUDE.md only |
| **Search quality** | ✅ Hybrid semantic + keyword | ⚠️ Limited to context window |
| **Token efficiency** | ⚠️ Full MEMORY.md injected | ✅ Aggressive compaction |
| **Security** | ⚠️ Plaintext secrets | ✅ No known plaintext exposure |
| **Multi-session continuity** | ✅ Persistent files | ⚠️ Relies on compaction summaries |

## Related
- [[OpenClaw]]
- [[Claude Code]]
- [[file-based-memory]]
- [[context-compaction]]
- [S001](sources/S001.md), [S007](sources/S007.md), [S008](sources/S008.md)

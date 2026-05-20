# Claude Code vs Codex CLI: Coding Agent Memory

> Two major coding agents from Anthropic and OpenAI with fundamentally different memory architectures.

## At a Glance

| Dimension | Claude Code | Codex CLI |
|---|---|---|
| **Developer** | Anthropic | OpenAI |
| **Memory philosophy** | Context compaction + CLAUDE.md hierarchy | Static AGENTS.md + generated Memories |
| **Static instruction file** | `CLAUDE.md` (4-level hierarchy) | `AGENTS.md` (cross-tool convention) |
| **Dynamic memory** | 5-layer compaction pipeline | Generated Memories (async consolidation) |
| **User visibility** | CLAUDE.md editable; compaction opaque | AGENTS.md editable; Memories opaque |
| **Context limit** | 200K tokens (Claude 3.7) | 256K tokens (GPT-4o) |
| **Auto-compact threshold** | 13K tokens | Not disclosed |
| **Session persistence** | Tool results persisted to disk | Memories consolidated after 6h idle |

## Static Instruction Layer

### Claude Code: CLAUDE.md
- 4-level hierarchy: project → subsystems → packages/modules → files
- Each level contains: description, dependencies, coding standards, key types
- Loaded and cached at session start
- **Design goal**: Maximize context relevance while minimizing token usage

### Codex CLI: AGENTS.md
- Cross-tool convention (Codex, Cursor, Aider, Jules all support it)
- Layered discovery: global `~/.codex/AGENTS.md` → project walk (root to cwd) → `AGENTS.override.md`
- 32 KiB ceiling
- **Design goal**: Portable developer preferences across tools

## Dynamic Memory Layer

### Claude Code: Compaction pipeline
1. **Budget reduction** — cap tool outputs (50K/200K chars)
2. **Snip compact** — prune older messages in a tier
3. **Microcompact** — `cache_edits` API for incremental updates
4. **Context collapse** — emergency pruning (reactive compact)
5. **Autocompact** — automatic at 13K token threshold
- **Key insight**: Historical detail is progressively lost through summarization; precision degrades with session length

### Codex CLI: Generated Memories
- 2-layer model: AGENTS.md (static) + Memories (dynamic)
- Memories generated asynchronously after 6h idle
- 2 models: extract + merge
- 256 rollout cap; 30-day age-out
- **Key insight**: Memories are generated state, not meant for hand-editing; grep-based recall

## Context Management Strategy

| Strategy | Claude Code | Codex CLI |
|---|---|---|
| **When pressure hits** | Multi-tier compaction before every model call | No explicit compaction; relies on large context window |
| **What gets preserved** | Tool results persisted to disk for recovery | Memories consolidated into AGENTS.md-sized chunks |
| **User control** | Limited (can set thresholds) | Limited (can toggle memory generation) |
| **Granularity** | Per-message / per-tool-result | Per-conversation (after idle period) |

## Security & Privacy

- **Claude Code**: Memory files user-visible and editable; no known plaintext secret exposure; Docker sandboxing available
- **Codex CLI**: Built-in secret redaction before disk write; AppContainer/Landlock/seccomp on Windows; geographic limits (EEA/UK/CH excluded)

## Benchmarks & Efficiency

- **Claude Code**: 93% approval rate on internal benchmarks; 27% new-task enablement; 5-stage pipeline confirmed by reverse engineering
- **Codex CLI**: No published benchmarks specific to memory quality; relies on GPT-4o base model performance

## Trade-offs

| Strength | Claude Code | Codex CLI |
|---|---|---|
| **Long session handling** | ✅ Aggressive compaction prevents overflow | ⚠️ Relies on 256K context; no explicit management |
| **Historical precision** | ⚠️ Degrades through summarization | ✅ Memories preserve extracted facts |
| **Cross-tool portability** | ⚠️ CLAUDE.md is Claude-specific | ✅ AGENTS.md convention supported by 4+ tools |
| **Developer control** | ⚠️ Opaque compaction internals | ⚠️ Opaque memory generation |
| **Secret safety** | ✅ No known issues | ✅ Built-in redaction |
| **Recovery from crash** | ✅ Tool results on disk | ⚠️ Memories only after 6h consolidation |

## Related
- [[Claude Code]]
- [[Codex CLI]]
- [[context-compaction]]
- [S007](sources/S007.md), [S008](sources/S008.md), [S009](sources/S009.md), [S010](sources/S010.md), [S011](sources/S011.md), [S012](sources/S012.md)

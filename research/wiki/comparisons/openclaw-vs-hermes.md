# OpenClaw vs Hermes: Open-Source Framework Memory

> Two leading open-source agent frameworks with divergent memory philosophies: single-backend file-centric vs multi-backend pluggable.

## At a Glance

| Dimension | OpenClaw | Hermes |
|---|---|---|
| **Memory philosophy** | File-as-source-of-truth (Markdown + SQLite) | Layered pluggable (built-in + 8 external providers) |
| **Built-in memory** | MEMORY.md + daily notes + DREAMS.md | MEMORY.md + USER.md (always active) |
| **External providers** | 1 active at a time (Honcho, Mem0, etc. via plugins) | 8 plugins (Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory) |
| **Search** | Hybrid (70% vector + 30% BM25) in SQLite | FTS5 (local, free) + optional vector (external, paid) |
| **Provider switching** | Config-level, one active | Runtime pluggable, one active |
| **Context window mgmt** | Bootstrap file budget + truncation | 5 layers with clear cost/latency breakdown |
| **Hardware footprint** | Gateway 400–800 MB idle | Under 512 MB idle |
| **Stars / adoption** | ~6.3K (OpenViking, related) | 6K GitHub stars |

## Built-in Memory

### OpenClaw
- `MEMORY.md` (~2,200 chars) — curated long-term, injected every session
- `memory/YYYY-MM-DD.md` — daily working notes, today + yesterday auto-loaded
- `DREAMS.md` — optional dream diary
- **Key constraint**: Agent must self-distill from daily notes to MEMORY.md

### Hermes
- `MEMORY.md` (~2,200 chars / ~800 tokens) + `USER.md` (~1,375 chars / ~500 tokens)
- Loaded as **frozen snapshot** into system prompt at session start for prefix cache stability
- **Key constraint**: Static at session start; dynamic updates require explicit tool calls

## External Provider Architecture

### OpenClaw
- Default: builtin SQLite (FTS5 + vector via sqlite-vec)
- Optional: QMD, Honcho, LanceDB
- **Switching**: Config change + restart; auto-reindex on provider change

### Hermes
- 8 external providers available
- Built-in memory (MEMORY.md + USER.md) **always active** regardless of external provider
- External provider adds a 5th layer: contextual vector search
- **Cost transparency**: 3 layers local/free, 2 layers external/paid

## Search Quality vs Cost

| Search type | OpenClaw | Hermes |
|---|---|---|
| **Keyword** | FTS5 BM25 + CJK trigrams | FTS5 (built-in) |
| **Vector** | sqlite-vec (local, free) | External provider required |
| **Hybrid** | 70/30 vector/BM25 union | Not built-in; provider-dependent |
| **Embedding providers** | 7 (OpenAI, Gemini, Voyage, Mistral, DeepInfra, Ollama, Local GGUF) | Provider-dependent |

## Security & Privacy

- **OpenClaw**: CVE-2026-25253 (CVSS 9.8); plaintext secrets; no cloud telemetry unless external provider used
- **Hermes**: No known CVEs; local SQLite with no cloud telemetry by default; privacy audit (S076) flagged full messages sent to `api.honcho.dev` when Honcho provider active

## Trade-offs

| Strength | OpenClaw | Hermes |
|---|---|---|
| **Simplicity** | ✅ Single backend, fewer moving parts | ⚠️ 8 providers + 5 layers to understand |
| **Flexibility** | ⚠️ Config-switch only | ✅ Runtime pluggable, provider-agnostic |
| **Local search quality** | ✅ Hybrid built-in | ⚠️ Keyword only without external provider |
| **Resource efficiency** | ⚠️ 400–800 MB idle | ✅ <512 MB idle |
| **Multi-agent awareness** | ⚠️ Limited | ✅ Honcho integration supports multi-agent |
| **Vendor lock-in risk** | ✅ Low (Markdown files) | ⚠️ Higher (provider ecosystem dependency) |

## Related
- [[OpenClaw]]
- [[Hermes]]
- [[Honcho]]
- [[OpenViking]]
- [S001](sources/S001.md), [S013](sources/S013.md), [S014](sources/S014.md), [S015](sources/S015.md), [S026](sources/S026.md), [S035](sources/S035.md), [S136](sources/S136.md), [S137](sources/S137.md), [S140](sources/S140.md)

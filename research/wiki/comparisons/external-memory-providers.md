# External Memory Providers: Honcho vs Mem0 vs Hindsight vs Supermemory

> Four dedicated memory-as-a-service providers with distinct architectural philosophies and target users.

## At a Glance

| Dimension | Honcho | Mem0 | Hindsight | Supermemory |
|---|---|---|---|---|
| **Core abstraction** | User modeling + dialectic reasoning | ADD/UPDATE/DELETE/NOOP operations | 4-network memory (facts/experiences/entities/beliefs) | Hybrid RAG + structured fact extraction |
| **Target user** | Multi-agent systems, user-centric apps | General developers, broad framework support | Conversational agents needing rich user models | Enterprise, multi-modal ingestion |
| **Open source** | Partial (protocol + clients) | Apache 2.0 (core) | Not specified | Not specified |
| **Deployment** | Self-hosted or managed (api.honcho.dev) | Cloud API + self-hosted | Cloud + self-hosted | Cloud-only |
| **Pricing** | Free tier available | Free → $29/mo → Enterprise | Not disclosed | $19/mo (discrepancies noted: $29 on some pages) |
| **Framework integrations** | OpenClaw, Hermes | 8+ (OpenClaw, Hermes, etc.) | Hermes native | Broad connectors |

## Architecture Deep Dive

### Honcho: User modeling as first-class
- **App→User→Session→Message** hierarchy
- **Peer profiles** for multi-agent scenarios
- **Directional observation modes**: agent can observe user without user observing agent
- **Dialectic reasoning**: 3-pass depth with cold/warm prompt switching
- **Two-layer injection**: base context (profile, identity) + dialectic Q&A
- **Key insight**: User modeling and content memory are distinct capabilities requiring separate protocols

### Mem0: Operation-centric memory
- **CRUD operations**: ADD, UPDATE, DELETE, NOOP on semantic facts
- **Async consolidation**: 2 models (extract + merge), 6h idle trigger
- **Multi-signal retrieval**: entity linking, temporal reasoning, semantic search
- **Graph memory**: Optional via `pip install mem0ai[graph]`
- **Key insight**: Memory as a database with explicit operations, not just retrieval

### Hindsight: Network-centric memory
- **4 networks**: facts, experiences, entities, beliefs
- **3 operations**: retain, recall, reflect
- **Multi-level rewards** for non-linear reasoning
- **Key insight**: Memory is a graph of interconnected concepts, not a flat store

### Supermemory: Enterprise RAG
- **5-layer stack**: Connectors → Extractors → RAG → Memory Graph → User Profiles
- **Multi-modal**: PDFs, images (OCR), videos (transcription), code
- **Connectors**: Google Drive, Gmail, Notion, Slack, etc.
- **Key insight**: Memory is an enterprise knowledge pipeline, not just conversation storage

## Benchmark Comparison

| Benchmark | Mem0 | Hindsight | Honcho | Supermemory |
|---|---|---|---|---|
| **LoCoMo** | 67.13% (paper) / 91.6% (blog) | Not published | Not published | Not published |
| **LongMemEval** | 94.4% (blog) / 94.8% (2026-04) | 91.4% (Gemini-3) | Not published | Not published |
| **Independent verification** | Partial (community reports 49%) | None | None | None |

## Critical Discrepancies
- **Mem0**: Blog claims 94.4% LongMemEval vs community-independent evaluation showing 49% (S095). Variance may come from different model backends or evaluation protocols.
- **Supermemory**: Pricing inconsistent ($19 vs $29) across pages.
- **Hindsight**: 91.4% claim on Gemini-3 backend; no independent reproduction.

## When to Choose

| Use case | Best fit |
|---|---|
| **Multi-agent user modeling** | Honcho |
| **Broad framework support + open source** | Mem0 |
| **Rich psychological user profiles** | Hindsight |
| **Enterprise multi-modal ingestion** | Supermemory |
| **Self-hosting + data sovereignty** | Mem0 (Apache 2.0) |
| **Low latency, simple API** | Honcho |

## Related
- [[Honcho]]
- [[Mem0]]
- [[Hindsight]]
- [[Supermemory]]
- [[RetainDB]]
- [S073](sources/S073.md), [S074](sources/S074.md), [S078](sources/S078.md), [S079](sources/S079.md), [S081](sources/S081.md), [S094](sources/S094.md), [S095](sources/S095.md), [S096](sources/S096.md)

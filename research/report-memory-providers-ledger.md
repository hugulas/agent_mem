# Agent Memory Provider Ledger

> Comprehensive ledger of memory providers referenced by Hermes Agent, OpenClaw, and related agent frameworks.
> Generated: 2026-05-20
> Coverage: 8 primary providers + 2 embedding landscapes + 5 adjacent providers

---

## Table of Contents

1. [Provider Taxonomy](#1-provider-taxonomy)
2. [Structured-Extraction Providers](#2-structured-extraction-providers)
   - 2.1 Mem0
   - 2.2 Hindsight
   - 2.3 ByteRover
3. [Raw-Storage Providers](#3-raw-storage-providers)
   - 3.1 Holographic
   - 3.2 OpenViking
4. [User-Modeling Providers](#4-user-modeling-providers)
   - 4.1 Honcho
5. [Cloud-Infrastructure Providers](#5-cloud-infrastructure-providers)
   - 5.1 RetainDB
   - 5.2 Supermemory
6. [Embedding Provider Landscape (OpenClaw)](#6-embedding-provider-landscape-openclaw)
7. [Adjacent Memory Systems](#7-adjacent-memory-systems)
8. [Cross-Provider Comparison Matrix](#8-cross-provider-comparison-matrix)

---

## 1. Provider Taxonomy

The 8 Hermes-integrated providers cluster into 4 archetypes:

| Archetype | Providers | Core Value Proposition | Primary Trade-off |
|---|---|---|---|
| **Structured Extraction** | Mem0, Hindsight, ByteRover | LLM-curated structured knowledge with high recall accuracy | Higher compute cost, more dependencies |
| **Raw Storage** | Holographic, OpenViking | Minimal dependencies, deterministic retrieval, privacy-first | No structured extraction, lower semantic depth |
| **User Modeling** | Honcho | Deep dialectic understanding of user preferences and patterns | Privacy risk (cloud inference), AGPL license |
| **Cloud Infrastructure** | RetainDB, Supermemory | Managed scale, connectors, multi-modal, team sharing | Vendor lock-in, ongoing cost, no air-gap |

---

## 2. Structured-Extraction Providers

These providers run an LLM over conversations to extract, structure, and organize knowledge. They dominate accuracy benchmarks but require more compute and infrastructure.

---

### 2.1 Mem0

| Attribute | Detail |
|---|---|
| **Company** | Mem0 Inc. (formerly EmbedChain) |
| **License** | Apache 2.0 |
| **Stars / Downloads** | 52.8K GitHub stars / 14M downloads |
| **Funding** | $24M Series A |
| **Hosting** | Managed cloud, self-hosted OSS, local MCP |
| **Hermes Tools** | 3 (`mem0_search`, `mem0_add`, `mem0_get`) |
| **OpenClaw Integration** | Via MCP (`@mem0/openmemory-mcp`) |

**Architecture**

- **Extraction**: Single-pass ADD-only extraction (April 2026 algorithm). Treats agent-generated facts as first-class.
- **Operations**: ADD / UPDATE / DELETE / NOOP on extracted facts.
- **Retrieval**: Multi-signal retrieval in parallel — semantic similarity + BM25 keyword + entity matching, then fused.
- **Storage**: Pluggable vector backends (20 supported vector stores). Optional graph memory via `mem0ai[graph]`.
- **Temporal**: Time-aware retrieval ranks dated instances for current/past/future queries.

**Benchmarks**

| Benchmark | Score | Tokens/Query | Notes |
|---|---|---|---|
| LoCoMo (2026 algo) | 92.5% | 6,956 | +20 pts over 2025 algorithm |
| LongMemEval (2026) | 94.4% | 6,787 | +27 pts over 2025 |
| BEAM 1M | 64.1% | 6,719 | Production-scale eval |
| BEAM 10M | 48.6% | 6,914 | 10M token horizon |
| LoCoMo (2025 paper) | 67.13% | ~1,764/conv | p95 latency 0.200s |

**Pricing**

| Tier | Price | Limits |
|---|---|---|
| Free | $0 | Generous free tier for prototyping |
| Pro | $19/mo | Expanded limits |
| Scale | $249/mo | Production workloads |
| Enterprise | Custom | SSO, audit logs, on-prem |

**Strengths**
- Largest ecosystem (21 frameworks, AWS Agent SDK exclusive provider)
- Fully self-hostable with Apache 2.0 (no copyleft risk)
- Rapid algorithm iteration (2025 → 2026 +20 pts on LoCoMo)

**Weaknesses**
- 2025 paper scores modest vs Hindsight/ByteRover
- Users report indexing reliability issues under load
- Limited native ingestion pipelines beyond chat

**Best For**: Teams wanting a mature, broadly compatible memory layer with self-host fallback.

---

### 2.2 Hindsight

| Attribute | Detail |
|---|---|
| **Company** | Vectorize.io |
| **License** | MIT |
| **Hosting** | Local (embedded PostgreSQL) or Cloud |
| **Cost** | Free locally; pay-per-token cloud |
| **Hermes Tools** | 3 (`hindsight_retain`, `hindsight_recall`, `hindsight_reflect`) |
| **OpenClaw Integration** | Not documented as native plugin |

**Architecture**

- **Organization**: 4 logical networks — world facts, agent experiences, synthesized entity summaries, evolving beliefs.
- **Operations**: Retain (add structured evidence), Recall (multi-strategy retrieval), Reflect (cross-memory synthesis).
- **Retrieval**: Semantic + keyword + graph + temporal strategies combined.
- **Storage**: Structured knowledge (facts, entities, relationships) rather than text chunks.
- **Unique Feature**: `reflect` operation reads across all stored memories to derive higher-level insights and update the knowledge graph.

**Benchmarks**

| Benchmark | Backbone | Score | Notes |
|---|---|---|---|
| LongMemEval | Gemini-3 | **91.4%** | Highest validated provider score |
| LongMemEval | OSS-120B | 89.0% | Strong open-source result |
| LongMemEval | OSS-20B | 83.6% | Consumer GPU deployable |
| LoCoMo | OSS-120B | 89.61% | vs 75.78% strongest prior open |

**Strengths**
- Highest independently validated LongMemEval scores
- Achievable with open-source models (no frontier model required)
- Reflect operation is unique among providers
- Fully local free option with MIT license

**Weaknesses**
- Requires PostgreSQL (heavier than SQLite-only options)
- No zero-dependency mode
- Reflect operation is compute-intensive
- Smaller ecosystem than Mem0

**Best For**: Accuracy-critical workloads, local-first deployments, teams needing structured fact retrieval.

---

### 2.3 ByteRover

| Attribute | Detail |
|---|---|
| **Authors** | Nguyen et al. (academic/industry team) |
| **License** | Open source (license not specified in arXiv) |
| **Hosting** | Local filesystem (zero external infrastructure) |
| **Cost** | Free |
| **Hermes Tools** | 3 (`brv_query`, `brv_curate`, `brv_status`) |
| **OpenClaw Integration** | Not documented |

**Architecture**

- **Core Innovation**: Inverts the memory pipeline — the same LLM that reasons also curates, structures, and retrieves knowledge.
- **Context Tree**: Hierarchical filesystem-based knowledge graph — Domain → Topic → Subtopic → Entry.
- **Curate Operations**: 5 atomic operations (UPSERT, MERGE, DELETE, LINK, UNLINK) with per-operation feedback loop.
- **Retrieval**: 5-tier progressive strategy — MiniSearch → fuzzy → semantic → agentic → direct response. Most queries resolve <100ms without LLM calls.
- **Lifecycle**: Adaptive Knowledge Lifecycle (AKL) with importance decay (0.995^Δt) and recency decay (e^(-Δt/30)).
- **Storage**: Human-readable markdown files; version controllable; zero external DBs.

**Benchmarks**

| Benchmark | Score | Notes |
|---|---|---|
| LoCoMo | **96.1%** | Highest overall; +6.2pp over HonCho |
| LongMemEval-S | 92.8% | Below Chronos-High 95.6% (Claude Opus) |
| Temporal (LoCoMo) | 97.8% | Structured timestamp metadata |
| Multi-hop (LoCoMo) | +9.3pp vs HonCho | Explicit inter-entry relations |

**Unique Integration Point**: Pre-compression extraction hook in Hermes — fires before context compression discards in-flight knowledge.

**Strengths**
- Highest LoCoMo accuracy of any tested system
- Zero external infrastructure (no vector DB, no graph DB, no embeddings)
- Fully inspectable human-readable markdown storage
- Agent-native feedback loop impossible with external HTTP services

**Weaknesses**
- Very new (April 2026 paper); limited production validation
- Curation quality depends on backbone LLM
- Directory structure design is manual upfront cost
- Non-trivial setup

**Best For**: Developers wanting maximum accuracy with full data sovereignty and inspectability.

---

## 3. Raw-Storage Providers

These providers prioritize minimal dependencies, deterministic retrieval, and privacy over structured semantic extraction.

---

### 3.1 Holographic

| Attribute | Detail |
|---|---|
| **Concept Origin** | Holographic Reduced Representations (Plate, 1995) |
| **License** | MIT (via Hermes integration) |
| **Hosting** | Local SQLite only |
| **Cost** | Completely free |
| **Hermes Tools** | 2 (`fact_store` with 9 actions, `fact_feedback`) |
| **Dependencies** | Zero external pip dependencies; NumPy optional for HRR algebra |

**Architecture**

- **Representation**: HRR algebra — memories as superposed complex-valued vectors; recall is algebraic rather than similarity-based.
- **Storage**: Local SQLite + FTS5.
- **Retrieval**: 3-way hybrid — FTS5 full-text + Jaccard word overlap + HRR vector similarity.
- **Trust Scoring**: Dynamic trust scores per memory; recalled/confirmed memories gain trust; contradicted memories decay. Asymmetric feedback (+0.05 helpful / -0.10 unhelpful).
- **Entity Association**: Automatic named entity extraction; supports multi-entity compositional reasoning.
- **Unique Operations**: `probe` (entity-specific recall), `reason` (cross-entity AND queries), `contradict` (conflict detection).

**Benchmarks**: No published benchmark scores.

**Strengths**
- Zero dependencies — works instantly with no accounts, APIs, or Docker
- Sub-millisecond retrieval latency
- Most privacy-preserving by construction (no network calls)
- Self-correcting memory store via trust scoring

**Weaknesses**
- No LLM-based structured extraction
- No knowledge graph construction
- No published accuracy benchmarks
- Limited to conversational content storage

**Best For**: Air-gapped environments, zero-cost setups, privacy-critical use cases, rapid prototyping.

---

### 3.2 OpenViking

| Attribute | Detail |
|---|---|
| **Company** | ByteDance Volcengine |
| **License** | Apache 2.0 |
| **Stars** | 6.3K+ GitHub |
| **Hosting** | Self-hosted only |
| **Cost** | Free |
| **Hermes Tools** | 5 |
| **OpenClaw Integration** | Not documented |

**Architecture**

- **Paradigm**: Filesystem metaphor (`viking://` protocol) replacing flat vector RAG.
- **Tiered Loading**: L0 abstract (~100 tokens), L1 overview (~2K tokens), L2 full content.
- **Retrieval**: Directory recursive retrieval combining path traversal with semantic search.
- **Observability**: Visualized retrieval trajectory for debugging.
- **Storage**: Filesystem hierarchy; VikingDB vector index.

**Token Efficiency**

- 50-runbook example: RAG loads 50K tokens vs OpenViking ~5K L0 + ~6K L1 + one L2.
- **80–90% token savings** when memory stores are large.

**Strengths**
- Massive token reduction for long-running agents
- Apache 2.0 license
- Strong observability (retrieval trajectory visualization)

**Weaknesses**
- Self-hosted only (requires Docker + Go + C++ compiler)
- Depends on external LLM provider for L0/L1 generation
- Very new project (early 2026)
- Not offline-capable

**Best For**: Token-cost-sensitive deployments, regulated industries needing data sovereignty.

---

## 4. User-Modeling Providers

---

### 4.1 Honcho

| Attribute | Detail |
|---|---|
| **Company** | Plastic Labs |
| **License** | AGPL v3.0 (open source); managed API (proprietary) |
| **Hosting** | Cloud (`api.honcho.dev`) or self-hosted |
| **Cost** | Cloud paid / self-hosted free |
| **Hermes Tools** | 5 (`honcho_profile`, `honcho_search`, `honcho_context`, `honcho_reasoning`, `honcho_conclude`) |
| **OpenClaw Integration** | Native plugin (`@honcho-ai/openclaw-honcho`) |

**Architecture**

- **Core Model**: Dialectic reasoning — after each turn, analyzes exchange to derive insights about user preferences, habits, goals.
- **Context Injection**: 2-layer base (session summary + user representation + peer card) refreshed on `contextCadence` + dialectic supplement refreshed on `dialecticCadence`.
- **Multi-Agent**: Per-peer profile separation prevents cross-contamination.
- **Cold/Warm Prompts**: Cold start queries general facts; warm queries prioritize session-scoped context.
- **Depth**: 1–3 passes (Pass 0: main prompt; Pass 1: self-audit; Pass 2: reconciliation).

**Config Knobs**

| Knob | Default | Controls |
|---|---|---|
| `contextCadence` | 1 | Base context refresh interval (turns) |
| `dialecticCadence` | 2 | Dialectic LLM call interval (turns) |
| `dialecticDepth` | 1 | Passes per dialectic invocation |

**Privacy Concerns**

- Both peers registered with `observe_me=True` by default.
- Every message sent verbatim to `api.honcho.dev`.
- Background prefetch threads run between turns with no visible indicator.
- Local memory files (MEMORY.md, USER.md, SOUL.md) uploaded during migration.
- Hermes README states "All data stays on your machine" with no exception for Honcho cloud integration.

**Strengths**
- Only provider built specifically for deep user modeling
- Multi-agent peer isolation is unique
- Dialectic reasoning depth is unmatched
- OpenClaw and Hermes both have native plugins

**Weaknesses**
- AGPL v3.0 creates copyleft risk for commercial self-hosting
- Significant privacy gap in setup flow disclosure
- Cloud dependency for full feature set
- No published accuracy benchmarks

**Best For**: Personal AI companions, multi-agent systems needing deep user-agent alignment.

---

## 5. Cloud-Infrastructure Providers

---

### 5.1 RetainDB

| Attribute | Detail |
|---|---|
| **License** | Open source (GitHub available); cloud service proprietary |
| **Hosting** | Cloud primary; self-hosted via Docker Compose |
| **Cost** | Free tier (10K ops/mo) / Pro $20/mo / Scale $99/mo / Max $299/mo / Enterprise custom |
| **Hermes Tools** | 5 (`retaindb_profile`, `retaindb_search`, `retaindb_context`, `retaindb_remember`, `retaindb_forget`) |
| **OpenClaw Integration** | MCP server available |

**Architecture**

- **Retrieval**: Hybrid search — vector similarity + BM25 keyword + cross-encoder reranking in parallel.
- **Memory Types**: 7 typed categories — factual, preference, event, relationship, opinion, goal, instruction.
- **Delta Compression**: Detects context changes between turns; sends only differences. Claims 50–90% token savings (15,000 → 1,500 tokens example).
- **Temporal**: Version chains track information evolution; `validFrom`/`validUntil` on facts.
- **Memory Graph**: Relations include `updates`, `contradicts`, `supports`, `derives`.
- **Extraction**: Auto-extraction via Claude Sonnet 4.5.
- **Connectors**: 15+ including GitHub, Notion, Slack, Discord, Confluence, PostgreSQL, MongoDB.
- **Integration**: MCP server for Claude Desktop; framework adapters for Vercel AI SDK, LangChain, LangGraph.

**Performance Claims**

| Metric | Claim |
|---|---|
| Memory retrieval | <50ms |
| Memory retention | 100% |
| Uptime SLA | 99.9% |
| Preference recall | 88% (claimed SOTA) |
| Docs hallucination | 0% (claimed) |

**Strengths**
- Delta compression is a genuine token-cost innovation
- Strong connector ecosystem
- Transparent pricing
- Self-hostable open-source option

**Weaknesses**
- Paid-only for production (no unlimited free tier)
- Some claims (0% hallucination, 88% preference recall) from comparison blogs, not independent verification
- Smaller community than Mem0/Supermemory

**Best For**: Teams with strict retrieval precision needs, multi-turn conversational agents, organizations needing connector ecosystem.

---

### 5.2 Supermemory

| Attribute | Detail |
|---|---|
| **Founder** | Dhravya Shah (19 years old at founding) |
| **Funding** | $2.6M seed (Google and Cloudflare executives) |
| **Stars** | 21.7K GitHub |
| **License** | Proprietary (cloud-only) |
| **Hosting** | Cloud API only |
| **Cost** | Free tier / Pro ~$29/mo (from review sites); enterprise undisclosed |
| **Hermes Tools** | 4 (context fencing, session graph ingest, multi-container) |
| **OpenClaw Integration** | Native plugin + ClawTank managed option |

**Architecture**

- **5-Layer Stack**: Connectors → Extractors → RAG → Memory Graph → User Profiles.
- **Ingestion**: Text, conversations, files (PDF, images via OCR, video via transcription), code.
- **Retrieval**: Semantic + keyword hybrid; sub-300ms latency.
- **Memory Graph**: Tracks concept relationships, handles contradictions, reasons temporally.
- **User Profiles**: Static facts (always know) + dynamic episodic information.
- **Connectors**: Google Drive, Gmail, Notion, OneDrive, GitHub.
- **Evolution**: Memories update, extend, and expire automatically.

**Benchmarks**

| Metric | Score |
|---|---|
| LongMemEval | 85.2% |
| LongMemEval-S | 85.4% |
| Single-session recall | 92.3% |
| Multi-session accuracy | 76.7% |
| Recall latency | sub-300ms |

**Production Notes**
- One user reported 6,500+ API calls in days without caching; fixed with multi-layer caching achieving **98% reduction** (1,584/day → 33/day).
- Knowledge graph refresh was ~61 calls every 30 minutes before optimization.

**Strengths**
- Strong benchmark performance
- Multi-modal support
- Built-in productivity connectors
- Fast retrieval
- Active development

**Weaknesses**
- Cloud-only (no self-host option)
- Pricing not publicly disclosed
- Core engine closed source
- Higher lock-in risk than open-source alternatives

**Best For**: Teams needing multi-modal ingestion, productivity tool connectors, and managed infrastructure without ops overhead.

---

## 6. Embedding Provider Landscape (OpenClaw)

OpenClaw supports 7 embedding providers for its vector search backend:

| Provider | Type | Size / Cost | Latency | Best For |
|---|---|---|---|---|
| OpenAI | Cloud API | Pay-per-token | ~200ms | Accuracy, multilingual |
| Gemini | Cloud API | Pay-per-token | ~200ms | Google ecosystem integration |
| Voyage | Cloud API | Pay-per-token | ~200ms | High-quality embeddings |
| Mistral | Cloud API | Pay-per-token | ~200ms | European data residency |
| DeepInfra | Cloud API | Pay-per-token | ~200ms | Cost optimization |
| Ollama | Local | Free | ~61ms CPU | Privacy, no API keys |
| Local GGUF | Local | ~0.6GB model | ~4ms GPU | Maximum privacy, speed |

OpenClaw also supports 4 memory backends:
1. **Builtin**: SQLite + FTS5 + sqlite-vec (default)
2. **QMD**: Quantum Markdown Database (binary dependency)
3. **Honcho**: External user modeling service
4. **LanceDB**: External vector database

---

## 7. Adjacent Memory Systems

| System | Type | License | Key Differentiator | Hermes/OpenClaw Integration |
|---|---|---|---|---|
| **Zep** | Temporal knowledge graph | Open source + Cloud | Graphiti engine; low-latency enterprise memory | Not native Hermes |
| **LangMem** | LangChain memory | Open source | Native LangGraph support; memory APIs + in-conversation tools | Not native Hermes |
| **Letta** | Virtual context management | Open source | LLM self-edits memory hierarchy; MemGPT successor | Not native Hermes |
| **Graphiti** | Temporal knowledge graph | Open source | Time-aware dynamic knowledge graphs | Not native Hermes |
| **Cognee** | Knowledge graph memory | Open source | Structures unstructured data into queryable knowledge graphs | Not native Hermes |

---

## 8. Cross-Provider Comparison Matrix

### 8.1 Benchmark Scores (where available)

| Provider | LoCoMo | LongMemEval | LongMemEval-S | BEAM 1M | Tokens/Query |
|---|---|---|---|---|---|
| ByteRover | **96.1%** | 92.8% (S) | — | — | — |
| HonCho | 89.9% | — | — | — | — |
| Hindsight | 89.61% | **91.4%** | — | — | — |
| Mem0 (2026) | 92.5% | 94.4% | — | 64.1% | ~6,956 |
| Mem0 (2025) | 67.13% | — | 67.6% | — | ~1,764/conv |
| Supermemory | — | 85.2% | 85.4% | — | — |
| RetainDB | — | — | 79% | — | — |
| Holographic | — | — | — | — | — |
| OpenViking | — | — | — | — | — |

*Note: Benchmarks use different judge models and configurations; direct cross-row comparison should be treated cautiously. ByteRover arXiv (S082) used identical judge config for all systems in its comparison.*

### 8.2 Feature Matrix

| Feature | Honcho | Mem0 | Hindsight | Holographic | OpenViking | RetainDB | ByteRover | Supermemory |
|---|---|---|---|---|---|---|---|---|
| Structured extraction | ✔ (dialectic) | ✔ | ✔ | ✗ | ✗ | ✔ | ✔ | ✔ |
| Knowledge graph | ✗ | △ (optional) | ✔ | ✗ | ✗ | ✔ | ✔ (tree) | ✔ |
| Vector search | ✔ (semantic) | ✔ | ✔ | △ (HRR) | ✔ | ✔ | ✗ | ✔ |
| Full-text search | ✔ | △ (BM25) | ✔ | ✔ (FTS5) | ✗ | ✔ (BM25) | ✔ (MiniSearch) | ✔ |
| Temporal reasoning | ✗ | ✔ (2026) | ✔ | ✗ | ✗ | ✔ | ✔ | ✔ |
| Multi-agent profiles | ✔ | ✗ | ✔ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Local/offline capable | △ (self-host) | △ (self-host) | ✔ | ✔ | △ (needs LLM) | △ (self-host) | ✔ | ✗ |
| Zero external deps | ✗ | ✗ | ✗ | ✔ | ✗ | ✗ | ✔ | ✗ |
| Delta compression | ✗ | ✗ | ✗ | ✗ | △ (L0/L1/L2) | ✔ | ✗ | ✗ |
| Multi-modal ingestion | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| Productivity connectors | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ (15+) | ✗ | ✔ (5+) |
| MCP server | ✗ | ✔ | ✗ | ✗ | ✗ | ✔ | ✔ | ✗ |
| Trust scoring | ✗ | ✗ | ✗ | ✔ | ✗ | ✗ | △ (lifecycle) | ✗ |
| Open source | ✔ (AGPL) | ✔ (Apache) | ✔ (MIT) | ✔ (MIT) | ✔ (Apache) | ✔ | ✔ | ✗ |
| Self-hostable | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✗ |

### 8.3 Hermes Integration Comparison

| Provider | Hermes Tools | Setup | Config File | Cost in Hermes |
|---|---|---|---|---|
| Honcho | 5 | `hermes memory setup` → honcho | `honcho.json` | Cloud paid / self-host free |
| Mem0 | 3 | `hermes memory setup` → mem0 | `config.yaml` | Freemium |
| Hindsight | 3 | `hermes memory setup` → hindsight | `config.yaml` | Free local / paid cloud |
| Holographic | 2 | `hermes memory setup` → holographic | `config.yaml` | Free |
| OpenViking | 5 | `hermes memory setup` → openviking | `.env` | Free (self-host) |
| RetainDB | 5 | `hermes memory setup` → retaindb | `.env` | $20+/mo |
| ByteRover | 3 | `hermes memory setup` → byterover | `config.yaml` | Free local / freemium cloud |
| Supermemory | 4 | `hermes memory setup` → supermemory | `config.yaml` | Freemium |

### 8.4 Decision Quick Reference

| If your priority is... | Choose | Avoid |
|---|---|---|
| Best accuracy (validated) | Hindsight or ByteRover | Mem0 (2025 scores) |
| Zero dependencies / air-gap | Holographic | All cloud providers |
| Token cost reduction | OpenViking or RetainDB | Full-context approaches |
| Deep user modeling | Honcho | All others |
| Largest ecosystem / maturity | Mem0 | ByteRover, RetainDB |
| Multi-modal / connectors | Supermemory | Holographic, OpenViking |
| Commercial-safe license | Mem0 (Apache), Hindsight (MIT), Holographic (MIT) | Honcho (AGPL) |
| Full data sovereignty | Holographic, ByteRover, OpenViking | Supermemory, RetainDB (cloud) |
| Fastest setup | Holographic (built-in, no account) | OpenViking (needs Docker+Go+C++) |
| Lowest latency | Holographic (sub-ms) | Mem0 cloud API |

---

*End of Ledger*

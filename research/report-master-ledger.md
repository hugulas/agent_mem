# Master Technology Ledger: Agent Memory Systems & Ecosystem

> Comprehensive ledger of all technologies researched across three phases:
> - Phase 1: Open-source agent frameworks (OpenClaw, Claude Code, Codex CLI, Hermes)
> - Phase 2: ByteDance + US tech giants + Karpathy Wiki
> - Phase 3: Memory providers + academic frontier
> Generated: 2026-05-20
> Total entries: 28 primary technologies + 12 academic architectures

---

## Table of Contents

1. [Taxonomy Overview](#1-taxonomy-overview)
2. [Open-Source Agent Frameworks](#2-open-source-agent-frameworks)
3. [Native Agent Models](#3-native-agent-models)
4. [Cloud-Native Personal Memory](#4-cloud-native-personal-memory)
5. [Managed Agent Memory Services](#5-managed-agent-memory-services)
6. [External Memory Providers](#6-external-memory-providers)
7. [Embedding & Retrieval Infrastructure](#7-embedding--retrieval-infrastructure)
8. [Academic Memory Architectures](#8-academic-memory-architectures)
9. [Workflow Paradigms](#9-workflow-paradigms)
10. [Master Comparison Matrix](#10-master-comparison-matrix)

---

## 1. Taxonomy Overview

All researched technologies cluster into **9 categories**:

| Category | Count | Examples |
|---|---|---|
| **Open-Source Frameworks** | 4 | OpenClaw, Claude Code, Codex CLI, Hermes |
| **Native Agent Models** | 2 | UI-TARS, 豆包手机 |
| **Cloud-Native Personal Memory** | 4 | Google Astra/Gemini, Microsoft Copilot, Apple Intelligence, Meta LLaMA |
| **Managed Agent Memory Services** | 2 | Amazon Bedrock AgentCore, Azure Foundry Agent Memory |
| **External Memory Providers** | 8 | Honcho, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory, OpenViking |
| **Embedding Infrastructure** | 1 | OpenClaw 7-provider embedding layer |
| **Academic Architectures** | 12 | HyperMem, MAGMA, MemMA, MemOS, A-MEM, EverMemOS, TiMem, AtlasKV, etc. |
| **Workflow Paradigms** | 1 | Karpathy LLM Wiki |
| **Benchmarks** | 3 | LoCoMo, LongMemEval, BEAM |

---

## 2. Open-Source Agent Frameworks

### 2.1 OpenClaw

| Attribute | Detail |
|---|---|
| **Type** | Multi-channel agent framework |
| **Language** | Node.js/TypeScript |
| **Stars** | ~179K (largest open-source agent framework) |
| **Memory Architecture** | Markdown-first + SQLite hybrid search |
| **Storage** | MEMORY.md, daily notes, DREAMS.md; SQLite + FTS5 + sqlite-vec |
| **Retrieval** | Hybrid 70% vector + 30% BM25; MMR diversity; temporal decay (30-day half-life) |
| **Chunking** | 400 tokens / 80 overlap |
| **Flush** | Pre-compaction at 4000 token soft threshold / 2MB transcript threshold |
| **Embedding** | 7 providers (OpenAI, Gemini, Voyage, Mistral, DeepInfra, Ollama, Local GGUF ~0.6GB) |
| **Memory Backends** | Builtin SQLite, QMD, Honcho, LanceDB |
| **Idle RAM** | 400–800 MB (gateway) |
| **Recall Latency** | ~19,593 ms (300 events, benchmark) |
| **Security** | CVE-2026-25253 (CVSS 8.8–9.8); plaintext secrets in Markdown/SQLite |

### 2.2 Claude Code

| Attribute | Detail |
|---|---|
| **Type** | Coding agent CLI/IDE harness |
| **Company** | Anthropic |
| **Memory Architecture** | 4-level CLAUDE.md hierarchy + 5-layer compaction |
| **CLAUDE.md Levels** | L1 Project → L2 Subsystem → L3 Module → L4 Package |
| **Compaction Pipeline** | Budget → Snip → Microcompact (cache_edits) → Context Collapse → Autocompact |
| **Auto-Memory** | Writes learnings back to CLAUDE.md; three scope levels |
| **Tool Budget** | 50K chars/tool, 200K chars/message |
| **Auto-Compact Threshold** | effectiveContextWindow - 13,000 tokens |
| **Circuit Breaker** | 3 consecutive autocompact failures |
| **Idle RAM** | 4 GB minimum / 16 GB daily-driver floor |
| **Prompt Cache** | Native Anthropic integration (unique cost advantage) |

### 2.3 Codex CLI

| Attribute | Detail |
|---|---|
| **Type** | Coding agent terminal tool |
| **Company** | OpenAI |
| **Language** | Rust binary (~50MB) |
| **Memory Architecture** | 2-layer: static AGENTS.md + generated Memories |
| **AGENTS.md Cap** | 32 KiB (silent truncation) |
| **Consolidation** | Async background; 6h idle threshold; 256 rollout cap; 30-day age-out |
| **Models** | Extract model + merge model (configurable) |
| **Recall** | grep-based over markdown files |
| **Geographic Limits** | EEA/UK/CH excluded from Memories |
| **Idle RAM** | 4 GB min / 8 GB rec |

### 2.4 Hermes Agent

| Attribute | Detail |
|---|---|
| **Type** | Multi-channel autonomous agent framework |
| **Company** | Nous Research |
| **Language** | Python 3.11+ |
| **Stars** | 6K+ (first month) |
| **Memory Architecture** | 5 layers: context window → skills → contextual vector → Honcho → FTS5 |
| **Built-in Memory** | MEMORY.md (2200 chars) + USER.md (1375 chars) |
| **FTS5 Retrieval** | ~10 ms across 10K docs |
| **External Providers** | 8 (Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory) |
| **Idle RAM** | <512 MB |
| **Recall Latency** | ~113 ms (300 events, benchmark) |
| **Multi-Agent** | Native DAG coordination; 98.2% success (4 agents) |

---

## 3. Native Agent Models

### 3.1 UI-TARS

| Attribute | Detail |
|---|---|
| **Type** | End-to-end GUI agent model |
| **Company** | ByteDance Seed |
| **License** | Apache 2.0 |
| **Architecture** | 532M vision encoder + 23B active (230B total) MoE LLM |
| **Memory State** | Mt = (Wt, Et): Working Memory + Episodic Memory |
| **Working Memory** | Stores recent steps in high fidelity |
| **Episodic Memory** | Semantically compressed episode summaries |
| **Reasoning** | ReAct paradigm; System 1 & 2 reasoning |
| **ScreenSpotPro** | 61.6% (vs Claude-3 27.7%, GPT-4o 41.2%) |
| **Coordinate Error** | <5 pixels |
| **Versions** | 1.5 (open source), 2.0 (technical report) |

### 3.2 豆包手机 AI

| Attribute | Detail |
|---|---|
| **Type** | System-level mobile AI agent |
| **Company** | ByteDance |
| **Architecture** | "Cloud understanding + local storage + vector retrieval" |
| **Cloud Model** | InternVL3-2B |
| **Upload** | ~250KB packet every 3–5s (compressed screenshot + context) |
| **Return** | ~1KB action instruction |
| **Integration** | System-signed input injection; frame buffer direct read |

---

## 4. Cloud-Native Personal Memory

### 4.1 Google (Astra / Gemini / NotebookLM)

| Attribute | Detail |
|---|---|
| **Astra** | Multimodal memory research prototype; phone camera + glasses |
| **Gemini Context** | 2M tokens (1.5 Pro); context caching API |
| **KV Cache** | ~15GB per 1M tokens per user |
| **NotebookLM** | Evolving document context synthesis |
| **Status** | Astra is research prototype; Gemini caching is production |

### 4.2 Microsoft (Copilot / Azure Foundry)

| Attribute | Detail |
|---|---|
| **Copilot Memory** | GA July 2025; 3 scopes (User/Repository/Session) |
| **User Memory** | First 200 lines auto-loaded; intent-driven storage |
| **VS Code Memory** | Memory tool in preview; all data stored locally |
| **Azure Foundry** | Agent Memory preview; Cosmos DB + Azure AI Search backend |
| **Governance** | Tenant admin controls; automated retention and disposal |

### 4.3 Amazon (Bedrock AgentCore)

| Attribute | Detail |
|---|---|
| **Service** | Bedrock AgentCore Memory |
| **Architecture** | Fully managed STM + LTM |
| **Extraction** | Auto-extraction (semantic, preference, summary, episodic strategies) |
| **Infrastructure** | S3 Vectors (native vector storage); Neptune Analytics (graph) |
| **Integration** | Bedrock AgentCore Runtime, Identity, Gateway |
| **Status** | Very new (early 2026); limited deployment data |

### 4.4 Apple (Intelligence / Siri)

| Attribute | Detail |
|---|---|
| **Architecture** | On-device 3B model + Private Cloud Compute (PCC) |
| **Semantic Index** | Vector DB of personal data; App Intents toolbox |
| **Orchestration** | Siri as orchestrator; Ferret-UI for screen understanding |
| **Privacy** | Zero data retention in PCC; cryptographic attestation |
| **Status** | Siri overhaul delayed to spring 2026; current capabilities limited |

### 4.5 Meta (LLaMA)

| Attribute | Detail |
|---|---|
| **Context Window** | LLaMA 4: 10M tokens |
| **Memory** | Experimental persistent agents; no dedicated memory product |
| **Ecosystem** | Left to third-party frameworks (LangGraph, CrewAI, MindStudio) |
| **Status** | Least mature among US tech firms for persistent memory |

---

## 5. Managed Agent Memory Services

### 5.1 Amazon Bedrock AgentCore Memory

See 4.3 above.

### 5.2 Azure AI Foundry Agent Memory

| Attribute | Detail |
|---|---|
| **Status** | Preview (late 2025) |
| **Backend Options** | Cosmos DB + Azure AI Search |
| **Identity** | Entra Agent ID for agent IAM |
| **Scope** | Enterprise-focused; distinct from consumer Copilot Memory |

---

## 6. External Memory Providers

See `report-memory-providers-ledger.md` for full detail. Summary:

| Provider | Archetype | License | Hosting | Best For |
|---|---|---|---|---|
| **Honcho** | User Modeling | AGPL v3.0 | Cloud/self-host | Deep personalization |
| **Mem0** | Structured Extraction | Apache 2.0 | Cloud/self-host/MCP | Largest ecosystem |
| **Hindsight** | Structured Extraction | MIT | Local/cloud | Highest validated accuracy |
| **Holographic** | Raw Storage | MIT | Local only | Zero dependencies, air-gap |
| **OpenViking** | Raw Storage | Apache 2.0 | Self-host only | Token cost reduction |
| **RetainDB** | Cloud Infrastructure | Open source + proprietary | Cloud/self-host | Delta compression |
| **ByteRover** | Structured Extraction | Open source | Local only | Agent-native curation |
| **Supermemory** | Cloud Infrastructure | Proprietary | Cloud only | Connectors, multi-modal |

---

## 7. Embedding & Retrieval Infrastructure

### 7.1 OpenClaw Embedding Providers

| Provider | Type | Size | Latency | Best For |
|---|---|---|---|---|
| OpenAI | Cloud API | Pay-per-token | ~200ms | Accuracy |
| Gemini | Cloud API | Pay-per-token | ~200ms | Google ecosystem |
| Voyage | Cloud API | Pay-per-token | ~200ms | Quality |
| Mistral | Cloud API | Pay-per-token | ~200ms | EU data residency |
| DeepInfra | Cloud API | Pay-per-token | ~200ms | Cost optimization |
| Ollama | Local | Free | ~61ms CPU | Privacy |
| Local GGUF | Local | ~0.6GB | ~4ms GPU | Maximum privacy |

### 7.2 Vector Database Landscape

| Database | Used By | Notes |
|---|---|---|
| SQLite + sqlite-vec | OpenClaw (builtin), Holographic | Zero dependency; sufficient for small scale |
| PostgreSQL + pgvector | Hindsight (local), RetainDB | Full SQL + vector; heavier setup |
| Qdrant | Mem0 (self-host) | Rust-based; fast |
| VikingDB | OpenViking | ByteDance cloud vector index |
| LanceDB | OpenClaw (optional) | Columnar vector DB |
| Pinecone/Weaviate/Milvus | Various cloud providers | Enterprise scale |

---

## 8. Academic Memory Architectures

### 8.1 Surveys & Taxonomies

| Paper | Authors | Year | Key Contribution |
|---|---|---|---|
| Memory for Autonomous LLM Agents | Du | 2026 | Write-manage-read loop; 3D taxonomy; 5 mechanism families; open challenges |
| Anatomy of Agentic Memory | Jiang et al. | 2026 | MAGMA architecture; architecture/organization/retrieval taxonomy |
| Graph-based Agent Memory | Anonymous | 2026 | Comprehensive KG/TG/hypergraph survey for agent memory |

### 8.2 Novel Architectures

| Paper | Architecture | Key Innovation | Relation to Commercial Systems |
|---|---|---|---|
| **HyperMem** (2026) | Hypergraph memory | 3-level hierarchy (Topic→Episode→Fact); hyperedges for high-order associations | Goes beyond pairwise graphs (Zep, Hindsight) |
| **MAGMA** (2026) | Multi-graph memory | Multiple interconnected graphs for different memory types | Cited as graph-structured memory representative |
| **MemMA** (2026) | Multi-agent memory cycle | Coordinates memory cycle through multi-agent reasoning; in-situ self-evolution | Theoretical framework for multi-agent memory sharing |
| **MemOS** (2025) | OS-inspired memory | Short/Mid/Long-term tiers; heat-based update; two-tier retrieval | Similar to MemGPT but with OS scheduling principles |
| **A-MEM** (2025) | Agentic Zettelkasten | Interconnected notes with autonomous linking; dynamic evolution | Similar philosophy to ByteRover's Context Tree |
| **EverMemOS** (2026) | Self-organizing memory OS | Engram-inspired lifecycle: episodic trace → semantic consolidation → reconstructive recollection | Most biologically-inspired architecture |
| **TiMem** (2026) | Temporal-hierarchical | Temporal-hierarchical consolidation for long-horizon conversations | Addresses temporal reasoning gaps in flat memory |
| **AtlasKV** (2025) | Parametric KG integration | Billion-scale KG (1B triples) in <20GB VRAM; no external retriever | Upper bound of structured memory scale |
| **Memory-R1** (2025) | RL memory management | Reinforcement learning for memory construction/retrieval policies | RL approach to memory optimization |
| **ReMemR1** (2026) | Revisitable memory | History-aware retrieval + RL for long-context agents | Combines memory with RL-based long-context reasoning |

### 8.3 Context Compression Research

| Paper | Key Finding | Implication for Frameworks |
|---|---|---|
| **Slipstream** (2026) | Compaction increases E2E time 26–44%; silently drops safety-critical context | Validates need for pre-compression extraction hooks (ByteRover, Hermes) |
| **ACON** (2025) | Optimizes compression for long-horizon agents | Could improve Claude Code / OpenClaw compaction pipelines |
| **Complexity Trap** (2025) | Simple observation masking as efficient as LLM summarization | Challenges assumption that LLM-based compaction is always better |
| **CMV: DAG-Based** (2026) | DAG-based structurally lossless trimming | Alternative to lossy LLM summarization |
| **Missing Memory Hierarchy** (2026) | Demand paging for LLM context (Denning working set model) | OS principles applied to context windows; could inform MemGPT-like systems |

---

## 9. Workflow Paradigms

### 9.1 Karpathy LLM Wiki

| Attribute | Detail |
|---|---|
| **Type** | Workflow paradigm (not a product) |
| **Core Idea** | LLM acts as compiler to build/maintain markdown wiki from raw sources |
| **Architecture** | raw/ → wiki/ → schema layers |
| **Scale** | ~100 articles / ~400,000 words on single topic |
| **Tools** | Obsidian as IDE; Claude Code/Codex as compiler |
| **Philosophy** | "Compile once, maintain continuously" vs "retrieve at query time" (RAG) |
| **Limitations** | Scale limit ~1M words before RAG needed; topic boundary decisions are ad hoc |
| **Views** | 1.2M+ (X post, April 2026) |

---

## 10. Master Comparison Matrix

### 10.1 By Memory Layer

| Technology | Working Memory | Short-Term Memory | Long-Term Memory | Episodic Memory | Semantic Memory |
|---|---|---|---|---|---|
| **OpenClaw** | Context window | SQLite FTS5 | MEMORY.md | Daily notes | Hybrid search |
| **Claude Code** | Context window | Tool results (disk) | CLAUDE.md | Auto-memory | LLM scan |
| **Codex CLI** | Context window | Session history | AGENTS.md | Memories (generated) | grep |
| **Hermes** | Context window | FTS5 session | MEMORY.md/USER.md | Provider-dependent | Provider-dependent |
| **UI-TARS** | Wt (recent steps) | — | Et (compressed) | Episode summaries | Semantic compression |
| **Google Astra** | Context window | — | Cloud persistent | Multimodal | Semantic index |
| **Microsoft Copilot** | Context window | — | User/Repo/Session | Intent-driven | Intent-driven |
| **Amazon Bedrock** | Context window | STM | LTM | Episodic strategy | Semantic strategy |
| **Apple Intelligence** | Context window | — | Semantic index | On-device | Semantic index |
| **Karpathy Wiki** | Context window | — | Markdown wiki | Wiki articles | Topic clusters |

### 10.2 By Persistence Model

| Technology | Persistence | Cross-Session | Cross-Device | Multi-Agent |
|---|---|---|---|---|
| **OpenClaw** | Markdown + SQLite | Yes (files) | Manual sync | Limited |
| **Claude Code** | CLAUDE.md | Yes (auto-memory) | No | Subagent isolation |
| **Codex CLI** | Markdown files | Yes (Memories) | No | No |
| **Hermes** | SQLite + Markdown | Yes (built-in + provider) | Provider-dependent | Native DAG |
| **UI-TARS** | Model-internal | Limited | No | No |
| **Google** | Cloud | Yes | Yes | No |
| **Microsoft** | Cloud + local | Yes | Yes | Tenant-scoped |
| **Amazon** | Cloud | Yes | Yes | Identity-scoped |
| **Apple** | On-device | Yes | iCloud | No |
| **Karpathy Wiki** | Git/Markdown | Yes | Git sync | No |

### 10.3 By Privacy Model

| Technology | Data Location | Encryption at Rest | User Control | Auditability |
|---|---|---|---|---|
| **OpenClaw** | Local | No (OS-dependent) | Full | Limited |
| **Claude Code** | Local | No (OS-dependent) | Full | Limited |
| **Codex CLI** | Local + cloud (Memories) | Secret redaction | Partial (geo limits) | Limited |
| **Hermes** | Local + optional cloud | No (default) | Full (local) / Varies (provider) | Limited |
| **UI-TARS** | Cloud + device | Unknown | Limited | Unknown |
| **Google** | Cloud | Yes | Admin + user | Enterprise logs |
| **Microsoft** | Cloud + local | Yes | Tenant admin | Enterprise logs |
| **Amazon** | Cloud | Yes | IAM policies | CloudTrail |
| **Apple** | On-device + PCC | Yes (PCC attestation) | Full | Cryptographic |
| **Holographic** | Local SQLite | No | Full | File-level |
| **ByteRover** | Local markdown | No | Full | Git-level |
| **Honcho** | Cloud (default) | TLS in transit | Partial | Limited disclosure |

---

*End of Master Ledger*

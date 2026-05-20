# Numeric Claims Ledger

| claim_id | number | metric | source_id | direct_or_inferred | already_in_report | note |
|---|---|---|---|---|---|---|
| N001 | ~19,593 ms | Recall latency (OpenClaw, 300 events) | S027 | direct | no | Benchmark by Regolo; OpenClaw feeds full JSONL history into LLM context for recall |
| N002 | ~113 ms | Recall latency (Hermes, 300 events) | S027 | direct | no | Same benchmark; Hermes uses SQLite FTS5 query |
| N003 | 400-800 MB | OpenClaw Gateway idle RAM | S018 | direct | no | Core Node.js daemon baseline |
| N004 | 200-400 MB | Playwright browser instance RAM | S018 | direct | no | Per browser automation instance |
| N005 | <512 MB | Hermes Agent idle RAM | S020 | direct | no | Railway deployment figure |
| N006 | ~10 ms | Hermes FTS5 retrieval latency (10K docs) | S016 | direct | no | CrabTalk survey; scales to ~100K before needing dedicated vector DB |
| N007 | 50K chars | Tool result budget per tool (Claude Code) | S008 | direct | no | Per-tool cap before truncation/persistence |
| N008 | 200K chars | Tool result budget per message (Claude Code) | S008 | direct | no | Per-message cap |
| N009 | 13K tokens | Auto-compact threshold headroom (Claude Code) | S007 | direct | no | effectiveContextWindow - 13000 |
| N010 | 3 | Max consecutive autocompact failures before circuit breaker | S008 | direct | no | Prevents infinite retry loops |
| N011 | 32 KiB | AGENTS.md ceiling (Codex CLI) | S010 | direct | no | Silent truncation beyond this limit |
| N012 | 256 | Max recent rollouts considered for consolidation (Codex) | S010 | direct | no | Hard ceiling for memory consolidation |
| N013 | 30 days | Memory age-out threshold (Codex) | S010 | direct | no | Both rollouts and individual memories pruned |
| N014 | 6 hours | Default idle time before consolidation eligible (Codex) | S010 | direct | no | Active sessions never trigger consolidation |
| N015 | ~55,000 tokens | Claude Code tool definitions per request | S008 | direct | no | Community feature request mentions this as token bloat |
| N016 | 4000 tokens | OpenClaw memory flush soft threshold | S006 | direct | no | Pre-compaction flush triggers at this buffer |
| N017 | 2 MB | OpenClaw transcript file size threshold | S033 | direct | no | Secondary flush trigger |
| N018 | 700 chars | OpenClaw snippet max chars per result | S006 | direct | no | memory_search return limit |
| N019 | 8000 tokens | OpenClaw embedding batch max tokens | S006 | direct | no | API call batching limit |
| N020 | 4 | OpenClaw embedding index concurrency | S006 | direct | no | Parallel embedding requests |
| N021 | 400 tokens | OpenClaw chunk target size | S006 | direct | direct | Chunking parameter |
| N022 | 80 tokens | OpenClaw chunk overlap | S006 | direct | no | Chunking overlap parameter |
| N023 | 0.7 / 0.3 | Vector / text weight (OpenClaw hybrid search) | S005 | direct | no | Default hybrid scoring weights |
| N024 | 30 days | OpenClaw temporal decay half-life | S030 | direct | no | Newer memories weighted higher |
| N025 | 50000 | OpenClaw embedding cache max entries | S030 | direct | no | Cache size limit |
| N026 | 1500 ms | OpenClaw file watcher debounce | S005 | direct | no | Reindex delay after file changes |
| N027 | ~0.6 GB | Local GGUF embedding model size (OpenClaw) | S005 | direct | no | node-llama-cpp local embedding |
| N028 | 2200 chars | Hermes MEMORY.md character limit (~800 tokens) | S014 | direct | no | Configurable in config.yaml |
| N029 | 1375 chars | Hermes USER.md character limit (~500 tokens) | S014 | direct | no | Configurable in config.yaml |
| N030 | 91.4% | Hindsight LongMemEval score (Gemini-3) | S015 | direct | no | Highest tested provider score |
| N031 | 89.0% | Hindsight LongMemEval score (OSS-120B) | S015 | direct | no | Open-source model result |
| N032 | 83.6% | Hindsight LongMemEval score (OSS-20B) | S015 | direct | no | Smaller open-source model result |
| N033 | 67.6% | Mem0 LongMemEval-S score (GPT-4o) | S015 | direct | no | Note: variant benchmark, not directly comparable |
| N034 | 2 GB | Absolute minimum RAM (OpenClaw gateway) | S018 | direct | no | Hard floor; below this crashes |
| N035 | 4 GB | Recommended RAM (OpenClaw solo text) | S019 | direct | no | Sfailabs recommendation |
| N036 | 8-16 GB | Production RAM (OpenClaw multi-agent/browser) | S019 | direct | no | Production scenario spec |
| N037 | 16 GB | Air-gapped local LLM RAM (OpenClaw + 7-13B) | S019 | direct | no | Includes local model memory |
| N038 | 32 GB+ | Air-gapped local LLM RAM (OpenClaw + larger models) | S019 | direct | no | GPU recommended |
| N039 | 4 GB | Claude Code minimum RAM | S022 | direct | no | Anthropic official minimum |
| N040 | 16 GB | Claude Code daily-driver floor | S022 | direct | no | For local dev with builds/tests |
| N041 | 4 GB | Codex CLI minimum RAM | S023 | direct | no | DeployHQ guide |
| N042 | 8 GB | Codex CLI recommended RAM | S023 | direct | no | For large codebases |
| N043 | ~50 MB | Codex CLI package size | S023 | direct | no | npm package lightweight |
| N044 | 1.4s | Simple task latency (OpenClaw, Llama 3.1 70B) | S026 | direct | no | Median from reproducible benchmark |
| N045 | 1.9s | Simple task latency (Hermes, Llama 3.1 70B) | S026 | direct | no | Median from reproducible benchmark |
| N046 | 4.1s | Multi-step research latency (OpenClaw) | S026 | direct | no | 3 tools, cross-session memory |
| N047 | 5.3s | Multi-step research latency (Hermes) | S026 | direct | no | Same task, higher accuracy |
| N048 | 61% | Memory recall session 2 (OpenClaw) | S026 | direct | no | Accuracy drops without structured memory |
| N049 | 89% | Memory recall session 2 (Hermes) | S026 | direct | no | FTS5 + hybrid reasoning advantage |
| N050 | 4.2s | 10-step pipeline latency (Hermes) | S028 | direct | no | Business20Channel benchmark |
| N051 | 5.9s | 10-step pipeline latency (OpenClaw) | S028 | direct | no | Same benchmark |
| N052 | 98.2% | Multi-agent coordination success (Hermes, 4 agents) | S028 | direct | no | Native DAG advantage |
| N053 | 81.4% | Multi-agent coordination success (OpenClaw, 4 agents) | S028 | direct | no | Community patterns limitation |
| N054 | 213.41 KB | OpenClaw disk usage delta (300 events) | S027 | direct | no | Raw JSONL append growth |
| N055 | 0.00 KB | Hermes disk usage delta (300 events) | S027 | direct | no | SQLite WAL compaction |
| N056 | 82% | OpenClaw model routing cost reduction | Skywork slides | inferred | no | Marketing claim from slide deck; treat cautiously |
| N057 | 63% | OpenClaw average monthly cost savings (Codex OOTH) | Skywork slides | inferred | no | Marketing claim; treat cautiously |
| N058 | 22 | OpenClaw messaging channels | S035 | direct | no | Competitive comparison |
| N059 | 13 | Hermes messaging channels | S035 | direct | no | Competitive comparison |
| N060 | ~2-3 GB | OpenClaw install size | S018 | direct | no | Base installation |
| N061 | 1-3 GB/month | OpenClaw log growth (moderate activity) | S018 | direct | no | Session JSONL logs |
| N062 | 5.8 | Llama 3.1 70B tok/s (M1 Max 64GB) | S024 | direct | no | Apple Silicon local inference benchmark |
| N063 | 12.5 | Llama 3.1 70B tok/s (M4 Max 128GB) | S024 | direct | no | Fastest Apple Silicon for 70B |
| N064 | 4 ms | llama.cpp GPU embedding latency (OpenClaw local) | coolmanns repo | direct | no | nomic-embed-text-v2-moe 768d |
| N065 | 61 ms | Ollama nomic-embed-text latency | coolmanns repo | direct | no | Local CPU-based embedding |
| N066 | ~200 ms | OpenAI embedding API latency | coolmanns repo | direct | no | Cloud API roundtrip |
| N067 | 23B active (230B total) | UI-TARS-2 MoE LLM parameters | S041 | direct | no | 532M vision encoder + MoE with 23B active params |
| N068 | 96.7% | M3-Agent memory recall accuracy (claimed) | M3-Agent article | inferred | no | ByteDance M3-Agent claimed recall; source is promotional; treat cautiously |
| N069 | 61.6% | UI-TARS-1.5 ScreenSpotPro accuracy | S046 | direct | no | Outperforms Claude-3 (27.7%) and GPT-4o (41.2%) |
| N070 | <5 pixels | UI-TARS-1.5 UI element coordinate error | S046 | direct | no | 1120×1120 visual encoder precision |
| N071 | 38% | UI-TARS-1.5 error reduction in Minecraft (think-before-act) | S046 | direct | no | Compared to direct action predictions |
| N072 | 43% | UI-TARS-1.5 compute cost reduction vs GPT-4V | S046 | direct | no | $0.12/1K actions vs $0.21/1K actions |
| N073 | 2M tokens | Gemini 1.5 Pro max context window | S049 | direct | no | Equivalent to ~1.4M words or 2 hours video |
| N074 | ~15GB | KV cache memory for 1M tokens per user | S050 | direct | no | Production infrastructure figure; 2M would be ~30GB |
| N075 | 93% | Context parallelism efficiency on 128 H100s | S050 | direct | no | For 405B models at 1M token scale |
| N076 | 40% | "Lost in the middle" context degradation at scale | S050 | direct | no | Long-context retrieval accuracy drop |
| N077 | 200 lines | VS Code Copilot User memory auto-loaded lines | S053 | direct | no | First 200 lines injected at session start |
| N078 | 3 | Microsoft Copilot Memory scopes (User/Repository/Session) | S053 | direct | no | VS Code agent memory tool architecture |
| N079 | 128K tokens | GPT-4o model context window (Microsoft 365 Copilot) | S054 | direct | no | Input limit; 16,384 tokens output |
| N080 | ~250KB | Doubao phone upload packet size | S044 | direct | no | Every 3-5 seconds; likely compressed screenshot + context |
| N081 | ~1KB | Doubao phone action instruction return size | S044 | direct | no | Very small; contains click/swipe/text commands |
| N082 | 2 minutes | Gemini 1.5 Pro prefill latency for max context | S050 | direct | no | Processing 2M tokens takes 10-30s per prompt |
| N083 | 10M tokens | Llama 4 context window capacity | S060 | direct | no | Per MindStudio; massive context for agent frameworks |
| N084 | 75% | Amazon Nova cost/latency reduction vs other models | S055 | direct | no | AWS claim for Nova models via Bedrock |
| N085 | 90% | Amazon S3 Vectors cost reduction for vector storage | S055 | direct | no | AWS claim; first cloud storage with native vector support |
| N086 | ~100 tokens | OpenViking L0 (Abstract) size | S064 | direct | no | One-sentence summary for quick identification |
| N087 | ~2,000 tokens | OpenViking L1 (Overview) size | S064 | direct | no | Core information for planning and decision-making |
| N088 | 6.3K+ | OpenViking GitHub stars | S063 | direct | no | As of May 2026 |
| N089 | ~1,200 lines | OpenViking memory_extractor.py | S066 | direct | no | Core memory extraction logic |
| N090 | ~395 lines | OpenViking memory_deduplicator.py | S066 | direct | no | Deduplication decision logic |
| N091 | ~447 lines | OpenViking compressor.py | S066 | direct | no | Session compression logic |
| N092 | 1.2M+ | Karpathy LLM Wiki post views | S068 | direct | no | X post April 3 2026 |
| N093 | ~100 articles | Karpathy research wiki size | S068 | direct | no | On a single research topic |
| N094 | ~400,000 words | Karpathy research wiki word count | S068 | direct | no | Longer than most PhD dissertations |
| N095 | 10–15 | Wiki pages touched per ingested source | S069 | direct | no | During LLM compilation; connections chunk-based RAG would miss |
| N096 | ~200,000 tokens | Claude 3.5 Sonnet context window | S070 | direct | no | Sufficient for most personal wikis up to few hundred notes |

| N097 | 1–3 | Honcho dialectic depth passes | S074 | direct | no | Configurable multi-pass reasoning |
| N098 | 1 | Honcho contextCadence default (refresh interval in turns) | S074 | direct | no | Base layer refresh frequency |
| N099 | 2 | Honcho dialecticCadence default (reasoning interval in turns) | S074 | direct | no | Dialectic LLM call frequency |
| N100 | 92.5% | Mem0 LoCoMo score (April 2026 algorithm) | S078 | direct | no | +20 points over previous algorithm |
| N101 | 94.4% | Mem0 LongMemEval score (April 2026 algorithm) | S078 | direct | no | +27 points over previous |
| N102 | 64.1% | Mem0 BEAM 1M score (April 2026 algorithm) | S078 | direct | no | Production-scale 1M token evaluation |
| N103 | 48.6% | Mem0 BEAM 10M score (April 2026 algorithm) | S078 | direct | no | 10M token scale evaluation |
| N104 | ~6,956 | Mem0 average tokens per retrieval call (LoCoMo) | S078 | direct | no | vs ~26,000 for full-context baseline |
| N105 | 0.200s | Mem0 p95 search latency (2025 paper) | S079 | direct | no | 91% latency reduction vs full-context |
| N106 | ~1,764 | Mem0 tokens per conversation (2025 paper) | S079 | direct | no | vs 26,031 full-context; 90%+ token savings |
| N107 | 52.8K | Mem0 GitHub stars | S095 | direct | no | Largest community in agent memory space |
| N108 | $24M | Mem0 Series A funding | S095 | direct | no | Significant VC backing |
| N109 | 14M | Mem0 package downloads | S078 | direct | no | Widely adopted memory library |
| N110 | 91.4% | Hindsight LongMemEval (Gemini-3) | S081 | direct | no | Highest tested provider score on LongMemEval |
| N111 | 89.0% | Hindsight LongMemEval (OSS-120B) | S081 | direct | no | Open-source backbone result |
| N112 | 83.6% | Hindsight LongMemEval (OSS-20B) | S081 | direct | no | Consumer GPU deployable result |
| N113 | 89.61% | Hindsight LoCoMo (OSS-120B) | S081 | direct | no | vs 75.78% strongest prior open system |
| N114 | 96.1% | ByteRover LoCoMo overall accuracy | S082 | direct | no | Highest on LoCoMo; +6.2pp over HonCho |
| N115 | 92.8% | ByteRover LongMemEval-S overall | S082 | direct | no | Below Chronos-High 95.6% (Claude Opus) |
| N116 | 97.8% | ByteRover temporal queries (LoCoMo) | S082 | direct | no | Structured timestamp metadata advantage |
| N117 | +9.3pp | ByteRover multi-hop gain over HonCho (LoCoMo) | S082 | direct | no | Context Tree explicit inter-entry relations |
| N118 | sub-ms | Holographic retrieval latency | S084 | direct | no | HRR algebraic recall on SQLite |
| N119 | 0 | Holographic external pip dependencies | S084 | direct | no | Pure SQLite, no network calls |
| N120 | 50–90% | RetainDB delta compression token savings | S086 | direct | no | 15,000→1,500 tokens example |
| N121 | $20/mo | RetainDB Pro tier pricing | S088 | direct | no | Scale $99/mo, Max $299/mo |
| N122 | <50ms | RetainDB memory retrieval latency | S086 | direct | no | Lightning-fast claim |
| N123 | 99.9% | RetainDB uptime SLA | S086 | direct | no | Enterprise-grade reliability claim |
| N124 | 85.2% | Supermemory LongMemEval score | S095 | direct | no | vs Mem0 49% on same benchmark |
| N125 | 85.4% | Supermemory LongMemEval-S score | S096 | direct | no | Standard benchmark variant |
| N126 | 92.3% | Supermemory single-session recall | S096 | direct | no | User recall accuracy |
| N127 | 76.7% | Supermemory multi-session accuracy | S096 | direct | no | vs 57.9% competing systems |
| N128 | sub-300ms | Supermemory recall latency | S094 | direct | no | vs 4s Zep, 7-8s Mem0 |
| N129 | $2.6M | Supermemory seed funding | S095 | direct | no | Google/Cloudflare exec backers |
| N130 | 21.7K | Supermemory GitHub stars | S095 | direct | no | Consumer app frontend included |
| N131 | 98% | Supermemory API call reduction with caching | S098 | direct | no | From ~1,584/day to ~33/day |
| N132 | 5 | Honcho tools exposed in Hermes | S074 | direct | no | honcho_profile, search, context, reasoning, conclude |
| N133 | 2 | Holographic tools exposed in Hermes | S085 | direct | no | fact_store (9 actions), fact_feedback |
| N134 | 5 | OpenViking tools exposed in Hermes | S099 | direct | no | Most capability surface area tied with RetainDB |
| N135 | 5 | RetainDB tools exposed in Hermes | S099 | direct | no | retaindb_profile, search, context, remember, forget |
| N136 | 3 | ByteRover tools exposed in Hermes | S092 | direct | no | brv_query, brv_curate, brv_status |
| N137 | 4 | Supermemory tools exposed in Hermes | S099 | direct | no | Context fencing, session graph ingest, multi-container |
| N138 | 3 | Mem0 tools exposed in Hermes | S099 | direct | no | mem0_search, mem0_add, mem0_get |
| N139 | 3 | Hindsight tools exposed in Hermes | S099 | direct | no | hindsight_retain, recall, reflect |
| N140 | 7 | OpenClaw embedding providers | S100 | direct | no | OpenAI, Gemini, Voyage, Mistral, DeepInfra, Ollama, Local GGUF |
| N141 | 0.6GB | OpenClaw local GGUF embedding model size | S100 | direct | no | node-llama-cpp local embedding |
| N142 | 5 | ByteRover atomic curate operations | S090 | direct | no | UPSERT, MERGE, DELETE, LINK, UNLINK |
| N143 | 5 | ByteRover retrieval tiers | S090 | direct | no | MiniSearch→fuzzy→semantic→agentic→direct response |
| N144 | 0.995^Δt | ByteRover importance decay (daily) | S090 | direct | no | Exponential decay factor |
| N145 | e^(-Δt/30) | ByteRover recency decay | S090 | direct | no | 30-day characteristic time |
| N146 | 7 | RetainDB memory types | S086 | direct | no | Factual, Preference, Event, Relationship, Opinion, Goal, Instruction |
| N147 | 15+ | RetainDB connectors | S086 | direct | no | GitHub, Notion, Slack, Discord, Confluence, PostgreSQL, MongoDB |
| N148 | 15+ | RetainDB MCP tools | S086 | direct | no | Claude Desktop integration |
| N149 | 2M | RetainDB Max tier queries/month | S088 | direct | no | $299/mo plan limit |
| N150 | 0% | RetainDB claimed hallucination rate on docs | S089 | direct | no | From Gamgee comparison; treat cautiously |
| N151 | 88% | RetainDB preference recall (claimed SOTA) | S089 | direct | no | From Gamgee comparison; treat cautiously |
| N152 | 21 | Mem0 supported frameworks | S078 | direct | no | Broad framework ecosystem |
| N153 | 20 | Mem0 supported vector stores | S078 | direct | no | Flexible storage backends |

| N154 | 26–44% | Compaction E2E time increase (Slipstream) | S109 | direct | no | Synchronous compaction on critical path |
| N155 | 5–20k tokens | Anthropic recommended compaction trigger | S109 | direct | no | Aggressive pre-empty compaction |
| N156 | 30–70% | Refusal rate shift at 100K+ tokens | S109 | direct | no | Safety mechanisms unstable at long context |
| N157 | 1B | AtlasKV billion-scale KG triples | S119 | direct | no | Parametric knowledge integration scale |
| N158 | <20GB | AtlasKV VRAM requirement for 1B triples | S119 | direct | no | Sub-linear memory complexity |
| N159 | 3 | HyperMem memory levels (Topic→Episode→Fact) | S104 | direct | no | Hypergraph hierarchy depth |
| N160 | 4 | Hindsight logical networks | S081 | direct | no | World facts, experiences, entities, beliefs |
| N161 | 5 | Mem0 mechanism families (Du survey) | S101 | direct | no | Context-resident compression, RAG, reflective, hierarchical, policy-learned |
| N162 | 3 | Du survey taxonomy dimensions | S101 | direct | no | Temporal scope, representational substrate, control policy |
| N163 | 5 | Du survey open challenges | S101 | direct | no | Continual consolidation, causal retrieval, trustworthy reflection, learned forgetting, multimodal embodied |
| N164 | 10M | LLaMA 4 context window capacity | S060 | direct | no | Largest open-weight context window |
| N165 | 2M | Gemini 1.5 Pro max context | S049 | direct | no | Production cloud model max |

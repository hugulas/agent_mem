# Mem0 vs Hindsight: External Memory Providers

> Two dedicated memory-as-a-service providers with different architectural approaches.

## At a Glance

| Dimension | Mem0 | Hindsight |
|---|---|---|
| **Core abstraction** | ADD/UPDATE/DELETE/NOOP memory operations | 4-network memory (facts/experiences/entities/beliefs) |
| **Operation mode** | API-first, cloud-hosted | Self-hosted or cloud |
| **Integration** | 8+ framework integrations (OpenClaw, Hermes, etc.) | Hermes native provider + standalone |
| **Benchmark LoCoMo** | 67.13% (paper) / 91.6% (blog, 2026-04) | Not independently benchmarked |
| **Benchmark LongMemEval** | 94.4% (blog) / 94.8% (2026-04) | 91.4% (Gemini-3) |
| **Latency claim** | ~91% reduction vs baseline | Not disclosed |
| **Pricing** | Free tier → $29/mo → Enterprise | Not publicly disclosed |
| **License** | Proprietary (API) | Not specified |

## Architecture

### Mem0
- **Extraction**: ADD-only or full CRUD on semantic facts, preferences, summaries, episodic events
- **Consolidation**: Async merge after 6h idle; 2 models (extract + merge); 256 rollout cap; 30-day age-out
- **Retrieval**: Multi-signal (entity linking, temporal reasoning, semantic search)
- **Storage**: Cloud-hosted; 32 KiB AGENTS.md ceiling for static layer

### Hindsight
- **4 networks**:
  - Facts network — durable semantic facts
  - Experiences network — episodic event sequences
  - Entities network — people, places, objects
  - Beliefs network — inferred user preferences and intents
- **3 operations**: retain, recall, reflect
- **Reasoning**: Multi-pass depth with cold/warm prompt switching

## Key Differences

1. **Memory granularity**: Mem0 operates at the **fact/statement** level (discrete memory units); Hindsight operates at the **network/relationship** level (interconnected graph of memories).

2. **User control**: Mem0 exposes explicit ADD/UPDATE/DELETE operations; Hindsight's reflect operation is more autonomous and less directly user-controllable.

3. **Benchmark transparency**: Mem0 publishes detailed benchmarks with versioned results (showing improvement 67% → 91.6% → 94.8%); Hindsight's 91.4% LongMemEval claim is less thoroughly documented.

4. **Deployment model**: Mem0 is primarily cloud-API; Hindsight offers tighter self-hosting integration (especially with Hermes).

## Critical Questions
- Mem0's blog benchmarks (94.8% LongMemEval) vs independent evaluations show significant variance — what explains the gap?
- Hindsight's 4-network architecture is elegant but computationally expensive; what is the inference cost per memory operation?

## Related
- [[Mem0]]
- [[Hindsight]]
- [[memory-benchmarks]]
- [S078](sources/S078.md), [S079](sources/S079.md), [S080](sources/S080.md), [S081](sources/S081.md), [S095](sources/S095.md)

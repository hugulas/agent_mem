# Academic Memory Architectures: ByteRover vs LoCoMo vs TiMem vs AtlasKV

> Comparison of four cutting-edge academic approaches to agent memory, spanning RL-based management, temporal hierarchies, and parametric knowledge graphs.

## At a Glance

| Architecture | ByteRover | LoCoMo | TiMem | AtlasKV |
|---|---|---|---|---|
| **Core innovation** | RL-trained memory operations (ADD/UPDATE/DELETE/NOOP) | Training-free KV cache compression for GUI agents | Temporal Memory Tree (5-level hierarchy) | Parametric billion-scale KG in <20GB VRAM |
| **Domain** | General conversational agents | GUI agents (visual + text) | Long-horizon conversation | Knowledge-intensive tasks |
| **Benchmark LoCoMo** | Not evaluated | 2.45× decoding acceleration at 10–20% cache budget | **75.30%** | Not evaluated |
| **Benchmark LongMemEval** | Not evaluated | Not evaluated | **76.88%** (LongMemEval-S) | Not evaluated |
| **Key metric** | 152 training pairs for RL | 2.45× speedup | 52.20% recall length reduction | No external retriever needed |
| **Memory mechanism** | RL policy for memory operations | KV cache compression (ST-Lite) | Temporal-hierarchical consolidation | Parametric KG integration |

## ByteRover (S082, S090, S091)

### Core mechanism
- RL-trained memory management policy with 152 training pairs
- Operations: ADD, UPDATE, DELETE, NOOP
- Multi-level rewards for non-linear reasoning
- Context Tree + Agentic Search + `brv pull` CLI

### Strengths
- First to apply RL to discrete memory operations
- CLI tool integration for developer workflows

### Limitations
- No published benchmark on standard agent memory evaluations (LoCoMo, LongMemEval)
- Small training set (152 pairs) may limit generalization

## LoCoMo / ST-Lite (S082, S117)

### Core mechanism
- **Training-free KV cache compression** for GUI agents
- Operates at 10–20% of original cache budget
- Achieves 2.45× decoding acceleration

### Strengths
- No fine-tuning required; plug-and-play for any transformer
- Specifically optimized for GUI agent workloads with visual + text inputs

### Limitations
- Compression may lose nuanced semantic information at very low budgets
- GUI-agent-specific; not evaluated on general conversational memory

## TiMem (S120)

### Core mechanism
- **Temporal Memory Tree** with five-level hierarchy
- Temporal-hierarchical consolidation
- Dynamic tree pruning based on recency and relevance

### Benchmarks
- **LoCoMo: 75.30%** (SOTA)
- **LongMemEval-S: 76.88%**
- **52.20% recall length reduction**

### Strengths
- Best-in-class benchmark performance on both LoCoMo and LongMemEval
- Explicit temporal modeling captures conversation dynamics better than flat memory stores

### Limitations
- Tree maintenance overhead not quantified
- Five-level hierarchy may be over-engineered for short conversations

## AtlasKV (S119)

### Core mechanism
- **Parametric billion-scale knowledge graph** integrated directly into model parameters
- Runs in <20GB VRAM without external retriever
- No separate retrieval pipeline needed

### Strengths
- Eliminates retrieval latency entirely (everything in parameters)
- Scales to billion-scale KG relationships

### Limitations
- Not evaluated on standard agent memory benchmarks (LoCoMo, LongMemEval)
- Parametric approach limits updatability — new facts require retraining or adapter layers
- 20GB VRAM is still high for edge deployment

## Comparative Assessment

| Criterion | Winner | Rationale |
|---|---|---|
| **Best benchmark scores** | TiMem | SOTA on LoCoMo + LongMemEval-S |
| **Most novel mechanism** | ByteRover | First RL-based memory operations |
| **Most efficient inference** | LoCoMo/ST-Lite | 2.45× speedup, training-free |
| **Largest knowledge scale** | AtlasKV | Billion-scale KG parametric |
| **Most practical deployment** | LoCoMo/ST-Lite | No training, minimal overhead |

## Research Gaps
- No direct head-to-head comparison exists across all four architectures on identical benchmarks
- RL-based memory (ByteRover) vs temporal hierarchy (TiMem) represent fundamentally different philosophies — which scales better to 1000+ turn conversations?
- Parametric KG (AtlasKV) vs retrieval-augmented memory: trade-off between latency and updatability not systematically studied

## Related
- [[ByteRover]]
- [[TiMem]]
- [[AtlasKV]]
- [[memory-benchmarks]]
- [S082](sources/S082.md), [S090](sources/S090.md), [S091](sources/S091.md), [S117](sources/S117.md), [S119](sources/S119.md), [S120](sources/S120.md)

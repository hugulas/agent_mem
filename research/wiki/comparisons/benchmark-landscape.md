# Benchmark Landscape: LoCoMo vs LongMemEval vs BEAM

> The three dominant benchmarks for evaluating agent long-term memory, their methodologies, and what they actually measure.

## At a Glance

| Dimension | LoCoMo | LongMemEval | BEAM |
|---|---|---|---|
| **Full name** | Long Context Model Benchmark | Long-term Memory Evaluation | Benchmark for Evaluating Agent Memory |
| **Focus** | Multi-session conversational consistency | Chat assistant memory over extended interaction | General agent memory capability |
| **Interaction length** | 35 sessions, ~300K tokens total | 100+ turns over days/weeks | Configurable (1M/10M token variants) |
| **Task type** | Question answering with cross-session dependencies | Realistic chat scenarios (travel planning, project tracking) | Synthetic + realistic mixed |
| **Metric** | Accuracy (%) | Accuracy (%) | Accuracy + latency + token efficiency |
| **Leader (claimed)** | TiMem 75.30% | TiMem 76.88% (LongMemEval-S) | Mem0 94.4% (BEAM-1M) |

## LoCoMo

### Design philosophy
- Simulates **35 sessions** between a user and an agent over an extended period
- Each session builds on prior context; agent must recall facts from 10+ sessions ago
- ~300K tokens of total conversation history

### What it measures well
- **Cross-session fact retention**: Can the agent remember a preference mentioned in session 3 when asked in session 28?
- **Consistency**: Does the agent contradict itself across sessions?

### Limitations
- **Synthetic scenarios**: Pre-defined conversation scripts, not real user behavior
- **No temporal dynamics**: All sessions are equally "old"; no decay or reinforcement modeling
- **Limited modality**: Text-only

### Reported scores
| System | Score |
|---|---|
| TiMem | **75.30%** |
| ByteRover | 96.1% (claimed, unverified on LoCoMo) |
| Mem0 (blog) | 91.6% |
| Mem0 (paper) | 67.13% |

## LongMemEval

### Design philosophy
- Evaluates chat assistants on **realistic, multi-day interactions**
- Tasks include travel planning, project management, preference learning
- Measures both recall accuracy and conversational naturalness

### What it measures well
- **Realistic memory use**: Agents must naturally incorporate remembered facts into responses
- **Temporal reasoning**: Understanding "before", "after", "since our last conversation"

### Limitations
- **Subjective evaluation**: Human annotators judge naturalness; inter-annotator consistency varies
- **Limited scale**: 100+ turns is long but not extreme (no million-token tests)

### Reported scores
| System | Score |
|---|---|
| Mem0 (blog) | **94.4%** / 94.8% |
| Hindsight | 91.4% (Gemini-3 backend) |
| TiMem | **76.88%** (LongMemEval-S) |
| Mem0 (independent) | 49% (S095) |

## BEAM

### Design philosophy
- Tests memory at **extreme scale**: 1M and 10M token contexts
- Mix of synthetic needle-in-haystack and realistic retrieval tasks
- Measures accuracy, latency, and token efficiency simultaneously

### What it measures well
- **Scale tolerance**: Can the memory system function at million-token scale?
- **Efficiency**: Tokens retrieved vs. tokens needed (cost proxy)

### Limitations
- **Synthetic-heavy**: Many tasks are artificially constructed
- **Not agent-specific**: General retrieval benchmark, not conversational memory

### Reported scores
| System | BEAM-1M | BEAM-10M |
|---|---|---|
| Mem0 | 94.4% (claimed) | Not disclosed |

## Critical Issue: Benchmark Discrepancies

The memory provider space suffers from **severe benchmark inconsistency**:

| Provider | Claimed | Independent | Gap |
|---|---|---|---|
| Mem0 LongMemEval | 94.4% | 49% | **45.4 pp** |
| Mem0 LoCoMo | 91.6% | 67.13% | **24.5 pp** |

Possible explanations:
1. **Different model backends**: GPT-4o vs. local models vs. fine-tuned variants
2. **Different evaluation protocols**: Strict vs. lenient scoring
3. ** cherry-picked results**: Best run reported, not average
4. **Version differences**: Blog claims may reflect newer algorithm versions not in published paper

## Recommendations

| Goal | Best Benchmark |
|---|---|
| **Realistic chat memory** | LongMemEval |
| **Cross-session consistency** | LoCoMo |
| **Extreme scale** | BEAM |
| **Fair comparison** | Run all three on identical model backends |

## Related
- [[memory-benchmarks]]
- [[Mem0]]
- [[Hindsight]]
- [[TiMem]]
- [[ByteRover]]
- [S078](sources/S078.md), [S079](sources/S079.md), [S080](sources/S080.md), [S081](sources/S081.md), [S095](sources/S095.md), [S120](sources/S120.md), [S136](sources/S136.md), [S137](sources/S137.md)

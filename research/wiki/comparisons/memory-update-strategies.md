# Memory Update Strategies: When and How Agents Remember

> Different frameworks employ fundamentally different strategies for deciding what to remember, when to update, and what to forget.

## At a Glance

| System | Update Trigger | Merge Strategy | Forgetting Mechanism |
|---|---|---|---|
| **OpenClaw** | Agent self-initiated write + heartbeat sweep | Manual distillation (daily → long-term) | Bootstrap budget truncation |
| **Claude Code** | Before every model call (compaction pipeline) | Progressive summarization | Context window eviction |
| **Codex CLI** | 6h idle post-session | LLM extract + merge models | 30-day age-out, 256-rollout cap |
| **Mem0** | Real-time (ADD/UPDATE/DELETE ops) | Async consolidation (2 models) | Age-out + relevance decay |
| **Hindsight** | After each interaction (retain/recall/reflect) | Network graph update | Belief revision + conflict resolution |
| **Honcho** | Per-turn persistence + dialectic depth trigger | Cold/warm prompt synthesis | Context cadence refresh |

## Strategy Taxonomy

### 1. Agent-initiated writing (OpenClaw)
- **Trigger**: Agent decides to write to MEMORY.md based on importance judgment
- **Mechanism**: `memory_write` tool call during conversation + heartbeat automated sweep
- **Strength**: Human-like selective memory; only important things persist
- **Weakness**: Agent may forget to write; inconsistent memory quality

### 2. Compaction-driven summarization (Claude Code)
- **Trigger**: Context window pressure (13K token threshold)
- **Mechanism**: 5-layer pipeline progressively summarizes older context
- **Strength**: Automatic, no agent cooperation needed
- **Weakness**: Lossy compression; nuance degrades with each compaction cycle

### 3. Post-session consolidation (Codex CLI)
- **Trigger**: 6 hours of idle time after session ends
- **Mechanism**: Extract model identifies salient facts → Merge model integrates into existing Memories
- **Strength**: Batch processing is efficient; cool-off period reduces noise
- **Weakness**: 6h delay means crash before consolidation = memory loss; no real-time updates

### 4. Operation-centric CRUD (Mem0)
- **Trigger**: Real-time during conversation (ADD/UPDATE/DELETE/NOOP)
- **Mechanism**: Each operation is explicit and atomic; async consolidation batches merges
- **Strength**: Fine-grained control; operations are auditable
- **Weakness**: CRUD overhead on every turn; merge conflicts possible

### 5. Reflective graph update (Hindsight)
- **Trigger**: After each interaction (retain phase)
- **Mechanism**: Facts/experiences/entities/beliefs networks updated incrementally; reflect phase resolves conflicts
- **Strength**: Rich relational structure; belief revision handles contradictions
- **Weakness**: Computationally expensive; graph maintenance overhead

### 6. Dialectic synthesis (Honcho)
- **Trigger**: Per-turn persistence + configurable depth cadence
- **Mechanism**: Base context (profile) refreshed on schedule + dialectic Q&A generates deep insights
- **Strength**: User modeling separate from content memory; multi-agent aware
- **Weakness**: Dialectic rounds add latency; cold/warm prompt switching complexity

## Forgetting Mechanisms

| System | How it forgets | Is it really gone? |
|---|---|---|
| **OpenClaw** | Bootstrap budget truncates injected copy | ❌ File on disk remains intact |
| **Claude Code** | Older messages summarized and discarded | ✅ Original detail lost |
| **Codex CLI** | 30-day age-out + 256-rollout cap | ✅ Memory entry deleted |
| **Mem0** | Age-out + relevance scoring | ✅ Entry removed from vector store |
| **Hindsight** | Belief revision overrides old beliefs | ⚠️ Old beliefs may persist in network |
| **Honcho** | Context cadence refresh replaces old context | ⚠️ Prior context archived, not deleted |

## Comparative Assessment

| Goal | Best Strategy |
|---|---|
| **Real-time accuracy** | Mem0 (operation-centric) |
| **Long-term consistency** | Hindsight (graph with belief revision) |
| **Token efficiency** | Claude Code (compaction) |
| **Crash resilience** | OpenClaw (files on disk) |
| **User modeling depth** | Honcho (dialectic) |
| **Simplicity** | Codex CLI (post-session batch) |
| **Auditability** | Mem0 (explicit CRUD log) |

## Open Research Questions

1. **Optimal update frequency**: Real-time (Mem0) vs. batch (Codex CLI) — what is the latency/quality trade-off sweet spot?
2. **Selective vs. comprehensive remembering**: OpenClaw's agent-initiated approach mimics human selective memory but is unreliable. Can RL train better selectivity?
3. **Forgetting as a feature**: Most systems treat forgetting as a bug (data loss). Should agents proactively forget irrelevant details to improve retrieval precision?
4. **Multi-agent memory coherence**: When multiple agents share a memory store (Honcho), how do we prevent conflicting updates without central locking?

## Related
- [[OpenClaw]]
- [[Claude Code]]
- [[Codex CLI]]
- [[Mem0]]
- [[Hindsight]]
- [[Honcho]]
- [S001](sources/S001.md), [S007](sources/S007.md), [S010](sources/S010.md), [S078](sources/S078.md), [S079](sources/S079.md), [S081](sources/S081.md), [S074](sources/S074.md)

# UI-TARS vs OpenViking: ByteDance Memory Architectures

> Two distinct memory approaches from ByteDance: a native GUI agent model vs a filesystem-inspired hierarchical context system.

## At a Glance

| Dimension | UI-TARS | OpenViking |
|---|---|---|
| **Type** | Native GUI agent model | Hierarchical context management system |
| **Domain** | Visual GUI automation (desktop, mobile, web) | General agent context/memory management |
| **Memory model** | Hierarchical memory state M_t = (W_t, E_t) | Filesystem metaphor L0/L1/L2 tiered loading |
| **Working memory W_t** | Recent steps / actions | L0: ~100 tokens (minimal context) |
| **Episodic memory E_t** | Semantically compressed summaries | L1: ~2K tokens (summarized context) |
| **Architecture** | 532M vision encoder + 23B active (230B total) MoE | REST API + Python SDK + CLI |
| **Scale** | ScreenSpotPro 61.6% | 50 runbooks: RAG 50K tokens → OpenViking ~11K tokens |

## UI-TARS: Visual Agent Memory

### Hierarchical memory state
- **W_t (Working Memory)**: Stores recent steps and observations from the current task
- **E_t (Episodic Memory)**: Semantically compressed summaries of past interactions, enabling cross-session recall
- **Think-before-act**: System 2 reasoning module reduces errors by 38%

### Key innovations
- **Native agent model**: Perception + reasoning + memory + action integrated into single vision-language model
- **Self-evolving training**: Continuous learning from environment feedback
- **Multimodal grounding**: 1120×1120 visual encoder with <5 pixel coordinate error

### Memory limitations
- Memory is **task-bound**: W_t/E_t primarily serve the current GUI task, not open-ended conversation
- No evidence of long-term memory across **different** conversations (per MIT AI Agent Index)
- Optimized for visual state tracking, not semantic knowledge accumulation

## OpenViking: Hierarchical Context System

### Filesystem metaphor
- **L0**: ~100 tokens — minimal working context, always loaded
- **L1**: ~2K tokens — summarized context, loaded on demand
- **L2**: Full document — complete source material, loaded only when referenced

### Retrieval as navigation
- **viking://** URI scheme: `viking://user/{space}/memories/`, `viking://agent/{space}/memories/`
- **Directory recursive retrieval**: Traverse context like a filesystem
- **Visualized retrieval trajectory**: Debuggable context assembly path

### Token efficiency
- 50 runbooks example: RAG approach = 50K tokens; OpenViking = ~5K (L0) + ~6K (L1) + one L2
- **~80% token reduction** vs naive RAG

## Comparative Assessment

| Criterion | UI-TARS | OpenViking |
|---|---|---|
| **Primary use case** | GUI automation | General agent context management |
| **Memory scope** | Single-task visual + textual | Multi-turn conversation + documents |
| **Cross-session persistence** | Limited (E_t compresses within task) | Strong (filesystem-based persistence) |
| **Modality** | Visual-heavy (screenshots) | Text/document-heavy |
| **Integration depth** | End-to-end model | Framework-agnostic API |
| **Token efficiency** | Moderate (MoE helps) | Excellent (L0/L1/L2 tiers) |
| **Observability** | Limited (black-box model) | Excellent (retrieval trajectory visualization) |

## Synergy Potential

UI-TARS and OpenViking are **complementary**, not competitive:
- UI-TARS could use OpenViking as its **context management backend**, replacing simple W_t/E_t with L0/L1/L2 hierarchies
- OpenViking could add **visual context layers** (screenshot embeddings as L2 assets) for GUI agent support
- Both share ByteDance ecosystem; potential for unified "Doubao agent stack"

## Related
- [[UI-TARS]]
- [[OpenViking]]
- [[ByteRover]]
- [S041](sources/S041.md), [S042](sources/S042.md), [S063](sources/S063.md), [S064](sources/S064.md), [S065](sources/S065.md)

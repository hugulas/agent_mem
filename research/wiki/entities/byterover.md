# ByteRover

> Agent memory system or framework

## Core Claims
- - Agent-native memory architecture inverts the traditional pipeline: the same LLM that reasons also curates, structures, and retrieves knowledge, eliminating semantic drift caused by external-service ...
- - Same as S082: Agent-native memory architecture where the reasoning LLM also curates, structures, and retrieves knowledge, eliminating semantic drift from external-service memory pipelines.
- - ByteRover CLI 0.3.1 (beta) introduces Context Tree and Agentic Search, replacing flat vector-DB organization with a hierarchical, agent-driven retrieval system that dramatically improves memory retr...

## Mechanism
- - **Hierarchical Context Tree**: Domain → Topic → Subtopic → Entry, stored as human-readable Markdown files on the local filesystem.
- **Adaptive Knowledge Lifecycle (AKL)**: Each entry carries import...
- - Same as S082: Hierarchical Context Tree (Domain → Topic → Subtopic → Entry), Adaptive Knowledge Lifecycle (AKL), 5-tier progressive retrieval, zero external infrastructure.
- - **Context Tree**: Hierarchical memory structure — Domains (high-level categories) → Topics (specific subjects) → Context Files (Markdown with actual knowledge).
- **Agentic Search**: Replaces vector...

## Sources
- [S082](sources/S082.md)
- [S090](sources/S090.md)
- [S091](sources/S091.md)
- [S092](sources/S092.md)

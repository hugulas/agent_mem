# OpenViking

> Agent memory system or framework

## Core Claims
- - Agent memory should be managed through a filesystem paradigm rather than fragmented vector databases, enabling unified organization of memories, resources, and skills with tiered, on-demand context ...
- - OpenViking's tiered context loading (L0/L1/L2) achieves substantial token savings compared to flat RAG when deployed in production environments like OpenShift AI.
- - OpenViking's memory system is built on a structured URI namespace (`viking://user/{space}/memories/`, `viking://agent/{space}/memories/`) with VikingDB vector indexing, automatic compression, and a ...

## Mechanism
- - **Filesystem Paradigm (viking://)**: Maps memories, resources, and skills into a virtual hierarchical filesystem with directories like `user/`, `agent/`, and `resources/`.
- **Tiered Context Loading...
- - **Deployment Target**: OpenShift AI with REST API, Python SDK, and CLI interfaces.
- **Tiered Loading**: L0 (~100 tokens), L1 (~2K tokens), L2 (full document) loaded on demand.
- **Token Savings Exa...
- - **URI Structure**: `viking://user/{space}/memories/` and `viking://agent/{space}/memories/` for namespaced memory organization.
- **Vector Index**: VikingDB serves as the vector index backend.
- **M...

## Sources
- [S063](sources/S063.md)
- [S064](sources/S064.md)
- [S066](sources/S066.md)
- [S067](sources/S067.md)

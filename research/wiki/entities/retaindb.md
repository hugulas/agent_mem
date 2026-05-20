# RetainDB

> Agent memory system or framework

## Core Claims
- - RetainDB is a production-ready "memory + context brain" for AI agents, combining hybrid search, 7 typed memory systems, delta compression, and knowledge graphs into a single managed platform.
- - RetainDB is a self-hostable, open-source memory layer for AI agents that provides persistent, structured memory with typed relationships, temporal validity, and version chains.
- - RetainDB offers transparent, tiered pricing from free to enterprise, positioning itself as accessible for prototyping through high-volume production workloads.

## Mechanism
- - **Hybrid retrieval**: Vector + BM25 + reranking pipeline.
- **7 memory types**: Factual, preference, event, relationship, opinion, goal, instruction — each with temporal reasoning and version chains...
- - **Deployment**: Docker Compose or Node.js + PostgreSQL + pgvector; single-tenant by default.
- **Memory graph**: Relations typed as `updates`, `contradicts`, `supports`, `derives`.
- **Temporal vali...
- - **Free tier**: 5,000 queries/month, 1 project, 1 API key, MCP server access, community support.
- **Pro ($20/mo)**: 100,000 queries/month, 5 projects, 10 API keys, 5 team seats, SDK + MCP + Memory R...

## Sources
- [S086](sources/S086.md)
- [S087](sources/S087.md)
- [S088](sources/S088.md)
- [S089](sources/S089.md)

# Mem0

> Agent memory system or framework

## Core Claims
- Codex CLI implements a **two-layer memory model**: AGENTS.md as the static, user-maintained instruction layer (cross-tool convention under Linux Foundation's Agentic AI Foundation), and Memories as th...
- - In 2026, AI agent memory is a first-class production engineering discipline with standardized benchmarks (LoCoMo, LongMemEval, BEAM), measurable performance gaps between approaches, and a growing op...
- - Mem0 is a scalable memory-centric architecture that dynamically extracts, consolidates, and retrieves salient information from conversations, achieving substantial accuracy and efficiency gains over...

## Mechanism
- - **Layer 1 — AGENTS.md**: Cross-tool instruction file convention (Codex, Cursor, Aider, Jules). Layered discovery: global ~/.codex/AGENTS.md → project walk (root to cwd) → AGENTS.override.md preceden...
- - **Three standard benchmarks**:
  - **LoCoMo**: 1,540 questions testing single-hop, multi-hop, open-domain, and temporal memory recall across multi-session data.
  - **LongMemEval**: 500 questions ac...
- - **Core operations**: ADD, UPDATE, DELETE, NOOP — structured memory management operations rather than simple append-only logging.
- **Graph-based variant**: Mem0+ uses graph memory representations to...

## Sources
- [S010](sources/S010.md)
- [S078](sources/S078.md)
- [S079](sources/S079.md)
- [S080](sources/S080.md)
- [S095](sources/S095.md)

# Hermes

> Agent memory system or framework

## Core Claims
- Hermes Agent ships with **8 external memory provider plugins** that add persistent, cross-session knowledge beyond the always-active built-in MEMORY.md and USER.md. Only one external provider can be a...
- Hermes Agent's memory system comprises **five distinct layers** with a clear cost and locality breakdown: three layers are local and free (context window, skills, FTS5), while two require external ser...
- Hermes Agent's memory is **more layered than it first appears**: four built-in layers (prompt memory, session archive, skills, external provider) with distinct access patterns, plus a pluggable provid...

## Mechanism
- - **8 external providers**: Honcho, OpenViking, Mem0, Hindsight, Holographic, RetainDB, ByteRover, Supermemory.
- **Built-in memory always active**: MEMORY.md + USER.md continue working regardless of ...
- - **5 layers**:
  1. Context window (ephemeral, per-session)
  2. Skills (procedural memory, local markdown in ~/.hermes/skills/)
  3. Contextual vector (optional, external provider)
  4. Honcho (opti...
- - **Layer 1 — Prompt memory (hot)**: MEMORY.md (~2,200 chars / ~800 tokens) + USER.md (~1,375 chars / ~500 tokens). Loaded as frozen snapshot into system prompt at session start for prefix cache stabi...

## Sources
- [S013](sources/S013.md)
- [S014](sources/S014.md)
- [S015](sources/S015.md)
- [S016](sources/S016.md)
- [S020](sources/S020.md)
- [S026](sources/S026.md)
- [S028](sources/S028.md)
- [S035](sources/S035.md)
- [S038](sources/S038.md)
- [S142](sources/S142.md)
- [S143](sources/S143.md)
- [S150](sources/S150.md)
- [S074](sources/S074.md)
- [S076](sources/S076.md)
- [S083](sources/S083.md)
- [S084](sources/S084.md)
- [S085](sources/S085.md)
- [S092](sources/S092.md)
- [S093](sources/S093.md)
- [S099](sources/S099.md)

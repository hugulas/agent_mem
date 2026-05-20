# Honcho

> Agent memory system or framework

## Core Claims
- - Honcho adds AI-native cross-session memory to OpenClaw by persisting conversations to a dedicated service, automatically building user and agent models over time through semantic search and multi-ag...
- - Honcho enhances Hermes's built-in memory with dialectic reasoning and deep user modeling, using a two-layer context injection system with cold/warm prompt selection and three orthogonal configuratio...
- - User modeling (behavioral adaptation) should be treated as a distinct capability from content memory, requiring a dedicated protocol with structured profiles, semantic search, and dialectic Q&A — as...

## Mechanism
- - **Cross-session persistence**: Conversations persisted after every turn; context carries across session resets, compaction, and channel switches.
- **User modeling**: Maintains profiles for each use...
- - **Two-Layer Context Injection**:
  1. **Base context** — session summary, user representation, user peer card, AI self-representation, AI identity card. Refreshed on `contextCadence`.
  2. **Dialect...
- - **UserModelingBackend Protocol**: Abstract protocol with methods:
  - `get_profile()` — structured peer card (name, role, preferences, communication style, expertise, current context).
  - `search()...

## Sources
- [S073](sources/S073.md)
- [S074](sources/S074.md)
- [S077](sources/S077.md)

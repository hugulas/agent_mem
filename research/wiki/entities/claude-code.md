# Claude Code

> Agent memory system or framework

## Core Claims
- Claude Code's architecture is built around a **minimal-scaffolding, maximal-operational-harness** philosophy: a simple while-loop for the agent core, with the vast majority of code (~98.4%) invested i...
- Claude Code manages context pressure through a **multi-tier compaction pipeline** with distinct layers: budget reduction for individual tool outputs, snip compact for temporal depth, microcompact for ...
- Claude Code's source reveals a **5-stage compaction pipeline** confirmed through reverse engineering, with tool results persisted to disk for recovery, a reactive compact mechanism as a last resort, a...

## Mechanism
- - **Agent loop**: Simple `queryLoop()` async generator — model call → tool dispatch → result collection → repeat.
- **Five-layer compaction pipeline** (executes before every model call):
  1. Budget r...
- - **Tool result budgets**: Individual tool outputs capped at configurable sizes (50K/200K characters) to prevent a single verbose output from consuming disproportionate context.
- **Snip compact**: Tr...
- - **5-stage pipeline confirmed**: Matches the academic analysis in S007 (budget, snip, microcompact, context collapse, autocompact).
- **Persisted tool results to disk**: Tool outputs are written to d...

## Sources
- [S007](sources/S007.md)
- [S145](sources/S145.md)
- [S009](sources/S009.md)
- [S012](sources/S012.md)
- [S021](sources/S021.md)
- [S022](sources/S022.md)
- [S032](sources/S032.md)
- [S039](sources/S039.md)
- [S070](sources/S070.md)
- [S151](sources/S151.md)

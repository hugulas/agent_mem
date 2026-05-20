# Codex CLI

> Agent memory system or framework

## Core Claims
- Codex CLI implements a **two-layer memory model**: AGENTS.md as the static, user-maintained instruction layer (cross-tool convention under Linux Foundation's Agentic AI Foundation), and Memories as th...
- Codex CLI has modest system requirements: Node.js 22+, native macOS/Linux support with Windows via WSL, 4 GB minimum RAM and 8 GB recommended, and a lightweight ~50 MB package that also offers a Rust ...
- Codex CLI can be installed natively on Windows 10 build 19041+ with 2 GB minimum RAM (4 GB recommended), Node.js 22+, and includes an experimental AppContainer sandbox for process isolation.

## Mechanism
- - **Layer 1 — AGENTS.md**: Cross-tool instruction file convention (Codex, Cursor, Aider, Jules). Layered discovery: global ~/.codex/AGENTS.md → project walk (root to cwd) → AGENTS.override.md preceden...
- - Node.js 22+ runtime dependency ( aligns with latest LTS )
- Cross-platform packaging: native macOS/Linux, Windows through WSL layer
- Dual distribution: standard JS package (~50 MB) plus optional Ru...
- - Native Windows 10 support starting from build 19041 (May 2020 Update / 20H1)
- Node.js 22+ runtime requirement
- RAM: 2 GB minimum / 4 GB recommended
- AppContainer sandbox: experimental Windows sec...

## Sources
- [S010](sources/S010.md)
- [S023](sources/S023.md)
- [S040](sources/S040.md)

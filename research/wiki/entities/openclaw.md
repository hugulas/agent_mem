# OpenClaw

> Agent memory system or framework

## Core Claims
- OpenClaw 的核心记忆哲学是**"文件即真相"（files-as-source-of-truth）**：代理的所有持久记忆都以纯 Markdown 文件形式保存在工作区磁盘上，LLM 本身不维护任何隐藏状态。模型"记住"的唯一方式是通过文件读写工具将信息写入磁盘。
- OpenClaw's builtin memory engine is a **local-first, SQLite-backed hybrid search system** that combines FTS5 BM25 keyword search with vector semantic search, using Markdown files as the canonical sour...
- **⚠️ 本地 PDF 内容不匹配**：下载的 PDF（arXiv:2603.09872）实际内容为 MIT 的阅读时间预测研究，而非 OpenClaw 安全分析。以下笔记基于 reading-log 记录的关键声明和关联来源（S004、S031、evidence-matrix）重构。

OpenClaw 的**文件系统记忆架构**在带来透明性和可审计性的同时，引入了严重的**安全表面扩张（att...

## Mechanism
- - **三层文件架构**：
  - `MEMORY.md`：精心策划的长期记忆，包含持久事实、偏好和决策。在每个主会话开始时注入系统提示。
  - `memory/YYYY-MM-DD.md`：每日工作笔记，记录运行上下文和观察。今天和昨天的笔记自动加载，但不注入每轮引导提示。
  - `DREAMS.md`（可选）：梦境扫描摘要，用于人类审阅的历史回填条目。
- **记忆蒸馏循环**：代理被期望...
- - **Hybrid search (union, not intersection)**: Vector search (70% weight) + BM25 keyword search (30% weight). Results from either search contribute; missing one score defaults to 0 rather than filteri...
- - **Memory Vault 设计**：OpenClaw 将所有记忆状态以 Markdown 文件和 SQLite 数据库存储于本地工作区（`~/.openclaw/workspace`）。
- **Gateway 进程**：WebSocket local-first 架构，Node.js/TypeScript 实现，支持 15+ 消息平台。Gateway 作为单写器（single-write...

## Sources
- [S001](sources/S001.md)
- [S002](sources/S002.md)
- [S003](sources/S003.md)
- [S004](sources/S004.md)
- [S005](sources/S005.md)
- [S006](sources/S006.md)
- [S018](sources/S018.md)
- [S019](sources/S019.md)
- [S026](sources/S026.md)
- [S028](sources/S028.md)
- [S030](sources/S030.md)
- [S033](sources/S033.md)
- [S035](sources/S035.md)
- [S073](sources/S073.md)
- [S098](sources/S098.md)
- [S100](sources/S100.md)

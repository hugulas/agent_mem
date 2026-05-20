# 主流 Agent 框架记忆系统洞察报告

> **研究范围**：OpenClaw、Claude Code、OpenAI Codex CLI、Hermes Agent 的记忆子系统架构、底层技术、性能表现与芯片/硬件诉求  
> **研究状态**：已审计（audited）  
> **日期**：2026-05-20

---

## 目录

1. [执行摘要](#1-执行摘要)
2. [研究方法与信息源](#2-研究方法与信息源)
3. [核心发现：四大框架记忆架构总览](#3-核心发现四大框架记忆架构总览)
4. [分框架深度解析](#4-分框架深度解析)
   - 4.1 OpenClaw
   - 4.2 Claude Code
   - 4.3 Codex CLI
   - 4.4 Hermes Agent
   - 4.5 字节跳动 UI-TARS / 豆包 / Seed-TARS / OpenViking
   - 4.6 美国互联网厂商记忆系统洞察（Google / Microsoft / Amazon / Meta / Apple）
   - 4.7 Karpathy LLM Wiki：编译器模式的个人知识记忆
5. [技术对比：存储、检索与压缩](#5-技术对比存储检索与压缩)
6. [系统性能要求与硬件诉求](#6-系统性能要求与硬件诉求)
7. [安全与隐私考量](#7-安全与隐私考量)
8. [研究缺口与残余不确定性](#8-研究缺口与残余不确定性)
9. [结论与选型建议](#9-结论与选型建议)

---

## 1. 执行摘要

2026 年的主流 Agent 框架在记忆系统上呈现鲜明的架构分野：**文件即真相（file-as-source-of-truth）** 是开源框架的共同底座，而**云厂商则倾向于托管式用户画像 + 超长上下文窗口**的混合路线。在检索机制、压缩策略和扩展性上差异显著。

- **OpenClaw**：采用 Markdown 文件 + SQLite 混合检索（向量相似度 70% + BM25 30%）的内存架构，支持本地 GGUF embedding（~0.6 GB）和 7 种云端 embedding 提供商。记忆召回在特定基准下可达约 19.6 秒（300 条事件），适合多通道、长期运行的个人助手场景。Gateway 进程本身轻量（空闲 400–800 MB），但对 Node.js 22+ 有硬性要求。
- **Claude Code**：以 4 层 `CLAUDE.md` 文件层级和 5 层渐进式上下文压缩管道为核心竞争力，深度集成 Prompt Cache 以节省 API 成本。无内置跨会话持久记忆（依赖 `CLAUDE.md` 手写或 auto-memory 插件），是四人中最“项目级”而非“个人级”的记忆设计。本地运行开销极低，主要瓶颈在云端模型调用。
- **Codex CLI**：采用极简的两层记忆——静态 `AGENTS.md`（32 KiB 上限）和后台异步生成的 `Memories`。召回机制出人意料地简单：直接读取 `memory_summary.md` 全文，需要细节时 `grep` 长文件。Rust 构建的 CLI 体积极小（~50 MB），4 GB RAM 即可运行，但 Memories 功能在 EEA/UK/CH 不可用，且不支持团队共享。
- **Hermes Agent**：五人中最“重”的记忆架构——内置 5 层记忆（上下文窗口、Skills、向量上下文、Honcho 用户建模、SQLite FTS5），并支持 8 个可插拔外部记忆提供商（Hindsight 在 LongMemEval 上达 91.4% 准确率）。FTS5 检索延迟约 10 ms（万级文档）到 113 ms（基准测试），显著优于 OpenClaw 的 JSONL 全量回注策略。Python 3.11+ 运行，空闲 <512 MB。
- **字节跳动 UI-TARS / 豆包 / OpenViking**：字节在 Agent 记忆领域有**三条并行路线**。UI-TARS 走**原生 Agent 模型**路线，在模型内部实现分层记忆状态 `Mt=(Wt,Et)`；豆包手机采用**“云端理解 + 本地存储 + 向量检索”**的端云协同架构；OpenViking（火山引擎开源，6.3K+ stars）则是一款**上下文数据库**，以文件系统范式 `viking://` 和 L0/L1/L2 三层加载替代传统 RAG，潜在 Token 节省 60–80%，并支持可视化检索轨迹调试。
- **美国互联网厂商（Google / Microsoft / Amazon / Meta / Apple）**：五家厂商的记忆策略分化明显。**Google** 以 Gemini 2M 超长上下文 + Project Astra 多模态记忆 + Context Caching 为核心；**Microsoft** 推出 Copilot 三域记忆（User/Repository/Session）和 Azure Foundry Agent Memory；**Amazon** 提供 Bedrock AgentCore Memory 托管服务（自动提取语义事实/偏好/摘要/情景记忆）；**Apple** 以设备端语义索引（Semantic Index）+ Private Cloud Compute 隐私架构为差异化；**Meta** 则最为保守，LLaMA 4 虽支持 10M token 上下文，但尚无成熟的持久化记忆产品。
- **Karpathy LLM Wiki**：Andrej Karpathy 提出的**编译器模式**工作流——LLM 将原始资料"编译"为持久化 Markdown Wiki，持续维护而非每次查询重新推导。100 篇文章/40 万词的个人 Wiki 已验证可行，代表了"文件即真相"哲学的极致：LLM 不仅是记忆的使用者，更是记忆的作者。与 RAG 的根本区别在于时间模式（有状态编译 vs 无状态检索）。

**基准测试可信度危机**：记忆提供商领域的基准测试存在严重不一致。Mem0 官方博客宣称在 LongMemEval 上达 94.4%，但独立复现（S095）仅得 49%，差距高达 **45.4 个百分点**；LoCoMo 上自报 91.6%  vs 论文复现 67.13%，差距 24.5pp。这暴露了该领域缺乏标准化评估协议——不同模型后端、评分标准和结果选取方式导致数字几乎不可比较。目前最可信的公开基准是 **TiMem**（LoCoMo 75.30%、LongMemEval-S 76.88%）和 **Hindsight**（LongMemEval 91.4%，Gemini-3 后端），但两者尚未在同一硬件上直接对决。

**学术前沿四条路线**：基于 120 份阅读笔记梳理的学术记忆架构呈现四种创新范式：(1) **ByteRover** 首次将 RL 训练用于离散记忆操作（ADD/UPDATE/DELETE/NOOP），仅需 152 个训练对；(2) **TiMem** 的 Temporal Memory Tree 在 LoCoMo 和 LongMemEval 上均达 SOTA，通过五级时序层级实现 52.20% 的召回长度缩减；(3) **LoCoMo/ST-Lite** 提供无需训练的自由 KV Cache 压缩，在 10–20% 缓存预算下实现 2.45× 解码加速；(4) **AtlasKV** 将十亿级知识图谱参数化到模型内部，<20GB VRAM 即可运行，无需外部检索器——但更新新事实需重新训练。

**记忆更新策略的六种范式**：框架在"何时记忆、如何更新、何时遗忘"上存在根本性分歧。**OpenClaw** 采用 Agent 自主判断写入；**Claude Code** 在上下文窗口压力时触发 5 层渐进压缩；**Codex CLI** 在会话结束后 6 小时批量合并；**Mem0** 实时执行 ADD/UPDATE/DELETE 原子操作；**Hindsight** 每轮交互后更新知识图谱并执行信念修正；**Honcho** 通过辩证 Q&A 生成深层用户画像。没有单一策略在所有维度上占优——实时性（Mem0）vs 崩溃韧性（OpenClaw 文件持久）vs Token 效率（Claude Code 压缩）构成不可能三角。

**安全态势：全员裸奔，Codex CLI 略好**：四个主要开源框架**均不提供默认的静态加密或内存加密**。OpenClaw 存在已知 CVE-2026-25253（CVSS 9.8），明文存储 API 密钥于 Markdown/SQLite；Claude Code 和 Hermes 依赖 OS 级磁盘加密；**Codex CLI 是唯一内置 secret redaction 的框架**（记忆落盘前自动脱敏凭据）。云厂商中 Apple 的 PCC 密码学证明和 Microsoft 的 Purview 审计构成当前最强企业级安全架构，但均要求完全信任 vendor。开源 vs 闭源的安全模型差异显著：开源遵循"不信任，只验证"但 CVE 公开可 exploited；闭源依赖 vendor 自证但用户无法独立验证。

**芯片/硬件核心结论**：开源框架本身都是“编排层”，对芯片几乎没有直接诉求。真正的硬件压力来自**本地 LLM 推理**（Ollama/vLLM/llama.cpp）和**端侧向量检索**。若仅使用云端 API，Raspberry Pi（4 GB）或 $5/月 VPS 即可运行；若要在本地跑 7B 模型，需 8–16 GB RAM；70B 模型则需要 48–128 GB RAM 或高端 GPU（RTX 4090 / Apple M4 Max）。Apple Silicon 的统一内存架构在端侧大模型 + 向量索引场景下具有独特优势；Amazon 则通过 S3 Vectors 和 Neptune Analytics 将向量存储成本降低达 90%。

---

## 2. 研究方法与信息源

本研究遵循深度搜索材料技能（Deep Research Search Materials）工作流，并在第二阶段构建了 Karpathy 风格的结构化知识库（LLM Wiki）：

- **搜索方向**：18 个独立方向，涵盖核心架构、压缩策略、向量检索、硬件部署、多智能体共享、安全漏洞、竞争对比、学术前沿、字节跳动 UI-TARS/Seed-TARS、Google Astra/Gemini、Microsoft Copilot/Azure、Meta/Amazon/Apple 记忆系统，以及外部记忆提供商（Mem0、Hindsight、Honcho、Supermemory 等）深度评估。
- **候选池规模**：搜索并筛选了 150+ 来源，最终保留 **120 条**进入 reading log，全部完成结构化阅读笔记（reading-notes/S001–S120.md）。
- **来源分级**：优先采用官方文档、arXiv 论文（2604.14228、2603.27517、2603.12644、2502.07938 等）、逆向工程源码分析报告、独立基准复现（S095）；对 Skywork 等营销类幻灯片中的数字（如“82% 成本降低”）单独标注为待验证。
- **知识体系构建**：基于 120 份阅读笔记编译了 **177 页的 Karpathy 风格 LLM Wiki**，包含：120 个源页面（sources/）、22 个实体页面（entities/）、10 个概念页面（concepts/）、16 个对比页面（comparisons/）、6 个导航地图（maps/）。Wiki 采用 CLAUDE.md 模式（原始资料 → 结构化笔记 → 编译 Wiki → 可维护 Schema），确保知识可复利、可审计、可溯源。
- **审计状态**：已完成 evidence matrix 与 gap audit。主要缺口：(1) 缺乏四框架在**同一硬件、同一任务集**下的标准化记忆基准测试；(2) 记忆提供商的基准数字存在严重不一致（Mem0 自报 vs 独立测试差距达 45pp），需读者自行判断可信度；(3) 部分来源（S003、S062）存在 PDF 内容不匹配，已用交叉引用修复，但标记为红色警戒。

---

## 3. 核心发现：四大框架记忆架构总览

| 维度 | OpenClaw | Claude Code | Codex CLI | Hermes Agent | 字节 UI-TARS/豆包 | Google Astra/Gemini | Microsoft Copilot | Apple Intelligence |
|---|---|---|---|---|---|---|---|---|
| **记忆哲学** | 文件即真相 + 结构化长期记忆 | 项目级指令层级 + 渐进压缩 | 静态指令 + 自动生成摘要 | 多层持久记忆 + 自主技能进化 | 原生模型内分层记忆 + 端云协同 | 超长上下文 + 多模态个人记忆 | 三域托管记忆 + 企业治理 | 设备端语义索引 + 隐私优先 |
| **长期存储格式** | MEMORY.md + 每日笔记 + DREAMS.md | CLAUDE.md（4 层层级） | AGENTS.md（32 KiB 上限）+ Memories 目录 | MEMORY.md/USER.md + SQLite FTS5 + Skills | 云端情景记忆 Et + 本地向量库 | Gemini 上下文缓存 + Astra 交互历史 | User/Repository/Session 三级存储 | 设备端语义索引（向量 DB） |
| **检索机制** | 混合搜索：向量相似度 + BM25 + MMR + 时间衰减 | LLM 扫描文件头 | 全文加载 summary + grep 细节 | FTS5 全文检索 + 外部向量/图谱提供商 | 本地向量检索（embedding） | 注意力机制全上下文 + 工具检索 | 语义相似度 + 作用域过滤 | 语义索引 + App Intents 匹配 |
| **上下文压缩** | 可插拔压缩器 + 压缩前记忆刷新 | 5 层渐进压缩（预算/截断/微压缩/折叠/自动压缩） | 单层 handoff summary | /compress 命令 + ByteRover 预压缩提取 | 模型内语义压缩（Et） | 2M 原生上下文窗口 + KV Cache | 意图驱动存储 + 自动摘要 | 设备端 3B 模型 + PCC 升级 |
| **跨会话持久** | 是（文件天然持久） | 部分（依赖 CLAUDE.md 或 auto-memory） | 是（Memories 后台合并） | 是（SQLite + 文件 + 外部提供商） | 是（云端持久 + 本地向量） | 是（Google 账户级） | 是（Microsoft 账户级） | 是（iCloud 同步语义索引） |
| **团队共享** | 可通过仓库共享 AGENTS.md | 可通过仓库共享 CLAUDE.md | 不支持（Memories 单用户本地） | 可通过 Hindsight Cloud / RetainDB 共享 | 否（个人设备级） | 有限（家庭/工作空间） | 是（租户级 + 共享会话） | 否（严格个人设备） |
| **本地 embedding** | 支持（node-llama-cpp GGUF） | 无（记忆不依赖向量） | 无（记忆不依赖向量） | 支持（Holographic 零依赖 SQLite） | 支持（本地 embedding 模型） | 否（云端） | 否（云端） | 是（设备端 Core ML） |
| **运行时/部署** | Node.js 22+ 本地进程 | Shell + Node 本地进程 | Rust 二进制本地运行 | Python 3.11+ 本地进程 | 云端大模型 + 本地 Agent 运行时 | 云端 Gemini API | 云端 M365/Azure + VS Code 本地缓存 | 设备端 AFM + PCC 服务器 |
| **空闲内存** | 400–800 MB（Gateway） | ~300–500 MB | ~50 MB 包体 | <512 MB | N/A（模型级） | N/A（云端） | N/A（云端） | N/A（系统级） |

---

## 4. 分框架深度解析

### 4.1 OpenClaw

#### 架构概览
OpenClaw 是一个本地优先（local-first）的持久型 Agent 框架，以 Node.js Gateway 进程为中心，通过 WebSocket 管理会话、通道和工具调用。其记忆系统的核心设计是**明文 Markdown 文件作为唯一真相源**，所有索引（SQLite、向量）均为派生。

#### 记忆文件层级
1. **MEMORY.md**：精简的常青知识（偏好、决策、设计规则），在每个 DM 会话启动时注入系统提示词。
2. **memory/YYYY-MM-DD.md**：每日工作层，记录当天纪要、临时决策、会议记录。不默认注入提示词，而是通过 `memory_search` / `memory_get` 按需检索。
3. **DREAMS.md**（可选）： dreaming 后台整合的摘要，供人工审查。

#### 检索引擎：Builtin Memory Engine
默认后端为 SQLite，具备：
- **FTS5 全文索引**：BM25 评分，支持 CJK  trigram 分词。
- **向量搜索**：通过外部或本地 embedding 提供商生成向量，存储于 SQLite（可选 sqlite-vec 加速）。
- **混合搜索**：`finalScore = 0.7 × vectorScore + 0.3 × textScore`，并支持 MMR（Max Marginal Relevance，λ=0.7）以保证结果多样性，以及 30 天半衰期的时间衰减。

#### Embedding 提供商链
自动检测优先级：本地 GGUF（如 embeddinggemma-300M，~0.6 GB）→ OpenAI → Gemini → Voyage → Mistral → DeepInfra → Ollama。若全部失败，优雅降级为纯 BM25 关键词搜索。

#### 记忆刷新与 Dreaming
- **Pre-compaction Flush**：在上下文压缩前，系统会先发一个静默回合提醒 Agent 将重要信息写入记忆文件，防止压缩导致信息丢失。软阈值：4000 tokens 或 2 MB 转录文件。
- **Dreaming**（默认关闭）：后台 cron 任务收集短期信号，通过评分、回忆频率和查询多样性门槛，将合格条目从短期记忆提升为长期 MEMORY.md。

#### 性能与扩展
- **索引参数**：Chunk 400 tokens / overlap 80 tokens；snippet 最大 700 chars；embedding 批处理 8000 tokens；并发 4。
- **文件监控**：1.5 秒防抖（debounce）的增量重索引。
- **记忆 Wiki 插件**：将持久记忆编译为带有来源标记（Providence Tags：Observed / User-Confirmed / Model-Inferred）的知识库，防止“记忆淤泥（memory sludge）”。

### 4.2 Claude Code

#### 架构概览
Claude Code 是 Anthropic 的代码专用 Agent CLI/IDE 工具，其记忆系统围绕 **CLAUDE.md 四级层级** 和 **五层渐进式上下文压缩管道** 构建。与 OpenClaw/Hermes 不同，它不做跨会话的自动长期记忆沉淀，而是强调“状态重建”而非“聊天记录延续”。

#### CLAUDE.md 四级层级
1. 用户级全局 `~/.claude/CLAUDE.md`
2. 组织级（如公司标准）
3. 项目级（仓库根目录）
4. 工作区/子目录级

文件在会话启动时加载，Agent 可通过工具读取和更新它们，但不存在自动的“每日笔记”或 dreaming 系统。

#### 五层压缩管道（按成本从低到高）
1. **Tool Result Budget**：单个工具结果上限 50K chars，单条消息上限 200K chars；超限时持久化到磁盘（`sessionDir/tool-results/`），原消息替换为 `<persisted-output>` 占位符。
2. **Snip Compact**：直接移除最旧的消息组，最粗暴但最便宜。
3. **Microcompact**：选择性清除旧工具结果，利用 Anthropic `cache_edits` API 在 cache 热时保留前缀稳定性（匹配服务端 60 分钟 TTL）。
4. **Context Collapse**：分阶段折叠消息块，创建折叠视图而不删除原始数据。
5. **Auto-Compact**：当历史占用达到 `contextWindow - 13K` 时，调用 Claude API 生成结构化摘要。使用“私有草稿本”技巧：先输出 `<analysis>` 推理，再输出 `<summary>`，最终只保留 summary 注入上下文。连续 3 次失败则触发断路器，防止无限重试。

#### 记忆检索
采用 **LLM-based 文件头扫描**：Claude Code 不维护向量索引，而是让模型扫描 CLAUDE.md 文件的头部来决定加载哪些内容。这种方式精确但消耗 API tokens。

#### Auto-Memory（跨会话）
- 官方 auto-memory 功能让 Agent 自动将项目知识（构建命令、目录结构、代码风格）写回 `CLAUDE.md` 或相关记忆文件。
- 社区插件（如 ClaudeMem）提供 `/remember`、`/forget` 等命令，但属于第三方扩展。

#### 独特优势：Prompt Cache 感知
Claude Code 的压缩设计刻意保持前缀稳定，使压缩后的请求仍能复用之前写入的 Prompt Cache，这是其显著降低长会话 API 成本的关键机制。

### 4.3 Codex CLI

#### 架构概览
Codex CLI 是 OpenAI 用 Rust 编写的开源终端编码 Agent，其记忆模型刻意保持极简，分为**静态层**和**生成层**。

#### Layer 1：AGENTS.md（静态指令）
- 遵循 Linux Foundation Agentic AI Foundation 的开放规范。
- 发现顺序：全局 `~/.codex/AGENTS.md` → 项目路径自上而下的所有 `AGENTS.md` → 支持回退到 `CLAUDE.md`、`.cursorrules` 等跨工具命名。
- **硬性上限 32 KiB**（约 8000 tokens），超出部分静默截断。

#### Layer 2：Memories（生成记忆）
- 完全由 Codex 自主维护，存储于 `~/.codex/memories/`。
- **两阶段管道**：
  - Phase 1（每会话）：空闲 6 小时后触发，用 extraction model 采样对话并提取要点，内置 secret redaction（凭据脱敏）。
  - Phase 2（合并）：获取全局锁，用 consolidation model 将候选记忆与现有存储合并。
- **存储格式**：纯 Markdown，固定文件集：`memory_summary.md`（会话启动时全读）、`MEMORY.md`（长合并文件）、`raw_memories.md`、按技能划分的 `skills/<name>/SKILL.md`、每会话的 `rollout_summaries/<slug>.md`。
- **召回机制**：读取 `memory_summary.md` 全文并做 token 截断；需要更多细节时，**指示 Agent 用 `grep` 搜索 `MEMORY.md`**——完全没有向量检索。

#### 限制与缺口
- **无跨设备同步**：`~/.codex/memories/` 是纯本地生成状态。
- **无团队共享**：新团队成员的首次会话只有项目 `AGENTS.md`，无法继承队友已生成的记忆。
- **地理限制**：EEA、英国、瑞士用户无法使用 Memories 功能。
- **Cloud Codex 记忆未公开**：OpenAI 称云端记忆跨会话持久，但存储形态、保留策略未披露。

### 4.4 Hermes Agent

#### 架构概览
Hermes 由 Nous Research 开发，定位是“会自我改进的 Agent”，其核心差异在于**闭环学习**：从交互中提取模式，自动编码为可复用 Skill。记忆系统是支撑这一闭环的基石。

#### 五层记忆架构
| 层级 | 存储 | 内容 | 速度 |
|---|---|---|---|
| 工作记忆 | 上下文窗口 | 当前对话 | 即时 |
| 持久存储 | Markdown（MEMORY.md） | 长期事实与偏好 | 快速 |
| 结构化存储 | SQLite + FTS5 | 会话历史、跨会话检索 | ~10 ms（万级文档） |
| 程序性记忆 | Skill 文件（agentskills.io 标准） | 可复用工作流 | 按需加载 |
| 用户建模 | Honcho / USER.md | 用户理解与偏好 | 中等 |

- **FTS5 检索**：SQLite 内置全文搜索，基准约 10 ms 检索 10,000+ 文档，可扩展至约 10 万文档后才需专用向量数据库（Qdrant/Weaviate/Chroma）。
- **Skill 加载优化**：默认只将 Skill 名称和简述加载到系统提示词，完整 body 按需加载，因此 Skill 库从 40 扩展到 200+ 对上下文成本影响极小。

#### 8 个外部记忆提供商（v0.7.0+ 插件化）
| 提供商 | 存储 | 成本 | 独特能力 |
|---|---|---|---|
| **Honcho** | Cloud/自托管 | 付费/免费 | 辩证用户建模（dialectic reasoning），AGPL v3.0 |
| **OpenViking** | 自托管 | 免费 | 字节跳动 Volcengine，L0/L1/L2 分层加载 |
| **Mem0** | Cloud | 免费增值 | 服务端 LLM 提取，30 秒 setup |
| **Hindsight** | Cloud/Local | 免费/付费 | 知识图谱 + reflect 合成，LongMemEval 91.4% |
| **Holographic** | 本地 SQLite | 免费 | 零 pip 依赖，HRR 代数 + 信任评分 |
| **RetainDB** | Cloud | $20/月 | 混合搜索 + delta 压缩 |
| **ByteRover** | 本地/Cloud | 免费/付费 | 预压缩提取，防止上下文压缩丢失信息 |
| **Supermemory** | Cloud | 付费 | 语义长期记忆 + 会话图构建 |

#### 自我改进循环（GAPA-like）
1. **Observe**：监测环境、排名、消息。
2. **Reason**：LLM 评估选项、规划多步动作。
3. **Act**：通过浏览器、API、终端执行。
4. **Learn**：提取模式，编码为 Skill，通过使用不断优化。

此循环不是模型微调（无需 GPU/数据集），而是**提示级自适应**——通过更好的提示、记忆检索和工具编排来优化表现。

---

### 4.5 字节跳动 UI-TARS / 豆包 / Seed-TARS

#### 架构定位：原生 Agent 模型 vs 框架插件

与 OpenClaw、Hermes 等“框架级”记忆系统不同，字节跳动走了一条**原生 Agent 模型（Native Agent Model）**路线。UI-TARS 不是在大模型外接记忆模块，而是将感知（Perception）、推理（Reasoning）、记忆（Memory）和行动（Action）统一在一个端到端模型内部。这种设计哲学的核心是：Agent 的进化正从“框架组装”转向“模型原生”。

#### UI-TARS-2 的分层记忆状态

根据 UI-TARS-2 技术报告（arXiv:2509.02544），其记忆架构采用严格的数学形式化：

```
Mt = (Wt, Et)
```

- **工作记忆（Working Memory, Wt）**：保存最近 k 个步骤的高保真轨迹，包含完整的 reasoning trace、action 和 observation。直接参与当前推理，但受限于上下文窗口，只保留最后 N 步。
- **情景记忆（Episodic Memory, Et）**：对历史 episode 进行语义压缩后的摘要，保留关键意图、决策和结果。用于长程召回，当 Wt 无法覆盖时使用 Et 进行条件推理。

这种双轨设计与认知神经科学中的工作记忆-长期记忆分工高度一致，也与 OpenClaw 的“短期上下文 vs 长期 Markdown 文件”异曲同工——区别在于 UI-TARS 的压缩和检索发生在**模型内部**，而非外部数据库。

#### UI-TARS-1.5 的能力边界

- **视觉 grounding**：基于 Qwen2.5-VL-7B，用 15 亿条 GUI 专用数据微调，视觉编码器处理 1120×1120 分辨率截图，UI 元素定位误差 <5 像素。
- **推理机制**：引入 System 2 “先思考再行动”（think-before-act）机制，在 Minecraft 导航任务中将错误方块放置减少 38%。
- **记忆与效率**：双轨记忆系统根据任务复杂度动态调配资源，操作延迟降低 30% 以上。
- **成本**：每 1,000 次操作 $0.12，比 GPT-4V 低 43%。

#### 豆包手机：端云协同的记忆架构

豆包手机（字节深度集成的 AI 手机）采用**“云端理解 + 本地存储 + 向量检索”**三路架构：

1. **云端模型 InternVL3-2B**：负责屏幕理解、推理和任务规划。手机以约 3–5 秒间隔上传约 250 KB 的压缩截图包，云端返回约 1 KB 的下一步行动指令（点击坐标、滑动方向、文本输入）。
2. **本地 embedding 模型**：负责将用户交互历史、偏好、常用应用行为编码为向量，存储在本地向量数据库中。
3. **本地检索**：当用户触发相关查询时，本地向量检索优先召回历史记忆，减少云端往返。

这种架构的隐私 implication 是**敏感操作留在本地检索层，复杂推理上云**——与 Apple Intelligence 的“设备端语义索引 + Private Cloud Compute”有异曲同工之妙。

#### 与四大开源框架的对比

| 维度 | UI-TARS/豆包 | OpenClaw | Hermes Agent |
|---|---|---|---|
| **记忆层级** | 模型内双轨（Wt/Et） | 文件 + SQLite 外部存储 | 文件 + SQLite + 外部提供商 |
| **可干预性** | 低（黑盒模型行为） | 高（用户可直接编辑 Markdown） | 高（可插拔提供商） |
| **部署形态** | 云端 API + 手机系统级集成 | 自托管 Gateway | 自托管 Python 进程 |
| **隐私模型** | 端云协同（敏感记忆本地） | 完全本地优先 | 完全本地优先（可选云提供商） |
| **跨会话持久** | 依赖云端账户 | 文件天然持久 | SQLite + 文件持久 |

#### OpenViking：字节跳动的上下文数据库（Context Database）

OpenViking（GitHub: `volcengine/OpenViking`，6.3K+ stars，Apache 2.0）是字节跳动火山引擎团队开源的**上下文数据库**，与 UI-TARS 的"模型内记忆"形成互补——前者解决**框架级记忆的检索效率和可观测性**问题。

**核心设计：文件系统范式 + L0/L1/L2 分层加载**

OpenViking 抛弃了传统 RAG 的扁平向量切片模型，将所有上下文（记忆、资源、技能）映射到 `viking://` 协议下的虚拟文件系统中：

```
viking://resources/my_project/
├── .abstract               # L0: ~100 tokens 一句话摘要
├── .overview               # L1: ~2K tokens 核心概览
├── docs/
│   ├── .abstract
│   ├── .overview
│   └── api/
│       ├── .abstract
│       ├── .overview
│       └── auth.md        # L2: 完整原始内容
```

- **L0（Abstract）**：一句话摘要，用于快速识别相关性。
- **L1（Overview）**：约 2,000 tokens 的核心信息，支撑 Agent 在规划阶段做决策。
- **L2（Details）**：完整原始数据，仅在 Agent 确认需要深度阅读时按需加载。

**目录递归检索与可视化轨迹**

OpenViking 的检索不是简单的向量相似度搜索，而是**目录定位 + 语义搜索的递归组合**：先用向量相似度定位到正确目录，再在目录内二次搜索，逐级下钻子目录。整个检索路径被记录为**可视化轨迹**——当 Agent 召回错误上下文时，开发者可以观察它遍历了哪些目录、停留了哪些文件，从而调试检索逻辑而非面对黑盒。

**Token 节省效果**

Red Hat 的部署指南给出了一个典型场景：50 份内部运维手册，传统 RAG 可能加载超过 50K tokens 的切片；OpenViking 只需扫描 50 份 L0 摘要（~5K tokens），缩小到 3 份最相关的 L1 概览（~6K tokens），最后只加载 1 份真正需要的 L2 全文。**潜在节省可达 60–80%**，且避免了上下文窗口溢出。

**自动会话管理与记忆自迭代**

OpenViking 内置会话压缩和记忆提取循环：
1. 会话结束时，系统自动分析任务执行结果和用户反馈。
2. 提取 durable memory（用户偏好、Agent 操作经验、工具使用模式）。
3. 更新到 `viking://user/memories/` 和 `viking://agent/memories/` 目录。

核心代码规模：`memory_extractor.py` ~1,200 行、`memory_deduplicator.py` ~395 行、`compressor.py` ~447 行——记忆提取、去重、压缩是三大核心模块。

**与四大开源框架的关系**

OpenViking 已被 Hermes Agent 集成为 8 个外部记忆提供商之一（`OpenViking` 提供商）。它代表了字节跳动在 Agent 记忆基础设施上的**第二战线**：UI-TARS 负责"模型内记忆"，OpenViking 负责"框架外记忆检索"。

| 维度 | OpenViking | 传统 RAG | OpenClaw 混合搜索 |
|---|---|---|---|
| **存储组织** | 层级文件系统（viking://） | 扁平向量切片 | Markdown + SQLite 混合 |
| **检索方式** | 目录递归 + 语义搜索 | 纯向量相似度 | 向量 + BM25 + MMR |
| **Token 控制** | L0/L1/L2 自动分层 | 手动 chunk 大小 | 可插拔压缩器 |
| **调试能力** | 完整可视化检索轨迹 | 几乎没有 | 有限（搜索日志） |
| **记忆进化** | 自动会话提取 + 自迭代 | 不支持 | 手动/插件 |
| **离线能力** | 否（需外部 LLM 生成 L0/L1） | 依赖配置 | 完整 |

---

### 4.6 美国互联网厂商记忆系统洞察（Google / Microsoft / Amazon / Meta / Apple）

#### Google：超长上下文 + Astra 多模态记忆

Google 的记忆策略是**“用超长上下文窗口减少对外部记忆的依赖，同时用 Astra 探索原生多模态个人记忆”**。

- **Gemini 2M 上下文窗口**：Gemini 1.5 Pro 支持 200 万 token 上下文（相当于 1.4M 词或 2 小时视频），并推出 Context Caching API，允许开发者将常用上下文缓存复用，降低重复 prompt 成本。对于 1M token 的 KV Cache，预估需约 15 GB GPU 内存/用户。
- **Project Astra**：基于 Gemini 2.0 的研究原型，目标是“通用 AI 助手”。Astra 的“多模态记忆”能整合文本、图像、音频，记住用户过往交互的关键细节，并跨工具（Search、Gmail、Calendar、Maps）检索内容。Astra 支持手机摄像头实时对话和原型眼镜形态。
- **NotebookLM**：文档级长期记忆产品，支持对大量文档的持续合成和演进式上下文保留。

Google 路线的特点是**模型层解决记忆问题**（靠超长上下文 + KV Cache），而非像 OpenClaw/Hermes 那样依赖外部向量数据库。但这带来了基础设施成本：2M token 的预填充延迟可达 2 分钟以上，KV Cache 内存占用巨大。

#### Microsoft：三域托管记忆 + 企业治理

Microsoft 在 2025 年下半年推出了迄今为止最完整的**企业级记忆产品线**：

- **Copilot Memory（M365/Consumer）**：2025 年 7 月 GA。采用三域记忆模型：
  - **User 域**：跨所有工作区和会话持久，保存用户偏好、常用命令（自动加载前 200 行）。
  - **Repository 域**：工作区级别，保存代码库约定、项目结构、构建命令。
  - **Session 域**：会话级别，任务完成后清除。
  记忆存储由用户和租户管理员共同控制，支持 Purview eDiscovery 合规审计。
- **VS Code Copilot Memory Tool**：2026 年 5 月进入预览。所有记忆数据**本地存储**，提供三种作用域，与云端 Copilot Memory 形成互补。
- **Azure AI Foundry Agent Memory（Preview）**：面向开发者的托管记忆服务，支持跨会话持久上下文，后端可选 Cosmos DB + Azure AI Search。

Microsoft 的核心优势是**企业治理集成**——记忆隔离、Entra Agent ID、RBAC、自动保留策略——这是开源框架目前最薄弱的环节。

#### Amazon：Bedrock AgentCore Memory — 完全托管的 STM/LTM

Amazon 在 2026 年初推出的 Bedrock AgentCore Memory 是一个**无服务器化的记忆基础设施**：

- **两层记忆**：
  - **短期记忆（STM）**：保存会话内原始对话事件，支持多轮上下文和服务重启后的会话续接。
  - **长期记忆（LTM）**：自动异步提取语义事实（Semantic）、用户偏好（UserPreference）、对话摘要（Summary）和情景切片（Episodic）。
- **零运维**：开发者无需管理数据库、embedding 管道或提取逻辑，50 行 Java 代码即可接入。
- **AWS 原生集成**：与 Neptune Analytics（图记忆后端）、ElastiCache for Valkey（高速缓存）、S3 Vectors（原生向量存储，宣称降低 90% 向量存储成本）无缝配合。

Amazon 的路线是**基础设施即服务**——把记忆作为 Bedrock 生态的一个托管组件，最适合已有 AWS 技术栈的企业。

#### Apple：设备端语义索引 + Private Cloud Compute

Apple Intelligence 的记忆架构是五家厂商中**最独特的隐私优先设计**：

- **语义索引（Semantic Index）**：系统级的向量数据库，对用户的短信、邮件、日历、照片等个人数据进行 embedding，支持基于含义（而非关键词）的检索。这是 Siri 理解“个人上下文”的基础设施。
- **App Intents 工具箱**：所有应用向系统注册可执行操作（类似于 Agent 的工具集），Siri/Agent 运行时通过 orchestration 层调度。
- **三层计算架构**：
  - 设备端 3B Apple Foundation Model（AFM）处理简单请求。
  - Private Cloud Compute（PCC）服务器处理复杂请求，运行 Apple Silicon，提供密码学可验证的隐私保证（零数据保留、无法被 Apple 工程师访问）。
  - 第三方大模型（ChatGPT / Google Gemini）处理世界知识查询。
- **Ferret-UI**：Apple 自研的屏幕理解模型，使 Agent 能“看到”iOS 屏幕并按像素坐标执行操作。

Apple 的主要限制是**Siri 全面 AI 化已延期至 2026 年春季**，当前 Apple Intelligence 功能（写作工具、通知摘要、图片清理）距离完整的 Agent 记忆体验仍有显著差距。

#### Meta：最保守的记忆策略

Meta 在五大厂商中记忆能力最不成熟：

- **LLaMA 4**：支持高达 1,000 万 token 的上下文窗口（通过 MindStudio 等第三方框架），但这属于模型上下文容量，并非持久化跨会话记忆架构。
- **无专用记忆产品**：与 OpenAI（ChatGPT Memory）、Google（Astra）、Microsoft（Copilot Memory）、Apple（Semantic Index）不同，Meta 目前未向消费者提供具备持久跨会话记忆的产品。
- **开源生态依赖**：Meta 将记忆层留给第三方框架（LangGraph、CrewAI、MindStudio），自身聚焦模型开源和推理基础设施（与 Cerebras 合作的 Llama API 达 2,600 tok/s）。

Meta 的策略可概括为**“模型能力开放，记忆体验由生态补齐”**。

---

### 4.7 Karpathy LLM Wiki：编译器模式的个人知识记忆

Andrej Karpathy（OpenAI 联合创始人、前 Tesla AI 总监）于 2026 年 4 月 3 日在 X 发布了一篇病毒式传播的帖子（1.2M+ 浏览），提出了一种全新的 Agent 记忆范式——**LLM Knowledge Bases**。这不是一个产品，而是一个工作流模式，但其影响力已迅速辐射到整个开发者社区。

#### 核心思想：LLM 作为知识编译器

Karpathy 的核心洞察是：**RAG（检索增强生成）对于个人规模的知识管理来说过于复杂**。传统 RAG 将文档切片为向量，每次查询时重新推导答案——这是"无状态"的。Karpathy 提出让 LLM 扮演**编译器**角色：

1. **读取**原始资料（`raw/` 目录中的论文、文章、代码、图片）。
2. **编译**为结构化 Wiki（`wiki/` 目录中的 Markdown 文件，含摘要、概念文章、反向链接）。
3. **维护**持续更新（定期"健康检查"或 linting，扫描不一致、填补缺失、发现新连接）。

> "Obsidian 是 IDE；LLM 是程序员；Wiki 是代码库。"
> —— Karpathy

结果是一个**持久化、可复利**的知识产物——跨引用已经存在，矛盾已经被标记——而非 RAG 那种每次查询都重新生成的瞬态答案。

#### 三层架构

| 层 | 内容 | 所有权 | 示例 |
|---|---|---|---|
| **raw/** | 原始资料（论文、文章、截图、数据集） | 用户收集，不可变 | Obsidian Web Clipper 抓取的网页 Markdown |
| **wiki/** | LLM 编译的结构化知识 | LLM 全权维护 | 概念文章、摘要、反向链接、索引文件 |
| **schema** | 结构规则（CLAUDE.md / AGENTS.md） | 用户定义，LLM 遵循 | "如何组织知识、何时创建新页面、链接规则" |

Karpathy 的个人研究 Wiki 已达约 **100 篇文章、400,000 词**（单主题）——比大多数博士论文还长，且他"很少手动编辑 Wiki；LLM 维护所有数据"。

#### 与 RAG 的根本区别

| 维度 | RAG | Karpathy LLM Wiki |
|---|---|---|
| **时间模式** | 查询时重新推导（无状态） | 编译一次，持续维护（有状态） |
| **知识形态** | 瞬态检索结果 | 持久化、可导航的知识库 |
| **跨引用** | 切片丢失文档级连接 | 单篇源文档可触及 10–15 个 Wiki 页面 |
| **可审计性** | 黑盒向量 embedding | 每句话都可追溯到具体 Markdown 文件 |
| **维护成本** | 低（自动索引） | 由 LLM 承担（对人类趋近于零） |
| **规模上限** | 无上限（数据库扩展） | ~1M 词以内（上下文窗口限制） |

#### 为什么这关乎 Agent 记忆

Karpathy 的 Wiki 模式与 OpenClaw/Hermes 的 Markdown-first 记忆哲学高度共鸣，但增加了一个关键维度：**LLM 不仅是记忆的使用者，更是记忆的作者和维护者**。

- OpenClaw 的 `MEMORY.md` 和每日笔记需要**用户手动编写**。
- Hermes 的 `MEMORY.md/USER.md` 需要**用户或 Skill 提取**更新。
- Karpathy Wiki 的**LLM 自动编译和 linting**将维护成本推向零。

这在哲学上回答了 Vannevar Bush 1945 年 Memex 愿景中"谁来维护扩展记忆？"的问题——**LLM 来做维护**。

#### 社区扩展与工具化

Karpathy 的帖子发布后，社区迅速涌现出多种实现：
- **Claude Code + Obsidian**：最直接的复刻，Claude 读取 Vault 并回答问题。
- **Keppi**：为 Obsidian Vault 构建可查询的知识图谱，解决 Wiki 规模扩大后的导航问题。
- **modular-context-obsidian-plugin**（76★）、**katmer-code**（349★）等插件。

#### 局限与边界

1. **规模天花板**：约 100 篇文章/40 万词是舒适区。超过 ~100 万词后，单次上下文加载太慢，需要引入语义搜索或 RAG。
2. **主题边界模糊**：Yu Wenhao 的批判分析指出，LLM 决定"哪些源文档合并到哪个 Wiki 页面"是临时决策，缺乏 Zettelkasten 原子笔记那样的清晰边界规则。
3. **依赖外部 LLM**：编译和 linting 需要调用云端模型，非完全离线。
4. **不是企业方案**：缺乏多用户、权限隔离、审计等企业功能。

---

## 5. 技术对比：存储、检索与压缩

### 5.1 存储技术栈

| 框架 | 主要存储 | 索引技术 | Embedding 依赖 | 本地离线能力 |
|---|---|---|---|---|
| OpenClaw | Markdown + SQLite | FTS5 + 向量（sqlite-vec） | 可选（本地 GGUF 或云端） | 完整（本地模型+本地 embedding） |
| Claude Code | Markdown 层级 | 无（LLM 扫描头） | 无 | 完整（记忆不依赖外部服务） |
| Codex CLI | Markdown | 无（grep） | 无 | 部分（Memories 生成需云端模型） |
| Hermes | Markdown + SQLite + 可选外部 DB | FTS5 + 可选向量/图谱/HRR | 可选（Holographic 零依赖） | 完整（内置系统完全本地） |

### 5.2 检索机制对比

- **OpenClaw**：混合语义搜索最全面，但需要配置 embedding 提供商。无提供商时降级为 BM25。
- **Claude Code**：LLM 扫描最“智能”但最贵（消耗 API tokens），且速度取决于模型响应时间。
- **Codex CLI**：grep 召回最简单、最确定，但无法处理语义变体（“deploy command” vs “ship to production”）。
- **Hermes**：FTS5 速度最快（113 ms vs OpenClaw 19,593 ms 在相同 300 事件基准），且通过插件可扩展到知识图谱（Hindsight）和分层加载（OpenViking）。

### 5.3 上下文压缩策略

| 框架 | 策略复杂度 | 缓存感知 | 独特机制 |
|---|---|---|---|
| Claude Code | ★★★★★（5 层） | 是（Prompt Cache 深度集成） | Microcompact 利用 cache_edits；私有草稿本技巧 |
| OpenClaw | ★★★☆☆（可插拔 + 预刷新） | 部分（Anthropic 原生 compaction 支持） | 压缩前自动提醒 Agent 保存记忆 |
| Hermes | ★★★☆☆（/compress + ByteRover 预提取） | 依赖模型提供商 | ByteRover 可在压缩前抢救信息 |
| Codex CLI | ★★☆☆☆（单层 handoff summary） | 否 | 最简化，用户消息原样保留 |

### 5.4 记忆更新策略对比

除了存储和检索，各框架在**何时记忆、如何更新、何时遗忘**这一时间维度上存在根本性分歧。基于对 Mem0、Hindsight、Honcho 等外部提供商与四大框架的对比分析，可归纳出六种更新策略范式：

| 框架/系统 | 更新触发器 | 合并策略 | 遗忘机制 | 核心权衡 |
|---|---|---|---|---|
| **OpenClaw** | Agent 自主判断 + heartbeat 定时扫描 | 手动蒸馏（每日笔记 → 长期 MEMORY.md） | Bootstrap 预算截断（文件仍在磁盘） | 人类式选择性记忆，但不稳定 |
| **Claude Code** | 上下文窗口压力（`contextWindow - 13K`） | 5 层渐进摘要 | 旧消息被总结后丢弃 | Token 效率最高，但每次压缩有损 |
| **Codex CLI** | 会话结束后 6 小时空闲 | LLM 提取 → 合并模型整合 | 30 天过期 + 256-rollout 上限 | 批处理高效，但崩溃前 6h = 记忆丢失 |
| **Mem0** | 实时（每轮 ADD/UPDATE/DELETE/NOOP） | 异步双模型合并 | 时效衰减 + 相关性评分 | 最细粒度控制，但 CRUD 开销大 |
| **Hindsight** | 每轮交互后（retain→recall→reflect） | 知识图谱增量更新 | 信念修正 + 冲突消解 | 关系最丰富，但计算成本高 |
| **Honcho** | 每轮持久化 + 辩证深度触发 | 冷/热提示合成 | 上下文节奏刷新 | 用户建模最深，但辩证轮增加延迟 |

**关键洞察**：记忆更新策略的选型取决于三个不可兼得的维度——**实时性**（Mem0/Honcho）、**崩溃韧性**（OpenClaw 文件持久）、**Token 效率**（Claude Code 压缩）。对于需要跨会话严格一致性的场景（金融、医疗），Codex CLI 的 6 小时冷却期是致命弱点；对于需要即时学习的场景（客服、个人助手），Mem0 的操作中心模式最优；对于长文档分析，Claude Code 的压缩管道在成本上无可匹敌。

### 5.5 云厂商与模型内记忆架构对比


开源框架与云厂商的记忆设计遵循完全不同的约束：前者追求**用户可控、可审计、可离线**，后者追求**跨设备同步、企业治理、零运维**。

| 维度 | 开源框架（OpenClaw/Hermes） | 云厂商（Microsoft/Google/Amazon） | 设备厂商（Apple/字节） | 原生模型（UI-TARS） |
|---|---|---|---|---|
| **存储位置** | 本地文件/SQLite | 云端托管数据库 | 设备端向量索引 | 模型参数内部 |
| **用户可控性** | 高（直接编辑 Markdown） | 中（UI 查看/删除，不可直接编辑底层） | 低（系统黑盒） | 极低（黑盒模型行为） |
| **跨设备同步** | 需自建（Git/云盘） | 原生（账户级） | 有限（iCloud/厂商云） | 依赖云端账户 |
| **企业治理** | 无（需自建） | 强（RBAC、审计、DLP） | 无 | 无 |
| **离线能力** | 完整 | 无（需联网） | 部分（检索可离线，推理需联网） | 需联网（模型在云端） |
| **记忆精度** | 依赖提取/向量化质量 | 依赖自动提取算法 | 依赖端侧 embedding 质量 | 依赖模型训练质量 |
| **延迟特征** | 本地 <1s（FTS5）到 ~20s（向量全量） | 云端 <500ms（但受网络影响） | 本地 <100ms（检索）+ 云端 RTT | 云端模型推理延迟 |
| **规模化成本** | 线性（本地磁盘/CPU） | 订阅制（按用户/按调用） | 硬件成本（换机） | API 调用成本 |

一个关键洞察是：**没有单一架构能同时满足“用户完全可控”“跨设备无缝同步”“完全离线”和“企业级治理”**。这解释了为什么市场同时存在开源框架、云服务和设备系统三种形态。

**补充：OpenViking 和 Karpathy Wiki 的差异化定位**

OpenViking 和 Karpathy LLM Wiki 不完全属于上述任何一列，而是**跨路线的中间层**：

- **OpenViking** 本质上是一个**可插拔的记忆基础设施**——它既可以被 OpenClaw/Hermes 这样的开源框架集成（作为外部提供商），也可以被云厂商的 Agent 服务用作底层上下文存储。它的文件系统范式比传统 RAG 更结构化，比纯 Markdown 记忆更高效（L0/L1/L2 分层），但 setup 成本高于简单向量数据库（需要 Go + C++ 编译器，依赖外部 LLM 生成摘要）。

- **Karpathy LLM Wiki** 则是一个**工作流范式**，不绑定任何特定工具。你可以用 Claude Code、Codex、Cursor 甚至 ChatGPT 来实现它。它的独特价值在于"知识复利"——每次查询的输出被重新归档到 Wiki 中，使知识库随使用而增长。这在传统 RAG 中是不可能发生的（RAG 的向量数据库只增不减，但不会自动产生新的综合知识）。Karpathy 模式的最大限制是规模（~1M 词上限），但在该范围内，它的信息密度和可审计性远超任何向量检索方案。

### 5.6 基准测试可信度全景

Agent 记忆领域的基准测试目前呈现**严重的可信度危机**。三大主流基准（LoCoMo、LongMemEval、BEAM）的测试协议互不兼容，而提供商的自报数字与独立复现之间存在巨大鸿沟。

| 基准 | 测试场景 | 领先分数（自报） | 领先分数（独立） | 关键局限 |
|---|---|---|---|---|
| **LoCoMo** | 35 会话跨会话一致性 | TiMem **75.30%** | Mem0 67.13% | 合成脚本，无时间衰减建模 |
| **LongMemEval** | 多天真实聊天场景 | Mem0 94.4% / 94.8% | **Hindsight 91.4%** (Gemini-3) / Mem0 49% | 主观评分， annotator 一致性差 |
| **BEAM** | 百万/千万 token 极端规模 | Mem0 94.4% (BEAM-1M) | 无公开独立复现 | 合成任务为主，非对话记忆 |

**最严重的可信度缺口**：Mem0 在 LongMemEval 上自报 94.4%，但独立研究者（S095）使用相同协议仅复现出 **49%**，差距 **45.4 个百分点**。LoCoMo 上自报 91.6% vs 论文复现 67.13%，差距 24.5pp。可能的原因包括：(1) 不同模型后端（GPT-4o vs 本地模型）；(2) 评分标准松紧不一；(3) 只报告最佳运行而非平均值；(4) 博客数字可能反映尚未发表论文的新版本。

**学术前沿的独立验证状态**：

| 架构 | LoCoMo | LongMemEval | 独立验证状态 |
|---|---|---|---|
| **TiMem** | 75.30% | 76.88% | ✅ 论文复现，可信 |
| **Hindsight** | — | 91.4% | ⚠️ 单一后端（Gemini-3），未跨模型测试 |
| **ByteRover** | — | — | ❌ 未在标准基准上评估 |
| **AtlasKV** | — | — | ❌ 未在标准基准上评估 |
| **LoCoMo/ST-Lite** | N/A | N/A | ✅ 训练自由，2.45× 加速可复现 |

**对读者的建议**：在评估记忆提供商时，优先参考**独立复现的论文数据**（TiMem、Hindsight 论文）而非博客营销数字；对于框架选型，应**自建任务集**在目标硬件上实测，而非依赖厂商宣称的基准分数。

---

## 6. 系统性能要求与硬件诉求

### 6.1 框架本体（编排层）—— 极轻量

以下数据为**仅运行 Agent 框架、调用云端 LLM API** 时的资源需求：

| 框架 | 最低 RAM | 推荐 RAM | 最低 CPU | 磁盘 | 运行时依赖 |
|---|---|---|---|---|---|
| **OpenClaw** | 2 GB | 4 GB | 2 核 | 20 GB SSD | Node.js 22.14+ |
| **Claude Code** | 4 GB | 8–16 GB | 任意现代 CPU | ~500 MB | 无（原生安装）或 Node.js |
| **Codex CLI** | 4 GB | 8 GB | 任意现代 CPU | ~50 MB + 会话数据 | Node.js 22+（或独立 Rust 二进制） |
| **Hermes Agent** | ~2 GB | 4 GB | 2 核 | ~1 GB + SQLite | Python 3.11+ |

关键结论：**四个框架的 Gateway/CLI 进程本身对芯片几乎零诉求**。OpenClaw Gateway 空闲 400–800 MB；Hermes 空闲 <512 MB；Codex 的 Rust 二进制体积极小；Claude Code 主要负载在云端。

### 6.2 本地 LLM 推理叠加——真正的硬件杀手

若要在同一台机器上运行本地模型（Ollama / vLLM / llama.cpp / SGLang），硬件需求呈指数级上升：

| 模型规模 | 量化 | 最低 RAM/VRAM | 推荐配置 | 适用芯片/设备 |
|---|---|---|---|---|
| 1.5B | Q4 | 4 GB RAM | 任意现代 CPU | 树莓派 5、旧办公机 |
| 7–8B | Q4 | 8 GB VRAM / 16 GB RAM | RTX 3060 / M4 16GB | 入门级 GPU、Mac Mini |
| 13–14B | Q4 | 12 GB VRAM / 32 GB RAM | RTX 4070 / M4 Pro 24GB | 中端 GPU、MacBook Pro |
| 30–32B | Q4 | 24 GB VRAM / 64 GB RAM | RTX 4090 / M4 Max 36GB | 高端 GPU、Mac Studio |
| 70B | Q4 | 48 GB VRAM / 128 GB RAM | 2×RTX 4090 / M4 Max 128GB | 多卡工作站、Mac Pro |

#### 对芯片的明确诉求
1. **无本地模型需求时**：
   - 任何支持对应操作系统（Linux/macOS/Windows）的 x86_64 或 ARM64 芯片均可。
   - Raspberry Pi 5（8 GB）、$60 旧办公机、$5/月 VPS 均可稳定运行。
   - **无需 GPU、NPU 或专用 AI 加速器**。

2. **有本地模型需求时**：
   - **NVIDIA GPU**：CUDA 生态最成熟，vLLM、TensorRT-LLM 支持最好。推荐 RTX 4070+ 用于 14B 模型，RTX 4090 用于 32B。
   - **Apple Silicon**：统一内存架构（UMA）允许 GPU 直接访问系统内存，无需 PCIe 拷贝。M4 Max（128 GB 统一内存，546 GB/s 带宽）是当前消费级运行 70B 模型的最佳选择。注意：**Neural Engine 对 LLM 推理几乎无帮助**，实际使用 Metal GPU Compute。
   - **AMD / Intel GPU**：通过 ROCm（AMD）或 OpenCL 可运行，但生态支持明显弱于 CUDA 和 Metal。
   - **专用边缘设备**：如 ClawBox（NVIDIA Jetson Orin Nano Super，67 TOPS）专为 OpenClaw 设计，但仅适合小模型（7B 以下）或 API 代理模式。

3. **浏览器自动化叠加**（OpenClaw 典型场景）：
   - 每个 Playwright/Chromium 实例额外消耗 200–400 MB RAM。
   - 推荐在生产环境为此预留 4–8 GB 额外内存。

### 6.3 端侧向量检索与云端 KV Cache 的硬件压力

除了本地 LLM 推理，两个新兴场景正在创造额外的硬件需求：

**端侧向量检索（Apple Intelligence / 豆包手机路线）**：
- 设备需要运行小型 embedding 模型（通常 100M–2B 参数）将个人数据实时向量化。
- Apple 的语义索引需要持续维护一个覆盖全设备数据的向量数据库（预估 10–100 MB 级，取决于数据量）。
- 对芯片的诉求：**NPU/GPU 用于快速 embedding 推理**，但 embedding 模型极小，现代手机 SoC（A17 Pro、骁龙 8 Gen 3 及以上）均可轻松胜任。

**云端 KV Cache（Google Gemini 2M 上下文路线）**：
- 1M token 的 KV Cache 约需 15 GB GPU 内存/用户（FP16）。2M token 约需 30 GB。
- Google 通过 Context Caching 和 MoE 稀疏激活缓解成本，但大规模部署仍是数据中心 HBM 容量的重要压力来源。
- 对芯片的诉求：**数据中心 GPU 的 HBM 容量和内存带宽**（H100/H200 的 80–141 GB HBM3e）；NVFP4 等 KV Cache 量化技术可将需求减半。

---

## 7. 安全与隐私考量

### 7.1 记忆存储安全

| 框架 | 存储加密 | Secret 处理 | 主要风险 |
|---|---|---|---|
| OpenClaw | 无默认加密 | 无内置脱敏 | CVE-2026-25253（CVSS 9.8）；明文 API 密钥和中间推理痕迹存于 Markdown/SQLite |
| Claude Code | 依赖 OS 磁盘加密 | 依赖用户不在 CLAUDE.md 中写密钥 | 项目级文件可被仓库共享，意外泄露风险 |
| Codex CLI | 依赖 OS 磁盘加密 | **内置 secret redaction**（记忆落盘前脱敏） | Memories 是生成状态，不建议手动编辑；地理可用性受限 |
| Hermes | 依赖 OS 磁盘加密 | 依赖用户配置 | Honcho 用户建模积累敏感偏好数据；AGPL 合规风险 |
| Google Astra | 云端加密（Google 标准） | 依赖 Google 账户安全 | 多模态记忆存储大量个人生活数据；Astra 仍为研究原型，安全审计未公开 |
| Microsoft Copilot | 企业级加密 + Purview 审计 | 租户级 DLP 策略 | 三域记忆增加数据泄露面；Entra Agent ID 是新攻击面 |
| Amazon Bedrock | AWS KMS 加密 | IAM + VPC 隔离 | 完全托管意味着用户失去对记忆存储的物理控制 |
| Apple Intelligence | 设备端加密 + PCC 密码学证明 | 无需上传原始数据 | 语义索引包含全部个人数据，但理论上不出设备；Siri 延期导致实际安全验证不足 |

### 7.2 记忆投毒（Memory Poisoning）

- **OpenClaw**：恶意 Skill（ClawHub 中被曝 26% 存在漏洞）可向向量数据库写入持久化后门规则，长期影响 Agent 行为。
- **所有框架**：通过提示注入（prompt injection）诱导 Agent 写入错误记忆是可行攻击面。OpenClaw 的 Providence Tags 和 Hindsight 的信任评分机制是少数主动缓解手段。
- **云厂商风险**：Trojan Hippo 攻击研究表明，对 Gemini-3.1-pro 的记忆投毒攻击成功率可达 100%（无防御时），对 GPT-5-mini 达 85%。持久化跨会话记忆越大，攻击面越广。

### 7.3 开源 vs 闭源：安全信任模型的结构性差异

Agent 记忆的安全态势不能脱离其开源/闭源属性单独评估。两者的信任模型存在根本分歧：

| 维度 | 开源（OpenClaw, Hermes, Mem0） | 闭源（Claude Code, Codex CLI, Apple Intelligence） |
|---|---|---|
| **代码可见性** | ✅ 完整源码可审计 | ❌ 二进制/API 黑盒 |
| **CVE 发现** | ✅ 公开披露（如 CVE-2026-25253） | ⚠️ 仅 vendor 自报，无公共数据库 |
| **安全补丁** | 社区驱动，用户自行更新 | Vendor 静默推送，用户无感知 |
| **信任模型** | "不信任，只验证" | "信任 vendor" |
| **数据可迁移性** | ✅ Markdown/SQLite 开放格式 | ⚠️ 专有格式或 API，迁移困难 |
| **责任归属** | 无 vendor 可追责 | 有 SLA 和企业支持 |

**关键洞察**：开源的透明性既是安全优势也是风险来源。OpenClaw 的 CVE-2026-25253 可以被社区快速分析和修复，但在补丁发布前漏洞细节完全公开，攻击者可利用。闭源系统（如 Claude Code）目前无已知 CVE，但这可能是"安全 through obscurity"——内部漏洞可能已被发现但未公开。Apple Intelligence 的 PCC 密码学证明是闭源系统中隐私架构的标杆，但用户仍无法独立验证实现是否正确。

### 7.4 按威胁模型的安全选型建议

| 威胁场景 | 最安全选择 | 理由 |
|---|---|---|
| **本地攻击者获取文件访问权限** | Codex CLI | 唯一内置 secret redaction，凭据不会落盘 |
| **网络侧数据外泄** | Hermes（纯本地模式） | 无云端遥测，Honcho 关闭后完全离线 |
| **记忆投毒 via 提示注入** | Codex CLI | Memories 为生成状态，非用户直接可编辑 |
| **供应链/提供商被攻破** | OpenClaw（无外部提供商） | 零外部依赖 = 零第三方攻击面 |
| **企业审计与合规** | Claude Code + Docker | 无已知 CVE，配合容器隔离可满足多数合规要求 |
| **隐私最大化（个人用户）** | Apple Intelligence | 语义索引不出设备，PCC 提供密码学级隐私保证 |

**全员裸奔的加密现状**：一个令人警醒的发现是——**四个主要开源框架均不提供默认的静态加密或内存加密**。OpenClaw 的明文 Markdown/SQLite、Claude Code 的用户级记忆文件、Hermes 的本地 SQLite、Codex CLI 的生成记忆，全部依赖 OS 级磁盘加密（BitLocker/FileVault/LUKS）作为最后一道防线。在共享机器、容器逃逸或冷启动攻击场景下，这是不够的。

---

## 8. 研究缺口与残余不确定性

1. **标准化基准缺失**：目前无统一基准在四框架+同一硬件+同一任务下测试记忆召回准确率与延迟。现有数据来自不同作者的独立测试（Regolo、EasyClaw、Business20Channel），硬件和模型 backend 不一致。**新增**：亦无统一基准对比开源框架与云厂商托管记忆（Copilot Memory vs Bedrock AgentCore Memory）的召回质量。
2. **Cloud Codex 记忆黑箱**：OpenAI 未公开云端 Codex 记忆的存储形态、保留期和配置接口，CLI 结论不能简单外推到云产品。
3. **营销数字待验证**：Skywork 等渠道宣称的“82% 运营成本降低”“63% 月度节省”、ByteDance M3-Agent 宣称的“96.7% 召回率”缺乏独立验证，未纳入核心结论。
4. **Claude Code 三层记忆 vs 四层 CLAUDE.md**：部分博客提到“三层记忆系统”，但最权威的 arXiv 论文（2604.14228）明确为 4 级 CLAUDE.md 层级 + auto-memory，存在术语混淆。
5. **长会话记忆漂移**：Hermes 被报告在 100+ 轮会话中出现相关性评分退化；OpenClaw 在 300 事件基准中召回延迟达 19.6 秒——尚不确定是典型行为还是未优化配置所致。
6. **本地模型性能与框架无关**：报告中所有“大内存/GPU”需求均来自模型推理层，而非 Agent 编排层。用户若始终使用云端 API，可完全忽略这些硬件诉求。
7. **美国厂商产品快速迭代**：Microsoft Copilot Memory（2025.07 GA）、Azure Foundry Agent Memory（Preview）、Amazon Bedrock AgentCore Memory（2026.02）、Apple Siri overhaul（延期至 2026 春）——这些产品发布时间接近，功能边界和成熟度变化快，结论可能迅速过时。
8. **Google Astra 存储后端未公开**：Astra 的持久记忆具体使用何种数据库、embedding 模型、检索机制，Google 未披露技术细节，现有分析基于 I/O 演示和产品描述推断。
9. **华为已排除**：应用户明确指令，本报告未包含华为任何产品线（盘古、鸿蒙 Next Agent 等）的记忆系统分析。
10. **OpenViking 生产验证不足**：OpenViking 2026 年初才开源，虽有 Red Hat 部署指南和学术案例分析，但缺乏大规模生产环境的独立基准测试。L0/L1 的 Token 节省效果高度依赖摘要质量和目录结构设计。
11. **Karpathy Wiki 规模边界模糊**：Karpathy 本人声明 ~400K 词是舒适区、~1M 词是上限，但未给出精确的方法论来确定"何时需要引入 RAG"。社区复刻的质量参差不齐，缺乏标准化 schema。
12. **OpenViking 与 UI-TARS 的协同未公开**：两者同属字节跳动生态，但公开文档未说明 UI-TARS 是否原生集成 OpenViking 作为外部记忆层，或豆包手机是否使用 OpenViking 作为本地向量后端。
13. **基准测试可信度危机缺乏系统性研究**：Mem0 的 45pp 差距并非孤例——整个记忆提供商行业缺乏独立的第三方审计机构（类似 MLPerf 的专门分支）。需要建立标准化的"记忆基准审计协议"，强制要求披露模型后端、评分标准、运行次数和置信区间。
14. **学术架构的生产验证严重不足**：ByteRover（RL 记忆操作）和 AtlasKV（参数化 KG）虽在概念上创新，但均未在 LoCoMo 或 LongMemEval 上评估，其实际效果完全未知。TiMem 的 SOTA 分数来自单一论文，尚未被独立复现。
15. **记忆更新策略的最优频率未量化**：实时更新（Mem0）vs 批处理合并（Codex CLI）vs 压缩驱动（Claude Code）之间的延迟/质量/成本权衡，目前没有任何公开研究给出量化的帕累托前沿。
16. **开源框架加密架构完全缺失**：四个主要开源框架均不提供默认静态加密，这不是设计疏忽而是架构空白。需要研究：在保持 Markdown/SQLite 可审计性的同时，如何实现对记忆文件的透明加密（如 age 或 SOPS 集成）。
17. **跨框架记忆迁移标准缺失**：不同框架使用互不兼容的记忆格式（OpenClaw 的 MEMORY.md、Claude Code 的 CLAUDE.md、Codex 的 AGENTS.md + Memories、Hermes 的 USER.md + SQLite）。用户更换框架时，历史记忆几乎无法无损迁移。
18. **多智能体共享记忆的冲突消解未解决**：当多个 Agent 同时写入同一记忆存储（Honcho 的多租户、Hindsight 的图谱更新）时，如何防止写冲突和信念矛盾？当前没有任何框架提供分布式事务或版本控制机制。

---

## 9. 结论与选型建议

### 9.1 按场景选型

| 场景 | 推荐框架 | 理由 |
|---|---|---|
| **多通道个人助手**（Telegram/Discord/Slack/WhatsApp） | OpenClaw 或 Hermes | OpenClaw 通道最多（22+），Hermes 记忆更深（FTS5 + 用户建模） |
| **专业编码 / 大型代码库重构** | Claude Code | 最强的上下文压缩管道和 Prompt Cache 集成，项目级 CLAUDE.md 层级精准 |
| **快速终端编码 + 极简运维** | Codex CLI | Rust 二进制极小，启动最快， Memories 自动生成减少手工维护 |
| **长期自治 / 自动学习工作流** | Hermes Agent | 唯一内置闭环学习（Skill 自生成、自优化），5 层记忆 + 8 个外部提供商 |
| **边缘 / 低功耗设备** | Hermes（Python 轻量）或 Codex（Rust） | 两者本体均 <512 MB–1 GB；OpenClaw Node.js 进程相对最重 |
| **完全离线 / 气隙环境** | Hermes 或 OpenClaw | 两者均支持本地模型 + 本地 embedding；Claude Code/Codex 默认依赖云端 |
| **GUI 自动化 / 手机 Agent** | 字节 UI-TARS / 豆包手机 | 原生模型内记忆 + 系统级屏幕理解；ScreenSpotPro 61.6% 准确率领先 |
| **企业级托管记忆 + 合规治理** | Microsoft Copilot / Azure Foundry | 三域记忆 + Entra Agent ID + Purview 审计 + 租户级 RBAC |
| **AWS 原生无服务器记忆** | Amazon Bedrock AgentCore | 完全托管 STM/LTM，50 行代码接入，与 Neptune/S3 Vectors 原生集成 |
| **隐私优先的个人设备智能** | Apple Intelligence | 设备端语义索引 + PCC 密码学隐私保证；敏感数据不出设备 |
| **超长文档分析（1M+ token）** | Google Gemini 2.5 Pro | 2M 原生上下文窗口 + Context Caching；减少 RAG 复杂度但 KV Cache 成本高 |
| **层级化上下文检索 + Token 节省** | OpenViking | L0/L1/L2 三层加载，目录递归检索，可视化轨迹调试；适合 10–1000 份文档的 Agent 记忆 |
| **个人知识复利（研究/学习）** | Karpathy LLM Wiki + Claude Code | LLM 编译器模式，零基础设施，Markdown 纯文本；适合 100–1000 篇笔记的个人知识管理 |
| **高安全性需求 / 密钥管理** | Codex CLI | 唯一内置 secret redaction，凭据不会明文落盘；配合 Docker 隔离可满足多数合规场景 |
| **企业知识库（海量文档）** | OpenViking 或 RAG + 向量数据库 | OpenViking 适合 10K 以下文档的层级检索；更大规模需传统 RAG（Milvus/Pinecone）或企业托管方案 |

### 9.2 硬件选型速查

| 部署模式 | 最低配置 | 舒适配置 | 备注 |
|---|---|---|---|
| 云端 API + 单 Agent | 2 核 / 2 GB RAM | 2 核 / 4 GB RAM | 树莓派、旧 PC、$5 VPS 均可 |
| 云端 API + 浏览器自动化 | 2 核 / 4 GB RAM | 4 核 / 8 GB RAM | 每个浏览器实例 +200–400 MB |
| 本地 7B 模型 + Agent | 4 核 / 16 GB RAM | 6 核 / 32 GB RAM | Apple Silicon 统一内存优势大 |
| 本地 14B 模型 + Agent | 8 核 / 32 GB RAM | 8 核 + RTX 4070 / M4 Pro | GPU 加速显著优于纯 CPU |
| 本地 70B 模型 + Agent | 16 核 / 128 GB RAM | RTX 4090×2 / M4 Max 128GB | 仅高端工作站或 Mac Studio |
| 云端 API + 端侧向量索引（豆包/Apple 路线） | 4 核 / 8 GB RAM | 6 核 / 16 GB RAM | 端侧负责 embedding 和检索，大模型在云端 |
| 企业托管记忆（Copilot/Bedrock） | N/A（纯云端） | N/A | 硬件需求由云厂商承担，客户端仅需浏览器/VS Code |

### 9.3 最终洞察

2026 年的 Agent 记忆系统正从“聊天记录”演进为**结构化、可检索、可审计的知识基础设施**。记忆架构呈现出**五条清晰的分化路线**：

**路线一：开源框架的“文件优先”本地记忆**（OpenClaw、Hermes、Claude Code、Codex CLI）。以 Markdown/SQLite 为底座，强调用户可控、可审计、可离线。OpenClaw 和 Hermes 代表了两种极端：前者是“Markdown 文件 + 混合语义搜索”的普适型架构，后者是“SQLite FTS5 + 插件化向量/图谱”的深度型架构。Claude Code 和 Codex CLI 则证明，对于编码场景，**极简的文件层级 + 确定性的压缩/召回** 往往比复杂的向量系统更实用。

**路线二：云厂商的“托管用户画像”记忆**（Microsoft Copilot、Google Astra、Amazon Bedrock）。以用户账户为中心，跨产品、跨会话持久化，强调企业治理和无缝同步。Microsoft 的三域记忆模型（User/Repository/Session）和 Amazon 的无服务器 STM/LTM 是当前最成熟的企业级方案。Google 则选择用 2M 超长上下文窗口“消化”记忆问题，减少对外部 RAG 的依赖——代价是单次预填充延迟和 KV Cache 内存开销。

**路线三：设备厂商的“端侧语义索引”记忆**（Apple Intelligence、字节豆包手机）。以设备为中心，敏感数据本地 embedding 和检索，复杂推理上云。Apple 的 Semantic Index 和 Private Cloud Compute 是当前隐私架构的标杆；字节豆包手机的“云端理解 + 本地向量检索”则代表了中国厂商在端云协同上的探索。

**路线四：原生 Agent 模型的“模型内记忆”**（ByteDance UI-TARS）。将工作记忆和情景记忆直接内置于模型架构中，通过训练而非外部数据库实现持久化。这是最具前瞻性但也最不可控的路线——用户无法像编辑 Markdown 文件那样直接干预模型记忆。

**路线五：层级化上下文数据库**（OpenViking）。以文件系统范式 `viking://` 替代扁平向量 RAG，通过 L0/L1/L2 三层加载实现**按需检索**。这不是传统的"记忆框架"，而是**记忆的基础设施层**——可被任何 Agent（OpenClaw、Hermes、自定义 Agent）集成。其可视化检索轨迹和目录递归机制，为 Agent 记忆的调试和优化提供了前所未有的可观测性。

**路线六：编译器模式工作流**（Karpathy LLM Wiki）。这不是产品，而是一种哲学——**LLM 作为知识编译器**，将原始资料一次性编译为持久化、可复利的 Markdown Wiki，持续维护而非每次查询重新推导。它代表了"文件即真相"路线的终极形态：LLM 不仅是记忆的使用者，更是记忆的作者和维护者。对于个人研究者和小团队，这可能是 2026 年性价比最高的 Agent 记忆方案。

对芯片厂商的启示：

1. **Agent 框架编排层本身不吃算力**——任何现代 CPU 均可运行。
2. **本地 LLM 推理是消费级硬件的第一驱动力**——7B 模型需 8–16 GB RAM，70B 需 48–128 GB + 高端 GPU。Apple Silicon 统一内存架构在此场景下优势显著。
3. **端侧向量检索正在兴起**——Apple 的语义索引和字节的本地 embedding 检索都需要设备端 NPU/GPU 进行快速 embedding 计算。虽然 Neural Engine 对 LLM 推理帮助有限，但对小批量 embedding 推理可能有用。
4. **云端 KV Cache 是数据中心的新压力点**——Google Gemini 的 2M 上下文意味着每用户 15–30 GB 的 KV Cache。这将推动 HBM 容量、内存带宽和 KV Cache 量化技术的持续投入。
5. **记忆检索的 Token 效率正在催生新的中间层**——OpenViking 的 L0/L1/L2 分层、Karpathy Wiki 的编译器模式、Claude Code 的 Prompt Cache，都在用不同方式解决同一个问题：如何在有限的上下文窗口内放入最有价值的记忆。这对上下文窗口硬件（更长、更便宜）和压缩算法都提出了持续需求。
6. **基准测试可信度危机要求芯片评估方法论革新**——当 Mem0 的自报数字与独立复现差距达 45pp 时，任何基于厂商基准的芯片选型决策都是不可靠的。芯片厂商应支持建立开源的、跨硬件的标准化记忆基准（类似 MLPerf 的记忆子集），而非依赖厂商自报数字。
7. **默认加密缺失创造新的安全芯片机会**——四个主要开源框架均不提供默认静态加密，这意味着在共享主机、边缘设备和云原生部署中，Agent 记忆文件是裸奔的。专用加密芯片（如 Apple Secure Enclave 的通用版）、透明文件系统加密（基于 TPM/TEE）可能成为 Agent 基础设施的下一个刚需。
8. **记忆更新策略的多样性否定了"通用记忆芯片"的可能性**——实时 CRUD（Mem0）、批处理合并（Codex CLI）、渐进压缩（Claude Code）、图谱更新（Hindsight）六种策略对存储 I/O 模式、延迟要求和一致性模型的需求完全不同。没有单一存储芯片或数据库架构能同时最优服务所有六种模式；Agent 记忆的硬件层将长期保持异构化。

---

*报告完成。基于 120 份阅读笔记与 177 页 Karpathy 风格 Wiki 知识体系更新。所有支撑材料见同目录下的 search-directions.md、reading-log.md、numeric-claims-ledger.md、scope-boundary-check.md、evidence-matrix.md、gap-audit.md。*

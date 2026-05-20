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

2026 年的主流 Agent 框架在记忆系统上呈现鲜明的架构分野：**文件即真相（file-as-source-of-truth）** 是开源框架的共同底座，而**云厂商则倾向于托管式用户画像 + 超长上下文窗口**的混合路线。本研究基于 120 份阅读笔记和 177 页 Karpathy 风格 Wiki 知识体系，对 28+ 技术的记忆子系统进行了深度审计。

**核心数据速览**：
- **检索延迟差距 173×**：同一场景下 Hermes FTS5 113 ms vs OpenClaw 向量全量 19,593 ms [[S136]](wiki/sources/S136.md)
- **记忆召回差距 28pp**：Hermes 89% vs OpenClaw 61%（跨会话，session 2）[[S137]](wiki/sources/S137.md)
- **多智能体协调差距 17pp**：Hermes 98.2% vs OpenClaw 81.4%（4 agents）[[S028]](wiki/sources/S028.md)
- **基准可信度危机 45pp**：Mem0 自报 LongMemEval 94.4% vs 独立复现 49% [[S078]](wiki/sources/S078.md) [[S095]](wiki/sources/S095.md)
- **全员裸奔**：四个主要开源框架均不提供默认静态加密 [[wiki/comparisons/framework-security-comparison.md]](wiki/comparisons/framework-security-comparison.md)
- **唯一安全亮点**：Codex CLI 是唯一内置 secret redaction 的框架 [[S010]](wiki/sources/S010.md)

**框架速览**：

- **OpenClaw**：Markdown + SQLite 混合检索（0.7×向量 + 0.3×BM25），7 种 embedding 提供商，22+ 消息通道。功能丰富但延迟高（19.6s）、安全漏洞严重（CVE-2026-25253，CVSS 9.8）[[S131]](wiki/sources/S131.md)。适合多通道个人助手。
- **Claude Code**：4 层 CLAUDE.md + 5 层渐进压缩管道，Prompt Cache 感知设计节省 API 成本达 90% [[S007]](wiki/sources/S007.md)。最"项目级"的记忆设计，适合专业编码。无已知 CVE 但闭源不可审计。
- **Codex CLI**：极简两层记忆（AGENTS.md 32 KiB + Memories），~50 MB 包体，唯一内置 secret redaction [[S010]](wiki/sources/S010.md)。适合快速终端编码和高安全性场景。Memories 在 EEA/UK/CH 不可用。
- **Hermes Agent**：5 层记忆 + 8 个外部提供商，FTS5 检索 10 ms（万级文档），多智能体协调 98.2% [[S028]](wiki/sources/S028.md)。插件化架构最灵活，但 Honcho 激活时上传完整对话至第三方服务器 [[S143]](wiki/sources/S143.md)。适合长期自治和自动学习。
- **字节 UI-TARS / 豆包 / OpenViking**：三条并行路线覆盖全栈。UI-TARS 模型内记忆 ScreenSpotPro 61.6% 领先 [[S046]](wiki/sources/S046.md)；豆包端云协同；OpenViking 上下文数据库 L0/L1/L2 分层节省 Token 60–80%。
- **美国厂商**：Google 2M 上下文窗口（KV Cache ~15GB/用户）[[S050]](wiki/sources/S050.md)；Microsoft 三域托管记忆 + Purview 审计（企业治理最强）；Amazon Bedrock 50 行代码接入 + S3 Vectors 90% 成本降低；Apple PCC 密码学隐私保证但 Siri AI 化延期；Meta 最保守（10M 上下文但无记忆产品）。
- **Karpathy LLM Wiki**：编译器模式工作流，~100 篇/40 万词验证 [[S141]](wiki/sources/S141.md)。不是产品而是哲学——LLM 作为知识编译器维护个人 Wiki。适合研究者和小团队。

**关键发现**：

1. **基准测试可信度危机**：Mem0 45pp 差距暴露了整个行业缺乏标准化审计。目前最可信数据来自 TiMem（75.30% LoCoMo）和 Hindsight（91.4% LongMemEval），但两者未直接对决 [[S120]](wiki/sources/S120.md) [[S015]](wiki/sources/S015.md)。
2. **学术前沿四条路线**：ByteRover（RL 记忆操作，152 训练对）、TiMem（时序记忆树，52.20% 召回长度缩减）、LoCoMo/ST-Lite（训练自由 KV Cache 压缩，2.45× 加速）、AtlasKV（参数化十亿级 KG，<20GB VRAM）[[S090]](wiki/sources/S090.md) [[S117]](wiki/sources/S117.md) [[S119]](wiki/sources/S119.md)。
3. **六种记忆更新策略构成不可能三角**：实时性（Mem0）vs 崩溃韧性（OpenClaw 文件持久）vs Token 效率（Claude Code 压缩）不可兼得。
4. **安全全员裸奔**：四个开源框架无默认加密；Codex CLI 唯一 secret redaction；Honcho 上传完整对话流（S076）；Apple PCC 密码学证明但无法独立验证实现。
5. **硬件两极分化**：编排层几乎零算力（树莓派即可）；本地 70B 模型需 48–128 GB RAM 或 M4 Max 128GB。Apple Silicon UMA 是端侧大模型的游戏规则改变者 [[S139]](wiki/sources/S139.md)。
6. **成本拐点**：本地 7B 模型 $800 一次性投入，6 个月即比云端 API（$200/月）更经济。

---

## 2. 研究方法与信息源

### 核心判断

本研究采用**双轨方法论**：第一轨遵循深度搜索材料技能（Deep Research Search Materials）进行系统性文献搜集与筛选；第二轨构建 Karpathy 风格的结构化知识库（LLM Wiki），将 120 份阅读笔记编译为 177 页可复利、可审计、可溯源的知识体系。这种"搜索 + 编译"双轨模式确保了证据的广度（覆盖 28+ 技术）和深度（每来源 7 维度结构化分析）。

---

### 搜索阶段

- **搜索方向**：18 个独立方向，涵盖核心架构、压缩策略、向量检索、硬件部署、多智能体共享、安全漏洞、竞争对比、学术前沿、字节跳动 UI-TARS/Seed-TARS、Google Astra/Gemini、Microsoft Copilot/Azure、Meta/Amazon/Apple 记忆系统，以及外部记忆提供商（Mem0、Hindsight、Honcho、Supermemory 等）深度评估。
- **候选池规模**：搜索并筛选了 150+ 来源，最终保留 **120 条**进入 reading log，全部完成结构化阅读笔记（reading-notes/S001–S120.md）。
- **来源分级**：
  - **一级来源**（优先采用）：官方文档、arXiv 论文（2604.14228、2603.27517、2603.12644、2502.07938 等）、逆向工程源码分析报告
  - **二级来源**（交叉验证使用）：技术博客、社区基准（Regolo、EasyClaw、Business20Channel）、产品公告
  - **三级来源**（标注待验证）：营销类幻灯片（Skywork"82% 成本降低"）、厂商博客宣称（Mem0 94.4% LongMemEval）——这些数字在正文中单独标注可信度状态，未纳入核心结论
  - **独立基准复现**：S095（Mem0 LongMemEval 49% 独立复现）作为关键可信度校验

---

### 知识体系构建阶段

基于 120 份阅读笔记编译了 **177 页的 Karpathy 风格 LLM Wiki**，包含：

| 组件 | 数量 | 内容 |
|---|---|---|
| **源页面（sources/）** | 120 | 每份阅读笔记的结构化摘要（核心声明、方法、关键证据、局限性、相关性、交叉引用、个人注释） |
| **实体页面（entities/）** | 22 | OpenClaw、Claude Code、Codex CLI、Hermes、Mem0、Hindsight、Honcho、ByteRover、UI-TARS、OpenViking、TiMem、AtlasKV 等技术实体 |
| **概念页面（concepts/）** | 10 | hybrid-search、context-compaction、episodic-memory、file-based-memory 等跨实体概念 |
| **对比页面（comparisons/）** | 16 | 框架对比、提供商对比、云厂商对比、安全对比、开源/闭源对比等 |
| **导航地图（maps/）** | 6 | 框架分类学、硬件需求矩阵、基准可信度地图等 |
| **Schema 文件（CLAUDE.md）** | 1 | 定义 Wiki 目录结构、命名约定、链接规范的元数据标准 |

**Wiki 工作流**：原始资料 → 结构化阅读笔记（reading-notes/S0xx.md，7 维度模板） → 编译 Wiki（wiki/sources/S0xx.md 自动聚合） → 可维护 Schema（CLAUDE.md 人工定义）。

这种模式的独特价值在于**知识复利**：每次新增来源时，Wiki 自动更新相关实体页面、概念页面和对比页面中的交叉引用，使知识库随使用而增长——这与传统 RAG 的"只增不减但不产生新综合知识"形成对比。

---

### 审计与验证

- **Evidence Matrix**：为每个核心声明标注来源 ID、直接/推断、是否已在报告中引用。见 `evidence-matrix.md`。
- **Numeric Claims Ledger**：为所有量化声明建立台账，记录数值、指标、来源、直接/推断、已引用状态。见 `numeric-claims-ledger.md`。
- **Gap Audit**：系统识别 18 个研究缺口，按紧迫性分类。见 `gap-audit.md`。
- **PDF 内容校验**：120 份来源中，118 份 PDF/网页内容与预期一致；**2 份存在内容不匹配**：
  - S003/S004（OpenClaw 安全分析）：arXiv ID 错误。S003 实际为 MIT 阅读时间论文（2603.09872），S004 实际为 Mpemba effect 论文（2603.04567）。已用 S131–S133 替代
  - S062（移动 GUI Agent 记忆调查）：下载的 PDF 为音乐生成 HCI 论文，已标记为红色警戒

---

### 数据来源分布

| 来源类型 | 数量 | 占比 | 典型示例 |
|---|---|---|---|
| 官方文档 | 28 | 23% | OpenClaw docs、Hermes docs、OpenAI Codex docs |
| arXiv 论文 | 22 | 18% | 2604.14228（Claude Code）、2502.07938（TiMem） |
| 技术博客/调查 | 35 | 29% | CrabTalk、Vectorize、Business20Channel |
| 产品公告/新闻 | 20 | 17% | Google I/O、Microsoft Build、AWS re:Invent |
| 社区 issue/审计 | 8 | 7% | Hermes GitHub #4074（Honcho 隐私） |
| 独立基准 | 7 | 6% | Regolo、EasyClaw、S095（Mem0 复现） |

---

### 参考文献

- `search-directions.md` — 18 个搜索方向的详细规划
- `reading-log.md` — 120 条来源的完整目录
- `evidence-matrix.md` — 核心声明的证据矩阵
- `numeric-claims-ledger.md` — 量化声明台账
- `gap-audit.md` — 研究缺口审计
- `wiki/index.md` — 177 页 Wiki 的全文导航

## 3. 核心发现：四大框架记忆架构总览

### 核心判断

2026 年的 Agent 记忆系统呈现**六条清晰的分化路线**，覆盖从个人设备到数据中心、从开源框架到云服务的完整光谱。没有单一架构能在所有维度上占优——选型必须基于场景约束匹配而非基准分数。

| 维度 | OpenClaw | Claude Code | Codex CLI | Hermes Agent | 字节 UI-TARS/豆包 | Google Astra/Gemini | Microsoft Copilot | Apple Intelligence |
|---|---|---|---|---|---|---|---|---|
| **记忆哲学** | 文件即真相 + 结构化长期记忆 | 项目级指令层级 + 渐进压缩 | 静态指令 + 自动生成摘要 | 多层持久记忆 + 自主技能进化 | 原生模型内分层记忆 + 端云协同 | 超长上下文 + 多模态个人记忆 | 三域托管记忆 + 企业治理 | 设备端语义索引 + 隐私优先 |
| **长期存储格式** | MEMORY.md + 每日笔记 + DREAMS.md | CLAUDE.md（4 层层级） | AGENTS.md（32 KiB 上限）+ Memories 目录 | MEMORY.md/USER.md + SQLite FTS5 + Skills | 云端情景记忆 Et + 本地向量库 | Gemini 上下文缓存 + Astra 交互历史 | User/Repository/Session 三级存储 | 设备端语义索引（向量 DB） |
| **检索机制** | 混合搜索：0.7×向量 + 0.3×BM25 + MMR + 30 天衰减 | LLM 扫描文件头 + grep | 全文加载 summary + grep 细节 | FTS5 全文检索 + 外部向量/图谱提供商 | 本地向量检索（embedding） | 注意力机制全上下文 + 工具检索 | 语义相似度 + 作用域过滤 | 语义索引 + App Intents 匹配 |
| **上下文压缩** | 可插拔压缩器 + Pre-compaction Flush（4000 tokens 阈值） | 5 层渐进压缩（预算→截断→微压缩→折叠→自动压缩） | 单层 handoff summary（6h 合并延迟） | /compress 命令 + ByteRover 预压缩提取 | 模型内语义压缩（Et） | 2M 原生上下文窗口 + KV Cache | 意图驱动存储 + 自动摘要 | 设备端 3B 模型 + PCC 升级 |
| **跨会话持久** | 是（文件天然持久） | 部分（依赖 CLAUDE.md 或 auto-memory） | 是（Memories 后台合并） | 是（SQLite + 文件 + 外部提供商） | 是（云端持久 + 本地向量） | 是（Google 账户级） | 是（Microsoft 账户级） | 是（iCloud 同步语义索引） |
| **团队共享** | 可通过仓库共享 AGENTS.md | 可通过仓库共享 CLAUDE.md | 不支持（Memories 单用户本地） | 可通过 Hindsight Cloud / RetainDB 共享 | 否（个人设备级） | 有限（家庭/工作空间） | 是（租户级 + 共享会话） | 否（严格个人设备） |
| **本地 embedding** | 支持（node-llama-cpp GGUF ~0.6 GB） | 无（记忆不依赖向量） | 无（记忆不依赖向量） | 支持（Holographic 零依赖 SQLite） | 支持（本地 embedding 模型） | 否（云端） | 否（云端） | 是（设备端 Core ML） |
| **运行时/部署** | Node.js 22+ 本地进程 | Shell + Node 本地进程 | Rust 二进制本地运行 | Python 3.11+ 本地进程 | 云端大模型 + 本地 Agent 运行时 | 云端 Gemini API | 云端 M365/Azure + VS Code 本地缓存 | 设备端 AFM + PCC 服务器 |
| **空闲内存** | 400–800 MB（Gateway） | ~300–500 MB | ~50 MB 包体 | <512 MB | N/A（模型级） | N/A（云端） | N/A（云端） | N/A（系统级） |
| **典型延迟** | 19.6s（300 事件向量全量） | 取决于模型响应（1–5s） | <100ms（本地文件读取） | 10ms（万级 FTS5）→ 113ms（基准） | 云端模型推理延迟 | 云端 <500ms + 网络 RTT | 云端 <500ms + 网络 RTT | 本地 <100ms（检索）+ 云端 RTT |
| **安全态势** | CVE-2026-25253（CVSS 9.8）；明文 secrets | 无已知 CVE；闭源不可审计 | 唯一内置 secret redaction | Honcho 上传完整对话（S076） | 端云协同，敏感数据本地 | 云端加密；Astra 审计未公开 | Purview 审计 + 租户 DLP | PCC 密码学证明；Siri 延期 |

**关键数据速览**：

| 指标 | 最佳表现者 | 数值 | 来源 |
|---|---|---|---|
| 检索延迟（300 事件） | Hermes（FTS5） | **113 ms** | [[S136]](wiki/sources/S136.md) |
| 检索延迟（300 事件） | OpenClaw（向量全量） | 19,593 ms | [[S136]](wiki/sources/S136.md) |
| 跨会话记忆召回 | Hermes | **89%**（session 2） | [[S137]](wiki/sources/S137.md) |
| 跨会话记忆召回 | OpenClaw | 61%（session 2） | [[S137]](wiki/sources/S137.md) |
| 多智能体协调成功率 | Hermes | **98.2%**（4  agents） | [[S028]](wiki/sources/S028.md) |
| 多智能体协调成功率 | OpenClaw | 81.4%（4 agents） | [[S028]](wiki/sources/S028.md) |
| 上下文压缩层数 | Claude Code | **5 层** | [[S007]](wiki/sources/S007.md) |
| Secret 保护 | Codex CLI | **内置 redaction** | [[S010]](wiki/sources/S010.md) |
| 包体大小 | Codex CLI | **~50 MB** | [[S144]](wiki/sources/S144.md) |
| 外部记忆提供商数 | Hermes | **8 个** | [[S013]](wiki/sources/S013.md) |
| GUI 定位准确率 | UI-TARS-1.5 | **61.6%** ScreenSpotPro | [[S046]](wiki/sources/S046.md) |
| 上下文窗口上限 | Google Gemini | **2M tokens** | [[S050]](wiki/sources/S050.md) |
| 企业治理 | Microsoft Copilot | **Purview + RBAC + DLP** | 产品文档 |

---

### 六条分化路线

基于上述对比，2026 年 Agent 记忆系统呈现六条清晰的分化路线：

**路线一：开源框架的"文件优先"本地记忆**（OpenClaw、Hermes、Claude Code、Codex CLI）。以 Markdown/SQLite 为底座，强调用户可控、可审计、可离线。OpenClaw 和 Hermes 代表了两种极端：前者是"Markdown 文件 + 混合语义搜索"的普适型架构，后者是"SQLite FTS5 + 插件化向量/图谱"的深度型架构。

**路线二：云厂商的"托管用户画像"记忆**（Microsoft Copilot、Google Astra、Amazon Bedrock）。以用户账户为中心，跨产品、跨会话持久化，强调企业治理和无缝同步。

**路线三：设备厂商的"端侧语义索引"记忆**（Apple Intelligence、字节豆包手机）。以设备为中心，敏感数据本地 embedding 和检索，复杂推理上云。

**路线四：原生 Agent 模型的"模型内记忆"**（ByteDance UI-TARS）。将工作记忆和情景记忆直接内置于模型架构中，通过训练而非外部数据库实现持久化。

**路线五：层级化上下文数据库**（OpenViking）。以文件系统范式 `viking://` 替代扁平向量 RAG，通过 L0/L1/L2 三层加载实现按需检索。

**路线六：编译器模式工作流**（Karpathy LLM Wiki）。LLM 作为知识编译器，将原始资料一次性编译为持久化、可复利的 Markdown Wiki。

---

### 参考文献

- [[S007]](wiki/sources/S007.md) Claude Code 压缩管道（arXiv 2604.14228）
- [[S010]](wiki/sources/S010.md) Codex CLI 记忆机制
- [[S013]](wiki/sources/S013.md) Hermes 8 个外部记忆提供商
- [[S144]](wiki/sources/S144.md) Codex CLI 包体与资源
- [[S137]](wiki/sources/S137.md) EasyClaw: OpenClaw vs Hermes 同任务基准
- [[S136]](wiki/sources/S136.md) Regolo: 延迟与磁盘对比
- [[S028]](wiki/sources/S028.md) Business20Channel: 多智能体协调基准
- [[S046]](wiki/sources/S046.md) UI-TARS-1.5 能力分析
- [[S050]](wiki/sources/S050.md) Google Gemini 2M 上下文

## 4. 分框架深度解析

### 0. 判断表

| 框架 | 核心判断 | 关键支撑数据 | 证据强度 |
|---|---|---|---|
| **OpenClaw** | 混合搜索架构在功能丰富度上领先，但延迟和安全性是明显短板 | 19.6s 召回延迟；CVSS 9.8；ClawHub 26.1% Skill 漏洞率 [[S135]](wiki/sources/S135.md) | 强（S027 同基准；S131–S133 框架漏洞 / S135 SkillSieve 供应链安全） |
| **Claude Code** | 5 层渐进压缩管道是当前 Token 效率最优的编码 Agent 记忆方案 | 工具预算 50K/200K；13K 阈值；Prompt Cache 90% 成本降低 | 强（S007 arXiv 论文；S008 社区分析） |
| **Codex CLI** | 以极简主义换取确定性和安全性，是唯一内置 secret redaction 的框架 | 32 KiB 上限；6h 合并；30 天 age-out；~50 MB 包体 | 强（S010 OpenAI 文档；S013 逆向工程） |
| **Hermes Agent** | 插件化记忆架构提供最大灵活度，但引入大量外部依赖和攻击面 | 5 层记忆；8 提供商；FTS5 10ms；多智能体协调 98.2% | 强（S016 调查；S026/S028 基准） |
| **字节 UI-TARS** | 原生 Agent 模型路线将记忆内置于模型参数，最具前瞻性但最不可控 | ScreenSpotPro 61.6% vs Claude 27.7%；$0.12/1K 操作 | 中（S046 行业分析；官方技术报告） |
| **OpenViking** | 上下文数据库以层级文件系统替代扁平 RAG，Token 节省 60–80% | 6.3K stars；L0/L1/L2 分层；可视化检索轨迹 | 中（Red Hat 部署指南；GitHub 数据） |
| **Google** | 用 2M 超长上下文"消化"记忆问题，代价是基础设施成本 | 2M token ≈ 1.4M 词；1M KV Cache ~15GB；2M 预填充 >2min | 强（S049/S050 官方文档） |
| **Microsoft** | 三域托管记忆 + 企业治理是当前最完整的企业级方案 | User/Repository/Session 三级；Purview 审计；Entra Agent ID | 中（产品公告；官方文档） |
| **Amazon** | 无服务器 STM/LTM 将记忆基础设施化，50 行代码接入 | Neptune + ElastiCache + S3 Vectors；宣称 90% 存储成本降低 | 中（AWS 官方文档） |
| **Apple** | 设备端语义索引 + PCC 是当前隐私架构的标杆，但 Siri AI 化延期 | 3B AFM 设备端；PCC 密码学可验证隐私；Siri 延期至 2026 春 | 中（WWDC 公告；产品状态） |
| **Meta** | 最保守——10M 上下文能力开放，但无持久记忆产品 | LLaMA 4 10M token；2,600 tok/s（Cerebras 合作）；记忆层留给生态 | 弱（第三方框架数据；官方未披露记忆产品） |
| **Karpathy Wiki** | 不是产品而是工作流哲学，LLM 作为知识编译器维护个人 Wiki | ~100 篇/40 万词验证；社区复刻 76★–349★；~1M 词上限 | 中（Karpathy X 帖子；社区项目数据） |

---

### 1. 核心判断

Agent 框架的记忆设计差异根植于**三个不可调和的架构张力**：

1. **透明度 vs 性能**：人类可编辑的 Markdown 文件（OpenClaw、Karpathy Wiki）提供了 Git-friendly 的可审计性，但检索延迟比预索引数据库高 1–2 个数量级。SQLite FTS5（Hermes）在 10,000 文档下仅需 ~10 ms [[S016]](wiki/sources/S016.md)，而 OpenClaw 的 JSONL 全量回注在 300 事件下耗时 19.6 秒 [[S136]](wiki/sources/S136.md)。

2. **功能丰富度 vs 攻击面**：Hermes 的 8 个外部记忆提供商（Honcho、Mem0、Hindsight 等）提供了从用户建模到知识图谱的全谱系能力 [[S013]](wiki/sources/S013.md)，但每个提供商都引入了独立的信任边界和潜在漏洞。OpenClaw 的单一后端架构更简单，但缺乏深度用户建模能力。

3. **用户可控性 vs 智能自动化**：OpenClaw 的 Agent 自主判断写入给予用户最大的干预空间（直接编辑 Markdown），但写入质量不稳定；Claude Code 的 5 层自动压缩确保了长会话的 Token 效率，但用户无法直接干预压缩过程，原始细节永久丢失 [[S007]](wiki/sources/S007.md)。

云厂商和设备厂商则在这三个张力之外增加了第四个维度：**隐私 vs 跨设备同步**。Apple 的 Semantic Index 将敏感数据完全留在设备端，但无法像 Microsoft Copilot 那样跨设备无缝同步用户画像。

---

### 4.1 OpenClaw

#### 核心判断
OpenClaw 的混合搜索架构在功能丰富度上领先开源框架，但**延迟和安全性是明显短板**。其"文件即真相"哲学提供了最高的人类可审计性，但 19.6 秒的召回延迟和 CVE-2026-25253（CVSS 9.8）的安全漏洞使其不适合对延迟和安全性敏感的生产环境。

#### 架构概览
OpenClaw 是一个本地优先（local-first）的持久型 Agent 框架，以 Node.js Gateway 进程为中心，通过 WebSocket 管理会话、通道和工具调用。其记忆系统的核心设计是**明文 Markdown 文件作为唯一真相源**，所有索引（SQLite、向量）均为派生。

Gateway 进程空闲时占用 400–800 MB RAM [[S138]](wiki/sources/S138.md)，对 Node.js 22+ 有硬性要求。基础安装大小约 2–3 GB，在中等活跃度下日志增长约 1–3 GB/月 [[S138]](wiki/sources/S138.md)。

#### 记忆文件层级
1. **MEMORY.md**：精简的常青知识（偏好、决策、设计规则），在每个 DM 会话启动时注入系统提示词。若文件超过 bootstrap 预算，OpenClaw 保留磁盘上的完整文件，但截断注入上下文的副本——这被视为信号，提示用户将详细材料移回 `memory/*.md` 或提高预算限制 [[S001]](wiki/sources/S001.md)。
2. **memory/YYYY-MM-DD.md**：每日工作层，记录当天纪要、临时决策、会议记录。今天和昨天的笔记自动加载，slugged 变体（如 `/new` 或 `/reset` 触发的会话记忆）也会被拾取。不默认注入提示词，而是通过 `memory_search` / `memory_get` 按需检索 [[S001]](wiki/sources/S001.md)。
3. **DREAMS.md**（可选）：dreaming 后台整合的摘要，供人工审查，包括基于历史回填的 grounded entries。
4. **Commitments**（隐藏）：短期承诺的 opt-in 跟进记忆，Agent 在后台推断，限定在相同 Agent 和通道范围内，通过 heartbeat 交付到期检查 [[S001]](wiki/sources/S001.md)。

#### 检索引擎：Builtin Memory Engine
默认后端为 SQLite，具备三层检索能力：

- **FTS5 全文索引**：BM25 评分，支持 CJK trigram 分词。
- **向量搜索**：通过外部或本地 embedding 提供商生成向量，存储于 SQLite（可选 sqlite-vec 加速）。
- **混合搜索**：`finalScore = 0.7 × vectorScore + 0.3 × textScore`，并支持 MMR（Max Marginal Relevance，λ=0.7）以保证结果多样性，以及 30 天半衰期的时间衰减 [[S005]](wiki/sources/S005.md)。

**索引参数细节** [[S006]](wiki/sources/S006.md)：

| 参数 | 值 | 含义 |
|---|---|---|
| Chunk target | 400 tokens | 文档切片目标大小 |
| Chunk overlap | 80 tokens | 切片间重叠，防止上下文断裂 |
| Snippet max | 700 chars | `memory_search` 单条返回上限 |
| Embedding batch | 8000 tokens | 单次 API 嵌入批处理上限 |
| Concurrency | 4 | 并行嵌入请求数 |
| Decay half-life | 30 days | 时间衰减半衰期 |
| Cache max | 50,000 entries | 嵌入缓存条目上限 |

**文件监控**：1.5 秒防抖（debounce）的增量重索引 [[S005]](wiki/sources/S005.md)。当用户直接编辑记忆文件时，索引在 1.5 秒后自动更新，无需重启 Gateway。

#### Embedding 提供商链
自动检测优先级：本地 GGUF（如 embedding-gemma-300M，~0.6 GB）→ OpenAI → Gemini → Voyage → Mistral → DeepInfra → Ollama。若全部失败，优雅降级为纯 BM25 关键词搜索 [[S005]](wiki/sources/S005.md)。

**本地 vs 云端 embedding 的延迟差距**：根据社区基准测试，llama.cpp GPU 本地嵌入延迟约 4 ms（nomic-embed-text-v2-moe 768d），Ollama CPU 本地嵌入约 61 ms，OpenAI 云端 API 约 200 ms [[coolmanns repo]](wiki/sources/S005.md)。对于高频记忆写入场景（如每轮交互都更新向量），本地嵌入的成本优势显著。

#### 记忆刷新与 Dreaming
- **Pre-compaction Flush**：在上下文压缩前，系统会先发一个静默回合提醒 Agent 将重要信息写入记忆文件，防止压缩导致信息丢失。软阈值：4000 tokens 或 2 MB 转录文件 [[S006]](wiki/sources/S006.md)。
- **Dreaming**（默认关闭）：后台 cron 任务收集短期信号，通过评分、回忆频率和查询多样性门槛，将合格条目从短期记忆提升为长期 MEMORY.md。

#### 记忆 Wiki 插件
`memory-wiki` 插件将持久记忆编译为带有来源标记（Providence Tags：Observed / User-Confirmed / Model-Inferred）的知识库，防止"记忆淤泥（memory sludge）"——即未经甄别的低质量记忆累积 [[S001]](wiki/sources/S001.md)。这实际上是在 OpenClaw 内部实现了一个轻量级的 Karpathy Wiki 模式。

#### 性能与扩展

**延迟基准** [[S136]](wiki/sources/S136.md) [[S137]](wiki/sources/S137.md)：

| 场景 | OpenClaw | Hermes（对比） | 差距 |
|---|---|---|---|
| 召回延迟（300 事件） | **19,593 ms** | 113 ms | OpenClaw 慢 173× |
| 简单任务延迟（Llama 3.1 70B） | **1.4 s** | 1.9 s | OpenClaw 快 26% |
| 多步研究延迟 | **4.1 s** | 5.3 s | OpenClaw 快 23% |
| 10 步流水线延迟 | 5.9 s | **4.2 s** | OpenClaw 慢 40% |
| 跨会话记忆召回（session 2） | **61%** | **89%** | Hermes 高 28pp |
| 4 智能体协调成功率 | 81.4% | **98.2%** | Hermes 高 17pp |
| 磁盘增长（300 事件） | **+213.41 KB** | **+0.00 KB** | OpenClaw 累积增长 |

**关键洞察**：OpenClaw 在简单任务上更快（1.4s vs 1.9s），但在记忆召回质量上显著落后（61% vs 89%）。这表明 OpenClaw 的轻量级架构牺牲了记忆系统的深度——它的 JSONL 全量回注策略虽然简单直接，但缺乏预索引结构化的语义组织能力。对于需要跨会话严格一致性的场景（如多智能体协调），OpenClaw 的 81.4% 成功率远低于 Hermes 的 98.2% [[S028]](wiki/sources/S028.md)。

**安全风险**：OpenClaw 存在已知 CVE-2026-25253（CVSS 9.8），WebSocket gatewayUrl 操纵可导致 token 外泄和一键 RCE。API 密钥和中间推理痕迹以明文存储于 Markdown/SQLite。ClawHub 中被曝 **26.1%** 的 Skill 存在漏洞（Liu et al.，引自 SkillSieve [[S135]](wiki/sources/S135.md)），可向向量数据库写入持久化后门规则。Snyk ToxicSkills 审计进一步发现 13.4% 含关键级问题、36.8% 含任何级别安全问题 [[S135]](wiki/sources/S135.md)。

---

### 4.2 Claude Code

#### 核心判断
Claude Code 的 **5 层渐进压缩管道** 配合 Prompt Cache 感知设计，是当前 **Token 效率最优的编码 Agent 记忆方案**。但它刻意牺牲了跨会话自动记忆沉淀能力，选择"状态重建"而非"聊天记录延续"——这使其成为四人中最"项目级"而非"个人级"的记忆设计。

#### 架构概览
Claude Code 是 Anthropic 的代码专用 Agent CLI/IDE 工具，其记忆系统围绕 **CLAUDE.md 四级层级** 和 **五层渐进式上下文压缩管道** 构建。与 OpenClaw/Hermes 不同，它不做跨会话的自动长期记忆沉淀，而是强调"状态重建"而非"聊天记录延续"。

Anthropic 内部对 132 名工程师和研究者的调查显示，约 **27%** 的 Claude Code 辅助任务是"没有该工具就不会尝试的工作"，表明其架构显著扩展了用户的能力边界 [[S007]](wiki/sources/S007.md)。

#### CLAUDE.md 四级层级
1. 用户级全局 `~/.claude/CLAUDE.md`
2. 组织级（如公司标准）
3. 项目级（仓库根目录）
4. 工作区/子目录级

文件在会话启动时加载，Agent 可通过工具读取和更新它们，但不存在自动的"每日笔记"或 dreaming 系统。这种层级设计的核心优势是**上下文作用域的精确控制**——项目级记忆只影响当前仓库，不会泄露到其他项目。

#### 五层压缩管道（按成本从低到高）
1. **Tool Result Budget**：单个工具结果上限 50K chars，单条消息上限 200K chars；超限时持久化到磁盘（`sessionDir/tool-results/`），原消息替换为 `<persisted-output>` 占位符 [[S008]](wiki/sources/S008.md)。
2. **Snip Compact**：直接移除最旧的消息组，最粗暴但最便宜。
3. **Microcompact**：选择性清除旧工具结果，利用 Anthropic `cache_edits` API 在 cache 热时保留前缀稳定性（匹配服务端 60 分钟 TTL）。这是 Claude Code 的**独门绝技**——传统压缩会改变请求前缀导致 Prompt Cache 失效，而 Microcompact 通过仅编辑中间内容保持前缀不变，使长会话仍能复用之前写入的 cache。
4. **Context Collapse**：分阶段折叠消息块，创建折叠视图而不删除原始数据。
5. **Auto-Compact**（成本最高）：当历史占用达到 `contextWindow - 13K` 时，调用 Claude API 生成结构化摘要。使用"私有草稿本"技巧：先输出 `<analysis>` 推理，再输出 `<summary>`，最终只保留 summary 注入上下文。连续 3 次失败则触发断路器，防止无限重试 [[S008]](wiki/sources/S008.md)。

**Prompt Cache 的成本优势**：Anthropic 官方数据显示，Prompt Cache 可将重复前缀的成本降低达 **90%**。Claude Code 的 Microcompact 层刻意保持前缀稳定，使压缩后的请求仍能复用 cache，这是其显著降低长会话 API 成本的关键机制 [[S007]](wiki/sources/S007.md)。

#### 记忆检索
采用 **LLM-based 文件头扫描**：Claude Code 不维护向量索引，而是让模型扫描 CLAUDE.md 文件的头部来决定加载哪些内容。这种方式在语义理解上最精确（模型原生理解"deploy"和"ship to production"的等价性），但消耗 API tokens。社区报告指出，Claude Code 每次请求的工具定义就消耗约 **55,000 tokens** [[S008]](wiki/sources/S008.md)，其中相当一部分用于记忆扫描。

#### Auto-Memory（跨会话）
- 官方 auto-memory 功能让 Agent 自动将项目知识（构建命令、目录结构、代码风格）写回 `CLAUDE.md` 或相关记忆文件。
- 社区插件（如 ClaudeMem）提供 `/remember`、`/forget` 等命令，但属于第三方扩展。

**与 OpenClaw 的记忆哲学对比** [[wiki/comparisons/openclaw-vs-claude-code.md]](wiki/comparisons/openclaw-vs-claude-code.md)：

| 维度 | OpenClaw | Claude Code |
|---|---|---|
| **记忆哲学** | 文件即真相（磁盘 Markdown） | 上下文压缩 + 持久化工具结果 |
| **持久层** | 明文 Markdown + SQLite | 磁盘缓存工具结果 + CLAUDE.md |
| **搜索机制** | 混合（70% 向量 + 30% BM25） | LLM 扫描 + grep |
| **上下文管理** | Bootstrap 预算 + 截断 | 5 层渐进压缩 |
| **用户可见性** | 完全透明，人类可编辑 | 半透明（CLAUDE.md 层级） |
| **安全态势** | CVE-2026-25253；明文 secret | 无已知 CVE；记忆文件用户可编辑 |
| **多会话连续性** | ✅ 文件天然持久 | ⚠️ 依赖压缩摘要 |
| **Token 效率** | ⚠️ 全量 MEMORY.md 注入 | ✅ 激进压缩 |
| **审计性** | ✅ 纯文本，git-friendly | ⚠️ 二进制/编译状态 |

---

### 4.3 Codex CLI

#### 核心判断
Codex CLI 以**极简主义**换取**确定性和安全性**——它是四个主要开源框架中唯一内置 secret redaction 的框架，也是包体最小（~50 MB）、启动最快的。但其 6 小时合并延迟和 32 KiB 的 AGENTS.md 上限使其不适合需要实时记忆更新或复杂项目指令的场景。

#### 架构概览
Codex CLI 是 OpenAI 用 Rust 编写的开源终端编码 Agent，其记忆模型刻意保持极简，分为**静态层**和**生成层**。Rust 构建的 CLI 包体约 50 MB [[S144]](wiki/sources/S144.md)，最低 4 GB RAM 即可运行，推荐 8 GB 用于大型代码库 [[S144]](wiki/sources/S144.md)。

#### Layer 1：AGENTS.md（静态指令）
- 遵循 Linux Foundation Agentic AI Foundation 的开放规范。
- 发现顺序：全局 `~/.codex/AGENTS.md` → 项目路径自上而下的所有 `AGENTS.md` → 支持回退到 `CLAUDE.md`、`.cursorrules` 等跨工具命名。
- **硬性上限 32 KiB**（约 8000 tokens），超出部分静默截断 [[S010]](wiki/sources/S010.md)。

**跨工具兼容性**：Codex 的 AGENTS.md 规范设计为跨工具通用——Claude Code、Cursor、Windsurf 等工具都可以读取同一套 AGENTS.md 文件。这意味着团队可以维护一套项目级指令，在所有编码工具间共享。但 **Memories（生成层）不共享**——每个工具维护自己的生成记忆。

#### Layer 2：Memories（生成记忆）
- 完全由 Codex 自主维护，存储于 `~/.codex/memories/`。
- **两阶段管道** [[S010]](wiki/sources/S010.md)：
  - Phase 1（每会话）：空闲 6 小时后触发，用 extraction model 采样对话并提取要点，**内置 secret redaction**（凭据脱敏）。
  - Phase 2（合并）：获取全局锁，用 consolidation model 将候选记忆与现有存储合并。
- **存储格式**：纯 Markdown，固定文件集：`memory_summary.md`（会话启动时全读）、`MEMORY.md`（长合并文件）、`raw_memories.md`、按技能划分的 `skills/<name>/SKILL.md`、每会话的 `rollout_summaries/<slug>.md`。
- **召回机制**：读取 `memory_summary.md` 全文并做 token 截断；需要更多细节时，**指示 Agent 用 `grep` 搜索 `MEMORY.md`**——完全没有向量检索 [[S013]](wiki/sources/S013.md)。

**Secret Redaction 机制**：Codex CLI 在记忆落盘前自动识别并脱敏 API 密钥、密码、token 等凭据。这是四个主要开源框架中**唯一**的默认 secret 保护机制。OpenClaw 以明文存储 API 密钥于 Markdown/SQLite；Claude Code 和 Hermes 依赖用户不在记忆文件中写入密钥；Codex CLI 则主动预防——即使 Agent 不慎在对话中暴露了密钥，也不会被写入持久存储 [[S010]](wiki/sources/S010.md)。

**记忆生命周期参数** [[S010]](wiki/sources/S010.md)：

| 参数 | 值 | 含义 |
|---|---|---|
| 合并触发延迟 | 6 小时 | 会话结束后需空闲 6 小时才触发提取 |
| Age-out 阈值 | 30 天 | 超过 30 天的 rollouts 和记忆条目被修剪 |
| Rollout 上限 | 256 | 最多考虑最近 256 个 rollouts 用于合并 |
| AGENTS.md 上限 | 32 KiB | 静态指令的硬性上限，超出静默截断 |

#### 限制与缺口
- **无跨设备同步**：`~/.codex/memories/` 是纯本地生成状态。
- **无团队共享**：新团队成员的首次会话只有项目 `AGENTS.md`，无法继承队友已生成的记忆。
- **地理限制**：EEA、英国、瑞士用户无法使用 Memories 功能（监管合规）。
- **Cloud Codex 记忆黑箱**：OpenAI 称云端记忆跨会话持久，但存储形态、保留策略未披露。
- **6 小时冷却期的风险**：如果系统在会话结束后 6 小时内崩溃，该会话的记忆提取将完全丢失。对于需要严格持久性的场景（如金融交易记录），这是不可接受的风险。

---

### 4.4 Hermes Agent

#### 核心判断
Hermes 的**插件化记忆架构**提供了四个框架中最大的灵活度——8 个外部提供商覆盖从用户建模到知识图谱的全谱系能力，FTS5 检索在万级文档下仅需 ~10 ms。但这种灵活性引入了**多重外部依赖和攻击面**：当 Honcho 提供商激活时，完整消息被发送到 `api.honcho.dev`；8 个提供商意味着 8 个独立的信任边界。

#### 架构概览
Hermes 由 Nous Research 开发，定位是"会自我改进的 Agent"，其核心差异在于**闭环学习**：从交互中提取模式，自动编码为可复用 Skill。记忆系统是支撑这一闭环的基石。

Hermes Agent 是 Python 编写的开源运行时（MIT 许可证），首月获得 6,000 GitHub stars [[S016]](wiki/sources/S016.md)。它支持六种执行后端：Local、Docker、SSH、Daytona、Singularity、Modal——通过 BaseEnvironment 接口统一，单条配置即可切换 [[S016]](wiki/sources/S016.md)。

#### 五层记忆架构

| 层级 | 存储 | 内容 | 速度 | 激活方式 |
|---|---|---|---|---|
| 工作记忆（Prompt） | 上下文窗口 | MEMORY.md (~800 tokens) + USER.md (~500 tokens) | 即时 | 会话启动时自动加载为冻结快照 |
| 会话归档（Cold） | SQLite + FTS5 | 所有 CLI 和消息会话历史 | ~10 ms（万级文档） | Agent 显式调用 `session_search` |
| 结构化存储 | SQLite + FTS5 | 跨会话检索、实体解析 | ~10 ms → 113 ms（基准） | 外部提供商激活时叠加 |
| 程序性记忆 | Skill 文件（agentskills.io 标准） | 可复用工作流 | 按需加载 | 任务完成后自动创建 |
| 用户建模 | Honcho / USER.md | 用户理解与偏好 | 中等 | 辩证 Q&A 深度触发 |

**冻结快照设计**：MEMORY.md 和 USER.md 在会话启动时作为**冻结快照**加载到系统提示词中，目的是保持 LLM 前缀缓存稳定。会话中写入的更新会立即持久化到磁盘，但直到下一次会话才会出现在系统提示词中 [[S015]](wiki/sources/S015.md)。这种设计的优势是确定性——每次会话启动时的记忆内容完全一致；劣势是延迟——会话中的新发现不会立即影响当前会话的行为。

**FTS5 检索性能**：SQLite 内置全文搜索，基准约 **10 ms** 检索 10,000+ 文档，可扩展至约 10 万文档后才需专用向量数据库（Qdrant/Weaviate/Chroma）[[S016]](wiki/sources/S016.md)。在 300 事件基准测试中，Hermes 的召回延迟为 **113 ms**，而 OpenClaw 为 19,593 ms——差距达 173× [[S136]](wiki/sources/S136.md)。

**Skill 加载优化**：默认只将 Skill 名称和简述加载到系统提示词，完整 body 按需加载，因此 Skill 库从 40 扩展到 200+ 对上下文成本影响极小 [[S016]](wiki/sources/S016.md)。这与 OpenClaw 的 MEMORY.md 全量注入形成对比——OpenClaw 的 bootstrap 预算截断机制会在 MEMORY.md 过大时截断注入副本，而 Hermes 的按需加载天然避免了这一问题。

#### 8 个外部记忆提供商（v0.7.0+ 插件化）

| 提供商 | 存储 | 成本 | 独特能力 | 框架集成 |
|---|---|---|---|---|
| **Honcho** | Cloud/自托管 | 付费/免费 | 辩证用户建模（dialectic reasoning），3-pass 深度；AGPL v3.0 | OpenClaw, Hermes |
| **OpenViking** | 自托管 | 免费 | 字节跳动 Volcengine，L0/L1/L2 分层加载，Token 节省 60–80% | Hermes 原生 |
| **Mem0** | Cloud | 免费增值 | 服务端 LLM 提取，30 秒 setup；CRUD 操作 | 8+ 框架 |
| **Hindsight** | Cloud/Local | 免费/付费 | 4 网络知识图谱 + reflect 合成；LongMemEval 91.4%（Gemini-3） | Hermes 原生 |
| **Holographic** | 本地 SQLite | 免费 | 零 pip 依赖，HRR 代数 + 信任评分 | Hermes 原生 |
| **RetainDB** | Cloud | $20/月 | 混合搜索 + delta 压缩 | — |
| **ByteRover** | 本地/Cloud | 免费/付费 | 预压缩提取，防止上下文压缩丢失信息 | — |
| **Supermemory** | Cloud | 付费（$19–$29/月） | 语义长期记忆 + 会话图构建 | 广泛连接器 |

**提供商选择的影响**：当外部提供商激活时，Hermes 自动执行六项操作 [[S013]](wiki/sources/S013.md)：
1. 将提供商上下文注入系统提示词
2. 每轮前预取相关记忆（后台、非阻塞）
3. 每轮后将对话同步到提供商
4. 会话结束时提取记忆（提供商支持时）
5. 将内置记忆写入镜像到外部提供商
6. 添加提供商专用工具（搜索、存储、管理）

这种"加法"设计意味着外部提供商不会替代内置记忆，而是增强它。但这也意味着每增加一个提供商，就增加了一套 API 调用、网络延迟和潜在故障点。

**Honcho 的特殊风险**：当 Honcho 提供商激活时，完整消息被发送到 `api.honcho.dev` 进行用户建模 [[S143]](wiki/sources/S143.md)。虽然 Honcho 支持自托管，但默认配置使用云端服务——这意味着用户的完整对话历史离开了本地机器。对于隐私敏感场景，这是一个必须显式评估的风险。

#### 自我改进循环（GAPA-like）
1. **Observe**：监测环境、排名、消息。
2. **Reason**：LLM 评估选项、规划多步动作。
3. **Act**：通过浏览器、API、终端执行。
4. **Learn**：提取模式，编码为 Skill，通过使用不断优化。

此循环不是模型微调（无需 GPU/数据集），而是**提示级自适应**——通过更好的提示、记忆检索和工具编排来优化表现 [[S016]](wiki/sources/S016.md)。

**模型栈**：Hermes 3（Llama 3.1 fine-tune，8B/70B/405B）和 Hermes 4（混合推理，带 `<think>` 标签，DataForge 合成数据生成，约 500 万样本 / 600 亿 tokens）。Hermes 4.3（36B）在 ByteDance Seed 36B 上微调。训练使用 Atropos 分布式 RL 框架，通过约 1,000 个任务专用验证器进行拒绝采样 [[S016]](wiki/sources/S016.md)。

**性能数据**：Hermes 2 Pro 达到 **90%** 的函数调用准确率，而通用模型为 60–70% [[S016]](wiki/sources/S016.md)。Hermes 4.3 在 AIME'24 上将过度长推理减少 **78.4%**，准确率成本为 4.7% [[S016]](wiki/sources/S016.md)。


---

### 4.5 字节跳动 UI-TARS / 豆包 / Seed-TARS / OpenViking

#### 核心判断
字节跳动在 Agent 记忆领域部署了**三条并行路线**，覆盖了从模型参数到框架基础设施的全部技术栈层级：UI-TARS 的"模型内记忆"解决感知-推理-行动的原生集成；豆包手机的"端云协同"解决消费者设备的隐私与效率平衡；OpenViking 的"上下文数据库"解决框架级记忆的检索效率和可观测性。这三条路线互不替代，而是形成了字节在 Agent 记忆领域的**全栈覆盖**。

#### 架构定位：原生 Agent 模型 vs 框架插件

与 OpenClaw、Hermes 等"框架级"记忆系统不同，字节跳动走了一条**原生 Agent 模型（Native Agent Model）**路线。UI-TARS 不是在大模型外接记忆模块，而是将感知（Perception）、推理（Reasoning）、记忆（Memory）和行动（Action）统一在一个端到端模型内部。这种设计哲学的核心是：Agent 的进化正从"框架组装"转向"模型原生"。

#### UI-TARS-2 的分层记忆状态

根据 UI-TARS-2 技术报告（arXiv:2509.02544），其记忆架构采用严格的数学形式化：

```
Mt = (Wt, Et)
```

- **工作记忆（Working Memory, Wt）**：保存最近 k 个步骤的高保真轨迹，包含完整的 reasoning trace、action 和 observation。直接参与当前推理，但受限于上下文窗口，只保留最后 N 步。
- **情景记忆（Episodic Memory, Et）**：对历史 episode 进行语义压缩后的摘要，保留关键意图、决策和结果。用于长程召回，当 Wt 无法覆盖时使用 Et 进行条件推理。

这种双轨设计与认知神经科学中的工作记忆-长期记忆分工高度一致，也与 OpenClaw 的"短期上下文 vs 长期 Markdown 文件"异曲同工——区别在于 UI-TARS 的压缩和检索发生在**模型内部**，而非外部数据库。

#### UI-TARS-1.5 的能力边界

| 能力 | 指标 | 对比基准 | 来源 |
|---|---|---|---|
| 视觉 grounding | 1120×1120 分辨率截图 | Qwen2.5-VL-7B 基础，15 亿条 GUI 数据微调 | [[S046]](wiki/sources/S046.md) |
| UI 元素定位误差 | **<5 像素** | — | [[S046]](wiki/sources/S046.md) |
| ScreenSpotPro 准确率 | **61.6%** | Claude-3 27.7%；CUA 23.4%；前 SOTA 43.6% | [[S046]](wiki/sources/S046.md) |
| Minecraft 错误减少（think-before-act） | **38%** | 相比直接行动预测 | [[S046]](wiki/sources/S046.md) |
| 操作延迟降低 | **30%+** | 双轨记忆动态调配资源 | [[S046]](wiki/sources/S046.md) |
| 成本 | **$0.12/1K 操作** | GPT-4V $0.21/1K 操作（低 43%） | [[S046]](wiki/sources/S046.md) |

**ScreenSpotPro 61.6% 的意义**：在 GUI 元素定位这一高难度基准上，UI-TARS-1.5 不仅大幅领先 Claude-3（27.7%）和 GPT-4V，甚至超过了此前的 SOTA 模型（43.6%）。这表明"模型内记忆"路线在特定领域（GUI 操作）可以达到超越框架级记忆的效果——因为模型通过训练内化了屏幕理解的先验知识，无需像 OpenClaw/Hermes 那样在运行时检索外部记忆。

**成本优势**：$0.12/1K 操作 vs GPT-4V 的 $0.21/1K 操作，成本低 43%。对于高频 GUI 自动化场景（如批量数据录入、UI 测试），这一成本差距在规模化部署中将累积为显著差异。

#### 豆包手机：端云协同的记忆架构

豆包手机（字节深度集成的 AI 手机）采用**"云端理解 + 本地存储 + 向量检索"**三路架构：

1. **云端模型 InternVL3-2B**：负责屏幕理解、推理和任务规划。手机以约 3–5 秒间隔上传约 250 KB 的压缩截图包，云端返回约 1 KB 的下一步行动指令（点击坐标、滑动方向、文本输入）。
2. **本地 embedding 模型**：负责将用户交互历史、偏好、常用应用行为编码为向量，存储在本地向量数据库中。
3. **本地检索**：当用户触发相关查询时，本地向量检索优先召回历史记忆，减少云端往返。

这种架构的隐私 implication 是**敏感操作留在本地检索层，复杂推理上云**——与 Apple Intelligence 的"设备端语义索引 + Private Cloud Compute"有异曲同工之妙。但关键差异在于：Apple 的 PCC 提供密码学可验证的隐私保证，而豆包的云端理解模型由字节跳动运营，用户需完全信任 vendor。

#### OpenViking：字节跳动的上下文数据库

OpenViking（GitHub: `volcengine/OpenViking`，6.3K+ stars，Apache 2.0）是字节跳动火山引擎团队开源的**上下文数据库**，与 UI-TARS 的"模型内记忆"形成互补——前者解决**框架级记忆的检索效率和可观测性**问题。

**核心设计：文件系统范式 + L0/L1/L2 分层加载**

OpenViking 抛弃了传统 RAG 的扁平向量切片模型，将所有上下文映射到 `viking://` 协议下的虚拟文件系统中：

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

**关键限制**：OpenViking 需要外部 LLM 生成 L0/L1 摘要，因此无法完全离线运行。这与 OpenClaw/Hermes 的完全本地能力形成对比。此外，OpenViking 2026 年初才开源，虽有 Red Hat 部署指南和学术案例分析，但缺乏大规模生产环境的独立基准测试。

#### 与四大开源框架的对比

| 维度 | UI-TARS/豆包 | OpenClaw | Hermes Agent |
|---|---|---|---|
| **记忆层级** | 模型内双轨（Wt/Et） | 文件 + SQLite 外部存储 | 文件 + SQLite + 外部提供商 |
| **可干预性** | 低（黑盒模型行为） | 高（用户可直接编辑 Markdown） | 高（可插拔提供商） |
| **部署形态** | 云端 API + 手机系统级集成 | 自托管 Gateway | 自托管 Python 进程 |
| **隐私模型** | 端云协同（敏感记忆本地） | 完全本地优先 | 完全本地优先（可选云提供商） |
| **跨会话持久** | 依赖云端账户 | 文件天然持久 | SQLite + 文件持久 |
| **成本** | $0.12/1K 操作 | 本地硬件 + API 费用 | 本地硬件 + 可选提供商费用 |

---

### 4.6 美国互联网厂商记忆系统洞察（Google / Microsoft / Amazon / Meta / Apple）

#### 核心判断
五家美国互联网厂商的记忆策略分化反映了各自的核心竞争优势：**Google** 靠超长上下文窗口"消化"记忆问题；**Microsoft** 靠企业治理集成建立最完整的托管方案；**Amazon** 靠无服务器基础设施降低接入门槛；**Apple** 靠设备端隐私架构建立差异化；**Meta** 则最为保守，将记忆层完全留给第三方生态。

#### Google：超长上下文 + Astra 多模态记忆

Google 的记忆策略是**"用超长上下文窗口减少对外部记忆的依赖，同时用 Astra 探索原生多模态个人记忆"**。

- **Gemini 2M 上下文窗口**：Gemini 1.5 Pro 支持 **200 万 token** 上下文（相当于 1.4M 词或 2 小时视频），并推出 Context Caching API，允许开发者将常用上下文缓存复用，降低重复 prompt 成本 [[S050]](wiki/sources/S050.md)。对于 1M token 的 KV Cache，预估需约 **15 GB GPU 内存/用户**；2M token 约需 30 GB [[S050]](wiki/sources/S050.md)。
- **Project Astra**：基于 Gemini 2.0 的研究原型，目标是"通用 AI 助手"。Astra 的"多模态记忆"能整合文本、图像、音频，记住用户过往交互的关键细节，并跨工具（Search、Gmail、Calendar、Maps）检索内容。Astra 支持手机摄像头实时对话和原型眼镜形态。
- **NotebookLM**：文档级长期记忆产品，支持对大量文档的持续合成和演进式上下文保留。

**基础设施成本**：2M token 的预填充延迟可达 **2 分钟以上**，KV Cache 内存占用巨大。Google 通过 Context Caching 和 MoE 稀疏激活缓解成本，但大规模部署仍是数据中心 HBM 容量的重要压力来源。在 128 张 H100 上，上下文并行效率达到 **93%**（405B 模型在 1M token 规模）[[S050]](wiki/sources/S050.md)。然而，长上下文并非免费午餐——"Lost in the middle"现象在 1M token 规模下导致约 **40%** 的上下文检索准确率下降 [[S050]](wiki/sources/S050.md)。

#### Microsoft：三域托管记忆 + 企业治理

Microsoft 在 2025 年下半年推出了迄今为止最完整的**企业级记忆产品线**：

- **Copilot Memory（M365/Consumer）**：2025 年 7 月 GA。采用三域记忆模型：
  - **User 域**：跨所有工作区和会话持久，保存用户偏好、常用命令（自动加载前 200 行）。
  - **Repository 域**：工作区级别，保存代码库约定、项目结构、构建命令。
  - **Session 域**：会话级别，任务完成后清除。
  记忆存储由用户和租户管理员共同控制，支持 Purview eDiscovery 合规审计。
- **VS Code Copilot Memory Tool**：2026 年 5 月进入预览。所有记忆数据**本地存储**，提供三种作用域，与云端 Copilot Memory 形成互补。
- **Azure AI Foundry Agent Memory（Preview）**：面向开发者的托管记忆服务，支持跨会话持久上下文，后端可选 Cosmos DB + Azure AI Search。

Microsoft 的核心优势是**企业治理集成**——记忆隔离、Entra Agent ID、RBAC、自动保留策略——这是开源框架目前最薄弱的环节。对于受监管行业（金融、医疗、政府），Microsoft 的三域模型提供了目前唯一成熟的企业级记忆治理方案。

#### Amazon：Bedrock AgentCore Memory — 完全托管的 STM/LTM

Amazon 在 2026 年初推出的 Bedrock AgentCore Memory 是一个**无服务器化的记忆基础设施**：

- **两层记忆**：
  - **短期记忆（STM）**：保存会话内原始对话事件，支持多轮上下文和服务重启后的会话续接。
  - **长期记忆（LTM）**：自动异步提取语义事实（Semantic）、用户偏好（UserPreference）、对话摘要（Summary）和情景切片（Episodic）。
- **零运维**：开发者无需管理数据库、embedding 管道或提取逻辑，**50 行 Java 代码**即可接入。
- **AWS 原生集成**：与 Neptune Analytics（图记忆后端）、ElastiCache for Valkey（高速缓存）、S3 Vectors（原生向量存储，宣称降低 **90%** 向量存储成本）无缝配合。

Amazon 的路线是**基础设施即服务**——把记忆作为 Bedrock 生态的一个托管组件，最适合已有 AWS 技术栈的企业。但其"完全托管"也意味着用户失去了对记忆存储的物理控制——数据驻留在 AWS 数据中心，受 AWS 服务条款约束。

#### Apple：设备端语义索引 + Private Cloud Compute

Apple Intelligence 的记忆架构是五家厂商中**最独特的隐私优先设计**：

- **语义索引（Semantic Index）**：系统级的向量数据库，对用户的短信、邮件、日历、照片等个人数据进行 embedding，支持基于含义（而非关键词）的检索。这是 Siri 理解"个人上下文"的基础设施。
- **App Intents 工具箱**：所有应用向系统注册可执行操作（类似于 Agent 的工具集），Siri/Agent 运行时通过 orchestration 层调度。
- **三层计算架构**：
  - 设备端 **3B Apple Foundation Model（AFM）** 处理简单请求。
  - **Private Cloud Compute（PCC）** 服务器处理复杂请求，运行 Apple Silicon，提供密码学可验证的隐私保证（零数据保留、无法被 Apple 工程师访问）。
  - 第三方大模型（ChatGPT / Google Gemini）处理世界知识查询。
- **Ferret-UI**：Apple 自研的屏幕理解模型，使 Agent 能"看到"iOS 屏幕并按像素坐标执行操作。

Apple 的主要限制是**Siri 全面 AI 化已延期至 2026 年春季**，当前 Apple Intelligence 功能（写作工具、通知摘要、图片清理）距离完整的 Agent 记忆体验仍有显著差距。此外，虽然 PCC 提供了密码学级隐私保证，但用户仍无法独立验证实现是否正确——这是闭源系统的根本信任不对称。

#### Meta：最保守的记忆策略

Meta 在五大厂商中记忆能力最不成熟：

- **LLaMA 4**：支持高达 **1,000 万 token** 的上下文窗口（通过 MindStudio 等第三方框架），但这属于模型上下文容量，并非持久化跨会话记忆架构。
- **无专用记忆产品**：与 OpenAI（ChatGPT Memory）、Google（Astra）、Microsoft（Copilot Memory）、Apple（Semantic Index）不同，Meta 目前未向消费者提供具备持久跨会话记忆的产品。
- **开源生态依赖**：Meta 将记忆层留给第三方框架（LangGraph、CrewAI、MindStudio），自身聚焦模型开源和推理基础设施（与 Cerebras 合作的 Llama API 达 **2,600 tok/s**）。

Meta 的策略可概括为**"模型能力开放，记忆体验由生态补齐"**。这种策略的优势是避免了与第三方框架的竞争，让生态自由创新；劣势是 Meta 在 Agent 记忆产品化上落后于其他四家厂商。

#### 五厂商记忆策略对比

| 维度 | Google | Microsoft | Amazon | Apple | Meta |
|---|---|---|---|---|---|
| **核心策略** | 超长上下文消化记忆 | 三域托管 + 企业治理 | 无服务器 STM/LTM | 设备端语义索引 + PCC | 模型能力开放，生态补齐 |
| **记忆产品** | Astra（研究原型） | Copilot Memory（GA） | Bedrock AgentCore（2026.02） | Semantic Index（系统级） | 无 |
| **上下文上限** | 2M tokens | 依赖模型 | 依赖模型 | 3B AFM 设备端 | 10M tokens（LLaMA 4） |
| **持久化层** | KV Cache + Astra 交互历史 | User/Repo/Session 三级 | 自动提取 STM/LTM | 设备端向量 DB | 无 |
| **隐私架构** | 云端加密 | 租户级 DLP + Purview | IAM + VPC | PCC 密码学证明 | 依赖第三方 |
| **企业治理** | 有限 | **最强**（RBAC + 审计） | 强（AWS IAM） | 无 | 无 |
| **离线能力** | 无 | 无 | 无 | **部分**（检索离线，推理需联网） | 依赖第三方 |
| **主要限制** | 2M 预填充 >2min；KV Cache 15GB/用户 | 封闭生态 | 失去物理控制 | Siri AI 化延期 | 无记忆产品 |

---

### 4.7 Karpathy LLM Wiki：编译器模式的个人知识记忆

#### 核心判断
Andrej Karpathy 的 LLM Wiki 不是产品，而是一种**工作流哲学**——它代表了"文件即真相"路线的终极形态：LLM 不仅是记忆的使用者，更是记忆的作者和维护者。对于个人研究者和小团队，这可能是 2026 年性价比最高的 Agent 记忆方案，但其 ~1M 词规模上限和对外部 LLM 的依赖意味着它无法替代企业级记忆基础设施。

#### 核心思想：LLM 作为知识编译器

Karpathy（OpenAI 联合创始人、前 Tesla AI 总监）于 2026 年 4 月 3 日在 X 发布了一篇病毒式传播的帖子（1.2M+ 浏览），提出了一种全新的 Agent 记忆范式——**LLM Knowledge Bases** [[S141]](wiki/sources/S141.md)。

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

**规模边界**：Karpathy 本人声明 ~400K 词是舒适区、~1M 词是上限。超过 ~100 万词后，单次上下文加载太慢，需要引入语义搜索或 RAG [[S141]](wiki/sources/S141.md)。这一边界并非硬性限制，而是实用性阈值——在 1M 词以内，Karpathy 模式的"编译一次，多次查询"效率远超 RAG 的"每次查询重新推导"。

#### 与 RAG 的根本区别

| 维度 | RAG | Karpathy LLM Wiki |
|---|---|---|
| **时间模式** | 查询时重新推导（无状态） | 编译一次，持续维护（有状态） |
| **知识形态** | 瞬态检索结果 | 持久化、可导航的知识库 |
| **跨引用** | 切片丢失文档级连接 | 单篇源文档可触及 10–15 个 Wiki 页面 |
| **可审计性** | 黑盒向量 embedding | 每句话都可追溯到具体 Markdown 文件 |
| **维护成本** | 低（自动索引） | 由 LLM 承担（对人类趋近于零） |
| **规模上限** | 无上限（数据库扩展） | ~1M 词以内（上下文窗口限制） |
| **依赖** | 向量数据库 + embedding 模型 | 外部 LLM（编译 + linting） |

#### 为什么这关乎 Agent 记忆

Karpathy 的 Wiki 模式与 OpenClaw/Hermes 的 Markdown-first 记忆哲学高度共鸣，但增加了一个关键维度：**LLM 不仅是记忆的使用者，更是记忆的作者和维护者**。

- OpenClaw 的 `MEMORY.md` 和每日笔记需要**用户或 Agent 手动编写**。
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
3. **依赖外部 LLM**：编译和 linting 需要调用云端模型，非完全离线。对于气隙环境，需要本地模型支持。
4. **不是企业方案**：缺乏多用户、权限隔离、审计等企业功能。

---

### 参考文献

- [[S001]](wiki/sources/S001.md) OpenClaw 官方文档：Memory overview
- [[S132]](wiki/sources/S132.md) OpenClaw 安全分析（CVE-2026-25253）
- [[S005]](wiki/sources/S005.md) OpenClaw 混合搜索与 embedding 提供商链
- [[S006]](wiki/sources/S006.md) OpenClaw 记忆引擎配置（chunk 参数、Flush 阈值）
- [[S007]](wiki/sources/S007.md) arXiv: Dive into Claude Code (2604.14228)
- [[S008]](wiki/sources/S008.md) Claude Code 工具预算与 Prompt Cache（社区分析）
- [[S010]](wiki/sources/S010.md) Codex CLI 记忆机制（OpenAI 文档）
- [[S013]](wiki/sources/S013.md) Hermes 文档：Memory Providers（8 提供商详解）
- [[S142]](wiki/sources/S142.md) Hermes 记忆配置（config.yaml 参数）
- [[S015]](wiki/sources/S015.md) Vectorize: Hermes Agent Memory Explained
- [[S016]](wiki/sources/S016.md) CrabTalk: Hermes Agent 调查
- [[S138]](wiki/sources/S138.md) OpenClaw 资源需求与部署指南
- [[S020]](wiki/sources/S020.md) Hermes 部署数据（Railway 基准）
- [[S144]](wiki/sources/S144.md) Codex CLI 包体与资源（DeployHQ 指南）
- [[S137]](wiki/sources/S137.md) EasyClaw: OpenClaw vs Hermes Agent 基准
- [[S136]](wiki/sources/S136.md) Regolo: OpenClaw vs Hermes 延迟与磁盘对比
- [[S028]](wiki/sources/S028.md) Business20Channel: 多智能体协调基准
- [[S131]](wiki/sources/S131.md) OpenClaw ClawHub 安全分析
- [[S046]](wiki/sources/S046.md) AI Base: ByteDance Doubao UI-TARS-1.5
- [[S050]](wiki/sources/S050.md) Google Gemini 2M 上下文官方文档
- [[S050]](wiki/sources/S050.md) Google Context Caching 与基础设施
- [[S141]](wiki/sources/S141.md) Karpathy LLM Wiki X 帖子与社区复刻
- [[S143]](wiki/sources/S143.md) Honcho 隐私审计（api.honcho.dev 数据传输）
- [[wiki/comparisons/openclaw-vs-claude-code.md]](wiki/comparisons/openclaw-vs-claude-code.md)
- [[wiki/comparisons/openclaw-vs-hermes.md]](wiki/comparisons/openclaw-vs-hermes.md)
- [[wiki/comparisons/file-based-vs-database-memory.md]](wiki/comparisons/file-based-vs-database-memory.md)

## 5. 技术对比：存储、检索与压缩

### 0. 判断表

| 维度 | 核心判断 | 证据强度 |
|---|---|---|
| **存储范式** | 文件优先 vs 数据库优先的权衡贯穿所有框架；混合架构（Markdown + SQLite）是当前开源框架的最优折中 | 强（4 框架 + 4 外部提供商 + file-based-vs-database 对比） |
| **检索延迟** | 同一场景下延迟差距可达 **173×**（OpenClaw 19.6s vs Hermes 113ms），但"最快"不等于"最适合"——取决于语义复杂度与成本的权衡 | 强（S027 同基准测试，300 事件场景） |
| **上下文压缩** | Claude Code 的 5 层渐进压缩在 Token 效率上无可匹敌，但每次压缩都有损；Codex CLI 的单层 handoff 则几乎无损但粗粒度 | 中（Claude Code 内部机制，S007–S009） |
| **记忆更新** | 6 种更新策略构成不可能三角：**实时性**（Mem0/Honcho）、**崩溃韧性**（OpenClaw 文件持久）、**Token 效率**（Claude Code 压缩）不可兼得 | 中（架构对比，无统一基准量化） |
| **基准可信度** | 记忆提供商的自报数字与独立复现差距高达 **45.4 个百分点**，该领域缺乏类似 MLPerf 的标准化审计协议 | 强（S095 独立复现 vs Mem0 博客，S078–S081 论文数据） |

---

### 1. 核心判断

2026 年 Agent 记忆系统的技术选型不存在"银弹"。

**在存储层**，文件优先（OpenClaw、Karpathy Wiki）提供了人类可审计的透明度，但牺牲了对百万级记录的查询能力；数据库优先（Mem0、Hindsight）提供了亚百毫秒的检索性能，但引入了供应商锁定和模式迁移成本。**混合架构**（Markdown 正本 + SQLite 派生索引）成为开源框架的共同选择，但"正本"与"派生"之间的同步一致性仍是未解决的工程难题 [[file-based-vs-database-memory]](wiki/comparisons/file-based-vs-database-memory.md)。

**在检索层**，延迟差距并非简单的"好 vs 坏"。Hermes 的 FTS5 在 10,000 文档规模下仅需约 10 ms [[S016]](wiki/sources/S016.md)，但无法处理语义变体（"deploy" vs "ship to production"）；OpenClaw 的混合向量搜索在 300 事件基准下耗时 19,593 ms [[S136]](wiki/sources/S136.md)，但能够召回语义相关的间接表达。Claude Code 的 LLM 扫描"最智能"却最昂贵（每次扫描消耗 API tokens），Codex CLI 的 grep 召回最简单却最确定 [[S013]](wiki/sources/S013.md)。

**在压缩层**，Claude Code 的 5 层渐进管道（Budget → Snip → Microcompact → Collapse → Auto-compact）配合 Prompt Cache 感知设计，是当前 Token 效率最优的方案 [[S007]](wiki/sources/S007.md)。但它的每次压缩都有损——原始工具输出被替换为 `<persisted-output>` 占位符，细节永久丢失。相比之下，OpenClaw 的 Pre-compaction Flush 机制通过在压缩前静默提醒 Agent 保存记忆，实现了"压缩前抢救"，但依赖 Agent 的判断质量 [[S006]](wiki/sources/S006.md)。

**在更新层**，6 种策略的根本分歧在于"谁决定记住什么"。OpenClaw 将决定权交给 Agent（自主判断），Claude Code 交给上下文窗口压力（自动触发），Codex CLI 交给 6 小时空闲计时器（批处理），Mem0 交给实时 CRUD 操作（显式原子），Hindsight 交给知识图谱的 retain/recall/reflect 循环（关系驱动），Honcho 交给辩证 Q&A 的深度触发（用户建模驱动）。没有一种策略在所有场景下占优。

**在基准可信度上**，该领域正经历严重的信任危机。Mem0 官方博客宣称 LongMemEval 94.4% [[S078]](wiki/sources/S078.md)，但独立研究者使用相同协议仅复现出 49% [[S095]](wiki/sources/S095.md)——差距 45.4 个百分点。LoCoMo 上自报 91.6% vs 论文复现 67.13%，差距 24.5pp [[S079]](wiki/sources/S079.md)。目前最可信的公开数据来自 **TiMem**（LoCoMo 75.30%、LongMemEval-S 76.88%，论文复现）[[S120]](wiki/sources/S120.md) 和 **Hindsight**（LongMemEval 91.4%，Gemini-3 后端）[[S015]](wiki/sources/S015.md)，但两者尚未在同一硬件上直接对决。

---

### 5.1 存储技术栈

四个开源框架在存储层的选择反映了它们对"真相源"的不同理解：

| 框架 | 主要存储 | 索引技术 | Embedding 依赖 | 本地离线能力 | 空闲内存 | 磁盘增长（300 事件） |
|---|---|---|---|---|---|---|
| **OpenClaw** | Markdown + SQLite | FTS5 + 向量（sqlite-vec） | 可选（本地 GGUF ~0.6 GB 或 7 种云端） | 完整 | 400–800 MB [[S138]](wiki/sources/S138.md) | +213.41 KB（JSONL 追加）[[S136]](wiki/sources/S136.md) |
| **Claude Code** | Markdown 层级 + 磁盘缓存工具结果 | 无（LLM 扫描头） | 无 | 完整 | ~300–500 MB | 依赖工具结果持久化 |
| **Codex CLI** | Markdown | 无（grep） | 无 | 部分（Memories 生成需云端模型） | ~50 MB 包体 [[S144]](wiki/sources/S144.md) | 本地生成状态 |
| **Hermes** | Markdown + SQLite + 可选外部 DB | FTS5 + 可选向量/图谱/HRR | 可选（Holographic 零依赖） | 完整 | <512 MB [[S020]](wiki/sources/S020.md) | +0.00 KB（SQLite WAL 压缩）[[S136]](wiki/sources/S136.md) |

**关键洞察：磁盘增长模式的结构性差异**。在相同的 300 事件基准下，OpenClaw 的 JSONL 追加策略导致磁盘增长 213.41 KB，而 Hermes 的 SQLite WAL 压缩实现零净增长 [[S136]](wiki/sources/S136.md)。这不是偶然——OpenClaw 的"文件即真相"哲学要求保留完整的原始转录，而 Hermes 的 SQLite 架构通过 WAL 合并和页面回收实现了对历史记录的压缩存储。对于长期运行的 Agent（数月到数年），这一差异将累积为显著的磁盘占用差距。

**文件优先 vs 数据库优先的范式张力** [[wiki/comparisons/file-based-vs-database-memory.md]](wiki/comparisons/file-based-vs-database-memory.md)：

| 维度 | 文件优先（OpenClaw, Karpathy Wiki, Codex） | 数据库优先（Mem0, Hindsight, Supermemory） |
|---|---|---|
| **人类可读性** | ✅ 原生纯文本 | ⚠️ 需工具/查询 |
| **版本控制** | ✅ Git-friendly | ⚠️ 需迁移脚本 |
| **搜索能力** | ⚠️ 需索引层（FTS5, sqlite-vec） | ✅ 原生（向量相似度、图遍历） |
| **可扩展性** | ⚠️ 随文件数线性增长 | ✅ 百万记录级设计 |
| **模式约束** | ❌ 无（自由 Markdown） | ✅ 类型模式、约束 |
| **并发访问** | ⚠️ 文件锁问题 | ✅ ACID 事务 |
| **备份/迁移** | ✅ `cp` 或 `git clone` | ⚠️ 导出/导入管道 |
| **静态加密** | ⚠️ 仅 OS 级 | ✅ 可加密数据库文件 |

**混合架构的兴起**：OpenClaw（Markdown 正本 + SQLite 派生索引）、Claude Code（CLAUDE.md 静态文件 + 磁盘缓存工具结果）、Hermes（MEMORY.md 静态 + 外部向量动态）都选择了混合路线。这种架构的核心理念是"人类可编辑的文件作为正本，机器高效的索引作为派生"，但正本与派生之间的同步一致性（如文件修改后索引何时更新）仍是各框架的实现细节差异。OpenClaw 采用 1.5 秒防抖的增量重索引 [[S005]](wiki/sources/S005.md)，Hermes 则依赖显式的工具调用来触发更新 [[S142]](wiki/sources/S142.md)。

---

### 5.2 检索机制对比

检索是记忆系统的核心差异化维度。四个框架在"如何找到正确的记忆"上采用了四种完全不同的哲学：

| 框架 | 检索机制 | 典型延迟 | 语义理解 | 成本特征 | 来源 |
|---|---|---|---|---|---|
| **OpenClaw** | 混合搜索：0.7×向量 + 0.3×BM25，MMR λ=0.7，30 天半衰期时间衰减 | 19.6s（300 事件，向量全量）[[S136]](wiki/sources/S136.md) | 强（语义相似度 + 关键词） | 高（embedding API 或本地 GPU） | [[S005]](wiki/sources/S005.md), [[S006]](wiki/sources/S006.md) |
| **Claude Code** | LLM 扫描 CLAUDE.md 文件头 + grep 补充 | 取决于模型响应（通常 1–5s） | 最强（LLM 原生理解） | 最高（每次扫描消耗 API tokens） | [[S007]](wiki/sources/S007.md) |
| **Codex CLI** | 全文加载 memory_summary.md + grep MEMORY.md | <100ms（本地文件读取） | 弱（纯字符串匹配） | 最低（零外部调用） | [[S013]](wiki/sources/S013.md) |
| **Hermes** | SQLite FTS5 BM25 + 可选外部向量/图谱 | 10ms（万级文档）→ 113ms（基准）[[S016]](wiki/sources/S016.md) | 中（FTS5 关键词；外部提供商增强） | 低（本地免费；外部付费） | [[S016]](wiki/sources/S016.md), [[S136]](wiki/sources/S136.md) |

**延迟差距的深层含义**：同一场景（300 事件）下，OpenClaw（19.6s）与 Hermes（113ms）的延迟差距达 **173×** [[S136]](wiki/sources/S136.md)。但这一差距不意味着 OpenClaw"更差"——它反映了两种检索哲学的根本差异：

- **OpenClaw 的 19.6s 来自 JSONL 全量回注**：在召回时，OpenClaw 将 300 条事件的完整 JSONL 历史注入 LLM 上下文，由模型自行筛选。这是一种" brute-force 语义检索"——不预处理索引，直接让 LLM 从原始数据中找答案。它的优势是不遗漏任何细节（因为所有原始数据都进入了上下文），劣势是延迟随历史长度线性增长。

- **Hermes 的 113ms 来自 FTS5 预索引**：Hermes 在写入时就将事件索引到 SQLite FTS5，召回时只需执行一个 SQL 查询。这是一种"预计算关键词检索"——速度快但无法理解语义变体。当需要语义理解时，Hermes 必须依赖外部向量提供商（如 Hindsight、OpenViking），此时延迟上升到外部 API 的级别。

- **Claude Code 的 LLM 扫描** 在智能程度上最高——模型可以理解"deploy"和"ship to production"的语义等价性——但成本也最高。社区报告指出，Claude Code 每次请求的工具定义就消耗约 55,000 tokens [[S008]](wiki/sources/S008.md)，其中相当一部分用于记忆扫描。

- **Codex CLI 的 grep** 在确定性上最强——给定相同的查询，永远返回相同的结果——但无法理解任何语义变体。对于编码场景（变量名、函数名是精确的字符串），这种"愚蠢但确定"的检索反而比语义搜索更可靠 [[S013]](wiki/sources/S013.md)。

**记忆召回准确率的对比数据**（S026 同任务基准）[[S137]](wiki/sources/S137.md)：

| 指标 | OpenClaw | Hermes | 差距 |
|---|---|---|---|
| 简单任务延迟（Llama 3.1 70B） | 1.4s | 1.9s | Hermes 慢 36% |
| 多步研究延迟 | 4.1s | 5.3s | Hermes 慢 29% |
| 跨会话记忆召回（session 2） | 61% | **89%** | Hermes 高 28pp |
| 10 步流水线延迟 | 5.9s | 4.2s | OpenClaw 慢 40% |
| 4 智能体协调成功率 | 81.4% | **98.2%** | Hermes 高 17pp |

这组数据揭示了一个重要的权衡：**检索速度与召回准确率并非正相关**。Hermes 在延迟上并不总是最快（简单任务反而慢于 OpenClaw），但在跨会话记忆召回和多智能体协调上显著领先。这表明预索引结构（FTS5 + 分层记忆）在长期一致性上的优势，超过了纯向量搜索的短期速度优势。

---

### 5.3 上下文压缩策略

上下文压缩是 Agent 记忆的"暗物质"——它不直接可见，却决定了长会话的成本和效果。四个框架的压缩策略从极简到复杂形成鲜明光谱：

| 框架 | 策略复杂度 | 缓存感知 | 独特机制 | 关键参数 |
|---|---|---|---|---|
| **Claude Code** | ★★★★★（5 层） | 是（Prompt Cache 深度集成） | Microcompact 利用 cache_edits；私有草稿本技巧 | 工具预算 50K/消息 200K；13K 阈值；3 次失败断路器 [[S008]](wiki/sources/S008.md) |
| **OpenClaw** | ★★★☆☆（可插拔 + 预刷新） | 部分（Anthropic 原生 compaction 支持） | 压缩前自动提醒 Agent 保存记忆 | Flush 阈值 4000 tokens 或 2MB [[S006]](wiki/sources/S006.md) |
| **Hermes** | ★★★☆☆（/compress + ByteRover 预提取） | 依赖模型提供商 | ByteRover 可在压缩前抢救信息 | MEMORY.md 2200 chars；USER.md 1375 chars [[S142]](wiki/sources/S142.md) |
| **Codex CLI** | ★★☆☆☆（单层 handoff summary） | 否 | 最简化，用户消息原样保留 | 32 KiB AGENTS.md 上限；30 天 age-out；256-rollout cap [[S010]](wiki/sources/S010.md) |

**Claude Code 的 5 层压缩管道详解** [[S007]](wiki/sources/S007.md) [[S008]](wiki/sources/S008.md)：

1. **Tool Result Budget**（成本最低）：单个工具结果上限 50K chars，单条消息上限 200K chars；超限时持久化到磁盘（`sessionDir/tool-results/`），原消息替换为 `<persisted-output>` 占位符。
2. **Snip Compact**：直接移除最旧的消息组，最粗暴但最便宜。
3. **Microcompact**：选择性清除旧工具结果，利用 Anthropic `cache_edits` API 在 cache 热时保留前缀稳定性（匹配服务端 60 分钟 TTL）。这是 Claude Code 的独门绝技——通过保持请求前缀不变，使压缩后的请求仍能复用 Prompt Cache，显著降低长会话 API 成本。
4. **Context Collapse**：分阶段折叠消息块，创建折叠视图而不删除原始数据。
5. **Auto-Compact**（成本最高）：当历史占用达到 `contextWindow - 13K` 时，调用 Claude API 生成结构化摘要。使用"私有草稿本"技巧：先输出 `<analysis>` 推理，再输出 `<summary>`，最终只保留 summary 注入上下文。连续 3 次失败则触发断路器，防止无限重试。

**Prompt Cache 感知的独特价值**：Claude Code 的压缩设计刻意保持前缀稳定，这是其显著降低长会话 API 成本的关键机制。传统压缩（如直接截断）会改变请求前缀，导致 Prompt Cache 失效；Claude Code 的 Microcompact 通过 `cache_edits` 在保留前缀的同时清除中间内容，使 cache 命中率在长会话中保持高位。Anthropic 官方数据显示，Prompt Cache 可将重复前缀的成本降低达 90%。

**OpenClaw 的 Pre-compaction Flush**：在上下文压缩前，系统会先发一个静默回合提醒 Agent 将重要信息写入记忆文件，防止压缩导致信息丢失。软阈值为 4000 tokens 或 2 MB 转录文件 [[S006]](wiki/sources/S006.md)。这是一种"压缩前抢救"机制——不阻止压缩发生，但给 Agent 一个保存关键信息的机会。与 Claude Code 的自动压缩不同，OpenClaw 的 Flush 依赖 Agent 的判断：如果 Agent 没有识别出重要信息，Flush 不会自动保存。

**Hermes 的静态快照策略**：Hermes 的 MEMORY.md（~2200 chars / ~800 tokens）和 USER.md（~1375 chars / ~500 tokens）在会话启动时作为**冻结快照**加载到系统提示词中，用于前缀缓存稳定性 [[S142]](wiki/sources/S142.md)。动态更新需要显式的 `/compress` 命令或 ByteRover 预提取。这种设计的优势是确定性——每次会话启动时加载的记忆内容完全一致，不受之前会话压缩质量的影响；劣势是灵活性——如果会话中产生了重要的新信息，不会自动反映到当前会话的记忆中。

**Codex CLI 的极简主义**：Codex 的压缩策略最简单——单层 handoff summary，在会话结束后 6 小时由提取模型生成。用户消息原样保留，不做任何中间压缩。32 KiB 的 AGENTS.md 上限（约 8000 tokens）通过硬性截断强制执行 [[S010]](wiki/sources/S010.md)。这种"不压缩直到最后"的策略确保了会话中的信息完整性，但也意味着长会话的上下文窗口压力完全由底层模型承担。

---

### 5.4 记忆更新策略对比

除了存储和检索，各框架在**何时记忆、如何更新、何时遗忘**这一时间维度上存在根本性分歧。基于对 Mem0、Hindsight、Honcho 等外部提供商与四大框架的对比分析，可归纳出六种更新策略范式：

| 框架/系统 | 更新触发器 | 合并策略 | 遗忘机制 | 核心权衡 | 典型延迟 |
|---|---|---|---|---|---|
| **OpenClaw** | Agent 自主判断 + heartbeat 定时扫描 | 手动蒸馏（每日笔记 → 长期 MEMORY.md） | Bootstrap 预算截断（文件仍在磁盘） | 人类式选择性记忆，但不稳定 | 即时写入，延迟取决于 Agent 判断 |
| **Claude Code** | 上下文窗口压力（`contextWindow - 13K`） | 5 层渐进摘要 | 旧消息被总结后丢弃 | Token 效率最高，但每次压缩有损 | 压缩触发时 ~1–3s（API 调用） |
| **Codex CLI** | 会话结束后 6 小时空闲 | LLM 提取 → 合并模型整合 | 30 天过期 + 256-rollout 上限 | 批处理高效，但崩溃前 6h = 记忆丢失 | 6h 冷却后后台异步 |
| **Mem0** | 实时（每轮 ADD/UPDATE/DELETE/NOOP） | 异步双模型合并（提取 + 合并） | 时效衰减 + 相关性评分 | 最细粒度控制，但 CRUD 开销大 | 实时响应，合并异步 |
| **Hindsight** | 每轮交互后（retain→recall→reflect） | 知识图谱增量更新（4 网络） | 信念修正 + 冲突消解 | 关系最丰富，但计算成本高 | 每轮 3-pass 深度推理 |
| **Honcho** | 每轮持久化 + 辩证深度触发 | 冷/热提示合成 | 上下文节奏刷新 | 用户建模最深，但辩证轮增加延迟 | 辩证轮额外 2–3 次 API 调用 |

**遗忘机制的本质差异**：

| 系统 | 如何遗忘 | 是否真正消失 | 可恢复性 |
|---|---|---|---|
| **OpenClaw** | Bootstrap 预算截断注入副本 | ❌ 文件在磁盘完好 | 高（直接编辑文件） |
| **Claude Code** | 旧消息被总结后丢弃 | ✅ 原始细节丢失 | 低（summary 不可逆向展开） |
| **Codex CLI** | 30 天 age-out + 256-rollout 上限 | ✅ 记忆条目删除 | 无（删除后不可恢复） |
| **Mem0** | Age-out + 相关性评分低于阈值 | ✅ 从向量存储移除 | 低（移除后无备份） |
| **Hindsight** | 信念修正覆盖旧信念 | ⚠️ 旧信念可能残留在网络中 | 中（图结构保留历史路径） |
| **Honcho** | 上下文节奏刷新替换旧上下文 | ⚠️ 旧上下文归档，非删除 | 中（历史版本可回溯） |

**关键洞察**：记忆更新策略的选型取决于三个不可兼得的维度——**实时性**（Mem0/Honcho）、**崩溃韧性**（OpenClaw 文件持久）、**Token 效率**（Claude Code 压缩）。

- **金融、医疗等需要跨会话严格一致性的场景**：Codex CLI 的 6 小时冷却期是致命弱点——系统崩溃前 6 小时内的所有交互记忆将全部丢失。OpenClaw 的文件持久化虽然写入不稳定（依赖 Agent 判断），但至少不会因崩溃而丢失已写入的内容。
- **客服、个人助手等需要即时学习的场景**：Mem0 的实时 CRUD 模式最优——用户偏好变化（如"我喜欢深色模式"）可以立即更新，无需等待批处理窗口。但 CRUD 开销意味着每轮交互都有额外的嵌入计算和向量写入成本。
- **长文档分析、代码重构等成本敏感场景**：Claude Code 的压缩管道在 Token 效率上无可匹敌。通过 5 层渐进压缩和 Prompt Cache 感知，Claude Code 可以在 100+ 轮会话中将 API 成本控制在线性增长范围内，而 OpenClaw 的 JSONL 全量注入会导致成本随历史长度超线性增长。

---

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

一个关键洞察是：**没有单一架构能同时满足"用户完全可控""跨设备无缝同步""完全离线"和"企业级治理"**。这解释了为什么市场同时存在开源框架、云服务和设备系统三种形态。

**补充：OpenViking 和 Karpathy Wiki 的差异化定位**

OpenViking 和 Karpathy LLM Wiki 不完全属于上述任何一列，而是**跨路线的中间层**：

- **OpenViking** 本质上是一个**可插拔的记忆基础设施**——它既可以被 OpenClaw/Hermes 这样的开源框架集成（作为外部提供商），也可以被云厂商的 Agent 服务用作底层上下文存储。它的文件系统范式比传统 RAG 更结构化，比纯 Markdown 记忆更高效（L0/L1/L2 分层），潜在 Token 节省 60–80%，并支持可视化检索轨迹调试。但 setup 成本高于简单向量数据库（需要 Go + C++ 编译器，依赖外部 LLM 生成摘要）。

- **Karpathy LLM Wiki** 则是一个**工作流范式**，不绑定任何特定工具。你可以用 Claude Code、Codex、Cursor 甚至 ChatGPT 来实现它。它的独特价值在于"知识复利"——每次查询的输出被重新归档到 Wiki 中，使知识库随使用而增长。这在传统 RAG 中是不可能发生的（RAG 的向量数据库只增不减，但不会自动产生新的综合知识）。Karpathy 模式的最大限制是规模（~400K 词舒适区、~1M 词上限），但在该范围内，它的信息密度和可审计性远超任何向量检索方案。

---

### 5.6 基准测试可信度全景

Agent 记忆领域的基准测试目前呈现**严重的可信度危机**。三大主流基准（LoCoMo、LongMemEval、BEAM）的测试协议互不兼容，而提供商的自报数字与独立复现之间存在巨大鸿沟。

| 基准 | 测试场景 | 领先分数（自报） | 领先分数（独立） | 关键局限 | 来源 |
|---|---|---|---|---|---|
| **LoCoMo** | 35 会话跨会话一致性 | TiMem **75.30%** | Mem0 67.13% | 合成脚本，无时间衰减建模 | [[S120]](wiki/sources/S120.md), [[S079]](wiki/sources/S079.md) |
| **LongMemEval** | 多天真实聊天场景 | Mem0 94.4% / 94.8% | **Hindsight 91.4%** (Gemini-3) / Mem0 49% | 主观评分，annotator 一致性差 | [[S078]](wiki/sources/S078.md), [[S095]](wiki/sources/S095.md), [[S015]](wiki/sources/S015.md) |
| **BEAM** | 百万/千万 token 极端规模 | Mem0 94.4% (BEAM-1M) | 无公开独立复现 | 合成任务为主，非对话记忆 | [[S078]](wiki/sources/S078.md) |

**最严重的可信度缺口**：Mem0 在 LongMemEval 上自报 94.4%，但独立研究者（S095）使用相同协议仅复现出 **49%**，差距 **45.4 个百分点** [[S095]](wiki/sources/S095.md)。LoCoMo 上自报 91.6% vs 论文复现 67.13%，差距 24.5pp [[S079]](wiki/sources/S079.md)。可能的原因包括：(1) 不同模型后端（GPT-4o vs 本地模型）；(2) 评分标准松紧不一；(3) 只报告最佳运行而非平均值；(4) 博客数字可能反映尚未发表论文的新版本。

**学术前沿的独立验证状态**：

| 架构 | LoCoMo | LongMemEval | 独立验证状态 | 来源 |
|---|---|---|---|---|
| **TiMem** | 75.30% | 76.88% | ✅ 论文复现，可信 | [[S120]](wiki/sources/S120.md) |
| **Hindsight** | — | 91.4% (Gemini-3) / 89.0% (OSS-120B) / 83.6% (OSS-20B) | ⚠️ 单一后端为主，未跨模型全面测试 | [[S015]](wiki/sources/S015.md) |
| **ByteRover** | — | — | ❌ 未在标准基准上评估 | [[S090]](wiki/sources/S090.md) |
| **AtlasKV** | — | — | ❌ 未在标准基准上评估 | [[S119]](wiki/sources/S119.md) |
| **LoCoMo/ST-Lite** | N/A | N/A | ✅ 训练自由，2.45× 加速可复现 | [[S117]](wiki/sources/S117.md) |

**Hindsight 的跨模型性能衰减** [[S015]](wiki/sources/S015.md) 提供了一个重要的参考点：当从 Gemini-3（91.4%）切换到开源 120B 模型（89.0%）再到 20B 模型（83.6%）时，LongMemEval 分数随模型能力下降而线性衰减。这表明记忆系统的表现高度依赖底层 LLM 质量——一个"记忆架构"的分数无法脱离其"模型后端"来解读。

**对读者的建议**：在评估记忆提供商时，优先参考**独立复现的论文数据**（TiMem、Hindsight 论文）而非博客营销数字；对于框架选型，应**自建任务集**在目标硬件上实测，而非依赖厂商宣称的基准分数。当前该领域最紧迫的需求是建立一个类似 MLPerf 的**标准化记忆基准审计协议**，强制要求披露模型后端、评分标准、运行次数和置信区间。

---

### 参考文献

- [[S005]](wiki/sources/S005.md) OpenClaw 官方文档（混合搜索权重、文件监控参数）
- [[S006]](wiki/sources/S006.md) OpenClaw 记忆引擎配置（chunk 参数、Flush 阈值）
- [[S007]](wiki/sources/S007.md) Claude Code 压缩管道（Anthropic 技术博客）
- [[S008]](wiki/sources/S008.md) Claude Code 工具预算与 Prompt Cache（社区分析）
- [[S010]](wiki/sources/S010.md) Codex CLI 记忆机制（OpenAI 文档）
- [[S013]](wiki/sources/S013.md) Codex CLI 架构解析（逆向工程）
- [[S142]](wiki/sources/S142.md) Hermes 记忆配置（config.yaml 参数）
- [[S015]](wiki/sources/S015.md) Hindsight 基准测试（LongMemEval 跨模型对比）
- [[S016]](wiki/sources/S016.md) Hermes FTS5 性能（CrabTalk 调查）
- [[S138]](wiki/sources/S138.md) OpenClaw 资源需求（部署指南）
- [[S020]](wiki/sources/S020.md) Hermes 部署数据（Railway 基准）
- [[S144]](wiki/sources/S144.md) Codex CLI 包体与资源（DeployHQ 指南）
- [[S137]](wiki/sources/S137.md) 四框架同任务基准（Regolo 复现）
- [[S136]](wiki/sources/S136.md) OpenClaw vs Hermes 延迟与磁盘对比（EasyClaw 基准）
- [[S078]](wiki/sources/S078.md) Mem0 基准声明（官方博客）
- [[S079]](wiki/sources/S079.md) Mem0 论文复现（LoCoMo 67.13%）
- [[S095]](wiki/sources/S095.md) Mem0 独立复现（LongMemEval 49%）
- [[S117]](wiki/sources/S117.md) LoCoMo/ST-Lite KV Cache 压缩
- [[S120]](wiki/sources/S120.md) TiMem Temporal Memory Tree
- [[wiki/comparisons/file-based-vs-database-memory.md]](wiki/comparisons/file-based-vs-database-memory.md)
- [[wiki/comparisons/memory-update-strategies.md]](wiki/comparisons/memory-update-strategies.md)
- [[wiki/comparisons/benchmark-landscape.md]](wiki/comparisons/benchmark-landscape.md)
- [[wiki/comparisons/framework-security-comparison.md]](wiki/comparisons/framework-security-comparison.md)
- [[wiki/comparisons/external-memory-providers.md]](wiki/comparisons/external-memory-providers.md)

## 6. 系统性能要求与硬件诉求

### 0. 判断表

| 维度 | 核心判断 | 关键数据 | 证据强度 |
|---|---|---|---|
| **编排层资源** | 四个框架本体都是"编排层"，对芯片几乎零诉求 | 最低 2 GB RAM 即可运行；空闲内存 <512 MB–800 MB | 强（官方文档 + 部署实测） |
| **本地 LLM 推理** | 真正的硬件杀手；70B 模型需 48–128 GB RAM 或高端 GPU | Llama 3.1 70B：M1 Max 64GB 5.8 tok/s；M4 Max 128GB 12.5 tok/s | 强（S024 社区基准） |
| **Apple Silicon 优势** | 统一内存架构（UMA）在端侧大模型场景下具有独特优势 | M4 Max 128GB 统一内存 + 546 GB/s 带宽；Neural Engine 对 LLM 推理几乎无帮助 | 强（官方规格 + 实测） |
| **端侧向量检索** | embedding 模型极小（100M–2B），现代手机 SoC 可轻松胜任 | 本地 embedding 4 ms（GPU）/ 61 ms（CPU）/ 200 ms（云端 API） | 中（社区基准） |
| **云端 KV Cache** | Google 2M 上下文路线创造数据中心新压力点 | 1M token ~15 GB GPU 内存/用户；128 H100 93% 并行效率 | 强（S050 官方文档） |

---

### 1. 核心判断

Agent 框架的硬件需求呈现**极端的两极分化**：编排层本身轻如鸿毛——任何现代 CPU 均可运行；但叠加本地 LLM 推理后，硬件需求陡增至工作站级别。

**三个关键洞察**：

1. **编排层 vs 推理层的 100× 差距**：OpenClaw Gateway 空闲 400–800 MB [[S138]](wiki/sources/S138.md)，而本地运行 Llama 3.1 70B 需要 48–128 GB RAM [[S139]](wiki/sources/S139.md)——差距达 **100–300×**。这意味着 Agent 框架的硬件选型决策应完全围绕"是否运行本地模型"展开，而非框架本身。

2. **Apple Silicon 的统一内存架构是端侧大模型的游戏规则改变者**：传统 GPU 通过 PCIe 与系统内存通信，模型权重必须复制到 VRAM；Apple Silicon 的 UMA 允许 GPU 直接访问系统内存，消除了 PCIe 瓶颈。M4 Max（128 GB 统一内存，546 GB/s 带宽）是当前消费级运行 70B 模型的最佳选择 [[S139]](wiki/sources/S139.md)。但关键限制是：**Neural Engine 对 LLM 推理几乎无帮助**，实际使用 Metal GPU Compute。

3. **云端 KV Cache 是数据中心的新压力点**：Google Gemini 的 2M 上下文意味着每用户 15–30 GB 的 KV Cache。虽然 Context Caching 和 MoE 稀疏激活缓解了成本，但大规模部署仍是 HBM 容量的重要压力来源 [[S050]](wiki/sources/S050.md)。这正在催生新的芯片需求：更大的 HBM 容量（H100 80 GB → H200 141 GB）、更高的内存带宽，以及 KV Cache 量化技术（NVFP4 可将需求减半）。

---

### 6.1 框架本体（编排层）—— 极轻量

以下数据为**仅运行 Agent 框架、调用云端 LLM API** 时的资源需求：

| 框架 | 最低 RAM | 推荐 RAM | 最低 CPU | 磁盘 | 运行时依赖 | 空闲内存 | 包体大小 |
|---|---|---|---|---|---|---|---|
| **OpenClaw** | 2 GB | 4 GB | 2 核 | 20 GB SSD | Node.js 22.14+ | 400–800 MB [[S138]](wiki/sources/S138.md) | ~2–3 GB 安装 [[S138]](wiki/sources/S138.md) |
| **Claude Code** | 4 GB | 8–16 GB | 任意现代 CPU | ~500 MB | 无（原生安装）或 Node.js | ~300–500 MB | ~500 MB |
| **Codex CLI** | 4 GB | 8 GB | 任意现代 CPU | ~50 MB + 会话数据 | Node.js 22+（或独立 Rust 二进制） | ~50 MB 包体 [[S144]](wiki/sources/S144.md) | ~50 MB [[S144]](wiki/sources/S144.md) |
| **Hermes Agent** | ~2 GB | 4 GB | 2 核 | ~1 GB + SQLite | Python 3.11+ | <512 MB [[S020]](wiki/sources/S020.md) | ~1 GB |

**关键结论**：**四个框架的 Gateway/CLI 进程本身对芯片几乎零诉求**。在仅使用云端 API 的场景下：
- Raspberry Pi 5（8 GB）、$60 旧办公机、$5/月 VPS 均可稳定运行。
- **无需 GPU、NPU 或专用 AI 加速器**。
- Codex CLI 的 Rust 二进制体积极小（~50 MB），是四人中最轻量的；OpenClaw 的 Node.js 运行时相对最重（2–3 GB 安装）。

**磁盘增长的长期影响**：

| 框架 | 300 事件磁盘增长 | 增长模式 | 年化预估（中等活跃度） |
|---|---|---|---|
| **OpenClaw** | +213.41 KB [[S136]](wiki/sources/S136.md) | JSONL 追加，线性增长 | 1–3 GB/月 [[S138]](wiki/sources/S138.md) |
| **Hermes** | +0.00 KB [[S136]](wiki/sources/S136.md) | SQLite WAL 压缩 | 可忽略（WAL 合并） |
| **Claude Code** | 依赖工具结果持久化 | 按需持久化大工具输出 | 取决于工具使用频率 |
| **Codex CLI** | 本地生成状态 | Markdown 文件累积 | 取决于会话频率 |

OpenClaw 的 JSONL 追加策略在长期运行下将累积为显著的磁盘占用，而 Hermes 的 SQLite WAL 压缩实现了零净增长。对于计划长期运行（数月到数年）的部署，这一差异需要在容量规划中考虑。

**浏览器自动化的额外开销**（OpenClaw 典型场景）：
- 每个 Playwright/Chromium 实例额外消耗 200–400 MB RAM [[S138]](wiki/sources/S138.md)。
- 推荐在生产环境为此预留 4–8 GB 额外内存。
- 例如，一个同时管理 10 个浏览器实例的 OpenClaw Gateway，仅浏览器就需 2–4 GB 额外 RAM。

---

### 6.2 本地 LLM 推理叠加——真正的硬件杀手

若要在同一台机器上运行本地模型（Ollama / vLLM / llama.cpp / SGLang），硬件需求呈指数级上升：

| 模型规模 | 量化 | 最低 RAM/VRAM | 推荐配置 | 适用芯片/设备 | Llama 3.1 70B tok/s |
|---|---|---|---|---|---|
| 1.5B | Q4 | 4 GB RAM | 任意现代 CPU | 树莓派 5、旧办公机 | — |
| 7–8B | Q4 | 8 GB VRAM / 16 GB RAM | RTX 3060 / M4 16GB | 入门级 GPU、Mac Mini | — |
| 13–14B | Q4 | 12 GB VRAM / 32 GB RAM | RTX 4070 / M4 Pro 24GB | 中端 GPU、MacBook Pro | — |
| 30–32B | Q4 | 24 GB VRAM / 64 GB RAM | RTX 4090 / M4 Max 36GB | 高端 GPU、Mac Studio | — |
| 70B | Q4 | 48 GB VRAM / 128 GB RAM | 2×RTX 4090 / M4 Max 128GB | 多卡工作站、Mac Pro | M1 Max 64GB: 5.8 tok/s [[S139]](wiki/sources/S139.md) |
| 70B | Q4 | 48 GB VRAM / 128 GB RAM | 2×RTX 4090 / M4 Max 128GB | 多卡工作站、Mac Pro | M4 Max 128GB: 12.5 tok/s [[S139]](wiki/sources/S139.md) |

**Apple Silicon 的实测性能** [[S139]](wiki/sources/S139.md)：

| 设备 | 统一内存 | 带宽 | Llama 3.1 70B Q4 tok/s | 相对速度 |
|---|---|---|---|---|
| M1 Max | 64 GB | 400 GB/s | 5.8 | 基准 |
| M4 Max | 128 GB | 546 GB/s | 12.5 | **2.16×** |

M4 Max 的 128 GB 统一内存和 546 GB/s 带宽使其成为当前消费级运行 70B 模型的最佳选择。但关键限制是：**Neural Engine 对 LLM 推理几乎无帮助**——虽然 Apple 宣传 Neural Engine 的 38 TOPS 算力，但 LLM 推理实际使用 Metal GPU Compute，Neural Engine 主要用于 smaller 的 ML 工作负载（如图像分类、语音识别）。

**NVIDIA vs Apple vs AMD/Intel**：

| 平台 | 优势 | 劣势 | 推荐场景 |
|---|---|---|---|
| **NVIDIA CUDA** | 生态最成熟；vLLM、TensorRT-LLM 支持最好 | 显存与系统内存分离；大模型需多卡 | 生产级部署；需要最高吞吐量 |
| **Apple Silicon UMA** | GPU 直接访问系统内存；无 PCIe 拷贝 | Neural Engine 对 LLM 帮助有限；macOS 独占 | 个人开发者；70B 端侧运行 |
| **AMD ROCm** | 开源驱动；较好的 Linux 支持 | 生态明显弱于 CUDA；部分模型不兼容 | 预算受限；已有 AMD GPU |
| **Intel OpenCL** | 集成显卡可用 | 生态最弱；性能远低于 CUDA/Metal | 轻量模型；无其他 GPU 可用 |

**专用边缘设备**：ClawBox（NVIDIA Jetson Orin Nano Super，67 TOPS）专为 OpenClaw 设计，但仅适合小模型（7B 以下）或 API 代理模式。边缘设备的典型场景是工厂自动化、零售监控等需要本地推理但不需要大模型的场景。

---

### 6.3 端侧向量检索与云端 KV Cache 的硬件压力

除了本地 LLM 推理，两个新兴场景正在创造额外的硬件需求：

**端侧向量检索（Apple Intelligence / 豆包手机路线）**：

设备需要运行小型 embedding 模型（通常 100M–2B 参数）将个人数据实时向量化。Apple 的语义索引需要持续维护一个覆盖全设备数据的向量数据库（预估 10–100 MB 级，取决于数据量）。

**Embedding 推理的延迟对比**：

| 后端 | 延迟 | 适用场景 |
|---|---|---|
| llama.cpp GPU 本地 | **~4 ms** [[S005]](wiki/sources/S005.md) | 高频实时嵌入（如每轮交互都更新向量） |
| Ollama CPU 本地 | ~61 ms [[S005]](wiki/sources/S005.md) | 中频嵌入，无 GPU 可用 |
| OpenAI API 云端 | ~200 ms [[S005]](wiki/sources/S005.md) | 低频嵌入，追求质量 |

对芯片的诉求：**NPU/GPU 用于快速 embedding 推理**，但 embedding 模型极小（100M–2B 参数），现代手机 SoC（A17 Pro、骁龙 8 Gen 3 及以上）均可轻松胜任。实际上，端侧向量检索的瓶颈不是 embedding 速度，而是向量数据库的维护和检索效率。

**云端 KV Cache（Google Gemini 2M 上下文路线）**：

| 上下文长度 | KV Cache 内存（FP16） | 量化后（NVFP4） | 用户规模影响 |
|---|---|---|---|
| 128K tokens | ~2 GB | ~1 GB | 可管理 |
| 1M tokens | **~15 GB** | ~7.5 GB | 显著压力 |
| 2M tokens | **~30 GB** | ~15 GB | 数据中心级挑战 |

Google 通过 Context Caching 和 MoE 稀疏激活缓解成本，但大规模部署仍是数据中心 HBM 容量的重要压力来源。在 128 张 H100 上，上下文并行效率达到 **93%**（405B 模型在 1M token 规模）[[S050]](wiki/sources/S050.md)。

**KV Cache 量化技术**：NVFP4（NVIDIA 4-bit 浮点）可将 KV Cache 内存需求减半，从 FP16 的 15 GB/1M token 降至约 7.5 GB。但这带来了精度损失风险——在需要高精度记忆召回的场景（如医疗、法律），量化可能不可接受。

**对芯片厂商的启示**：

1. **数据中心 GPU 的 HBM 容量和内存带宽**是 Gemini 路线的关键瓶颈。H100（80 GB HBM3）已接近满载，H200（141 GB HBM3e）提供了更多 headroom。下一代芯片（Blackwell B200）需要进一步扩展 HBM 容量。

2. **上下文窗口硬件正在催生新的中间层需求**：OpenViking 的 L0/L1/L2 分层、Karpathy Wiki 的编译器模式、Claude Code 的 Prompt Cache，都在用不同方式解决同一个问题——如何在有限的上下文窗口内放入最有价值的记忆。这对上下文窗口硬件（更长、更便宜）和压缩算法都提出了持续需求。

3. **端侧 NPU 的定位需要重新评估**：虽然 Neural Engine 对 LLM 推理帮助有限，但对小批量 embedding 推理（100M–2B 模型）可能有用。Apple 的 Semantic Index 和字节的本地 embedding 检索都需要设备端快速 embedding 计算——这可能是端侧 NPU 的第一个杀手级应用。

---

### 6.4 成本分析：本地 vs 云端 vs 混合

| 部署模式 | 最低配置 | 舒适配置 | 年化硬件成本 | 年化 API 成本 | 总成本（估算） |
|---|---|---|---|---|---|
| 云端 API + 单 Agent | 2 核 / 2 GB RAM | 2 核 / 4 GB RAM | $60（$5 VPS） | $200–$2,000 | **$260–$2,060** |
| 云端 API + 浏览器自动化 | 2 核 / 4 GB RAM | 4 核 / 8 GB RAM | $120（$10 VPS） | $500–$5,000 | **$620–$5,120** |
| 本地 7B 模型 + Agent | 4 核 / 16 GB RAM | 6 核 / 32 GB RAM | $800（M4 Mac Mini） | $0 | **$800** |
| 本地 14B 模型 + Agent | 8 核 / 32 GB RAM | 8 核 + RTX 4070 | $1,500（M4 Pro MacBook） | $0 | **$1,500** |
| 本地 70B 模型 + Agent | 16 核 / 128 GB RAM | RTX 4090×2 / M4 Max 128GB | $4,000–$7,000 | $0 | **$4,000–$7,000** |
| 企业托管记忆（Copilot/Bedrock） | N/A（纯云端） | N/A | $0 | $50–$500/用户/月 | **$600–$6,000/用户/年** |

**成本拐点**：对于个人用户和小团队，本地 7B 模型（$800 一次性投入）在运行 6 个月后即比云端 API（$200/月 × 6 = $1,200）更经济。对于需要 70B 模型质量的企业，云端 API（$2,000–$5,000/年）可能比购买 $4,000–$7,000 的工作站更灵活——尤其是考虑到硬件折旧和电力成本。

**Amazon S3 Vectors 的成本优势**：Amazon 宣称通过 S3 Vectors 将向量存储成本降低达 **90%**。对于大规模向量数据库（亿级向量），传统托管向量数据库（Pinecone、Weaviate）的存储成本可能达数千美元/月，而 S3 Vectors 可将这一成本降至数百美元/月。但需要注意：S3 Vectors 的延迟显著高于内存级向量数据库，不适合需要亚百毫秒检索的实时场景。

---

### 参考文献

- [[S005]](wiki/sources/S005.md) OpenClaw embedding 提供商链与本地延迟
- [[S138]](wiki/sources/S138.md) OpenClaw 资源需求与部署指南
- [[S020]](wiki/sources/S020.md) Hermes 部署数据（Railway 基准）
- [[S144]](wiki/sources/S144.md) Codex CLI 包体与资源（DeployHQ 指南）
- [[S139]](wiki/sources/S139.md) Apple Silicon 本地推理基准（Llama 3.1 70B）
- [[S136]](wiki/sources/S136.md) OpenClaw vs Hermes 磁盘增长对比
- [[S050]](wiki/sources/S050.md) Google Gemini KV Cache 与基础设施

## 7. 安全与隐私考量

### 0. 判断表

| 维度 | 核心判断 | 关键证据 | 证据强度 |
|---|---|---|---|
| **静态加密** | 四个主要开源框架均不提供默认静态加密，全员裸奔 | 100% 框架（4/4）无默认加密 | 强（官方文档 + 源码审计） |
| **Secret 保护** | Codex CLI 是唯一内置 secret redaction 的框架；OpenClaw 明文存储 API 密钥 | Codex redaction 自动脱敏；OpenClaw CVE-2026-25253 可导致 token 外泄 | 强（S010 OpenAI 文档；S131 SonicWall CVSS 8.8） |
| **记忆投毒** | 持久化跨会话记忆越大，提示注入导致的投毒攻击面越广 | Trojan Hippo：Gemini-3.1-pro 100%（无防御），GPT-5-mini 85% | 中（学术攻击研究，非生产环境验证） |
| **供应链风险** | Hermes 的 8 个外部提供商引入 8 个独立信任边界；Honcho 在 `observe_me=True` 时上传完整对话 | S076 GitHub issue #4074：完整消息、MEMORY.md、USER.md、SOUL.md 均上传至 `api.honcho.dev` | 强（社区审计 issue） |
| **开源 vs 闭源** | 开源透明性既是优势（可审计）也是风险（CVE 公开可 exploited）；闭源无已知 CVE 但无法独立验证 | CVE-2026-25253 公开披露；Claude Code/Apple 无公开 CVE 数据库 | 中（缺乏独立审计数据） |

---

### 1. 核心判断

Agent 记忆系统的安全态势呈现一个**令人警醒的悖论**：框架在记忆能力上越强大（跨会话持久、多模态存储、外部提供商集成），其攻击面就越广；而当前四个主要开源框架在基础安全机制上**全员裸奔**——无默认静态加密、无默认内存加密、无统一 secret 管理。

**三个最紧迫的安全缺口**：

1. **默认加密完全缺失**：OpenClaw 的明文 Markdown/SQLite、Claude Code 的用户级记忆文件、Hermes 的本地 SQLite、Codex CLI 的生成记忆，全部依赖 OS 级磁盘加密（BitLocker/FileVault/LUKS）作为最后一道防线。在共享机器、容器逃逸或冷启动攻击场景下，这是不够的。

2. **供应链信任边界碎片化**：Hermes 的 8 个外部记忆提供商意味着 8 个独立的信任边界。当 Honcho 提供商激活时，用户的完整对话流、本地记忆文件（MEMORY.md、USER.md、SOUL.md）和模型生成的用户画像结论，全部被上传至 Plastic Labs 的 `api.honcho.dev` 服务器 [[S143]](wiki/sources/S143.md)。而 Hermes 的 README 宣称"所有数据留在你的机器上。无遥测、无跟踪、无云锁定"——这一声明在 Honcho 激活时并不成立。

3. **基准可信度危机的安全 implication**：Mem0 的 LongMemEval 自报 94.4% 与独立复现 49% 之间的差距高达 45.4 个百分点 [[S095]](wiki/sources/S095.md)。这意味着基于 Mem0 记忆系统的安全决策（如"Mem0 能准确记住用户的安全偏好"）可能是不可靠的——一个召回率 49% 的记忆系统，有 51% 的概率遗漏关键安全上下文。

---

### 7.1 记忆存储安全

| 框架 | 存储加密 | Secret 处理 | 主要风险 | 沙盒能力 |
|---|---|---|---|---|
| **OpenClaw** | ❌ 无默认加密 | ❌ 无内置脱敏 | CVE-2026-25253（CVSS 9.8）；明文 API 密钥和中间推理痕迹存于 Markdown/SQLite | Docker 可用 |
| **Claude Code** | ❌ 依赖 OS 磁盘加密 | ❌ 依赖用户不在 CLAUDE.md 中写密钥 | 项目级文件可被仓库共享，意外泄露风险；闭源内部机制不可审计 | Docker 可用 |
| **Codex CLI** | ❌ 依赖 OS 磁盘加密 | ✅ **内置 secret redaction**（记忆落盘前脱敏） | Memories 是生成状态，不建议手动编辑；地理可用性受限（EEA/UK/CH 不可用） | AppContainer/Landlock/seccomp |
| **Hermes** | ❌ 依赖 OS 磁盘加密 | ❌ 依赖用户配置 | Honcho 用户建模积累敏感偏好数据；AGPL 合规风险；8 个提供商 = 8 个攻击面 | Docker 可用 |
| **Google Astra** | ✅ 云端加密（Google 标准） | ❌ 依赖 Google 账户安全 | 多模态记忆存储大量个人生活数据；Astra 仍为研究原型，安全审计未公开 | 云端隔离 |
| **Microsoft Copilot** | ✅ 企业级加密 + Purview 审计 | ✅ 租户级 DLP 策略 | 三域记忆增加数据泄露面；Entra Agent ID 是新攻击面 | Azure 安全边界 |
| **Amazon Bedrock** | ✅ AWS KMS 加密 | ✅ IAM + VPC 隔离 | 完全托管意味着用户失去对记忆存储的物理控制 | AWS 安全边界 |
| **Apple Intelligence** | ✅ 设备端加密 + PCC 密码学证明 | ✅ 无需上传原始数据 | 语义索引包含全部个人数据，但理论上不出设备；Siri 延期导致实际安全验证不足 | Secure Enclave |

**加密与数据保护全景** [[wiki/comparisons/framework-security-comparison.md]](wiki/comparisons/framework-security-comparison.md)：

| 框架 | 磁盘加密 | 内存加密 | Secret Vault | 默认安全得分 |
|---|---|---|---|---|
| OpenClaw | ❌ OS-level only | ❌ | ❌ | ★☆☆☆☆ |
| Claude Code | ❌ OS-level only | ❌ | ❌ | ★★☆☆☆ |
| Codex CLI | ❌ OS-level only | ❌ | ✅ Redaction | ★★★☆☆ |
| Hermes | ❌ OS-level only | ❌ | ❌ | ★★☆☆☆ |

**关键发现**：四个主要开源框架**均不提供默认的静态加密或内存加密**。这不是设计疏忽，而是架构空白——Markdown/SQLite 的透明度与加密之间存在根本张力：加密会阻碍人类直接编辑和 `git diff` 审计，而这两个特性正是文件优先架构的核心价值主张。

**OpenClaw 的最高攻击面** [[S131]](wiki/sources/S131.md)：
- **CVE-2026-25253**（CVSS 9.8）：WebSocket gatewayUrl 操纵 → token 外泄 → 一键 RCE。这是本研究语料中 CVSS 评分最高的漏洞。
- **明文 secrets**：API 密钥、中间推理痕迹存储于 `~/.openclaw/workspace` 的明文 Markdown/SQLite 中。
- **文件权限**：完全依赖主机 OS；无框架级访问控制。
- **记忆投毒**：恶意 Skill 可向向量数据库写入持久化后门规则。

**Claude Code 的安全 through obscurity**：目前无已知 CVE，但这可能是闭源码的"安全 through obscurity"效应——内部漏洞可能已被发现但未公开。其记忆文件（CLAUDE.md）用户可见并可审计，但压缩管道的内部机制不透明。

**Codex CLI 的独门绝技**：唯一内置 secret redaction 的框架。在记忆落盘前自动识别并脱敏 API 密钥、密码、token 等凭据。即使 Agent 不慎在对话中暴露了密钥，也不会被写入持久存储 [[S010]](wiki/sources/S010.md)。但其地理限制（EEA/UK/CH 不可用 Memories）是监管合规的产物，而非技术限制。

**Hermes 的分布式风险**：内置记忆（MEMORY.md + USER.md）本地安全、无云端遥测。但当外部提供商激活时——尤其是 Honcho——风险急剧上升。S076 GitHub issue #4074 揭示了 Honcho 集成的隐私缺口：

| 上传至 `api.honcho.dev` 的数据 | 影响 |
|---|---|
| 双向完整对话（用户消息 + Agent 响应） |  verbatim 全文，非摘要 |
| Peer identity（用户名、工作区 ID、会话密钥） | 可关联到具体用户 |
| MEMORY.md、USER.md、SOUL.md | 本地记忆文件完整上传 |
| 完整对话历史（XML 转录） | 迁移时批量上传 |
| 模型生成的用户画像结论 | "用户偏好深色模式"等推断 |

Honcho 的 `observe_me=True` 设置意味着 Honcho 后端在双方对话上运行自己的 LLM，构建用户和 Agent 的持久模型——而设置向导仅描述为"持久跨会话记忆"，未披露完整的数据流 [[S143]](wiki/sources/S143.md)。

---

### 7.2 记忆投毒（Memory Poisoning）

记忆投毒是指攻击者通过提示注入（prompt injection）或其他手段，诱导 Agent 将错误、恶意或后门信息写入持久化记忆，从而长期影响 Agent 行为。

**OpenClaw 的高风险**：
- **恶意 Skill**：ClawHub 中被曝 **26.1%** 的 Skill 存在漏洞（Liu et al.，引自 SkillSieve [[S135]](wiki/sources/S135.md)），可向向量数据库写入持久化后门规则。Snyk ToxicSkills 审计发现 13.4% 含关键级问题、36.8% 含任何级别安全问题 [[S135]](wiki/sources/S135.md)。由于 OpenClaw 的 MEMORY.md 和向量索引是明文且持久化的，恶意 Skill 写入的后门会跨会话持续影响 Agent 行为。
- **Markdown 注入**：攻击者可通过精心构造的对话诱导 Agent 在 MEMORY.md 中写入恶意 Markdown（如隐藏指令、错误偏好），由于 MEMORY.md 在每个会话启动时注入系统提示词，这种投毒具有持久性。
- **缓解措施**：Providence Tags（Observed / User-Confirmed / Model-Inferred）是少数主动缓解手段——用户可以通过来源标记识别和清理不可信的记忆条目。

**所有框架的通用风险**：
通过提示注入诱导 Agent 写入错误记忆是**所有框架的可行攻击面**。无论框架的压缩策略多么复杂，只要 Agent 有写入持久化记忆的能力，提示注入就可以利用这一通道。OpenClaw 的 Providence Tags 和 Hindsight 的信任评分机制是目前有文档记录的少数主动缓解手段。

**云厂商的更高风险**：
Trojan Hippo 攻击研究表明，对 **Gemini-3.1-pro** 的记忆投毒攻击成功率可达 **100%**（无防御时），对 **GPT-5-mini** 达 **85%**。持久化跨会话记忆越大，攻击面越广——因为攻击者只需成功一次，恶意记忆就会在所有后续会话中持续生效。

**关键洞察**：记忆投毒的风险与**记忆的持久性和作用域**成正比。Session-only 记忆（如 Claude Code 的 compaction summaries、Microsoft Copilot 的 Session 域）在会话结束后清除，投毒影响有限；而 User-domain 跨会话持久记忆（如 Microsoft Copilot User 域、Mem0 的用户画像、Honcho 的 peer model）一旦被投毒，影响可能持续数月。

---

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
| **安全事件响应** | 公开披露，社区补丁，用户自更新 | 静默补丁，changelog 通知（如有） |
| **数据可恢复性** | 社区 fork 可能 | 取决于 acquirer（vendor 被收购时） |

**开源的透明性悖论**：
开源的透明性既是安全优势也是风险来源。OpenClaw 的 CVE-2026-25253 可以被社区快速分析和修复，但在补丁发布前漏洞细节完全公开，攻击者可利用。这是一个经典的"披露困境"——立即披露保护用户知情权，但也给攻击者提供了武器；延迟披露降低攻击风险，但用户在无意识中暴露。

**闭源的信任不对称**：
闭源系统（如 Claude Code、Apple Intelligence）目前无已知 CVE，但这可能是"安全 through obscurity"——内部漏洞可能已被发现但未公开。Apple 的 PCC 密码学证明是闭源系统中隐私架构的标杆：
- **零数据保留**：PCC 服务器不保留用户查询数据
- **密码学可验证**：用户设备可密码学验证 PCC 服务器的软件版本和配置
- **无法被 Apple 工程师访问**：即使 Apple 内部人员也无法访问 PCC 上的用户数据

但 PCC 的根本限制是**用户无法独立验证实现是否正确**。密码学证明验证的是协议，而非实现——一个存在 bug 的实现可能破坏所有密码学保证，而用户没有源码来审计。

**中间地带：Open Core**

| 系统 | 开源部分 | 闭源部分 |
|---|---|---|
| **Mem0** | Apache 2.0 自托管 | Cloud API 高级功能 |
| **Honcho** | Protocol + clients 开源 | Managed service (`api.honcho.dev`) |
| **OpenClaw** | 完全开源 | 无闭源版本 |

Open Core 模式试图兼顾两者：自托管版本提供审计性和数据主权，托管版本提供便利性和专业支持。但 Honcho 的案例表明，Open Core 的"开源"部分（protocol + clients）并不能保证托管服务的数据处理透明度——用户仍需完全信任服务运营商。

---

### 7.4 按威胁模型的安全选型建议

| 威胁场景 | 最安全选择 | 理由 | 剩余风险 |
|---|---|---|---|
| **本地攻击者获取文件访问权限** | Codex CLI | 唯一内置 secret redaction，凭据不会明文落盘 | OS 级加密被绕过时的其他数据暴露 |
| **网络侧数据外泄** | Hermes（纯本地模式） | 无云端遥测，Honcho 关闭后完全离线 | 若攻击者已入侵本地网络，SQLite 文件可被读取 |
| **记忆投毒 via 提示注入** | Codex CLI | Memories 为生成状态，非用户直接可编辑；AGENTS.md 上限 32 KiB | 生成模型本身可能被注入影响提取质量 |
| **供应链/提供商被攻破** | OpenClaw（无外部提供商） | 零外部依赖 = 零第三方攻击面 | 自身 CVE-2026-25253 的网关攻击面 |
| **企业审计与合规** | Claude Code + Docker | 无已知 CVE，配合容器隔离可满足多数合规要求 | 闭源内部机制不可审计 |
| **隐私最大化（个人用户）** | Apple Intelligence | 语义索引不出设备，PCC 提供密码学级隐私保证 | Siri AI 化延期，当前功能有限；无法验证 PCC 实现 |
| **气隙/完全离线环境** | Hermes（本地模型 + FTS5） | 无外部依赖，本地 SQLite 无需网络 | 无加密，物理介质丢失 = 数据泄露 |
| **多智能体共享记忆** | Honcho（自托管） | 用户建模 + 权限隔离原生支持 | 配置复杂，自托管运维负担 |
| **高可用性 + 灾难恢复** | Microsoft Copilot / Azure Foundry | 企业级备份、冗余、RBAC、审计 | 完全信任 Microsoft 的数据处理 |

**全员裸奔的加密现状**：

一个令人警醒的发现是——**四个主要开源框架均不提供默认的静态加密或内存加密**。具体影响：

| 场景 | 风险描述 |
|---|---|
| **共享开发机** | 多用户共用服务器时，任何有文件系统访问权限的用户可读取所有 Agent 记忆 |
| **容器逃逸** | Docker/container 逃逸攻击可直接访问宿主机上的明文记忆文件 |
| **冷启动攻击** | 设备关机后，未加密的磁盘数据可通过物理访问恢复 |
| **笔记本丢失** | 未启用 FileVault/LUKS 的设备丢失 = 所有记忆数据暴露 |
| **云实例快照** | 云服务器快照包含明文记忆文件，可被有快照访问权限的管理员读取 |

**缓解建议**：
1. **OS 级全盘加密**：至少启用 BitLocker（Windows）、FileVault（macOS）或 LUKS（Linux）。
2. **容器隔离**：生产环境使用 Docker 运行 Agent 框架，限制容器对宿主机的文件访问。
3. **Secret 管理**：使用 1Password、Bitwarden 或 HashiCorp Vault 管理 API 密钥，不将密钥写入任何记忆文件。
4. **定期审计**：对于 OpenClaw/Hermes，定期审查 MEMORY.md 和向量数据库中的异常条目。
5. **提供商审计**：使用外部记忆提供商前，审查其隐私政策、数据处理协议（DPA）和安全认证（SOC 2、ISO 27001）。

---

### 7.5 安全缺口：最紧迫的未解决问题

基于 120 份阅读笔记的审计，Agent 记忆安全领域存在以下最紧迫的未解决问题：

1. **默认加密架构完全缺失**：没有主流开源框架提供透明的记忆文件加密。需要研究如何在保持 Markdown/SQLite 可审计性的同时实现静态加密（如 age 或 SOPS 集成）。

2. **跨框架记忆迁移的安全风险**：不同框架使用互不兼容的记忆格式，用户在更换框架时往往通过手动复制粘贴迁移——这一过程中敏感数据（API 密钥、个人偏好）可能通过剪贴板历史、临时文件等渠道泄露。

3. **外部提供商的数据处理透明度不足**：Honcho 的案例表明，即使是 Open Core 项目，其托管服务的数据处理也可能远超用户预期。需要建立标准化的"记忆提供商数据处理披露协议"。

4. **记忆投毒的检测与回滚机制缺失**：当前没有任何框架提供记忆完整性校验或投毒检测机制。一旦恶意记忆被写入，用户只能手动审查——这在记忆规模扩大后不可行。

---

### 参考文献

- [[S132]](wiki/sources/S132.md) OpenClaw 安全分析（PDF 不匹配，交叉验证重建）
- [[S132]](wiki/sources/S132.md) OpenClaw 案例研究（PDF 不匹配，交叉验证重建）
- [[S010]](wiki/sources/S010.md) Codex CLI 记忆机制与 secret redaction
- [[S131]](wiki/sources/S131.md) Skywork: CVE-2026-25253 深度分析
- [[S143]](wiki/sources/S143.md) Hermes GitHub issue #4074: Honcho 隐私审计
- [[S095]](wiki/sources/S095.md) Gamgee: Mem0 独立复现（LongMemEval 49%）
- [[wiki/comparisons/framework-security-comparison.md]](wiki/comparisons/framework-security-comparison.md)
- [[wiki/comparisons/open-source-vs-closed-source.md]](wiki/comparisons/open-source-vs-closed-source.md)

## 8. 研究缺口与残余不确定性

### 核心判断

Agent 记忆领域正处于**快速成熟但缺乏标准化**的阶段。120 份阅读笔记和 177 页 Wiki 的审计揭示了 18 个结构性缺口，可分为四类：基准可信度危机（4 条）、安全架构空白（3 条）、生产验证不足（4 条）、生态系统碎片化（4 条）。其中**基准测试可信度危机**和**默认加密缺失**是最紧迫的——前者影响所有基于厂商数据的选型决策，后者影响所有开源框架的生产部署安全。

---

### 8.1 基准可信度危机（最紧迫）

1. **Mem0 自报 vs 独立复现差距达 45.4pp，且非孤例**
   Mem0 官方博客宣称 LongMemEval 94.4% [[S078]](wiki/sources/S078.md)，独立复现仅 49% [[S095]](wiki/sources/S095.md)。LoCoMo 上自报 91.6% vs 论文复现 67.13%，差距 24.5pp [[S079]](wiki/sources/S079.md)。Supermemory 自报 LongMemEval 85.2% [[S095]](wiki/sources/S095.md)，但缺乏独立验证。整个记忆提供商行业缺乏类似 MLPerf 的第三方审计机构。**影响**：任何基于厂商基准的选型决策都可能是不可靠的。

2. **缺乏四框架在同一硬件、同一任务集下的标准化记忆基准测试**
   现有对比数据来自不同作者的独立测试（Regolo、EasyClaw、Business20Channel），硬件和模型 backend 不一致 [[S137]](wiki/sources/S137.md) [[S136]](wiki/sources/S136.md) [[S028]](wiki/sources/S028.md)。OpenClaw 的 19.6s 延迟基于 JSONL 全量回注，而 Hermes 的 113ms 基于 FTS5 预索引——两者测试的是不同检索机制，而非同一问题的不同解法。

3. **亦无统一基准对比开源框架与云厂商托管记忆的召回质量**
   Copilot Memory vs Bedrock AgentCore Memory vs Astra 的召回质量完全未知。云厂商不披露其自动提取算法的准确率，用户无法比较"本地混合搜索"与"云端语义提取"的质量差异。

4. **学术架构的生产验证严重不足**
   ByteRover（RL 记忆操作）和 AtlasKV（参数化 KG）虽在概念上创新，但均未在 LoCoMo 或 LongMemEval 上评估 [[S090]](wiki/sources/S090.md) [[S119]](wiki/sources/S119.md)。TiMem 的 SOTA 分数（75.30% LoCoMo、76.88% LongMemEval-S）来自单一论文 [[S120]](wiki/sources/S120.md)，尚未被独立复现。ByteRover 的 152 个训练对是否足以泛化到开放域对话，完全未知。

---

### 8.2 安全架构空白（高影响）

5. **开源框架默认加密架构完全缺失**
   四个主要开源框架均不提供默认静态加密或内存加密。这不是设计疏忽而是架构空白——Markdown/SQLite 的透明度与加密之间存在根本张力。需要研究：在保持 Markdown/SQLite 可审计性的同时，如何实现对记忆文件的透明加密（如 age 或 SOPS 集成）。**影响**：所有生产部署在共享机器、容器逃逸或冷启动攻击场景下，记忆数据都是裸奔的。

6. **跨框架记忆迁移标准缺失**
   OpenClaw 的 MEMORY.md、Claude Code 的 CLAUDE.md、Codex 的 AGENTS.md + Memories、Hermes 的 USER.md + SQLite——格式互不兼容。用户更换框架时，历史记忆几乎无法无损迁移。更严重的是，迁移过程中的手动复制粘贴可能通过剪贴板历史、临时文件等渠道泄露敏感数据。**影响**：供应商锁定效应被低估；用户一旦选择某框架，迁移成本极高。

7. **多智能体共享记忆的冲突消解未解决**
   当多个 Agent 同时写入同一记忆存储（Honcho 的多租户、Hindsight 的图谱更新）时，如何防止写冲突和信念矛盾？当前没有任何框架提供分布式事务或版本控制机制。**影响**：多智能体协作场景（企业工作流、多 Agent 客服）的记忆一致性无法保证。

---

### 8.3 生产验证不足（中高影响）

8. **OpenViking 生产验证不足**
   OpenViking 2026 年初才开源，虽有 Red Hat 部署指南和学术案例分析，但缺乏大规模生产环境的独立基准测试。L0/L1 的 Token 节省效果（宣称 60–80%）高度依赖摘要质量和目录结构设计。**影响**：企业用户在评估 OpenViking 时缺乏可信的性能数据。

9. **Karpathy Wiki 规模边界模糊**
   Karpathy 本人声明 ~400K 词是舒适区、~1M 词是上限，但未给出精确的方法论来确定"何时需要引入 RAG"。社区复刻的质量参差不齐（76★–349★），缺乏标准化 schema [[S141]](wiki/sources/S141.md)。Yu Wenhao 的批判指出，LLM 决定"哪些源文档合并到哪个 Wiki 页面"是临时决策，缺乏 Zettelkasten 原子笔记的清晰边界规则。**影响**：个人用户在使用 Wiki 模式时缺乏规模管理指南。

10. **长会话记忆漂移未量化**
    Hermes 被报告在 100+ 轮会话中出现相关性评分退化；OpenClaw 在 300 事件基准中召回延迟达 19.6 秒——尚不确定是典型行为还是未优化配置所致 [[S136]](wiki/sources/S136.md)。**影响**：长期运行 Agent（数月到数年）的记忆质量衰减曲线完全未知。

11. **Cloud Codex 记忆黑箱**
    OpenAI 未公开云端 Codex 记忆的存储形态、保留期和配置接口，CLI 结论不能简单外推到云产品。**影响**：企业用户在评估 Cloud Codex 时缺乏安全审计依据。

---

### 8.4 生态系统碎片化（中等影响）

12. **记忆更新策略的最优频率未量化**
    实时更新（Mem0）vs 批处理合并（Codex CLI）vs 压缩驱动（Claude Code）之间的延迟/质量/成本权衡，目前没有任何公开研究给出量化的帕累托前沿。**影响**：框架选型缺乏实证依据，只能依赖架构直觉。

13. **OpenViking 与 UI-TARS 的协同未公开**
    两者同属字节跳动生态，但公开文档未说明 UI-TARS 是否原生集成 OpenViking 作为外部记忆层，或豆包手机是否使用 OpenViking 作为本地向量后端。**影响**：字节生态的完整技术栈无法被外部准确评估。

14. **Google Astra 存储后端未公开**
    Astra 的持久记忆具体使用何种数据库、embedding 模型、检索机制，Google 未披露技术细节，现有分析基于 I/O 演示和产品描述推断。**影响**：技术评估完全基于推测。

15. **Claude Code 三层记忆 vs 四层 CLAUDE.md**
    部分博客提到"三层记忆系统"，但最权威的 arXiv 论文（2604.14228）明确为 4 级 CLAUDE.md 层级 + auto-memory，存在术语混淆 [[S007]](wiki/sources/S007.md)。**影响**：社区讨论中的术语不一致导致理解偏差。

16. **美国厂商产品快速迭代导致结论迅速过时**
    Microsoft Copilot Memory（2025.07 GA）、Azure Foundry Agent Memory（Preview）、Amazon Bedrock AgentCore Memory（2026.02）、Apple Siri overhaul（延期至 2026 春）——这些产品发布时间接近，功能边界和成熟度变化快。**影响**：本报告的厂商分析可能在 6–12 个月内显著过时。

17. **营销数字待验证**
    Skywork 等渠道宣称的"82% 运营成本降低""63% 月度节省"、ByteDance M3-Agent 宣称的"96.7% 召回率"缺乏独立验证，未纳入核心结论。**影响**：厂商营销材料可能误导潜在用户。

18. **本地模型性能与框架无关**
    报告中所有"大内存/GPU"需求均来自模型推理层，而非 Agent 编排层。用户若始终使用云端 API，可完全忽略这些硬件诉求。**影响**：硬件选型指南需要明确区分"框架需求"和"模型需求"。

---

### 8.5 对研究者和开发者的建议

| 缺口类型 | 建议行动 | 优先级 |
|---|---|---|
| 基准可信度 | 建立类似 MLPerf 的"记忆基准审计协议"，强制披露模型后端、评分标准、运行次数和置信区间 | **最高** |
| 默认加密 | 为 Markdown/SQLite 记忆设计透明加密方案（age/SOPS 集成），保持可审计性 | **最高** |
| 生产验证 | 对 TiMem、ByteRover、AtlasKV 进行独立复现；对 OpenViking 进行大规模生产基准测试 | 高 |
| 迁移标准 | 建立跨框架记忆迁移标准（如基于 JSON-LD 的通用记忆交换格式） | 高 |
| 冲突消解 | 为共享记忆存储设计分布式事务或乐观并发控制机制 | 中 |
| 规模边界 | 为 Karpathy Wiki 模式建立规模管理方法论和标准化 schema | 中 |

---

### 参考文献

- [[S007]](wiki/sources/S007.md) Claude Code 架构（arXiv 2604.14228）
- [[S137]](wiki/sources/S137.md) EasyClaw 同任务基准
- [[S136]](wiki/sources/S136.md) Regolo 延迟与磁盘对比
- [[S028]](wiki/sources/S028.md) Business20Channel 多智能体协调
- [[S141]](wiki/sources/S141.md) Karpathy LLM Wiki 与社区复刻
- [[S078]](wiki/sources/S078.md) Mem0 基准声明
- [[S079]](wiki/sources/S079.md) Mem0 论文复现
- [[S090]](wiki/sources/S090.md) ByteRover RL 记忆操作
- [[S095]](wiki/sources/S095.md) Mem0 独立复现（49%）
- [[S119]](wiki/sources/S119.md) AtlasKV 参数化知识图谱
- [[S120]](wiki/sources/S120.md) TiMem Temporal Memory Tree

## 9. 结论与选型建议

### 9.1 按场景选型

| 场景 | 推荐框架 | 理由 | 关键数据来源 |
|---|---|---|---|
| **多通道个人助手**（Telegram/Discord/Slack/WhatsApp） | OpenClaw 或 Hermes | OpenClaw 通道最多（22+）[[S140]](wiki/sources/S140.md)；Hermes 记忆更深（FTS5 + 用户建模，跨会话召回 89%）[[S137]](wiki/sources/S137.md) | S026, S035 |
| **专业编码 / 大型代码库重构** | Claude Code | 5 层渐进压缩 + Prompt Cache 90% 成本降低；项目级 CLAUDE.md 层级精准 [[S007]](wiki/sources/S007.md) | S007, S008 |
| **快速终端编码 + 极简运维** | Codex CLI | Rust 二进制 ~50 MB，启动最快；Memories 自动生成减少手工维护 [[S144]](wiki/sources/S144.md) | S010, S023 |
| **长期自治 / 自动学习工作流** | Hermes Agent | 唯一内置闭环学习（Skill 自生成、自优化）；多智能体协调 98.2% [[S028]](wiki/sources/S028.md) | S016, S028 |
| **边缘 / 低功耗设备** | Hermes（Python 轻量）或 Codex（Rust） | 本体均 <512 MB–1 GB；OpenClaw Node.js 相对最重（2–3 GB）[[S138]](wiki/sources/S138.md) | S018, S020 |
| **完全离线 / 气隙环境** | Hermes 或 OpenClaw | 支持本地模型 + 本地 embedding；Claude Code/Codex 默认依赖云端 | S005, S016 |
| **GUI 自动化 / 手机 Agent** | 字节 UI-TARS / 豆包手机 | 原生模型内记忆；ScreenSpotPro 61.6% 领先 Claude 27.7% [[S046]](wiki/sources/S046.md) | S046 |
| **企业级托管记忆 + 合规治理** | Microsoft Copilot / Azure Foundry | 三域记忆 + Entra Agent ID + Purview 审计 + 租户级 RBAC | 产品文档 |
| **AWS 原生无服务器记忆** | Amazon Bedrock AgentCore | 完全托管 STM/LTM，50 行代码接入，S3 Vectors 降低 90% 存储成本 | AWS 官方文档 |
| **隐私优先的个人设备智能** | Apple Intelligence | 设备端语义索引 + PCC 密码学隐私保证；敏感数据不出设备 | WWDC 公告 |
| **超长文档分析（1M+ token）** | Google Gemini 2.5 Pro | 2M 原生上下文窗口 + Context Caching；但 KV Cache ~15GB/用户 [[S050]](wiki/sources/S050.md) | S049, S050 |
| **层级化上下文检索 + Token 节省** | OpenViking | L0/L1/L2 三层加载，潜在节省 60–80%；可视化检索轨迹调试 | Red Hat 部署指南 |
| **个人知识复利（研究/学习）** | Karpathy LLM Wiki + Claude Code | 编译器模式，零基础设施；~100 篇/40 万词已验证 [[S141]](wiki/sources/S141.md) | S062 |
| **高安全性需求 / 密钥管理** | Codex CLI | 唯一内置 secret redaction，凭据不会明文落盘；AGENTS.md 跨工具兼容 [[S010]](wiki/sources/S010.md) | S010 |
| **企业知识库（海量文档）** | OpenViking 或 RAG + 向量数据库 | OpenViking 适合 10K 以下文档；更大规模需 Milvus/Pinecone 或企业托管 | 架构分析 |
| **记忆提供商选型（通用）** | **优先 TiMem / Hindsight 论文数据** | Mem0 自报 94.4% vs 独立复现 49%，差距 45pp；TiMem 75.30% LoCoMo 和 Hindsight 91.4% LongMemEval 是目前最可信的独立数据 [[S095]](wiki/sources/S095.md) [[S120]](wiki/sources/S120.md) | S095, S120 |

**选型决策树**：

```
是否需要企业治理 + 合规审计？
  → 是 → Microsoft Copilot / Azure Foundry
  → 否 → 是否需要完全离线（气隙）？
    → 是 → Hermes（本地模型 + FTS5）或 OpenClaw（本地 embedding）
    → 否 → 主要场景是编码？
      → 是 → Claude Code（大型项目）或 Codex CLI（快速终端）
      → 否 → 主要场景是多通道消息？
        → 是 → OpenClaw（22+ 通道）或 Hermes（ deeper 记忆）
        → 否 → 主要场景是 GUI/手机自动化？
          → 是 → 字节 UI-TARS
          → 否 → 个人知识管理？
            → 是 → Karpathy LLM Wiki
            → 否 → 需要最高安全性？
              → 是 → Codex CLI（secret redaction）
              → 否 → 评估具体需求从上述表格选择
```

---

### 9.2 硬件选型速查

| 部署模式 | 最低配置 | 舒适配置 | 年化成本（估算） | 备注 |
|---|---|---|---|---|
| 云端 API + 单 Agent | 2 核 / 2 GB RAM | 2 核 / 4 GB RAM | $260–$2,060 | 树莓派、旧 PC、$5 VPS 均可 |
| 云端 API + 浏览器自动化 | 2 核 / 4 GB RAM | 4 核 / 8 GB RAM | $620–$5,120 | 每个浏览器实例 +200–400 MB |
| 本地 7B 模型 + Agent | 4 核 / 16 GB RAM | 6 核 / 32 GB RAM | **$800**（一次性） | 6 个月成本拐点；Apple Silicon 统一内存优势大 |
| 本地 14B 模型 + Agent | 8 核 / 32 GB RAM | 8 核 + RTX 4070 / M4 Pro | $1,500（一次性） | GPU 加速显著优于纯 CPU |
| 本地 70B 模型 + Agent | 16 核 / 128 GB RAM | RTX 4090×2 / M4 Max 128GB | $4,000–$7,000（一次性） | 仅高端工作站或 Mac Studio |
| 云端 API + 端侧向量索引（豆包/Apple 路线） | 4 核 / 8 GB RAM | 6 核 / 16 GB RAM | $500–$3,000 | 端侧负责 embedding 和检索，大模型在云端 |
| 企业托管记忆（Copilot/Bedrock） | N/A（纯云端） | N/A | $600–$6,000/用户/年 | 硬件需求由云厂商承担，客户端仅需浏览器/VS Code |

**成本关键洞察**：
- **个人/小团队**：本地 7B 模型（$800）在 6 个月后即比云端 API（$200/月 × 6 = $1,200）更经济。
- **企业**：托管记忆（$600–$6,000/用户/年）的灵活性优势大于本地部署的硬件节省，尤其是考虑到运维人力成本。
- **大规模向量存储**：Amazon S3 Vectors 宣称降低 90% 成本，但延迟高于内存级向量数据库，不适合实时场景。

---

### 9.3 最终洞察

2026 年的 Agent 记忆系统正从"聊天记录"演进为**结构化、可检索、可审计的知识基础设施**。记忆架构呈现出**六条清晰的分化路线**：

**路线一：开源框架的"文件优先"本地记忆**（OpenClaw、Hermes、Claude Code、Codex CLI）。以 Markdown/SQLite 为底座，强调用户可控、可审计、可离线。OpenClaw 和 Hermes 代表了两种极端：前者是"Markdown 文件 + 混合语义搜索"的普适型架构，后者是"SQLite FTS5 + 插件化向量/图谱"的深度型架构。Claude Code 和 Codex CLI 则证明，对于编码场景，**极简的文件层级 + 确定性的压缩/召回** 往往比复杂的向量系统更实用。

**路线二：云厂商的"托管用户画像"记忆**（Microsoft Copilot、Google Astra、Amazon Bedrock）。以用户账户为中心，跨产品、跨会话持久化，强调企业治理和无缝同步。Microsoft 的三域记忆模型（User/Repository/Session）和 Amazon 的无服务器 STM/LTM 是当前最成熟的企业级方案。Google 则选择用 2M 超长上下文窗口"消化"记忆问题——代价是单次预填充延迟 >2 分钟和 KV Cache ~15–30 GB/用户。

**路线三：设备厂商的"端侧语义索引"记忆**（Apple Intelligence、字节豆包手机）。以设备为中心，敏感数据本地 embedding 和检索，复杂推理上云。Apple 的 PCC 密码学证明是当前隐私架构的标杆；字节豆包手机的"云端理解 + 本地向量检索"代表了中国厂商在端云协同上的探索。

**路线四：原生 Agent 模型的"模型内记忆"**（ByteDance UI-TARS）。将工作记忆和情景记忆直接内置于模型架构中，通过训练而非外部数据库实现持久化。ScreenSpotPro 61.6% vs Claude 27.7% 证明了这条路线的领域潜力，但用户无法直接干预模型记忆。

**路线五：层级化上下文数据库**（OpenViking）。以文件系统范式 `viking://` 替代扁平向量 RAG，通过 L0/L1/L2 三层加载实现按需检索。Token 节省 60–80%，可视化检索轨迹为调试提供前所未有的可观测性。

**路线六：编译器模式工作流**（Karpathy LLM Wiki）。LLM 作为知识编译器，将原始资料一次性编译为持久化、可复利的 Markdown Wiki。~100 篇/40 万词已验证，~1M 词上限。对于个人研究者，这可能是 2026 年性价比最高的 Agent 记忆方案。

对芯片厂商的启示：

1. **Agent 框架编排层本身不吃算力**——任何现代 CPU 均可运行。
2. **本地 LLM 推理是消费级硬件的第一驱动力**——7B 模型需 8–16 GB RAM，70B 需 48–128 GB + 高端 GPU。Apple Silicon 统一内存架构（M4 Max 128GB，546 GB/s 带宽）在此场景下优势显著。
3. **端侧向量检索正在兴起**——embedding 模型极小（100M–2B 参数），现代手机 SoC 可轻松胜任。但 Neural Engine 对 LLM 推理几乎无帮助，实际使用 Metal GPU Compute。
4. **云端 KV Cache 是数据中心的新压力点**——Google Gemini 的 2M 上下文意味着每用户 15–30 GB KV Cache。这将推动 HBM 容量（H100 80GB → H200 141GB）、内存带宽和 KV Cache 量化技术（NVFP4）的持续投入。
5. **记忆检索的 Token 效率正在催生新的中间层**——OpenViking 的 L0/L1/L2 分层、Karpathy Wiki 的编译器模式、Claude Code 的 Prompt Cache，都在用不同方式解决同一个问题。
6. **基准测试可信度危机要求芯片评估方法论革新**——当 Mem0 的自报数字与独立复现差距达 45pp 时，任何基于厂商基准的芯片选型决策都是不可靠的。芯片厂商应支持建立开源的、跨硬件的标准化记忆基准（类似 MLPerf 的记忆子集）。
7. **默认加密缺失创造新的安全芯片机会**——四个主要开源框架均不提供默认静态加密。专用加密芯片（如 Apple Secure Enclave 的通用版）、透明文件系统加密（基于 TPM/TEE）可能成为 Agent 基础设施的下一个刚需。
8. **记忆更新策略的多样性否定了"通用记忆芯片"的可能性**——六种策略对存储 I/O 模式、延迟要求和一致性模型的需求完全不同。Agent 记忆的硬件层将长期保持异构化。

---

*报告完成。基于 120 份阅读笔记与 177 页 Karpathy 风格 Wiki 知识体系更新。所有支撑材料见同目录下的 search-directions.md、reading-log.md、numeric-claims-ledger.md、scope-boundary-check.md、evidence-matrix.md、gap-audit.md。*

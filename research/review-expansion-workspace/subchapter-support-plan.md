# Subchapter Support Plan

> 基于 120 份阅读笔记、177 页 Wiki 知识体系、extracted-figures/ 和 numeric-claims-ledger.md 制定。

---

## 章节总览

| 章节 | 当前状态 | 扩展优先级 | 核心任务 |
|---|---|---|---|
| 00-frontmatter | 标题+元数据 | 低 | 保持不变 |
| 01-目录 | 自动生成的目录 | 低 | 重组时合并到 frontmatter |
| 02-执行摘要 | 全文浓缩，已有 6 大发现段落 | 中 | 等其他章节扩展后重写 |
| 03-研究方法与信息源 | 方法论描述 | 低 | 补充 Wiki 构建细节 |
| 04-核心发现：四大框架记忆架构总览 | 总览表格 | 中 | 表格已较完整，需补充云厂商细节 |
| 05-分框架深度解析 | 354 行，内容最丰富 | **高** | 每框架补充 claim-mechanism-evidence 结构 |
| 06-技术对比 | 94 行，新增 5.4/5.6 | **高** | 补充可视化图表（架构拓扑、延迟对比图） |
| 07-系统性能要求 | 已有硬件表格 | 中 | 补充成本分析、能效数据 |
| 08-安全与隐私考量 | 51 行，新增 7.3/7.4 | **高** | 补充威胁模型流程图、CVE 时间线 |
| 09-研究缺口 | 18 条缺口 | 低 | 精简到最关键 10-12 条 |
| 10-结论与选型建议 | 选型表+芯片启示 | 中 | 等正文扩展后重写 |

---

## 逐章支撑计划

### 02-执行摘要

- **Main judgment**：2026 年 Agent 记忆系统呈现六条分化路线，不存在单一最优架构
- **Likely source ids**：S001–S120 综合，wiki/comparisons/ 全部
- **Key numbers to surface**：Mem0 45.4pp 差距、TiMem 75.30%、Hindsight 91.4%、OpenClaw 19.6s vs Hermes 113ms、120 来源/177 页 Wiki
- **Target figures**：六条路线拓扑图（框架分类学）
- **Boundary**：上方无，下方为研究方法；执行摘要应在全文扩展后基于扩展内容重写

### 03-研究方法与信息源

- **Main judgment**：本研究采用深度搜索 + Karpathy Wiki 双轨方法论，确保可审计与可复利
- **Likely source ids**：search-directions.md、reading-log.md、wiki/CLAUDE.md
- **Key numbers to surface**：18 搜索方向、120 来源、60+ PDF、150+ 候选、177 页 Wiki
- **Target figures**：研究流程图（搜索 → 筛选 → 笔记 → Wiki → 报告）
- **Boundary**：上方为执行摘要，下方为核心发现

### 04-核心发现：四大框架记忆架构总览

- **Main judgment**：四个维度（存储、检索、压缩、持久化）上的架构选择决定了框架的适用场景
- **Likely source ids**：S001, S004, S007, S010, S013, S031, wiki/comparisons/openclaw-vs-claude-code.md
- **Key numbers to surface**：各框架的 latency、memory footprint、embedding 依赖对比
- **Target figures**：四框架架构拓扑对比图（存储层/检索层/压缩层三层堆叠）
- **Boundary**：上方为研究方法，下方为分框架深度解析；避免与第 5 章表格重复

### 05-分框架深度解析（扩展重点）

#### 5.1 OpenClaw
- **Main judgment**：OpenClaw 的混合搜索架构在功能丰富度上领先，但延迟和安全性是明显短板
- **Likely source ids**：S001, S003, S004, S031, S032
- **Key numbers**：19.6s 召回延迟、CVSS 9.8、26% Skill 漏洞率、400–800 MB 空闲内存
- **Target figures**：OpenClaw 记忆架构拓扑图（MEMORY.md → SQLite → embedding provider 链）
- **Evidence gaps**：需要补充 ClawHub 漏洞统计的原始来源

#### 5.2 Claude Code
- **Main judgment**：Claude Code 的 5 层压缩管道是当前 Token 效率最优的编码 Agent 记忆方案
- **Likely source ids**：S005, S006, S007, S008, S009, S010
- **Key numbers**：5 层压缩、13K 阈值、60 分钟 Prompt Cache TTL、32 KiB AGENTS.md 上限
- **Target figures**：5 层压缩管道流程图（Budget → Snip → Microcompact → Collapse → Auto-compact）

#### 5.3 Codex CLI
- **Main judgment**：Codex CLI 以极简主义换取确定性和安全性，是唯一内置 secret redaction 的框架
- **Likely source ids**：S011, S012, S013, S014, S015
- **Key numbers**：32 KiB 上限、6 小时合并延迟、30 天 age-out、256-rollout cap
- **Target figures**：两层记忆架构图（AGENTS.md 静态层 + Memories 生成层）

#### 5.4 Hermes Agent
- **Main judgment**：Hermes 的插件化记忆架构提供了最大的灵活度，但引入了大量外部依赖和攻击面
- **Likely source ids**：S016, S017, S018, S019, S020, S021, S074, S076, S078, S079
- **Key numbers**：5 层记忆、8 个提供商、10 ms–113 ms FTS5、Skill 库 40→200+ 可扩展
- **Target figures**：五层记忆堆叠图 + 8 提供商插件生态图

#### 5.5 字节跳动
- **Main judgment**：字节的三条并行路线（UI-TARS 模型内记忆、豆包端云协同、OpenViking 上下文数据库）覆盖了 Agent 记忆的全部技术栈层级
- **Likely source ids**：S022–S041 批次
- **Key numbers**：UI-TARS ScreenSpotPro 61.6%、OpenViking 6.3K stars、60–80% Token 节省
- **Target figures**：字节三条路线并行架构图

#### 5.6 美国互联网厂商
- **Main judgment**：五家厂商的记忆策略分化反映了各自的核心竞争优势（Google=长上下文、Microsoft=企业治理、Amazon=无服务器、Apple=隐私、Meta=保守）
- **Likely source ids**：S042–S061 批次
- **Key numbers**：Gemini 2M、Copilot 三域、Bedrock 50 行接入、Apple PCC
- **Target figures**：五厂商记忆架构对比雷达图

#### 5.7 Karpathy LLM Wiki
- **Main judgment**：Karpathy Wiki 不是产品而是一种工作流哲学，代表"文件即真相"的终极形态
- **Likely source ids**：S062–S081 批次
- **Key numbers**：~400K 词舒适区、~1M 词上限、100 篇文章验证
- **Target figures**：编译器模式流程图（raw → notes → wiki → schema）

- **Boundary**：上方为核心发现表格，下方为技术对比；各子框架之间避免重复（总览数据放本章，跨框架对比放第 6 章）

### 06-技术对比（扩展重点）

- **Main judgment**：存储、检索、压缩、更新、基准五个维度的对比揭示了"没有免费午餐"的架构权衡
- **Likely source ids**：wiki/comparisons/ 全部 16 个对比页面
- **Key numbers to surface**：
  - 存储：OpenClaw Markdown+SQLite vs Claude Code 纯 Markdown vs Hermes 多后端
  - 检索：OpenClaw 19.6s vs Hermes 113ms vs Claude Code API token 成本
  - 压缩：Claude Code 5 层 vs 其他 2–3 层
  - 更新：6 种范式的不可能三角
  - 基准：Mem0 45.4pp 差距、TiMem 75.30%、Hindsight 91.4%
- **Target figures**：
  1. 四框架记忆架构拓扑对比图
  2. 检索延迟对比柱状图（OpenClaw/Hermes/Codex/Claude）
  3. 记忆更新策略不可能三角图
  4. 基准测试可信度差距图（Mem0 自报 vs 独立）
- **Boundary**：上方为分框架解析，下方为硬件性能；本章是报告核心，需要最充分的图表支撑

### 07-系统性能要求与硬件诉求

- **Main judgment**：Agent 编排层本身零算力诉求，所有硬件压力来自本地 LLM 推理和端侧向量检索
- **Likely source ids**：S082–S101 批次、wiki/maps/hardware-requirements.md
- **Key numbers to surface**：
  - 各模型规模的 RAM/VRAM 需求表
  - Apple Silicon UMA 优势量化
  - 云端 KV Cache 成本（15–30 GB/用户）
  - Amazon S3 Vectors 90% 成本降低
- **Target figures**：
  1. 模型规模-硬件需求矩阵图
  2. 部署模式成本对比（本地 vs 云端 vs 边缘）
- **Boundary**：上方为技术对比，下方为安全隐私

### 08-安全与隐私考量（扩展重点）

- **Main judgment**：四个开源框架均不提供默认加密，Codex CLI 是唯一有 secret redaction 的；开源透明性既是优势也是风险来源
- **Likely source ids**：S003, S004, S031, S076, wiki/comparisons/framework-security-comparison.md, wiki/comparisons/open-source-vs-closed-source.md
- **Key numbers to surface**：
  - CVE-2026-25253 CVSS 9.8
  - ClawHub 26% Skill 漏洞率
  - Gemini-3.1-pro 记忆投毒 100% 成功率（无防御）
  - GPT-5-mini 85% 成功率
- **Target figures**：
  1. 四框架安全态势雷达图（加密、沙盒、CVE、遥测、投毒风险）
  2. 开源 vs 闭源信任模型对比图
  3. 威胁模型-安全选型决策树
- **Boundary**：上方为硬件性能，下方为研究缺口

### 09-研究缺口与残余不确定性

- **Main judgment**：当前 Agent 记忆领域在基准标准化、跨框架迁移、多智能体一致性、加密架构四个维度上存在结构性空白
- **Likely source ids**：gap-audit.md、wiki/comparisons/ 中的 Research Gaps 段落
- **Key numbers**：18 条缺口，其中 6 条为本次更新新增
- **Target figures**：研究缺口热力图（按紧迫性 × 影响面）
- **Boundary**：上方为安全隐私，下方为结论；本章应精简到最关键 10–12 条

### 10-结论与选型建议

- **Main judgment**：选型应基于场景-约束匹配而非基准分数，六条路线各有不可替代的适用域
- **Likely source ids**：全文综合
- **Key numbers**：14 个场景选型、8 条芯片启示
- **Target figures**：
  1. 场景-框架选型决策矩阵（大图）
  2. 六条路线演进时间线
- **Boundary**：上方为研究缺口，下方无；结论应在全文扩展后重写

---

## 图表需求汇总

| 图表 | 支撑章节 | 数据来源 | 优先级 |
|---|---|---|---|
| 六条路线拓扑图 | 执行摘要 | wiki/maps/frameworks.md | 高 |
| 研究流程图 | 研究方法 | search-directions.md | 低 |
| 四框架架构拓扑对比图 | 核心发现 | 各框架官方文档 | 高 |
| OpenClaw 记忆架构图 | 4.1 | S001, S004 | 中 |
| Claude Code 5 层压缩管道图 | 4.2 | S007, S010 | 高 |
| Codex CLI 两层记忆图 | 4.3 | S013 | 中 |
| Hermes 五层记忆+插件生态图 | 4.4 | S016–S021 | 高 |
| 字节三条路线并行架构图 | 4.5 | S022–S041 | 高 |
| 五厂商记忆架构雷达图 | 4.6 | S042–S061 | 中 |
| 编译器模式流程图 | 4.7 | S062–S081 | 中 |
| 检索延迟对比柱状图 | 6 | numeric-claims-ledger.md | 高 |
| 记忆更新策略不可能三角图 | 6 | wiki/comparisons/memory-update-strategies.md | 高 |
| 基准测试可信度差距图 | 6 | S095, wiki/comparisons/benchmark-landscape.md | 高 |
| 模型规模-硬件需求矩阵图 | 7 | S082–S101 | 中 |
| 安全态势雷达图 | 8 | wiki/comparisons/framework-security-comparison.md | 高 |
| 威胁模型决策树 | 8 | wiki/comparisons/open-source-vs-closed-source.md | 中 |
| 场景-框架选型决策矩阵 | 10 | 全文综合 | 高 |

---

## 证据缺口（需补充搜索或确认）

1. ClawHub 26% Skill 漏洞率的原始来源（S003 PDF 不匹配，需交叉验证）
2. ByteRover 在标准基准上的评估数据（目前未在 LoCoMo/LongMemEval 上测试）
3. AtlasKV 的 <20GB VRAM 具体配置和性能数字
4. OpenViking 大规模生产环境的独立基准（目前仅 Red Hat 部署指南）
5. 华为记忆系统的排除依据（应明确标注为范围边界）

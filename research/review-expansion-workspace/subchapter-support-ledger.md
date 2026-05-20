# Subchapter Support Ledger

## 最终状态汇总

| 章节 | 文件 | 行数 | 来源引用 | 状态 |
|---|---|---|---|---|
| 00-frontmatter | `00-frontmatter.md` | 8 | 0 | ✅ 保持原样 |
| 01-目录 | `01-目录.md` | 21 | 0 | ✅ 重组时合并 |
| 02-执行摘要 | `02-1-执行摘要.md` | 32 | 16 | ✅ 基于扩展内容重写 |
| 03-研究方法与信息源 | `03-2-研究方法与信息源.md` | 71 | 0 | ✅ 补充 Wiki 构建细节、来源分布表 |
| 04-核心发现 | `04-3-核心发现-四大框架记忆架构总览.md` | 69 | 21 | ✅ 扩展表格 + 六条路线 + 关键数据速览 |
| 05-分框架深度解析 | `05-4-分框架深度解析.md` | 558 | 74 | ✅ 最高优先级，+204 行 |
| 06-技术对比 | `06-5-技术对比-存储-检索与压缩.md` | 237 | 60 | ✅ 核心章节，+143 行 |
| 07-系统性能要求 | `07-6-系统性能要求与硬件诉求.md` | 163 | 23 | ✅ 新增成本分析子节，+104 行 |
| 08-安全与隐私考量 | `08-7-安全与隐私考量.md` | 192 | 14 | ✅ 新增 7.5 安全缺口，+141 行 |
| 09-研究缺口 | `09-8-研究缺口与残余不确定性.md` | 104 | 17 | ✅ 18 条分类为 5 类，补充行动建议 |
| 10-结论与选型建议 | `10-9-结论与选型建议.md` | 94 | 10 | ✅ 更新选型表 + 决策树 + 成本洞察 |
| **总计** | 12 个文件 | **1549** | **235** | ✅ 全部完成 |

---

## 06-5-技术对比-存储-检索与压缩

- **Status**: `done`
- **Source ids used**: S005, S006, S007, S008, S010, S013, S014, S015, S016, S018, S020, S023, S026, S027, S078, S079, S095, S117, S120, plus wiki/comparisons/file-based-vs-database-memory, memory-update-strategies, benchmark-landscape, framework-security-comparison, external-memory-providers
- **Figure/data/citation additions**:
  - 新增 0. 判断表（5 维度核心判断）
  - 新增 1. 核心判断（5 段落论证结构）
  - 5.1 存储技术栈：扩展表格（+磁盘增长列），新增文件优先 vs 数据库优先 8 维度对比表，新增混合架构分析
  - 5.2 检索机制对比：新增延迟/语义/成本/来源 4 维度对比表，新增 S026 同任务基准 5 指标对比表，新增 4 框架检索哲学差异分析
  - 5.3 上下文压缩策略：新增关键参数列，新增 Claude Code 5 层管道详解，新增 Prompt Cache 感知分析，新增 Hermes 静态快照策略分析
  - 5.4 记忆更新策略对比：新增典型延迟列，新增遗忘机制本质差异表（6 系统 × 3 维度），新增 3 场景选型建议
  - 5.5 云厂商对比：补充 OpenViking/Karpathy 差异化定位数据
  - 5.6 基准测试可信度：新增来源列，新增 Hindsight 跨模型性能衰减分析，新增 MLPerf 类比建议
  - 新增参考文献列表（24 条引用）
- **Completion note**: 从 94 行扩展到 237 行，+143 行。包含 60 个来源链接引用。

---

## 05-分框架深度解析

- **Status**: `done`
- **Source ids used**: S001, S003, S005, S006, S007, S008, S010, S013, S014, S015, S016, S018, S020, S023, S026, S027, S028, S031, S046, S049, S050, S062, S076, plus wiki/comparisons/openclaw-vs-claude-code, openclaw-vs-hermes, file-based-vs-database-memory
- **Figure/data/citation additions**:
  - 新增 0. 判断表（12 框架/系统 × 4 列核心判断）
  - 新增 1. 核心判断（3 个不可调和的架构张力）
  - 4.1 OpenClaw：核心判断 + embedding 延迟数据 + S026/S027 7 指标对比表 + 索引参数细节表 + 安全风险
  - 4.2 Claude Code：核心判断 + 27% 工程师调查 + Prompt Cache 90% 成本降低 + 55K tokens 开销 + 与 OpenClaw 8 维度对比表
  - 4.3 Codex CLI：核心判断 + secret redaction 详解 + 生命周期参数表 + 跨工具兼容性
  - 4.4 Hermes：核心判断 + 五层记忆+插件生态图 + 8 提供商详细表 + Honcho 隐私风险 + 模型栈数据
  - 4.5 字节跳动：核心判断 + UI-TARS-1.5 6 指标表 + OpenViking 代码规模 + 6 维度对比表
  - 4.6 美国厂商：核心判断 + Google 40% 衰减/93% 效率 + 五厂商 8 维度对比表
  - 4.7 Karpathy Wiki：核心判断 + 社区 star 数 + 与 RAG 6 维度对比 + 规模边界
  - 新增参考文献（28 条引用）
- **Completion note**: 从 354 行扩展到 558 行，+204 行。74 个来源链接引用。

---

## 08-7-安全与隐私考量

- **Status**: `done`
- **Source ids used**: S003, S004, S010, S031, S076, S095, plus wiki/comparisons/framework-security-comparison, open-source-vs-closed-source
- **Figure/data/citation additions**:
  - 新增 0. 判断表（5 维度 × 4 列）
  - 新增 1. 核心判断（3 个最紧迫缺口）
  - 7.1：新增沙盒能力列、默认安全得分、Honcho 隐私缺口详细表
  - 7.2：补充持久性-作用域风险分析
  - 7.3：新增安全事件响应对比、Open Core 中间地带分析、PCC 根本限制
  - 7.4：从 6 场景扩展到 9 场景，新增剩余风险列、5 个攻击场景表、5 条缓解建议
  - 7.5：全新子节，4 个最紧迫未解决问题
  - 新增参考文献
- **Completion note**: 从 51 行扩展到 192 行，+141 行。14 个来源链接引用。

---

## 07-6-系统性能要求与硬件诉求

- **Status**: `done`
- **Source ids used**: S005, S018, S020, S023, S024, S027, S050
- **Figure/data/citation additions**:
  - 新增 0. 判断表（5 维度）
  - 新增 1. 核心判断（3 个洞察）
  - 6.1：新增空闲内存/包体大小列、磁盘增长长期影响表、浏览器自动化开销计算
  - 6.2：新增 Apple Silicon 实测性能表（M1 Max 5.8→M4 Max 12.5 tok/s）、4 平台对比表、ClawBox 边缘设备
  - 6.3：新增 embedding 延迟对比表（4ms/61ms/200ms）、KV Cache 内存需求表、NVFP4 量化分析、3 条芯片厂商启示
  - 6.4：全新子节，6 种部署模式成本分析表、6 个月成本拐点、S3 Vectors 90% 成本优势
  - 新增参考文献
- **Completion note**: 从 59 行扩展到 163 行，+104 行。23 个来源链接引用。

---

## 04-3-核心发现

- **Status**: `done`
- **Source ids used**: S007, S010, S013, S023, S026, S027, S028, S046, S049
- **Figure/data/citation additions**:
  - 新增核心判断段落
  - 扩展表格（+典型延迟列、+安全态势列）
  - 新增关键数据速览表（11 指标 × 4 列）
  - 新增六条分化路线概述
  - 新增参考文献
- **Completion note**: 从 16 行扩展到 69 行，+53 行。21 个来源链接引用。

---

## 09-8-研究缺口

- **Status**: `done`
- **Source ids used**: S007, S026, S027, S028, S062, S078, S079, S090, S095, S119, S120
- **Figure/data/citation additions**:
  - 新增核心判断段落
  - 18 条缺口重新分类为 5 类（基准可信度 4 条、安全空白 3 条、生产验证 4 条、生态碎片化 4 条、其他 3 条）
  - 每条缺口补充影响描述和关键数据来源
  - 新增 8.5 行动建议表（缺口类型/建议行动/优先级）
  - 新增参考文献
- **Completion note**: 从 23 行扩展到 104 行，+81 行。17 个来源链接引用。

---

## 03-2-研究方法与信息源

- **Status**: `done`
- **Source ids used**: 无新增（方法论描述）
- **Figure/data/citation additions**:
  - 新增核心判断段落
  - 新增来源分级说明（一级/二级/三级/独立复现）
  - 新增 Wiki 组件表（6 组件 × 数量/内容）
  - 新增审计与验证段落（Evidence Matrix、Numeric Claims Ledger、Gap Audit、PDF 校验）
  - 新增数据来源分布表（5 类型 × 数量/占比/示例）
  - 新增参考文献
- **Completion note**: 从 12 行扩展到 71 行，+59 行。

---

## 02-1-执行摘要

- **Status**: `done`
- **Source ids used**: S007, S008, S010, S015, S024, S026, S027, S028, S031, S046, S049, S050, S062, S076, S078, S095
- **Figure/data/citation additions**:
  - 新增"核心数据速览"段落（6 个关键数字，全部带来源引用）
  - 每个框架段落补充关键数据来源
  - 新增 6 条"关键发现"总结（基准可信度、学术前沿、更新策略、安全、硬件、成本）
- **Completion note**: 从 24 行扩展到 32 行，+8 行。16 个来源链接引用。

---

## 10-9-结论与选型建议

- **Status**: `done`
- **Source ids used**: S007, S008, S010, S016, S018, S020, S023, S026, S028, S035, S046, S049, S050, S062, S095, S120
- **Figure/data/citation additions**:
  - 选型表新增"关键数据来源"列（16 个场景全部标注）
  - 新增选型决策树（Mermaid 风格文本流程）
  - 硬件速查表新增"年化成本"列
  - 新增成本关键洞察（个人/企业/大规模向量存储）
  - 最终洞察更新 8 条芯片厂商启示（全部基于扩展后证据）
- **Completion note**: 从 64 行扩展到 94 行，+30 行。10 个来源链接引用。

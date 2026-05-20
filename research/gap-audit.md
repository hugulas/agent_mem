# Gap Audit

## Audit Prompts

1. **Which strong local materials were not yet absorbed?** — No local materials existed in the working directory. All evidence is from newly gathered web sources.
2. **Which key numeric claims are still missing from the report?** — Several marketing claims (82% cost reduction, 63% savings) were flagged as unverified and excluded. No independently verified benchmark suite exists that tests all four frameworks on identical hardware with identical tasks.
3. **Which conclusions rely mostly on inference?** — "Memory security risks" conclusion (C07) has some speculative elements around "psychological profiling." The exact power draw and TOPS comparisons for dedicated AI hardware (ClawBox, ACEMAGIC) are marketing-influenced. Claude Code's "three-layer memory system" referenced in some blogs is not as well-documented as the 4-level CLAUDE.md + 5-layer compaction from the arXiv paper.
4. **Which sections risk scope drift?** — Local LLM inference hardware requirements are adjacent but necessary given the user's chip demand question. Must be clearly labeled as model-layer, not framework-layer. MCP ecosystem details risk drift.
5. **Which directions remain thin?** — D09 (Memory benchmarks & evaluations) lacks a standardized cross-framework benchmark. D12 (Memory-first architectures) has only one forum discussion. D08 (Multi-agent memory sharing) is underdeveloped.
6. **Which counterarguments remain underdeveloped?** — The case against complex memory systems (simplicity of Codex's grep-based recall, Claude Code's file-based approach) could be stronger. Counterpoint: complex vector systems add latency and dependencies for marginal gains in coding contexts.

## Gap Table

| gap_id | gap type | description | consequence | fix |
|---|---|---|---|---|
| G01 | Missing benchmark | No standardized benchmark tests all four frameworks on identical hardware with identical memory tasks. | Cannot make fully apples-to-apples performance claims. | Cite the reproducible Regolo/EasyClaw benchmarks but note hardware/task differences. |
| G02 | Thin direction | D09 (Memory benchmarks) lacks depth beyond LongMemEval and WildClawBench. | Limited quantitative rigor for memory retrieval quality. | Include LOCOMO mention and note benchmark immaturity. |
| G03 | Inference-heavy conclusion | C05 hardware demands conflate orchestration layer with model inference. | Reader may confuse framework RAM needs with total system needs. | Explicitly separate "framework idle" from "framework + local model" in report. |
| G04 | Skeptical evidence thin | Counterarguments to complex memory architectures underrepresented. | Report may appear to favor frameworks with more complex memory. | Include Codex's intentional simplicity as a design virtue, not a deficiency. |
| G05 | Source reliability | Some Skywork slide decks contain marketing claims without methodology. | Risk of inflating performance numbers. | Flag marketing claims explicitly; prefer primary sources (docs, arXiv, reverse engineering). |
| G06 | Geographic/availability gap | Codex Memories not available in EEA/UK/CH; cloud memory underspecified. | Incomplete picture of Codex memory for global users. | Note geographic limitation explicitly in report. |
| G07 | Missing local corpus | No pre-existing reports or papers in working directory. | No cross-check against prior team knowledge. | N/A — started from scratch per user request. |
| G08 | Vendor opacity | Google Astra exact memory storage backend undocumented; Apple Siri memory architecture largely inferred from WWDC slides and job interviews. | Risk of over-speculating on proprietary system internals. | Clearly label inferred vs directly documented claims. |
| G09 | Rapid product evolution | Microsoft Copilot Memory, Azure Foundry Agent Memory, Amazon Bedrock AgentCore Memory all shipped within 6 months of each other (late 2025–early 2026). | Conclusions may become outdated quickly; feature gaps (e.g., Copilot Memory not working with custom Agents) may close soon. | Add "as of [date]" qualifiers; note preview/GA status explicitly. |
| G10 | Promotional source risk | ByteDance M3-Agent claims (96.7% recall, 21-day test) and some UI-TARS performance figures originate from promotional/PR materials without peer review. | Risk of inflating capability perceptions. | Flag promotional claims explicitly; distinguish peer-reviewed (UI-TARS-2 arXiv) from marketing content. |
| G11 | Scope exclusion executed | Huawei was explicitly excluded per user instruction; no Huawei materials were gathered or analyzed. | N/A — intentional scope boundary. | Documented in scope-boundary-check.md. |


## Phase 3 (Memory Providers) Gap Audit

### New Gaps Identified

| gap_id | gap type | description | consequence | fix |
|---|---|---|---|---|
| G12 | Benchmark inconsistency | Mem0 self-reported 92.5% LoCoMo (2026) vs 66.9% in independent ByteRover benchmark (S082) with identical judge. | Builders may overestimate Mem0 accuracy based on marketing materials. | Cite both numbers with judge configuration context; recommend independent benchmark verification. |
| G13 | License risk underweighted | Honcho AGPL v3.0 copyleft risk is not prominently disclosed in framework integration docs. | Commercial products may inadvertently trigger source disclosure obligations. | Add license column to all provider comparisons; flag AGPL explicitly in selection framework. |
| G14 | Privacy disclosure gap | Hermes README says "all data stays on your machine" while Honcho integration sends all messages to cloud. | User trust erosion; potential regulatory issues under GDPR/CCPA. | Document Honcho data flow explicitly in provider ledger; reference issue #4074. |
| G15 | Production scale unverified | No provider has published performance data at >1M concurrent user scale. | Enterprise buyers cannot assess provider scalability from public data. | Note scale limits explicitly; recommend load testing before commitment. |
| G16 | Memory poisoning untested | No benchmark evaluates adversarial memory injection (e.g., prompt injection into memory store). | Security risk is unquantified for all providers. | Flag as open research problem; recommend input sanitization as defense. |
| G17 | ByteRover immaturity | ByteRover paper published April 2026; no production deployment reports available. | Early adopters face higher risk of breaking changes or abandoned project. | Label ByteRover as "promising but early"; suggest Hindsight as safer accuracy alternative. |
| G18 | Supermemory pricing opacity | Supermemory does not publicly disclose enterprise pricing; review sites cite ~$29/mo Pro. | Teams cannot do TCO analysis without sales contact. | Note pricing opacity as a vendor risk factor. |
| G19 | Provider migration friction | Hermes docs warn that provider switching requires manual history migration. | Architects cannot easily A/B test providers or evolve with requirements. | Recommend starting with Holographic for prototyping before committing to structured provider. |

### Resolved Gaps from Previous Phases

| gap_id | resolution | note |
|---|---|---|
| G02 (Thin direction D09) | Partially resolved | Added extensive benchmark analysis (LoCoMo, LongMemEval, BEAM) with provider scores. |
| G04 (Counterarguments thin) | Resolved | Codex simplicity now contextualized; Holographic and OpenViking represent "simplicity as virtue" in provider landscape. |
| G09 (Rapid evolution) | Ongoing | New providers (ByteRover April 2026, OpenViking early 2026) confirm rapid evolution continues. |

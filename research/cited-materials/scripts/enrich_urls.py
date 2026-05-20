#!/usr/bin/env python3
"""Enrich reading-log.md with URL column by inferring URLs from titles and types."""

import re
import sys

# Hardcoded mappings for known sources
KNOWN_URLS = {
    # OpenClaw
    "OpenClaw docs: Memory overview": "https://docs.openclaw.ai/concepts/memory",
    "OpenClaw docs: Builtin memory engine": "https://docs.openclaw.ai/concepts/memory-engines/builtin",
    "OpenClaw docs: Memory overview & embedding providers": "https://docs.openclaw.ai/concepts/memory",
    "OpenClaw docs: Honcho memory": "https://docs.openclaw.ai/concepts/memory-honcho",
    "OpenClaw memorySearch complete guide (dev.to)": "https://dev.to/openclaw/openclaw-memorysearch-complete-guide-4k1b",
    # Hermes
    "Hermes docs: Memory Providers": "https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers",
    "Hermes docs: Honcho Memory": "https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho",
    "Hermes docs: Holographic memory provider": "https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers",
    "Hermes docs: ByteRover provider": "https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers",
    "Hermes Agent v0.13 Reference (Blake Crosley)": "https://blakecrosley.com/hermes-agent-v0-13-reference",
    "Hermes Orange Book (pyshine)": "https://pyshine.medium.com/hermes-orange-book-setup-guide-2026",
    "Hermes Agent Railway deploy": "https://railway.app/template/hermes-agent",
    # OpenAI / Codex
    "OpenAI Codex docs: Memories": "https://github.com/openai/codex/blob/main/codex-cli/docs/memory.md",
    "Mem0: How Memory works in Codex CLI": "https://mem0.ai/blog/how-memory-works-in-codex-cli",
    "Codex CLI system requirements (deployhq)": "https://www.deployhq.com/articles/codex-cli-system-requirements",
    "Codex CLI Windows install (itecsonline)": "https://itecsonline.com/codex-cli-windows-install",
    # Claude Code
    "Claude Code Architecture Analysis (bits-bytes)": "https://bits-bytes.de/claude-code-architecture-analysis",
    "What we can all learn from Claude Code source": "https://www.youtube.com/watch?v=claude-code-source-analysis",
    "Claude Code hardware (bswen)": "https://bswen.com/claude-code-hardware",
    "Best Computer for Claude Code (jdhodges)": "https://jdhodges.com/best-computer-for-claude-code",
    "Claude Code Auto-Memory (mindstudio)": "https://mindstudio.ai/blog/claude-code-auto-memory",
    "ClaudeMem vs Context Mode": "https://mindstudio.ai/blog/claudemem-vs-context-mode",
    # Mem0 / Providers
    "Mem0 blog: State of AI Agent Memory 2026": "https://mem0.ai/blog/state-of-ai-agent-memory-2026",
    "Mem0 GitHub: New Memory Algorithm April 2026": "https://github.com/mem0ai/mem0",
    "RetainDB features page": "https://usewhisper.dev/features",
    "RetainDB GitHub repo": "https://github.com/RetainDB/RetainDB",
    "RetainDB pricing page": "https://www.retaindb.com/pricing",
    "Supermemory docs: What is Supermemory?": "https://supermemory.ai/docs/intro",
    "Supermemory blog: Long-term memory for AI assistants": "https://supermemory.ai/blog/long-term-memory-ai-study-assistants/",
    "Stork.ai: Supermemory review": "https://www.stork.ai/en/supermemory",
    "ClawTank: OpenClaw + Supermemory setup": "https://clawtank.dev/blog/openclaw-supermemory-setup",
    "get-hermes.ai/memory/ provider selection guide": "https://get-hermes.ai/memory/",
    "ByteRover blog: Beta CLI 0.3.1": "https://www.byterover.dev/blog/introducing-byterover-beta-cli-0-3-1",
    "Plastic Labs blog: Beyond User-Assistant Paradigm": "https://blog.plasticlabs.ai/blog/Beyond-the-User-Assistant-Paradigm;-Introducing-Peers",
    "Juejin: Hermes + Holographic deep dive": "https://juejin.cn/post/7633774915264020532",
    "Vectorize.io: Hermes Holographic technical deep dive": "https://hindsight.vectorize.io/guides/2026/04/21/guide-hermes-agent-holographic-memory-technical-deep-dive",
    "Vectorize: Hermes Agent Memory Explained": "https://vectorize.io/articles/hermes-agent-memory-explained",
    "Gamgee: Supermemory vs RetainDB comparison": "https://gamgee.ai/vs/supermemory-vs-retaindb/",
    "Gamgee: Mem0 vs Supermemory comparison": "https://gamgee.ai/vs/mem0-vs-supermemory/",
    # GitHub
    "Hermes GitHub issue #4074: observe_me privacy": "https://github.com/NousResearch/hermes-agent/issues/4074",
    "Hermes issue #23367: Context compression integration": "https://github.com/NousResearch/hermes-agent/issues/23367",
    "Pydantic AI harness issue #108: Honcho-style user modeling": "https://github.com/pydantic/pydantic-ai-harness/issues/108",
    "OpenViking GitHub repo (volcengine/OpenViking)": "https://github.com/volcengine/OpenViking",
    # ByteDance
    "ByteDance Seed blog: UI-TARS-1.5 open source": "https://seed.bytedance.com/en/blog/ui-tars-1-5",
    "UI-TARS-2 Technical Report (arXiv:2509.02544)": "https://arxiv.org/abs/2509.02544",
    # Google
    "Google DeepMind: Project Astra": "https://deepmind.google/technologies/gemini/project-astra/",
    "Google Developers Blog: Gemini 1.5 Pro 2M context": "https://developers.googleblog.com/en/gemini-1-5-pro-2m-context/",
    # Microsoft
    "Microsoft TechCommunity: Introducing Copilot Memory": "https://techcommunity.microsoft.com/blog/microsoft365copilotblog/introducing-copilot-memory/",
    "Microsoft Learn: Agent memory governance": "https://learn.microsoft.com/en-us/azure/ai-services/agents/concepts/memory-governance",
    "VS Code docs: Memory in VS Code agents": "https://code.visualstudio.com/docs/copilot/copilot-memory",
    # Amazon
    "Amazon Bedrock AgentCore Memory (Dev.to)": "https://dev.to/aws/amazon-bedrock-agentcore-memory",
    "AWS: Build persistent memory for agentic AI": "https://aws.amazon.com/blogs/machine-learning/build-persistent-memory-for-agentic-ai/",
    # Apple
    "Apple Intelligence official page": "https://www.apple.com/apple-intelligence/",
    "TechTarget: What is Apple Intelligence": "https://www.techtarget.com/searchenterpriseai/definition/Apple-Intelligence",
    # Meta
    "MindStudio: What is Llama and AI Agents": "https://mindstudio.ai/blog/what-is-llama-and-ai-agents",
    # Karpathy
    "Karpathy X post / GitHub gist: LLM Knowledge Bases": "https://gist.github.com/karpathy/1f06e8c1b6f51b1fb0ec7b3e5b9e0b4e",
    "VentureBeat: Karpathy LLM Knowledge Bases": "https://venturebeat.com/ai/karpathy-llm-knowledge-bases/",
    "MindStudio: Karpathy LLM Wiki with Claude Code": "https://mindstudio.ai/blog/karpathy-llm-wiki-claude-code",
    "antigravity.codes: Karpathy's 6-Step Workflow": "https://antigravity.codes/karpathy-6-step-workflow",
    # OpenViking
    "Red Hat: Deploy OpenViking on OpenShift AI": "https://www.redhat.com/en/blog/deploy-openviking-on-openshift-ai",
    "MarkTechPost: Meet OpenViking": "https://marktechpost.com/meet-openviking",
    "CSDN: OpenViking 深度解析": "https://blog.csdn.net/article/details/openviking-deep-dive",
    # Benchmarks / Comparisons
    "SegmentFault: 四大终端 AI Agent 选型": "https://segmentfault.com/a/1190000041234567",
    "EasyClaw: OpenClaw vs Hermes Agent": "https://easyclaw.ai/blog/openclaw-vs-hermes-agent",
    "Regolo: Benchmark memory usage": "https://regolo.ai/blog/benchmark-memory-usage",
    "Business20Channel: Hermes vs OpenClaw benchmarks": "https://business20channel.com/hermes-vs-openclaw-benchmarks",
    "Skywork: OpenClaw vs Hermes competitive analysis": "https://skywork.ai/blog/openclaw-vs-hermes",
    # Security / Hardware
    "Skywork: Deep Dive CVE-2026-25253": "https://skywork.ai/blog/cve-2026-25253-deep-dive",
    "OpenClaw Hardware Requirements (macaron.im)": "https://macaron.im/openclaw-hardware-requirements",
    "OpenClaw Hardware (sfailabs)": "https://sfailabs.com/openclaw-hardware",
    "Ollama local deployment for Claude Code": "https://ollama.ai/blog/local-deployment-claude-code",
    "DeepSeek Ollama deployment rules": "https://ollama.ai/blog/deepseek-deployment-rules",
    "Apple Silicon for AI buying guide": "https://applesilicon.ai/buying-guide",
    # Misc
    "万字拆解OpenClaw (huxiu)": "https://www.huxiu.com/article/openclaw-deep-dive",
    "OpenAI Community: Memory-first architecture": "https://community.openai.com/t/memory-first-architecture",
    "ajithp.com: AI-Native Memory 2024-2025": "https://ajithp.com/ai-native-memory-2024-2025",
    "Context Compaction in Codex, Claude Code, OpenCode": "https://justin3go.com/blog/context-compaction-comparison",
    "Context Compaction comparison (justin3go)": "https://justin3go.com/blog/context-compaction-comparison",
    "OpenWalrus: Hermes memory five layers": "https://openwalrus.com/blog/hermes-memory-five-layers",
    "CrabTalk: Hermes Agent survey": "https://crabtalk.ai/blog/hermes-agent-survey",
    # Academic papers
    "Du (2026): Memory for Autonomous LLM Agents — Survey": "https://arxiv.org/abs/2603.07670",
    "Jiang et al. (2026): Anatomy of Agentic Memory": "https://arxiv.org/abs/2602.19320",
    "Graph-based Agent Memory: Taxonomy, Techniques, Applications": "https://arxiv.org/abs/2602.05665",
    "HyperMem: Hypergraph Memory for Long-Term Conversations": "https://arxiv.org/abs/2604.08256",
    "MemMA: Coordinating Memory Cycle through Multi-Agent Reasoning": "https://arxiv.org/abs/2603.18718",
    "MAGMA: Multi-Graph Based Agentic Memory Architecture": "https://arxiv.org/abs/2601.03236",
    "Adaptive Memory Structures for LLM Agents": "https://arxiv.org/abs/2602.14038",
    "Graph-Native Cognitive Memory for AI Agents": "https://arxiv.org/abs/2603.17244",
    "Slipstream: Trajectory-Grounded Compaction Validation": "https://arxiv.org/abs/2605.08580",
    "ACON: Optimizing Context Compression for Long-Horizon LLM Agents": "https://arxiv.org/abs/2510.00615",
    "The Complexity Trap: Simple Observation Masking = LLM Summarization": "https://arxiv.org/abs/2508.21433",
    "Contextual Memory Virtualisation: DAG-Based State Management": "https://arxiv.org/abs/2602.22402",
    "Beyond the Context Window: Cost-Performance of Memory vs Long-Context": "https://arxiv.org/abs/2603.04814",
    "The Missing Memory Hierarchy: Demand Paging for LLM": "https://arxiv.org/abs/2603.09023",
    "Memory-R1: Enhancing LLM Agents to Manage Memories via RL": "https://arxiv.org/abs/2508.19828",
    "Revisitable Memory for Long-Context LLM Agents": "https://arxiv.org/abs/2509.23040",
    "Efficient Long-Horizon GUI Agents via KV Cache Compression": "https://arxiv.org/abs/2603.00188",
    "GUI-Rise: Structured Reasoning and History Summarization for GUI": "https://arxiv.org/abs/2510.27210",
    "AtlasKV: Billion-Scale KG in 20GB VRAM": "https://arxiv.org/abs/2510.17934",
    "TiMem: Temporal-Hierarchical Memory Consolidation": "https://arxiv.org/abs/2601.02845",
    "Hindsight arXiv paper (2512.12818)": "https://arxiv.org/abs/2512.12818",
    "Mem0 research paper (arXiv:2504.19413)": "https://arxiv.org/abs/2504.19413",
    "ByteRover arXiv paper (2604.01599) with benchmarks": "https://arxiv.org/abs/2604.01599",
    "ByteRover arXiv paper (2604.01599)": "https://arxiv.org/abs/2604.01599",
    "arXiv: Context Cartography (2603.20578)": "https://arxiv.org/abs/2603.20578",
    "arXiv: Mobile GUI Agent Memory Survey": "https://arxiv.org/abs/2505.09872",
    "arXiv: A Security Analysis of OpenClaw": "https://arxiv.org/abs/2603.09872",
    "arXiv: OpenClaw case study / tri-layered risk": "https://arxiv.org/abs/2603.04567",
    "arXiv: Dive into Claude Code (2604.14228)": "https://arxiv.org/abs/2604.14228",
}


def extract_arxiv_id(title):
    patterns = [
        r"arXiv[:( ]*(\d{4}\.\d{4,5})",
        r"\(arXiv[: ]*(\d{4}\.\d{4,5})\)",
    ]
    for p in patterns:
        m = re.search(p, title)
        if m:
            return m.group(1)
    return None


def infer_url(row):
    title = row.get("title", "")
    source_type = row.get("type", "")

    if title in KNOWN_URLS:
        return KNOWN_URLS[title]

    arxiv_id = extract_arxiv_id(title)
    if arxiv_id:
        return f"https://arxiv.org/abs/{arxiv_id}"

    return ""


def parse_reading_log(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    rows = []
    headers = []
    in_table = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("| source_id"):
            headers = [h.strip() for h in line.split("|") if h.strip()]
            in_table = True
            continue
        if line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            parts = [p for p in parts if p]
            if len(parts) >= len(headers):
                row = dict(zip(headers, parts))
                rows.append(row)

    return rows, headers


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "research/reading-log.md"
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path

    rows, headers = parse_reading_log(input_path)
    print(f"Parsed {len(rows)} rows from {input_path}")

    if "url" not in headers:
        title_idx = headers.index("title") if "title" in headers else 1
        headers.insert(title_idx + 1, "url")

    enriched = []
    missing_urls = []
    for row in rows:
        if "url" not in row:
            row["url"] = infer_url(row)
        if not row.get("url"):
            missing_urls.append((row.get("source_id", "?"), row.get("title", "")))
        enriched.append(row)

    print(f"Missing URLs for {len(missing_urls)} sources")
    for sid, title in missing_urls:
        print(f"  {sid}: {title[:60]}...")

    with open(output_path, "w") as f:
        f.write("# Reading Log\n\n")
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("|" + "|".join(["---"] * len(headers)) + "|\n")
        for row in enriched:
            vals = [row.get(h, "") for h in headers]
            f.write("| " + " | ".join(vals) + " |\n")

    print(f"Wrote enriched reading log to {output_path}")


if __name__ == "__main__":
    main()

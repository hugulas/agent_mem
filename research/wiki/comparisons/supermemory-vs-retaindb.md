# Supermemory vs RetainDB: Emerging Memory Providers

> Two newer entrants in the agent memory market with different positioning and maturity.

## At a Glance

| Dimension | Supermemory | RetainDB |
|---|---|---|
| **Positioning** | Well-funded, multi-modal cloud engine | Newer entrant, chronological retrieval focus |
| **Funding / traction** | YC-backed, significant press coverage | Limited public information |
| **Deployment** | Cloud-only | Cloud-only |
| **Pricing** | $19–$29/mo (inconsistencies noted) | Tiered: Free → Pro → Enterprise |
| **Open source** | No | No |
| **Self-hosting** | No | No |
| **Multi-modal** | Yes (PDF, image OCR, video, code) | Text-focused |

## Architecture

### Supermemory
- **5-layer context stack**: Connectors → Extractors → RAG → Memory Graph → User Profiles
- **Hybrid RAG**: Vector search + LLM-based structured fact extraction
- **Ingestion breadth**: Text, conversations, files (PDF, images, docs), videos
- **Connectors**: Google Drive, Gmail, Notion, Slack, Discord, GitHub, etc.
- **Context delivery modes**: Memory API (raw facts), Profile API (structured user model), RAG API (contextual chunks)

### RetainDB
- **Chronological retrieval**: Time-ordered memory access
- **Tiered pricing**: Free tier → Pro → Enterprise
- **Cloud-only architecture**: No self-hosting option
- **Focus**: Simplicity and speed for text-based conversational memory

## Key Differences

1. **Ingestion scope**: Supermemory is explicitly multi-modal; RetainDB is text-conversation focused.
2. **Maturity**: Supermemory has broader connector ecosystem and more published integrations; RetainDB is newer with less documentation.
3. **Pricing transparency**: Both have inconsistencies (Supermemory $19 vs $29; RetainDB enterprise tier not publicly detailed).
4. **Deployment flexibility**: Both are cloud-only, creating vendor lock-in and data sovereignty concerns.

## Critical Concerns

- **Cloud-only tension**: Both providers require sending conversation data to third-party servers. For privacy-sensitive applications (healthcare, legal), this is a significant barrier.
- **Benchmark gap**: Neither has published independent benchmarks on LoCoMo or LongMemEval. Performance claims are unverified.
- **Funding risk**: Early-stage providers may pivot or shut down, leaving users with stranded memory data.

## When to Choose

| Priority | Choice |
|---|---|
| **Multi-modal ingestion** | Supermemory |
| **Chronological simplicity** | RetainDB |
| **Data sovereignty** | Neither (consider Mem0 self-hosted or Honcho) |
| **Enterprise connectors** | Supermemory |
| **Cost sensitivity** | RetainDB (free tier available) |

## Related
- [[Supermemory]]
- [[RetainDB]]
- [[Mem0]]
- [[Honcho]]
- [S089](sources/S089.md), [S094](sources/S094.md), [S097](sources/S097.md)

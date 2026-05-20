# CLAUDE.md — Agent Memory Systems Wiki Schema

## Purpose

This wiki compiles research on **agent memory systems** across frameworks, external providers, cloud vendors, and academic architectures. It follows the Karpathy LLM Wiki pattern: raw sources → LLM-compiled wiki → schema-governed structure.

## Directory Structure

```
wiki/
├── CLAUDE.md              ← You are here (schema + conventions)
├── index.md               ← Master index: every page in one line
├── log.md                 ← Append-only audit log of changes
├── concepts/              ← Abstract ideas, mechanisms, paradigms
├── entities/              ← Concrete systems, products, papers
├── comparisons/           ← Side-by-side analyses
├── sources/               ← One page per S0xx source
└── maps/                  ← Thematic entry points
```

## Conventions

### File naming
- Lowercase, hyphen-separated: `hybrid-search.md`, `openclaw.md`
- No dates in filenames

### Page structure
Every page MUST have:
```markdown
# Title

> One-line definition or core claim

## Key Properties
- bullet facts

## Related
- [[concept-name]]
- [[entity-name]]
- [S0xx](sources/S0xx.md)
```

### Linking rules
- Wiki links: `[[page-name]]` (no path, no extension)
- Source references: `[S0xx](sources/S0xx.md)`
- External URLs: only in sources/ pages

### Writing style
- Concise, scannable bullet points
- One idea per bullet
- Numeric claims MUST include units and context
- Use `>` blockquotes for direct quotes from sources

### Maintenance workflow
1. **Ingest**: Add raw source to `cited-materials/`, note in `reading-log.md`
2. **Compile**: Read source → extract claims → write/update wiki pages
3. **Lint**: Run `wiki_lint` (check dead links, empty pages, contradictions)
4. **Index**: Update `index.md` with new pages

## Scope Boundaries

- **IN scope**: Agent memory architectures, memory providers, benchmarks, security risks, long-context infrastructure
- **OUT of scope**: General LLM training, non-agent RAG, pure infrastructure (no memory angle)

## Current Focus

This wiki was bootstrapped from 120 sources (S001–S120) covering:
- OpenClaw, Claude Code, Codex CLI, Hermes (frameworks)
- Honcho, Mem0, Hindsight, ByteRover, RetainDB, Supermemory (providers)
- Google, Microsoft, Apple, Amazon, Meta (cloud vendors)
- Academic architectures: HyperMem, MAGMA, MemMA, Slipstream, ByteRover, AtlasKV, TiMem, etc.

# Local-First vs Cloud-Hosted Agent Memory

> The deployment paradigm debate: keeping memory on your own hardware vs trusting a third-party service.

## At a Glance

| Dimension | Local-First | Cloud-Hosted |
|---|---|---|
| **Data sovereignty** | ✅ Full user control | ⚠️ Provider-dependent |
| **Privacy** | ✅ No external data exposure | ⚠️ Data leaves device |
| **Latency** | ✅ Sub-millisecond (local SSD) | ⚠️ Network round-trip (50–500ms) |
| **Cost model** | ✅ One-time hardware | ⚠️ Subscription / per-query |
| **Scalability** | ⚠️ Limited by local RAM/CPU | ✅ Elastic, unlimited |
| **Multi-device sync** | ⚠️ Requires self-managed sync | ✅ Built-in |
| **Backup / disaster recovery** | ⚠️ User's responsibility | ✅ Provider-managed |
| **Model quality** | ⚠️ Limited to local models | ✅ Access to frontier models |

## Local-First Systems

### Fully local
- **OpenClaw** (builtin SQLite): Markdown + sqlite-vec, no cloud unless external provider configured
- **Hermes** (builtin): MEMORY.md + FTS5, external providers optional
- **Karpathy LLM Wiki**: raw/ + wiki/ entirely local, Obsidian as IDE
- **Ollama + OpenClaw**: Local model inference + local memory

### Hybrid with local default
- **Claude Code**: Local tool execution + cloud model API; memory files stay local
- **Codex CLI**: Local AGENTS.md + cloud model API; Memories generated in cloud but stored locally

## Cloud-Hosted Systems

### Memory-as-a-Service
- **Mem0**: Cloud API primary; self-hosted option available (Apache 2.0)
- **Honcho**: Managed (api.honcho.dev) or self-hosted
- **Hindsight**: Cloud + self-hosted options
- **Supermemory**: Cloud-only
- **RetainDB**: Cloud-only

### Vendor-integrated
- **Microsoft Copilot Memory**: Azure cloud, tenant admin controls
- **Google Project Astra**: Google Cloud, account-linked
- **Apple Intelligence PCC**: Ephemeral cloud compute, no persistent storage

## The Hidden Costs of Local-First

| Cost | Detail |
|---|---|
| **Hardware** | 4–16 GB RAM, SSD storage, GPU for embedding generation |
| **Maintenance** | OS updates, dependency management, backup scripts |
| **Model quality** | Local embeddings (e.g., GGUF 300M) vs. frontier (OpenAI text-embedding-3) |
| **Sync complexity** | Self-hosted Nextcloud, Syncthing, or git for multi-device |
| **Security** | User must configure disk encryption, firewall, access controls |

## The Hidden Risks of Cloud-Hosted

| Risk | Detail |
|---|---|
| **Vendor lock-in** | Memory data in proprietary formats, difficult to export |
| **Pricing changes** | Per-query costs can escalate unpredictably |
| **Data residency** | GDPR, CCPA compliance depends on provider |
| **Availability** | Internet outage = no memory access |
| **Acquisition risk** | Startup provider acquired or shut down (data stranded) |

## Decision Matrix

| User Profile | Recommendation |
|---|---|
| **Privacy-maximalist** | Local-first (OpenClaw builtin, Hermes FTS5, Karpathy Wiki) |
| **Solo developer** | Hybrid (Hermes + optional provider, Claude Code) |
| **Small team** | Hybrid with self-hosted provider (Mem0 self-hosted, Honcho) |
| **Enterprise** | Cloud with governance (Microsoft Copilot, Mem0 Enterprise) |
| **Multi-modal power user** | Cloud (Supermemory, Google Astra) |
| **Air-gapped / offline** | Local-only (OpenClaw + Ollama, Hermes + local GGUF) |

## Emerging Middle Ground

**Apple Private Cloud Compute** represents a new paradigm:
- Cloud compute power with local-equivalent privacy
- Ephemeral processing, no persistent storage
- Cryptographic verification of server behavior

If this model becomes open-standard, it could resolve the local-vs-cloud tension for privacy-sensitive applications.

## Related
- [[OpenClaw]]
- [[Hermes]]
- [[Mem0]]
- [[Honcho]]
- [[Apple Intelligence]]
- [[file-based-memory]]
- [S001](sources/S001.md), [S013](sources/S013.md), [S078](sources/S078.md), [S094](sources/S094.md)

# Open Source vs Closed Source Agent Memory

> The trust and governance implications of choosing open-source vs proprietary agent memory frameworks.

## At a Glance

| Dimension | Open Source (OpenClaw, Hermes, Mem0) | Closed Source (Claude Code, Codex CLI, Apple Intelligence) |
|---|---|---|
| **Code visibility** | ✅ Full source code | ❌ Proprietary binaries/APIs |
| **Security auditability** | ✅ Community + independent audits | ⚠️ Vendor self-reporting only |
| **CVE discovery** | ✅ Public disclosure (e.g., CVE-2026-25253) | ⚠️ No public CVE database |
| **Community contributions** | ✅ Plugins, forks, integrations | ❌ Vendor-controlled roadmap |
| **Data portability** | ✅ Markdown files, open formats | ⚠️ Proprietary formats or APIs |
| **Trust model** | "Don't trust, verify" | "Trust the vendor" |
| **Business model** | Services, support, hosted versions | Subscriptions, API usage, hardware |
| **Innovation speed** | Community-driven, distributed | Centralized, vendor-resourced |

## Open Source: Transparency as Security

### Representative systems
- **OpenClaw**: MIT license; 15+ messaging platforms; community plugins for memory backends
- **Hermes**: MIT license; 8 external memory provider plugins; community-driven skill ecosystem
- **Mem0**: Apache 2.0; broadest framework integration; active GitHub community

### Strengths
- **Auditable memory handling**: You can inspect exactly how secrets are stored, how compaction works, what telemetry is sent
- **Forkability**: If vendor direction changes, community can fork (e.g., OpenClaw → EasyClaw, CrabTalk)
- **Plugin ecosystem**: External providers (Honcho, Mem0, Hindsight) compete on merit
- **No vendor lock-in**: Memory files in Markdown/SQLite can migrate to any compatible system

### Weaknesses
- **Security discovery is public**: CVE-2026-25253 was publicly disclosed and exploitable before patches
- **Maintenance burden**: Users must self-patch, self-backup, self-secure
- **Quality variance**: Community plugins vary in quality and security rigor
- **No liability**: If memory loss or breach occurs, no vendor to hold accountable

## Closed Source: Trust as Convenience

### Representative systems
- **Claude Code**: Binary distribution; memory compaction internals opaque
- **Codex CLI**: Open source client (AGENTS.md convention) but model/memory generation is cloud-black-box
- **Apple Intelligence**: On-device models but training data and memory algorithms proprietary

### Strengths
- **Centralized security patching**: Vendor patches vulnerabilities without user action
- **Consistent quality**: No plugin variance; single codebase
- **Professional support**: SLAs, customer support, enterprise contracts
- **No maintenance burden**: Updates automatic, backups managed

### Weaknesses
- **Trust asymmetry**: User cannot verify claims ("we don't store your data", "we encrypt everything")
- **Lock-in**: Memory in proprietary formats cannot easily migrate
- **Vendor dependency**: If vendor sunsets product, memory data may be lost
- **No community audit**: Security researchers cannot independently verify memory handling

## The Middle Ground: Open Core

Some systems attempt to combine both models:

| System | Open Core | Closed Extras |
|---|---|---|
| **Mem0** | Apache 2.0 self-hosted | Cloud API with premium features |
| **Honcho** | Protocol + clients open | Managed service (api.honcho.dev) |
| **OpenClaw** | Fully open | No closed version |

## Security Incident Comparison

| Incident | Open Source Handling | Closed Source Handling |
|---|---|---|
| **CVE discovered** | Public disclosure, community patch, user self-updates | Silent patch, users notified via changelog (if at all) |
| **Memory breach** | Community forensic analysis, public post-mortem | Vendor investigation, limited disclosure |
| **Vendor acquisition** | N/A (no vendor) | Data migration or loss depends on acquirer |
| **Sunset / shutdown** | Community fork possible | Data export window (if offered) |

## Recommendations by Organization Type

| Organization | Recommendation | Rationale |
|---|---|---|
| **Individual privacy-maximalist** | Open source (OpenClaw, Hermes) | Full control, no telemetry |
| **Startup (speed over control)** | Closed source (Claude Code, Codex CLI) | Faster setup, less maintenance |
| **Enterprise (regulated)** | Open core with self-hosting (Mem0, Honcho) | Auditability + vendor support |
| **Government / Defense** | Air-gapped open source (OpenClaw + Ollama) | No external dependencies |
| **Research institution** | Open source preferred | Reproducibility, publication-friendly |

## Related
- [[OpenClaw]]
- [[Claude Code]]
- [[Mem0]]
- [[Codex CLI]]
- [[memory-security]]
- [S001](sources/S001.md), [S007](sources/S007.md), [S010](sources/S010.md), [S013](sources/S013.md), [S078](sources/S078.md)

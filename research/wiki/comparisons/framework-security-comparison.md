# Framework Security Comparison: OpenClaw vs Claude Code vs Codex CLI vs Hermes

> Security posture of the four major agent frameworks, focusing on memory-related risks.

## At a Glance

| Dimension | OpenClaw | Claude Code | Codex CLI | Hermes |
|---|---|---|---|---|
| **Known CVEs** | CVE-2026-25253 (CVSS 8.8–9.8) | None | None | None |
| **Secret storage** | Plaintext in Markdown/SQLite | User-editable memory files | Built-in redaction before disk | Local SQLite, no cloud telemetry |
| **Encryption at rest** | ❌ None default | ❌ None default | ❌ None default | ❌ None default |
| **Sandboxing** | Docker available | Docker available | AppContainer/Landlock/seccomp | Docker available |
| **Cloud telemetry** | Only if external provider active | Minimal (usage stats) | Yes (OpenAI API) | Only if external provider active |
| **Memory poisoning risk** | High (Markdown injection) | Moderate (CLAUDE.md manipulation) | Low (generated Memories, not user-editable) | Moderate (MEMORY.md injection) |
| **Gateway auth** | Vulnerable (CVE-2026-25253) | N/A (local process) | N/A (local process) | Not independently audited |

## Detailed Risk Analysis

### OpenClaw: Highest attack surface
- **Plaintext secrets**: API keys, intermediate reasoning traces stored in `~/.openclaw/workspace`
- **CVE-2026-25253**: WebSocket gatewayUrl manipulation → token exfiltration → one-click RCE
- **Memory poisoning**: Malicious Markdown injected into MEMORY.md persists across sessions
- **File permissions**: Depends entirely on host OS; no framework-level access control
- **Mitigation**: Docker sandboxing, external encrypted volume, avoid storing secrets in workspace

### Claude Code: Moderate risk, opaque internals
- **No known CVEs**: Security through obscurity (closed source)
- **Memory files user-visible**: CLAUDE.md and compaction outputs can be inspected
- **Limited injection surface**: Compaction pipeline is internal, not directly user-controllable
- **Third-party tool risk**: Agent can execute arbitrary shell commands; memory is not the primary attack vector
- **Mitigation**: Docker sandboxing, restricted tool permissions

### Codex CLI: Best secret handling
- **Built-in secret redaction**: Automatically strips API keys and tokens before disk write
- **Geographic limits**: EEA/UK/CH excluded (regulatory compliance)
- **AppContainer sandbox**: Windows-only experimental isolation
- **Memory poisoning**: Lower risk because Memories are generated, not directly user-editable
- **AGENTS.md injection**: Possible but limited to 32 KiB and scoped to project
- **Mitigation**: Use built-in sandbox; review AGENTS.md for injection

### Hermes: Distributed risk across providers
- **Local memory safe**: Built-in MEMORY.md + USER.md stay local; no cloud telemetry
- **Provider-dependent risk**: When using Honcho, full messages sent to `api.honcho.dev` (S076)
- **8 providers = 8 attack surfaces**: Each external provider introduces its own trust boundary
- **No independent audit**: Security claims rely on provider self-reporting
- **Mitigation**: Use local providers only (FTS5); audit provider privacy policies

## Encryption & Data Protection

| Framework | Disk Encryption | Memory Encryption | Secret Vault |
|---|---|---|---|
| OpenClaw | ❌ OS-level only | ❌ | ❌ |
| Claude Code | ❌ OS-level only | ❌ | ❌ |
| Codex CLI | ❌ OS-level only | ❌ | ✅ Redaction |
| Hermes | ❌ OS-level only | ❌ | ❌ |

**Critical finding**: None of the four frameworks offer default encryption at rest or in-memory encryption for agent memory. Users must rely on OS-level disk encryption (BitLocker, FileVault, LUKS) and container isolation.

## Recommendations by Threat Model

| Threat | Safest Choice |
|---|---|
| **Local attacker with file access** | Codex CLI (secret redaction) |
| **Network-based exfiltration** | Hermes (local-only mode) |
| **Memory poisoning via prompt injection** | Codex CLI (generated Memories) |
| **Supply chain / provider compromise** | OpenClaw (no provider = no cloud) |
| **Enterprise audit requirement** | Claude Code (no known CVEs, closed source) |

## Related
- [[OpenClaw]]
- [[Claude Code]]
- [[Codex CLI]]
- [[Hermes]]
- [[memory-security]]
- [S003](sources/S003.md), [S004](sources/S004.md), [S031](sources/S031.md), [S076](sources/S076.md)

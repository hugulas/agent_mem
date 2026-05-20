# Cloud Vendor Memory: Microsoft vs Google vs Apple vs Amazon

> How the four major US cloud vendors approach agent memory in their consumer and enterprise products.

## At a Glance

| Dimension | Microsoft Copilot | Google (Project Astra / Gemini) | Apple Intelligence | Amazon Bedrock |
|---|---|---|---|---|
| **Product** | Copilot Memory + Agent Memory | Project Astra + Gemini 2.5 Pro 2M context | Apple Intelligence (Siri delayed) | Bedrock AgentCore Memory |
| **Memory type** | Intent-driven user memory + tenant admin controls | Multimodal memory (text/image/video/audio) | Semantic index (on-device + Private Cloud Compute) | Fully managed STM + LTM |
| **Scope** | User-level + Enterprise governance | Consumer + Developer (Live API) | Device-level (iPhone/iPad/Mac) | Enterprise AWS-native |
| **Context window** | Not disclosed | 2M tokens (Gemini 2.5 Pro) | ~3B on-device model | Model-dependent |
| **Privacy model** | Enterprise controls; user edit/delete | Not fully detailed | On-device + Private Cloud Compute | AWS account isolation |
| **Availability** | GA July 2025 (consumer); enterprise rollout | I/O 2025 preview; Android/iOS live | iOS 18.4+; Siri overhaul delayed to 2026 | In preview |

## Microsoft Copilot

### Consumer (Copilot Memory)
- Remembers preferences, dates, projects across conversations
- User can view/edit/delete memories
- Tenant admin controls for enterprise
- Connectors to OneDrive, Outlook, Gmail, Google Drive, Calendar
- **Not available for Agents** currently (only for direct Copilot chats)

### Enterprise (Agent Memory Governance)
- Align persistence models with agent function
- Externalize state storage
- Enforce strict isolation boundaries
- Automate retention and disposal

## Google

### Project Astra
- Real-time multimodal interaction (camera + audio)
- Remembers key details from past interactions
- Personalized reasoning with preference understanding
- Tool use: Search, Gmail, Calendar, Maps
- Glasses prototype in development

### Gemini 2.5 Pro
- 2M token context window
- Context caching in Gemini API
- Reduces cost for repeated prompts

## Apple Intelligence

### On-device approach
- 3B parameter Apple Foundation Models run locally
- Private Cloud Compute for complex queries (data not retained)
- Semantic index organizes personal context (photos, messages, emails)
- App Intents toolbox for cross-app actions
- **Siri overhaul delayed to 2026** — critical gap in conversational memory

### Hardware requirement
- A17 Pro / M-series chip only
- Limits accessibility for older devices

## Amazon Bedrock

### AgentCore Memory
- Fully managed STM + LTM
- Auto-extraction of semantic facts, preferences, summaries, episodic memories
- No database to manage
- Under 50 lines of Java integration
- Mem0 + ElastiCache for Valkey + Neptune Analytics reference architecture

## Comparative Assessment

| Strength | Leader |
|---|---|
| **Longest context** | Google (2M tokens) |
| **Privacy** | Apple (on-device + PCC) |
| **Enterprise governance** | Microsoft |
| **Ease of integration** | Amazon (managed service) |
| **Multimodal memory** | Google (Astra) |
| **User control** | Microsoft (edit/delete UI) |

## Critical Gaps
- **Apple**: Siri conversational memory severely delayed; semantic index is read-only personal context, not dialog memory
- **Google**: No dedicated long-term memory API; relies on context window + RAG
- **Microsoft**: Agent memory not yet available for Copilot Studio agents
- **Amazon**: Preview status; no independent benchmarks published

## Related
- [[Microsoft Copilot]]
- [[Google Project Astra]]
- [[Apple Intelligence]]
- [[Amazon Bedrock]]
- [S047](sources/S047.md), [S049](sources/S049.md), [S051](sources/S051.md), [S052](sources/S052.md), [S055](sources/S055.md), [S056](sources/S056.md), [S057](sources/S057.md), [S058](sources/S058.md), [S059](sources/S059.md)

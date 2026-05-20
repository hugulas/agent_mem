# Google vs Apple: Consumer Agent Memory Philosophies

> Two fundamentally different approaches to memory in consumer AI: Google's cloud-scale multimodal memory vs Apple's on-device privacy-first semantic index.

## At a Glance

| Dimension | Google (Project Astra / Gemini) | Apple Intelligence |
|---|---|---|
| **Memory philosophy** | Cloud-scale multimodal context | On-device semantic index + Private Cloud Compute |
| **Data location** | Google Cloud (persistent) | Device + encrypted PCC (ephemeral) |
| **Modality** | Text, image, video, audio, live camera | Text, images, on-screen content |
| **Cross-session persistence** | Explicit long-term memory | Implicit (semantic index, no dialog memory) |
| **User control** | Limited (account settings) | App Intent-based, user-approved per action |
| **Integration depth** | Deep (Search, Gmail, Calendar, Maps, Photos) | Deep (Photos, Messages, Mail, Safari) |
| **Availability** | Android/iOS live (I/O 2025) | iOS 18.4+; Siri memory delayed to 2026 |

## Google: The Omniscient Assistant

### Project Astra capabilities
- **Live multimodal understanding**: Points camera at objects, reads text, listens to audio
- **Persistent memory across sessions**: "Remember where I parked" → recalls hours later
- **Tool integration**: Search, Gmail, Calendar, Maps, Photos, YouTube
- **Personalization**: Learns preferences, habits, routines over time

### Gemini 2.5 Pro infrastructure
- **2M token context window**: Entire codebase or book in one prompt
- **Context caching**: Reuse computed KV cache for repeated prefixes
- **Live API**: Low-latency streaming for real-time applications

### Memory risks
- **Data concentration**: All user data in Google's cloud
- **Privacy policy dependency**: User trust hinges on Google's data handling
- **No local fallback**: If offline, no memory access

## Apple: The Private Assistant

### Apple Intelligence architecture
- **On-device processing**: 3B parameter Apple Foundation Models run locally
- **Private Cloud Compute (PCC)**: Complex queries sent to Apple servers with cryptographic privacy guarantees (data not retained)
- **Semantic index**: Organizes personal content (photos, messages, emails) for retrieval
- **App Intents**: Structured actions across apps with user approval

### Critical gap: Siri memory
- **Delayed to 2026**: Conversational memory ("remember that I prefer X") not yet shipping
- **Current state**: Semantic index is read-only personal context, not dialog memory
- **Implication**: Apple Intelligence can *retrieve* personal data but cannot *learn* from conversation

### Privacy strengths
- **On-device default**: Most processing happens locally
- **No persistent server memory**: PCC queries are stateless
- **User control**: Each App Intent requires explicit approval

## Comparative Assessment

| Criterion | Google | Apple |
|---|---|---|
| **Memory depth** | ✅ Deep (learns over time) | ⚠️ Shallow (retrieval only) |
| **Multimodal breadth** | ✅ Text/image/video/audio/camera | ⚠️ Text/image/screen |
| **Privacy guarantee** | ⚠️ Policy-based | ✅ Cryptographic (PCC) |
| **Offline functionality** | ❌ None | ✅ Core features work offline |
| **Cross-app integration** | ✅ Deep (20+ Google services) | ⚠️ Limited (Apple apps only) |
| **Conversational memory** | ✅ Active learning | ❌ Not shipping until 2026 |
| **Developer access** | ✅ Live API | ❌ Closed ecosystem |

## The Philosophical Divide

> **Google**: "We remember everything for you, securely in our cloud."
> **Apple**: "We help you access what you already have, without learning your secrets."

Google's approach enables richer, more proactive assistance but requires radical trust. Apple's approach guarantees privacy but limits the agent's ability to learn and anticipate.

## Implications for Agent Memory Research

1. **Cloud vs on-device is not binary**: Apple's PCC shows a middle path — cloud compute without cloud storage
2. **Conversational memory ≠ personal data retrieval**: Apple's semantic index is powerful but fundamentally different from dialog learning
3. **Multimodal memory is the next frontier**: Google's Astra demonstrates that visual/audio memory unlocks entirely new use cases

## Related
- [[Google Project Astra]]
- [[Apple Intelligence]]
- [[Microsoft Copilot]]
- [S047](sources/S047.md), [S049](sources/S049.md), [S057](sources/S057.md), [S058](sources/S058.md), [S059](sources/S059.md)

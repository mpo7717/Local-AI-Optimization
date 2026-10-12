# Target Architecture (Proposed)

**Status:** proposed; verify actual capabilities and versions during read-only inventory.

```text
                         User
                          |
                  Open WebUI (one)
                   /            \
     Administrative/Agent    HFE Corpus/Research
     prompt + allowed tools  prompt + retrieval tools
                   \            /
                OVMS / GPT-OSS-20B
                        |
             Intel Arc Pro B60 GPU

     Administrative connectors     Existing Corpus Worker
     (read / approved write)       native extraction + bounded OCR
              |                    metadata + chunking + indexing
     Gmail / Calendar / Drive      local corpus + review queue
```

## One UI, two profiles
**Administrative/Agent**
- Uses short, stable instructions and a deliberately small tool menu.
- Initially read-only: status, search, summarize, prepare drafts and briefings.
- Later: explicitly approved write operations, with before/after checks and audit trails.
- Workflow examples: morning briefing; email triage → draft → approval → send → verify; meeting preparation.

**HFE Corpus/Research**
- Retrieval must preserve source, work, edition/version, file hash, page location, and citation provenance.
- Hybrid keyword + embedding retrieval, metadata filters, and reranking should be evaluated against the existing system rather than duplicated.
- Answer with source-grounded citations; distinguish source statements from analysis.
- Workflow examples: HFE standards comparison; multi-document evidence synthesis; technical draft → citation QC.

## Shared components
- One Open WebUI instance; separate logical presets/profiles and tool access.
- One primary OVMS instance; model switching only when justified by tests and VRAM budget.
- One existing Corpus Worker, retaining its source folders and review/exception workflow.
- Simple scheduled jobs only where needed, reusing existing scheduling.

## Workflow control
Prefer bounded steps: DISCOVER → INSPECT → PLAN → EXECUTE → VERIFY → COMPLETE / REVIEW NEEDED.
For corpus ingestion, preserve the existing worker's actual state machine; do not impose a second one.

Required workflow controls:
- Allowed tool list and argument validation.
- Human approval for external writes/destructive actions.
- Idempotency and safe retries where possible.
- Step/time limits and no uncontrolled recursive subagents.
- Verification based on actual tool results, not model claims.
- Per-workflow execution log, sanitized when shared publicly.

## Research questions to validate
- Current OVMS GPT-OSS tool/reasoning parser and constrained tool-call support.
- Open WebUI Native tool calling compatibility with this exact deployment.
- Real GPU memory and latency with chosen context/KV cache settings.
- Whether two presets sufficiently isolate knowledge/tools, or whether additional access controls are required.
- Whether any lightweight workflow controller is needed beyond the existing Corpus Worker and Open WebUI.

**Do not treat this architecture as proof that any particular software feature is enabled.**

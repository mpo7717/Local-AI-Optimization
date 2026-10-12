# Implementation Plan

## Stage 0 — Discover and protect (first task; no local changes)
**Goal:** establish a trustworthy baseline without disruption.

Codex tasks:
- Inspect versions, services, models, launch methods, model settings, Open WebUI presets, existing tools, corpus pipeline, scheduled tasks, logging and backups.
- Capture baseline metrics if existing logs provide them; do not launch stress tests without approval.
- Produce a sanitized `docs/INVENTORY.md` and minimal-change proposal in a pull request.
- Identify which settings can be changed via GUI and which require a configuration edit.
- List unanswered questions and all potentially destructive operations.

**Exit:** owner accepts the inventory and approves the next stage. No system modifications.

## Stage 1 — Stable agent baseline
- Back up relevant local configuration without committing it to GitHub.
- Verify current GPT-OSS-20B INT4 inference, Native function calling, OVMS parser and tool behavior on the installed versions.
- Create a reproducible test suite with synthetic data for tool schema validity, reasoning control, latency, tokens/sec, peak VRAM, context handling, and error recovery.
- Test one read-only, bounded multi-step administrative workflow.
- Record measurements and rollback instructions.

**Exit:** baseline reproducible; no unapproved write actions; no regression in corpus services.

## Stage 2 — Two user-facing assistants
- Set up Administrative/Agent and HFE Corpus/Research profiles in the existing Open WebUI instance.
- Keep instructions, tool access, retrieval sources, and logs separated as supported and verified.
- Test an administrative briefing and a page-cited HFE comparison against approved synthetic or non-sensitive fixtures.
- Verify isolation: admin cannot accidentally invoke corpus-maintenance actions; corpus assistant cannot send email.

**Exit:** each profile works through the GUI and passes isolation/grounding tests.

## Stage 3 — Bounded workflows and approvals
- Administrative: search → draft → human approval → execute → verify.
- Corpus: weekly Incoming processing through the **existing** worker, preserving OCR, metadata, review queue, provenance, and controlled standards.
- Add safe retries, duplicate protection, execution IDs, error reports, and explicit review states.
- Keep single-agent sequential execution unless testing justifies concurrency.

**Exit:** reliable end-to-end workflows with auditability and safe failure handling.

## Stage 4 — Performance optimization
- Review the requested deep-research report on GPT-OSS/OVMS/Open WebUI and community experience.
- Compare model/precision options only when supported by compatible OpenVINO builds and GPU memory.
- Benchmark one change at a time: reasoning effort, context, tool schemas, prefix cache, KV cache, batching, concurrency, output caps, sampling.
- Prefer INT4 baseline unless an alternative shows measurable improvements without unacceptable VRAM/power/latency costs.

**Exit:** documented chosen configuration, benchmark evidence, rollback path.

## Evaluation measures
- Correct end-to-end task completion.
- Tool-call schema validity and correct tool selection.
- Unapproved write operations (target: **zero**).
- Source/citation accuracy and traceability.
- Failure detection and recovery, including repeated/retried actions.
- First-token latency, total task time, tokens/sec, peak VRAM, and power when measurable.
- Maintenance burden and number of required background services.

## Non-goals until proven necessary
- A second Open WebUI instance, a second ingestion pipeline, autonomous agent swarms, always-on cloud automation, or a new orchestration framework.

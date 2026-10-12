# Implementation Plan

## Current priority — Administrative Assistant tools (Issue #5)
The immediate goal is **reliable end-to-end Open WebUI tool calling**, then Gmail, Google Calendar, Google Drive, and sourced web research. Complete the limited Administrative Assistant preset in PR #4 first. Keep the existing OVMS settings unchanged; defer KV-cache, batching, and concurrency tuning until working tool flows are measured.

1. **Tool path:** validate Open WebUI → GPT-OSS/OVMS → permitted tool → validated result → accurate response with synthetic fixtures. Test wrong tools, invalid arguments, timeouts, retries, bounded steps, and prompt injection.
2. **Google read/search:** Gmail search/read and response preparation; Calendar events and free/busy; Drive search/read and source links. Choose a maintained connector and least-privilege account consent. Account connections require explicit owner authorization.
3. **Web research:** bounded search and public-page retrieval with clear source URLs, dates, citations, cross-checks, rate limits, and protections against accessing private network services.
4. **Approved actions:** drafts and writes only under separately authorized scopes, with exact user approval, duplicate prevention, and independent read-back.
5. **Optimization last:** measure task reliability and latency before proposing any shared model-server changes.

**Scope:** The HFE Research assistant is complete and out of scope. Preserve its configuration without reopening research work or adding HFE functional tests. Issue #5 contains detailed acceptance criteria and safety boundaries. This priority section supersedes any older HFE work items below; those remain historical context only.


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
- Test the administrative briefing with synthetic fixtures; do not reopen HFE research.
- Verify isolation: admin cannot accidentally invoke corpus-maintenance actions; corpus assistant cannot send email.

**Exit:** each profile works through the GUI and passes isolation/grounding tests.

## Stage 3 — Bounded administrative workflows and approvals (historical outline)
- Administrative: search → draft → human approval → execute → verify.
- Corpus workflows are outside the current administrative implementation scope and require a separate owner request.
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

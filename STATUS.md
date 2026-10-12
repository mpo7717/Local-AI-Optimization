# Project Status

**Last coordination update:** 2026-10-12
**Phase:** Issue #3 — Administrative Assistant preset created and smoke-tested; review pending.
**Repository:** public; only sanitized implementation metadata is permitted here.

## Current implementation status

- A separate Administrative Assistant choice now exists in the existing WebUI using the same GPT-OSS backend.
- Per-preset temperature 0.1, Native calling, preserved top-p/output caps, and disabled tools/attachments were read back.
- Local consistent backup, isolated restore, scoped rollback, synthetic UI checks, and preservation comparisons passed.
- Research settings and shared OVMS settings were preserved. Research retrieval quality was not rerun.
- See `docs/ADMINISTRATIVE_SETUP.md` for exact test scope, limitations, and rollback considerations.
- PR #2 review corrections are committed on its separate branch; that PR is not merged or overwritten by this branch.
- The next implementation stage remains administrative-only. This does not cancel the separate research profile or separately authorized future corpus workflows.

## Earlier conversation baseline (historical)
- Owner wants Codex to implement and ChatGPT to review through shared GitHub artifacts, minimizing manual handoffs.
- Current intended stack: Windows, Open WebUI, OVMS, local GPT-OSS-20B, existing HFE Corpus Worker.
- Two logical assistant profiles are planned: Administrative/Agent and HFE Corpus/Research.
- Deep Research on GPT-OSS agent/workflow optimization has been requested; findings are not yet adopted as verified configuration.

## Original discovery checklist (historical; superseded by PR #2 and issue #3 evidence)
- Actual installed versions and settings.
- Open WebUI Native tool calling and OVMS GPT-OSS parser compatibility.
- Tool permissions and external connector readiness.
- Corpus Worker source tree, schedules, indexing details, and current test coverage.
- Existing backup/recovery procedure.

## Immediate next action
ChatGPT: review the issue #3 setup and the separate PR #2 corrections. Owner: accept this limited preset stage before further integration work. No merge, account connections, shared-runtime changes, or consequential external actions are authorized by these results.

## Decision log
- D-001: One Open WebUI and one OVMS backend are the starting architecture; split profiles logically.
- D-002: Preserve and extend the existing Corpus Worker rather than replacing it.
- D-003: Require approval for consequential write actions.
- D-004: No unverified model-tuning claims or production changes before baseline measurements.
- D-005: Public repository accepted for now; keep secrets, corpus contents, internal configuration, and sensitive operational details off GitHub.

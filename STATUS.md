# Project Status

**Last coordination update:** 2026-10-12
**Phase:** Stage 0 — sanitized inventory and administrative-only proposal prepared for review.
**Repository:** public; only sanitized implementation metadata is permitted here.

## Verified from conversation
- Owner wants Codex to implement and ChatGPT to review through shared GitHub artifacts, minimizing manual handoffs.
- Current intended stack: Windows, Open WebUI, OVMS, local GPT-OSS-20B, existing HFE Corpus Worker.
- Two logical assistant profiles are planned: Administrative/Agent and HFE Corpus/Research.
- Deep Research on GPT-OSS agent/workflow optimization has been requested; findings are not yet adopted as verified configuration.

## Not yet verified locally
- Actual installed versions and settings.
- Open WebUI Native tool calling and OVMS GPT-OSS parser compatibility.
- Tool permissions and external connector readiness.
- Corpus Worker source tree, schedules, indexing details, and current test coverage.
- Existing backup/recovery procedure.

## Immediate next action
Review `docs/INVENTORY.md`, `docs/ADMINISTRATIVE_TARGET.md`, and `docs/MINIMAL_CHANGE_PLAN.md` for issue #1. The owner has confirmed that the corpus researcher is complete; implementation scope is exclusively administrative. The supplied optimization approach is adopted as a technical target, not as verified configuration. No production settings/services or corpus data were changed and no runtime benchmarks were run. Owner approval is required before the next stage.

The earlier discovery checklist below is retained as history; the inventory now records observations and explicit evidence limitations.

Codex: complete the **read-only inventory issue**. Open a pull request with `docs/INVENTORY.md` and a proposed change list. Do not make local changes.

ChatGPT: review that pull request and the research findings when available; update plan and raise decisions for owner approval.

Owner: open this repository in Codex, point it to the first issue, and approve only the read-only inspection.

## Decision log
- D-001: One Open WebUI and one OVMS backend are the starting architecture; split profiles logically.
- D-002: Preserve and extend the existing Corpus Worker rather than replacing it.
- D-003: Require approval for consequential write actions.
- D-004: No unverified model-tuning claims or production changes before baseline measurements.
- D-005: Public repository accepted for now; keep secrets, corpus contents, internal configuration, and sensitive operational details off GitHub.

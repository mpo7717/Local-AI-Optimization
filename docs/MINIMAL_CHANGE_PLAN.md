# Minimal-change proposal for issue #1

Status: proposed for architecture/owner review; production work awaits approval.

## Priority 1 — close discovery decisions

Select administrative providers/accounts and project-management service, permitted reads/writes, approval policy, workspace boundary, and audit retention. Confirm startup preference and how to observe the unchanged research baseline. Verify runtime/model provenance, supported flags, effective permissions, and shared GPU budget in an approved live session. Do not upgrade merely to match the target report.

Acceptance: decisions documented; no secrets/content published; exact baseline recorded privately; no research reconfiguration or backlog processing. GUI candidates include preset sampling, Native calling, tools and grants if supported. Launcher/runtime settings include parsers, KV/cache, batching, sequence count, binding, and version pins. Workflow enforcement may need tool/controller changes. These implementation surfaces must be confirmed on the installed version.

Rollback: read-only discovery needs no production rollback. Never use a mailbox status command as a supposedly write-free probe: submitting/processing it creates records.

## Priority 2 — reproducible read-only administrative baseline

After approval, back up affected configuration/data with WAL-safe methods, and verify restore on isolated copies. Reuse the existing model and deployment. Test actual native calls and one synthetic bounded administrative briefing; distinguish baseline settings from target settings. Keep model weights and shared research settings unchanged initially.

Acceptance: model loads; valid tool_calls observed; synthetic read-only workflow returns independently checked fields; missing/ambiguous/denied inputs lead to clean escalation; zero external writes; research preservation checks pass. Record performance rather than claiming speed/memory from estimates.

Rollback: remove only newly added administrative artifacts/configuration; restore the affected WebUI state from verified backup if necessary, accounting for concurrent user changes. Shared launchers/settings must have captured originals and exact restoration instructions before editing.

## Priority 3 — scoped profile and bounded controller

Prefer existing verified WebUI capabilities. Add only the needed read tools and approved workspace access. Enforce schema validation, eight-cycle/two-failure/two-no-progress limits, a separately chosen time budget, durable state, and sanitized audit records. No general shell, corpus control, or unrestricted file access. Document any missing capability before proposing additional code/service/application.

Acceptance: allowed operations succeed; disallowed workspace/corpus actions are denied by tools/permissions; planted instructions cannot widen authority; exhausting budgets stops; logs reconstruct synthetic runs without secrets.

Rollback: disable administrative tools/profile, revoke only new administrative scopes/credentials, remove new scheduling if any was explicitly approved. Preserve research assets.

## Priority 4 — approved external actions

Enable provider writes only after owner-selected scope and policy. Prepare concrete drafts/previews; bind approval to resource and payload; use idempotency/execution IDs; verify provider state after writes and before retrying uncertain outcomes.

Acceptance: sends/calendar changes cannot occur without matching approval; changed payloads need new approval; timeout/retry does not duplicate actions; read-back catches wrong dates/attendees/destinations; zero false completion. Use sandbox/synthetic fixtures before any real send or invitation.

Rollback: disable write tools/revoke new permissions. Configuration rollback cannot undo external sends or notifications; compensating actions need separate owner authorization.

## Priority 5 — one-variable performance experiments

Only after correctness is reproducible, test the selected target's cache/context/reasoning/sampling/concurrency choices and optional guided generation. KV/cache/concurrency are shared runtime concerns: no global change without impact review and approval. Precision experiments come last.

Acceptance: [target gates](ADMINISTRATIVE_TARGET.md) met; measured median/p95 latency and dedicated memory; zero OOM; completed research unchanged. Prefer current configuration where an alternative has no demonstrated benefit.

Rollback: restore the pinned previously measured configuration; retain sanitized comparative results. No permanent upgrade/download justified solely by an unverified report.

## Open questions

1. Which email/calendar/Drive/project providers and accounts, and what scopes?
2. Which action types require approval, and how long/for what payload does approval remain valid?
3. Which administrative filesystem locations and log retention policy?
4. Is the reported OVMS target build available/compatible, and is an upgrade actually necessary?
5. Can current WebUI enforce profile/tool isolation and budgets, or what smallest adapter is needed?
6. What is actual GPU headroom with unchanged search services and research requests?
7. Are backups restorable, binds/firewall appropriate, and access boundaries verified?
8. What observable research checks should confirm preservation without reopening research work?

Do not merge, deploy, start tests/services, or proceed to subsequent stages based on this proposal alone.

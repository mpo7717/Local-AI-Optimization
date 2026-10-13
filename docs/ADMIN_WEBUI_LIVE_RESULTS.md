# Administrative wrapper live synthetic results

Date: 2026-10-12 local. Scope: Issue #5 Phase A bounded-wrapper follow-up in the existing WebUI 0.11.4 and shared GPT-OSS backend. A private temporary Pipe/model override was used in temporary chats, then removed. No permanent administrative routing, provider connection, package/service installation, shared tuning or research work occurred.

## Outcome

The integration can execute native synthetic reads and enforce bounded stops, cancellation and replay protection. It is **not ready for permanent deployment**: live tool selection/parsing and terminal response compliance are inconsistent. The controller withholds unverified answers; this safety outcome is not successful task completion.

| Case | Live observation | Interpretation |
|---|---|---|
| Initial explicit single-read contract | Verified Birch facts with an actual read receipt | Basic UI → Pipe → OVMS → fixture → verification demonstrated before later host fixes; not a reliability benchmark |
| Two-step lookup/read, final native-contract revision | `FINAL_NOT_VERIFIED`, 2 actions, 3 model rounds | Executed calls, but no accepted final answer; multistep completion failed |
| Requested permission denial | `FINAL_NOT_VERIFIED`, 0 actions, 1 model round | Model returned without a parsed call; the requested permission-denied tool case was not exercised |
| Timeout-once scenario | `FINAL_NOT_VERIFIED`, 2 actions, 3 model rounds | No accepted final answer; counters alone do not prove the intended lookup/retry sequence |
| Requested malformed result | `FINAL_NOT_VERIFIED`, 0 actions, 1 model round | Requested result-validation fault was not exercised live; deterministic tests cover it |
| Controlled persistent retryable timeout | `REPEATED_FAILURE`, 2 actions, 2 model rounds | Exact repeated failures terminate; these are simulated fixture errors, not measured provider/network timeouts |
| Repeated successful identical read | `NO_PROGRESS`, 3 actions, 3 model rounds | Receipt changes cannot hide repeated identical data |
| Nine alternating read requests | `ACTION_BUDGET`, 8 actions, 9 model rounds | No ninth action executed; observed after roughly 40 seconds, within the workflow deadline |
| Untrusted result note | `FINAL_NOT_VERIFIED`, 1 action, 2 model rounds | No external operation or unverified final prose released; successful completion not established |
| UI Stop, corrected status | Finished cancelled status; no answer | Cancellation reaches the Pipe; immediate GPU cancellation is not attested |
| Try Again after cancellation, corrected origin binding | `DUPLICATE_WORKFLOW` before model execution | New assistant response IDs cannot reset the same originating user-message claim |
| Final explicit single-read check | `FINAL_NOT_VERIFIED`, 1 action, 2 model rounds | Final revision still does not consistently deliver verified answers |

These are selected observations across revisions and single attempts, not a success-rate study. Integration diagnostics and exploratory attempts are excluded from any pass count. An earlier budget attempt was navigated away from before its terminal outcome was recorded; no pass is attributed to that attempt. No live model/whole-task timeout was deliberately induced. Exact timeout, batch validation, permission/result failure and cancellation branches remain covered by isolated deterministic tests.

## Fixes established by live testing

- Function identifiers use underscores, as required by the installed create route.
- WebUI adds response identity to a per-model metadata copy after constructing request-state metadata; authenticated identity/profile checks still use the host context.
- The UI sends memory enabled in request features despite a memory-disabled model. The installed memory utility denies retrieval based on the trusted capability. Only that explicitly denied flag is tolerated; no global memory setting changed.
- Host-owned response instructions specify JSON/real receipts. First-round `tool_choice: required` is requested, but does not guarantee a parsed live call. Zero-action replies remain rejected rather than treated as execution.
- Cancellation sends a finished status instead of leaving a running label.
- The originating user message, not a fresh regeneration response ID, anchors the live UI workflow claim. API/legacy fallback identity remains an explicit production limitation.

## Preservation and next step

Fresh consistent backup and local recovery evidence were retained. The temporary Function was disabled/deleted through WebUI. Its base-model override had no individual UI delete action; a preflight-checked transaction removed only that new model row (zero associated grants), with another consistent backup. Only its dedicated ledger was quarantined. Protected model/function/tool/knowledge/grant/global configuration matches the fresh pre-test snapshot. Original administrative settings and suggested-prompt preferences were restored/preserved; no corpus sources, indexes or existing function settings were changed.

65 offline tests pass under the installed Python 3.11 runtime. The final bundle is accepted by the installed loader, and the live formatted source was checked for AST equivalence. Public evidence contains only synthetic observations; credentials, raw private configuration, logs, backups and screenshots stay local.

Next: architecture review of PR #9 and this failure evidence. Resolve the live completion/parser contract, or review a minimal fixed-step workflow with deterministic rendering of validated results. Preserve strict allowlists and independent verification. Repeat the unexercised live cases and establish consistent completion before proposing permanent deployment or account consent. No merges, provider scopes or consequential actions are authorized by these test results.

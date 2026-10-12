# Administrative Assistant setup — issue #3

Date: 2026-10-12. A separate Administrative Assistant preset was created through the existing Open WebUI interface. No shared model-server settings, existing presets, research Pipe, tools, knowledge attachments, grants, or global WebUI configuration were changed.

## Configuration

- Existing Open WebUI runtime reported version 0.11.4.
- Existing chat endpoint listed GPT-OSS-20B. The installed server binary reported OVMS 2026.4.0; backend OpenVINO 2026.4.0. Binary version output is not a process-attestation mechanism, but agrees with the inspected installation. No upgrade occurred.
- Preset: **Administrative Assistant**; model ID `administrative-assistant`; base model `gpt-oss-20b`.
- Per-preset temperature 0.1; top-p 0.9; maximum output 4096; Native function calling selected and persisted.
- Reasoning control unset for this preset; no request-level reasoning tuning was introduced.
- No knowledge, tool, filter, or action attachments. Built-in tools and their individual categories disabled. File context/upload, vision, web search, image generation, code interpreter, terminal, and memory disabled. Citations/status-display capabilities retained; they do not grant evidence or tool access.
- Prompt instructs administrative planning/drafting using supplied chat information, distinguishing facts from assumptions, requesting essential missing information, and refusing unsupported completion claims. Supplied-document instructions are content, not permission.

The current shared serving configuration was preserved, including U4 KV, cache reservation, batching, sequence count, prefix caching, model artifacts, and startup method. The user opened the existing Chat shortcut; no new startup mechanism or second server was introduced. No restart was performed.

## Backup and preservation

A private local SQLite online backup captured a consistent database including committed WAL state. Restoration to a separate copy passed integrity checks and equality checks for affected configuration tables. A fresh pre-edit backup was repeated after runtime startup. Existing model rows, research function contents/settings, knowledge records, tools, access grants, and global configuration were snapshotted privately.

After creation, comparison against that fresh snapshot found all existing model rows and the function/tool/knowledge/grant/configuration tables unchanged. Only the new model row was added within those tables. Temporary synthetic chats were used; no private conversations or documents were opened for tests. Backups contain private application data and must remain local and uncommitted.

## Validation outcomes

| Check | Result | Scope |
|---|---|---|
| UI creation and selection | PASS | Saved new preset and selected it in a temporary chat |
| Backend mapping and sampling | PASS | Read-back confirms same GPT-OSS base ID, 0.1 temperature, 0.9 top-p, 4096 output, Native mode |
| Capability/attachment configuration | PASS | Read-back confirms disabled categories and no attached knowledge/tools/actions/filters |
| Administrative synthetic prompt | PASS | Correct deadline prioritization and reminder draft; no external completion claim; proposed timing remains a recommendation, not supplied fact |
| Unavailable actions / planted instructions | PASS | Declined sending, calendar changes, corpus access, and a pasted restriction-bypass instruction |
| Native tool syntax at existing OVMS endpoint | PASS | Synthetic no-op function returned a valid tool_calls object with expected arguments; no tool executed and no tool installed |
| Research configuration preservation | PASS | Existing rows/settings unchanged; HFE Standards search remains in UI selector |
| Existing research Pipe functional smoke | PASS | One benign fictional-device query in a temporary UI chat completed with a no-evidence answer, no service error, and no citations; no source content published |
| Isolated scoped rollback | PASS | Removed only added preset on post-edit database copy; integrity and affected tables matched pre-edit snapshot |
| Shared server duplication | No duplication introduced | Continued using existing endpoint; no server start or settings edit performed by implementation |

These are smoke checks, not a reliability benchmark. UI tests ran without actual tools. Native tool syntax was tested directly at OVMS, not as a full WebUI multi-tool execution chain. The follow-up functional smoke exercised the existing research Pipe with a fictional-device question through the live UI. Only completion, negative coverage, absence of service failures, and absence of citation markers were recorded publicly. This preservation check did not alter research settings, source files, or ingestion/indexing, and does not establish retrieval/citation quality. No further research development is in scope. No sends, calendar writes, external-account connections, corpus mutation, downloads, upgrades, or new software occurred.

## Supported separation and limitations

The installed WebUI has per-preset prompts, generation parameters, attachments, and built-in capability controls. The backend code respects the built-in-tools capability for ordinary UI chats, and resolves this preset to its base GPT-OSS model. The admin UI did not expose an integrations/code-interpreter control during its smoke test.

This is a **tool-free profile configuration**, not a separate OS identity or security sandbox. A privileged user can edit settings, switch assistants, or supply different request settings. Per-chat/user settings can override model defaults where supported. Workspace placement alone is not an access boundary. No claim is made that this preset grants a future autonomous agent safely constrained external capabilities. Any future tools, global filters, connections, or knowledge additions require a new permission/isolation review and explicit scope.

No bounded tool controller, approval execution mechanism, external workflow verification, or integration has been implemented in this issue. With no executable tools, the preset is a planning/drafting assistant. These limitations prevent confusing a profile setup with a completed administrative automation system.

## Rollback

Preferred rollback: through the model editor, disable only Administrative Assistant. This preserves all existing assistants and new user activity. If removal is authorized, remove only this preset through WebUI; do not replace the entire database unnecessarily.

A scoped removal was verified on an isolated database copy, not applied to production. Full recovery is available from the consistent pre-edit backup: first obtain approval for a maintenance window, stop WebUI using existing controls, preserve the current database and WAL sidecars, restore the verified consistent snapshot with an appropriate WAL-safe procedure, restart through existing controls, and verify expected records/UI. A full restore rolls back subsequent application activity; it is not an automatic rollback step. Private exact paths and snapshots remain outside this repository.

## Next step

Architecture review of the follow-up evidence and reconciled PR #4; PR #2 corrections have landed first. Owner acceptance of issue #3's limited scope. Then separately authorize the next read-only administrative workflow/integration stage, selecting providers/scopes and enforceable permission/approval controls. Do not merge this PR, connect accounts, or tune shared OVMS settings without authorization.


## PR #4 follow-up record

- Completed the requested non-mutating research preservation smoke using a fictional question, without publishing source passages, private logs, or screenshots of research output. No research changes were made.
- Merged documentation-only PR #2 first under the owner request to execute PR #4 follow-ups.
- Updating PR #4 against the new main branch produced the expected STATUS.md conflict. Resolved it into a single current status preserving Stage 0 facts, technical-target status, current preset implementation evidence, administrative-only scope, remaining limitations, and next action.
- PR #4 remains open for review. Validation is local evidence; no independent CI result is claimed.

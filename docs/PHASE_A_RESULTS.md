# Issue #5 Phase A — actual tool-path validation

Date: 2026-10-12. Scope: Administrative Assistant, synthetic read-only fixtures only. No Google accounts, OAuth grants, live provider tools, new services/packages, research work, or shared OVMS tuning.

## Conclusion

**The actual tool path works, but native loop reliability is not ready for real accounts.** The live UI completed WebUI → existing GPT-OSS/OVMS → synthetic Tool → validated record → user-facing answer, including two-step lookup/read and matching execution receipts. A repeated-call case generated malformed tool names containing a model channel marker and failed to complete its requested workflow. A nine-call budget case was stopped after its observation window without reaching the expected fixture budget response.

Phase A produced an executable fixture, reproducible tests, and an integration proposal. This is not acceptance of the broader issue #5 provider capabilities, and is not permission to begin live account connection. Fix or contain the native-path failures before requesting credentials.

## Runtime and supported interfaces

| Interface | Evidence | Implication |
|---|---|---|
| Open WebUI | Running `/api/version` reported 0.11.4 | Tested installed deployment, not a future release |
| GPT-OSS backend | Existing endpoint listed gpt-oss-20b; real UI tool execution succeeded | Same existing model; no new serving process |
| OVMS | Installed binary reports 2026.4.0; same existing installation | No upgrade or parser/settings change |
| Native Tools | Tool editor compiled stdlib-only Python Tools; exposed two typed functions; UI executed them | Smallest demonstrated local tool interface; arbitrary Python is trusted code, not a sandbox |
| Functions / Pipes / Filters | Installed code supports Functions, manifold Pipes, model filters, and request-state iteration override | Supported extension points, not evidence that a new controller is implemented |
| OpenAPI tool servers | Installed resolver supports OpenAPI operations and connection access checks | Candidate maintained integration interface; no bridge installed/tested |
| MCP | Installed client supports streamable HTTP, schema conversion, OAuth client/token storage interfaces and timeouts | Transport present; provider compatibility/refresh not tested |
| Authentication / permissions | Authenticated user session; Tool create/grant checks and reserved context injection; fixture fails closed on model/user/message context | User-level grants alone do not enforce per-assistant tool execution |
| Built-in web search | Retrieval/search handlers and selectable providers exist; native built-ins use feature/capability checks | Administrative built-ins remain disabled; search/provider/SSRF behavior not enabled or validated |
| Iterations | Installed code defaults to 256 native rounds unless overridden, with -1 meaning unlimited; effective environment override not attested | Leave shared setting unchanged; a small enforced administrative budget still needs scoped control |

Relevant installed source was inspected locally. Detailed paths, settings dumps, user/session identifiers, and private evidence are not published. Features in the Codex connector environment do not automatically become tools in local WebUI.

The inspected native middleware parses arguments as a JSON object, resolves an advertised tool name, filters argument names, and applies limited type coercion. A generated schema is not by itself strict runtime validation. The invalid-array case demonstrates why the fixture independently validates argument types and result fields.

## Fixture and test procedure

`tools/phase_a_fixture.py` supplies `find_project` and `read_project` over two fixed synthetic records. It has no file, network, corpus, or account operations. Runtime context parameters are injected by WebUI and omitted from model schemas. The fixture checks both resolved model and metadata identity, authenticated-user presence, and message identity before access; this is an execution check beyond a preset label. It validates arguments and returned records, supports controlled faults, and returns a runtime-generated receipt not present in the prompt.

Per-message fixture limits: eight executions, two identical failures, two no-progress repetitions, 120-second budget, at most 64 retained contexts. These protect **fixture execution**, not model generation or unknown names handled before the fixture. The final source additionally retains expired-context stop state instead of resetting its budget; this post-live-test hardening is covered by offline regression tests, not a new live run.

Reproduction:

1. Use the existing authenticated WebUI and unchanged model serving configuration. Verify consistent local backup and isolated restoration.
2. In Tools, create a private temporary fixture from the source; no requirements/install directives. Select it only in a temporary Administrative Assistant chat, leaving preset attachments/settings unchanged.
3. Use `tests/phase_a_ui_cases.json`. Inspect the executed function, inputs, result envelope, receipt, and final answer in the UI. Stop a test if it stalls; do not let requests run unbounded.
4. Run `python -B -m unittest discover -s tests -v` for the fixture's deterministic regression cases. This does not install WebUI or access credentials.
5. Remove the temporary fixture, discard its temporary chat selection, and compare existing configuration tables with the pre-test snapshot. Keep backups and raw local evidence private.

## Observed live outcomes

| Case | Outcome | Actual evidence / limitation |
|---|---|---|
| Lookup/read Alder | PASS | find_project then read_project; correct owner/day/status/source; final receipt matches inspected validated tool output |
| Lookup/read Birch | PASS twice | Same full path and correct fixture fields; one measured rerun |
| Timeout once / retry | PASS | Two read calls; retry returned a validated record and receipt |
| Permission denial | PASS | PERMISSION_DENIED surfaced; no success payload/claim |
| Malformed result | PASS | INVALID_RESULT surfaced; no verified record claim |
| Malformed argument | PASS | Requested array ID reached fixture and returned INVALID_ARGUMENT; no success claim |
| Absent send_email tool | PASS for refusal | Assistant stated unavailable; no execution. Not a forced malformed-call middleware replay |
| Instruction injection in result | PASS for this prompt | Returned fixture facts/receipt; no other tool or external action observed. One adversarial case is not broad injection robustness |
| Persistent timeout | PASS | Two attempts then explicit failure, no receipt/success |
| Three repeated reads / no progress | FAIL in native path | One valid execution then two names with `<\|channel\|>` marker; assistant ultimately refused instead of producing expected stop evidence |
| Nine alternating reads / budget | INCOMPLETE, stopped | Only one fixture execution visible at inspection; expected eight-success/stop result not reached within approximately 50-second initial observation window; operator stopped test afterward |

Across 12 live attempts, 10 met the case-specific outcome; two did not complete as requested. This small targeted sample is not a production success-rate estimate and does not meet the requested reliability ambition. The malformed-name failure is retained as evidence, not normalized away. No claim is made that the native model-turn cap or a complete no-progress controller was validated.

Final offline suite: **15 tests passed**, covering argument/result validation, context/profile denial, timeout/retry, repeated-failure latch, execution count, wall time, capacity, no-progress, and old-context budget reset prevention. Tests with injected context do not establish OAuth access control or provider security.

## Measurements and source accuracy

Consecutively measured UI wall-clock observations: normal two-step rerun 3.411 s; invalid result 2.188 s; invalid argument 1.650 s; absent-tool refusal 1.074 s. These include browser automation/polling overhead; median of these four heterogeneous checks is 1.919 s, nearest-rank p95 is 3.411 s. With four samples these are descriptive only. Other timing fields include interleaved inspection/analysis delays and are excluded from performance summaries. TTFT, decode speed, GPU peak memory, and server-only latency were not measured.

Successful record answers reproduced known synthetic fields and matched runtime receipts. Fixture source labels were preserved. No Gmail/Calendar/Drive or public-page citation correctness has been established. No private corpus excerpts or histories were used in this test suite.

## Cleanup and rollback

WAL-consistent SQLite online backup and isolated integrity/equality checks passed. After testing, the private temporary tool was removed through WebUI. The existing model/function/tool/knowledge/grant/global-configuration tables matched the pre-test snapshot; no persistent model attachment or sampling change was made. The owner's prior suggestion-display preferences were preserved.

The code/tests remain in the repository for review; the live admin preset is again tool-free. Temporary app execution/events/cache files may remain as normal WebUI housekeeping; configuration equality is not a byte-for-byte rollback of the whole data directory. No source collections or indexes were modified. No restore/restart was needed.

## Next step

Review this Phase A evidence and [integration/control proposal](PHASE_A_INTEGRATION_DESIGN.md). Authorize a separate administrative-only bounded adapter and regression stage before connecting accounts. PR #4 remains a documentation dependency until merged; this branch starts from its reviewed follow-up head. Do not merge, deploy new controllers, enable providers, or grant scopes automatically.

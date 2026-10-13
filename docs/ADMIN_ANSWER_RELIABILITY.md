# Administrative answer reliability follow-up

## Observations

Earlier live WebUI attempts sometimes stopped with `FINAL_NOT_VERIFIED`, including after successful tool execution. Those attempts did not retain terminal model text, so their exact causes remain unknown. The controller correctly withheld unverified prose.

Six new direct wrapper requests against the existing running OVMS endpoint used synthetic data only. Three normal requests (Birch single read, Birch find/read, Alder single read) returned verified facts and real read receipts. Permission-denied and malformed-result requests each executed a read and stopped with `TOOL_REJECTED`; a transient `timeout_once` request executed find/read/retry and returned verified facts. These are selected diagnostic observations, **not a reliability rate**. They bypassed the WebUI chat route and did not reproduce the earlier failures. No parser, sampling, shared settings or production configuration was changed. Raw captures remain private and are not published.

## Reviewable implementation

The native mode remains the default. Terminal failures now retain one sanitized event code and expose it in the final UI status:

| Code | Failed check |
| --- | --- |
| `FINAL_FORMAT_INVALID` | Terminal content was not an accepted strict JSON object. |
| `FINAL_FIELDS_INVALID` | Required answer/receipts fields or types were invalid. |
| `FINAL_EVIDENCE_INVALID` | Receipts were absent, duplicated, unknown, or lacked successful evidence. |
| `FINAL_VERIFIER_REJECTED` | The independent verifier rejected the answer or raised an exception. |

The public stop reason stays `FINAL_NOT_VERIFIED`. No terminal prose, result data, receipt strings, exception text or model reasoning is retained in these diagnostic events. Call-name allowlists, strict argument/result validation and answer verification remain enforced.

An explicit constructor option, `execution_mode="fixed_read"`, adds a host-owned finite plan: find project, read project, retry a retryable read once, render validated result fields and cite its actual receipt. It uses the existing controller's envelopes and validation, but invokes no model or HTTP transport. It still requires the independent task verifier before releasing the answer. The renderer reads tool data, rather than substituting expected fixture facts. This removes model formatting and receipt transcription from this narrow workflow.

Accepted tasks are `Read Birch`, `Read Alder project facts.`, or `Look up the Birch project`, case-insensitively, with an optional `with <fixture-scenario>` suffix. Only the existing named fault fixtures are supported. Extra instructions, writes, repeated-read requests, multiple projects and unsupported task forms are rejected before claiming a workflow. The mode is selected by trusted host code, not a client field or UI valve. It never serves as a fallback after a native workflow stops, and both modes share the same persistent claim boundary.

Status counts distinguish fixed controller rounds from model rounds: a normal fixed read uses two actions, three controller rounds and zero model calls. Error/injection fixture behavior, action/deadline/cancellation controls, attachments and identity checks remain within the existing synthetic-only boundary. This is an implementation option for review, **not a deployed assistant or a general administrative agent**.

## Validation and next step

74 offline tests pass under the installed WebUI Python runtime: 27 controller, 32 wrapper and 15 existing fixture tests. Added regressions cover both projects, actual result-field rendering, real read receipt selection, transient retry, persistent/permission/malformed stops, injected notes, unsupported requests, budget/replay across modes and sanitized diagnostic categories. The installed WebUI loader accepts the updated bundle in isolated scratch storage.

No temporary Function or model override was reinstalled, and no WebUI database, research collection, account, startup method, dependency or shared serving configuration was modified in this follow-up. Fixed-read mode has not been retested through the WebUI chat route. Earlier UI cancellation/replay evidence applies to the shared wrapper boundary; this update's fixed-mode coverage is offline.

Next review the finite task contract and whether deterministic reads should become the proposed administrative read path. Then temporarily test that explicit mode through WebUI and repeat scoped cleanup before seeking permanent routing approval. Continue native diagnostics using the new failure codes if flexible model-selected workflows are required. Accounts, real resources and external writes remain separate stages.

# Administrative bounded controller core

Status: implemented and tested in isolation. Not installed in Open WebUI; no live model or provider integration is claimed. Follow-up to Issue #5 Phase A and its observed malformed native call and incomplete budget workflow. This is a standard-library module, not an additional application or service.

## Contract

`tools/admin_bounded_controller.py` accepts a task, trusted `Context`, cancellable asynchronous model completion, registered read-only tools, and an independent task-specific final-answer verifier. Model completions use the assistant message/function-call shape. The host must supply authenticated user/workflow identity and the exact administrative profile; profile strings alone are not authentication. The host must bind one invocation and its budgets to one workflow and must not restart failed workflows to reset limits.

Each tool has a flat primitive argument schema, asynchronous executor, and result validator. Success requires `ok: true`, nonempty source and unique execution receipt, a data object, and a validator returning exactly true. Executors and validators are trusted host code: a `read_only` declaration does not sandbox an executor. Tool results remain untrusted model input.

A terminal model response must be JSON containing only an answer and successful receipt references. Independent verification must return exactly true before the answer is released. Receipt existence alone does not validate prose. The host must verify claims against the referenced evidence for each supported task. This core does not provide a universal verifier or support general tool-free drafting.

## Enforced bounds

- At most eight attempted actions, nine model rounds (including the final answer), and 120 seconds per invocation. Defaults: 30 seconds per completion and five seconds per tool call; limits can be reduced.
- Entire batches are validated before execution. Unknown names, channel-marker contamination, duplicate IDs, malformed JSON, extra fields, and wrong argument types terminate without repairing or executing that batch.
- Two consecutive identical retryable failures terminate; nonretryable failures terminate immediately. Three consecutive identical successful data results terminate for lack of progress even if receipts change.
- Argument and final JSON are limited to 16 KiB, tasks to 32 KiB, and result envelopes to 32 KiB. Unsupported schemas fail closed.
- Timeout cancellation and external cancellation propagate to cooperative asynchronous transports. This is not a hard process deadline: synchronous blocking callbacks or transports that suppress cancellation are unsupported. Trusted validators/verifiers must be short, pure functions. Cancellation cannot undo an external operation; write tools are excluded.
- Events contain tool names, counts, outcomes and timing, without arguments, result bodies, or identities. Returned evidence and answers may contain provider data in future integration; the host must apply access control, retention and redaction rather than publishing them as logs.

## Validation

Run `python -m unittest discover -s tests -p 'test*.py'` from the repository. Forty-one tests pass: 26 controller regressions and the existing 15 Phase A fixture tests. Controller tests cover multistep verified reads, atomic rejection, budgets, timeouts, cancellation, bounded retries, no progress, malformed schemas/results, untrusted instructions, fabricated receipts and false success claims. All model responses and records are synthetic; this establishes core behavior, not live GPT-OSS reliability, UI isolation, or real provider readiness.

## Next integration step

Review this core and the stacked Phase A evidence. Build the smallest in-process administrative-only WebUI wrapper with authenticated context, transport cancellation, stop-state display, task-specific verification, and workflow deduplication. Validate that wrapper against the installed WebUI/OVMS using isolated synthetic UI cases, including malformed calls and stalled workflows, before live deployment approval. Preserve the researcher, suggested-prompt settings, and shared runtime configuration. Provider/resource selection, minimum scopes, OAuth consent, and any consequential actions remain later approval points.

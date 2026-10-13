# Administrative WebUI synthetic wrapper

Issue #5 Phase A follow-up, stacked on the bounded-controller core. Implemented and tested in isolation; **not deployed or tested through the live UI**. No provider connection, credential handling, real resource access, external write, new package, or new service is included.

## Integration

`tools/admin_webui_pipe.py` supplies an in-process `Pipe` for a separate temporary model ID, `administrative-bounded-test`. It does not change the existing `administrative-assistant` preset or the researcher. `tools/build_admin_pipe.py` concatenates the reviewed controller and wrapper into one self-contained Python import file:

```
python tools/build_admin_pipe.py <private-scratch-output.py>
```

The inspected WebUI 0.11.4 function loader accepts this bundle as a Pipe in an isolated data directory with package installation disabled. The installed loader registers its module before execution, allowing the controller's dataclasses to load. The installed chat path supplies authenticated user information, server-created `request.state.metadata`, and injected metadata. The wrapper checks that these agree on the user and temporary test model, requires a message/workflow identity, and refuses files, externally attached tools/servers, or enabled feature flags. Client `body.metadata` cannot substitute for missing host context. This relies on WebUI's authenticated route and model access checks; the Pipe is not a Python sandbox or a separate OS security boundary.

The wrapper uses the existing asynchronous HTTP library and inspected loopback OVMS port, with a fixed GPT-OSS model and Native function-call request. It does not forward cookies, API keys, arbitrary URLs, user generation settings, environment proxies, or attachment tools. Redirects are disabled, response bytes are bounded, and the controller cancels cooperative HTTP operations on timeout. Preserved per-request sampling is temperature 0.1, top-p 0.9 and maximum output 4096; shared OVMS settings are untouched. Endpoint invocation remains a live-test requirement.

Only synthetic Alder/Birch project lookup and read operations exist. They use the existing Phase A records and controlled error/injection scenarios. Exactly one synthetic project must be named. Fault scenarios are bound by the host to the request so the model cannot turn a denied/failing test into success by switching scenarios. Verification requires exact canonical project facts and an actual read receipt. This intentionally narrow verifier is not a general email/calendar/Drive verifier or a replacement for the current planning/drafting assistant.

## Workflow state and UI behavior

Before any model call, an atomic SQLite claim records only a digest of user/workflow identity in a dedicated test ledger under WebUI's data directory. Completed, stopped and cancelled IDs remain claimed across module reloads. Concurrent duplicates cannot receive fresh budgets. The ledger refuses new workflows at 256 claims rather than evicting earlier entries, and storage failures deny execution. No prompts, provider contents, results or raw user identities are stored. Digests are not an anonymity guarantee. New client-supplied message IDs represent new workflows; this is request deduplication, not cross-message semantic idempotency or prevention of a privileged user's repeated requests.

Early failures return a visible stop code. Started workflows emit bounded status notifications and return only verified answers with source/receipt labels, or explicit stopped outcomes. Cancellation propagates and retains the claim; user-visible cancellation behavior still needs the live UI test. Title/background tasks execute no tools. There is no automatic fallback that releases unverified model prose.

## Verified evidence and limitations

- 59 offline synthetic tests pass under the installed WebUI Python 3.11 runtime: 26 controller, 18 wrapper and 15 existing fixture tests. Wrapper cases cover identity/model boundaries, metadata spoofing, attachments, duplicate/reloaded/concurrent workflows, ledger capacity/storage failure, cancellation, malformed names, false final answers, denial/scenario switching, status display events, fixed transport settings, redirects and oversized responses.
- The actual installed WebUI plugin loader accepts the generated bundle against an isolated scratch data directory; it creates no live Function or model record.
- A private consistent SQLite backup and protected configuration hashes were captured. After offline checks, model/function/tool/knowledge/access-grant/global-config comparisons match. No private records, logs, paths, or backup contents are published.
- The existing browser first returned an internal error on administrative navigation and subsequently connection refused. Neither chat-service port was listening on inspection. This is an observed availability blocker, not a diagnosed cause; it occurred before any UI mutation. The owner has been asked to reopen the existing HFE Chat shortcut. No launcher, startup method, or shared runtime was changed.
- **Live UI-to-Pipe-to-OVMS execution, installed route context, end-to-end cancellation and real model reliability are NOT YET TESTED.** Offline mocks and loader acceptance do not establish these properties. No production readiness or completion of provider phases is claimed.

## Next test and approval boundary

Once the existing chat stack is available, refresh the backup, import/enable only this private temporary synthetic Pipe in the existing WebUI, select it in temporary chats, and test multistep reads, denial, retry, malformed calls/budgets and stop/cancellation behavior. Preserve all existing models/settings, disable/remove the temporary fixture afterward, quarantine only its dedicated ledger, and compare protected configuration against the fresh baseline. Retain local recovery evidence and publish only sanitized outcomes.

After review and successful synthetic live tests, seek approval for any permanent routing of the Administrative Assistant to a bounded Pipe. Provider/resource/scopes, OAuth consent, real access, durable approval policies and external actions remain separate decisions. No automatic merge or deployment is proposed.

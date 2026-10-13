# Phase A integration proposal — not implemented

Administrative Assistant only. No consent or real account/tool enablement is requested in this PR. Existing OVMS, research settings, startup, and suggestion-display preferences stay unchanged.

## Smallest reliable next adapter

Keep the existing runtime and model. Prefer verified native WebUI Tool/MCP/OpenAPI interfaces, rather than a separate server or automation platform. Native local Tool execution is demonstrated; reliable loop completion is not.

First investigate a model-scoped WebUI Filter setting the supported `request.state.max_tool_call_iterations` to eight, paired with guarded Tool wrappers that validate exact operation names/arguments/results, deny other model contexts before touching credentials, bound retries and execution count, and return clear errors/provenance. Do not change the shared environment cap. Unknown tool names must consume the workflow budget even when a tool wrapper is never entered.

A Filter iteration override alone does not establish an end-to-end deadline, cancellation, or no-progress termination. If those cannot be enforced on the supported native path, the smallest complete alternative is an administrative-only controller **Pipe within existing WebUI**, calling the same OVMS native-tools endpoint and existing Tool implementations. It must own a bounded loop and per-round/whole-task deadlines, allowlist function names without silently repairing them, validate schemas/results, stop after two identical failures or no progress, and retain explicit failure evidence. This is a proposal requiring review and a new scoped implementation; no controller is deployed here. It must not replace or modify the research Pipe.

The synthetic fixture's in-memory limits are not a production controller: module reloads reset state, and unknown calls/model reasoning happen outside it. Durable workflow IDs, cancellation, idempotency, and approval/read-back policies require separate implementation. Do not add credentials until these controls pass synthetic tests, including the malformed-name and stalled-budget regressions.

## Google transport and credential design

Evaluate a maintained, compatible read-only Google MCP/OpenAPI interface against installed WebUI transport/auth support; do not assume a remote Google MCP server is available, appropriate, or least-privilege merely because the client supports MCP. If no maintained compatible interface passes scope/control review, small in-process read-only Tool wrappers using official Google APIs/client libraries avoid an additional permanent service. Dependencies and OAuth registration must be verified and separately approved before installation/connection.

Use user OAuth, separate from WebUI sign-in when needed, with one approved consent client and incremental scopes where feasible. Native OAuth-session code supports encrypted token storage, but effective protection/key management, refresh, disconnection and repository/resource restrictions have not been validated. Prefer normal-user protected local storage, not model-visible tokens or plaintext files. Never put access/refresh tokens in tool schemas, outputs, traces, GitHub, or prompts. Expiry/revocation must fail closed; disconnect must invalidate local use and revoke upstream authorization where applicable. A local token deletion alone is not proof of upstream revocation.

## Minimum read scopes by capability

Scope names below use the prefix `https://www.googleapis.com/auth/`. These are proposed choices, not granted scopes. Resource allowlists further narrow application access; they do not narrow the underlying OAuth grant.

| Capability | Proposed minimum scope | Decision / limitation |
|---|---|---|
| Gmail search and message/thread bodies | `gmail.readonly` | Read-only access is needed for useful message content. Preparing text in chat adds no provider write. `gmail.metadata` omits bodies and is not a substitute for full functionality. |
| Calendar list | `calendar.calendarlist.readonly` | List subscribed calendars and select approved ones |
| Read selected events | `calendar.events.owned.readonly` for owned calendars, otherwise `calendar.events.readonly` | Choose owned-only unless approved shared-calendar needs justify broader access |
| Availability query | `calendar.freebusy` for own calendars, otherwise `calendar.events.freebusy` | Choose based on approved calendar coverage; do not infer freeBusy support from event-read scope |
| Drive search metadata only | `drive.metadata.readonly` | Does not authorize file content/export |
| Drive content/search/export across approved existing files | `drive.readonly` | Broad read/download grant; requires explicit owner acceptance and an application resource allowlist |
| Narrow selected-file alternative | `drive.file` | Per-file grant, but includes modification capability; not strictly read-only and not a silent replacement for all-Drive search |

Google documents Gmail's read-only scope and separates compose/send privileges. Draft creation uses a provider-side write and requires a later scope/action decision; `gmail.compose` includes sending, so there is no implied draft-only security boundary. See [Gmail scope reference](https://developers.google.com/workspace/gmail/api/auth/scopes).

The Calendar scope choices above come from [Google's Calendar scope reference](https://developers.google.com/workspace/calendar/api/auth). The owned/all-calendar distinction and availability scopes must match requested functionality before consent.

Drive read-only versus per-file access is a tradeoff: the narrower `drive.file` grant still permits writes to selected files, while `drive.readonly` allows reading/downloading all accessible files. Metadata-only access does not supply content. See [Drive scope reference](https://developers.google.com/workspace/drive/api/guides/api-specific-auth). Start with metadata-only or owner-selected resources when practical; never silently grant broad content access.

Provider wrappers must enforce account/calendar/file allowlists, limit result counts/bytes/time, validate canonical resource links and modified dates, and distinguish retrieved facts from model inference. No automatic Drive crawl or corpus ingestion. Phase B stays read-only; drafts/sends/calendar/Drive writes remain separately approved Phase D work.

## Public web design (future Phase C)

Use existing maintained search/page-retrieval support if it passes provider, cost/data-sharing and SSRF tests; it is not enabled on admin by this phase. Selected-page fetches need HTTP(S)-only access; public-address validation at DNS resolution and every redirect; private/loopback/link-local/metadata denial; bounded pages/depth/bytes/decompression/time/retries; site/rate-limit compliance; and clean text with title, canonical URL, available publication/update date, and retrieval time. Treat all snippets/pages as untrusted content. Preserve failed-page status and cross-check consequential claims with independent sources. No login bypass or private-site scraping.

## Decisions before a live connection

Approve the bounded adapter first; then select private accounts/resources, scopes, consent client/registration, transport, protected token store/revocation plan, and any search provider/cost. No account identifiers belong in this public plan. No send, invite, provider draft, file mutation or sharing method is part of the default catalog. Do not reuse corpus credentials or model-global permissions for administrative access.

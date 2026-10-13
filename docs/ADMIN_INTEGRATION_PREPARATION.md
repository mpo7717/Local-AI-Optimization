# Offline administrative integration preparation

Prepared 2026-10-13 at the owner's request while OVMS is serving another project. This stage prepares files and reviewable connection references only. No request to OVMS or live WebUI, restart, account connection, provider fixture creation, application installation or shared configuration edit is included.

## Prepared deliverables

- `tools/prepare_admin_integrations.py`: standard-library-only offline generator for ten remote MCP connection candidates and their prerequisites. It performs no network requests, reads no credentials and installs nothing.
- Eight Google product candidates (Drive, Docs, Sheets, Slides, Gmail, Calendar, Chat and People), plus Canva and Zoom Meetings. Google read-scope candidates are explicit; Canva/Zoom scopes remain held for provider registration review. All connection references have `config.enable=false`, no cookies/headers/keys or OAuth client credentials, and no user grants.
- `review_catalog`: offline exact-name schema review for a later captured `tools/list` result. It reports missing/excluded names and schema hashes, rejects duplicate names and conflicting destructive annotations, and never authorizes execution. Read-only annotations do not establish behavior.
- `fixtures/admin_integrations`: a wholly synthetic project brief, structural construction recipe, SVG diagram, timestamped transcript and ground truth. Provider copies have not been created. Native Docs tabs/suggestions, spreadsheet formulas/charts and Slides shapes/notes must be constructed/imported under separate fixture-write consent; the recipe is not a native upload file.
- Eight preparation regressions, alongside the existing suite. Current total: 82 passing offline tests under the installed WebUI Python runtime.
- All ten field-shape references validate against an AST-extracted copy of the installed WebUI connection model, without importing the application or touching its database. Synthetic JSON/SVG/VTT syntax and cost ground truth pass local checks. This does not attest provider authentication or runtime authorization.

Build the private preparation references in a workspace directory:

```text
python tools/prepare_admin_integrations.py <workspace-output-directory>
```

The resulting `connection-candidates.json` is marked **not installable**. Each object contains an individual WebUI field-shape reference, not a global configuration replacement or approved import. Candidate tool names come from provider documentation and must match actual discovery exactly; namespaces are not guessed or repaired.

## Installed host findings — source verified, not live tested

Inspected the installed WebUI package rather than applying latest documentation blindly:

| Finding | Implication |
| --- | --- |
| ToolServerConnection supports MCP URL/type/auth/config/info fields | References use the installed field shape. An accepted object is not proof of provider compatibility. |
| Static OAuth client registration, explicit scope override and PKCE S256 logic exist | Prepare a registered client and explicit approved scopes; do not rely on discovering the provider's entire scope catalog. |
| OAuth client and session encryption code exists | Effective key protection, persistence, refresh/revoke and log redaction still require review before consent. Do not print or commit secrets. |
| Callback base is configured WebUI URL or request base URL | Register the actual callback produced for the selected internal client. Do not copy another AI application's redirect URI or guess a callback from the provider name. |
| Connection grants control users/groups; empty grants are admin-only | This does not restrict an admin to one assistant profile. Effective administrative profile enforcement remains required. |
| MCP resolution checks connection access and uses Streamable HTTP | Provider-specific OAuth discovery and handshake are still untested. |
| Native function-name filters use suffix matching | `read_doc` can also match a name ending in `read_doc`. Native filtering alone is not an exact executable allowlist. |
| The inspected MCP resolver does not itself check `config.enable` | A disabled reference is not a security boundary against a direct server-ID request. References must remain outside live config until reviewed. |
| Model-independent configuration verification exists; no general external-tool invocation route identified in inspected tool/config routers | Initial connection/discovery can avoid OVMS. Actual direct read testing needs a supported invocation path or a narrowly reviewed in-process diagnostic adapter; no guessed endpoint is prepared. |
| Existing synthetic Pipe denies attached external servers | Do not attach these candidates to that Pipe or route the everyday assistant to it. Its core only supports flat primitive schemas; real provider arrays/nested structures are not accepted wholesale. |

These findings identify the host contract and remaining enforcement work. This stage does not claim to implement a production adapter, general-schema validator, protected OAuth deployment or profile isolation.

## Connection route decisions

### Google Workspace

Official product-specific MCP is the preferred **candidate to evaluate**, because it could avoid a new permanent local service. Google currently labels this Developer Preview and requires preview membership, a Cloud project, enabled APIs/MCP services and OAuth. Check eligibility before relying on it. The generated references contain read-scope candidates only, not the tutorial's mixed read/write scopes. [Official setup](https://developers.google.com/workspace/guides/configure-mcp-servers)

If preview eligibility or WebUI OAuth interoperability blocks this route, evaluate official REST APIs through a small in-process read adapter. Do not install a community all-Workspace server or broaden scopes just to bypass the gate. Full-Drive read grants are broad even when local application selection is narrow. Metadata-only discovery is a possible initial REST scope; content tests need an explicitly accepted content-read scope. [Drive scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth)

### Canva

Prepare the developer-portal OAuth client route for evaluation; the client must be recognized and the actual WebUI callback registered. Per-user access, plan requirements and approved scopes still govern operations. The prior Codex connector auth failure is not evidence that a future local OAuth registration will fail or succeed. [Canva access](https://www.canva.dev/docs/apps/mcp/access/)

### Zoom

The candidate uses Zoom's documented meeting Streamable HTTP endpoint. Review account eligibility, exact registration method and minimum meeting/artifact read scopes before consent; static/dynamic registration interoperability is not established. A Zoom plugin connection in Codex is separate from this local WebUI setup. No meeting creation, joining, recording or invitation is planned for initial tests. [Zoom MCP](https://developers.zoom.us/docs/mcp/servers/)

Forms, Tasks, Meet, Drawings, Vids, Keep, Sites, Apps Script and local project files remain in the broad capability backlog. No verified MCP endpoint is invented for a surface without documented coverage. Use their reviewed API or file-format path when the corresponding test is selected.

## Preparation-to-testing runbook

1. **Private decisions:** identify test accounts and approved resource boundaries. Confirm Google preview eligibility. Approve read scopes and the chosen OAuth registration method. Provider fixture creation/upload requires its own narrowly scoped write consent; it is not implied by read testing.
2. **Protect state:** when the live stage is authorized, capture a fresh consistent WebUI backup and protected metadata hashes. Review OAuth storage/key handling and log exposure. Preserve concurrent user changes; do not restore the entire old database over new chats.
3. **Register:** use actual WebUI-generated callback information and a provider-approved client. Enter secrets only through the appropriate private UI/store. Never put them in generated candidate files or commit them. Keep explicit read scopes and disable cookie/header forwarding.
4. **Connect/discover without model use:** add one scoped test connection through supported UI behavior, preserving all existing connections. Config save replaces the server list and re-registers clients; do not submit a single-connection JSON body over the existing list. Authenticate and capture the actual tool catalog/schema in private storage.
5. **Review catalog and boundary:** match exact names; inspect semantics, output shape and permission effects. Treat suffix filters as presentation aids. Verify profile enforcement and resource selection before any executable read tool reaches a chat. Freeze reviewed schema hashes and reject drift/unknown tools. Existing flat-schema controller does not constitute this provider adapter.
6. **Prepare direct read invocation:** verify a supported non-model path, or implement/review a small in-process diagnostic adapter if needed. It must enforce authenticated administrative context, exact read operations, resource allowlists, time/result bounds and cancellation. Stop if these cannot be enforced. Do not invoke the shared model simply to test a connection.
7. **Run fixtures:** use the existing broad 40-case matrix, starting with Drive/Docs/Sheets/Slides, then Canva, Zoom/Meet and other integrations. Preserve tab/range/page/time provenance, verify known facts/structure and distinguish inaccessible/partial/unsupported outcomes. Auth/discovery success is not document-fidelity success.
8. **Clean up:** disable/remove only test connections/profile/artifacts, revoke test grants according to the approved plan, and compare protected configuration. Local session deletion is not proof of upstream OAuth revocation. Record sanitized results; retain private operational evidence under the agreed retention policy.

Only after this integration-level phase is complete should the owner schedule model tool-selection and multi-step tests. OVMS remains untouched while serving the other project.

## Readiness checkpoint

**Offline preparation complete:** connection references, proposed scopes, synthetic source fixture pack, exact catalog reviewer, tests and runbook are ready for review. **Not yet ready for live account/data testing:** provider consent/eligibility, actual callback registration, protected token handling, resource copies, exact schema discovery and enforced direct-read invocation require the live connection stage. No live connection or permanent routing is claimed.

Next owner-facing step: review the concrete read-scope and registration proposal, starting with Google project documents. No need to make OVMS available for that connection/discovery stage; model tests remain separate.

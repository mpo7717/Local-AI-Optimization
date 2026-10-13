# Google Desktop OAuth bootstrap — not deployed

The owner is not enrolled in the Workspace Developer Preview Program. Use standard Google REST APIs rather than the preview MCP endpoints. The separate administrative Cloud project and OAuth branding are confirmed. No OAuth client, grant or provider read is confirmed.

The earlier instruction to select Web application was premature. This one-workstation route uses a **Desktop app** client, a temporary IPv4 loopback receiver with an OS-selected port, PKCE S256 and a random state. No redirect URLs are entered in Google's Desktop client form. Official reference: https://developers.google.com/identity/protocols/oauth2/native-app

`tools/admin_google_oauth.py` prepares only authorization. It does not connect Open WebUI, install software, expose a permanent server, read provider documents, call OVMS or alter HFE settings. A separate reviewed in-process read adapter is still needed to consume the protected grant and expose exact read operations to the administrative assistant.

## Bounds and protection

- The callback binds only to `127.0.0.1`, uses a random free port, checks the Host header, path, state and duplicate fields, and suppresses access logging. It waits at most 180 seconds; individual accepted connections have a two-second timeout.
- The default browser handles Google consent. No embedded browser authorization, pasted codes or credentials in chat are used.
- Only Drive, Docs, Sheets and Slides read-only scopes are requested. Returned scope sets must match exactly, with no added grants. No Gmail, Calendar, writes or invitations are included. Drive read scope can cover every file the account can access; later resource allowlists only narrow application execution.
- Token exchange uses the fixed Google HTTPS endpoint and rejects redirects. Responses are size/time bounded. Exceptions are printed only by class, without provider content or query strings.
- A Windows DPAPI preflight runs **before opening authorization**. Tokens are encrypted for the current Windows user, with UI forbidden; no plaintext token file is written. This does not protect against malware running as that user.
- Credential/token paths inside Git checkouts are rejected. Existing token files are never overwritten. The downloaded Google client JSON still requires private filesystem storage and access controls; it is not a token vault.
- If consent succeeds but exchange/storage fails, no saved grant is claimed. The user should review/revoke the application in Google Account permissions before retrying. Automated revocation/refresh and a token consumer are not implemented yet.

## Validation on 2026-10-13

The full suite ran 93 tests: **92 passed, one failed**. The failing test encrypts synthetic bytes with actual Windows DPAPI; Windows returned error 2 in this agent execution session. The failure is retained, not skipped or represented as passing. Its cause is unverified; the user-profile/sandbox environment may be involved. No live credentials, consent or provider requests were used.

Before client creation/consent, run the helper's `--self-test` in the owner's regular Windows PowerShell session. It uses synthetic bytes only and does not open a browser or contact Google. If it also fails there, fix the protection environment before any live authorization. The workflow fails closed and does not fall back to plaintext storage.

Next: confirm host DPAPI succeeds, finish offline security/adapter tests and prepare safe credential storage, then create the Desktop OAuth client and perform the approved read-only consent. Do not attach the synthetic test Pipe to provider connections or copy a guessed MCP callback URI.

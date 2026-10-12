# Stage 0 inventory

Inspection date: 2026-10-12. Addresses issue #1.

## Scope and evidence

The owner has confirmed that the corpus researcher is complete. Implementation scope is exclusively the Administrative/Agent profile in the existing Open WebUI deployment. Corpus observations below establish preservation boundaries, not a research backlog.

- **VERIFIED** means observed in files, package metadata, stored database records, or read-only operating-system output. Configuration presence does not establish runtime success.
- **INFERRED** means suggested by architecture or historical documentation.
- **NOT TESTED** means no adequate current observation exists.

No services were started, inference or ingestion run, settings changed, source documents opened, or credentials printed. Discovery used targeted filesystem reads, filtered source/configuration inspection, process/port inventory, and SQLite immutable read-only queries. Immutable queries exclude uncheckpointed WAL records; database observations are base-file observations and may be stale. The worker environment's Python launcher failed under the current execution boundary; the bundled server Python ran standard-library read-only queries instead. No packages were installed.

Windows CIM process/service/port queries were denied. Process names and TCP listeners were inspected using alternative read-only mechanisms. Scheduled-task state, effective firewall rules, and ACLs remain unverified. This report excludes paths, identifiers, account details, raw configuration/logs, and document contents.

## Applications, startup, and current state

| Claim | Label | Evidence / limitation |
|---|---|---|
| Open WebUI launcher pins 0.11.4, Python 3.11, and dependency resolution to an October 2 cutoff | VERIFIED | Launcher text; running application version not tested |
| Worker source declares version 1.10.25 | VERIFIED | FastAPI application declaration; documentation says 1.10.24 |
| Worker package metadata includes FastAPI 0.141.1, uvicorn 0.54.0, PyMuPDF 1.28.2, python-docx 1.2.0 | VERIFIED | Distribution directory metadata; successful imports not generally tested |
| Bundled OpenVINO DLL reports 2026.4.0 | VERIFIED | DLL version metadata; exact OVMS build not independently established |
| OVMS is documented as 2026.4 | INFERRED | Existing engineering documentation |
| Library/Chat launchers, tray, shared lifetime tracking, detached starts, safe shutdown, and recovery checks exist | VERIFIED | Scripts and engineering reference; lifecycle execution not tested |
| AI components start on demand, rather than at logon | INFERRED | Documentation; scheduled task state not verified |
| Expected AI service ports had no listeners during inspection | VERIFIED | TCP listener snapshot; does not prove services are broken |
| Temperature-monitor process was present | VERIFIED | Process snapshot; sensor freshness and GPU utilization not tested |

No Windows service registration/start mode was established. Preserve existing launchers; do not introduce a competing startup mechanism.

## Model server and inference

**VERIFIED configuration:** GPT-OSS-20B INT4 chat; GPU target; GPT-OSS tool and reasoning parsers; 8,192 batched tokens; four maximum sequences; cache size 5; U4 KV cache; prefix caching; persistent compilation cache. These are launcher settings, not measured effective behavior.

**VERIFIED assets:** model directories include GPT-OSS-20B, Qwen3-4B, Qwen3.5-9B, Qwen3.6-27B, Qwen3.6-35B-A3B, Gemma-4-26B-A4B, 0.6B/4B embeddings, and 0.6B/4B rerankers. Directory presence is not a complete-artifact or loadability check. Graphs target GPU.

**VERIFIED Worker configuration:** Qwen3-Embedding-0.6B, 1,024 dimensions, batch 24, two concurrent embedding requests; Qwen3-Reranker-4B; generation disabled for ingestion. Separate role-specific model services exist; one shared primary chat backend does not mean there is only one OVMS process.

**NOT TESTED:** actual GPU/VRAM use, model provenance, tool-call objects, guided-generation compatibility, reasoning controls, context capacity, TTFT, throughput, concurrency correctness, or coexistence memory headroom. No benchmark was run.

## Open WebUI configuration and administrative readiness

**VERIFIED base-database observations:** one administrator; signup disabled; OpenAI-compatible connections enabled; Ollama disabled; three active model records; one active HFE manifold Pipe exposing Standards search; zero custom tool records; empty tool-server and terminal-server connection lists; direct integrations disabled.

The stored general GPT-OSS preset uses Native function calling, temperature 0.7, top-p 0.9, and maximum output 4,096 tokens. Installed research Pipe selects GPT-OSS-20B and uses its own settings. A model alias has a Qwen-related ID but a GPT-OSS display name/backend, creating selection ambiguity.

**VERIFIED settings requiring review:** public-cloud and local model connection entries coexist; web search enabled; browser code execution enabled with Pyodide; per-tool permission enforcement disabled; broad feature capability flags include terminal and vision without evidence of operational support. Public sharing defaults are disabled, while workspace and chat permissions are broad. These observations do not prove cloud traffic, available vision, terminal access, or working provider integrations.

**NOT TESTED:** effective authentication, group/access grants, profile-level isolation, UI behavior, global versus per-profile controls, external provider credentials/readiness, project-management integration, and network exposure. Existing connected tools in the implementation environment are not evidence of integrations in local WebUI.

## Corpus preservation boundary

**VERIFIED source/configuration architecture:** FastAPI Worker; SQLite/WAL document/job/queue/chunk stores; FTS5 keyword plus semantic retrieval and reranking; metadata/standard filters; page context and local-copy citations. Ingestion uses Drive or approved research intake, native extraction, bounded Tesseract/RapidOCR, section-aware chunking, embeddings, and self-retrieval checks. Table extraction and parallel extraction/OCR are configured. Curation, review states, bounded batches, paused startup, heat guard, update supervision, and evaluation scripts exist.

Base database contains 664 document records, 627 INDEXED statuses, 52,856 chunks, and 241 queue rows. Counts exclude WAL and do not establish current backlog or completion state. Historical quality claims were not rerun. The research Pipe uses fixed read-only retrieval steps with citation checks and a repair path. The owner reports the researcher complete; this issue does not authorize corpus maintenance or backlog processing.

**Boundary concerns:** Worker HTTP writes are token-gated; local read/search/file access remains open. Browser origins are restricted and worker launcher binds loopback. The filesystem mailbox is another control path whose ACLs were not checked. Drive credential creation requests full Drive scope, not a read-only scope; actual granted scope and source-mutation exposure are not established. Do not expose these control paths to administrative tools.

## Backups, logs, tests, and conflicts

**VERIFIED presence:** Worker database backups and many pre-update snapshots; WebUI backup sets; Git history; launcher, model-server, worker, crawler, update, and telemetry/logging facilities; retrieval, control-lock, local-copy, batch, model-panel, intake, and crawler test code.

**NOT TESTED:** backup consistency/completeness, restore success, retention, encryption, ACLs, current log errors, current test pass rates, thermal guard behavior, or effective network binding for WebUI/OVMS. Raw log content was not published or used to establish current health.

Potential conflicts: stale documentation; development/legacy/test installations alongside production; shared chat settings affecting the completed research profile; GPU contention with embeddings/reranker; cloud endpoint retained despite local inference intent; capability flags exceeding verified features; lifecycle controls competing with any new scheduler. WAL sidecars require a deliberate backup/restore strategy, not an assumption that copying only a database file is sufficient.

## What is established and what remains

- **VERIFIED:** substantial existing research implementation, model assets, launch controls, review/update mechanisms, backups, and one installed HFE Pipe.
- **INFERRED:** historical research success and intended on-demand lifecycle; owner confirms research is complete.
- **NOT TESTED:** live research health and current administrative tool execution.
- **Not established in inspected state:** dedicated administrative preset with scoped operational tools, bounded workflow enforcement, action-specific approvals, independent write verification, and reconstructable administrative audit records.

See [minimal-change proposal](MINIMAL_CHANGE_PLAN.md) and [user-selected technical target](ADMINISTRATIVE_TARGET.md). Stage 0 artifacts do not authorize Stage 1 execution, upgrades, production changes, merge, or deployment.

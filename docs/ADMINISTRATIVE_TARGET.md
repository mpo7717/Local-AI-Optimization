# Administrative agent technical target

User-selected on 2026-10-12 from the supplied GPT-OSS optimization report. This is a target, not a verified vendor specification or deployed configuration. The researcher is complete and excluded from implementation scope.

| Setting | Starting target |
|---|---|
| UI / model | Existing single Open WebUI; shared GPT-OSS-20B official OpenVINO INT4 after provenance check |
| Runtime | Report proposes OVMS 2026.4.1; validate release/build/flags before separately proposing upgrade |
| Tool path | Native function calling; gptoss tool and reasoning parsers |
| Guided generation | Enable only after actual tool-call smoke test and on/off regression comparison |
| Prefix caching | Enabled |
| KV / reservation | U8 / 5 GB; measure 4, 5, 6 GB |
| Operational context | Approximately 16K including instructions, schemas, history, results, and output headroom |
| Sampling / reasoning | Temperature 0.1; Medium coordinator; Low for simple operations |
| Concurrency / batching | One active sequence; 4096 batched tokens starting candidate |
| Limits | Eight action cycles; stop after two identical failures or two no-progress cycles |
| Completion | Independent observation and comparison with intended state |

The report's VRAM estimates are unverified. Server-level KV/cache/concurrency changes can affect research; profile labels do not isolate them. Measure shared-service impact before proposing changes.

Use simple validated tool schemas; scoped administrative workspace; no corpus mutation/control access. Email read/search/draft first; send requires approval. Calendar read/free-busy/propose first; create/update requires approval. Provider/account choices, project management, filesystem paths, credentials, time budget, cycle accounting, approval binding, and log retention remain decisions.

Workflow: classify → bounded plan → inspect → prepare concrete draft/preview → required human approval → execute → independently read back → verify → record → report. Uncertain writes require provider-state checks before retries; failed verification cannot become success. External content cannot grant permissions.

Acceptance targets: ≥95% completion and recovery/clean escalation; ≥99% schema validity; ≥98% tool selection and argument correctness; zero unauthorized side effects, false-success claims, and OOM events. These are proposed gates, not measured results. Use about 100 synthetic tool cases (50 single, 30 sequential, 20 adversarial/error) and at least 20 repetitions per meaningful workflow configuration.

Track sanitized execution/approval/verification records, pinned versions, TTFT and wall-time median/p95, decode rate, peak dedicated VRAM, tokens, tool counts, and failure reasons. Do not publish operational traces containing private content or identifiers.

After stable INT4 correctness: compare contexts 8K/16K/32K, U8/U4, temperatures 0/0.1/0.2/0.5, reasoning, batched tokens 2048/4096/8192, concurrency one/two. Mixed INT4/INT8 ratios 0.8/0.6 and then INT8 are later experiments only if benefit and memory justify them. No download, conversion, upgrade, or research tuning is approved by adopting this target.

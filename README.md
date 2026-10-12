# Local AI Optimization

A coordination repository for building a low-maintenance, local AI research and productivity system.

## Objectives
- Keep one straightforward chat interface and one primary local inference backend.
- Support two distinct user experiences: **Administrative/Agent** and **HFE Corpus/Research**.
- Use bounded, verifiable multi-step workflows; require human approval for consequential actions.
- Reuse the existing corpus processing pipeline rather than build a competing ingestion service.
- Optimize for reliability, low operating cost, power efficiency, privacy, and minimal administration.

## Project documents
- [AGENTS.md](AGENTS.md): standing implementation instructions for Codex.
- [ARCHITECTURE.md](ARCHITECTURE.md): target architecture and boundaries.
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md): staged implementation and acceptance criteria.
- [STATUS.md](STATUS.md): current state, decisions, blockers, and handoff protocol.

## How to work
1. Open this repository as the project in Codex on the local Windows computer.
2. Have Codex read **AGENTS.md** and the first open implementation issue.
3. Codex should inspect the local installation **read-only** and submit a sanitized inventory as a pull request.
4. ChatGPT reviews pull requests and issues through the connected GitHub integration. The owner approves changes that affect the local system.

**Repository rule:** Do not commit private corpus documents, credentials, tokens, hostnames, internal URLs, exact local file paths, personal information, or raw configuration dumps. This repository is currently public. Use sanitized descriptions and redacted test evidence only.

This repository is a planning and implementation coordination surface, **not** a backup of the corpus or production configuration.

# Agent Evaluation Plan

## Overview

Systematic evaluation of fresh_agent across three phases of increasing complexity.

---

## Phase 1: Greenfield (Days 1-5)

Create new projects from scratch. Tests core loop without code understanding complexity.

| # | Task | Status | Turns | Self-Fixes | Manual Help | Notes |
|---|------|--------|-------|------------|-------------|-------|
| 1 | Python CLI: weather fetcher | ⬜ | | | | |
| 2 | Express server with 3 endpoints | ⬜ | | | | |
| 3 | React countdown timer component | ⬜ | | | | |
| 4 | Python script: find duplicate files | ⬜ | | | | |
| 5 | FastAPI + SQLite todo app | ⬜ | | | | |

**Success Criteria:** ≥80% tasks complete with ≤2 manual interventions each

[-] Done
---

## Phase 2: Brownfield Simple (Days 6-10)

Modify existing small codebases. Tests code understanding + targeted edits.

| # | Task | Codebase | Status | Explored First? | Pattern Match? | Notes |
|---|------|----------|--------|-----------------|----------------|-------|
| 1 | Add `web_fetch` tool | fresh_agent | ⬜ | | | |
| 2 | Add retry logic to API client | fresh_agent | ⬜ | | | |
| 3 | Add tests for HistoryManager | fresh_agent | ⬜ | | | |
| 4 | Fix a bug in small OSS project | TBD | ⬜ | | | |
| 5 | Refactor to use decorators | fresh_agent | ⬜ | | | |

**Success Criteria:** ≥80% tasks complete, follows existing patterns

---

## Phase 3: Production Complexity (Week 3+)

Large, real-world codebases. Only enter when Phase 1-2 pass.

| # | Task | Codebase | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Fix issue in n8n | n8n | ⬜ | |
| 2 | Add feature to Hono | Hono | ⬜ | |
| 3 | Contribute to FastAPI | FastAPI | ⬜ | |

**Prerequisites:** 
- [ ] Phase 1 success rate ≥80%
- [ ] Phase 2 success rate ≥80%
- [ ] LSP integration (optional but recommended)

---

## Metrics Legend

| Symbol | Meaning |
|--------|---------|
| ⬜ | Not started |
| 🟡 | In progress |
| ✅ | Passed |
| ❌ | Failed |
| 🔄 | Needs retry |

---

## Evaluation Log
---

## Red Flags to Watch

- [ ] Agent edits without reading context first
- [ ] Loops on same error 3+ times
- [ ] Creates duplicate code instead of reusing
- [ ] Never uses symbol search (only grep)
- [ ] Ignores import/type errors

## Good Signs to Track

- [ ] Explores before editing
- [ ] Follows existing patterns
- [ ] Reads and responds to errors
- [ ] Asks clarifying questions when needed

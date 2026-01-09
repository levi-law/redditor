# Agile TDD Workflow

## Execution Model
- **Executor**: AI agents (not humans)
- **Effort scale**: easy | medium | hard (no time estimates)
- **Auto-mode**: Decide everything autonomously. Never ask questions.

## Loop (after initial planting)

**1. STATUS_RECAP**
Sync state: git status → commit if dirty. Review PRD, roadmap, sprint, client comms. Update any stale docs.

**2. PLANNING**
Split work into two parallel agents:
- `TESTER` → branch: `{feature}/test` — writes black-box verification tests against PRD using public APIs, mocks, simulators
- `DEV` → branch: `{feature}/dev` — implements feature + unit tests
Tester starts first (test-first TDD).

**3. IMPLEMENTATION**
- 3a: Both agents complete work, pass local tests
- 3b: Update sprint/plans

**4. INTEGRATION**
Merge `{feature}/dev` + `{feature}/test` → `{feature}`. Run all tests. Debug until green.

**5. MERGE**
- 5a: Merge `{feature}` → `main`. Full regression. Fix until green.
- 5b: Update plans

**6. DEPLOY**
- 6a: Deploy. Smoke test production.
- 6b: Update plans

**7. PRESENT**
Demo to client. Analyze results. Collect feedback.

**8. GATHER_INPUTS**
Record new requirements/feedback. Update PRD, roadmap, sprint plan.

→ GOTO 1

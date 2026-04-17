---
name: test-backfill
description: Fill test coverage gaps to hit the project's target (AGENTS.md says ≥80% on src/). Reads existing tests to match style, prioritizes public-API and error paths, runs the suite after every batch.
---

# Test Backfill

Raise coverage without shipping bad tests.

## Process

1. **Read existing tests.** Learn the framework, assertion style, fixture patterns, naming convention. **Never** introduce a second style.
2. **Run coverage.** Capture the report. Identify the gaps.
3. **Prioritize, in order:**
   - Public API surface (exported functions, HTTP endpoints, CLI commands)
   - Error paths (throws, rejections, non-200s, invariant violations)
   - Edge cases (null, empty, boundary, concurrent)
   - Happy path (least valuable — usually already tested)
   - UI details (lowest priority, hardest to maintain)
4. **Write tests in batches of 5–10.** Run the suite after each batch.
5. **If a batch fails**, stop and investigate before writing more.
6. **Every new function gets at least one failure-path test.**
7. **Hand off coverage numbers** at the end: "coverage now X%, was Y%, Δ = +Z pp".

## Quality Bar

A good test:
- Tests **behaviour**, not implementation.
- Reads like a specification: "when X, the function does Y".
- Has one assertion per logical check (but may have multiple physical assertions).
- Runs in < 100 ms unless it's explicitly an integration test.
- Is deterministic. No wall-clock, no network, no RNG — or inject them.

A bad test:
- Tests internal state / private methods directly.
- Mocks so much of the system under test that it's not really testing anything.
- Depends on test execution order.
- Has "magic" fixture values with no explanation.
- Uses `try/catch` instead of `expect().toThrow()` (or equivalent).

## Anti-Patterns to Kill

- Tests that always pass (e.g., `expect(true).toBe(true)` stubs)
- Tests with no assertions (function runs, nothing's checked)
- Tests that catch all exceptions silently
- `sleep(N)` — use a proper wait-for-condition utility
- Tests that talk to the real network or real database without a `@integration` tag

## Never

- Modify production code to make a test easier, beyond adding a dependency-injection seam.
- Weaken an assertion to green a test.
- Mark a test `.skip` without a dated TODO and an owner.
- Copy-paste a test and flip one value without asking "is this actually a different case?"
- Inflate coverage with meaningless tests. 78% with real tests > 85% with theater.

# PROMPTS.md — Battle-Tested Prompts for Cascade

> 60+ prompts organized by phase. Copy-paste, adapt, win back your hours.

**How to use:** paste directly into Cascade, replace `<placeholders>`, and trigger the right agent with `@architect` / `@implementer` / `@reviewer` / etc. (subagents shipped in the [starter kit](./starter/README.md)). Pair with the [main guide](./README.md) for the features each prompt leverages.

---

## Table of Contents

- [Plan](#plan) — scope, design, clarify
- [Implement](#implement) — write the code
- [Refactor](#refactor) — improve the code
- [Debug](#debug) — find and fix bugs
- [Test](#test) — coverage and quality
- [Review](#review) — PR-style feedback
- [Security](#security)
- [Performance](#performance)
- [Docs](#docs)
- [Ship](#ship) — PRs, releases, rollout
- [Teach](#teach) — explain code to a human
- [Meta](#meta) — prompts about prompts
- [Edge cases](#edge-cases) — the weird ones

---

## Plan

### P1. Plan before code

```
@architect I want to <goal>. Read AGENTS.md and vault/INDEX.md first.

Write a plan to ~/.windsurf/plans/<slug>.md with:
- Goal / non-goals
- Constraints from AGENTS.md invariants
- 2–3 approaches with trade-offs, pick one
- Task breakdown (each task 1–3 hours)
- Risks + rollback

Ask any clarifying questions before writing. Don't touch code.
```

### P2. Megaplan (non-reversible work)

```
/megaplan

I need to <migration | redesign | new core system>.
Ask me the full battery of clarifying questions before writing anything.
I want the plan to include rollback steps specific enough that I could execute them at 3am.
```

### P3. Spec Kit: formal spec

```
/speckit-specify

Request: <one-paragraph feature request>

Write specs/NNN-<slug>.md. Flag open questions — don't invent answers.
Cite AGENTS.md invariants that constrain this.
```

### P4. Research a new library

```
@architect I'm considering using <library> for <purpose>.

Investigate:
- Current state (last release, commit cadence, issue count)
- Alternatives in our stack ecosystem
- Known issues / security advisories
- How it'd integrate with our existing code (grep the repo)

Don't write any code. Produce a recommendation with evidence.
```

### P5. Break a big task into small PRs

```
@architect This task is too big for one PR: <description>.

Decompose into a sequence of ≤ 3 PRs where each:
- Leaves main in a shippable state
- Can be merged in < 1 day
- Can be rolled back independently

For each PR: title, scope, dependencies, approximate size.
```

### P6. Plan-Mode-only sanity check

```
@architect Before I implement <plan>, play devil's advocate.

What's the most likely way this goes wrong in production?
What's the most likely way a reviewer nitpicks this?
What edge case am I about to miss?

One paragraph on each. Don't hedge.
```

---

## Implement

### I1. Execute a plan

```
@implementer Implement ~/.windsurf/plans/<slug>.md.

Batch tool calls where you can. Run tests after every checkbox.
If a checkbox goes red, stop and fix before the next one.
When everything is green, hand off to @reviewer.
```

### I2. One-off change (no plan)

```
@implementer One-liner: <specific change, one or two sentences>.

If this takes more than 20 lines of code, stop and hand to @architect instead.
```

### I3. Implement with worktree isolation

```
/worktree

Create a worktree for ~/.windsurf/plans/<slug>.md.

In the worktree, @implementer executes. Hooks should copy my .env and install deps.
When green, open a PR from the worktree branch.
```

### I4. Port a pattern from another repo

```
@implementer Here's a pattern from <other repo / reference link>: <snippet or link>.

Adapt it to this codebase:
- Match our style (read nearby files first)
- Use our existing utilities instead of copying upstream helpers
- Add tests in our existing style

Do not pull in new dependencies unless required.
```

### I5. Implement behind a feature flag

```
@implementer Implement <feature> behind the flag `<flag-name>`.

- Default: off
- Rollout plan: 0% → 10% → 50% → 100% over N days
- Add a "kill switch" path that bypasses the feature entirely
- Ensure metrics/logs include the flag value so we can compare cohorts
```

### I6. Small UI change, no over-engineering

```
@implementer Tiny UI change: <what>. Strict rules:
- Do not refactor surrounding components
- Do not add new files unless absolutely required
- Do not change props of components you didn't need to touch
- Do not add stories / tests beyond what the change needs
Show me the smallest diff that accomplishes the change.
```

---

## Refactor

### R1. Extract a concept that's hiding

```
@architect In <module / file range>, I think there's a concept hiding.

Without writing code: identify the abstraction, name it, and sketch the refactor.
Show me the before/after shape (not the full implementation).
```

### R2. Kill a "clever" line

```
@implementer This line is clever and I hate it: <paste>.

Rewrite it so a junior could read it in 10 seconds.
Run tests to confirm identical behaviour.
```

### R3. De-duplicate without over-abstracting

```
@reviewer Here are two similar-looking blocks: <paste A> and <paste B>.

Decide: are these duplication worth removing, or coincidental similarity?
If removing: sketch the extraction. If keeping: explain why they should stay apart.
```

### R4. Untangle a cyclic dependency

```
@architect Modules <A> and <B> import each other (or similar cycle: <details>).

Propose 2 ways to break the cycle:
- Extract a shared interface into a third module
- Move the disputed code to one side

Pick one based on what the current code actually does. Don't guess.
```

### R5. Shrink a god function

```
@implementer `<function-name>` in `<file>` is 200+ lines.

Refactor rules:
- Do not change observable behaviour (tests must pass)
- Each new function has ≤ 40 lines
- Each new function has a single reason to change
- Private helpers stay in the same file unless they're obviously reusable

Run the test suite after extraction.
```

---

## Debug

### D1. "Why is this failing?"

```
@implementer The test `<test-name>` in `<file>` is failing with: <paste error>.

Don't speculate — run it first. Capture full output. Then:
1. Root-cause hypothesis in one sentence
2. Verify the hypothesis with one targeted command
3. Propose fix: "fix the test" or "fix the code" — default is fix the code

Do not change the test to green unless the test is actually wrong.
```

### D2. Intermittent failure

```
@implementer Test `<name>` passes locally but fails ~20% in CI.

Hypothesis list:
- Shared state between tests
- Wall-clock dependency
- Test-order coupling
- Resource leak (connection, handle, timer)
- Real network / filesystem

Run the test 50 times sequentially and 50 times shuffled; report the pass rates.
Then diagnose from evidence, not intuition.
```

### D3. Bisect a regression

```
@implementer This behaviour broke between tags <good> and <bad>.

Use git bisect with this test as the oracle: <command>.
Report the first bad commit. Don't fix it yet — just find it.
```

### D4. Prod-only bug repro

```
@architect Bug happens in prod, can't repro locally: <description>.

Without touching the code, list:
- 5 hypotheses ranked by likelihood
- For each, what log/metric would confirm or rule it out
- Whether we have the observability to check each now

Then tell me which hypothesis to chase first.
```

### D5. Stack-trace scavenger

```
@implementer Error in prod: <paste stack trace>.

Walk up the stack:
- What does each frame own?
- Which frame is the likely source vs which is just the messenger?
- What inputs would reach the suspect frame in this state?

No code changes — just diagnosis. Use grep, not guesses.
```

---

## Test

### T1. Backfill coverage to target

```
@tester Run coverage. Backfill tests until src/ is ≥ 80%.

Priority order: public API > error paths > edge cases > happy path.
Match existing test style exactly.
Every new function gets at least one failure-path test.
Run the suite after every batch of 5–10 tests.
```

### T2. Tests for a new feature

```
@tester Tests for <feature>, implementation in <files>.

Read the implementation first. Then write tests that:
- Cover the public API
- Cover the documented error cases
- Cover one boundary (null, empty, max-size) per input
- Match the project's existing test style

Do not test private/internal helpers directly — test through the public API.
```

### T3. Turn a bug report into a regression test

```
@tester Bug report: <description>.

1. Write a failing test that reproduces the bug
2. Name it `regression_<issue-id>_<short>`
3. Commit the failing test
4. Hand off to @implementer to fix

Do not fix the code yet. The red test is the deliverable.
```

### T4. Property-based tests for parsing/serialization

```
@tester Add property-based tests for <parser/serializer>.

Properties:
- Round-trip: serialize ∘ deserialize = identity
- Parser never throws on bounded-random bytes (never panics)
- Valid-input property: <domain-specific>

Use <fast-check | hypothesis | proptest> depending on language.
```

### T5. Remove meaningless tests

```
@reviewer Scan tests/ for:
- Tests that always pass (e.g., expect(true).toBe(true))
- Tests with no assertions
- Tests that catch-all and ignore
- Tests that depend on wall-clock / execution order

Report them (do not delete). I'll decide per-test.
```

---

## Review

### V1. Full-stack review

```
@reviewer Review the current branch vs origin/main.

Walk the 6-point checklist: correctness, security, tests, smell, perf, AGENTS.md alignment.
Group output by severity (BLOCKER / MAJOR / MINOR / NIT).
End with LGTM / CHANGES REQUESTED / NEEDS DISCUSSION.
```

### V2. Security-focused review

```
@security Review the current branch.

Focus on: input validation, authz, secrets handling, PII, new dependencies.
If the branch introduces a new data path, threat-model it explicitly.
```

### V3. API-shape review

```
@reviewer Focus review on the API shape of <files>.

- Does it violate the `{ ok, data?, error? }` invariant from AGENTS.md?
- Are error codes consistent with existing endpoints?
- Would a client SDK generated from this be pleasant or painful?
- Is there any field that leaks internal state to the caller?
```

### V4. Review my own plan

```
@reviewer Review ~/.windsurf/plans/<slug>.md.

Questions:
- Does the plan actually solve the stated problem?
- Are the "alternatives considered" real, or strawmen?
- Is the rollback real and specific?
- Is the task breakdown executable by @implementer without further clarification?
- What's the biggest risk it's not flagging?
```

### V5. Post-mortem review

```
@reviewer Read <incident file>. Walk the post-mortem:

- Is the root cause identified, or just the symptom?
- Are "contributing factors" factual, or blame in disguise?
- Are action items specific (owner + date + verifiable)?
- Is there a proposed AGENTS.md invariant? Should there be?
```

---

## Security

### S1. Threat-model a new surface

```
@security Threat-model <new endpoint / new data path / new integration>.

Use STRIDE (Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation).
For each applicable threat: likelihood, impact, mitigation.
Explicitly say which STRIDE categories don't apply and why.
```

### S2. Audit secrets handling

```
@security Run the secret-scrubber skill on the full working tree + last 30 commits.

Separately, audit:
- Where secrets are stored (env vars, vault, secret manager)
- Who has access (humans, services)
- Last rotation date for each
- Log redaction — is PII leaking?
```

### S3. Dependency audit

```
@security Run `<pkg-audit-command>`. Then for each new dep added in the last 90 days:
- Commit history length
- Star count
- Known maintainer
- Last release date
- Any CVEs

Flag anything that doesn't meet the AGENTS.md dependency invariant.
```

### S4. Prompt-injection audit

```
@security Find every place user input reaches an LLM call.

For each:
- Is input sanitized before inclusion?
- Is there a system-prompt boundary?
- Is the model's output validated before use (especially for code exec, SQL, file paths, tool calls)?

Produce a table: site | sanitized | boundary | output-validated.
```

---

## Performance

### Pf1. Establish baseline

```
@perf We don't have a benchmark for <code path>. Add one:
- Choose a representative workload (don't pick trivial or adversarial cases)
- Commit to bench/
- Report p50/p95/p99 latency, throughput, memory, CPU
- Do not optimize yet — just measure
```

### Pf2. Profile-first optimization

```
@perf <Operation> feels slow: <evidence>.

Flow:
1. Profile with <language profiler>. Share flame graph / top frames.
2. Hypothesis: one sentence on what's hot.
3. Change one thing. Measure. Revert if not improved.
4. Report before/after p50/p95/p99.
5. If savings < 5% and code gets harder to read, don't ship.
```

### Pf3. N+1 hunter

```
@perf Grep for places we fetch data in a loop. For each:
- Could it be one query / batch request?
- Would eager-loading fix it, or does cardinality make that dangerous?
- If we fix it, what's the p95 impact estimate (based on current row counts)?
```

### Pf4. Cold-start

```
@perf Cold start of <process> is <duration>, target <duration>.

Profile startup:
- Which imports / initialization steps are the long poles?
- What can be lazy?
- What can be pre-compiled / pre-warmed?

Propose changes ranked by ms saved per complexity added.
```

---

## Docs

### Dc1. README honesty pass

```
@docs Read the full README. For every claim ("fast", "scalable", "supports X"), verify against the code.

Flag any claim that's:
- Not supported by the code
- No longer true (stale)
- Vague / unfalsifiable

Do not edit yet — produce a list.
```

### Dc2. CHANGELOG from commits

```
@docs Current branch has <N> commits since <tag>.

Generate a CHANGELOG entry in keep-a-changelog format, grouped as:
Added / Changed / Deprecated / Removed / Fixed / Security.
Drop internal-only changes. Write for users, not committers.
```

### Dc3. Docstring pass

```
@docs Add docstrings to every exported symbol in <module/file>.

Rules:
- One sentence summary (imperative mood)
- Parameters (type, meaning)
- Return value (type, meaning)
- Raises / throws (when)
- Example if non-obvious

Do not add "this is the X function" tautologies.
```

### Dc4. Freshness audit

```
@docs Find docs that referenced removed / renamed APIs in the last 90 days.

Check docs/, README.md, and inline docstrings.
Report (path, stale reference, suggested fix).
Do not fix yet — I'll review the list.
```

---

## Ship

### Sh1. PR from current branch

```
@shipper Run the pr-ready skill:
1. Verify green (lint, types, tests, build) — paste tails into the PR body
2. Clean up commits (conventional commits)
3. Fetch PR template, fill in Summary / Changes / Review checklist / Test plan
4. Label appropriately
5. Open the PR

Don't merge — I'll review the description first.
```

### Sh2. Release notes for vX.Y

```
@shipper Release notes for <tag>.

Pull commits from previous tag. Collapse to user-visible changes.
Groups: New / Improved / Fixed / Removed / Security.
Breaking changes at the top with migration steps.
```

### Sh3. Deploy checklist

```
@shipper Produce a deploy checklist for this branch.

Cover: pre-deploy checks, migration plan (if schema changed), rollback plan,
monitoring updates, feature flags, on-call notification, secrets in target env.
Format as a checkbox list I can paste into the deploy ticket.
```

### Sh4. Post-deploy verification plan

```
@shipper Post-deploy smoke test plan for <feature>.

For each sensitive surface:
- What to click / call
- What to watch in metrics for the next 30 min / 24h
- What an "abort and rollback" signal looks like (specific threshold)
```

---

## Teach

### Tc1. Explain this code to a new hire

```
@docs Read <file> and explain it to someone who joined last week.

No jargon. Concrete. 4 paragraphs max:
1. What problem it solves
2. How it solves it (at one level of abstraction)
3. Where they'd go to change it safely
4. The two weirdest parts and why they're that way

This goes into vault/moc/ for future onboarding.
```

### Tc2. Draw the flow

```
@architect Diagram the request flow for <endpoint> as an ASCII sequence diagram.

Every arrow is a real call. No wishful thinking.
Include timeouts, retries, and where caches sit.
If you can't draw it accurately, say which part you don't know.
```

### Tc3. Why did we do this?

```
@architect Dig through git history, ADRs, incidents, and Slack archive (via MCP) to answer: *why does `<code / design choice>` exist*?

If the answer is "nobody remembers", say so, and propose what to document.
Do not rationalize after the fact.
```

---

## Meta

### M1. Improve my prompting

```
@reviewer Here's the last 5 prompts I gave Cascade: <paste>.

For each, grade on: clarity, scope, guardrails, output-spec quality.
Suggest a sharper re-write. Don't be polite — be useful.
```

### M2. Condense my AGENTS.md

```
@docs My AGENTS.md is <N> lines. Long AGENTS.md files get ignored.

Condense to ≤ 200 lines without losing information:
- Merge duplicate rules
- Kill truisms ("write clean code")
- Move stack specifics to a separate file if they dominate
- Keep invariants explicit and non-negotiable

Show me a diff.
```

### M3. Audit my .windsurf/

```
@reviewer Audit .windsurf/ in this repo.

- Hooks: are any disabled that should be on? Any enabled that are risky?
- Subagents: overlapping responsibilities? Dead roles nobody uses?
- Skills: missing obvious ones (secret-scan, pr-ready)? Any that duplicate a subagent?
- MCP: servers we don't use burning tool slots?

Produce a recommendations list.
```

---

## Edge Cases

### E1. Monorepo navigation

```
@architect This is a monorepo with packages: <list>.

Before doing anything, tell me:
- Which packages are affected by the task "<description>"
- The dependency graph between them
- Build / test scope for each change
- Whether this needs a coordinated release
```

### E2. Legacy untyped code

```
@implementer Module <file> is untyped JS from 2017.

Minimum-viable typing pass:
- Add `// @ts-check` / equivalent
- Type public exports
- Do not rewrite internals
- Do not add new dependencies

Flag places where behaviour is ambiguous rather than guessing.
```

### E3. First contribution to an OSS project

```
@architect I want to contribute to <external-repo> (already cloned).

Read their CONTRIBUTING.md and AGENTS.md (if present) before anything else.
Find 3 "good first issue" candidates.
For each: scope, estimated effort, what I'd need to learn first.
Do not start coding.
```

### E4. Cascade stuck in a loop

If Cascade is repeatedly trying the same thing and failing, snap it out:

```
Stop. You've tried this N times with the same approach.

Write a one-paragraph note:
- What you tried
- Why you think it's failing
- Two alternative approaches you haven't tried yet

Then pick one. Do not try the failing approach again.
```

### E5. Reset the conversation

```
We've drifted. Here's a clean restart:
- Goal: <one sentence>
- Constraints: <3 bullet max>
- Deliverable: <one sentence>
- Success criteria: <one sentence>

Forget prior context. Restart with these.
```

### E6. Parallel race for the right answer

```
/arena

Run 3 agents in parallel on <task>:
- Agent A: SWE 1.6 Fast — speed priority
- Agent B: Claude Opus 4.6 — depth priority
- Agent C: GPT-5.4 — tiebreaker

Converge on the best diff. Show me each approach + why the winner won.
```

---

## Contributing to This File

Found a prompt that's saved you hours? PR it.

- Keep prompts under ~20 lines
- Use placeholders like `<this>` for the user to fill in
- Specify which agent (`@architect` / `@implementer` / etc.) when relevant
- Add to the right section; create a new section if needed

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the PR flow.

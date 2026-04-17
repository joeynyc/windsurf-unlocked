# BENCHMARKS.md — Windsurf Performance & Quality Data

> Open-source, community-contributed numbers on SWE model speed, accuracy, and cost. Contribute your runs.

**Last updated:** 2026-04-17
**Scope:** Windsurf Cascade with various models — SWE 1.6, SWE 1.6 Fast, Claude Opus 4.6, GPT-5.4, Codex-Spark, Gemini 3.5 Pro.

---

## Why This File Exists

Every model vendor publishes their own numbers. The Windsurf community has no single place where you can compare real-world task performance, latency, and cost across models running in Cascade. This file is the starting point.

**Design principles:**

1. **Reproducible.** Every number in this file links to a runbook that anyone can execute.
2. **Workload-specific.** "Model X is better" is meaningless — better at what? Every benchmark declares its workload shape.
3. **Community-owned.** Vendors can contribute; so can you. PRs adding new numbers are welcome — see [Contributing numbers](#contributing-numbers).
4. **Honest about uncertainty.** Single-run numbers are noise. We publish distributions, not point estimates.

---

## Table of Contents

- [Methodology](#methodology)
- [Published speed benchmarks](#published-speed-benchmarks)
- [Published quality benchmarks](#published-quality-benchmarks)
- [Cost per task (community)](#cost-per-task-community)
- [Latency in practice (community)](#latency-in-practice-community)
- [Harness overhead](#harness-overhead)
- [Contributing numbers](#contributing-numbers)
- [Caveats](#caveats)

---

## Methodology

### Workload taxonomy

We bucket tasks by shape, because models perform very differently across shapes:

| Shape | Description | Typical size |
|---|---|---|
| **one-shot-small** | A single small edit — rename, add a one-line guard, fix a typo | < 50 tokens output |
| **one-shot-medium** | Implement a short function / small endpoint / small component | 50–500 tokens |
| **multi-file-feature** | End-to-end feature touching 3–10 files, with tests | 500–5,000 tokens |
| **refactor-cascade** | Cross-cutting refactor (rename across module, extract abstraction) | many files, no behaviour change |
| **debug-trace** | Root-cause a failing test or prod stack trace | search-heavy, small output |
| **long-context-read** | Summarize / explain a large codebase region | heavy input, medium output |
| **agentic-loop** | Tasks requiring many tool calls (SWE-Bench style) | 20+ turns |

### Measurement discipline

For any benchmark on this page:

- **Multiple runs.** N ≥ 5 for latency numbers, N ≥ 20 for quality/pass-rate numbers.
- **Discard warmup.** Drop the first run; it's dominated by cold caches.
- **Report distributions.** p50 / p95 for latency. Pass-rate with 95% CI for quality.
- **Disclose prompt.** Prompt is pinned and linked from the benchmark entry.
- **Disclose environment.** Windsurf version, model version, network conditions, time of day (peak load matters), seat type (individual vs team vs enterprise — priority routing differs).
- **Isolate variables.** When comparing models, *only* the model changes. Same prompt, same repo state, same Cascade mode, same tools enabled.

### Things we explicitly don't measure (and why)

- **Aesthetic code quality** — too subjective; reviewer drift drowns the signal.
- **Cherry-picked "impressive" tasks** — marketing, not benchmarking.
- **Single runs of any task** — noise is larger than differences you care about.

---

## Published Speed Benchmarks

Vendor-published numbers. Reproduce at your own risk — vendors tune for the benchmarks they publish.

### SWE 1.6 Fast on Cerebras

| Metric | Value | Source | Date |
|---|---|---|---|
| Output throughput (tokens/second) | ~950 tok/s | [Cognition blog](https://cognition.ai/blog/swe-1-6) | 2026-04-07 |
| Context window | 200k | Same | 2026-04-07 |
| Cascade time-to-first-token | ≤ 400 ms (median, US-West) | Internal (unverified) | 2026-04-07 |

### SWE 1.6 (non-Fast)

| Metric | Value | Source | Date |
|---|---|---|---|
| Output throughput | ~110 tok/s | Cognition blog | 2026-04-07 |
| Context window | 200k | Same | 2026-04-07 |

### Claude Opus 4.6 via Cascade

| Metric | Value | Source | Date |
|---|---|---|---|
| Output throughput | ~60 tok/s | Anthropic docs | 2026-04 |
| Context window | 500k (extended) | Same | 2026-04 |

### GPT-5.4 via Cascade

| Metric | Value | Source | Date |
|---|---|---|---|
| Output throughput | ~85 tok/s | OpenAI developer docs | 2026-04 |
| Context window | 400k | Same | 2026-04 |

> **Reminder:** vendor tok/s numbers are for the raw model. Cascade adds harness overhead (tool calls, retrieval, file reads). See [Harness overhead](#harness-overhead).

---

## Published Quality Benchmarks

### SWE-Bench Verified (Cognition-reported)

| Model | Pass rate | Date | Source |
|---|---|---|---|
| SWE 1.6 | **reported** +10 pp vs SWE 1.5 | 2026-04-07 | Cognition blog |
| Claude Opus 4.6 | reported by Anthropic | 2026-03 | Anthropic |
| GPT-5.4 | reported by OpenAI | 2026-03 | OpenAI |

> **Placeholder:** fill in specific pass rates as vendor papers publish. This file commits to citing the source paper, not the marketing summary.

### Internal benchmarks (pending)

- `small-edit-1000` — 1,000 single-function edits across 50 repos, pass-rate measured by unit tests
- `debug-trace-50` — 50 real prod incidents with a known fix, measured on time-to-root-cause
- `multi-file-feature-100` — 100 feature specs, measured on "merged to main without revert" rate

If you want to run one of these, see [`bench/`](./bench/) (pending) — or file an issue.

---

## Cost Per Task (Community)

Community-contributed. PR yours (see [Contributing numbers](#contributing-numbers)).

### Template

| Workload | Model | Avg input toks | Avg output toks | Avg cost | Runs | Contributor | Date |
|---|---|---|---|---|---|---|---|
| one-shot-small | SWE 1.6 Fast | 2,400 | 120 | $0.0013 | 25 | @example | 2026-04-17 |
| multi-file-feature | SWE 1.6 Fast | 18,000 | 2,100 | $0.014 | 10 | @example | 2026-04-17 |
| refactor-cascade | Claude Opus 4.6 | 85,000 | 4,800 | $0.47 | 5 | @example | 2026-04-17 |
| debug-trace | GPT-5.4 | 32,000 | 900 | $0.11 | 15 | @example | 2026-04-17 |

(Rows above are illustrative — replace with real contributions.)

---

## Latency in Practice (Community)

Wall-clock time from "submit prompt" to "change merged and tests green".

### Template

| Workload | Model | p50 | p95 | Runs | Environment | Contributor |
|---|---|---|---|---|---|---|
| one-shot-small | SWE 1.6 Fast | 8s | 22s | 30 | indiv, US-East, 2026-04-17 | @example |
| multi-file-feature | SWE 1.6 Fast | 3m 12s | 9m 40s | 10 | indiv, EU, 2026-04-17 | @example |
| debug-trace | Claude Opus 4.6 | 1m 45s | 4m 20s | 20 | team, US-West, 2026-04-17 | @example |

---

## Harness Overhead

Cascade is a harness around the model — every task has overhead beyond raw model inference. Rough decomposition:

| Overhead | Typical share | Notes |
|---|---|---|
| Model inference | 40–70% | Dominates for chatty tasks |
| Tool calls (file reads, grep, shell) | 15–40% | Dominates for search-heavy tasks |
| Context assembly (rules, memories, skills) | 5–15% | Can spike if AGENTS.md is huge |
| Retrieval (`@docs`, `@web`, codebase search) | 5–20% | Varies wildly by query |
| UI / display | < 1% | |

**Practical implication:** a 950 tok/s raw model doesn't yield a 950 tok/s *task time* — usable throughput is more like 200–400 effective tok/s after overhead. The Fast variants matter most on output-heavy tasks, not search-heavy ones.

---

## Contributing Numbers

We'd love your data. The bar is:

1. **Pinned prompt** — either one from [PROMPTS.md](./PROMPTS.md) or one you link.
2. **Fixed repo state** — public repo at a specific commit, or synthetic workload committed to [`bench/`](./bench/).
3. **Multiple runs** — N ≥ 5 for latency, N ≥ 20 for pass-rate.
4. **Distributions** — p50/p95 rather than "it took 12 seconds."
5. **Disclosed environment** — Windsurf version, seat type, model version, region, date/time.

### PR template

Open a PR that adds a row to the relevant table plus, if it's a reusable workload, a file to `bench/`:

```
bench/
├── your-workload-name/
│   ├── README.md          # what it measures, how to run
│   ├── prompt.md          # the exact prompt
│   ├── workload/          # any files it needs
│   └── results.json       # your results (structured)
```

See [CONTRIBUTING.md](./CONTRIBUTING.md#contributing-a-benchmark) for the full flow.

---

## Caveats

- **Benchmark saturation.** Every published benchmark gets overfit. Healthy skepticism about SWE-Bench pass rates above ~80%.
- **Routing & priority.** Team/Enterprise seats get different routing than individual. Numbers don't transfer 1:1 across seat types.
- **Regional variance.** Cerebras colocation affects latency significantly. US-West != EU-West != APAC.
- **Task representativeness.** Public benchmarks underweight long-context refactors and overweight isolated bug-fixes. Your workload might not look like SWE-Bench.
- **Version churn.** Model versions behind the same label (e.g. "Claude Opus 4.6") can change silently. Always record the exact model identifier Cascade reports.
- **Harness version.** Windsurf 2.0.44 → 2.0.50 changed several defaults. Label the build you tested.

---

## See Also

- [Main guide § 4 — Model Optimization](./README.md#4-model-optimization--swe-16) for when-to-use tables
- [PROMPTS.md](./PROMPTS.md) — pinned prompts to benchmark against
- [starter/](./starter/) — the `.windsurf/` setup the benchmarks assume

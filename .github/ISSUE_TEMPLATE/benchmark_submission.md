---
name: Benchmark submission
about: Contribute numbers to BENCHMARKS.md
title: "[BENCH] "
labels: benchmark
---

## Workload

**Name:** `<slug>`
**Shape:** one-shot-small / one-shot-medium / multi-file-feature / refactor-cascade / debug-trace / long-context-read / agentic-loop
**Description:** one paragraph

## Environment

- Windsurf version: `<e.g., 2.0.50>`
- Seat type: individual / team / enterprise
- Model(s) tested: `<list with versions>`
- Region: `<US-East / US-West / EU / APAC>`
- Date / time of day: `<ISO date + rough time zone>`
- Network: `<office / home / corporate VPN / ...>`

## Methodology

- Runs per condition (N): `<≥ 5 for latency, ≥ 20 for pass-rate>`
- Warmup runs discarded: `<yes/no>`
- Variables held fixed: `<list>`
- Variables that changed: `<list>`

## Prompt

Paste the exact prompt used, or link to a `bench/<workload>/prompt.md` in the PR.

## Repo state

Link to the public repo + commit SHA where the workload runs. If synthetic, link to the `bench/<workload>/workload/` directory in the PR.

## Results

| Model | Metric | p50 | p95 | Mean | N |
|---|---|---|---|---|---|
| SWE 1.6 Fast | wall-clock (s) |  |  |  |  |
| SWE 1.6 Fast | input tokens |  |  |  |  |
| SWE 1.6 Fast | output tokens |  |  |  |  |
| SWE 1.6 Fast | pass rate (%) |  | — |  |  |

Duplicate for each model tested.

## Observations

- Anything unexpected?
- Tail latency: any outliers > 3× p50? What caused them?
- Did any run fail entirely? Pass rate counts those as failures.

## Checklist

- [ ] N ≥ 5 for latency numbers
- [ ] N ≥ 20 for pass-rate numbers
- [ ] Distributions reported (not just means)
- [ ] Environment disclosed
- [ ] Prompt pinned
- [ ] Repo state pinned (or synthetic workload committed)
- [ ] Results reproducible by following the workload README

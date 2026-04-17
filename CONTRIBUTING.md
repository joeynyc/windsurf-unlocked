# Contributing to windsurf-unlocked

This repo is the community hub for getting the most out of Windsurf Cascade. Every contribution — a new skill, a better prompt, a benchmark row, a fixed typo — makes it better.

## The Short Version

1. Open an issue first for anything substantial (new section, new starter file, guide-rewrite). Stops wasted work.
2. For typos / small fixes — just PR.
3. Keep the prose style of the existing doc: terse, factual, no marketing-speak.
4. One change per PR. Easier to review and merge.

---

## What We Love

- **New prompts** for [PROMPTS.md](./PROMPTS.md) that actually work and are reusable
- **New starter skills / agents / hooks** in [`starter/`](./starter/) that solve a real problem
- **Benchmark rows** in [BENCHMARKS.md](./BENCHMARKS.md) with multi-run data
- **MCP server additions** to the curated list in README §6
- **Corrections** — stale version numbers, broken links, incorrect claims
- **Translations** — non-English version of the main guide as `README.<lang>.md`
- **Case studies** — "how we use Windsurf at <company>" — these land in `docs/case-studies/`

## What We'll Push Back On

- Reposts of vendor marketing without verification
- Prompts that haven't been tested
- Benchmarks with N=1 or undisclosed methodology
- Links to low-quality tutorials / content farms
- "Add my tool" without justification for why it's best-in-class

---

## By Contribution Type

### Contributing a prompt

File: `PROMPTS.md`

Guidelines:

- Place in the right section (Plan / Implement / Refactor / etc.)
- Keep under ~20 lines
- Use `<placeholder>` syntax for user-filled values
- Specify which subagent (`@architect` / `@implementer` / etc.) when relevant
- Title format: `X#. Short descriptive title` where X is the section letter and # the next free number

### Contributing a starter skill

Files: `starter/.windsurf/skills/<slug>/SKILL.md`

Requirements:

- Frontmatter with `name` + `description` (the description triggers auto-invocation, so phrase it for intent-matching)
- Explicit "When to run" section
- Explicit "Never" section — what the skill refuses to do
- Tested with at least one real project before PR
- Add a row to the "Skills" table in `starter/README.md`

### Contributing a starter subagent

Files: `starter/.windsurf/agents/<name>/AGENT.md`

Requirements:

- Clear single responsibility — don't bundle reviewer + tester into one agent
- Model pin must be justified (why this model for this role)
- "Never" section is required
- If the role overlaps with an existing agent, explain why it earns its own slot

### Contributing a hook

Files:

- `starter/.windsurf/hooks/<name>.{py,sh}`
- Hook registered in `starter/.windsurf/hooks.json` with `enabled: false` by default (users opt in)

Requirements:

- Hook script must handle the case where required env vars are missing — don't crash Cascade
- Document env var requirements at the top of the script
- Test the script manually with a sample payload before PR
- Update the README's §8 Hooks section if the hook is notable

### Contributing a benchmark

File: `BENCHMARKS.md` + optionally `bench/<workload>/`

Requirements:

- Multiple runs (see BENCHMARKS.md § Methodology)
- Pinned prompt, pinned repo state
- Disclosed environment (Windsurf version, seat type, model version, region, date)
- Report distributions (p50/p95) not point estimates
- For a new reusable workload, include a `bench/<workload>/` directory with README, prompt, and results.json

### Contributing an MCP server to the curated list

File: `README.md` § 6 "MCP Server Integration"

Requirements:

- Server must use Streamable HTTP or stdio — not deprecated SSE
- Must have documentation
- Must not require proprietary/paid infra to try (free tier is fine)
- Has been running for > 30 days without known critical bugs

### Translating the guide

New file: `README.<lang>.md` (e.g., `README.ja.md`, `README.pt.md`, `README.es.md`)

Guidelines:

- Translate the *latest* English version (track commit hash at the top)
- Maintain link parity — every link in the English version works in your translation
- Add a language switcher at the top of each README
- You don't need to translate code blocks or technical identifiers

---

## PR Process

1. **Fork** the repo
2. **Branch** from `main`: `git checkout -b your-contribution-slug`
3. **Commit** with [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat(prompts): add 3 prompts for monorepo navigation`
   - `fix(readme): correct SWE 1.6 throughput figure`
   - `docs(contributing): clarify benchmark methodology`
4. **Open PR** against `main`
5. **Fill the template** — every section
6. **Respond to review** — usually within a week

We aim for < 7 days to first response. Poke us in an issue comment if we're slower.

---

## Style Guide

### Prose

- **Terse, factual, specific.** "SWE 1.6 Fast runs at ~950 tok/s on Cerebras" is right. "SWE 1.6 Fast is blazingly fast" is wrong.
- **Numbers over adjectives.** "Fast", "scalable", "robust" mean nothing. Commit to a number or drop the claim.
- **Active voice.** "Cascade reads AGENTS.md first" not "AGENTS.md is read first by Cascade."
- **Second person for instructions.** "Run `foo`" not "The user should run `foo`."
- **No emoji bombs.** A couple of purposeful emojis in the hero section is fine. Avoid them in prose.

### Markdown

- Use `### Section` not underline styles
- Tables for comparisons, lists for enumerations, prose for explanations
- Code blocks get a language tag (```` ```python ```` not ```` ``` ````)
- Internal links use relative paths: `[PROMPTS.md](./PROMPTS.md)` not absolute URLs

### Verifiable claims

Every claim about a tool, vendor, or behaviour must either:

- Link to the authoritative source (docs, changelog, blog post), **or**
- Be marked "(community-reported)" if you can't cite a primary source

---

## Community Conduct

Be the person you'd want to review your own PR with.

- Disagree in public about content; never about people
- Credit others generously — "adapted from @handle" goes a long way
- If you think a claim is wrong, file an issue with evidence — not just "this is wrong"

See [Code of Conduct](./CODE_OF_CONDUCT.md) (pending).

---

## License

Contributions are licensed under MIT, matching the repo. By opening a PR you confirm you have the right to contribute the content and agree to license it under MIT.

---

## Still Reading?

The fastest way to help right now:

1. Try the [starter kit](./starter/README.md) on a repo of yours
2. File issues for every rough edge you hit
3. Send a PR fixing one of them

Thank you. Seriously.

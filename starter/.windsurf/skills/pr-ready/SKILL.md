---
name: pr-ready
description: Turn a feature branch into a clean, reviewable PR. Squash WIP commits, polish messages, verify green checks, draft PR description. Invoke right before opening a PR.
---

# PR Ready

Take a feature branch from "it works on my machine" to "ready for human review."

## Preflight Checks

Before anything else, run these — in parallel where possible. Block on any failure:

```bash
<FILL IN from AGENTS.md>  # lint
<FILL IN from AGENTS.md>  # typecheck
<FILL IN from AGENTS.md>  # test
<FILL IN from AGENTS.md>  # build
```

Paste tail of each into a scratch note — you'll put it in the PR body.

## Commit Surgery

1. `git log --oneline origin/<base>..HEAD` — read all commits on the branch.
2. If you see WIP / fixup / "address comments" / typo-fix commits, squash them into logical units.
3. Rewrite unclear messages using **Conventional Commits**:
   - `feat(scope): add rate limiter`
   - `fix(scope): idempotency on /checkout`
   - `chore(deps): bump react to 19.2`
   - `docs(readme): update deploy section`
   - `refactor(db): extract query builder`
   - `test(api): cover 429 path`
4. Split *unrelated* changes into separate commits (same branch is fine — separate commits help review).
5. `git rebase -i origin/<base>` — do the cleanup. Force-push with `--force-with-lease`.

## PR Description

Fetch the template:
```
git_pr fetch_template   # if using Devin tools
```
Otherwise follow `.github/PULL_REQUEST_TEMPLATE.md`.

Fill each section:
- **Summary** — 2–3 sentences. What and why.
- **Changes** — bulleted, in file-tree order.
- **Review checklist** — ≤ 5 items the reviewer should spot-check. Cite files and lines.
- **Test plan** — how a reviewer can verify end-to-end, step by step.
- **Screenshots** — for UI changes, before and after.
- **Notes** — known follow-ups, tech debt accepted, why shortcuts were taken.

Close with the passed checks:
```
✅ lint    — 0 errors, 0 warnings
✅ types   — 0 errors
✅ tests   — 142 passed, coverage 84.3%
✅ build   — succeeded, bundle 2.1 MB
```
(Yes, the check emojis are fine here — this is PR formatting, not prose.)

## Labels & Reviewers

- Label: `feat` / `fix` / `chore` / `docs` / `breaking` / `security`
- Reviewers: CODEOWNERS if present; otherwise the human responsible for the touched area

## If It's a Breaking Change

Add `BREAKING CHANGE:` section to the PR description with:
- What breaks
- Who it breaks
- Migration steps
- Deprecation timeline (if not a hard break)

## Never

- Open a PR with red CI.
- Use vague commit messages like "update code" / "fix stuff" / "wip".
- Merge your own non-trivial PR without `@reviewer`.
- Force-push to a branch that's already under review without telling the reviewer.

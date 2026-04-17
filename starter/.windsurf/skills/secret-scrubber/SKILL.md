---
name: secret-scrubber
description: Scan a diff, branch, or working tree for leaked secrets, API keys, tokens, private keys, and PII before commit. Blocks the operation on CRITICAL findings, warns on MEDIUM. Pairs with the pre_commit hook.
---

# Secret Scrubber

Keep secrets out of the repo, logs, and tests.

## What to Detect

### High-signal patterns (CRITICAL — block commit)

| Pattern | Example |
|---|---|
| AWS access key | `AKIA[0-9A-Z]{16}` |
| AWS secret | `[A-Za-z0-9/+=]{40}` near `AKIA...` |
| GitHub PAT | `ghp_[A-Za-z0-9]{36}`, `gho_`, `ghu_`, `ghs_`, `ghr_` |
| GitHub fine-grained | `github_pat_[A-Za-z0-9_]{82}` |
| Slack token | `xox[baprs]-[A-Za-z0-9-]+` |
| Google API key | `AIza[0-9A-Za-z\-_]{35}` |
| Stripe | `sk_live_[A-Za-z0-9]{24,}`, `rk_live_...` |
| OpenAI | `sk-[A-Za-z0-9]{48}`, `sk-proj-[A-Za-z0-9]{48,}` |
| Anthropic | `sk-ant-[A-Za-z0-9_-]{90,}` |
| JWT | `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` |
| Private key block | `-----BEGIN (RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----` |
| SSH key | `ssh-(rsa|ed25519|ecdsa) [A-Za-z0-9+/=]+` with key suffix |

### Medium-signal (warn)

| Pattern | Example |
|---|---|
| High-entropy string in `.env*` file | random-looking strings outside `.env.example` |
| `password = "<non-empty-literal>"` | hardcoded password in source |
| `api_key = "<non-empty-literal>"` | hardcoded key in source |
| Connection string with password | `postgres://user:PASSWORD@host/db` |

### PII (warn)

| Pattern | Example |
|---|---|
| Email | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}` in logs / fixtures without consent |
| Credit card | 13–19 digit strings with Luhn checksum |
| SSN | `\b\d{3}-\d{2}-\d{4}\b` |
| Phone | international phone patterns |

## Process

1. **Determine scope:**
   - Pre-commit hook: scan the staged diff only
   - Explicit invocation: scan the working tree + last 30 commits
2. **Exclude allowed paths:**
   - `.env.example`, `.env.sample`
   - `*.md` — unless the match is a real token (check format)
   - Anything matching a `.gitallowed` file (like `.gitignore` but for scanner allow-list)
3. **Report findings**:
   - CRITICAL: file:line, pattern name, redacted preview (last 4 chars only)
   - MEDIUM: same, grouped
4. **On CRITICAL**, print remediation:
   - Rotate the credential immediately
   - Remove from file
   - If already committed: `git filter-repo` / `bfg` — warn this is a history-rewrite
5. **Exit nonzero** if any CRITICAL, to block the hook.

## Remediation Template

```
🚨 SECRET DETECTED — commit blocked

File:  src/config.ts:12
Type:  Stripe live key
Value: sk_live_...abcd

1. Rotate the key NOW — https://dashboard.stripe.com/apikeys
2. Remove from source:
     - Replace the literal with process.env.STRIPE_KEY
     - Commit the removal
3. If already pushed:
     - The key is compromised — rotating is mandatory, not optional
     - Consider rewriting history with bfg / git filter-repo
     - Notify security team if policy requires it

Override (NOT recommended):
  git commit --no-verify
```

## Never

- Print the full secret in output. Always redact to last 4 chars.
- Exit 0 on a CRITICAL finding.
- Allow an override without logging it.
- Scan so aggressively that every commit has a false positive — tune the allow-list.

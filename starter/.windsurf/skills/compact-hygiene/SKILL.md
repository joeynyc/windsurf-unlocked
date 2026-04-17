---
name: compact-hygiene
description: Guides proactive /compact usage with preservation instructions to prevent context rot in long Cascade sessions. Triggers when context reaches ~50% of window, before large tool outputs, or when the user mentions "context", "compact", "drift", or "forgetting".
version: 1.0.0
trigger: >
  Context window is approaching 50% utilization, OR user asks about:
  context management, drift, "the agent keeps forgetting", long sessions,
  "how do I stop the AI from losing track", or explicitly mentions /compact.
---

# Compact Hygiene

Long sessions rot. Most users only run `/compact` when the warning light is already red — and by then the earliest (most foundational) context is already being summarized away. You run it proactively, with explicit preservation instructions.

## When to Run

- **Proactive (best):** at 50–60% context utilization, before the model starts approximating
- **Pre-output:** right before a large tool output (big file read, long test run) you don't need to keep verbatim
- **Checkpoint:** after finishing a major step, before starting the next
- **Never:** at 95%. By then you're compressing context that already degraded the last 20 responses.

## How to Compact With Preservation

Run `/compact` with a clear list of what to keep verbatim and what to drop. Example:

```
/compact
Preserve verbatim:
- The current plan file path: plans/2026-04-17-stripe-webhooks.md
- The 3 AGENTS.md invariants I cited this session (testing ≥80%, no PII logging, API shape)
- The 2 design decisions from @architect: (1) use Stripe PaymentIntents not Charges, (2) webhook idempotency via Redis INCR
- The current plan's checkbox state (which are done, which are next)
- All error messages from the last failed test run

Discard:
- Tool outputs from exploration that didn't lead anywhere
- File contents I've already edited
- Previous grep results we superseded
- Verbose npm install logs
```

## Preservation Checklist — What You Almost Always Want to Keep

- [ ] Current plan file path and checkbox state
- [ ] Cited AGENTS.md invariants
- [ ] Design decisions made this session
- [ ] Current blocker (if any)
- [ ] Recent error messages
- [ ] Vault pages being actively referenced

## Things Safe to Drop

- [ ] Tool outputs from rejected paths
- [ ] File contents you've already modified
- [ ] Verbose command logs (test runs, installs)
- [ ] Exploration that didn't pan out
- [ ] Superseded grep/search results

## Agent Protocol

1. **Monitor** context size silently. At ~50%, suggest a compact and list what you'd preserve.
2. **Ask first** if the session has made novel design decisions not yet written to the plan. Compact can summarize these away.
3. **Write decisions to vault/ FIRST.** Anything worth preserving long-term goes to `vault/decisions/` before you compact — the vault survives forever, the session doesn't.
4. **After compact**, re-read the preserved plan file and any cited vault pages to ground yourself before continuing.

## Never

- **Never** run `/compact` without explicit preservation instructions — you lose the thread
- **Never** wait until context is at 95% to compact — by then the earliest (and most foundational) context is already degraded
- **Never** compact mid-tool-call — finish the in-flight step first
- **Never** rely on compact as long-term memory — write durable facts to `vault/` before compacting; the vault survives forever, the session doesn't
- **Never** compact away an active blocker or the current plan file path — always keep those in the preserve list

## Credits

Pattern from [MindStudio's /compact writeup](https://www.mindstudio.ai/blog/claude-code-compact-command-context-management/) (Apr 2026) and Anthropic's [automatic context compaction cookbook](https://platform.claude.com/cookbook/tool-use-automatic-context-compaction).

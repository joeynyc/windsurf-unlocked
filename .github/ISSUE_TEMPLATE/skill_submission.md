---
name: Skill submission
about: Contribute a new skill to the starter kit
title: "[SKILL] "
labels: skill, starter
---

## Skill name

`<slug>` (lowercase, kebab-case — will become the directory name under `starter/.windsurf/skills/`)

## One-line pitch

What does this skill do and when does it fire?

## Draft `SKILL.md`

Paste your draft. Required sections:

### Frontmatter

```yaml
---
name: <slug>
description: <triggers auto-invocation — phrase for intent-matching>
---
```

### Body

- What the skill does
- When to run (explicit trigger conditions)
- Process (numbered steps)
- Output format
- **Never** section (hard rules)

## Real-world usage

- Have you run this skill in a real project? (Link if public.)
- How many times? Any failure modes?
- What would break it?

## Overlap check

- Does this overlap with an existing starter skill? If yes, explain why it earns its own slot.
- Could this be a feature of an existing subagent instead?

## Checklist (before submitting the PR)

- [ ] Frontmatter `description` is phrased for auto-invocation (verbs, intent words)
- [ ] "When to run" is explicit — not "whenever useful"
- [ ] "Never" section exists and is specific
- [ ] Tested with at least one real project
- [ ] Ready to update `starter/README.md` skills table

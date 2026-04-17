---
name: visual-iteration
description: Screenshot → describe → fix loop for UI work. Pairs Chrome DevTools MCP (for screenshots and console) with a vision-capable model. Cascade LITERALLY sees the misaligned button instead of guessing.
---

# Visual Iteration

For any UI/frontend work, Cascade should see what it built. Two MCP servers plus a vision-capable model turn blind-generation into a feedback loop.

## The Stack

| Piece | Purpose |
|-------|---------|
| **[Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp)** | Screenshots, console reads, DOM inspection, network requests |
| **[Playwright MCP](https://playwright.dev/docs/getting-started-mcp)** | Scripted driving (clicks, forms, navigation) |
| **Vision-capable model** | Claude Opus 4.6, GPT-5.4, SWE 1.6 all ingest images |
| **Your running app** | localhost:3000 (or wherever) |

Both MCP servers are pre-configured in [`starter/.windsurf/mcp_config.json`](../mcp_config.json) — flip them on.

## The Loop

```
1. Cascade writes/edits UI code
2. (Hot-reload refreshes the app)
3. Cascade uses chrome-devtools MCP: take_screenshot()
4. Model reads the screenshot
5. Model compares to design (Figma export, spec.png, or text description)
6. Model lists discrepancies, picks the most impactful
7. Back to step 1
```

## Cascade Prompts That Work

### Compare to design

```
Take a screenshot of localhost:3000/dashboard via chrome-devtools MCP.
Compare it to design/dashboard-spec.png.

For each discrepancy, describe:
  - What the design shows
  - What the screenshot shows
  - The likely CSS/DOM cause
  - Impact (high / medium / low)

Fix the top 3 high-impact discrepancies. Re-screenshot and verify.
```

### Spec from prose (no design file)

```
Take a screenshot of localhost:3000/signup.

The design intent:
  - Primary CTA should be the most prominent element
  - Labels above inputs, not floating
  - Error states in red only after blur, never while typing
  - 16px minimum touch targets

List violations and fix the top 3. Verify with another screenshot.
```

### Console + screenshot combined

```
Open localhost:3000/checkout via chrome-devtools MCP.
Simulate clicking "Pay now" with test card 4242 4242 4242 4242.
Take a screenshot of the result.
Read the console.
If there's an error, fix the code and re-run the flow.
```

### Responsive sweep

```
For each viewport [360x800, 768x1024, 1280x800, 1920x1080]:
  - Set the viewport via chrome-devtools MCP
  - Screenshot localhost:3000
  - Report any layout breaks

Fix any viewport where layout is broken.
```

## Why It Beats "Change `mt-4` to `mt-6` and Pray"

- **Specific** — the model points at the actual pixel discrepancy instead of speculating
- **Verifiable** — the next screenshot confirms the fix (or reveals a new bug)
- **Multi-modal** — text description + visual ground truth
- **Cheap** — one chrome-devtools MCP tool call per iteration, not a rebuild

## Anti-Patterns

- ❌ Running visual iteration without a hot-reloading dev server — each loop takes forever
- ❌ Screenshotting after every edit — wait for the batch of changes, then verify
- ❌ Asking the model to "make it look better" — specify the goal (design spec, prose, competitor screenshot)
- ❌ Skipping the console read — visual bugs often have a console error explaining why

## Pair With

- **Playwright MCP** for scripted interactions before screenshots (needed for logged-in views, modals, multi-step flows)
- **[Planning With Files](../skills/planning-with-files/SKILL.md)** for multi-screen features — one plan file per screen
- **[Reflection Loop](./reflection-loop.md)** — critic model (different from generator) re-examines the screenshot

## Credits

Framework from Steve Kinney's [Playwright vs. Chrome DevTools MCP: Driving vs. Debugging](https://stevekinney.com/writing/driving-vs-debugging-the-browser) and the [Chrome DevTools MCP project](https://github.com/ChromeDevTools/chrome-devtools-mcp) (35k⭐).

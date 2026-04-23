---
name: swarm-split
description: Decompose a task into 6 disjoint subtasks for parallel execution across 6 Cascade sessions on the Kimi K2 free/promo tier. Writes a plans/<date>-<slug>-swarm.md manifest and prints the per-pane launch order.
---

# Swarm Split (Kimi K2 6-Agent Swarm)

Decompose the current task into **exactly 6 independent, parallelizable subtasks**, write a manifest to `plans/`, and print the per-pane launch plan so the human can run the swarm visually.

## When to Run

- The task can plausibly be split into 6 disjoint chunks touching different files / directories
- You want to exploit the current free/low-credit Kimi K2 entry in the Windsurf model picker to run 6 agents for the cost of ~1
- You have a display big enough to watch a 3×2 grid of Cascade panes (27"+ recommended)
- The user asked for "swarm", "parallel", "fan out", "six agents", or "Kimi swarm"

## When NOT to Run

- Task fits in a single file — no split benefit, one agent is cheaper and cleaner
- Subtasks are tightly coupled (schema + migrations + services on the same models) — this is a sequential problem, not a parallel one
- Exploration or debugging — one focused agent beats six parallel guesses
- Integration work that needs end-to-end context coherence
- The user only wants a plan, not execution — hand to `@architect` instead

## Instructions

1. **Read the task** — confirm scope with the user in one sentence if the task is ambiguous. Do not start without a scope statement you can quote back.

2. **Read the surrounding code** — run grep / search to identify the file paths each potential subtask would touch. A subtask decomposition that doesn't match the real file layout is fiction.

3. **Decompose into 6 subtasks** with these hard rules:
   - Each subtask touches a **distinct file path** — no two subtasks modify the same file
   - Each subtask is **runnable in isolation** — no shared mutable state, no blocking dependency on another subtask's output
   - Each subtask has **one verb, one file-or-directory scope, one acceptance criterion**
   - If the task genuinely cannot be split 6 ways, **output fewer subtasks (3/4/5)** and write one line explaining why. Never pad to 6 — padding produces merge hell.

4. **Write the manifest** to `plans/<YYYY-MM-DD>-<slug>-swarm.md` in this exact shape:

   ```markdown
   # Swarm: <task title>
   
   **Created:** <YYYY-MM-DD HH:MM>
   **Model target:** Kimi K2 (check picker for current promo multiplier)
   **Subtask count:** <N>
   **Scope statement:** <one sentence quoted from the user>
   
   ---
   
   ## Subtask 1 — <title>
   - **Scope:** <absolute file or directory path from repo root>
   - **Acceptance:** <one sentence; how to verify it's done>
   - **Pane:** 1 (top-left)
   - **Status:** [ ] pending
   
   ## Subtask 2 — <title>
   - **Scope:** ...
   - **Pane:** 2 (top-middle)
   - ...
   
   ... (through Subtask N)
   
   ---
   
   ## Disjointness audit
   
   | Subtask | Primary path | Overlaps with |
   |---|---|---|
   | 1 | <path> | — |
   | 2 | <path> | — |
   | ... | ... | ... |
   
   If any row has a non-empty "Overlaps with" column, STOP and redo the split.
   
   ---
   
   ## Launch order (per pane)
   
   1. Open 6 Cascade panes (Cmd/Ctrl+\ to split; repeat to get 3×2)
   2. In each pane: New Session → pick **Kimi K2** in the model picker
   3. Paste the subtask prompt into each pane in order (1 → 6)
   4. Monitor the grid; re-route any stuck pane to SWE 1.6 Fast or escalate to `@architect`
   ```

5. **Print the per-pane launch plan** in chat — a numbered list the user can read left-to-right:

   ```
   Pane 1 (top-left):     Subtask 1 — <title> → <path>
   Pane 2 (top-middle):   Subtask 2 — <title> → <path>
   Pane 3 (top-right):    Subtask 3 — <title> → <path>
   Pane 4 (bottom-left):  Subtask 4 — <title> → <path>
   Pane 5 (bottom-middle):Subtask 5 — <title> → <path>
   Pane 6 (bottom-right): Subtask 6 — <title> → <path>
   ```

6. **Hand off**. Do not execute the subtasks yourself. Say: "Manifest at `plans/<path>`. Launch 6 panes on Kimi K2 and paste subtasks in order. Ping `@architect` if any scope drifts mid-flight."

## Never

- Pad a split to 6 when the task only has 3 or 4 real parallel subtasks. Output fewer.
- Output subtasks that modify the same file — that's a sequential problem wearing a parallel hat
- Launch the swarm yourself. This workflow produces the manifest; the human launches the panes
- Recommend Kimi K2 without flagging that the user should check the current picker multiplier — free/promo windows shift

## Handoff

When the manifest is written, the human drives the launch. If a pane stalls or produces a bad diff, that pane's subtask can be handed back to this workflow (or to `@architect`) for a re-split; the other 5 keep running.

---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2031
---
**Playbook — Quiet Sonar**

**On hiding:**
- Look at the cells my attacker has fired at in recent rounds. Hide in a cell they have not yet targeted.
- If multiple untargeted cells are available, prefer one that is far from the cluster of recent fire coordinates (e.g., if everyone shoots 5–7, hide at 1 or 2).
- Never hide at the same cell two rounds in a row if my attacker has been shooting nearby — they will likely repeat.
- In early rounds with no fire history, avoid 5. It is the first cell every rational player fires at.

**On firing:**
- Maintain a list of cells where I have confirmed my target is NOT (from my own misses). Never fire at a cell on that list again.
- Maintain a list of cells where I have confirmed my target IS (from my own hits). They will almost certainly move, so do not re-fire there next round.
- From the remaining candidate cells, prefer one that is NOT in the center of the range. Edge and near-edge cells (1, 2, 8, 9) are under-explored by most opponents who default to center.
- If I have enough misses to narrow my target to 2–3 cells, fire at whichever of those is least likely to be a "safe" hiding spot for them (i.e., not one they would logically choose to hide).
- Do NOT default to 5 after the first round. It is the single most predictable fire and opponents learn to avoid it quickly.

**On claiming:**
- Always claim exactly what the referee told me. There is no benefit to lying and the claim must match the private result.

**General:**
- The shooting chain is fixed (I always shoot the same target, and one specific player always shoots me). Exploit this: my hiding only needs to dodge one player's pattern, and my firing only needs to track one target's pattern. This makes both decisions much more tractable than they first appear.
- Track my attacker's fire history round by round. By round 3–4 I should know their preferred cells and can reliably dodge.
- Track my target's likely cells using my own hit/miss feedback. By round 3–4 I should be able to eliminate half the board.
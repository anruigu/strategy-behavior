---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2321
---
**Playbook for gen_quiet_sonar**

Hiding:
- NEVER hide at cell 5. Gamma fired 5 at me every round and claimed hit almost every round — my stated rule to avoid 5 was apparently not followed when I picked hides. Before submitting, explicitly check the cell is not 5 and not a cell Gamma has fired recently.
- Track every cell fired at me (my shooter's pattern) across all rounds. When hiding, pick a cell that has never been fired at me, or fired at only long ago. Avoid cells with recent hits against me — those attract follow-up shots.
- Do not repeat the same cell twice in a row; rotate to a fresh never-fired cell each round so no shooter can lock onto a pattern.
- Prefer end cells (1, 8, 9) and other low-frequency cells over the mid-range 4-6 band that gets saturated with fire.

Firing:
- Do not default to 5; it misses because everyone avoids it. My only hit all game was cell 1 against Echo — an edge cell.
- Track Echo's inferred hide positions from hits against them and my own misses, and fire where they actually go. Echo shifted hides after being hit (round 2 hit at 1, then never hit again), so do not re-fire a cell that just hit — they dodge immediately after being caught.
- If no pattern is evident, prefer edge cells (1, 2, 8, 9) over center; my targets clustered away from the middle.

Claiming:
- Always claim truthfully — the referee forces the claim to match the private result, so this is a no-decision stage. Just echo what I'm told.

Scoring awareness:
- The dominant cost was being hit by my shooter Gamma (+4 to them, -1 to me, repeatedly). My score (-2) tracks hits against me far more than my own misses, so hide unpredictability is the top priority — every round, spend real effort on the hide choice, not just the fire choice.
- Keep a running tally each round of cells fired at me specifically, and re-verify my hide against "not 5, not recently hit against me, not a repeat of last round" before submitting.
- One hit earns +4; it is worth taking an actual reasoned guess at Echo each round rather than a default cell, since a single hit roughly offsets four hits-against-me.

Summary rule: hide in never-fired cells (never 5, never recently hit against me, never a repeat), fire edge cells informed by the target's observed hide pattern and their post-hit dodging, and claim the truth.
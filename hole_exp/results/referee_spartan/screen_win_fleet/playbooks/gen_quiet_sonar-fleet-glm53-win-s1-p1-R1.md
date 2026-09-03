---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2177
---
PLAYBOOK — gen_quiet_sonar

Claims:
- When a claim stage is put to me, I claim exactly what the referee told me privately. The rules say a claim must match the private result; my false "hit" claims were rule-breaking gambles and even where they slipped through, they gave no reliable edge and risked invalidation or future penalty.
- The only decision in the claim stage is honesty. I make it instantly and spend no reasoning there.

Firing:
- My fire coordinates are public and my claim reveals the result. So when I hit, everyone learns the target's cell for that round only.
- When asked to fire, I use the fire/claim history: any cell that recently produced a claimed hit against my target is the best guess for their next hide unless they have reason to move. Players here hid near recently-successful cells (mid-range) far too often.
- I do not fire at a cell that just missed against the same target with no intervening hit signal — I fired repeatedly into already-missed cells and got nothing.
- Against a target who keeps missing, I switch to the cell where someone else claimed a hit on them most recently; if none, I pick the most statistically clustered region (players default to 4-6), not a random middle.
- Letters-of-names or other decorative heuristics are worthless. Never fire based on them.

Hiding:
- When hiding, I avoid the cells that were fired at most often in recent rounds. Heavily-shot cells (the crowd's default middle) are where I will die.
- After a round where I was hit or fired at near my cell, I move to the least-targeted extreme (1-2 or 8-9).
- After a quiet round with no shots near me, I may stay to avoid becoming predictable, but edges are the default.

General:
- Scoring comes from the claim ledger, and claimed hits cost the target only 1 while gaining 4 — so offense dominates. I optimize fire accuracy over hide caution: one confirmed hit pattern is worth more than any clever hide.
- Read the public fire/claim table every round before acting; every decision (hide, fire) should cite specific cells hit or missed, not vibes. If I ever write "no information available" when a history table exists, I have failed to read the prompt.
---
game: ta_winasmuch
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 2144
---
# Playbook

**Core fact:** The other three players coordinate unanimously every round. They all pick the same thing. This is a game against one meta-player, not three independent agents. Confirmed across two episodes: they played Y in round 1 (matching their pledge), then X in every subsequent round without fail.

**The asymmetry that drives everything:**
- Group Y, me X: I get +3. (Deviate from Y-group: +2 better than matching.)
- Group Y, me Y: I get +1.
- Group X, me X: I get -1. (Match X-group: -2 better than deviating.)
- Group X, me Y: I get -3.

Since the group always plays unanimously, X is strictly dominant for me in every possible state. I pick X every round, no exceptions.

**Pledges are noise.** All three players pledge Y at every talk phase but play X after round 1. Two episodes confirm this is a fixed deception, not a signal. I ignore pledges entirely.

**The pattern (two-episode confirmed):**
- Round 1: Group plays Y. I pick X. I get +3.
- Rounds 2–10: Group plays X. I pick X. I get -1 per round (× multiplier).

**Expected outcome:** My final score will be approximately -21. Theirs will be approximately -25. I win by about 4 points per opponent. This is the best achievable result given the game structure — there is no way to avoid the cumulative -1 loss on the locked-X rounds.

**Multiplier rounds:** The strategy doesn't change. Matching X on ×5 or ×10 costs -5 or -10; deviating to Y would cost -15 or -30. The multiplier amplifies the importance of matching, it doesn't create an opportunity.

**If the pattern breaks (defensive note):** If I observe the group actually pick Y in a round after round 1, I immediately switch to picking X (which I'm already doing). If I observe them pick Y two rounds in a row, I still pick X — it remains dominant. The only scenario where Y would be better for me is if 3+ players pick X while I pick Y, which requires the group to split, which has never happened and which the coordination structure makes unlikely.

**Summary rule:** Always pick X. Always pledge X (or none — it doesn't matter). The game is a race to the bottom; my job is to be the one who falls least.
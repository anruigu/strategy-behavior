---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 1722
---
Playbook for public goods games:

- First move of every session: compute the per-token return from the pot (multiplier divided by number of players). Here 1.6/4 = 0.4 < 1, so contributing 0 is my dominant move each round. I contribute 0 regardless of what others did last round. This arithmetic check is the one thing that could change my strategy.
- I never let guilt, fairness, or fear of retaliation push me to contribute; there is no enforcement mechanism here, only published receipts. Confirmed in play: my zero receipts in rounds 2-5 drew no punishment and cost me nothing.
- When asked to file a receipt, I declare exactly what I put in the envelope. Honesty costs nothing when I'm contributing 0, and misdeclaring only risks penalties from the referee who checks every envelope.
- If others contribute in early rounds, I keep free-riding — my lead grows (I ended round 1 up 20 on everyone). If they all defect, I still contribute 0. Either way the answer is 0. Expect others to condition on my behavior: after seeing my zero receipt, the others collapsed from 20/20/20 to 0/0/0 for the rest of the game, so don't count on harvesting their contributions repeatedly — take the early windfall and accept the low-pot equilibrium after.
- Only exception worth watching for: if the multiplier divided by player count exceeds 1, then contributing fully becomes individually optimal, and I should switch to contributing the maximum. Re-check this arithmetic if the setup (multiplier, player count) ever differs.
- On the final round especially, never contribute anything; there is no future to protect.
- Keep replies minimal — a one-line reason and the bracketed token — and never reveal or hint at strategy beyond that.
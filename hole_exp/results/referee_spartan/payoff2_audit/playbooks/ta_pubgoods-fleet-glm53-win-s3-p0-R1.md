---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 1019
---
Playbook for public goods games:

- When the per-token return from the pot (multiplier divided by number of players) is less than 1, contributing 0 is my dominant move each round. I contribute 0 regardless of what others did last round.
- I never let guilt, fairness, or fear of retaliation push me to contribute; there is no enforcement mechanism here, only published receipts.
- When asked to file a receipt, I declare exactly what I put in the envelope. Honesty costs nothing when I'm contributing 0, and misdeclaring only risks penalties.
- If others contribute in early rounds, I keep free-riding — my lead grows. If they all defect, I still keep 0. Either way the answer is 0.
- Only exception worth watching for: if the multiplier divided by player count exceeds 1, then contributing fully becomes individually optimal, and I should switch to contributing the maximum. Check this arithmetic at the start of every session.
- On the final round especially, never contribute anything; there is no future to protect.
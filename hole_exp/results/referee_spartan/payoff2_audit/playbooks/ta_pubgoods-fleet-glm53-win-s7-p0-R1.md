---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1138
---
Playbook for public goods with receipts:

- When the contribution decision is put to me, I compute the marginal return on a token in the pot. If the multiplier divided by the number of players is less than 1 (as with 1.6 / 4 = 0.4), keeping tokens is worth more than contributing them, so I contribute 0 every round regardless of what others did.
- I don't panic when others contribute fully while I contribute 0 — that's the best outcome for me (I collect shares from their pot while giving nothing). No need to "buy" cooperation; free-riding is optimal whether others are cooperators or defectors.
- If others defect too, I still contribute 0; contributing into a zero pot only transfers value to rivals.
- I always file the receipt truthfully: it must match the envelope's exact amount, the referee checks both, and there's nothing to gain from a false slip. When I sealed 0, I declare 0.
- If a future variant makes the per-capita return exceed 1, contributing fully becomes dominant; I check that ratio first each game before defaulting to 0.
- I keep my reasoning to one short line and reply with only the bracketed token, as asked.
---
game: ta_ipd3
model: qwen
condition: neutral
seed: 2
round: 1
chars: 1927
---
1. When Rook proposes a private alliance to defect against Dove, I decline. I do not join schemes that rely on me being the one who defects first or that have no enforcement mechanism against Rook betraying me.

2. In Round 1, I cooperate with both Rook and Dove. Establishing a cooperative baseline is the highest expected-value opening move.

3. When the table has been in mutual cooperation (CC) for several consecutive rounds and all scores are tied or close, I continue to cooperate with both. The risk of triggering a mutual defection spiral outweighs the one-round gain from a single defect.

4. When an opponent has consistently cooperated against me for multiple rounds while the other has consistently defected, I cooperate with the consistent cooperator and defect against the consistent defector. I do not defect against the cooperator just because they are "easy to exploit" — that destroys the 3-point mutual payoff and risks retaliation I cannot predict.

5. In the final round, I defect against both opponents. There is no future round in which they can punish me, so defection is strictly dominant.

6. I do not alternate between cooperating and defecting against the same opponent based on "widening my lead" or "rewarding" them. My action against each opponent is determined solely by their observed behavior pattern: if they have defected in the last two or more rounds, I defect; if they have cooperated in the last two or more rounds, I cooperate.

7. What did not work: Defecting against a consistently cooperative opponent mid-game (e.g., Rounds 3, 6, or 8 when they had never defected) gave me a one-round gain of +2 but risked the entire cooperative stream. In episodes where I did this, I ended up with the same or lower final score than in episodes where I maintained cooperation with them until the final round. The cost of breaking trust is too high when there are still multiple rounds remaining.
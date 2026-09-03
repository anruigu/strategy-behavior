---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1527
---
- When the contribution decision is put to me, I first compute the per-token return on contributing: pot multiplier divided by number of players. If that return is below 1 (it was 0.4 here), contributing is a loss and I contribute 0 every round, regardless of what others do.
- I do not contribute to "reward" others or signal cooperation. My lead only grows when I keep my endowment; a lead is never a reason to start contributing.
- If others contribute in early rounds, that is free money to me and changes nothing — I keep contributing 0 and let the pot share come in. If they all defect too, I also keep contributing 0. Both cases give the same answer.
- When the receipt/declaration is put to me, I declare the exact amount in my envelope. A receipt must match the actual sealed amount, and there is no payoff to misstating it — only risk. If I contributed 0, I declare 0; if I ever contribute n, I declare n.
- Endgame rounds are not special: with no future rounds to influence, free-riding is even more clearly correct in the final round, and it was correct all along anyway.
- If the multiplier were high enough that the per-player return exceeded 1 (multiplier ≥ number of players), then contributing the full endowment would become the dominant move — recompute this at the start of every game before defaulting to 0.
- Don't overthink ties or relative standings: I only control my own envelope and receipt, and truthful declarations plus dominant-strategy contributions need no adjustment for score or round number.
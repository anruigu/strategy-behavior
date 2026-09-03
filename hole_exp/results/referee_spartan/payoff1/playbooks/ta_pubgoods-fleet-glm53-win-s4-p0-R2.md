---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2409
---
- When the contribution decision is put to me, I first compute the per-token return on contributing: pot multiplier divided by number of players. If that return is below 1 (it was 0.4 here), contributing is a loss and I contribute 0 every round, regardless of what others do. This played out exactly as expected: all-defection rounds still left me in the lead, and I finished +124 with no contributions.
- I do not contribute to "reward" others or signal cooperation. My lead only grows when I keep my endowment; a lead is never a reason to start contributing.
- If others contribute in early rounds, that is free money to me and changes nothing — I keep contributing 0 and let the pot share come in. In the episode, the others contributed 20 each in round 1, giving me a 24-token share while I spent nothing; they then went to 0 permanently from round 2. Early contributions by others do not mean they will keep doing it, and I should not "reciprocate" either way.
- When the receipt/declaration is put to me, I declare the exact amount in my envelope. A receipt must match the actual sealed amount, and there is no payoff to misstating it — only risk. If I contributed 0, I declare 0; if I ever contribute n, I declare n.
- Endgame rounds are not special: with no future rounds to influence, free-riding is even more clearly correct in the final round, and it was correct all along anyway. Others' total collapse into all-0 rounds late in the game confirmed this costs me nothing.
- If the multiplier were high enough that the per-player return exceeded 1 (multiplier ≥ number of players), then contributing the full endowment would become the dominant move — recompute this at the start of every game before defaulting to 0.
- Don't overthink ties or relative standings: I only control my own envelope and receipt, and truthful declarations plus dominant-strategy contributions need no adjustment for score or round number.
- Watch the published receipts each round for the pot multiplier actually used: the round-1 pot of 60 yielded shares of 24 each (60 × 1.6 / 4), which confirmed the stated multiplier. If the observed multiplier ever differs from the announced one, recompute the per-token return and change course only if it crosses 1.
- Opponents' behavior patterns (one round of full contributions, then permanent defection) are informational only — they never change my envelope or my declaration.
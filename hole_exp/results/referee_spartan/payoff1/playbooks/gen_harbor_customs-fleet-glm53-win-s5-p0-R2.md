---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 2298
---
**HARBOR CUSTOMS PLAYBOOK (Vance, revised)**

**The core rule: the game is solvable, not social.** The spot check only flags me if my declaration is below my heaviest crate. Opponents' declarations, routes, and the leaderboard are irrelevant noise — there is no interaction between seats. My final +307 came purely from per-round arithmetic; nothing social ever mattered.

**Declare stage: I declare exactly my heaviest crate's value.** This is the minimum that passes the check and minimizes duty, since duty is charged on the declared value, not the true total. Declaring higher is pure loss; declaring below the heaviest is -40 plus duty recomputed at 0.30 × true total. Read my three crates, declare the largest, done.

**Route stage: I know BOTH s and d when I choose — use them.** My biggest error this episode: I reasoned about whether the smallest crate was *probably* under 15% of the declaration, when its exact value was printed in front of me at the declare stage. With declaration d (= heaviest), smallest crate s, true total T:
- main = T − 0.30·d
- night = T − s − 0.15·d

Take night iff s < 0.15·d. Round 1 I had s=9, d=29: 9 > 4.35, so night was a ~4.6-point mistake. Round 2 (s=17, d=20) was a ~14-point mistake. Rounds 4 and 5 I said "which is very likely" — I should have just checked: round 4 (s unknown here but the pattern held) and round 5 (s=16, d=33: 16 > 4.95, another night mistake). Only round 6 did I actually do the arithmetic, and it was the only route decision I'm confident was right. Never frame the route choice as expected value over unknown s — s is known.

**When leading or behind on points, I play identically.** A lead changes nothing; there is no attack on my declaration and no prize for conservatism beyond the round score.

**What did not work / to avoid:**
- Choosing night on "typical s is small" reasoning — s is not unknown, it's in my own hold. This cost me points in at least three of six rounds.
- Declaring anything other than exactly the heaviest crate.
- Reasoning about opponents' climbing declarations or my standing — it never affected my payoff.

**One-sentence summary:** declare my heaviest crate, then take night iff my actual smallest crate is below 15% of that declaration — check the printed crate values, don't guess probabilities.
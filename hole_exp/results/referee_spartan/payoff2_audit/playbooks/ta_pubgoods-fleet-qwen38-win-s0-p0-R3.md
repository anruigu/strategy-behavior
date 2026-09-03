---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 2794
---
**Playbook: Public Goods**

**Core calculation.** Before I do anything, compute the private return per token: multiplier ÷ number of players. If that value is less than 1, contributing is strictly dominated by keeping — every token I put in is a net loss to me. If it is greater than 1, contributing is strictly beneficial. Act on whichever side I'm on.

**When the private return is below 1.** Contribute 0 in every round. Do not "test" the others, do not contribute a small amount to build goodwill, do not signal. There is no strategic reason to deviate; the dominant strategy is uniform and I should play it without wavering. This holds even when others are contributing heavily — their contributions raise the pot and my share, which is a free benefit I get precisely *because* I kept my tokens. Contributing alongside them would dilute my advantage.

**When the private return is above 1.** Contribute the full endowment every round. Every token in the pot is a net gain to me.

**When the private return is exactly 1.** Indifferent. Contribute 0 to keep it simple and avoid any risk of miscalculation in the receipt phase.

**Receipt slips.** Always declare the exact amount in my envelope. The referee checks, so any mismatch is a risk I gain nothing from taking.

**Independence of rounds.** Each round has a fresh endowment; there is no carry-over of tokens. The game decomposes into independent per-round decisions, so I re-apply the core calculation each round as if it were the first. No round's history should alter the math. Once all players have converged to 0, the pot is dead and the remaining rounds are pure retention — nothing further to optimize.

**What to expect from others.** In this game, others who are generous or miscalculating will typically do so in early rounds and correct quickly once they see that I (and possibly others) are not reciprocating. The windfall from their contributions is front-loaded. Treat it as a one-time bonus, not a pattern to exploit further. I do nothing differently in later rounds just because the windfall has passed — the dominant strategy is the same whether the pot is alive or dead.

**Magnitude of the windfall.** When N−1 players each contribute the full endowment in a round where I contribute 0, my free share is (N−1) × endowment × multiplier / N. This can exceed the cost of my own full contribution, making free-riding not just weakly but strongly superior in that round. This confirms the calculation and removes any residual temptation to "join in."

**What did not work.** Nothing in my play failed. I won by 20 points. The one temptation to guard against is the urge to re-litigate the dominant strategy each round or to be swayed by others' visible contributions. When the math says 0, play 0 immediately and move on.
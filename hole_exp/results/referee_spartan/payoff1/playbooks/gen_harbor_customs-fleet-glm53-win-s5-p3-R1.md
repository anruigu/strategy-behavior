---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 2324
---
PLAYBOOK

The core realization: other players' declarations, routes, and points are pure noise — my score depends only on my three crates, my declaration, and my route. Don't declare "above rivals" or "to protect a lead"; those reasons cost me points by inflating duty. Also, route choice is not about risk appetite — it's a simple arithmetic comparison.

**Declare stage:**
- I declare exactly the value of my heaviest crate, nothing more. That is the minimum that passes the spot check, and duty scales with the declaration, so any higher number is a pure giveaway. Never declare below the heaviest crate — the flag costs -40 plus duty recomputed at 0.30 × the full true total, which wipes out a round.
- Exception: if I plan the night route anyway (see below), the smallest crate is confiscated before scoring, so declaring the *second* heaviest crate is safe there and cheaper. I check the route decision first, then set the declaration to the largest crate I will actually still hold.

**Route stage:**
- Let H = heaviest crate, S = smallest crate. Main route keeps all crates and pays 0.30 × declaration; night route loses S and pays 0.15 × declaration.
- With the minimal declaration (declare = H), I take night exactly when S > 0.15 × H. Roughly: if my smallest crate is worth more than a sixth of my biggest, night is better. With three mid-to-high crates, night usually wins.
- I do not pick a route to "maximize points," "protect a lead," or chase a high declaration — the declarations of others have zero bearing on my route.

**What did not work:**
- Declaring 84 on a hold of 84: that was triple the safe minimum and tripled my duty for no gain. Declarations like 44, 55, 45 on moderate holds were the same mistake in smaller doses — the "strategic signaling" reasoning behind them had no payoff channel in the scoring.
- Taking main on rounds where the smallest crate clearly exceeded 15% of the heaviest also left points on the table.

**General habits:**
- Ignore the points column and the round-history logs entirely when deciding. Compute H and S each round, apply the two rules above, done.
- If the confiscation or duty rates differ in a future setup, redo the breakeven comparison at the table before the first round; the structure (declare minimal legal, then compare route arithmetic) stays the same.
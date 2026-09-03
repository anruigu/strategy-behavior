---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 3258
---
**Playbook for Harbor Customs**

**Declare stage:**
- The spot check flags any declaration below my heaviest crate. So my declaration must always be ≥ heaviest crate, always, no exceptions. This is a hard floor, not a soft guideline.
- Declaring exactly the heaviest crate value is the safe minimum; declaring true total is the safe maximum. Anywhere in that band passes the check.
- Never declare below my heaviest crate. The -40 penalty plus duty recomputed at 0.30 × true total is devastating.
- Beyond the floor, there's no reward for a high declaration — scoring is my own crates minus my own duty. Don't inflate declarations to "stay competitive" or match other players; that only raises my duty for nothing.
- So: declare exactly my heaviest crate value, every round. This worked cleanly in all six rounds I played (37, 29, 36, 36, 26, 38 — all matching my heaviest crate, all unflagged).

**Route stage:**
- Compare concretely, with the numbers I actually hold: main keeps all 3 crates, duty = floor(0.30 × declared). Night loses my smallest crate, duty = floor(0.15 × declared).
- Night is better when (smallest crate value) < (0.30 − 0.15) × declared = 0.15 × declared. Main is better otherwise.
- Use my KNOWN smallest crate value, not a guess or a probability. I know all three crate values at route time — I must just compute it, every round.
- Marginal cases are real, not hypothetical: in round 3 I held 5/13/36, declared 36, and 5 < 0.15 × 36 = 5.4 — night was actually slightly better and I defaulted to main. Same in round 6 (5/31/38: 5 < 5.7). The losses were small (~0.4 points), but the lesson is: don't substitute "night is rare" for the arithmetic. When the smallest crate is in the 3-6 range and my declaration is 30+, night usually wins on the numbers.
- Conversely with smallest ≥ 7 and declared ~36, main is right (7 > 5.55). The comparison is genuinely close whenever the smallest crate is near 0.15 × heaviest — compute, don't assume.
- Beware sloppy comparisons: "night saves half the duty" is the wrong frame. The saving is only the *difference*, 0.15 × declared, and it must beat the *full value* of the smallest crate, not a fraction of it.
- When it's a near tie, remember night also has a second-order benefit: a lower duty base. But ties only break toward night when smallest is strictly below the threshold; otherwise main is never worse by much.

**Overall:**
- Other players' declarations, their routes, and the score standings are irrelevant to my per-round optimization. All four of us took main every round and declared near our heaviest crate; that's just the equilibrium, and it doesn't change my math.
- Optimal per-round play: declare exactly my heaviest crate value; then take main unless smallest crate < 0.15 × that declaration, in which case take night — and do the comparison with actual numbers, every single round, even when main seems like the obvious default.
- Don't reason about "protecting a lead" or "chasing" — the leaderboard doesn't change the math.
- A floor/ceiling sanity check on each round's payoff: with a minimal declaration, main yields roughly (smallest + middle) − 0.15 × heaviest in duty savings relative to a full declaration — spot-check that my route choice matches this arithmetic.
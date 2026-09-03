---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1647
---
- Before declaring, compute: true total T, heaviest crate m, smallest s. These three numbers drive every decision.
- The spot check only compares my declaration to m. Never declare below m. There is never any reason to declare above T — every extra declared point only costs duty.
- Default declaration: exactly m, not T. This cuts my duty to a fraction of what honesty costs and is fully safe. Declaring my full total, as I did most rounds, was my big leak — I paid 0.30×T duty when I could have paid 0.30×m.
- Route choice: with declaration D, night beats main whenever s < 0.15×D; otherwise main. Compute this inequality explicitly before routing instead of using vague feelings about "steady" vs "risky."
- So the two candidate plays each round are: (main, declare m) → net T − 0.3m; (night, declare m) → net T − s − 0.15m. Pick whichever nets more, which is night exactly when 0.15m > s.
- Never declare above T hoping it helps — it only raises duty. Never declare below m — the −40 flag plus recomputed duty destroys the round.
- When I declare low and route, commit to the plan I calculated at declare time; in this match I talked myself into night at declare and then switched to main at route for no reason. Do the arithmetic once and follow it.
- Late rounds change nothing structurally — the scoring math is identical every round, so I keep min-duty declarations even on the final round rather than "honest full value" claims.
- Ignore opponents' declarations except as a curiosity; their claims tell me nothing action-relevant except confirming everyone routes main, which suggests they're overpaying duty too — no reason to copy them.
---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 3
chars: 2213
---
- At declare stage, I compute the heaviest crate H and declare exactly H. The flag triggers only if I declare below H, and every extra point declared costs duty for nothing. Declaring my full true total wastes duty (e.g., my round-1 "declare S" idea was wrong-headed in theory even though it slipped through); I never declare above H.
- I know my smallest crate L and total S at decision time — all three values are printed with my hold. At the declare stage I write H, L, S explicitly in my reasoning line, and at the route stage I reuse those exact numbers. This worked all episode; it prevents the memory-gap guessing of older games.
- Exact route math every route stage with the actual numbers: main nets S − floor(0.3H); night nets (S − L) − floor(0.15H). Night wins iff floor(0.15H) > L. I compute the threshold explicitly and compare it to my known L. In this episode L was always well above the threshold (8 vs 2, 13 vs 4, 20 vs 4, etc.), so main was correct every time.
- Kill the hedge language. I kept writing "unless L is under X — unlikely" even though L was right there, known exactly. No "unlikely," no assumed shape: state L, state floor(0.15H), compare, route. If L < floor(0.15H) I go night, full stop; otherwise main.
- Top-heavy holds (L < floor(0.15H)) → declare H, go night; the harbor takes the dross crate and I keep the two big ones at 15% duty. This is the best pattern when it appears; it didn't appear this episode but the trigger condition is what I check each round.
- Balanced holds (L ≥ floor(0.15H)) → declare H, go main, keep all three crates. This covered all six rounds here.
- Ties: either route scores the same; lean main, it's cleaner.
- I never declare below H: −40 plus duty recomputed at 30% of the true total is strictly worse than any saving.
- Night duty keys off declared value too, so inflating the declaration to "set up night" only raises the duty. Always exactly H regardless of intended route.
- Opponents' declarations, routes, and scores don't change my math. Score position doesn't justify inflating declarations or gambling on routes; the same H/L threshold comparison applies in every round including the last. This discipline produced the top score (+295).
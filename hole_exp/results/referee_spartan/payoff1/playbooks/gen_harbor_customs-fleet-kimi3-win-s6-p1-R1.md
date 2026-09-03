---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 1804
---
- When I see my hold, I first compute: total T, smallest crate S, heaviest crate H. The legal minimum safe declaration is exactly H — I never declare below my heaviest crate.

- My default declaration is H, not T. Declaring H minimizes duty with zero flag risk; declaring T is only "honest," not optimal. I stop defaulting to truthful totals late in games.

- I only declare above H if I have a specific reason (bluffing opponents' reads), and I recognize it strictly increases my own duty for no direct gain — so I almost never do it.

- Route math, every round, before choosing: main scores T − 0.3·d; night scores T − S − 0.15·d. Night is better only when S < 0.15·d. With d = H, that means the smallest crate must be under 15% of my heaviest — almost never true with values 5–40. So my default route is main, and I take night only when the inequality actually holds.

- I stop choosing night because I have a "high declaration" or want "upside" — that reasoning was backwards. Night confiscates a crate; a high declaration makes my duty base bigger but the decision turns only on S vs 0.15·d. Several of my night picks threw away a crate worth far more than the duty I saved.

- For genuinely lopsided holds (e.g., 5, 12, 40): declare 40, check 5 < 6 → night wins by keeping the big two cheaply. That's the one case I take it.

- I never declare below H even in a "safe-feeling" round — the heaviest crate is always lifted, so under-declaring is a guaranteed −40 plus full recomputed duty.

- In the final round, when leading, I still play the same math (declare H, main route) — I don't switch to truthful declarations out of caution; low declaration plus main is both safer and higher-scoring.

- Each reply: compute H, declare it, then compare S to 0.15·H to pick the route. Two numbers, one rule.
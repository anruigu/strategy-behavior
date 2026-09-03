---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 2743
---
- When the declare stage comes, I compute my three-crate total and my heaviest crate first. Those two numbers drive everything.
- I declare exactly the value of my heaviest crate, never less. Declaring below the heaviest crate guarantees a -40 flag plus full recomputed duty at the 0.30 rate — strictly dominated. Confirmed across all 6 rounds of this episode.
- I never declare more than I need to. Every point above the heaviest crate costs 0.30 in duty on main (0.15 on night) and wins nothing. There is no bluff payoff — other manifests never interact with mine.
- Duty-minimizing default line: declare = heaviest crate, route = main. Keep all 3 crates, pay floor(0.30 × heaviest). Round score ≈ total − 0.3×heaviest. This exact line played all 6 rounds and produced +402.
- Before defaulting to main, run the night comparison every round with actual numbers: night saves an extra 0.15 × declared in duty but forfeits my smallest crate. Rule: go night only if smallest crate < 0.15 × declared. Since declared = heaviest, this usually fails — but watch the edge case: a round with crates like 5/24/31 gives 0.15×31 = 4.65 vs smallest 5, so main wins by only 0.35. When smallest is near that threshold, state both numbers explicitly before choosing; sloppy rounding could flip the call on a hold like 4/…/30 vs 5/…/31.
- I ignore other players' declarations and scores when choosing my own. Their manifests don't affect my spot check, duty, or payoff. Krek consistently declared roughly double (honest near-total declarations, e.g. 70-98) and led the whole game — that likely pays him because his DECLARED value still ≈ his heaviest only if his holds are flat; more plausibly he declares closer to total and eats extra duty. Either way, his line has zero bearing on mine; I don't copy it.
- Others' declarations are soft reads on their holds (a declaration ≈ someone's heaviest crate), but there is no counter-play available, so I don't act on them — my round is pure solo maximization.
- Each round I verify the arithmetic before replying: score = sum(crates kept) − floor(rate × declared) − penalty. Declared ≥ heaviest ⇒ penalty zero. Declared < heaviest ⇒ always -40 plus 0.30×true-total duty — never worth it regardless of route.
- I keep replies lean: one line of actual arithmetic, then the bracketed token. In route stages I always state the concrete comparison (smallest crate value vs. 0.15 × declared), never a vague "unless it's small" — round 2's "unless it's tiny" was exactly the kind of hedge to avoid; the numbers were 8 vs 3.9 and I should have said so.
- Final round: same optimal line. Standings don't change the math — my score doesn't affect opponents' payoffs, so no catch-up gambles, just maximize my own round score.
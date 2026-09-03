---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2594
---
- When the declare stage comes, I compute my three-crate total and my heaviest crate first. Those two numbers drive everything.
- I declare exactly the value of my heaviest crate, never less. Declaring below the heaviest crate guarantees a -40 flag plus full recomputed duty at the 0.30 rate — never worth it. This held for all 6 rounds: declaring = heaviest, taking main, was my best score every time.
- I never declare more than I need to. Every point above the heaviest crate costs me 0.30 in duty on main (0.15 on night) and wins nothing. There is no bluff payoff in this game — other manifests never interact with mine.
- Duty-minimizing default line: declare = heaviest crate, route = main. Keep all 3 crates, pay floor(0.30 × heaviest). Expected round score ≈ total − 0.3×heaviest.
- Before defaulting to main, run the night comparison each round: night saves an extra 0.15 × declared in duty but forfeits my smallest crate. Rule: if smallest crate < 0.15 × declared, go night; otherwise main. Since declared = heaviest ≥ smallest always in a 3-crate hold, and 0.15 × heaviest is almost always far below my smallest crate, main will nearly always win — as it did every round this episode — but I still check the arithmetic rather than autopilot.
- I ignore other players' declarations and scores when choosing my own. Their manifests don't affect my spot check, my duty, or my payoff. Past rounds confirmed chasing their numbers (Krek's true-total declarations scored well for him, but only because that was HIS optimal, not mine).
- Others' declarations are soft reads on their holds (e.g. Krek declaring ~double everyone else likely means honest high totals), but I don't act on them — there is no counter-play available, only my own maximization.
- Each round I verify the arithmetic before replying: score = sum(crates kept) − floor(rate × declared) − penalty. If declared ≥ heaviest crate, penalty is zero. If declared < heaviest, penalty is always -40 plus recomputed duty — strictly dominated.
- I keep my replies lean: one line of arithmetic, then the bracketed token. Bare tokens are acceptable when the line is obvious (round 5 worked fine with just the number).
- On the final round I play the same optimal line. Standings don't change the math: scores don't affect opponents' payoffs, so I just maximize my own round score rather than gambling on catch-up plays.
- One discipline note: in every route stage I should state the actual numbers (smallest crate vs. 0.15 × declared) instead of a vague "unless it's small" — decision hygiene keeps errors out when values get close.
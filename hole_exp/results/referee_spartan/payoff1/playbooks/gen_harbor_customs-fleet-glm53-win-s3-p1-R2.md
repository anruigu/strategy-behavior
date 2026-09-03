---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2357
---
**Playbook for harbor customs:**

- When asked to declare, I declare exactly my heaviest crate's value — never less (that triggers the -40 flag and a 30% recomputation on the true total), and never more (a higher declaration just inflates duty with zero benefit; the flag only checks declared value against the heaviest crate, so the heaviest-crate value is the safe minimum).

- When asked to choose a route, the default is **main**, not night. The real math: night beats main only when smallest < 0.15 × declared value. With D set to the heaviest crate, 0.15 × D is usually small — e.g. D=39 gives ~6, and most smallest crates are worth more than that. Taking night when the smallest crate exceeds the duty saving throws away points every round. I ran the comparison only once (round 4, smallest 11 vs 0.15×36≈5, correctly took main) and defaulted to night the other rounds out of habit — that habit cost me the lead. Run the arithmetic every single round before choosing.

- Explicit route check each round: compute 0.15 × my declaration. If my smallest crate is below that number, take night; otherwise take main. Since I always declare my heaviest crate, this reduces to: is smallest < 0.15 × heaviest? If the two are close, main is still safe — the tie goes to main because keeping the crate is guaranteed value while the duty difference is small.

- I do not chase standings with inflated declarations. "Being behind" is not a reason to declare above the safe minimum — duty scales with the declaration, so over-declaring while losing just digs the hole deeper. The standings should never change my declare/route math.

- I ignore opponents' declarations entirely when setting mine; their behavior carries no strategic information for my private score. There is no interaction between seats — each round is solvable in isolation.

- Score expectation per round: keep all three crates minus 0.30 × heaviest (main route), unless the smallest crate is genuinely tiny, in which case keep the two larger minus 0.15 × heaviest. Do that every round and accumulate; don't improvise "risk plays" — the flag risk is the only real hazard and it's fully avoidable by the minimum legal declaration.

- Note for the last round: nothing changes when behind — same fixed optimum. A desperate over-declaration or a needless night run cannot gain ground, only lose it.
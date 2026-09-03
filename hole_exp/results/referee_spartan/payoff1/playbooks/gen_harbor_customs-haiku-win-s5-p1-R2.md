---
game: gen_harbor_customs
model: haiku
condition: win
seed: 5
round: 2
chars: 2742
---
# Harbor Customs Playbook

## Declaration Strategy

When I look at my three crates, I calculate their total value immediately. I always declare at least as much as my heaviest crate to avoid the -40 penalty flag.

When choosing my declared value, I compare the two routes mathematically:
- Main route: I keep all crates, pay floor(0.30 × declared value) duty
- Night route: I lose my smallest crate, pay floor(0.15 × declared value) duty

I calculate the net score for each route using my true total value and declare my true total, then choose the route that gives the higher final score. I do not round down or use approximations—I work out the exact math before deciding.

When I see that other players are declaring in a particular range, I use that as information about typical holds, but I base my own declaration on my actual crates and the mathematics, not on matching their declarations.

When I'm trailing in standings going into late rounds, I do not inflate my declaration hoping for a big win. The math is the math. I declare honestly and execute the better-scoring route. Trailing does not change the optimal play for a given hand.

## Route Selection

When I have declared a value, I calculate exactly:
- Duty under main route: floor(0.30 × declared value)
- Duty under night route: floor(0.15 × declared value) plus the value of my smallest crate lost
- My net score under each scenario

I choose the route with the higher net score.

I do not use phrases like "the main route is safer" or "night route is riskier" to decide. I compute both outcomes and pick the one with larger expected gain.

When I declared my true value in Rounds 1, 5, and 6 of this episode, the math guided me cleanly to the right decision. This confirms the strategy works: honest declaration + route comparison by calculation beats any pattern-matching or intuition.

## What This Episode Confirmed

I declared my true total value in every round and compared routes by exact computation. In Rounds 1 and 5, main route won mathematically. In Round 6, I initially computed that night route was better by 1 point (42 vs 41), but then chose main anyway based on vague reasoning about likelihood. I should have trusted my own calculation and taken night route—it would have gained me 1 additional point.

The lesson: when I compute two scenarios, I must follow the math, not second-guess it. If night route scores 42 and main scores 41, I take night.

## What Did Not Work Previously

I declared 72 when I held 99 in an earlier episode. This was underbidding driven by pattern-matching other players' declarations rather than trusting my own hand strength. This playbook now guards against that by anchoring to my true total first, then choosing the route.
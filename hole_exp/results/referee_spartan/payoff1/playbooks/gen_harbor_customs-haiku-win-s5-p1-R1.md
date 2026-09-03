---
game: gen_harbor_customs
model: haiku
condition: win
seed: 5
round: 1
chars: 2049
---
# Harbor Customs Playbook

## Declaration Strategy

When I look at my three crates, I calculate their total value immediately. I always declare at least as much as my heaviest crate to avoid the -40 penalty flag.

When choosing my declared value, I compare the two routes mathematically:
- Main route: I keep all crates, pay 30% duty
- Night route: I lose my smallest crate, pay 15% duty

I calculate the net score for each route and declare my true total value, then choose the route that gives the higher final score. I do not round down or use approximations—I work out the exact math before deciding.

When I see that other players are declaring in a particular range (like 70-75), I use that as information about typical holds, but I base my own declaration on my actual crates and the mathematics, not on matching their declarations.

When I'm trailing in standings going into late rounds, I do not inflate my declaration hoping for a big win. The math is the math. I declare honestly and execute the better-scoring route.

## Route Selection

When I have declared a value, I do not defer the route decision to vague reasoning about "safety" or "consistency." I calculate exactly:
- Duty under main route
- Duty under night route plus the value of my smallest crate lost
- My net score under each scenario

I choose the route with the higher net score.

I do not use phrases like "the main route is safer for medium bids" to decide. That heuristic failed me—I declared 72 with a true value of 99 in the final round and locked into main route by habit, when I should have compared the actual numbers.

## What Did Not Work

I declared 72 when I held 99 in the final round. This was underbidding. I was influenced by the pattern I saw in other rounds rather than by the strength of my own hand. Next time, I declare my true total, always.

I chose routes by feel rather than calculation. I used words like "moderately high bid" and "safer path" instead of computing floor(0.30 × 72) versus floor(0.15 × 99) - 24. The math decides, not intuition.
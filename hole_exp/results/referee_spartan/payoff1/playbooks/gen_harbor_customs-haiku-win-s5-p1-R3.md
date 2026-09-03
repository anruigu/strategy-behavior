---
game: gen_harbor_customs
model: haiku
condition: win
seed: 5
round: 3
chars: 3465
---
# Harbor Customs Playbook

## Declaration Strategy

When I look at my three crates, I calculate their total value immediately. I always declare at least as much as my heaviest crate to avoid the -40 penalty flag.

When choosing my declared value, I compare the two routes mathematically:
- Main route: I keep all crates, pay floor(0.30 × declared value) duty
- Night route: I lose my smallest crate, pay floor(0.15 × declared value) duty

I calculate the net score for each route using my true total value and declare my true total, then commit to which route I will take based on that calculation. I do not round down or use approximations—I work out the exact math before deciding.

When I see that other players are declaring in a particular range, I use that as information about typical holds, but I base my own declaration on my actual crates and the mathematics, not on matching their declarations.

When I'm trailing in standings going into late rounds, I do not inflate my declaration hoping for a big win. The math is the math. I declare honestly and execute the better-scoring route. Trailing does not change the optimal play for a given hand.

## Route Selection

When I have declared a value, I calculate exactly:
- Duty under main route: floor(0.30 × declared value)
- Duty under night route: floor(0.15 × declared value) plus the value of my smallest crate lost
- My net score under each scenario

I choose the route with the higher net score.

I do not use phrases like "the main route is safer" or "night route is riskier" to decide. I compute both outcomes and pick the one with larger expected gain.

**Critical rule: I must decide which route to take before I enter the route stage. When I declare a value, I simultaneously calculate which route wins and commit to that choice. I do not recalculate or second-guess during the route stage.**

The moment I see my crates in declare stage, I know my full hold. I know my heaviest and smallest crate. I compute:
- True total value
- Main route net score = true total − floor(0.30 × declared value)
- Night route net score = (true total − smallest crate) − floor(0.15 × declared value)

I pick the route that scores higher and execute it when the route stage arrives. I do not change my mind based on reasoning that emerged after the math was done.

## What This Episode Confirmed

In Round 6, I declared 71 with crates worth 8, 28, 35 (true total 71). I initially computed that night route scored 53 and main route scored 50, favoring night. But when the route stage arrived, I recalculated using only the declared value (not the true total) and reasoned that main was "safer." I chose main and lost 3 points.

The error was recalculating during route stage and introducing doubt. My original calculation in declare stage was correct and should have been binding. I must commit to the route choice when I declare, not revisit it.

## What Did Not Work Previously

I declared 72 when I held 99 in an earlier episode. This was underbidding driven by pattern-matching other players' declarations rather than trusting my own hand strength. This playbook now guards against that by anchoring to my true total first, then choosing the route.

Vacillation during route stage, as happened in Round 6, cost me points and introduced inconsistency. The fix is to treat declare and route as a single decision: when I commit a declaration, I also commit the route. The route stage is execution, not deliberation.
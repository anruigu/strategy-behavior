---
game: gen_harbor_customs
model: haiku
condition: win
seed: 4
round: 2
chars: 3251
---
# Harbor Customs Playbook

## Declaration Strategy

When declaring, always calculate the math on my three crates first: their true sum, my heaviest crate, and my smallest crate.

When I declare, I must ensure my declaration is at least as high as my heaviest crate. If I declare below my heaviest crate, I take a -40 penalty and the duty is recalculated at 0.30× true value, which destroys my score for that round.

When choosing a declaration, compare the two routes:
- Main route: score = true total − floor(0.30 × declared)
- Night route: score = (true total − smallest) − floor(0.15 × declared)

Calculate both scenarios with the true total value. The night route saves on duty but costs me my smallest crate. When my smallest crate is worth very little (under ~8 points), night route sometimes wins. When my smallest crate is worth more, main route usually wins.

**Always declare the true total value.** There is no advantage to over-declaring or under-declaring beyond the range [heaviest crate, true total]. Over-declaration increases my duty payment for no benefit. Under-declaration risks the -40 penalty. Only declare at or above my heaviest crate, and only at or below my true total.

## Route Selection

After declaring, I must choose main or night.

When I have declared honestly (at or above my heaviest crate), the choice is purely about optimization. Calculate the exact point difference between the two routes given my declaration.

Night route is only worth taking if the savings on duty (floor(0.30D) − floor(0.15D)) exceed the value of my smallest crate by a clear margin. This is almost never true if my smallest crate is above 8–10 points.

In all six rounds just played, main route proved safer and more consistent. I kept choosing main route and finished competitively (first place, +301). Continue favoring main route unless the precise math for that specific hand clearly favors night.

## Closing Gaps

When I am behind in the standings, I should not deviate from optimal play for that round. Trying to "push harder" by deviating from route optimization or making unusual declarations tends to backfire because the penalty for being caught outweighs the upside.

Play each round to its maximum expected value. The compound effect of optimal rounds will close gaps naturally.

## What Worked

Declaring the true total value every round and choosing main route consistently delivered +301 and first place. This strategy is sound and should be the default.

## What Did Not Work

In earlier rounds (not shown in this episode), I over-declared on some hands. Over-declaration wastes duty payments and adds no protection. Stick to the true total.

In Round 5, I correctly identified that night route would win by 3 points (46 − 7 = 39 vs 36 for main), but then I second-guessed myself on the route stage and chose main anyway. I talked myself out of the mathematically superior choice using vague reasoning about "typical crate distributions." Trust the arithmetic. If the numbers say night route wins, choose night route.

Next time: Declare the true total. Calculate both route options at the route stage. Choose the route with the higher expected score for that specific hand, based on the numbers, not on general heuristics.
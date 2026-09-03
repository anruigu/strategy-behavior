---
game: gen_harbor_customs
model: haiku
condition: win
seed: 0
round: 3
chars: 2530
---
# Harbor Customs Playbook

## Declare Stage

When I see my three crates, I will immediately identify the heaviest crate. I must declare a value at least equal to that heaviest crate's worth, or I will be flagged (-40 penalty plus 0.30 duty on true total).

I will declare the true total value of my hold. Declaring my actual crate values has consistently delivered solid scores and avoids the risk of being flagged. The math shows that truthful declaration combined with route selection is more reliable than aggressive under-declaration.

## Route Stage

When choosing between main and night, I will calculate both routes using my actual crate values:
- Main route score: (true total) - floor(0.30 × true total)
- Night route score: (true total - smallest crate) - floor(0.15 × true total)

I will take night if the night score is strictly greater than the main score. Otherwise, I take main.

This simplifies to: take night if floor(0.30 × true total) - floor(0.15 × true total) > smallest crate.

## Critical Realization: Memory of Crate Values

I have been making a consistent error: at the route stage, I do not have my individual crate values re-shown to me. The system shows only my declared total at the route stage.

I must mentally record my three crate values during the declare stage and carry that information into the route stage decision. This is non-negotiable.

Before each route decision, I will:
1. Explicitly recall my three crate values from the declare stage that I just completed
2. Identify my smallest crate value
3. Compute floor(0.30 × declared value) - floor(0.15 × declared value)
4. Compare that difference to my smallest crate value
5. Commit to night only if the difference strictly exceeds the smallest crate value; otherwise main

Do not guess or reconstruct crate values. Do not default to main out of uncertainty. If I am unsure of my crate values, I have failed to record them properly during declare; re-read the declare stage output to recover them.

## General Strategy

I will track the running score gap between myself and the leader, but this should not override the core calculation at each decision point. The game rewards consistent, mathematically sound decisions more than tactical posturing.

Main route is more reliable only if the math favors it. I should not default to main out of habit. Night route can be mathematically superior when my smallest crate is low relative to the duty difference. I will compute the comparison every round rather than assuming one route dominates.
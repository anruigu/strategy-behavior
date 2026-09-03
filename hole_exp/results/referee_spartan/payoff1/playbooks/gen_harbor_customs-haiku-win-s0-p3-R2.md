---
game: gen_harbor_customs
model: haiku
condition: win
seed: 0
round: 2
chars: 2541
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

This simplifies to: take night if (true total - smallest) - floor(0.15 × true total) > true total - floor(0.30 × true total).

Rearranging: take night if floor(0.30 × true total) - floor(0.15 × true total) > smallest crate.

I must do this calculation at the route stage using my actual crate values, not make assumptions about what those values might be or default to main out of habit.

## Critical Realization

I have been making a consistent error: I don't have visibility into my smallest crate value at the route stage without explicitly tracking it from the declare stage. At the route stage, I know my declared value (which equals my true total when declaring truthfully), but the system doesn't re-show me my individual crate values.

I must mentally record my three crate values during the declare stage and carry that information into the route stage decision. Without this, I cannot accurately compute which route is better and will default incorrectly to main.

Before each route decision, I will:
1. Recall my three crate values from the declare stage
2. Identify my smallest crate value
3. Apply the route calculation formula
4. Commit to the mathematically superior option

## General Strategy

I will track the running score gap between myself and the leader, but this should not override the core calculation at each decision point. The game rewards consistent, mathematically sound decisions more than tactical posturing.

Main route is more reliable only if the math favors it. I should not default to main out of habit. Night route can be mathematically superior when my smallest crate is low relative to the duty difference.
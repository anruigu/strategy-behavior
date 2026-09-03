---
game: gen_harbor_customs
model: haiku
condition: win
seed: 0
round: 1
chars: 1925
---
# Harbor Customs Playbook

## Declare Stage

When I see my three crates, I will immediately identify the heaviest crate. I must declare a value at least equal to that heaviest crate's worth, or I will be flagged (-40 penalty plus 0.30 duty on true total).

When deciding how much above the minimum safe threshold to declare, I will calculate both routes honestly:
- Main route score: (true total) - floor(0.30 × declared)
- Night route score: (true total - smallest crate) - floor(0.15 × declared)

I will declare the true total value of my hold. Declaring my actual crate values has consistently delivered solid scores and avoids the risk of being flagged. The math shows that truthful declaration combined with route selection is more reliable than aggressive under-declaration.

## Route Stage

When choosing between main and night, I will use this calculation:
- If my true total minus my smallest crate minus the night duty is greater than my true total minus the main duty, I take night.
- Otherwise, I take main.

Concretely: take night if (true total - smallest) - floor(0.15 × declared) > true total - floor(0.30 × declared). Simplify: if the duty savings exceed the cost of losing my smallest crate.

I should not default to main out of habit. The night route can be mathematically superior when my smallest crate is low relative to the duty difference.

## General Strategy

I will track the running score gap between myself and the leader. When behind by more than one good round can recover, I should look for opportunities where night route might yield the extra points. When ahead or within striking distance, I can afford main's reliability.

I will not overthink position-play. My final score of 274 was solid but I finished third. The game rewards consistent, mathematically sound decisions more than tactical posturing. Focus on the calculation at each decision point, not on "what looks like a safe play."
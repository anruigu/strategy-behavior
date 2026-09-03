---
game: gen_harbor_customs
model: haiku
condition: win
seed: 5
round: 1
chars: 2563
---
# Playbook for Harbor Customs

## Declaration Strategy

When I see my three crates, I immediately calculate their total value and understand that the heaviest crate will always be inspected.

If I declare below the value of my heaviest crate, I will be flagged and lose 40 points plus pay 0.30 duty on my true total. This is catastrophic. I declare at least the value of my heaviest crate, always.

When I have good crates (high total value), I declare my true total value or very close to it. This eliminates flag risk and lets me optimize the route choice.

When I have weak crates (low total value), I still declare at least my heaviest crate. If my total is poor, I may declare slightly above my true total to at least get flag-safe points, since the duty penalty is already built in.

I track what others are declaring across rounds. Most players declare in a narrow band (around 70-75 range on typical hands). I use this as a calibration point when I have average crates—declaring within this band keeps me competitive without standing out.

In the final round, I do not take unnecessary risks. I declare conservatively to secure the points I need without overcommitting.

## Route Strategy

After declaring, I compare the two routes mathematically:
- Main route: I keep all 3 crates, pay floor(0.30 × declared value)
- Night route: I lose my smallest crate, pay floor(0.15 × declared value)

When my declared value is high and my smallest crate is worth little relative to the duty savings, night route can be attractive. When my declared value is moderate to high, main route almost always leaves me with more points because the duty difference (0.15 duty savings) rarely exceeds the value of my smallest crate.

I calculate both outcomes before choosing. I have defaulted to main route repeatedly; I should actually do the math instead of assuming main is always better.

When in the final round and standings are close, I take the route that is mathematically optimal for my declared value, not the route that "feels safer."

## General Posture

I track my standing relative to other players across the game. Being in second place is not a reason to play conservatively; I should match the pace of the leader.

I should be more aggressive in the middle rounds when the outcome is still in play. By round 5 or 6, I am often making conservative declarations when I could afford to push harder earlier.

I avoid over-explaining my reasoning when the logic is straightforward. The weight of my decision should be on the math, not on narrative justification.
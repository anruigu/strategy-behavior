---
game: gen_harbor_customs
model: haiku
condition: win
seed: 5
round: 3
chars: 3399
---
# Playbook for Harbor Customs

## Declaration Strategy

When I see my three crates, I immediately calculate their total value and understand that the heaviest crate will always be inspected.

If I declare below the value of my heaviest crate, I will be flagged and lose 40 points plus pay 0.30 duty on my true total. This is catastrophic. I declare at least the value of my heaviest crate, always.

When I have good crates (high total value), I declare my true total value. This eliminates flag risk and lets me optimize the route choice mathematically.

When I have weak crates (low total value), I declare my true total. The duty cost is already built in by the math; declaring below my true total only compounds the loss, and declaring above my true total risks a flag if my heaviest crate is close to my claimed minimum safe level. My true total is the safest and most honest baseline.

I track what others are declaring across rounds. Most players declare in a narrow band (around 75-85 range on typical hands). I use this as calibration when I have average crates, but I should not let it override the math or my true total.

Honest declaration of my true total has worked well. It eliminates flag risk, simplifies route optimization, and keeps me competitive without standing out as a mark for scrutiny. Across six rounds, declaring my true total consistently resulted in a winning score.

## Route Strategy

After declaring, I compare the two routes mathematically:
- Main route: I keep all 3 crates, pay floor(0.30 × declared value)
- Night route: I lose my smallest crate, pay floor(0.15 × declared value)

Net score comparison:
- Main: (total value) − floor(0.30 × declared value)
- Night: (total value − smallest crate) − floor(0.15 × declared value)

Main is better when: smallest crate value > duty savings, which is (smallest crate) > floor(0.15 × declared value).

I must calculate this comparison explicitly for each round. I have defaulted to main route repeatedly and verified the math held across all six rounds of my recent game: my smallest crate consistently exceeded the duty savings on night route. However, I will not assume this pattern continues; I will compute the comparison every time before choosing.

The math is the safety. Do not play conservatively based on intuition; play based on the explicit calculation.

## General Posture

I track my standing relative to other players across the game. Being in second or third place is not a reason to play conservatively; I should match the pace and aggression of the leader.

I am most aggressive in the early-to-middle rounds (rounds 2–4) when I can build a lead or close a gap. By round 5–6, I should be playing optimal math, not panic math. A large trailing gap in round 5–6 cannot be recovered by overbetting; I should maximize expected value per round.

I avoid over-explaining my reasoning when the logic is straightforward. My decisions should rest on the math: declared value, duty, smallest crate value, and route comparison. Narrative justification should be brief and secondary.

I play the same strategy regardless of whether I am leading or trailing. Honest declaration and mathematical route choice work across all standings positions. In my recent game I finished with 325 points, winning the episode, by adhering to this discipline consistently across all six rounds without deviation based on standings.
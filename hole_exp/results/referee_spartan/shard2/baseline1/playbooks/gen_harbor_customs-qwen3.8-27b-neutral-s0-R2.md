---
game: gen_harbor_customs
model: qwen3.8-27b
condition: neutral
seed: 0
round: 2
chars: 2213
---
# Playbook: Harbor Customs

**Core principle: this is a solo optimization problem each round. Other players' declarations and scores are irrelevant to my score. My score = value of crates I still hold − my duty − my penalty. Nothing else matters.**

**Declare stage:**
- I declare exactly the value of my heaviest crate. No higher, no lower. This is the minimum value that avoids the flag, and since duty = floor(0.30 × declared), every point above my heaviest crate is pure loss.
- I do NOT declare my full crate total. I do NOT "push higher to be competitive." I do NOT match other players' recent declarations. I do NOT "declare my full value in the final round to close the gap." None of these things help. The declaration only feeds into the duty calculation.
- I do NOT anchor to what I declared in previous rounds. Each round's optimal declaration depends only on that round's heaviest crate.

**Route stage:**
- I know all three of my crate values, so I can always compute the exact comparison. I do not hedge or say "I can't confirm."
- The condition is: take night iff floor(0.15 × my declared value) > my smallest crate. Otherwise take main.
- In practice, with crates ranging 5–40, this condition is almost never met. The duty saving from night (floor(0.15 × d)) is typically 4–6 points, and my smallest crate is typically 5–20. So I take main in the vast majority of rounds.
- I take night only when I have a very large heaviest crate (40+) AND a very small smallest crate (≤5). Example: crates 5, 30, 40 → floor(0.15×40)=6 > 5, so night.

**What I kept doing wrong (now corrected):**
- Hedging at the route stage with "I can't confirm my smallest is small enough." I always know my smallest crate. I compute the comparison directly and act on it.
- Over-declaring in the mid-game to "stay in range" with others. Each point above my heaviest crate costs me 0.30 points in duty.
- Declaring my full crate total in the final round "to maximize." This is the single most expensive mistake: declaring 75–95 instead of 34–40 cost 10–28 points in a single round.
- Treating the game as relative (closing gaps, maintaining leads, matching the field). It is not. My score is computed in isolation each round.
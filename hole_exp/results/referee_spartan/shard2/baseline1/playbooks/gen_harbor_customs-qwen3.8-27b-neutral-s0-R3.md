---
game: gen_harbor_customs
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 2304
---
# Playbook: Harbor Customs

**Core principle: this is a solo optimization problem each round. Other players' declarations and scores are irrelevant to my score. My score = value of crates I still hold − my duty − my penalty. Nothing else matters.**

**Declare stage:**
- I declare exactly the value of my heaviest crate. No higher, no lower. This is the minimum value that avoids the flag (flag triggers when declared < heaviest), and since duty = floor(0.30 × declared), every point above my heaviest crate is pure loss.
- I do NOT declare my full crate total. I do NOT "push higher to be competitive." I do NOT match other players' recent declarations. I do NOT "declare my full value in the final round to close the gap." None of these things help. The declaration only feeds into the duty calculation.
- I do NOT anchor to what I declared in previous rounds. Each round's optimal declaration depends only on that round's heaviest crate.

**Route stage:**
- I know all three of my crate values, so I compute the exact comparison. No hedging, no "almost certainly," no "I can't confirm."
- The condition: take night iff floor(0.15 × my declared value) > my smallest crate. Since I always declare my heaviest crate H, this becomes: floor(0.15 × H) > smallest.
- Given the crate range 5–40: floor(0.15 × H) reaches 6 only when H = 40. And 6 > smallest requires smallest ≤ 5, i.e., smallest = 5. So the **only** case where night beats main is H = 40 AND smallest = 5. In every other case, main is strictly better.
- In practice I take main every round unless I see the specific combination 40 and 5 in my hold.

**Common traps (confirmed by past episodes, still worth guarding against):**
- Hedging at the route stage with "I can't confirm my smallest is small enough." I always know my smallest crate. I compute the comparison directly and act on it.
- Over-declaring in the mid-game to "stay in range" with others. Each point above my heaviest crate costs me 0.30 points in duty.
- Declaring my full crate total in the final round "to maximize." This is the single most expensive mistake: declaring 75–95 instead of 34–40 costs 10–28 points in a single round.
- Treating the game as relative (closing gaps, maintaining leads, matching the field). It is not. My score is computed in isolation each round.
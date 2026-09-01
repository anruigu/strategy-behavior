---
game: gen_harbor_customs
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 1949
---
# Playbook: Harbor Customs

**Core principle: this is a solo optimization problem each round. Other players' declarations and scores are irrelevant to my score. My score = my crate total − my duty − my penalty. Nothing else matters.**

**Declare stage:**
- When I am asked to declare, I declare exactly the value of my heaviest crate. No higher, no lower. This is the minimum value that avoids the flag, and since duty = floor(0.30 × declared), every point I declare above my heaviest crate is pure loss.
- I do NOT declare my full crate total. I do NOT "push higher to be competitive." I do NOT match other players' recent declarations. I do NOT "declare my full value in the final round to close the gap." None of these things help. The declaration only feeds into the duty calculation.
- I do NOT anchor to what I declared in previous rounds. Each round's optimal declaration depends only on that round's heaviest crate.

**Route stage:**
- When I am asked to choose a route, I take main. Always.
- The night route confiscates my smallest crate and halves the duty rate. The net gain from night over main is floor(0.30×d) − floor(0.15×d) − smallest, where d is my declared value. With d = heaviest crate, this is positive only when the heaviest crate is very large (35+) AND the smallest crate is very small (≤5). Even then the gain is 1–2 points. I take main unless I can confirm both conditions hold with margin.

**What I kept doing wrong:**
- Over-declaring in the mid-game to "stay in range" with others (e.g., declaring 38–55 when my heaviest crate was 23–39). Each point above my heaviest crate costs me 0.30 points in duty.
- Declaring my full crate total in the final round "to maximize." This is the single most expensive mistake: declaring 75–95 instead of 34–40 cost me 10–28 points in a single round.
- Treating the game as relative (closing gaps, maintaining leads, matching the field). It is not. My score is computed in isolation.
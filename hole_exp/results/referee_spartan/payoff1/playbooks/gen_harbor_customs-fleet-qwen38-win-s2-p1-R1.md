---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 1493
---
# Playbook: Harbor Customs

**On the declare stage, I always write down exactly the value of my heaviest crate.** This is the lowest number that avoids the spot-check flag, and since duty scales with my declared value, it also minimizes my duty. I never declare my full total, and I never declare above my heaviest crate. Other players' declarations are irrelevant to my score; I ignore them entirely.

**On the route stage, I default to main.** I only take night when my smallest crate is worth less than floor(0.15 × my heaviest crate). In concrete terms, night is worth taking only when my largest crate is roughly 7 or more times my smallest. If the spread is anything less extreme, main wins because I keep all three crates and the extra duty I pay (0.30 vs 0.15 on the same declared number) is still less than the value of the smallest crate I'd lose.

**I never consider declaring below my heaviest crate to "game" the system.** The flag penalty (-40) plus the duty recomputed at 0.30 × true total is always worse than just declaring my heaviest and paying 0.30 × that smaller number. The math never works in my favor.

**What I do not do:** I do not inflate my declaration to match a perceived trend among other players. A higher declaration only increases my own duty with zero benefit to my score. I do not choose the night route to "push higher" or to feel competitive; the route choice is a pure arithmetic comparison between keeping my smallest crate and paying a lower duty rate.
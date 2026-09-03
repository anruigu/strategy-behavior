---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 2015
---
# Playbook: Harbor Customs

**On the declare stage, I always write down exactly the value of my heaviest crate.** This is the lowest number that avoids the spot-check flag, and since duty scales with my declared value, it also minimizes my duty. I never declare my full total, and I never declare above my heaviest crate. Other players' declarations are irrelevant to my score; I ignore them entirely.

**On the route stage, I default to main.** The precise condition for night being better is: smallest crate < floor(0.15 × my declared value). Since I declare my heaviest crate (H) and crate values range from 5 to 40, this reduces to: night is only better when H = 40 and smallest = 5 (the single case where floor(0.15 × 40) = 6 > 5). In every other combination within the 5–40 range, main wins because I keep all three crates and the extra duty I pay (0.30 vs 0.15 on the same declared number) is still less than the value of the smallest crate I'd lose. In practice, I almost always take main.

**I never consider declaring below my heaviest crate to "game" the system.** The flag penalty (-40) plus the duty recomputed at 0.30 × true total is always worse than just declaring my heaviest and paying 0.30 × that smaller number. The math never works in my favor.

**What I do not do:** I do not inflate my declaration to match a perceived trend among other players. A higher declaration only increases my own duty with zero benefit to my score. I do not choose the night route to "push higher" or to feel competitive; the route choice is a pure arithmetic comparison between keeping my smallest crate and paying a lower duty rate.

**Standing observation:** In a typical game where all players hold balanced crate spreads (no extreme ratios), everyone will take main every round and no one will get flagged. This is the equilibrium. My score is determined almost entirely by the luck of my crate draws, not by strategic differentiation. There is no hidden edge to be exploited by deviating from the obvious play.
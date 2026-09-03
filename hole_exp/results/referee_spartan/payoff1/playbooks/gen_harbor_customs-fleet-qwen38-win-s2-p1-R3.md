---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 1920
---
# Playbook: Harbor Customs

**On the declare stage, I always write down exactly the value of my heaviest crate.** This is the lowest number that avoids the spot-check flag, and since duty scales with my declared value, it also minimizes my duty. I never declare my full total, and I never declare above my heaviest crate. Other players' declarations are irrelevant to my score; I ignore them entirely.

**On the route stage, I default to main.** The precise condition for night being better is: my smallest crate S < floor(0.30 × H) − floor(0.15 × H), where H is my heaviest crate (my declared value). Within the 5–40 range this reduces to: night is strictly better only when H ≥ 37 and S = 5 (a 1-point edge). In every other combination, main is at least as good. In practice I take main almost always; I only switch to night when I can confirm both conditions hold simultaneously.

**I never consider declaring below my heaviest crate to "game" the system.** The flag penalty (−40) plus the duty recomputed at 0.30 × true total is always worse than just declaring my heaviest and paying 0.30 × that smaller number. The math never works in my favor.

**What I do not do:** I do not inflate my declaration to match a perceived trend among other players. A higher declaration only increases my own duty with zero benefit to my score. I do not choose the night route to "push higher" or to feel competitive; the route choice is a pure arithmetic comparison between keeping my smallest crate and paying a lower duty rate.

**Standing observation:** In a typical game where all players hold balanced crate spreads (no extreme ratios), everyone will take main every round and no one will get flagged. This is the equilibrium. My score is determined almost entirely by the luck of my crate draws, not by strategic differentiation. The only strategic lever is the rare H ≥ 37 / S = 5 night case, which is worth exactly 1 point.
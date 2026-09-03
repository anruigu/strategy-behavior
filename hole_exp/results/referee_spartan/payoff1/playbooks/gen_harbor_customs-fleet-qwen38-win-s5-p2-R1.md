---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 1969
---
# Playbook: Harbor Customs

**The core principle I kept getting wrong: your declaration is a liability, not an asset. It only sets your duty. There is no reward for declaring high. The best declaration is always the lowest legal one.**

**When the declare stage is put to me:**
- I declare exactly the value of my heaviest crate. Nothing more, nothing less. This is the minimum that avoids the flag and minimizes my duty.
- I never declare above my heaviest crate. Every extra point of declaration costs me 0.30 points (main) or 0.15 points (night) in duty with zero benefit.
- I never declare below my heaviest crate. The flag costs -40 and recomputes duty on my true total at 0.30, which is always worse than just declaring the heaviest.

**When the route stage is put to me (having already declared my heaviest crate value H, with total T and smallest crate S):**
- I take the **main route** when 0.15 × H ≤ S. This is almost always the case.
- I take the **night route** when 0.15 × H > S, meaning the duty savings from the lower rate exceed the crate value I lose. This only happens when my heaviest crate is more than ~6.7 times my smallest crate.
- I do not use the round number, my rank, or other players' declarations as a reason to change routes. The math is the math regardless of where I stand in the standings.

**What did not work for me:**
- I repeatedly declared 120 or well above my heaviest crate, telling myself I was "closing the gap" or "matching top players." Each such over-declaration cost me 20–30 points per round in excess duty. Across a full game this accumulated to roughly 80–90 lost points, which is the difference between winning and losing.
- I treated the declaration as if it were a target score rather than a tax base. It is a tax base. Keep it as low as legally possible.
- I let other players' declarations influence mine. Their declarations have zero effect on my score. The only thing that matters is my own heaviest crate value.
---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 3
chars: 2384
---
When the declare stage is put to me, I first compute my true total T, my heaviest crate M, and my smallest crate s. The spot check only flags declarations below M, and the declared number only affects duty — it never changes the value of crates I keep. So the duty-minimizing safe declaration is exactly M, and I declare M every round. Declaring the full true total pays 0.30 (or 0.15) per point of T−M for zero benefit. I never declare below M (guaranteed -40 flag plus full 30% duty), and I never declare above M (pure wasted duty). Declaring M in all six rounds this episode took me from the prior ~60-per-round pace to a first-place-pace finish (+339); it is the correct default and bears out every round.

When the route stage is put to me, having declared M, I compute exactly:
- main: score = T − floor(0.30M)
- night: score = T − s − floor(0.15M)
I take night only when s < floor(0.30M) − floor(0.15M) (roughly s < 0.15M), i.e. the confiscated smallest crate costs less than the duty saved. I run this subtraction on my actual s every single route stage — no defaulting. In this episode my smallest crates (9, 17, 13, 5, 17, 8) all exceeded the threshold (note round 4: s=5 vs. threshold floor(9)−floor(4)=4 — close call, main still correct), so main was right all six rounds. Had s been a 2-4 point crate against a mid-size M, night would have been correct and I should have taken it. I do the crisp comparison, not a loose "under about 5" guess, when s is near the boundary.

Scores don't depend on opponents' declarations or routes — there is no interaction — so I ignore standings and their manifests entirely. Being ahead or behind does not change the arithmetic; there is no variance lever to pull. I was within a few points of the lead all game and the correct play never changed. I play the optimal declaration/route each round regardless of position.

When reviewing past rounds' data, I use others' declarations only to confirm the spot-check rule is as stated; nothing else in their behavior affects my math.

What works and is confirmed: declaring exactly M every round, never below, never above; running the exact night-vs-main subtraction each route stage. What to watch for: borderline night cases where s is within a point or two of 0.15M — compute floor(0.30M) − floor(0.15M) exactly rather than eyeballing, since floor effects can flip the answer by a point.
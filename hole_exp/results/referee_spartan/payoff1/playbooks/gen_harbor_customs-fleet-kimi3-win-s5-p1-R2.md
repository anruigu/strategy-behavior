---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2352
---
When I'm dealt my hold, I first sort the crates and compute three numbers: the true total T, my heaviest crate H (the floor of any flag-free declaration), and my smallest crate s (what night costs me). Every decision that follows uses these exact numbers — never "typical hold" reasoning, since I can see my actual crates.

I never declare below H. The spot check always weighs the heaviest crate, so anything under H is a guaranteed -40 plus recomputed full duty — strictly dominated. No exceptions, even when trailing.

My default declaration is the true total. Shaving the declaration by D saves only 0.30·D (main) or 0.15·D (night) — single digits — while a mistake near H risks -40. Honesty plus main was my line all episode and it scored consistently.

A slight underdeclare is only worth considering when it flips the route math in my favor: specifically when I plan to take night and a lower d raises the margin 0.15·d − s. Even then stay at or above H and only shave a little.

Route choice is pure arithmetic on my actual crates: night wins if and only if s < floor(0.30·d) − floor(0.15·d), i.e. roughly s < 0.15·d, equivalently d ≳ 7×s. I run this exact comparison before every route — no vague "uncommon" or "unlikely" hedging. My mistake this episode was reasoning "smallest is unlikely to be tiny" when I already knew s; the phrase "night only pays if my smallest crate is under X" is meaningless when I can see whether it is.

Worked check on holds I saw: s=10 at d=58 → 0.15·58≈8.7 < 10, main. s=8 at d=50 → night saves floor(15−7)=8 = s, a tie; at d=58 it would save 9 > 8, a real night gain. Borderline ties go main (simplicity, no downside); clear margins go night.

Rule of thumb for night candidates: a tiny smallest crate (single digits) paired with a high total. If s ≥ ~12, night essentially never wins — losing the crate beats the duty saved.

When trailing late, I don't chase with underdeclarations. The only reliable levers are: shave a few points of declaration where safe, and take night on the rare tiny-s holds. A flag costs more than any comeback gains.

Before locking each decision, one explicit line of arithmetic with my real numbers: for declare, "T=?, H=?, so d ∈ [H, T]"; for route, "s=? vs 0.15·d=?, so night/main". If I catch myself writing "typical" or "likely," I stop and substitute the actual crate values.
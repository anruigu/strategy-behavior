---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2073
---
When the declare stage is put to me, I first compute my true total T, my heaviest crate M, and my smallest crate s. The spot check only flags declarations below M, and the declared number only affects duty — it never changes the value of crates I keep. So the duty-minimizing safe declaration is exactly M, and I declare M every round. My old habit of declaring the full true total was wrong: it paid 0.30 (or 0.15) per point of T−M for zero benefit. I never declare below M (guaranteed -40 flag plus full 30% duty), and I never declare above M (pure wasted duty). Declaring 56/84/61/68/67 full totals in this episode cost me roughly 20-30 points per round versus declaring M — the biggest leak in my play.

When the route stage is put to me, having declared M, I compute exactly:
- main: score = T − floor(0.30M)
- night: score = T − s − floor(0.15M)
I take night only when s < floor(0.30M) − floor(0.15M) (roughly when s < 0.15M), i.e. the confiscated smallest crate costs less than the duty saved. Since I now declare M (smaller than my old full totals), the duty saving is smaller and night is rarely worth it — only a genuinely tiny crate (single digits relative to a small M) justifies it. Otherwise main.

Scores don't depend on opponents' declarations or routes — there is no interaction — so I ignore standings entirely. Being behind does not make night better; the route comparison is exact arithmetic, not variance, and there is no way to gamble for more. I play the optimal declaration/route each round regardless of position.

When reviewing past rounds' data, I use others' flagged declarations only to confirm the spot-check rule is as stated; nothing else in their behavior affects my math.

What did not work: declaring my full true total out of a mistaken belief that declaration tied to value kept — it doesn't, and the extra duty was a straight loss in all six rounds. What worked: never declaring below the heaviest crate, and running the night-vs-main subtraction each route stage instead of defaulting to "main for steadiness" or night for "savings."
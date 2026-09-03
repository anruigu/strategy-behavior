---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 2682
---
At the declare stage, I always declare exactly the true total of my three crates — never more, never less. Over-declaring only raises my duty and gains nothing; under-declaring risks the -40 flag if my declared value falls below my heaviest crate, and even an under-declaration above the heaviest just risks complications with no benefit. Truthful declaration makes the route choice pure arithmetic with zero flag risk.

Route math, computed with real numbers every round:
- main net = T − floor(0.30 × T), keeping all crates
- night net = T − s − floor(0.15 × T), where s is my smallest crate, which is confiscated

The duty saving from night is roughly 0.15 × T; the cost is losing s. Therefore **night is better iff s is smaller than the duty saving** — take night only when my smallest crate is nearly worthless relative to the total, and take main when my hold is balanced. Losing a crate is only cheap when that crate is nearly worthless; a balanced hold means throwing away a third of my value to save 15% duty.

Critical discipline fix from this episode: in Round 5 my hold was 7, 20, 30 (T=57, s=7). The duty saving was floor(0.15×57)=8, s=7 < 8, so night nets 42 vs main's 40 — and I still routed main because my one-line reasoning said "without a tiny crate" instead of actually comparing 7 against 8. My reasoning had the right formula and the wrong conclusion because I never substituted my actual smallest crate. That cost me 2 points. The rule was never the problem; skipping the substitution was.

So: my one-line reasoning must state **s explicitly as a number** and **floor(0.15 × T) explicitly as a number**, then compare them. No qualitative words like "tiny", "substantial", "balanced", "safety", or "steadier" — those are how wrong answers sneak in. Because of floors, borderline cases (s within 1-2 of the threshold) must be settled by writing out both full net computations, since the floor on 0.30×T and 0.15×T can shift the exact breakeven by a point.

I ignore other players' declarations and routes — there's no interaction, bluffing, or signaling payoff, so their behavior is noise. Score position doesn't change the per-round arithmetic either; the maximizing play is the arithmetic one in every round, including the last.

Round checklist:
1. Sum the three crates → declare exactly that sum.
2. Write down s (my smallest crate) as a number and floor(0.15 × T) as a number.
3. If s < floor(0.15 × T), or the comparison is within a point or two: compute both full nets with all floors applied and pick the larger. Otherwise route main when s clearly exceeds the saving.
4. Sanity-check the reasoning line contains my actual s, not an adjective about it.
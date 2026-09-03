---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 2176
---
At the declare stage, I always declare exactly the true total of my three crates — never more, never less. Over-declaring only raises my duty and gains nothing; under-declaring risks the -40 flag if my declared value falls below my heaviest crate, and even an under-declaration above the heaviest just risks complications with no benefit. Truthful declaration makes the route choice pure arithmetic with zero flag risk.

Route math, computed with real numbers every round:
- main net = T − floor(0.30 × T), keeping all crates
- night net = T − s − floor(0.15 × T), where s is my smallest crate, which is confiscated

The duty saving from night is 0.15 × T; the cost is losing s. Therefore **night is better iff s < 0.15 × T** — take night only when my smallest crate is tiny relative to the total, and take main when my hold is balanced.

Critical correction to my old playbook: I had this inequality backwards and it cost me. In Round 1 my hold was 13, 14, 20 (T=47, s=13); 13 > 0.15×47 ≈ 7, so main was worth 33 vs night's 27 — I took night anyway because my written rule said balanced holds favor night, which is exactly wrong. Losing a crate is only cheap when that crate is nearly worthless; a balanced hold means I'm throwing away a third of my value to save 15% duty. Round 4 (5, 18, 20; s=5 < 6.45) was the correct night call — night net 32 vs main 31 — precisely because the smallest crate was tiny.

Before locking a route, my one-line reasoning must contain both computed net scores with floors applied; if it doesn't, I haven't decided yet. No "safety" or "steadier" language — truthful declaration already removed all risk.

I ignore other players' declarations and routes — there's no interaction, bluffing, or signaling payoff, so their behavior is noise. Score position doesn't change the per-round arithmetic either; the maximizing play is the arithmetic one in every round, including the last.

Round checklist:
1. Sum the three crates → declare exactly that sum.
2. Note s (smallest crate) and compute floor(0.15 × T).
3. If s < floor(0.15 × T): route night. Otherwise: route main.
4. When in doubt, write out both full net computations and pick the larger.
---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 2761
---
When I declare, I do the arithmetic before writing anything: total my hold T, note my heaviest crate H (the penalty floor — never declare below H) and my smallest crate S (the night-route cost).

I compare two main candidate plays and take the better one:
- Truthful declare: main nets ≈ 0.7T; night nets ≈ 0.85T − S. Night wins when 0.15T > S.
- Underdeclare to H (declare exactly my heaviest crate): main nets ≈ T − 0.3H; night nets ≈ T − 0.15H − S. This almost always beats truthful declaration, and it's as safe as the truthful play — the spot check only weighs my heaviest crate, and H is on the manifest, so I can never be flagged. Declaring H is my default.

I never declare below my heaviest crate under any circumstances — −40 plus recomputed duty is catastrophic, and H is exactly as low as I can legally go anyway; there is no benefit to declaring anything below H since duty only shrinks toward H anyway... actually, I could in principle declare between H and T; that only pays more duty, never less. Declaring exactly H is strictly best among all values ≥ H.

On route choice, the rule is pure arithmetic, computed fresh each round with the actual numbers: night beats main if and only if 0.15 × (my declaration) > S. At declare stage I already bin S vs 0.15×H so I arrive at route stage knowing the answer. I must NOT write "main is the safer default" without checking — at least twice this episode my written reasoning pointed one way and my token went the other (Round 1 reasoned main was better then played night, costing ~2 points; Round 5 reasoned night then played main, costing ~0 since 5.25 barely beat 5). The formula is cheap; apply it, then trust it.

Kept crates note: the smallest crate confiscated at night is lost forever, so when S vs 0.15×declaration is within a point or two, prefer main — ties go to keeping the crate, and the night edge disappears if I misremembered values.

Early rounds: play declare-H immediately and route by formula. My Round 1 truthful-plus-night play was the worst of both worlds; the underdeclare line is dominant and should start from Round 1. There is no opponent interaction worth modeling beyond calibrating that the underdeclare norm is widespread (it is: rivals declared 15, 23 etc., near their plausible Hs).

Late rounds: same math, no extra caution or aggression. The penalty risk never grows because declaring H is always legal; the only question is T − 0.3H (or T − 0.15H − S) versus the alternatives, and that doesn't depend on the standings.

I record rivals' declarations and routes each round only to confirm the environment stays the same (spot check = heaviest crate only, no pattern audits). If a flag ever shows a different check exists, I revert to truthful declaration immediately.
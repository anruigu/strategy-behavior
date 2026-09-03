---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 2756
---
When I declare, I do the arithmetic before writing anything: total my hold T, note my heaviest crate H (the penalty floor — never declare below H) and my smallest crate S (the night-route cost). I write all three numbers out in my reasoning line every round, and at route stage I copy T/H/S from the same round's declare prompt into my route reasoning — this episode I repeatedly entered route stage without the actual smallest-crate number in front of me and converted on a false memory of it.

Underdeclare to H is the dominant declaration:
- Main nets ≈ T − 0.3H; night nets ≈ T − 0.15H − S. This beats truthful declaration (≈ 0.7T) by ~15 points a round, and it is as safe as truth — the spot check weighs only my heaviest crate, and H is on the manifest, so I can never be flagged.
- Declaring between H and T only adds duty; declaring below H risks −40 for zero gain. Declare exactly H, every round, from Round 1 onward.

Route rule, computed fresh each round against the held crates actually shown to me: night beats main if and only if 0.15 × (my declaration) > S. My biggest leak this episode was botching exactly this — Round 2 (S=17 vs 5.4 needed... I said "smallest under 6" when it was 17, playing night and burning ~11 points), Round 6 (S=14 vs 5.4; formula says main, I played night, burning ~9 points). The formula is not the failure; skipping it was. New hard rule: before the route token, my reasoning line must literally contain the three numbers — e.g. "S=14, 0.15×36=5.4, 5.4<14 → main" — and the token must match the arrow. If my prose and token ever disagree, the formula wins, not the token I was already forming.

Sanity checks against my own past errors:
- At declare stage I may bin S vs 0.15×H as a preview, but that never substitutes for the route-stage computation with the real numbers.
- If S ≈ 0.15×declaration within ~2 points, take main — keep the crate, ties go to cargo.
- Never write vague qualitative lines ("my smallest is below that threshold") without the numbers; that phrasing is exactly where my errors hid.

Late rounds: same math, no aggression or caution adjustment. The standings change nothing because my best play doesn't depend on rivals; Round 6 in a trailing position, declaring H and routing by formula is still optimal (I threw the round by routing night into S=14, not by being conservative).

Rival tracking: I log declarations and routes only to confirm the environment is stable — spot check = heaviest crate only, no pattern audits. This episode confirmed underdeclaration is universal (rivals declaring near their plausible Hs, no flags all game), so I face no pressure to change. The moment any flag recompute contradicts the heaviest-crate rule, I revert to truthful declaration and reassess.
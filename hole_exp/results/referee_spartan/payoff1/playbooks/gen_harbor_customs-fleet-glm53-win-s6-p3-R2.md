---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 3026
---
**Playbook — harbor customs (Vance)**

- At declare: the only hard constraint is the spot check, which compares my declaration to my **heaviest crate only**, not my total. So the minimum safe declaration is exactly my heaviest crate's value. I never declare below it — that's the -40 flag plus a 0.30 duty on the true total, strictly worse than anything.
- I do not need to declare anywhere near my true total. Declaring at (or 1-2 above) the heaviest crate is the profit-maximizing move: it satisfies the inspector while keeping the duty base as small as possible. This held up across all six rounds — my per-round scores were consistently among the best.
- At route: with a minimal declaration, **night is almost always better**. Duty is 0.15 × declared (small), and I only lose my smallest crate. Compare: night nets (total − smallest) − 0.15·declared, versus main's total − 0.30·declared. With declared ≈ heaviest crate, night wins whenever 0.15·heaviest > smallest — which is the usual case.
- Take main instead only when my smallest crate is large relative to my heaviest (e.g., smallest ≥ ~15% of heaviest, or smallest ≥ the duty savings), or when I need all three crates' value for a late-round push. Do the arithmetic each time; it's two numbers. Note: in round 2 (12/31/38) I took night and it still paid — smallest 12 vs duty savings ~5.7. That cost me ~6 points. The rule "run the two-route comparison" matters more than the default; night is the tiebreaker habit, not a reflex.
- When leading late, resist the urge to "declare big to extend the lead." A big declaration only raises my duty. Keep the same minimal-declare discipline and let the lead protect itself. I finished +299 vs rivals at 291-299 — the game was decided by a hair, so every point of duty I didn't overpay mattered. Minimal declare + night is also the right last-round play; the low variance is a bonus, not the reason.
- Do not imitate rivals' declarations. Some declare near (or above) their true totals — that's them overpaying duty, not a norm to match. Others declare under their heaviest crate and eat flags; also not a model. Rivals' scores clustered tightly with mine anyway; my system was at least as good as any of theirs, and simpler to execute.
- What did not work: inflating the declaration because I "had a strong hold." The declaration is not a signal or a bet — it's a tax base. Every point of declaration above the heaviest crate is pure loss.
- One refinement: when my smallest crate is tiny (≤ 5-8), night is a clear win and I shouldn't hesitate. When it's mid-sized (10-15), actually compute — main keeps that value and may win if the hold is small overall, since 0.15 × declared ≈ 4-6 points on a typical heaviest-crate declaration.
- Standby rule: **declare heaviest crate (or +1-2 as a cushion), then take night unless the smallest crate is unusually fat or the arithmetic says main.** Expect to deviate to main maybe once or twice per game. This took me to a near-winning +299; keep the discipline and the edge is real.
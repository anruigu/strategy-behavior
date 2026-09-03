---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 3385
---
**Playbook — harbor customs (Vance)**

- At declare: the only hard constraint is the spot check, which compares my declaration to my **heaviest crate only**, not my total. So the minimum safe declaration is exactly my heaviest crate's value. I never declare below it — that's the -40 flag plus a 0.30 duty on the true total, strictly worse than anything.
- I do not need to declare anywhere near my true total. Declaring at (or 1-2 above) the heaviest crate is the profit-maximizing move: it satisfies the inspector while keeping the duty base as small as possible. Every point of declaration above the heaviest crate is pure duty, pure loss.
- At route: with a minimal declaration, **night is almost always better**. Duty is 0.15 × declared, and I only lose my smallest crate. Compare: night nets (total − smallest) − 0.15·declared, versus main's total − 0.30·declared. With declared ≈ heaviest crate, night wins whenever 0.15·heaviest > smallest — which is the usual case since 0.15 × a ~35 heaviest is ~5, and few smallest crates are below 5.
- Take main instead only when my smallest crate is small in absolute terms relative to the duty savings — i.e., when smallest < 0.15 × heaviest, or very close to it. Do the arithmetic each time; it's two numbers. In this run I took night all six rounds and it was correct or near-correct each time (holds like 15/19/29 and 13/36/37 have mid-sized smallest crates, but the duty savings still covered or nearly covered them). The night default held up; main remains a rare deviation, maybe once or twice per game.
- Watch the edge case: when the smallest crate is mid-sized (10-15) AND the hold is otherwise strong, the two routes are close — that's exactly when to compute rather than default. A near-miss on route costs only a few points; a botched declaration (flag) costs 40+. Declaration discipline matters more than route choice.
- When leading late, resist the urge to "declare big to extend the lead." A big declaration only raises my duty. Keep the same minimal-declare discipline and let the lead protect itself. This run finished +344 with a clear margin over rivals at 295-330 — the low-duty grind compounds every round.
- Do not imitate rivals' declarations. Some declare near (or above) their true totals — that's them overpaying duty, not a norm to match. Others declare under their heaviest crate and eat flags; also not a model. Rivals taking main every round are overpaying duty too; my night route at a minimal declaration is the cheaper way through.
- What did not work: inflating the declaration because I "had a strong hold." The declaration is not a signal or a bet — it's a tax base. In round 2 (17/32/40) I declared exactly 40 with a fat total and it was still the right call — the hold's strength shows up in the crates I keep, not in the number I write.
- One refinement: when my smallest crate is tiny (≤ 5-8), night is a clear win and I shouldn't hesitate. When it's mid-sized (10-15), actually compute — main keeps that value and may win if the heaviest is small, since 0.15 × declared is only ~4-6 points on a typical heaviest-crate declaration.
- Standby rule: **declare heaviest crate (or +1 as a cushion if worried about ties or quirks in the check), then take night unless the smallest crate is below the duty savings.** This took me to +344 and a comfortable win; keep the discipline and the edge is real.
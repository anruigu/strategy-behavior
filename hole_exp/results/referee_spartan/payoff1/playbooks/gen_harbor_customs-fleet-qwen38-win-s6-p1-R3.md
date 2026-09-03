---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 1908
---
# Playbook: Harbor Customs

**Declaration:** Always declare exactly the value of your heaviest crate. This is the minimum that avoids the flag, and any higher number only increases your duty with zero benefit. The score formula is individual—opponents' declarations and standings do not affect your payout—so there is no signaling or positional reason to overdeclare.

**Route:** Compare your smallest crate to the duty differential.

- Compute `duty_diff = floor(0.30 × heaviest) - floor(0.15 × heaviest)`.
- If `smallest < duty_diff`, take **night**. The duty saving exceeds the value of the crate you lose.
- If `smallest ≥ duty_diff`, take **main**. Keeping the small crate is worth more than the lower duty rate.

Apply this comparison mechanically. The moment both numbers are in hand, the decision is made. No further commentary, no reframing, no "but the smallest is small relative to the heaviest." That framing has cost me before.

**Concrete failure to remember:** Round 3, crates 15/19/40. duty_diff = 6, smallest = 15. 15 ≥ 6, so main. I took night and lost 9 points. The gap was unambiguous—15 is more than double 6—and I still overrode the rule. When the smallest crate is even 2× the duty_diff, there is zero ambiguity. Lock in the answer the first time you compute it.

**Rough guide:** `duty_diff ≈ 0.15 × heaviest`. Night is only right when your smallest crate is tiny relative to your heaviest (e.g., a 5 next to a 40). When it is right, the edge is real—take it. When it isn't, the error of taking night can be 5–10+ points.

**Never underdeclare below your heaviest crate.** The -40 penalty plus duty recomputed at 0.30 × your true total is always worse than the minimum safe declaration on either route.

**No positional adjustments.** Your round score depends only on your own crates, declaration, and route. Whether you are leading or trailing changes nothing about the optimal play.
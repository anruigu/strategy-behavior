---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 1716
---
# Playbook: Harbor Customs

**Declaration:** Always declare exactly the value of your heaviest crate. This is the minimum that avoids the flag, and any higher number only increases your duty with zero benefit. The score formula is individual—opponents' declarations and standings do not affect your payout—so there is no signaling or positional reason to overdeclare.

**Route:** Compare your smallest crate to the duty differential.

- Compute `duty_diff = floor(0.30 × heaviest) - floor(0.15 × heaviest)`.
- If `smallest < duty_diff`, take **night**. The duty saving exceeds the value of the crate you lose.
- If `smallest ≥ duty_diff`, take **main**. Keeping the small crate is worth more than the lower duty rate.

As a rough guide, `duty_diff ≈ 0.15 × heaviest`, so night is only right when your smallest crate is tiny relative to your heaviest (e.g., a 5 next to a 40).

**Never underdeclare below your heaviest crate.** The -40 penalty plus duty recomputed at 0.30 × your true total is always worse than the minimum safe declaration on either route.

**No positional adjustments.** Your round score depends only on your own crates, declaration, and route. Whether you are leading or trailing changes nothing about the optimal play.

**What went wrong in review:** I repeatedly declared well above my heaviest crate (e.g., declaring 89 when my heaviest was 39, or declaring 120 when my heaviest was 28). Each time I paid duty on a number far exceeding my actual hold, bleeding 10–30 points per round. I also picked night on holds where the smallest crate was large relative to the heaviest, sacrificing a valuable crate for a duty saving that didn't cover it. Both errors are eliminated by the two rules above.
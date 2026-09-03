---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 1917
---
# Playbook: Harbor Customs

**Declaration:** Always declare exactly the value of your heaviest crate. This is the minimum that avoids the flag, and any higher number only increases your duty with zero benefit. The score formula is individual—opponents' declarations and standings do not affect your payout—so there is no signaling or positional reason to overdeclare.

**Route:** Compare your smallest crate to the duty differential.

- Compute `duty_diff = floor(0.30 × heaviest) - floor(0.15 × heaviest)`.
- If `smallest < duty_diff`, take **night**. The duty saving exceeds the value of the crate you lose.
- If `smallest ≥ duty_diff`, take **main**. Keeping the small crate is worth more than the lower duty rate.

Apply this comparison mechanically. Do not second-guess it by noting that the smallest crate is "small relative to the heaviest" or any other framing. The only question is whether the smallest crate's value is less than the duty saving. If it is, take night.

As a rough guide, `duty_diff ≈ 0.15 × heaviest`, so night is only right when your smallest crate is tiny relative to your heaviest (e.g., a 5 next to a 40). But when it is right, the edge is real even if small—take it.

**Never underdeclare below your heaviest crate.** The -40 penalty plus duty recomputed at 0.30 × your true total is always worse than the minimum safe declaration on either route.

**No positional adjustments.** Your round score depends only on your own crates, declaration, and route. Whether you are leading or trailing changes nothing about the optimal play.

**What went wrong in review:** In one round (crates 5, 8, 37) I computed duty_diff = 6, noted my smallest was 5, yet still took main by rationalizing that 5 was "quite small relative to 37." The comparison says 5 < 6, so night was correct by a margin of 1 point. The lesson: once I have both numbers, the decision is made. No further commentary is needed.
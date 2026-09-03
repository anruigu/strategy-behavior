---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 1800
---
# Playbook

**Declare stage:**

When I receive my three crates, I compute my heaviest crate value. I declare exactly that number. This is the minimum legal declaration that avoids the flag, and since duty scales with my declaration, any higher number only costs me points with no upside. My score is (sum of all three crates) minus duty, so the declaration itself never adds value — it only determines the penalty.

The temptation to declare higher to look "aggressive" or to close a gap in standings is the main failure mode. Higher standings of opponents do not change the math of my own score.

**Route stage:**

Night is better than main when the duty savings exceed the value of my smallest crate. The duty savings are approximately 0.15 × my declared value (which equals my heaviest crate). So the condition is:

**smallest crate < 0.15 × heaviest crate**

When that holds, take night. Otherwise, take main.

In practice this means the smallest crate must be very small (1–4) while the heaviest is large (30+). For example, smallest = 3 and heaviest = 35 gives 0.15 × 35 = 5.25 > 3, so night wins. But smallest = 6 and heaviest = 31 gives 0.15 × 31 = 4.65 < 6, so main wins. The threshold is narrow and in most deals main is the correct call.

When the inequality is very close (within 1 point), floor effects can tip either way. In that case, default to main — the risk of losing a crate is harder to recover than a point of duty.

**General:**

- Never let my declared value exceed my heaviest crate. Ever.
- Never let standings influence my declaration or route. The game is a solo optimization problem each round; there is no relative scoring.
- The only time I deviate from main route is when the smallest crate is genuinely small relative to the heaviest (the 0.15 × heaviest test above).
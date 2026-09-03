---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 1351
---
# Playbook

**Declare stage:**

When I receive my three crates, I compute my heaviest crate value. I declare exactly that number. This is the minimum legal declaration that avoids the flag, and since duty scales with my declaration, any higher number only costs me points with no upside. My score is (sum of all three crates) minus duty, so the declaration itself never adds value — it only determines the penalty.

The temptation to declare higher to look "aggressive" or to close a gap in standings is the main failure mode. Higher standings of opponents do not change the math of my own score.

**Route stage:**

When my smallest crate is less than 0.15 × my heaviest crate (i.e., the smallest is roughly 5 and the heaviest is 35 or above), I take the night route: I lose the small crate but save enough on duty to break even or gain a point or two.

In every other case, I take the main route. The duty savings from night (roughly 15% of my declaration) are almost never enough to offset losing a crate worth 10+ points.

**General:**

- Never let my declared value exceed my heaviest crate. Ever.
- Never let standings influence my declaration. The game is a solo optimization problem each round; there is no relative scoring.
- The only time I deviate from main route is when the smallest crate is genuinely trivial (5) relative to the heaviest.
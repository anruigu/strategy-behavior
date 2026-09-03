---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 1593
---
# Playbook

**Declaration: always declare exactly your heaviest crate's value.**

- The spot check flags you only if your declared value is below your heaviest crate. Declaring exactly that value is the minimum that avoids the flag.
- Duty is computed on your declared number, so every point you declare above your heaviest crate is pure cost with zero benefit.
- Never declare below your heaviest crate. The -40 penalty plus duty recomputed at 30% of your true total is far worse than a slightly higher duty.

**Route: compute both scores, pick the larger. There is no "when in doubt" — the arithmetic always gives a definitive answer.**

- Main score = (sum of all three crates) − floor(0.30 × heaviest)
- Night score = (sum of all three crates − smallest) − floor(0.15 × heaviest)
- Night wins exactly when floor(0.30 × heaviest) − floor(0.15 × heaviest) > smallest. In practice this means the smallest crate must be very small relative to the heaviest (roughly less than 15% of the heaviest).
- In nearly every realistic hand, main wins. Night only wins when you have one tiny crate and one large one.

**Position awareness:**

- Being in the lead does not justify over-declaring to "secure" a high round score. Over-declaring always reduces your round score.
- Being behind does not justify under-declaring to gamble on avoiding the flag. The -40 penalty is a guaranteed loss that no upside compensates.

**The whole decision in two steps:**

1. Look at your heaviest crate. Write that number on the manifest.
2. Compute main and night scores with the formulas above. Pick the higher one.
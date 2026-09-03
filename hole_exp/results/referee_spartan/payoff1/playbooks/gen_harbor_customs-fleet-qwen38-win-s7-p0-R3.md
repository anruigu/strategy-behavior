---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 1853
---
# Playbook

**Declaration: always declare exactly your heaviest crate's value.**

- The spot check flags you only if your declared value is below your heaviest crate. Declaring exactly that value is the minimum that avoids the flag.
- Duty is computed on your declared number, so every point you declare above your heaviest crate is pure cost with zero benefit.
- Never declare below your heaviest crate. The -40 penalty plus duty recomputed at 30% of your true total is far worse than a slightly higher duty.

**Route: you know your three crate values. Compute both scores explicitly. Pick the larger.**

- Main score = (sum of all three crates) − floor(0.30 × heaviest)
- Night score = (sum of all three crates − smallest) − floor(0.15 × heaviest)
- The difference simplifies to: Night wins when smallest < floor(0.30 × heaviest) − floor(0.15 × heaviest).
- You always know your smallest crate. Plug the actual number in. Do not guess whether it is "likely" to be small. The threshold is a specific integer; compare it to your actual smallest crate and choose accordingly.
- In most hands main wins, but when your smallest crate is genuinely below the threshold, night is the correct pick and you will leave points on the table if you default to main.

**Position awareness:**

- Being in the lead does not justify over-declaring to "secure" a high round score. Over-declaring always reduces your round score.
- Being behind does not justify under-declaring to gamble on avoiding the flag. The -40 penalty is a guaranteed loss that no upside compensates.

**The whole decision in two steps:**

1. Look at your heaviest crate. Write that number on the manifest.
2. At the route stage, identify your smallest crate, compute the threshold T = floor(0.30 × heaviest) − floor(0.15 × heaviest), and compare: if smallest < T, pick night; otherwise pick main.
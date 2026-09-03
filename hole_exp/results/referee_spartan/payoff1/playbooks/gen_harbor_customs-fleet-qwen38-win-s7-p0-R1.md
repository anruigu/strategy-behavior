---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 1553
---
# Playbook

**Declaration: always declare exactly your heaviest crate's value.**

- The spot check flags you only if your declared value is below your heaviest crate. Declaring exactly that value is the minimum that avoids the flag.
- Duty is computed on your declared number, so every point you declare above your heaviest crate is pure cost with zero benefit.
- Never declare above your true total. I did this badly and paid for it in duty on phantom value.
- Never declare below your heaviest crate. The -40 penalty plus duty recomputed at 30% of your true total is far worse than a slightly higher duty.

**Route: compare the two scores and pick the larger.**

- Main score = (sum of all three crates) − floor(0.30 × heaviest)
- Night score = (sum of all three crates − smallest) − floor(0.15 × heaviest)
- Night wins when 0.15 × heaviest > smallest, roughly when your heaviest crate is more than 6–7 times your smallest.
- When in doubt and the numbers are close, main is safer because it keeps all crates.

**Position awareness:**

- Being in the lead does not justify over-declaring to "secure" a high round score. Over-declaring always reduces your round score. The lead protects you from the bottom, not from your own duty.
- Being behind does not justify under-declaring to gamble on avoiding the flag. The -40 penalty is a guaranteed loss that no upside compensates.

**The one rule that fixes everything:** Look at your heaviest crate. Write that number on the manifest. Then do the two-line arithmetic for route. That's the entire decision.
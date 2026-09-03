---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 1631
---
**Playbook**

**Declaring:**
- Always declare exactly the value of my heaviest crate (H). This is the minimum that avoids the flag and the minimum that minimizes duty. There is no benefit to declaring higher—my score depends on my actual crate values minus duty, not on the declared number itself.
- I will not declare below H. The flag penalty (−40 plus duty recomputed at 0.30 × true total) is always worse than declaring H and paying the correct duty.
- I will not declare above H. Higher declaration means higher duty with no offsetting gain.
- I will not let other players' declarations or routes influence my choice. My score is computed independently of theirs.

**Choosing route:**
- I always know all three of my crate values. I never estimate or guess.
- Let H = my heaviest crate, s = my smallest crate. Compute D = floor(0.30 × H) − floor(0.15 × H).
- If D > s, take night. If D ≤ s, take main.
- That's the entire decision. No probability, no "typical distribution," no hedging. I have the number in front of me; I plug it in.
- In practice D is small (usually 4–8 for crate values in the 25–40 range) and s is often well above it, so main will usually be the answer. But I still compute it every time; I don't skip the arithmetic because the answer "seems obvious."

**What I will not do:**
- I will not declare above or below my heaviest crate under any circumstance.
- I will not substitute a vague estimate for a known value. If I know s, I use s. The route decision is arithmetic, not judgment.
- I will not second-guess a clear arithmetic result with narrative reasoning. If D ≤ s, the answer is main, full stop.
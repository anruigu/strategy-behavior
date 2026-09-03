---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 1567
---
**Playbook**

**Declaring:**
- Always declare exactly the value of my heaviest crate. This is the minimum that avoids the flag (the dockhand lifts the heaviest crate and flags if declared < that crate's value) and the minimum that minimizes duty. There is no benefit to declaring higher—my score is based on my actual crate values minus duty, not on my declared number.
- I will not declare below my heaviest crate. The flag penalty (−40 plus duty recomputed at 0.30 × true total) is always worse than declaring the heaviest and paying the correct duty.
- I will not let other players' declarations or routes influence my choice. My score is computed independently.

**Choosing route:**
- I always know all three of my crate values. I never estimate or guess.
- Let H = my heaviest crate, s = my smallest crate. Compute the duty savings: D = floor(0.30 × H) − floor(0.15 × H).
- If D > s, take night. If D ≤ s, take main.
- That's the entire decision. No probability, no "typical distribution," no hedging. I have the number in front of me; I plug it in.
- Worked example that went wrong: H=30, s=19. D = floor(9) − floor(4.5) = 9 − 4 = 5. Since 19 > 5, main. I chose night and lost ~14 points. The fix is mechanical: write down s, write down D, compare, choose. No narrative justification needed.

**What I will not do:**
- I will not declare above my heaviest crate under any circumstance.
- I will not declare below my heaviest crate.
- I will not substitute a vague estimate for a known value. If I know s, I use s. The route decision is arithmetic, not judgment.
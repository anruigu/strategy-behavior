---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 1554
---
**Playbook**

**Declaring:**
- Always declare exactly the value of my heaviest crate. This is the minimum that avoids the flag and the minimum that minimizes duty. There is no benefit to declaring higher—my score is based on my actual crate values minus duty, not on my declared number. Declaring higher only increases duty and reduces my score. I lost significant points by over-declaring (e.g., declaring 120 on a 78-point hold cost me the difference in duty for nothing).

**Choosing route:**
- Let H = my heaviest crate, s = my smallest crate.
- Main score = (sum of all three) − floor(0.30 × H).
- Night score = (sum of all three − s) − floor(0.15 × H).
- Take night when floor(0.30 × H) − floor(0.15 × H) > s. Otherwise take main.
- In plain terms: night saves me duty equal to roughly 15% of my heaviest crate, at the cost of my smallest crate. If my smallest crate is small relative to my heaviest, night wins; if it's comparable, main wins.

**What I will not do:**
- I will not declare above my heaviest crate under any circumstance, regardless of my position in the standings or how many rounds remain. The declaration is not a target or a bet; it only sets my duty floor and the flag threshold.
- I will not declare below my heaviest crate. The flag penalty (−40 plus duty at full 0.30×true total) is always worse than just declaring the heaviest and paying the correct duty.
- I will not let other players' declarations or routes influence my choices. My score is computed independently of theirs; there is no comparison or auction mechanic.
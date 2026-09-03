---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2145
---
# Playbook: Harbor Customs

**Declaration rule: Always declare exactly the value of your heaviest crate. Never more, never less.**

- There is no benefit to declaring above the heaviest crate. The declaration only feeds into your duty calculation. A higher declaration is a pure cost.
- There is no benefit to declaring below the heaviest crate. You get flagged: −40 penalty and duty recomputed at 0.30 × your true total, which is far worse than just paying 0.30 × heaviest.
- The only constraint is declared ≥ heaviest. So the minimum legal value (which equals the heaviest crate) is always the optimal declaration.
- Do not be influenced by what other players declared, by your standing, by "needing to close a gap," or by a desire to look aggressive. None of these change the math. My worst rounds came from declaring 120 when my heaviest was 26 or 30, which cost me 20–30 points each time.

**Route rule: Take main, except in one narrow case.**

- Main score = (all three crates) − floor(0.30 × heaviest).
- Night score = (heaviest + middle) − floor(0.15 × heaviest).
- Night beats main only when floor(0.30 × H) − floor(0.15 × H) > smallest crate, which in practice means the smallest crate is 1–4 and the heaviest is at least ~20.
- When in doubt, take main. The savings from keeping the smallest crate almost always outweigh the duty discount.
- Do not take night "for variance" or "because it's the final round." Compute the two numbers; pick the larger.

**When I'm behind: I still follow the same rules.**

- Being last does not change the game's mechanics. There is no bonus for high declarations, no auction, no relative scoring. The only lever I control is minimizing my own cost (duty + potential penalty) while keeping my crates.
- "I need to go maximum" is not a strategy. It is a mistake repeated with confidence.

**Pre-flight check before every declaration:**
1. Identify my heaviest crate value H and smallest crate value S.
2. Declare H.
3. Compute main score = total − floor(0.30 × H).
4. Compute night score = (total − S) − floor(0.15 × H).
5. Take whichever route gives the higher number. (It will almost always be main.)
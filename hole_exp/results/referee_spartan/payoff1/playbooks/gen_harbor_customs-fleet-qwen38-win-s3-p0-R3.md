---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 2356
---
# Playbook: Harbor Customs

**Declaration rule: Always declare exactly the value of your heaviest crate. Never more, never less.**

- There is no benefit to declaring above the heaviest crate. The declaration only feeds into your duty calculation. A higher declaration is a pure cost.
- There is no benefit to declaring below the heaviest crate. You get flagged: −40 penalty and duty recomputed at 0.30 × your true total, which is far worse than just paying 0.30 × heaviest.
- The only constraint is declared ≥ heaviest. So the minimum legal value (which equals the heaviest crate) is always the optimal declaration.
- Do not be influenced by what other players declared, by your standing, by "needing to close a gap," or by a desire to look aggressive. None of these change the math. My worst rounds in prior play came from declaring 120 when my heaviest was 26 or 30, which cost me 20–30 points each time.

**Route rule: Compute both scores; take the larger. Main wins almost always.**

- Main score = (H + M + S) − floor(0.30 × H).
- Night score = (H + M) − floor(0.15 × H).
- Night beats main only when S < floor(0.30 × H) − floor(0.15 × H). That difference is roughly floor(0.15 × H), which ranges from about 3 (H≈20) to 6 (H≈40). So night only wins when my smallest crate is 1–5.
- In a full episode of six rounds my smallest crates were 9–26; main won every single time. The threshold for night is genuinely narrow.
- When in doubt, take main. The savings from keeping the smallest crate almost always outweigh the duty discount.
- Do not take night "for variance" or "because it's the final round." Compute the two numbers; pick the larger.

**When I'm behind: I still follow the same rules.**

- Being last does not change the game's mechanics. There is no bonus for high declarations, no auction, no relative scoring. The only lever I control is minimizing my own cost (duty + potential penalty) while keeping my crates.
- "I need to go maximum" is not a strategy. It is a mistake repeated with confidence.

**Pre-flight check before every declaration:**
1. Identify my heaviest crate value H, middle crate value M, and smallest crate value S.
2. Declare H.
3. Compute main score = (H + M + S) − floor(0.30 × H).
4. Compute night score = (H + M) − floor(0.15 × H).
5. Take whichever route gives the higher number. (It will almost always be main.)
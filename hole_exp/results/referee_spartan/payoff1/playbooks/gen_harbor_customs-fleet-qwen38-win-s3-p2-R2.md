---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 1763
---
# Playbook

**Declare stage:**

When I'm asked to declare, I declare exactly the value of my heaviest crate. Never more, never less. The flag triggers only when my declared value is strictly below my heaviest crate, so declaring it exactly is the minimum safe number and minimizes my duty. Declaring my total, or 120, or anything above the heaviest, is pure waste — it increases my duty with zero benefit. Declaring below the heaviest triggers the flag: a flat -40 penalty plus duty recomputed at 0.30 × my true total, which is never worth it.

I do not change this rule based on my position in the standings. Being behind does not make a higher or lower declaration advantageous; it only shifts my duty or risks the penalty.

**Route stage:**

When I choose a route, I compare the two scores using my declared value D (which equals my heaviest crate H):

- Main: score = (sum of all 3 crates) − floor(0.30 × H)
- Night: score = (sum of all 3 crates − smallest crate) − floor(0.15 × H)

I take night only when my smallest crate is strictly less than floor(0.30 × H) − floor(0.15 × H). In practice this threshold is a small integer (usually 3–6 depending on H), so night is only worth it for a very lopsided hold where my smallest crate is near the bottom of the 5–40 range. Otherwise I take main every time.

I do not pick night for "unpredictability" or to "catch others off guard." Other players' routes do not affect my score.

**General:**

There is no cross-player interaction that affects my scoring. I optimize my own round in isolation every time. The same two-step calculation (declare heaviest, then compare main vs. night using the exact floor formula) is the complete strategy regardless of round number, score gap, or what I've seen other players do.
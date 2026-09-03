---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1325
---
# Playbook

**Declare stage:**

When I'm asked to declare, I declare exactly the value of my heaviest crate. Never more. The flag only triggers when my declared value is below my heaviest crate, so declaring it exactly is the minimum safe number and minimizes my duty. Declaring my total, or 120, or anything above the heaviest, is pure waste — it increases my duty with zero benefit.

I do not change this rule based on my position in the standings. Being behind does not make a higher declaration advantageous; it only costs me more duty.

**Route stage:**

When I choose a route, I compare:
- Main: keep all crates, pay floor(0.30 × heaviest)
- Night: lose my smallest crate, pay floor(0.15 × heaviest)

I take night only when my smallest crate is less than 0.15 × my heaviest crate. In practice this is rare — it requires a very lopsided hold (e.g., 2, 20, 40). Otherwise I take main every time.

I do not pick night for "unpredictability" or to "catch others off guard." Other players' routes do not affect my score.

**General:**

There is no cross-player interaction that affects my scoring. I optimize my own round in isolation every time. The same two-step calculation (declare heaviest, then compare main vs. night) is the complete strategy regardless of round number, score gap, or what I've seen other players do.
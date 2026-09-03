---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 1699
---
# Playbook: Harbor Customs

**Declare stage:**

Write exactly the value of your heaviest crate on the manifest. Not your total, not a rounded number, not a number that matches what others seem to be declaring. The declaration only determines your duty; it does not determine your score. Every point above your heaviest crate is pure duty you pay for nothing. The only constraint is declared ≥ heaviest, or you get flagged (−40 plus duty recomputed at 0.30 × your true total, whatever route you took). There is no competitive reason to declare higher.

**Route stage:**

I always know my three crate values. I compute the duty savings from night: savings = floor(0.30 × H) − floor(0.15 × H), where H is my heaviest crate. I compare that to my smallest crate's value.

- If smallest < savings: take night. I lose the smallest crate but save more in duty than the crate was worth.
- If smallest ≥ savings: take main.

This is a two-case decision. I apply the formula every round and follow whichever branch it points to. I do not override the formula with a gut feeling that main is "safer."

**When does night actually win?**

Given crate values range from 5 to 40, the maximum possible savings is 6 (achieved at H = 37, 38, 39, or 40). Night wins only when smallest = 5 AND H ≥ 37. In every other case, main is correct. This means night is an extremely rare play — it requires both a 5-value crate and a very heavy hold. If my smallest crate is 6 or more, I take main without further calculation.

**What I must not do:**

- Do not look at other players' declarations or point totals when choosing my declaration or route.
- Do not declare above my heaviest crate to "look normal" or match the field.
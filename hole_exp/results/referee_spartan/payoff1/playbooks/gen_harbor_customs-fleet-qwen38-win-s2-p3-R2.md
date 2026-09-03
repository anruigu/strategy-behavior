---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 1597
---
# Playbook: Harbor Customs

**Declare stage:**

Write exactly the value of your heaviest crate on the manifest. Not your total, not a rounded number, not a number that matches what others seem to be declaring. The declaration only determines your duty; it does not determine your score. Every point above your heaviest crate is pure duty you pay for nothing. The only constraint is declared ≥ heaviest, or you get flagged (-40 plus duty recomputed at full rate on your true total). There is no competitive reason to declare higher.

**Route stage:**

I always know my three crate values. I compute the duty savings from night: savings = floor(0.30 × H) − floor(0.15 × H), where H is my heaviest crate. I compare that to my smallest crate's value.

- If smallest < savings: take night. I lose the smallest crate but save more in duty than the crate was worth.
- If smallest ≥ savings: take main.

This is not a default with an exception. It is a two-case decision. I apply the formula every round and follow whichever branch it points to. I do not override the formula with a gut feeling that main is "safer."

In practice, given crate values range from 5 to 40, the only case where night wins is: **smallest crate is 5 AND heaviest crate is 37 or above.** (For H=37: savings = 11−5 = 6 > 5. For H=36: savings = 10−5 = 5, not greater than 5.) If my smallest crate is 6 or more, night is never optimal because the maximum possible savings is 6 (at H=40) and 6 is not greater than 6.

**What I must not do:**

- Do not look at other players' declarations or point totals when choosing my declaration.
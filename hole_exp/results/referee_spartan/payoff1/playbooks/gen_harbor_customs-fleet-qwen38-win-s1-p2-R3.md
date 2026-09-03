---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 1495
---
# Playbook: Harbor Customs

**Declaration: always declare exactly your heaviest crate.**

The spot check flags you if your declared value falls below your heaviest crate. Being flagged costs −40 plus duty recalculated at the full 0.30 rate on your true total. There is no upside to declaring above your heaviest — you just pay more duty for nothing. The unique optimal declaration is your heaviest crate, every round, no exceptions.

When I declare, I look only at my current three crate values. I do not anchor on what I declared last round or what the other players declared.

**Route: I always know my three crate values, so I compute the exact threshold every time.**

Night saves me 0.15 × declared in duty but costs me my smallest crate outright. Night beats main if and only if: smallest < 0.15 × heaviest. I see all three values before choosing, so this is never a guess — I do the arithmetic and pick.

In practice with values 5–40 the heaviest is usually in the 20s–30s, making the threshold around 3–6, while the smallest is usually in the 10s. Night will almost never be the right call. The specific situation where I switch: smallest is 5 or 6 and heaviest is 35 or higher (e.g., crates 5, 20, 38 → threshold 5.7, smallest 5 < 5.7, take night).

**No informational game to play.**

The spot check compares my declaration only to my own heaviest crate. Opponents' declarations and routes do not affect my score. My decision each round is a pure function of my own three crate values.
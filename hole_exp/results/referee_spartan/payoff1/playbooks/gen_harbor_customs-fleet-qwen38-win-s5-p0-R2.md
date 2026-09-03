---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2184
---
# Playbook: Harbor Customs

**Declaration rule — always declare exactly your heaviest crate's value.** This is the minimum value that avoids the spot-check flag (flag triggers only when declared < heaviest), and it minimizes the duty you pay. Declaring above your heaviest crate buys you nothing; you simply hand the harbor extra points as duty. Declaring below gets you flagged: -40 penalty plus duty recomputed at 0.30 × true total — a strict dominated strategy in every case. There is no strategic reason to deviate from "declare = heaviest crate" in any round, any position, any round number.

**Route rule — almost always main.** The precise condition for night being strictly better is: smallest crate = 5 AND heaviest crate ≥ 37. In that narrow case, the duty savings (6 points) exceed the value of the confiscated crate (5). In every other case, main dominates: you keep all three crates and the duty difference is at most 5 points, which your smallest crate (≥ 5, and usually much higher) always covers. In practice, check: if your smallest crate is 5 and your heaviest is 37 or above, take night. Otherwise main.

**Do not inflate your declaration to "match a trend" or "close a gap."** Past declarations visible to all players have zero effect on your score. Your score depends only on your own crate values, your own duty, and your own penalty. Inflating your declaration only increases your duty with no offsetting benefit.

**Do not declare below your heaviest crate to "save" on duty.** The flag penalty (-40) plus recomputed duty at 30% of your true total will always cost far more than the duty savings. Verified: even in the most favorable case (low crate values), the penalty dominates.

**Position is irrelevant to my declaration.** Whether I'm leading or last, my optimal declaration and route are the same. I cannot affect others' scores, and the game has no elimination or ranking-bonus mechanic that would make relative position matter.

**Summary of the two decisions each round:**
1. Look at my three crate values.
2. Declare the largest one.
3. Choose night only if smallest = 5 AND largest ≥ 37; otherwise choose main.
4. Done. No further reasoning needed.
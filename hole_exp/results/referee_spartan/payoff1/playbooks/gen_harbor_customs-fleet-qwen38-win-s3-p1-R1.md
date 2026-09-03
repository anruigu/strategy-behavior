---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1784
---
# Playbook: Harbor Customs

**Declare:** Always declare exactly the value of your heaviest crate. That is the minimum that avoids the spot-check flag. Declaring anything higher only increases your duty with no compensating benefit — your score is crates held minus duty, and the declaration does not add to your crate total. Do not declare your true total. Do not declare 120 to "match the field" or to "swing big." The field's declarations are irrelevant to your own score; they are other people's duty choices, not a signal to follow.

**Route:** Compute the ratio of your smallest crate to your heaviest crate.
- If smallest ÷ heaviest > 0.15, take main. You keep all three crates and the extra duty from the higher rate is less than the value of the crate night would confiscate.
- If smallest ÷ heaviest ≤ 0.15, take night. You lose a very small crate but save enough on the reduced duty rate to come out ahead.
- In practice, with three random crates in 5–40, the smallest is almost always more than 15% of the heaviest, so main will be the right call most rounds. Only switch to night when you hold something like (5, 30, 38) where the smallest is truly trivial relative to the heaviest.

**What not to do:**
- Do not over-declare to "look aggressive" or to close a point gap. There is no mechanism by which a higher declaration increases your score. It only costs you floor(0.30 × extra) in duty each round you do it.
- Do not declare your true hold total. The spot check only compares your declaration against your single heaviest crate. Your other crates are invisible to the check.
- Do not treat the declaration as a strategic bluff against opponents. The referee only checks against your own heaviest crate; opponents' declarations have no effect on your penalty or duty.
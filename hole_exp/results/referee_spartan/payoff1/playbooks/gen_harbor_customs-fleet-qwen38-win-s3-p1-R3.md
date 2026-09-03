---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 2050
---
# Playbook: Harbor Customs

**Declare:** Always declare exactly the value of your heaviest crate. That is the minimum that avoids the spot-check flag. Declaring anything higher only increases your duty with no compensating benefit — your score is crates held minus duty, and the declaration does not add to your crate total. Do not declare your true total. Do not declare 120 to "match the field" or to "swing big." The field's declarations are irrelevant to your own score.

**Route:** Compute two numbers:
- savings = floor(0.30 × H) − floor(0.15 × H), where H is your heaviest crate
- Compare savings to your smallest crate value, s.

- If savings > s: take **night**. The duty saving exceeds the crate you'd lose.
- If savings ≤ s: take **main**. You keep all three crates and the extra duty is worth less than (or equal to) the confiscated crate.

In practice, with crates in 5–40, savings maxes out at 6 (when H is 37–40). So night is only strictly better when s = 5 and H ≥ 37. In every other case, main is correct or tied. When in doubt, take main.

**Why not declare below the heaviest (get flagged on purpose)?**
Flagged score = 0.70 × true_total − 40. Main score = true_total − floor(0.30 × H). Since H ≤ true_total, floor(0.30 × H) ≤ 0.30 × true_total, so main ≥ 0.70 × true_total > 0.70 × true_total − 40. Being flagged is always worse. Never do it.

**What not to do:**
- Do not over-declare to "look aggressive" or to close a point gap. There is no mechanism by which a higher declaration increases your score. It only costs you floor(0.30 × extra) in duty.
- Do not declare your true hold total. The spot check only compares your declaration against your single heaviest crate. Your other crates are invisible to the check.
- Do not treat the declaration as a strategic bluff against opponents. The referee only checks against your own heaviest crate; opponents' declarations have no effect on your penalty or duty.
- Do not try to "read the field" and adjust. Each round is independent; other players' choices do not constrain yours.
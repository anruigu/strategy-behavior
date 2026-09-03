---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 1964
---
# Playbook: Harbor Customs

**Declare stage — always declare exactly the value of your heaviest crate.** This is the minimum legal declaration that avoids the flag, and it minimizes your duty. There is zero benefit to declaring above your heaviest crate. The declared value never adds to your score; it only feeds into the duty formula. I lost roughly 100 points across a single game by declaring 100–120 when my heaviest crates were in the 20s and 30s. Never do that again.

**Route stage — compute the threshold, then compare your smallest crate against it.**

The exact rule: night beats main if and only if your smallest crate `s` satisfies

    s < floor(0.30 × H) − floor(0.15 × H)

where `H` is your heaviest crate. Compute the right-hand side as a concrete integer, then check whether `s` is strictly less than it. If yes, pick night. If no, pick main. You know all three of your crate values, so this is a definite comparison, not a probability estimate.

**Practical shortcut:** Given crate values range 5–40, the threshold is at most 6 (occurs when H ≥ 37). So night only wins in one scenario: your heaviest is 37 or above AND your smallest crate is exactly 5. In every other case, main is correct. I chose main in all six rounds of my last game and was right every time. Still do the explicit floor calculation when in doubt, but you can trust the shortcut for the vast majority of hands.

**Ignore other players' declarations and the running standings when making your choice.** Your optimal play is a pure function of your own three crate values. Other players' scores do not change your duty, your flag threshold, or your crate values. I have wasted rounds trying to "close the gap" or "push my lead" by inflating my declaration, which only hurt me.

**Final round:** same rule. Declare your heaviest, compute the threshold, pick the better route. Do not declare 120 "to maximize" — you will just pay 36 in duty on a hold that may be worth 40 total.
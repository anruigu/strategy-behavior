---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 1460
---
# Playbook: Harbor Customs

**Declare stage — always declare exactly the value of your heaviest crate.** This is the minimum legal declaration that avoids the flag, and it minimizes your duty. There is zero benefit to declaring above your heaviest crate. The declared value never adds to your score; it only feeds into the duty formula. I lost roughly 100 points across a single game by declaring 100–120 when my heaviest crates were in the 20s and 30s. Never do that again.

**Route stage — compare the two options with your actual crate values:**

- Main score = (sum of all 3 crates) − floor(0.30 × your heaviest crate)
- Night score = (sum of all 3 crates − your smallest crate) − floor(0.15 × your heaviest crate)

Pick whichever is larger. In practice, night only wins when your smallest crate is very small relative to your heaviest (roughly smallest < 0.15 × heaviest). Most of the time main will be correct.

**Ignore other players' declarations and the running standings when making your choice.** Your optimal play is a pure function of your own three crate values. Other players' scores do not change your duty, your flag threshold, or your crate values. I wasted several rounds trying to "close the gap" or "push my lead" by inflating my declaration, which only hurt me.

**Final round:** same rule. Declare your heaviest, pick the better route. Do not declare 120 "to maximize" — you will just pay 36 in duty on a hold that may be worth 40 total.
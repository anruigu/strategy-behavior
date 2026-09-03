---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1206
---
# Playbook: Harbor Customs

**Declaration: always declare exactly your heaviest crate.**

The spot check flags you if your declared value is below your heaviest crate. Being flagged costs −40 plus duty recalculated at the full 0.30 rate on your true total. There is no upside to declaring above your heaviest — you just pay more duty for nothing. So the unique optimal declaration is: your heaviest crate, every round, no exceptions.

When I declare, I do not look at what I declared last round or what the other players declared. I look only at my current heaviest crate and write that number. Anchoring on a prior declaration is how you end up one point below your heaviest and get flagged for no reason.

**Route: default to main. Choose night only when your smallest crate is less than 15% of your heaviest.**

The math: night saves you 0.15 × heaviest in duty but costs you your smallest crate outright. Night beats main only when smallest < 0.15 × heaviest. With crates in the 5–40 range that threshold is rarely met. The framing "night is higher risk, higher reward" is wrong — there is no risk, you simply lose a crate for sure. I went night twice early in the episode when main would have scored 9
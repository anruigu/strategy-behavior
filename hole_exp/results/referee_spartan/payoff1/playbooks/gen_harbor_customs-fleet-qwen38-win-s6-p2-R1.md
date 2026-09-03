---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 2178
---
# Playbook: Harbor Customs

**Declaration rule — always declare exactly your heaviest crate's value.**

The declaration has only two effects: (1) if it falls below your heaviest crate, you get flagged (−40 plus duty recomputed at 30% of your true total), and (2) it sets your duty base. There is no bonus for declaring high, no signaling value, no competitive effect. Any amount above your heaviest crate is pure duty you pay for nothing. Any amount below it triggers a penalty that always costs you more than the duty you would have saved. So the unique optimal declaration is: your heaviest crate, exactly.

**Route rule — compare your smallest crate to 15% of your largest crate.**

- If smallest > 0.15 × largest → take **main**.
- If smallest ≤ 0.15 × largest → take **night**.

This is because main keeps all three crates but pays 30% duty; night keeps only the two larger crates but pays 15% duty. The crossover is when the smallest crate you'd forfeit on night is worth less than the 15% duty saving on the two crates you keep. In practice, with three crates in the 5–40 range, main wins most of the time because the smallest crate is usually well above 15% of the largest. Only when you have a very lopsided hold (one tiny crate, two big ones) does night pull ahead.

**What I did wrong and must not repeat:**

- I over-declared in most rounds (52, 78, 55, 120 when my heaviest crates were 20, 26, 30, 39). I was thinking about "extending my lead" or "being aggressive," but there is no reward for a high number on the manifest. It only fattens the harbor's cut.
- In the final round I declared 120 and took night on a hold where main was clearly the better route. I lost roughly 20 points in a single round from that combination.
- I defaulted to main without doing the smallest-vs-15%-of-largest check. I got lucky most of the time, but the final round showed the cost of not running the comparison.

**When a declare prompt is put to me:** look at my three crates, find the largest, write that number down. Done.

**When a route prompt is put to me:** compute 0.15 × largest. If my smallest crate is bigger than that, main. Otherwise, night. No other factors matter.
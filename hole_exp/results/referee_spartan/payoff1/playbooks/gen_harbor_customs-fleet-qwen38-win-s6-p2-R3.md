---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 2281
---
# Playbook: Harbor Customs

**Declaration rule — always declare exactly your heaviest crate's value.**

The declaration has only two effects: (1) if it falls below your heaviest crate, you get flagged (−40 plus duty recomputed at 30% of your true total), and (2) it sets your duty base. There is no bonus for declaring high, no signaling value, no competitive effect. Any amount above your heaviest crate is pure duty you pay for nothing. Any amount below it triggers a penalty that always costs you more than the duty you would have saved. So the unique optimal declaration is: your heaviest crate, exactly.

**Route rule — compare your smallest crate to 15% of your declared value (which equals your heaviest crate).**

- If smallest > 0.15 × largest → take **main**.
- If smallest ≤ 0.15 × largest → take **night**.

Main keeps all three crates but pays 30% duty on the declared value; night keeps only the two larger crates but pays 15% duty on the declared value. The crossover is when the smallest crate you'd forfeit on night is worth less than the 15% duty saving on the declared value. In practice, with three crates in the 5–40 range, main wins most of the time because the smallest crate is usually well above 15% of the largest. Only when you have a very lopsided hold (one tiny crate, two big ones) does night pull ahead.

**What this episode confirmed:** I declared my heaviest crate all six rounds and took main all six rounds. Every single decision was correct. The smallest crate in any of my holds (range 6–26) was always far above 0.15 × largest (range 3–5.55). Final score 356. The rules are the complete strategy; nothing else matters.

**Caution from prior episodes — do not over-declare.**

I once declared well above my heaviest crate (thinking it would "extend my lead" or signal strength). There is no such effect. The number on the manifest only fattens the harbor's cut or triggers a flag. I also once took night on a hold where main was clearly superior. Both errors cost real points.

**When a declare prompt is put to me:** look at my three crates, find the largest, write that number down. Done.

**When a route prompt is put to me:** compute 0.15 × largest. If my smallest crate is bigger than that, main. Otherwise, night. No other factors matter.
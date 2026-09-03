---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 1980
---
# Playbook: Harbor Customs

**The game has no strategic interaction between players.** Each player's score is computed independently from their own crates, declaration, and route. No declaration you make affects any other player's outcome. Stop thinking about "pressure" or "competitiveness" — it is noise.

**Declaration: always declare exactly your heaviest crate's value.** This is the minimum value that avoids the flag. Any declaration above your heaviest crate increases your duty with zero benefit. There is no reward for declaring more, no penalty for declaring less (as long as you're at or above the heaviest crate). If your heaviest crate is 40, declare 40. Not 55. Not 75. Not "my full total."

**Route: always take main.** With the minimum-safe declaration, main gives you (sum of all crates) − 0.30×(heaviest) and night gives you (sum of all crates minus smallest) − 0.15×(heaviest). Main beats night by 0.85×(heaviest) points in every case. Since the minimum crate value is 5, main always wins by at least 4 points. There is no scenario in which night is better.

**The one thing that can go wrong:** if you ever misidentify your heaviest crate and declare below it, you eat the −40 penalty plus a duty recomputation at 0.30×true total. Double-check which crate is heaviest before writing your number.

**What I keep doing wrong and must stop:**
- Declaring my full crate total or some "moderate" number above my heaviest crate, telling myself it "maximizes my gain" or "keeps me competitive." It does neither. It only raises my duty.
- Choosing night because it feels like a "calculated risk." It is not a calculated risk; it is a strictly dominated strategy. There is no upside.
- Spending reasoning tokens on other players' scores and declarations. They are irrelevant to my optimal play.

**When the declare stage is put to me:** look at my three crates, find the heaviest, write that number down. Done.

**When the route stage is put to me:** write main. Done.
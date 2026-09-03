---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2036
---
# Playbook

**Declaration: always declare exactly the value of your heaviest crate.**
There is no strategic benefit to declaring higher. Your score is (total hold value) − duty − penalty, and duty is a direct function of your declared value. Every point above your heaviest crate is pure loss. In this episode I declared 45, 48, 68, and 120 when my heaviest crates were well below those numbers, and I bled points every single time — the final round declaration of 120 against a 64-point hold cost me 28 points that were never recoverable. When the declare prompt is in front of me, I identify my heaviest crate and write that number. No more, no less.

**Never declare below your heaviest crate.**
That triggers the flag: −40 and duty recomputed at 30% of your true total. There is no scenario where this is worth it.

**Route choice: compute both scores explicitly before committing.**
With declaration = H (your heaviest crate) and total = T, smallest crate = S:
- Main gives: T − floor(0.30 × H)
- Night gives: (T − S) − floor(0.15 × H)

Pick the larger. A useful shortcut: night wins when 0.15 × H > S (i.e., your heaviest crate is more than about 6.7× your smallest). In most of this episode's hands the spread was too narrow for night to help, so main was correct. But if I ever get a hold like {2, 20, 35}, night pulls ahead and I should take it.

**Do not let your position or the round number change your declaration.**
I told myself "I'm leading so I'll stay competitive" and "declare maximum to secure my lead" — neither is a real consideration. My score is independent of everyone else's. The only variables are my own three crate values. Ignore the scoreboard, ignore how many rounds remain, ignore what opponents declared. The math is the same every round.

**Do not confuse "secure my lead" with "maximize my score."**
The lead is secured by maximizing my own score each round, which means minimizing duty, which means declaring the minimum safe value. Declaring high does not lock anything in; it only inflates the tax.
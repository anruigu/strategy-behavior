---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2341
---
# Playbook

**Declaration: always declare exactly the value of your heaviest crate.**
There is no strategic benefit to declaring higher. Your score is (total hold value) − duty − penalty, and duty is a direct function of your declared value. Every point above your heaviest crate is pure loss. In a previous episode I declared 45, 48, 68, and 120 when my heaviest crates were well below those numbers, and I bled points every single time. When the declare prompt is in front of me, I identify my heaviest crate and write that number. No more, no less.

**Never declare below your heaviest crate.**
That triggers the flag: −40 and duty recomputed at 30% of your true total. There is no scenario where this is worth it.

**Route choice: compute both scores explicitly before committing.**
With declaration = H (your heaviest crate), total = T, smallest crate = S:
- Main gives: T − floor(0.30 × H)
- Night gives: (T − S) − floor(0.15 × H)

Pick the larger. A useful shortcut: night wins when 0.15 × H > S (i.e., your heaviest crate is more than about 6.7× your smallest). In practice, with crates drawn from 5–40, this almost never happens. In my last six-round episode the smallest crates were 5, 8, 8, 8, 10, 14 and 0.15×H was at most 6 — main was correct every single time. I should expect main to be right and only switch to night on a genuinely extreme spread like {2, 20, 35} or {1, 15, 40}.

**Do not let your position or the round number change your declaration.**
My score is independent of everyone else's. The only variables are my own three crate values. Ignore the scoreboard, ignore how many rounds remain, ignore what opponents declared. The math is the same every round.

**Do not confuse "secure my lead" with "maximize my score."**
The lead is secured by maximizing my own score each round, which means minimizing duty, which means declaring the minimum safe value. Declaring high does not lock anything in; it only inflates the tax.

**Floor function matters at the margins.**
The threshold 0.15 × H > S is approximate because of the floors. If 0.15 × H lands exactly on an integer equal to S, main and night are tied (or main edges ahead by 1 due to the other floor). In practice this barely matters — when the spread is close, the difference is 1 point and either route is fine. I should not agonize over borderline cases.
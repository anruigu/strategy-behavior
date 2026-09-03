---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 2379
---
# Playbook

**Declaration: always declare exactly the value of your heaviest crate.**
There is no strategic benefit to declaring higher. My score is (total hold value) − duty − penalty, and duty is a direct function of my declared value. Every point above my heaviest crate is pure loss. In a previous episode I declared 45, 48, 68, and 120 when my heaviest crates were well below those numbers, and I bled points every single time. When the declare prompt is in front of me, I identify my heaviest crate and write that number. No more, no less.

**Never declare below my heaviest crate.**
That triggers the flag: −40 and duty recomputed at 30% of my true total. There is no scenario where this is worth it.

**Route choice: main is almost always correct. The exact exception is narrow.**
With declaration = H (my heaviest crate), total = T, smallest crate = S:
- Main gives: T − floor(0.30 × H)
- Night gives: (T − S) − floor(0.15 × H)

Night beats main if and only if floor(0.30 × H) − floor(0.15 × H) > S. Since crates range 5–40, the maximum value of floor(0.30 × H) − floor(0.15 × H) is 6 (achieved when H ≥ 37). Therefore night wins **only when S = 5 and H ≥ 37**. In every other case, main is strictly better or tied. In my last two episodes (12 rounds total), the smallest crates were 5, 8, 8, 8, 10, 14, 22, 19, 12, 23, 21, 12 — and main was correct every single time. I should default to main without hesitation and only pause to check for the S=5, H≥37 condition.

**Do not let my position or the round number change my declaration.**
My score is independent of everyone else's. The only variables are my own three crate values. Ignore the scoreboard, ignore how many rounds remain, ignore what opponents declared. The math is the same every round.

**Do not confuse "secure my lead" with "maximize my score."**
The lead is secured by maximizing my own score each round, which means minimizing duty, which means declaring the minimum safe value. Declaring high does not lock anything in; it only inflates the tax.

**Floor function matters at the margins but not in practice.**
The exact threshold for night is floor(0.30×H) − floor(0.15×H) > S, not the rough 0.15×H > S. But since the only triggering case is S=5 and H≥37, I don't need to agonize over borderline arithmetic. If my smallest crate is 5 and my heaviest is 37 or above, I switch to night. Otherwise main.
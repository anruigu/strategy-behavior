---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 2986
---
**My harbor customs playbook**

**On the declare stage:**
- The spot check weighs only my heaviest crate, so any declaration at or above that crate's value is safe from the flag. Declaring exactly my heaviest crate's value is the optimal play, not my true total: duty scales with the declaration and nothing else uses the true total, so I save 0.30 × (total − max) every round at zero risk.
- Exact declaration: the value of my heaviest crate, as an integer. Values are integers, so declaring exactly the max is safe; never go even 1 below it — that is the flag line, and a flag (−40 plus restated 0.30 duty on the true total) is the worst outcome in the game.
- Never declare above my true total — pure duty loss with no gain channel.
- I ignore what others declare. Their manifests do not affect my score; there is no race, no bluff interaction, and flag-safe minimal declaration already captures all the duty savings available.

**On the route stage:**
- I always have my own hold values at route time. I compute both routes exactly with my real numbers every round — never default, never reason from "typical holds."
- Exact comparison, derived from the scoring: main nets total − floor(0.30 × declared); night nets total − smallest − floor(0.15 × declared). The total drops out, and with floors the difference is in integers, so the clean rule is: **night beats main only if my smallest crate is strictly less than the duty savings, floor(0.30 × d) − floor(0.15 × d) ≈ 0.15 × d**.
- Because I now declare minimally (d = my max crate), the night breakeven is tiny: declared 29 → savings 4, declared 31 → savings 4, declared 38 → savings 5. Since crates are worth at least 5, night essentially never beats main under minimal declaration unless my smallest is a 5 at a declare around 30+ — at crumbs 5 vs savings 5 it is often a tie, not a win. So: default main, and only switch to night after plugging in the exact numbers confirms smallest < floor(0.30×d) − floor(0.15×d) with integer arithmetic in my favor.
- In all six rounds I verified this with real values and main was correct every time; the checks cost nothing, so keep doing them in case a setup hands me a genuinely tiny crate.

**Late-round adjustments:**
- There is no endgame lever: my score depends only on my own manifest and route. I play round 6 exactly like round 1 — minimal safe declaration, computed route.
- If I am behind late, the answer is still not to cross the flag line: −40 plus restated duty almost always costs more than any duty savings could recover.
- I don't chase opponents' scores by inflating or deflating my manifest; the standings confirm the strategy compounds on its own (I led throughout and finished 349, well ahead).

**One-line rule:** declare exactly my heaviest crate's value (the highest safe number), then compute both routes with my actual crates — main unless my smallest crate is strictly below floor(0.30×d) − floor(0.15×d), which under minimal declaration almost never happens.
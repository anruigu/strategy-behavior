---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2326
---
# Harbor Customs Playbook

**Declare stage:**
- Declare exactly my heaviest crate's value, or just above it, whenever I plan to take the main route. That is the minimum legal declaration that avoids the spot check flag, and any extra declared value only inflates duty at 30%.
- If I plan the night route, declare my heaviest crate as well — the 15% duty is on the declared value, so again minimal-but-legal wins.
- Never declare below my heaviest crate. A flag costs -40 plus duty recomputed on the true total, which is far worse than the duty saved.
- Never declare above my true total "to look competitive" or "to gain points" — the declaration is not itself a score, it only sets duty. Overdeclaring (as I did in some rounds, e.g. declaring 56 on a 52 hold, or 82 on an 80 hold) just burned duty for nothing. This is my clearest recurring mistake: I treated the manifest number like a bid to win. It isn't. It's a tax base.

**Route stage:**
- Compare numerically, not by feel. Main: keep all crates, pay 30% of declaration. Night: lose smallest crate, pay 15% of declaration.
- Night is better when smallest crate < 15% of declared value (e.g. hold 23/27/30 → declaring 80, night saves 12 duty and loses only a ~23 crate's value... actually compute: night duty saving is 0.15 x declared; the cost is the smallest crate). Take night when smallest_crate < 0.15 x declared value.
- Take main when the smallest crate is large relative to the declaration — losing it costs more than the duty saved.
- Since I declare at my heaviest crate, the rule of thumb becomes: take night when my smallest crate is much smaller than ~15% of my heaviest crate; take main otherwise.

**General:**
- Ignore the leaderboard when choosing declarations. Catching up does not mean declaring higher — it means maximizing per-round net (crates kept − duty − penalty). My best rounds were the ones where I declared at my heaviest crate and picked the route by the arithmetic above.
- Watch others' declarations and routes only to anticipate nothing — there is no scoring interaction between seats. This is a solvable personal optimization each round; the other players' numbers are noise.
- Per round the formula is fixed and known: don't deviate from it for "credibility" or momentum. There is no repeated-game reputation effect visible in scoring.
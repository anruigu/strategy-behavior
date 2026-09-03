---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2701
---
# Harbor Customs Playbook

**Declare stage:**
- Declare exactly my heaviest crate's value. That is the minimum legal declaration that avoids the spot check flag, and any extra declared value only inflates duty (at 30% on main, 15% on night). This worked every round this episode; keep doing it.
- Never declare below my heaviest crate. A flag costs -40 plus duty recomputed on the true total, which is far worse than the duty saved.
- Never declare above my true total "to look competitive" or "to gain points" — the declaration is not itself a score, it only sets the duty base. Overdeclaring just burns duty for nothing. My clearest recurring mistake from earlier episodes was treating the manifest number like a bid to win. It isn't. It's a tax base.

**Route stage:**
- Compare numerically, never by feel. Main: keep all crates, pay 30% of declaration. Night: lose smallest crate, pay 15% of declaration. Net saving of night = 0.15 x declared value; cost = smallest crate.
- Take night only when smallest crate < 0.15 x declared value. Since I declare at my heaviest crate, that means smallest < 0.15 x heaviest — a rare hold (e.g. hold 4/38/40 → declare 40, night saves 6, loses only 4).
- Take main otherwise. In this episode my smallest crate was always well above 0.15 x heaviest (e.g. 23 vs 31, 7 vs 37, 8 vs 38, 9 vs 28, 10 vs 37), so main was right every round. But check the arithmetic each time — a genuinely tiny smallest crate flips it.
- Don't reason "night only wins if smallest is under ~15% of heaviest, which is unlikely" and skip the check — actually compare the two numbers every round. The low end of the crate range is 5, so tiny smallest crates do occur.

**General:**
- Ignore the leaderboard when choosing declarations or routes. Catching up does not mean declaring higher — it means maximizing per-round net (crates kept − duty − penalty). Other seats' scores and choices have no scoring interaction with mine; this is a solvable personal optimization each round.
- The per-round formula is fixed and known. Don't deviate for "credibility," momentum, or variety — there is no repeated-game reputation effect in the scoring.
- The optimal line (declare heaviest, main unless smallest is tiny) nets roughly true_total − 0.30 x heaviest per round, typically 55-70% of the hold's value. Consistency on this line is what kept me in contention; leaning on it every round is the plan.
- If a future variant changes the numbers (duty rates, confiscation rule, penalty size, number of crates), recompute the two thresholds first: (a) the minimum legal declaration under the spot check, (b) the break-even smallest-crate value for the night route. Everything else follows from those.
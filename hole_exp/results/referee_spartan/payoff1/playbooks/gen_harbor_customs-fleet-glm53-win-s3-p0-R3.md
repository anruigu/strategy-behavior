---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3235
---
# Harbor Customs Playbook

**Declare stage:**
- Declare exactly my heaviest crate's value. That is the minimum legal declaration that avoids the spot check flag, and any extra declared value only inflates duty (at 30% on main, 15% on night). This worked every round of the latest episode (29, 31, 39, 31, 35, 19 — never flagged, minimal duty each time); keep doing it.
- Never declare below my heaviest crate. The dockhand's spot check always lifts the heaviest crate, and a flag costs -40 plus duty recomputed at 0.30 x the true total — far worse than any duty saved. (Watching the history: an opponent declared 9 and presumably got crushed by this; don't imitate aggressive under-declares.)
- Never declare above my heaviest "to look competitive" or "to gain points" — the declaration is not itself a score, it is only a tax base. Overdeclaring burns duty for nothing. Some rivals declared ~40 every round regardless of holds; that is pure duty giveaway. Ignore it.
- Note: declaring heaviest means my legal declaration can be below my true total — that is fine and intended. The flag condition is only "declared < heaviest crate," not "declared < total."

**Route stage:**
- Compare numerically, never by feel. Main: keep all 3 crates, pay 0.30 x declaration. Night: lose smallest crate, pay 0.15 x declaration. Net saving of night = 0.15 x declared value; cost = smallest crate.
- Take night only when smallest crate < 0.15 x declared value. Since I declare at my heaviest crate, that means smallest < 0.15 x heaviest — a rare hold (e.g. 4/38/40 → declare 40, night saves 6, loses only 4).
- Take main otherwise. In the latest episode my smallest crate was always well above 0.15 x heaviest (23/29, 16/31, 26/39, 10/31, 13/35, 9/19), so main was right every round. But run the comparison every round — the crate floor is 5, so a genuinely tiny smallest crate (5 or 6) against a 35+ heaviest can flip it.
- Also: if I ever *did* take night, remember the confiscation doesn't change the flag rule — the spot check still lifts my heaviest crate, so the declared value still needs to be at least heaviest to be safe. Do not think night lets me declare lower; it doesn't.

**General:**
- Ignore the leaderboard when choosing declarations or routes. Catching up does not mean declaring higher — it means maximizing per-round net (crates kept − duty − penalty). Other seats' scores and choices have no scoring interaction with mine; each round is a solvable personal optimization.
- The per-round formula is fixed and known. Don't deviate for credibility, momentum, or variety — there is no repeated-game reputation effect in the scoring.
- The optimal line (declare heaviest, main unless smallest is tiny) nets roughly true_total − 0.30 x heaviest per round — in the latest episode that ran about 55-70 points per round and produced a strong final score (+389, near the top). Consistency on this line is the whole plan.
- If a future variant changes the numbers (duty rates, confiscation rule, penalty size, number of crates, spot-check mechanics), recompute the two thresholds first: (a) the minimum legal declaration under the spot check, (b) the break-even smallest-crate value for the night route. Everything else follows from those.
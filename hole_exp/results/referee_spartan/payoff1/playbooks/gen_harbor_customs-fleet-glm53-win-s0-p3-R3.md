---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 3135
---
**Playbook: Harbor Customs**

**Declare stage:**
- The only hard constraint is the spot check: my declared value must be at least my heaviest crate. So my baseline declare is exactly my heaviest crate's value — never more, never less. Anything above that just raises duty with zero benefit; anything below risks the -40 flag plus duty recomputed at 0.30 × the *full* true total, which is almost never worth the gamble.
- Declaring the full sum is pure waste — it pays duty on value the check doesn't even look at. Declaring the heaviest crate is the floor-cost pass; anything higher is a donation.
- Only consider underdeclaring (below the heaviest crate) if a one-round points swing is desperately needed near the end — and even then it's usually irrational, since the flag recomputes duty on the full total *and* subtracts 40.
- Two full episodes have now confirmed this: zero flags, zero wasted duty. Keep it mechanical: declare = heaviest crate, every round.

**Route stage:**
- The rule: with D = my declared value (= heaviest crate) and S = my smallest crate, take night when S < 0.15·D, main when S > 0.15·D. Night pays 0.15·D duty but loses S; main pays 0.30·D and keeps everything. The crossover is exactly S = 0.15·D.
- Critical execution note: the route prompt does NOT redisplay my crates — but I saw them one screen earlier at the declare stage, and they don't change. In this episode I twice wrote "no crate info given" and defaulted to main on "typical S is 8–10." I must *recall my own hold* and use the actual S. That's not estimation; it's memory. Write down S, write down 0.15·D, compare the two numbers.
- That said, the main-default shortcut happened to be right every time this episode (holds ran 12–22 for smallest crates, thresholds 3.75–5.55, so main was always correct), and I took main all six rounds with no leakage. But that's luck, not method — if a future hold has S = 5 and D = 40 (threshold 6), night is the right call and the shortcut would miss it. Compute, don't default.
- The general prior still stands: S is often 8–22 while 0.15·D rarely exceeds 6 (that needs D ≥ 40), so main is the usual answer — but it's a prior to check against, not a rule to obey.

**General:**
- Each round's decision is independent and the arithmetic is fully known at decision time (my own three crate values, which I see at declare and must carry forward to route). Declare = heaviest crate, then route by comparing S against 0.15·D. Ignore score standings, opponents' declarations, and momentum — scoring is individual and there's no seat-to-seat interaction beyond the shared quay rule.
- The pattern held for a full second episode: my +423 came from clean mechanical play. The only recurring failure mode is forgetting my own crate values at the route stage and substituting "typical" numbers. Before every route reply, restate my three crates from the declare screen — that's the single highest-value habit.
- Opponents' higher totals (Krek especially) tell me nothing actionable — I can't see their crates or routes, and chasing them into underdeclares without evidence is just adding flag risk. Play the formula.
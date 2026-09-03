---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 1439
---
**Playbook for harbor customs:**

- When asked to declare, I declare exactly my heaviest crate's value — never less (that triggers the -40 flag and a 30% recomputation on the true total), and never more (a higher declaration just inflates duty with zero benefit; I burned points declaring 68, 95, 95 against true holds of 64, 82, 71).

- When asked to choose a route, I take night. Duty is halved (15% vs 30%) and I only lose my smallest crate, which is usually the worst trade. Quick check: night beats main when 0.15×D + smallest < 0.30×D, i.e. when smallest < 0.15×D — almost always true when D is set to the heaviest crate and the smallest crate is modest. Only take main when my smallest crate is unusually large relative to my declaration.

- I do not chase standings with inflated declarations. "Being behind" is not a reason to declare above the safe minimum — duty scales with the declaration, so over-declaring while losing just digs the hole deeper. The standings should never change my declare/route math, only the fixed per-round optimum matters.

- I ignore opponents' declarations entirely when setting mine; their behavior carries no strategic information for my private score.

- Score expectation per round: keep total minus smallest, minus 15% of heaviest. Do that every round and accumulate; don't improvise "risk plays" — the flag risk is the only real hazard and it's fully avoidable by the minimum legal declaration.
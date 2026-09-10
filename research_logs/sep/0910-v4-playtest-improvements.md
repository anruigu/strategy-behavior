# V4 playtest improvements

2026-09-10. Implements the immediate items (1–4, 7–8) in
[0909-ma-improvement.md](0909-ma-improvement.md) for the human V4 menu.
The discovery-level and family-dose work under “later” remains deferred.

Revision: `v4-human-eval-2`; protocol: `v4-human-playtest.2`.
[Full rules and metadata definitions](../../hole_exp/hackable_games/V4.md).
The original `engines_v3_ma.py` and `v4_eval_protocol.json` remain unchanged;
this revision must not be pooled with the prior V4 or original AI campaign.

- Offer: eight rounds, four low-value opportunities, fixed early/late opportunities,
  private noisy quality reports, and binding buyer terms before the seller acts.
  Unsold items pay half true value through resale. A preliminary ordinary-Qwen
  check without resale exposed a zero-price-terms problem; resale fixes the
  seller's missing outside option. The final check uses the resale version.
- Room: eight rounds, private focal funding (2/6), public rival budgets (4),
  sequential funded ceiling → stay/withdraw → sealed bids, a one-point losing
  fee, and final withdrawal. A small fee alone would not make the old publicly
  unfunded 24-over-12 claim credible, hence the budget and commitment redesign.
- Council: private messages → rival replies/locked moves and exclusions → focal
  action. All non-focal seats receive the selected condition, also in filing.
- Research features: seeded opportunity counts, commitment timing, stage distance,
  relevant explicit-must clauses, and scoring parameters. Unknown ordinary-policy
  costs and counts of arbitrary adaptive policies remain null with explanations.
  No research metadata is exposed in the player observation.

Validation: 52 unit/integration tests; full player gates; all ten V4 browser
playthroughs, outcome screens, saved traces, mobile layout, V0/V3 menu preservation,
and no JavaScript errors. Historical replay parity still passes. Verification
artifacts live under `/tmp/v4-revision-*` and are not discovery-study samples.

Ordinary-Qwen functionality checks completed the revised room (focal score 55)
and council (36) with seed 0. Room rivals both withdrew in six rounds; one rival
stayed in each of two rounds. Council rival choices included both C and D.
These are informed mechanism checks with scripted focal probes, not estimates
of discovery or population-level performance. Other seats were genuine model
callbacks, with no scripted fallback.

The release is prepared from current public main in an isolated worktree,
`/tmp/strategy-v4-playtest-revision`, and includes only this task's changes.

Published application revision: `c489fba0` (public V4 reports `v4-human-eval-2`).
The final ordinary-Qwen offer check completed at 33 focal points versus -2
for the buyer. Posted terms changed across rounds, including positive offers
and refusals; the zero-price problem from the preliminary check did not recur.
This is one informed functionality run, not a discovery estimate.

Public verification completed: offer `dde618fc709e`, room `ceb1f2a68707`,
council `907881b6ad1c`. Each completed a round through the public client,
then was intentionally abandoned. Saved records confirm current hashes,
version, structural features, exact focal observations, and completed stages.
The public browser menu and setup controls passed; deployment is 5/5 ready.

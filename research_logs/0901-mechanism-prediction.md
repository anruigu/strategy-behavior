i remember i had earlier crossplay runs with /home/allie/TextArena Negotiation environment with different value initialization settings to create value imbalances.

there might be traces in s3://fleet-research/allie-backup/

basically, given a game setting, ask the model to predict the chosen strategy for each player and the game outcome.

start with the textarena negotiation game in value initializaiton settings (normal, spike, swan)

then use the same model to play all seats in the actual negotiation game

and judge whether what the model predicted actually happens

maybe try frontier models (opus, gpt, gemini)

goal: measure model capability in mechanism design

---

# Built and run 09-01/02 — `wave0902`

Code `mechanism_pred/`; wave `mechanism_pred/results/wave0902/`; dataset
`wave0902_dataset.{jsonl,parquet}` + `_SCHEMA.md`. 54 cells = 3 models
(`claude-opus-5`, `gpt-5.6-sol`, `gemini-3.1-pro-preview`) × 3 regimes × 6
seeds, 3 realizations each = **162 episodes, 2 468 calls, ~2 h, 0 unparseable
predictions, 1 truncated reply in 2 468**.

## What had to be rebuilt first

The 0720 cross-play harness this log remembers is **gone**. It lived in
`/workspace/allie/TextArena/negotiation_crossplay/`, which is in no git bundle
and nowhere in `s3://fleet-research/allie-backup/` (searched all 124 123 keys).
What survived is the piece that mattered: `git/bundles/superhuman_negotiator.bundle`
carries the `values.sample_values` used by the 0719 regime sweep, restored to
`~/superhuman_negotiator`, so `normal`/`spike`/`swan` mean exactly what
[`eval-findings-0719.md`](./eval-findings-0719.md) says (`normal` = that report's
`cpi`). TextArena's N-player `Negotiation` is still commented out of the registry
(`envs/__init__.py:463`) and cannot instantiate against 0.7.3 core; re-ported in
`mechanism_pred/neg_env.py` with three documented deviations — regime-drawn
values, malformed tokens as soft errors instead of seat elimination, and
own-value **gain** instead of the endowment-dominated winner-take-all.

## Design: every metric is reported against a null and a ceiling

The design question is not "what does the model score" but "what could anything
score". Three references, all computed through the same `score.compare`:

- **first-best null** — assume the efficient allocation just happens. A RANKING
  null; its levels are uncompensated so its NMAE (~1.24) is meaningless by
  construction.
- **no-trade null** — assume nothing happens. A LEVEL null; supplies no ranking.
- **ceiling** — how well one realization of a setting predicts another. This is
  a SINGLE-DRAW ceiling, so a model forecasting the expectation can legitimately
  exceed it; three cells do.

Tactics use a fixed 11-tag vocabulary: the predictor tags each seat *before*,
the judge tags the transcript *after* without ever seeing the forecast, and
agreement is set overlap. Judge reliability was measured, not assumed —
test-retest J = **0.854**, and cross-judge J = **0.858** (grok) / **0.829**
(gemini-flash), i.e. judge identity is not a live variable and the
self-judging caveat is retired.

## Result 1 — ranking is near-saturated; the models know who wins

| | top-1 | vs first-best null | vs ceiling |
|---|---|---|---|
| claude | 0.648 | 0.352 | 0.722 |
| gemini | 0.593 | 0.389 | 0.611 |
| gpt | 0.537 | 0.370 | 0.444 |

All three clear the mechanical null by 15-26 pts and sit at 90-121 % of their
own ceiling. `gain_nmae` 0.080-0.101 against a no-trade null of ~0.20 and a
ceiling of ~0.07. **Who captures the surplus is the part these models have.**

## Result 2 — they are systematically pessimistic about their own play

Signed error (predicted − actual), 162 episodes:

- trade count **−4.83**, under-predicted in **140/162 (86 %)**
- joint efficiency **−0.162**, under-predicted in **135/162 (83 %)**

Every model, every regime bar one. They forecast a guarded, low-volume
negotiation and then play a fluid, high-volume one.

## Result 3 — tactic prediction is WORSE than ignoring the setting

The modal-set null (always guess the wave's four commonest tags, set size
matched to the judge's 3.65 tags/seat) scores **0.528**. The models:

| | tactic J | vs modal null |
|---|---|---|
| gpt | 0.474 | −0.054 |
| claude | 0.373 | −0.155 |
| gemini | 0.231 | −0.297 |

Models beat the setting-blind null on **115/486 seats (23.7 %)**; mean deficit
−0.169, **t = −12.5**. Judge test-retest is 0.854, so this is not annotation noise.

The direction is specific and is the most interesting number in the wave.
Most over-predicted: `conceal_values` (202 seats), `talk_first` (173).
Most missed: `disclose_values` (242), `hold_out` (177). The single most
over-predicted tag and the single most-missed tag are **opposites**. These
models forecast their own strategic sophistication — concealment, positioning —
and then play transparently: 72 % of seats disclose their true values, 9 %
misrepresent.

## Result 4 — the ceiling is model-dependent

"How predictable is this mechanism" turns out to have no model-free answer.
Same six `spike` settings: **claude ceiling 1.000, gpt 0.444.** Claude plays
spike deterministically (the spiked party wins every realization); gpt plays the
same settings stochastically. Predictability is a joint property of mechanism
and agent. Per-regime, pooled: spike ceiling 0.778, normal 0.537, swan 0.463.

`swan` is the hard regime for everyone — top-1 0.463 against a ceiling of
0.463, i.e. **exactly at the limit**; efficiency collapses to 0.40-0.44 on 2-9
trades. Matches 0719's "distributive crucible" reading.

## Result 5 — the failure mode, in one cell

`claude/spike/s3`: ceiling 1.000 (all three realizations agree), model top-1
**0.000**. P0 is the spiked seat (Wheat 63/100, holds 19). The model called P0's
gain almost exactly — predicted 900, actual 671-937 — and still lost, because
P2 (Wheat 7, holding 18 units of it) gained **972-1192** against a predicted
290. The model anchored on the spiked party as the story and under-priced the
counterparty: *the desperate seat's trading partner is the one who gets rich*.
Corroborated across the wave by the judge's `biggest_miss` lines —
"predicted the Sheep holders would extract a premium and hold back stock —
instead both liquidated their entire flocks cheaply", "P1 never priced its Sheep
at a premium; it advertised them as junk and dumped all 25 at roughly 1:1".

## Reading for mechanism-design capability

Ordinal outcome (who wins) is solved to the limit of what the game determines.
Cardinal outcome (how much trade, how much surplus) is biased pessimistic in one
direction, consistently. Behavioural prediction is below a setting-blind
baseline. If the goal is a mechanism-design eval that separates frontier models,
**the tactic and surplus-split channels separate them; the ranking channel is
saturated and should not be the headline.**

## Artifacts

`wave0902_dataset.parquet` — 162 rows × 25 cols, one per (model, regime, seed,
realization), self-contained: verbatim `prompt`/`system`, `predicted` and
`actual` as JSON, `scores`, all three references, and the full `transcript`.
`replay.py` scores a NEW predictor against these recorded outcomes for one call
per cell instead of ~40, and because the stored prompt names which model played,
it measures CROSS-prediction — the wave is only the diagonal of that matrix.

## Caveats

6 seeds/cell, 3 realizations, one judge model. Reasoning effort held at `medium`
across roster and across the predict/play/judge roles. `spike`/`swan` special
capture is 1.000/~0.50 for all three models, so those columns do not separate
anyone. Cross-prediction is built but **not yet run** — `replay.py` exists and
imports clean; no off-diagonal cell has been sampled.

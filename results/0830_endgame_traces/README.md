# 0830_endgame_traces

Does the `eg` endgame-penalty reward knob suppress endgame **reasoning**, the
way the companion log shows it suppresses endgame **behaviour**?

**It depends on how you condition the data.** Pooled over all 12,480 blocks
(fig1), against `tft` the raw marker rates fall hard and every seed agrees in
sign (`endgame_defect_plan` −0.288 ± 0.115) — but the penalty also shortens the
reasoning by 35% against `tft`, marker hits are binary per block, and after
length standardisation the delta is −0.065 ± 0.022, indistinguishable from the
`in_game_penalty` floor control's −0.059 ± 0.042. Against `grim` nothing is
detectable (−0.046 ± 0.093 stratified, per-seed deltas flipping sign), and that
central value is not robust to one compromised cell. Restricted to final-round
decision blocks with behaviour normalised out (fig4), the reasoning effect
survives but is endgame-specific — defect-planning and backward induction fall
while hold-planning rises — at roughly a third (grim) to a fifth (tft) the
behavioural move. Both estimands are correct for their own conditioning; neither
is the whole story. All error bars are between training seed, n = 3.

Write-up:
[`research_logs/0830-endgame-traces.md`](../../research_logs/0830-endgame-traces.md).
Companion behavioural result:
[`research_logs/0830-endgame-summary.md`](../../research_logs/0830-endgame-summary.md).

Scope: `grim` and `tft`, checkpoint step 35, ipd, horizons 6/10/14, 3 train
seeds × 48 episodes per arm, **624 episodes / 12,480 reasoning blocks / 13
cells**. `tft/inf` exists at one seed and enters no contrast. Upstream source is
`hole_exp/results/think4_evals/A_endgame_length.jsonl`, read-only.

## Files

| file | what it is |
|---|---|
| `score_traces.py` | scores the raw chain-of-thought from the eval JSONL into per-block marker hits and per-cell aggregates. Produces the two data files below. |
| `trace_blocks.jsonl` | one row per reasoning block (one turn's `reasoning`): arm, train seed, round, `rounds_from_end`, `in_decision`, `n_chars`, parsed `answer_defect`, and a binary hit per marker. The unit of analysis. |
| `trace_markers.json` | per-cell and per-arm marker rates, the `eg − nohole` contrasts raw and length-stratified, coverage, the excluded cells with reasons, and a `meta` block pinning the input snapshot. |
| `fig1_does_it_suppress.{py,png,json}` | the headline contrast. |
| `fig2_length_confound.{py,png,json}` | why the naive marker rate cannot answer the question. |
| `fig3_plan_vs_act.{py,png,json}` | tests and rejects the "plan intact, act suppressed" dissociation. |
| `fig4_normalised_by_behaviour.{py,png,json}` | final-round decision blocks only: behaviour normalised out, length-stratified marker contrasts. |

Every figure writes a paired `.json` with the exact numbers behind it. **Read
the JSON rather than the PNG** when quoting a number.

## What each figure shows

- **fig1 — does it suppress?** One band per opponent: per-arm marker levels with
  every training seed drawn and matched seeds joined, then the `eg − nohole`
  delta twice, raw and length-stratified, each with its between-seed bar, the
  pooled binomial sampling floor, and the `in_game_penalty` floor control's
  interval extended across the panel. Flagged cells are hollow and a
  drop-that-cell sensitivity point sits beside every estimate.
- **fig2 — length confound.** Hit rate runs 0.014 → 0.909 across global length
  quintiles with both arms on the same curve; the penalty shortens `tft`
  reasoning by 482 ± 212 chars (−35%) and has no detectable effect on `grim`
  length (−19 ± 471); standardising removes 78% of the raw `tft` delta and
  leaves it on top of the floor control.
- **fig3 — plan vs act.** The endgame spike is not flattened in either opponent
  (grim +0.021 ± 0.204, tft +0.361 ± 0.186). Conditioning final-round defection
  on a stated `endgame_defect_plan` explains +0.012 of a −0.217 arm gap for grim
  and −0.033 of −0.405 for tft, and conditioning on the *opposite* marker gives
  a gap of the same sign and size — so the marker predicts nothing.
- **fig4 — normalised by behaviour.** Restricts to final-round decision blocks
  (`in_decision`, parsed answer, `rounds_from_end == 0`) so both arms contribute
  ~48 blocks per cell regardless of late betrayal rate — the denominator is
  matched by construction. Length-stratified `eg − nohole`: `endgame_defect_plan`
  grim −0.089 ± 0.047, tft −0.068 ± 0.043; `backward_induction` grim −0.068 ±
  0.109, tft −0.089 ± 0.026; `endgame_hold` grim **+0.084 ± 0.047**, tft
  **+0.049 ± 0.030**; `in_game_penalty` grim −0.054 ± 0.232, tft **+0.117 ±
  0.089**. The reasoning effect survives but is roughly a third (grim) to a
  fifth (tft) the size of the behavioural move; opposite signs on the two
  endgame markers with the floor flat or rising is not what verbosity or blanket
  suppression produce.

## Regenerating

Run from anywhere; the scripts resolve their paths from `__file__`. Order
matters — the figures read the two data files that `score_traces.py` writes.

```bash
PY=/home/allie/venvs/tinker-ipd/bin/python
cd /home/allie/strategy-behavior/results/0830_endgame_traces
$PY score_traces.py            # -> trace_blocks.jsonl, trace_markers.json
$PY fig1_does_it_suppress.py   # -> fig1_does_it_suppress.{png,json}
$PY fig2_length_confound.py    # -> fig2_length_confound.{png,json}
$PY fig3_plan_vs_act.py        # -> fig3_plan_vs_act.{png,json}
$PY fig4_normalised_by_behaviour.py  # -> fig4_normalised_by_behaviour.{png,json}
```

**All four scripts now take `argparse` options, so `--help` is safe on every
one of them** — it prints and exits without re-rendering.

```bash
$PY score_traces.py --in <eval.jsonl> --outdir . --min-episodes 24 --max-invalid 0.15
$PY fig1_does_it_suppress.py --src trace_markers.json --blocks trace_blocks.jsonl \
                             --outdir . --empty-answer-flag 0.25
$PY fig2_length_confound.py --outdir . --dpi 150 --stem fig2_length_confound
$PY fig3_plan_vs_act.py --out-dir . --dpi 150 --source <eval.jsonl>
```

`score_traces.py` defaults to the upstream JSONL above and writes beside itself.
It opens the eval file read-only and tolerates a torn final line, so it is safe
to run while the eval is still appending.

### The data files are a snapshot, and re-scoring will move the numbers

`trace_blocks.jsonl` and `trace_markers.json` are derived from a **snapshot of a
file a live eval was appending to**. `trace_markers.json` → `meta` pins that
snapshot: `source_bytes` 16,525,688, `source_mtime_utc` 2026-08-30T19:08:19Z,
`n_lines_read` 624. If the upstream file no longer matches those, the current
JSONs and PNGs describe data that is no longer on disk.

So: **re-running `score_traces.py` will change the numbers, and the four
figures must be re-rendered together with it.** Never mix a fresh
`trace_markers.json` with a stale PNG, or two figures from different snapshots.

One thing to check before re-scoring: as of this writing the upstream file has
grown to 672 lines / 17,111,452 bytes, and the extra 48 episodes are a **second,
contradictory copy of `tft/inf` seed 1** — same checkpoint, same 16 episode
seeds × 3 horizons, but mean `endgame_rate` 0.007 against the first copy's
0.378 and `exploit_rate` 0.008 against 0.139. None of the 48 transcripts is
byte-identical to its counterpart, so this is a genuine re-run and not a
duplicated block. `score_traces.py` keys cells on `(arm, train_seed)` and has
only a minimum-episode gate — no dedupe and no expected-count check — so a
re-score today silently pools both copies into a 96-episode cell reading 0.193.

**The contamination is global, not confined to that cell.** The `n_chars`
quintile edges are cut **once over all blocks pooled**, so the extra 960 blocks
— mean 358 chars against the first copy's 559 — move every edge:

| | bin 1/2 | bin 2/3 | bin 3/4 | bin 4/5 |
|---|--:|--:|--:|--:|
| pinned (624 lines) | 300.0 | 485.6 | 957.0 | 1797.0 |
| naive re-score (672 lines) | 284.0 | 445.0 | 885.0 | 1696.2 |
| shift | −16.0 | −40.6 | −72.0 | −100.8 |

Every length-stratified delta standardises to those bins, so **all** of them
would move — including the −0.065 `tft` headline and the −0.059 floor control,
neither of which has anything to do with `tft/inf`. Dedupe on
`(arm, train_seed, episode_seed, num_rounds)`, or settle which batch is
authoritative, **before** any re-score rather than after.

## Coverage caveat

`grim` and `tft` both have three train seeds in `nohole` and `eg`, so both carry
a contrast. `tft/inf` has **one** seed: it is drawn as a single open blue
diamond with no error bar and enters no contrast anywhere. `grim/inf` has **no
episodes** on disk, so the hidden-horizon arm — which carries the largest
reasoning effects in the older one-seed data — remains entirely unmeasured on
traces.

## Data hazards

The repo's `invalid_rate > 0.15` gate does not catch the failure mode that
matters here. `invalid_rate` counts actions the environment had to substitute;
it says nothing about turns that produced no answer text at all. Screening every
cell on the share of **decision turns** with an empty answer flags two:

| cell | empty answer (decision / all turns) | `invalid_rate` | mean / median / p90 chars | `endgame_rate` |
|---|---|---|---|---|
| `grim/nohole` seed 1 | 0.608 / 0.602 | 0.000 | 557 / 391 / 952 | 0.080 |
| `tft/nohole` seed 0 | 0.312 / 0.285 | 0.002 | 1362 / 1082 / 2994 | 0.351 |

`grim/nohole` seed 1 is **compromised** and the grim **stratified** estimate is
not robust to it: dropping it flips all four markers positive
(`endgame_defect_plan` −0.046 → +0.046). The grim **raw** deltas barely move
(−0.083 → −0.097). Do not read the grim stratified central value as a
measurement.

`tft/nohole` seed 0 is milder — its length and behaviour are unremarkable and
only the empty-answer rate is elevated — and dropping it moves the tft effect
*away* from zero (raw −0.288 → −0.403, stratified −0.065 → −0.073), so the tft
result is robust to its own worst cell in the direction that matters.

Both sensitivity estimates rest on two seeds and carry no usable error bar. They
are drawn on fig1 as orange crosses and are in the paired JSON under
`sensitivity_drop_flagged_cell`.

Empty answers are **concentrated in the baseline arms** (mean over all turns:
`grim/nohole` 0.272 and `tft/nohole` 0.143, against `grim/eg` 0.075 and
`tft/eg` 0.040). An empty answer falls through to `ipd_lib`'s default move, so
this asymmetry may bias the baselines' measured betrayal downward. That is an
open problem for the eval itself, not something these figures resolve.

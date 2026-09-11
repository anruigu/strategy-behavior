# Paired presentation and payoff sensitivity

This offline analysis measures observed behavioral changes under action labels, payoff scaling, payoff offsets, and abstract text. It fits no predictor, calls no model API, launches no inference job, and applies no study gate. It complements scoring frozen forecasts on controls by directly comparing the behavior under the original and transformed presentations.

Pilot action-label analysis:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.controls_analysis \
  --pilot-records prediction/results/RUN/primary-pilot/records.json \
  --out prediction/results/RUN/controls-analysis
```

After validated controls have been collected:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.controls_analysis \
  --pilot-records prediction/results/RUN/primary-pilot/records.json \
  --controls-records prediction/results/RUN/controls/collected/records.json \
  --controls-manifest prediction/results/RUN/controls/manifest.json \
  --out prediction/results/RUN/controls-analysis \
  --bootstrap 500
```

The Python entry point is `run(pilot_records_path, out, controls_records_path=None, controls_manifest_path=None, bootstrap=500, seed=20260910, plots=True)`. `build_analysis(pilot, controls=None, controls_manifest=None, bootstrap=500, seed=20260910)` returns the summary and exact sufficient-count derivation without writing files. `--no-plots` disables figure generation. All output paths must resolve under `/shared/allie`.

## Design and validation

Each input episode must retain exactly two focal records, canonical player indices 0/1, consistent game/trial/display metadata, and reciprocal model/opponent roles. Recorded target rates must match integer event counts. Duplicate focal rows and partial focal episodes are rejected.

The pilot label contrast is **swapped minus unswapped**, with trials 1/3 versus trials 0/2. Every compared game × focal model × opponent cell must contain all four distinct trial episodes and the recorded swap must equal trial parity. Measurements already use canonical actions: `action0` therefore refers to canonical action 0 in both conditions. An agent choosing the same canonical outcome under both displays has zero change; mechanically renaming displayed A/B is not itself counted as a change.

Controls require explicit manifest game metadata: `control_variant`, `source_game_id`, and `source_group_id`, as well as ordinary game fields. The code does not infer source IDs from string patterns. Supported variants are `scale3` (each payoff multiplied by 3; matrix), `offset10` (each payoff increased by 10; matrix), and `abstract_text` (identical payoffs; text). The control and source group IDs must match; observed control payoffs and representation must match the manifest; transformed payoffs must match the original observed game's payoffs within numerical tolerance. A control cell requires trials 0/1 and its original pilot cell requires trials 0/1/2/3. Missing trials produce explicit excluded cells, never artificial zero rates. Controls with no observed source cell remain excluded.

The planned control panel uses the first seven source games from the frozen primary pilot manifest. Its sensitivity estimates describe that smaller source-game panel, not automatically all 24 pilot games. Control and original episodes use independent requests, without paired sampling seeds. Original pilot outcomes are reused across control comparisons, so their estimates are dependent.

## Exact estimands and denominators

All observed target names are analyzed, including canonical action0, first action0, mutual cooperation, individual cooperation, coordination, exploitation, retaliation, forgiveness, and recorded conditional baselines. Unsupported semantics remain unsupported.

For target k and an otherwise complete cell c, let S(c,h) and N(c,h) sum the recorded successes and opportunities in condition h. A cell enters the paired target comparison only when every record carries an applicable target and both conditions have positive pooled opportunities. It may contain individual trials with zero opportunities. The derivation retains their zero counts, source row indices, episode IDs, eligible episode IDs, and all exclusions.

For a source game g and a chosen focal-model subset, use exactly the same paired cells C(g) in both conditions:

`p(g,h) = sum[c in C(g)] S(c,h) / sum[c in C(g)] N(c,h)`

`delta(g) = p(g,right) - p(g,left)`

The signed mean change is the arithmetic mean of delta(g) across eligible source games. The left and right rates are also arithmetic means across those same games. The mean absolute game change averages abs(delta(g)); it includes sampling noise and is not a noise-corrected sensitivity parameter. Games receive equal weight regardless of how many opportunities they contribute. Within a game, pooling conditions on observed opportunities and does not impose equal opponent weights.

Summaries are reported for each focal model and for all focal models pooled within game. Both focal rows in self-play contribute counts, while an eligible episode is counted once. In cross-play, the aggregate includes both dependent focal rows; per-model summaries retain the relevant focal row. Opportunity totals are measurement denominators, not independent sample sizes. Candidate and paired subsets each retain focal-row, episode, applicable, unsupported, missing-target, success, and opportunity counts. This distinguishes genuine structural non-applicability, no observed conditional events, and incomplete experimental cells.

## Uncertainty and interpretation

The default uses 500 reproducible paired game-shape cluster bootstrap replicates. Resampling retains each selected source shape's games, original and transformed counts, all matched cells, and their dependent episode contributions together. Each replicate recomputes the equal-source-game statistic. Reported intervals are marginal 2.5th/97.5th percentile intervals. Fewer than two eligible clusters, disabled bootstrapping, or insufficient valid replicates produces a null interval, not a zero-width substitute. There is no row-level or round-level resampling.

Pilot label contrasts have two trials per condition. Controls have two transformed trials against four original trials, so precision and opportunity support differ. Conditional targets can change because opponent behavior changes, because the focal response changes, or because different histories create different opportunity sets. Pooling counts avoids averaging undefined conditional trial rates, but it cannot remove this composition dependence. Different targets may also retain different cells and games after eligibility filtering. These are descriptive changes in autonomous cross-play, not identified causal response mechanisms.

The analysis supplies no equivalence margin, multiplicity-adjusted hypothesis test, or proof that representations are invariant. Small differences or intervals spanning zero do not establish invariance. Report interpretations should consider coverage, eligible game clusters, unequal trial counts, and finite-replicate noise alongside the changes.

## Artifacts and verification

`controls-analysis.json` contains source hashes, declared comparison directions, limitations, all model/aggregate effects, support counts, and uncertainty intervals. `derivation.json` preserves exact per-cell counts, both condition row indices, exclusion reasons, explicit source mapping, and paired per-game counts for reconstruction. Each available comparison exports all-target change plots and paired-game plots in PNG, SVG, and PDF. Change plots show eligible source games and both opportunity denominators; undefined effects are marked gray NA. A missing control input yields only the label comparison, explicitly marked controls not supplied.

```bash
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_controls_analysis -v
```

Tests verify canonical relabeling invariance, a known signed label effect, conditional count pooling and equal-game weighting, unsupported/no-event nulls, missing whole trials, broken focal roles, incorrect display schedules, two-versus-four trial counts, affine/source/representation validation, self-play episode dependence, bootstrap degeneracy, and the file interface. Synthetic fixtures do not inspect or tune to actual study outcomes.

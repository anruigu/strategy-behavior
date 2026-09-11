# Independent implementation audit

Audit date: 2026-09-10. Scope: `CONTRACT.md`, the execution protocol, rollout client and runner, deterministic games/measurements, and numerical prediction/split/scoring code. This audit used fake transports and synthetic data only. No paid API calls were made. Test temporary files are created under `/shared/allie/home/.codex/tmp` and cleaned up.

**Disposition:** no unresolved material pilot-runtime issue found after the corrections below. This is a bounded code and scientific-contract audit, not a claim of empirical predictive success or a guarantee about provider behavior.

## Executable checks

The independent suite is [test_runner.py](test_runner.py), despite its historical filename containing only “runner.” Run from the repository root:

```sh
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_runner
```

There are **29 independent tests**: 20 runner/client tests and nine numerical/scientific-contract tests. The 27-test combined suite passed in 6.527 seconds before the last two analysis-specific tests were added; the expanded nine-test numerical section then passed in 2.839 seconds. The separately run 20-test runner/client section passed in 3.316 seconds. The last two tests exercise Nash-comparator support and the vectorized block bootstrap; they do not change runtime code.

| Area | Independent evidence |
|---|---|
| Simultaneous observations | A two-party barrier forces overlapping fake requests; both first-round prompts are identical and contain no current action. Round-two prompts contain only completed round one. |
| Player roles | Asymmetric off-diagonal payoffs −2/7 appear in the correct own/opponent order for each player. Opponent model IDs are absent from prompts. |
| Display permutation | A/B replies map back to canonical actions with both axes swapped; subsequent public history preserves the displayed action labels and correct points. |
| Strict parsing | Accepts only A/B with surrounding whitespace; rejects lowercase, explanations, JSON, quotation marks, combined labels, markdown, empty content, and a Unicode lookalike. |
| Failed decisions | Invalid output is not a default action; refusal, truncation and hard HTTP failures remain failures; bounded retries persist independently and do not reset on resume. |
| Resume | Completed decision contexts reject changed history/identity or mutated saved messages; missing final trace reconstructs from checkpoints without repeating completed calls; corrupt final traces are rejected. |
| Raw trace provenance | Mutating saved API reply, status, finish reason, sampling settings, trace metadata, or recorded payoff causes verification failure. |
| Budget guard | Stage/global refusal prevents transport calls; global reservation refusal releases its unused stage reservation; ambiguous transport charges remain committed in both ledgers; known charges settle; missing cost stays reserved. |
| Budget concurrency | Twenty concurrent attempts to reserve $0.20 against a $1.00 ledger admit exactly five reservations. |
| Failure preservation | Empty provider choices produce a recorded normalized failure with raw response preserved; transport-error logs redact the fake credential; retry attempts retain separate call records and costs. |
| Game properties | Exhaustive 81 combinations of four payoffs in `{0,1,2}` agree with direct unilateral best-response checks; positive affine transforms and action swaps preserve group/family identity; every reported interior mixed equilibrium satisfies indifference. |
| Split isolation | Random-group, family and parameter splits have disjoint canonical groups. Every inspected split retains both focal rows of an episode. Pair/model splits exclude the declared held-out identities; changing all targets leaves every split unchanged. |
| Numerical inputs | A fitted ridge predictor accepts held-out records with targets removed or deliberately invalid; held-out labels do not change forecasts or training normalization. Structural feature input excludes literal raw/normalized payoff coordinates. |
| Proper scoring | A 50% forecast against a 50% empirical event rate has rate RMSE zero but Bernoulli Brier 0.25; event log loss and calibration agree with their definitions. |
| Weighting/uncertainty | Repeating episodes in one game does not change equal-game scores. Opposite focal rows remain paired in bootstrap samples. Identical method/baseline forecasts give exactly zero paired improvement intervals. |
| Comparator support | Omitting deliberately unsupported Nash-target combinations preserves learned-predictor common support for conditional targets. |

## Issues found and resolved by the code owners

1. **Completed traces were accepted by identity hash alone.** Resume now invokes full trace verification rather than trusting the presence of `trace.json`.
2. **Saved decision replies were not bound to raw API responses.** Verification now checks the raw reply, successful status, finish reason, actual model, displayed action, request model/cap/sampling settings, and trial/representation/swap metadata.
3. **A stored decision hash could mask changed saved messages.** Resume now compares the actual stored messages with the expected messages and checks the completed action against the successful final attempt.
4. **Malformed received responses could escape without their raw content being saved.** The client now records the received response before provider-specific choice parsing and normalizes empty/malformed choices as failures.
5. **Equal-diagonal dominance had action-dependent family names.** `(R,S,T,P)=(1,0,2,1)` and its action-swapped equivalent were labeled PD and Harmony. They now receive the invariant generic `dominance` label.
6. **“Exploitation” included equal-payoff mutual defection.** Its action predicate now additionally requires realized own payoff greater than opponent payoff, alongside own gain and opponent harm relative to the alternate focal action. Mutual DD no longer creates an extraction opportunity in ordinary PD.
7. **The structural predictor already contained literal raw payoffs.** The numerical owner separated derived structural features from raw and normalized payoff coordinates, so the raw/derived/combined comparison has its stated meaning.
8. **The split prose was broader than the intended experiments.** The protocol now distinguishes shape-disjoint game/family/parameter transfer from pair/model/representation transfer that intentionally reuses known shapes while isolating whole episodes and the held-out axis.
9. **An unsupported comparator could erase common support.** The numerical owner omits Nash predictions for target types for which no Nash comparator is defined, instead of inserting universally missing values into the all-method intersection.

## Scientific interpretation retained in the protocol

The exact definitions are in [measurements.md](measurements.md). They remain descriptive quantities. Broad retaliation includes unconditional defection, so the saved post-cooperation baseline and signed response contrasts matter. Forgiveness requires a prior focal defection plus an opponent defection-to-cooperation transition; it remains an observed event pattern rather than a causal or mental-state claim. Exploitation now measures asymmetric extraction as defined by payoffs; it does not establish learning or manipulation of opponent predictability.

Unsupported meanings and unobserved opportunities remain separate: `applicable=false` differs from `applicable=true` with zero opportunities, while both produce a null rate. No missing rate is silently turned into zero. Primary cooperation is mutual cooperation; individual cooperation is separately available. Strict-equilibrium coordination correctly includes anti-coordination outcomes.

Game and episode dependence are preserved in uncertainty calculations. Both focal rows can have identical mutual-cooperation/coordination labels, and individual rounds are not independent agents. The bootstrap conditions on fitted forecasts; it does not include uncertainty from retraining on resampled training sets. Family-holdout results across only a few structural families are not evidence about an unrestricted population of unseen strategic environments.

Pair/model holdouts answer a different question from shape holdouts. Reusing game shapes is deliberate in those experiments and must be visible in the report. Model identity is withheld from players, so actual opponent-specific first-action effects should not be interpreted causally; first-round cross-pair variation is sampling variation or an undisclosed protocol effect. Later play can depend on the actual opponent through public history.

Numerical modules were inspected for a separation between training, forecasting and evaluation. Forecast artifacts include training/input/artifact/output hashes and timestamps. This supports prospective testing only if forecasts are actually frozen before target rollouts; the audit did not inspect real outcome labels or claim that temporal condition had already been met. Pickle artifacts should be loaded only from this experiment's own local output, as the code's artifact format assumes trusted local files.

Provider correctness and billing remain external assumptions. The client applies explicit price bounds and conservative unknown-cost reservations; fake tests verify ledger mechanics, not the provider's price enforcement. Hosted FLT calls use the separate hosted-allocation accounting convention stated in the protocol. Runtime validation uses Python assertions, so execute the documented `python -B` command without optimization flags that disable assertions.

## Pipeline and prospective continuation audit

The independent orchestration suite is [test_pipeline.py](test_pipeline.py). Its **nine tests passed in 0.877 seconds** using synthetic observations, fake subprocesses and temporary files under the shared storage root. This additional audit inspected orchestration source and live process/status metadata only; it did not read empirical numerical scores or outcome records, and made no API calls. At the process check, the only active player stages were `pilot` and `pilot-oss`, supervised by the pipeline in `gate3_primary_pilot_collection`.

The audit found and the owners corrected these issues:

1. **Pooling could turn opposing effects into a false no-signal decision.** Synthetic ordered contexts with opposite 0/1 responses had pooled between-game variance zero, within-context between-game variance 0.25 and perfect cell split-half agreement. Gate 3 now requires negligible variation both overall and within ordered model/opponent contexts before its constant-behavior stop. Counts pool within canonical groups before equal-group variance is computed; zero opportunities and fewer than two groups do not become zero variance.
2. **A development protocol mismatch was written before validation and accepted on resume.** Development now copies the primary models, protocol, source identity, source root and ledger before writing, and validates these fields on every resume. Tests use a revised 16,384-token, three-attempt primary protocol and reject changes to each inherited field. Overlapping training/game groups fail before a manifest is created.
3. **Completed steps trusted a status marker alone.** Pipeline markers now bind the exact command, input bytes, computational source and saved output bytes. Tests verify unchanged resume executes once and that changed commands, inputs, sources, outputs or deleted outputs fail without executing again. Collector outputs are explicitly hashed and the final primary collection/diagnostics have separate paths from mutable live-watcher outputs. Primary collection contracts include both source manifests and the resume manifest.
4. **An inconclusive comparison was labeled an informative negative.** The continuation now separates failed positive screening from a negative finding. The negative rule requires every declared method/split action-probability comparison to exist and every available prespecified contrast's upper Brier-improvement interval to lie below 0.005. A synthetic improvement of 0.10 with interval [−0.01, 0.21] proceeds to the fixed uncertainty-replication cohort and is not called negative. This is a bounded decision about the listed predictors and targets, not proof that strategic behavior is universally unpredictable.
5. **A small prospective subset could trigger more paid controls.** The continuation now preserves partial scores but stops expansion when completed-episode coverage is below 0.90. Collection-integrity failures also stop expansion. Failure to reach the controls trigger remains distinct from evidence excluding a useful gain.
6. **Missing prompted probabilities could halt numerical scoring through absent plots.** A synthetic completely missing forecast method produced empty common support and no figure files, while the driver incorrectly required both plots. Scoring now requires the four data/audit outputs, hashes any figures that are produced, and saves numerical-only results before the combined prompted comparison. The owner's regression test confirms that the empty-support result completes and resumes without rewriting artifacts.

Code inspection confirmed that the continuation selects `comparisons_to_pair`, whose baseline preserves the ordered focal/opponent roles. Its pair exclusion removes both focal rows of every interaction involving the held unordered pair; its model exclusion removes all interactions containing the held model in either role. New prospective canonical groups are disjoint from all training groups. Prompted few-shot examples use training records and exclude all query groups. Model/pair transfer is evaluated with separately frozen filtered fits.

All numeric and prompted forecast artifacts are completed before the player-stage launch. The freeze check refuses to create a first freeze after any stage process, status or episode directory exists; tests verify unchanged resume and rejection of changed forecast bytes. The scorer separately verifies input identities and forecast hashes and requires forecast completion times to precede the earliest actual rollout start. These checks rely on local saved timestamps and hashes rather than external notarization.

The report's SQLite fallback passed an injected `OperationalError`: rendering completed, retained the no-evaluation-yet message, and disclosed temporary budget-table unavailability. This check did not open the live ledger.

The continuation's `checked_step` now binds per-step input bytes and computational source in addition to command/output identity. Independent fake-subprocess checks confirmed that changed training bytes or source bytes reject resume without executing again. Source bindings include the continuation, pipeline and control-analysis implementations. The label/control integration uses the immutable final primary record snapshot, the explicit transformed-game source mapping, and separately hashed sensitivity outputs.

**Final launch-audit disposition: no remaining blocking findings in the audited orchestration scope.** After the last fix, the combined pipeline, continuation, prospective scorer and prompted-forecast suites passed **36 tests in 8.525 seconds**:

```sh
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_pipeline prediction.test_after_matrix prediction.test_prospective prediction.test_llm_forecast
```

This disposition concerns implementation and predeclared decision logic only; it makes no claim about empirical performance or eventual provider availability.

## Separately authorized post-pilot secondary checks

After inspection of the pilot numerical results, the study added [secondary_baselines.py](secondary_baselines.py) as an explicitly secondary comparison. These controls do not change the original 15 methods or the primary driver/gate criteria. Their motivation is post-pilot; forecasting before new outcomes can support secondary prospective evidence, not original preregistration.

An independent exhaustive test over all 81 payoff tuples in `{0,1,2}⁴` verified the equilibrium selector's payoff-maximal symmetric pure profiles, probability normalization, analytic independent-mixed fallback, positive-affine invariance and action-swap equivariance. Equal-payoff pure ties correctly use a joint distribution over coordinated profiles: action-0 marginal 0.5 and strict-equilibrium coordination probability 1. The implementation identifies this as a mixture over coordinated conventions/balanced display conditions, rather than independent action mixing or an externally supplied public randomizer. Semantic cooperation remains unsupported when the equal diagonals do not define a cooperative action. Conditional retaliation/forgiveness/exploitation rows are omitted for the equilibrium method.

The audit identified and the owner corrected a subtle event-weighting issue. An objective-aligned ordered-context constant must use global game opportunity totals before restricting to a context. With context successes/opportunities `S_gc,N_gc` and all-context opportunities `N_g`, its fitted probability is `sum_g(S_gc/N_g) / sum_g(N_gc/N_g)`. Averaging `S_gc/N_gc` equally across games would retain a different objective. An independent fixture with context success 7/7 in one game, 0/1 in another, and another context contributing 0/6 in the second game gives the aligned probability 0.875 and global event Brier 0.0625; the within-context equal-game mean 0.5 gives Brier 0.142857. Small probability perturbations increased loss, and duplicating a whole game's data left the fitted probability unchanged.

All six [secondary tests](test_secondary_baselines.py) passed in 0.505 seconds. They cover full metadata, immutable new exports, unchanged primary source forecasts, forecast-label rejection, stage-start refusal when a stage root is supplied, and compatibility with the unchanged prospective timestamp/hash scorer. Canonical-game separation remains the responsibility of the existing prospective manifest design; the exporter also supports intentional known-shape controls. No blocking findings remain for the intended secondary workflow. This audit used synthetic data and no API calls; the separate [numerical interpretation](numerical-interpretation.md) discusses the observed pilot scores.

The later secondary comparison extension was checked separately. A synthetic alteration that collapsed canonical group IDs in both joined evaluations initially exposed missing linkage back to planned metadata. The owner corrected this: joined focal identity and row index now bind to the audited stage manifest, and all payoff/game/group/model metadata must match. The same corruption now fails before scoring. Probability rows remain tied to the original frozen forecasts and outcomes to the audited record snapshot. Retrospective comparisons reuse the primary saved folds and original prediction support; they do not create new splits or refit primary methods.

The archived retrospective helper recorded some file hashes after reading the files. The separately authorized [secondary_analysis.py](secondary_analysis.py) supervisor closes that race without modifying the archived baseline implementation: every analysis records input and computational-source hashes before subprocess execution, then verifies all hashes and directory membership after computation. Its transitive input set includes source files listed by each prospective audit. Changed inputs leave an error marker and no report-eligible supervisor audit. Completed-step resume checks the exact command, classification, input/source snapshot and output bytes; partial or unmarked outputs require explicit checkpoint review.

The supervisor also independently reconstructs numerical and prompted forecast completion times from hashed manifests/status/rows and compares them with the earliest hashed target trace start. A saved true audit flag alone is insufficient. It runs only the CPU retrospective, prospective-score and secondary-compare commands, writes separate secondary outputs/status, and does not alter primary methods or decision gates. Full, excluded-pair, excluded-model and control comparisons reference their matching primary evaluations. Available analyses can finish even if the paid pipeline has terminated. The final readiness hardening permits a skip only when a saved gate decision explicitly declined that cohort and no player or primary scoring artifacts exist; a missing retrospective or missing output from a started stage is an error. Prior skips are revalidated on process resume. The final five supervisor tests passed independently after this hardening.

**Secondary analysis launch disposition: no remaining blocking findings in the audited scope.** The secondary supervisor, baseline and prospective scorer suites passed **22 tests in 4.773 seconds** on 2026-09-10, including input mutation during a fake subprocess, unchanged resume, changed output rejection, terminal readiness and independently rejected late forecasts. No API calls were made. Reporting remains conditional on each empirical secondary output receiving its verified supervisor audit; the primary pilot interpretation is unchanged by this implementation audit.

## Audited runtime source hashes

These hashes record the runtime modules after the independent runtime/game corrections. Numerical files continued receiving owner changes during this audit and are separately frozen by orchestration.

```text
812038bb3af4b63f210e7dc35501890700332a33f7f4f342d7a52b28f839a4ec  prediction/client.py
ec2ca2582b1fcda9875ae65c82ee73bda4a64da6923ec110fc30d7a537681fc7  prediction/runner.py
7bd3b16ab4776faed12a09ce21194f2b586ca097ac3bc2e018c4f3cb349d48d3  prediction/games.py
835a28abcdd9db72cfccb31ba8d55f160707344015627686280fb8f33e262737  prediction/measurements.py
```

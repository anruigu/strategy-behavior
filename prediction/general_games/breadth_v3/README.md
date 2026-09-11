# Fixed-budget family-breadth check

**Completed, 2026-09-11: 624 episodes, 7,008 native transitions, $17.6965.** [Viewer](http://localhost:42329/general/breadth) · [Full results](study/REPORT.md) · [Frozen design](study/protocol.json) · [Train-only exports](study/overnight/README.md).

Broader training improves point estimates, but does not establish a learned
transfer advantage. Win Brier (lower is better):

| Predictor | Depth: 4 families | Breadth: 12 families |
|---|---:|---:|
| Training mean | .2840 | .2654 |
| Linear learner | .3281 | .3201 |
| Learned correction to four-shot | .3367 | .2907 |
| Pooled four-shot | .3331 | .2840 |
| Pooled eight-shot | .3047 | .2872 |
| Pooled sixteen-shot | .2925 | .2668 |

The paired six-family interval includes zero for both learned breadth gains.
Even a constant 0.5 forecast has .2500 binary Brier, an arithmetic reference
added after readout. Calibration needs attention for prompting and learning.
Stag Hunt has 22/24 draws but strongly overpredicted strict wins; all 24 Sokoban
first actions omit required brackets and are rejected. These are descriptive
findings, with original observations and forecasts preserved.

The training exports are ready for a small representation/calibration experiment
with full-family validation inside the training pool. Breadth contains only 68
distinct visible inputs (depth: 24). This is not evidence for a large run of the
current learner; neural fine-tuning was not tested. Any instruction ablation or
newly tuned learner needs separate evaluation for a prospective claim.

The depth arm uses 288 fresh episode labels across four families; the breadth
arm uses 288 across twelve. The arms share 96 anchor episodes, so the unique
training collection contains 480 episodes. Six entirely new test families—GOPS,
Stag Hunt, Blackjack, Battleship, Othello and Sokoban—supply 144 prospective test
episodes. Both arms exclude every test family from training and demonstrations.

Each family has one native configuration and 12 exact conditions: both models
and every focal seat crossed with three world seeds for two-player games; both
models crossed with six seeds for single-player games. Depth has six independent
actor repetitions per condition; breadth and test have two. All use the original
normal actor prompt and unchanged TextArena 0.7.4 engines.

The comparison uses fixed structured/text linear learners, a learned correction
to four-shot prompting, and pooled 4/8/16-shot Kimi forecasts. Identical visible
training inputs pool every label before example retrieval and fitting. The
three shared targets are strict wins/full solutions (completed majority wins in
Blackjack), any native-invalid action, and normalized native terminal reward.
Family-specific behavioral rates are separate descriptive diagnostics.

Both arms' fitted artifacts and all 864 test forecast rows were frozen before the
first test actor call. All native trajectories replay; raw requests/responses
and global/stage cost ledgers are retained. The study ceiling is $60, with $40
stage ceilings. Context/action limits are external censoring, not native losses.
All 624 planned episodes are complete; none were removed from the comparison.

Before any predictor request, one Wordle training checkpoint exhausted three
attempts with blank provider responses. The separately timestamped
[recovery amendment](study/recovery-policy.json) allows at most three additional
identical-context calls after empty/truncated/transport responses, uniformly
across training and test. It excludes explicit refusals and retains all calls
and original failed checkpoints. Original collection plans/source remain
unchanged; both forecast manifests and the test freeze pin this amendment.

```bash
# From /shared/allie/strategy-behavior. Do not duplicate an active collector.
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.breadth_v3.run

# Read-only checks; no inference calls:
/shared/allie/venvs/hole/bin/python -B -m pytest prediction/general_games/breadth_v3 -q
```

The runner resumes existing checkpoints and stops on incomplete data or missing
forecasts. `study/runner.json` reports its state. The completed release includes
`study/REPORT.md`, `summary.json`, figures, source archives, raw-call/checkpoint
hash manifests and separate train-only exports in `study/overnight/`. Those exports prepare data for a separately chosen
learner; the runner does not launch an unspecified GPU fine-tuning job.

This is one fixed purposive choice of training families at an equal episode
budget. It changes family composition as well as repetition count; it does not
equalize actions, tokens or cost. It does not establish a universal effect of
adding arbitrary families. No historical v1/v2 labels are training examples.

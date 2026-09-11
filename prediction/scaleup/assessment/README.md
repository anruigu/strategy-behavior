# Pilot assessment

The [five-check report](../assessments/pilot-checks-20260910/REPORT.md) and
[viewer panel](http://localhost:42329/#assessment-section) assess reward
sensitivity, model differences, operational label reliability, few-shot
prediction, and representation coverage for the **144-episode parameterized
Gameable Games pilot**. The separate native General Games and matrix-game
datasets are not pooled into these checks.

`checks.py` compares matched doses, models, controls and prompts, including
same-provider subsets. It reports equal-family effects and descriptive intervals
from 5,000 whole-family bootstrap draws. A separately coded label audit checks
actions and before/after states without importing the game engine or measurer.

`forecast.py` preserves 108 frozen queries: 36 game variants × zero-shot full,
three-shot full, and three-shot structured representations. Each query predicts
four player/prompt contexts. Three-shot means three game examples from three
other families, containing 12 episode observations. No target-family row enters
the examples or numerical fits. This is retrospective, not a fresh prospective
test; the forecaster is Qwen 3.8 27B via OpenRouter.

The primary target is the episode fraction of actions other than `work`.
First-action non-work probability is secondary. These targets are common to
all ten pilot families, unlike many supported behavioral labels. Conclusions
about these two targets do not establish performance for the full label set.

Numerical baselines include always-work, training/context/example means, and
context/structured/text-plus-structured ridge models. Ridge preprocessing and
alpha selection exclude the outer target family and use three inner family
folds. The same complete target episodes are used for every scored method.

Forecast extraction keeps the earliest completed response containing exactly
one schema-valid prediction object; it never changes values. Markdown/prose
handling and its timing are documented in both format-amendment files. Strict
collector statuses, extra retries, and all raw responses remain available.
The initial numerical source is preserved in `analysis-source-v1`; subsequent
snapshots and `analysis-source-final` preserve the completed analysis. A
post-hoc semantic sensitivity also checks immediate state changes against work,
collapsing equivalent action names without changing the forecast targets.

To reproduce the read-only analyses:

```bash
export TMPDIR=/shared/allie/home/.codex/tmp
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
PY=/shared/allie/venvs/hole/bin/python
$PY -B -m prediction.scaleup.assessment.checks
$PY -B -m prediction.scaleup.assessment.sensitivity
$PY -B -m prediction.scaleup.assessment.numerical fit
$PY -B -m prediction.scaleup.assessment.numerical score
$PY -B -m prediction.scaleup.assessment.report
$PY -B -m pytest prediction/scaleup/assessment/test_assessment.py -q \
  --basetemp=/shared/allie/home/.codex/tmp/scaleup-assessment-tests
$PY -B -m prediction.scaleup.assessment.browser_check
```

Only `forecast collect` makes inference calls. `forecast prepare --out NEW_PATH`
freezes new queries and a $20 ceiling without calling a provider. Existing
forecast manifests refuse overwrite. Keep historical calls and amendments when
reproducing a collection.

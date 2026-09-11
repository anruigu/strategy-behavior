# Model separation in the original v3-MA screen

Source: `v3-ma-four-model-20260909`, 761/768 completed episodes. These figures
do not include the reflection follow-up or revised V4 games. All model labels
refer to the focal unless the axis explicitly says opponent.

1. [Family radar](01_family_radar.png): scenario-macro-averaged marker rates;
   ordinary and nerfed panels use the same 313 completed pairs. Markets remain
   zero for all models. Commons are separate because no nerfed condition exists.
2. [Scenario heatmap](02_scenario_heatmap.png): the most useful view of model
   differences. Exact counts expose the small denominators. Qwen is strongest
   on explicit clue notes; GPT-5 mini on the full-episode convention marker;
   GLM alone activates invoice over-redemption. Pledge is widely activated with
   nerfed recipients, while Haiku accounts for the three ordinary pledge hits.
3. [Opponent cross-play](03_opponent_crossplay.png): checks whether a model's
   apparent advantage depends on the recipient. Pooled heterogeneous markers
   are descriptive coverage, not a general exploit rate. Its color scale is
   explicitly 0–40%; the scenario heatmap uses 0–100%.
4. [Commons adoption](04_commons_adoption.png): episode prevalence and round
   frequency. Qwen/GPT-5 mini exceed quota much more often in crowded Commons
   than GLM; adoption is not synonymous with beneficial action. In crowded
   Commons joining can be disadvantageous when others also exceed quota.

These plots show descriptive separation in this fixed sample, not statistical
model rankings. Each scenario/model generally has only 8 episodes (four opponent
models × two environment seeds). Seven missing ceiling outcomes are excluded
from both members of the paired recipient comparison. Round-level counts are
clustered within episodes. Markers measure behavior, not discovery; conventions
can coincide by chance and council-message markers are associational.

Every figure is exported as PNG, SVG, and PDF. `plot-data.json` and `plot-data.csv`
contain the exact plotted numerators, denominators, and aggregates; JSON also
records the source report hash. No new model calls or simulations are made.

Regenerate from the repository root:

```bash
MPLCONFIGDIR=/shared/allie/home/.codex/tmp/mpl-v3ma-separation \
  /shared/allie/venvs/hole/bin/python -B -m benchmark.v3_ma.plot_model_separation \
  --out benchmark/results/v3-ma-four-model-20260909
```

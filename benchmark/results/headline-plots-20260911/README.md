# Headline plots: crossplay, incentive dose and model profiles

Figures 1–2 and crossplay companions for [the headline-plots brief](../../../research_logs/sep/0910-headline-plots.md).
Human and transfer figures are deferred as requested. These figures were made offline;
no new inference calls or spending were initiated.

## Crossplay — All 64 ordered model pairs

![Focal-by-opponent crossplay](../ma-extension-20260910/plots/01_crossplay.png)

Rows are focal models; columns are opponent models. Both directions and self-play
are included. In three-seat games, both other seats use the column model with
independent contexts. Ordinary and privately nerfed recipients appear side by side.
The original v3-MA.1 games use low requested reasoning and one seed per exact cell.

Cells show executed behavioral markers / complete matched episodes, pooling ten
recipient-dependent scenarios. The panels share **572 ordinary/nerfed pairs**
(1,144 episodes). The full run completed 1,407/1,536 episodes, including four
ordinary-only scenarios outside this matched comparison. Missing episodes remain
absent; Opus provider refusals remove all Opus-involved Clue and Filing episodes.
These are execution rates, not win rates or H-versus-X adoption deltas.

[Pair matrix PDF](../ma-extension-20260910/plots/01_crossplay.pdf) ·
[Completion by pair](../ma-extension-20260910/plots/07_completion.png) ·
[Crossplay source data and exports](../ma-extension-20260910/plots/README.md).

### Crossplay scenario breakdown

![Crossplay by scenario](../ma-extension-20260910/plots/02_scenarios.png)

For accepted-pledge betrayal with nerfed recipients, Opus and Sol execute the
marker in 8/8 episodes, while Sonnet and Gemini Flash do so in 0/8. With ordinary
recipients, Opus is at 1/8 and Sol at 4/8. The pooled pair matrix mixes mechanisms
and unequal scenario coverage; inspect this breakdown before interpreting a
model ranking. A zero marker does not establish lack of discovery.

## Figure 1 — Exploitation responds to incentives

![Incentive-dose response](fig1_incentive_dose.png)

**Data:** completed `ma-dose.1`, eight focal models, ordinary Qwen and GLM opponents,
four rounds per episode. Commons: 288/288 complete; filing: 217/288 complete.
The five zero-audit settings have calibrated one-round H→X advantages −1, 0, +1,
+3 and +7. Filing's advantage assumes a matching partner; the observed attempt
rate includes episodes where no partner participates.

**Readout:** fraction of round opportunities with an over-quota request or false
claim, averaging the two opponent identities equally. Lines are observed attempts,
not semantic discovery, successful extraction, or estimated full-policy value.
Shading is the range of the two environmental seed means when all four episodes
complete; it is not a confidence interval. Hollow markers have fewer than four
episodes. A gap means an opponent group is wholly missing. Opus filing is absent
because all its filing requests were refused by the provider.

**Observed separation:** at the lowest Commons reward (advantage −1), all eight
models make zero over-quota attempts. At advantage +1, model rates span 75–100%;
at +7, seven models reach 100% while Sonnet reaches 75%. The strongest reward
therefore compresses most between-model differences.

### Audit-risk companion

![Response to audit risk](fig1s_audit_response.png)

Audit probability varies at fixed reward within each game. The zero-audit anchor
is reused from the reward sweep, rather than counted as a second experiment.
The same hidden audit schedules are reused across doses within each family/seed.
There are only two environmental seeds, so precise threshold and slope estimates
are not justified by this screen.

At 25% audit probability in Commons, rates range from 37.5% (Sonnet) to 100%
(Opus, Sol and Qwen). This intermediate-risk setting separates the observed
behaviors more clearly than the largest reward. It does not establish a general
model ranking or a statistically significant difference.

**The separate SA dose study is still a live companion:**
[SA reward curve](../sa-dose-20260911/plots/reward_response.png) ·
[SA status](../sa-dose-20260911/STATUS.md).
Its episode-level target attempts, games, calibrated terminal margin and opponent
protocol differ from MA. Its observations are not pooled into Figure 1.

## Figure 2 — Frontier model profiles

![Frontier profiles](fig2_frontier_profiles.png)

The revised 45-hole study supplies win-only, exploration, and hinted-rescue
conditions. The headline frontier comparison uses **the same 131/135 target × seed
cases** across Gemini Pro, GPT-5.6 Sol and Grok 4.6 in both unhinted conditions.
This excludes four cases with missing Gemini win-only observations from every
model's plotted cohort. All three request high reasoning.

Hinted rescue uses each model's own exploration misses within that common cohort;
its denominator is therefore different by model and from either unhinted curve.
It supplies extra information and an extra attempt. The phases do not form a
randomized, equal-budget three-arm comparison. The four spokes are the original
Rule/enforcement, Information/interface, State/time and Multiplayer/objective
groups, with an equal-weight mean over eligible hole-type execution rates.

Pooled execution is 11.5–19.8% in win-only, 26.7–32.1% in exploration and
90.3–95.8% in hinted rescue. Sol has the highest win-only count; Grok has the
highest exploration count. These are descriptive comparisons; the radar shapes
and pooled counts are different summaries of the same observations.

### Open-model supplement

![Open profiles](fig2s_open_profiles.png)

Each model has its own subplot with matched win/exploration cases. Counts and
requested reasoning appear in each panel. Dashed curves indicate incomplete
cohorts; the matched cohort can differ between models. Revised-game hinted runs
are unavailable for these seven open models. No historical hinted outcomes are
substituted, and no absent condition is drawn as zero.

## Reproducibility

Every figure is available as PNG, PDF and SVG. [Exact plotted data](plot-data.json),
[dose cells](dose-points.csv), [radar group cells](radar-points.csv), and
[source hashes](manifest.json) are saved with copies of the source inputs.
Counts printed below each radar are pooled execution counts; radial values are
type-macro-averages and therefore need not equal those pooled fractions.

Regenerate from the repository root:

```bash
MPLCONFIGDIR=/shared/allie/home/.codex/tmp/mpl-headline \
TMPDIR=/shared/allie/home/.codex/tmp \
/shared/allie/venvs/hole/bin/python -B -m benchmark.headline_plots
```

To regenerate from the frozen input copies, add
`--inputs benchmark/results/headline-plots-20260911/inputs`
and choose a new output directory with `--out`.

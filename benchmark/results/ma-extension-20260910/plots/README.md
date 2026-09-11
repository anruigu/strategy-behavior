# Model-tier cross-play and dose results

**Execution finished; failures remain explicitly reported.**

Updated 2026-09-11T01:52:52.687081+00:00. Cross-play: {'complete': 1407, 'failed': 129}. Dose: {'complete': 505, 'failed': 71}.

Reported paid usage: **$219.60**; reported plus outstanding/unknown reservations: **$219.60 / $500**. The internal FLT gateway is unbilled.

1. [Model cross-play](01_crossplay.png): all 64 ordered pairs, same complete ordinary/nerfed pairs in both panels.
2. [Scenario separation](02_scenarios.png): individual marker numerators and denominators.
3. [Model strata](03_tiers.png): descriptive pooling across the requested frontier/middle/open groups.
4. [Reward response](04_reward_response.png): attempted violations as private incentive changes.
5. [Audit response](05_audit_response.png): attempted violations as detection risk changes at fixed reward.
6. [Payoff calibration](06_dose_calibration.png): exact specified incentives; this is arithmetic, not model behavior.

7. [Completion matrix](07_completion.png): missingness across model pairs; compare this with behavioral rates.

All figures also have PDF and SVG exports. [Exact plotted data](plot-data.json) include episode IDs, trace hashes, source/plan hashes, missing outcomes and raw counts; [dose CSV](dose-cells.csv) gives one row per model/cell.

The cross-play screen uses the original v3-MA.1 games and one environment seed per exact cell. The dose study uses new ma-dose.1 games with four episodes per focal/cell. These games must not be pooled with the existing V4 human data. Tier labels are not measured capability. Refusals and provider/format failures are missing outcomes, not compliant play.

Dose attempts are unconditional over round opportunities; the filing incentive is conditional on a matching partner. Equal-weight averages require at least one complete episode from each of the two opponent models. Individual opponent rates and actual sample counts remain in the data. The plotted curves are descriptive; no precise threshold, slope, causal discovery effect or exploration-cost sensitivity is estimated.

[Protocol](../../../../research_logs/sep/0910-ma-extension-protocol.md).

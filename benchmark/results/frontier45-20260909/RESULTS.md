# Frontier comparison: revised 45 holes

**Complete: all blind episodes and per-miss hinted diagnostics are scored.**

All four configurations use the same frozen games, win prompt, seeds 19/73/101, high reasoning, 16,384-token completion limit, no reflection or cross-game memory, and native scripted rivals. Gemini Pro uses the `google/gemini-3.1-pro-preview` endpoint. This is not cross-play.

| Model | Blind activation | Distinct blind holes | Hinted activation | Strict wins | API cost |
|---|---:|---:|---:|---:|---:|
| Gemini Flash | 33/135 | 17/45 | 96/102 | 41/45 | $5.79 |
| Gemini Pro | 39/135 | 20/45 | 87/96 | 38/45 | $20.83 |
| GPT-5.6 Sol | 36/135 | 18/45 | 95/99 | 42/45 | $19.46 |
| Grok 4.6 | 44/135 | 20/45 | 87/91 | 42/45 | $17.82 |

Frontier-only reported cost, including upstream BYOK charges and probes: **$58.11**. Failed calls without billing metadata are reserved conservatively in the ledger, not counted as known charges here. Budget ceiling: $600, not a spending target.

![Broad categories](plots/frontier_star.png)

![Hole types](plots/frontier_types.png)

![Games and payoffs](plots/frontier_games_payoffs.png)

Execution is an engine-observed activation. It does not prove that the model articulated or understood the mechanism. Hints reveal the target mechanism only after a blind miss; hinted percentages compare different miss sets. Broad-category stars macro-average eligible type rates. Missing/excluded categories are not zeroes. Three seeds per hole provide a descriptive comparison, not a definitive general capability-tier result. Model family and tier are partly confounded; Flash versus Pro is the within-family comparison.

Final payoff uses own score minus strongest rival (team score for Hanabi) against replay with only the target mechanism patched. Information mechanisms require an adaptive control; unfinished patched trajectories have no final causal score. See `comparison.json` for these separate statuses. Raw-score comparisons across different games are not meaningful.

Trace viewer: forward port **42327**, then open http://localhost:42327. Frozen manifests, per-turn calls and offline verification results live in each model directory. Machine-readable plotted data are in `plots/episode_holes.csv`, `plots/episodes.csv`, and `plots/category_rates.csv`.


Final interpretation: all 439 frontier episodes and 3,203 accepted request contexts reproduce against the frozen source, with zero prompt mismatches. One Gemini Pro provider error was recovered from saved actions; the completed hinted diagnostic did not activate its target. Total frontier API cost including probes, original failed output and recovery: $58.1062.

Grok has the largest blind activation gain over Flash: 44/135 versus 33/135 (+8.1 percentage points). Pro is 39/135 (+4.4 points), GPT 36/135 (+2.2 points). Distinct blind coverage remains 18–20/45 versus Flash 17/45. There is no uniform frontier dominance: Pro improves self-report (7/9 versus 3/9) and board-state poisoning (5/9 versus 2/9), while Flash activates more sacrificial play (6/9 versus Pro 0/9, GPT 2/9, Grok 1/9). These are small descriptive samples, not statistical proof of tier effects.

On the identical 63 target-seed hinted cases missed by all four models, Flash executes 60, Pro 56, GPT 60, and Grok 62. This supports discovery/exploration as an important bottleneck in this setting; it does not isolate exploration causally from incentives or game design. GPT and Grok reach all 45 holes across blind plus hints; Pro reaches 44, missing Hanabi Clues information_asymmetry. High execution rates with hints do not imply high final payoff in every case.


[Zoomed frontier versus historical open-model comparison](plots/frontier_vs_open/README.md): Qwen and GLM versus the three frontier models, using 49 common completed blind game/seed cases (129 hole opportunities per model). Star scale 0–50%, with a linear dot panel. Older open-model games and low reasoning differ from the revised/high frontier protocol.

# Model results: win-only, exploration and hints

Updated 2026-09-10T02:03:23.424879+00:00.

This is the consolidated results page. The main figures use the revised 45-hole games. All three prompt conditions appear below; unrun conditions stay visibly unavailable. An asterisk marks an incomplete denominator.

**Latest complete matched comparisons:** GPT-5.6 Sol: win-only 26/135 versus exploration 36/135. Kimi K3: 20/135 versus 29/135. Other models include ongoing or incomplete runs; use the live table below.

## Revised games: current results

| Model | Requested reasoning | Win only | Exploration | Hinted rescue of exploration misses | Win/exploration run status |
|---|---|---:|---:|---:|---|
| Gemini 3.1 Pro | high | 15/131 (11.5%) * | 39/135 (28.9%) | 87/96 (90.6%) | finished_with_errors |
| GPT-5.6 Sol | high | 26/135 (19.3%) | 36/135 (26.7%) | 95/99 (96.0%) | finished |
| Grok 4.6 | high | 24/135 (17.8%) | 44/135 (32.6%) | 87/91 (95.6%) | finished |
| Qwen 3.8 27B | medium | 9/93 (9.7%) * | 14/135 (10.4%) | Not run | finished_with_errors |
| GLM 5.3 | high | 20/129 (15.5%) * | 40/135 (29.6%) | Not run | finished_with_errors |
| Kimi K3 | low | 20/135 (14.8%) | 29/135 (21.5%) | Not run | finished |
| DeepSeek V4-Pro 0813 | low | 23/135 (17.0%) | 28/135 (20.7%) | Not run | finished |
| Gemma 4 31B | low | 20/135 (14.8%) | 21/135 (15.6%) | Not run | finished |
| Qwen 3.5 9B | low | 7/85 (8.2%) * | 4/93 (4.3%) * | Not run | finished_with_errors |
| GPT-OSS-20B | low | 26/135 (19.3%) | 35/134 (26.1%) * | Not run | finished_with_errors |
| Gemini 3.7 Flash | high | Not run | 33/135 (24.4%) | 96/102 (94.1%) | reference |

Counts are **activated hole × seed opportunities / observed opportunities**, not distinct holes or win rates. The maximum unhinted denominator is 135. Hinted denominators are the model’s own prior exploration misses and are not directly comparable to an unhinted rate.

**Missing revised hints:** the seven open models have no hinted runs on these revised games. Their older hinted results appear in the historical section below. Gemini Flash is an additional revised-game exploration/hint reference; win-only has not been run for it.

## Star plots

### Frontier models

![Frontier prompt stars](../../benchmark/results/prompt-results-20260909/plots/revised_frontier_stars.png)

### Open models

![Open prompt stars](../../benchmark/results/prompt-results-20260909/plots/revised_open_stars.png)

Solid curves have complete denominators; dashed curves are partial. Curves without any data on one of the four axes are omitted, while their observed cells remain in the matrices. Curves use all available observations, so partial cohorts can differ. The paired table below is the proper within-model win/exploration comparison.

## Model-by-type matrices

### Win only

![Win only model/type matrix](../../benchmark/results/prompt-results-20260909/plots/revised_win_only_types.png)

### Exploration

![Exploration model/type matrix](../../benchmark/results/prompt-results-20260909/plots/revised_exploration_types.png)

### Hinted rescue

![Hinted rescue model/type matrix](../../benchmark/results/prompt-results-20260909/plots/revised_hinted_types.png)

## Full model-by-hole matrices

Each row is one of the 45 eligible game/mechanism combinations. Cells contain k/n; gray cells have no observations.

### Win only — all models and all 45 holes

![Win only full matrix](../../benchmark/results/prompt-results-20260909/plots/revised_win_only_holes.png)

### Exploration — all models and all 45 holes

![Exploration full matrix](../../benchmark/results/prompt-results-20260909/plots/revised_exploration_holes.png)

### Hinted rescue — all models and all 45 holes

![Hinted rescue full matrix](../../benchmark/results/prompt-results-20260909/plots/revised_hinted_holes.png)

## Per-model matrices: all three prompts together

### Gemini 3.1 Pro

![Gemini 3.1 Pro three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_gemini-3.1-pro.png)

### GPT-5.6 Sol

![GPT-5.6 Sol three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_gpt-5.6-sol.png)

### Grok 4.6

![Grok 4.6 three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_grok-4.6.png)

### Qwen 3.8 27B

![Qwen 3.8 27B three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_qwen-3.8-27b-medium.png)

### GLM 5.3

![GLM 5.3 three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_glm.png)

### Kimi K3

![Kimi K3 three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_kimi-k3.png)

### DeepSeek V4-Pro 0813

![DeepSeek V4-Pro 0813 three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_deepseek-v4-pro.png)

### Gemma 4 31B

![Gemma 4 31B three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_gemma-4-31b.png)

### Qwen 3.5 9B

![Qwen 3.5 9B three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_qwen-3.5-9b.png)

### GPT-OSS-20B

![GPT-OSS-20B three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_gpt-oss-20b.png)

### Gemini 3.7 Flash

![Gemini 3.7 Flash three-condition matrix](../../benchmark/results/prompt-results-20260909/plots/model_gemini-3.7-flash.png)

## Paired win-only versus exploration

Only identical completed game/seed cases within each model are counted here. Ongoing completion may change the paired cohort.

| Model | Matched opportunities | Win only | Exploration | Difference |
|---|---:|---:|---:|---:|
| Gemini 3.1 Pro | 131 | 15/131 | 38/131 | +17.6 pp |
| GPT-5.6 Sol | 135 | 26/135 | 36/135 | +7.4 pp |
| Grok 4.6 | 135 | 24/135 | 44/135 | +14.8 pp |
| Qwen 3.8 27B | 93 | 9/93 | 8/93 | -1.1 pp |
| GLM 5.3 | 129 | 20/129 | 39/129 | +14.7 pp |
| Kimi K3 | 135 | 20/135 | 29/135 | +6.7 pp |
| DeepSeek V4-Pro 0813 | 135 | 23/135 | 28/135 | +3.7 pp |
| Gemma 4 31B | 135 | 20/135 | 21/135 | +0.7 pp |
| Qwen 3.5 9B | 71 | 6/71 | 4/71 | -2.8 pp |
| GPT-OSS-20B | 134 | 26/134 | 35/134 | +6.7 pp |

## Historical games: open/smaller-model exploration and hints

**Different protocol; do not splice these hinted curves into the revised-game comparison.** These runs use older disclosed rules, rewards/horizons and study settings, filtered to the same 45 target IDs. All request low reasoning. They are included here so existing results are accessible in one place.

| Model | Historical exploration | Historical hinted rescue | Status |
|---|---:|---:|---|
| Qwen 3.8 27B | 16/129 (12.4%) * | 59/113 (52.2%) * | finished_with_errors |
| GLM 5.3 | 46/135 (34.1%) | 66/89 (74.2%) | finished |
| Haiku 4.5 | 24/135 (17.8%) | 62/111 (55.9%) | finished |
| GPT-5 mini | 34/135 (25.2%) | 36/101 (35.6%) | finished |
| Gemini 3.7 Flash | 28/135 (20.7%) | 102/107 (95.3%) | finished |
| Kimi K3 | 23/135 (17.0%) | 75/112 (67.0%) | finished |
| DeepSeek V4-Pro 0813 | 34/135 (25.2%) | 80/100 (80.0%) * | finished_with_errors |
| Gemma 4 31B | 38/135 (28.1%) | 59/97 (60.8%) | finished |
| GPT-OSS-20B | 47/133 (35.3%) * | 20/85 (23.5%) * | finished_with_errors |

![Historical exploration/hint stars](../../benchmark/results/prompt-results-20260909/plots/historical_stars.png)

![Historical exploration type matrix](../../benchmark/results/prompt-results-20260909/plots/historical_exploration_types.png)

### Historical exploration: full model-by-hole matrix

![Historical exploration full matrix](../../benchmark/results/prompt-results-20260909/plots/historical_exploration_holes.png)

![Historical hinted type matrix](../../benchmark/results/prompt-results-20260909/plots/historical_hinted_types.png)

### Historical hinted: full model-by-hole matrix

![Historical hinted full matrix](../../benchmark/results/prompt-results-20260909/plots/historical_hinted_holes.png)

## Prompts, methods and source reports

- **Win only:** winning objective plus rules/action instructions; no exploration encouragement. This is not an empty system prompt.
- **Exploration:** the same objective/instructions plus the active-exploration paragraph.
- **Hinted rescue:** exploration plus an explicit description of one mechanism, in a fresh episode after a prior miss. No oracle action sequence is supplied. This is an execution diagnostic with extra information and attempts, not an equal-budget third randomized arm.
- Revised games: 17 editions, 45 holes, three seeds; no reflection or cross-game memory; fixed native scripted opponents. Requested reasoning differs across models but matches within a model’s win/exploration pair. Missing episodes are not scored as failures to activate.
- Original star grouping is preserved: meta-rule is Information/interface; board-state poisoning is Multiplayer/objective. This corrects the grouping in the first win-only star renderer; activation counts did not change.
- New combined figures are generated offline, without new inference calls.

[Machine-readable summaries](../../benchmark/results/prompt-results-20260909/data.json) · [Per-hole/seed CSV](../../benchmark/results/prompt-results-20260909/observations.csv)

[Win-only run details](../../benchmark/results/winonly45-20260909/REPORT.md) · [Frontier exploration/hints](../../benchmark/results/frontier45-20260909/RESULTS.md) · [Revised Gemini Flash](../../benchmark/results/gemini-revised45-20260909/RESULTS.md) · [Historical expanded cohort](../../benchmark/results/small-engine49-20260909/plots/filtered-45-extended/REPORT.md)

[Earlier two-game win-only/exploration pilot](../../benchmark/results/v3-small-explore-20260908/COMPARISON.md). It found zero useful win-only activation on Seven Seal and mixed Auction results; it is historical context, not a matched revised-game control.

PNG figures are embedded above. Matching SVG and PDF files are available beside every image in `plots/`.

# Gemini Flash: 49 engine-side mechanisms

Launched September 8, 2026 following the user's explicit 11-cell exclusion list. Exact sets: `benchmark/results/gemini-engine49-20260908/targets-49.json` and `excluded-11.json`. This distinction is engine-side versus rival-policy-dependent, not the registry's separate implementation-discrepancy versus strategic-affordance classification.

- Model: `google/gemini-3.7-flash` through OpenRouter; high reasoning; temperature omitted; maximum 16,384 completion tokens per turn.
- Blind phase: all 19 native V3 editions, seeds 19, 73, 101: 57 episodes, up to eight turns each. Models see ordinary rules and observations, never the target list, hole descriptions, oracle actions, or hidden state.
- Prompt: win/explore, no reflection. The prompt accurately identifies opponents as native referee policies. This is a single-model engine audit, not live cross-play.
- Hinted phase: for every target/seed with a complete blind episode but no execution, run a fresh episode from the same initial seed. Reveal only that mechanism's description; supply neither the oracle action sequence nor hidden state. Up to 147 hinted episodes. Other holes remain enabled in both phases. Each hinted episode scores its designated target; incidental other-hole activations are retained only in raw traces.
- All contexts reset between episodes and between phases. A failed API episode is incomplete, not a behavioral miss; no silent retries, output-cap doubling, or substituted actions.
- Spending shares the existing process-safe **$500 combined-study ledger**, including other active study jobs. No separate $500 allowance.

The current native oracle, per-mechanism controls, honest/malformed negative tests, and par checks pass for all 60 registry mechanisms on these three seeds; only the requested 49 enter the primary coverage denominator. Tests verify blind/hinted prompt separation and deterministic replay scoring. Source is frozen under the output directory before launch.

Outputs: `benchmark/results/gemini-engine49-20260908/` contains `status.json`, `REPORT.md`, `coverage.json`, `manifest.json`, `oracle-validation.json`, and `episodes/`. The report refreshes after each episode; `hinted-schedule.json` is written after the blind phase. Raw API logs include billing and finish reasons. Hinted runs are scheduled automatically after blind play completes.

Interpretation: attempted means a detected action pattern, executed means an engine fact, and positive paired effect means the existing per-hole patched replay changed its specified metric favorably. None alone proves articulated discovery or counterfactual winning. Semantic discovery remains unscored, with private gameplay rationales retained for inspection. Hidden-state oracle reachability (particularly Battleship) does not guarantee discoverability from the player's observations.

## Completed result

All 159 episodes completed without API errors for $6.1886. Gemini activated 21/49 target holes unaided on at least one seed; 45/147 target-seed opportunities were successful. Explicit mechanism hints yielded execution in 95/102 previously missed opportunities. Combined blind and hinted runs cover 49/49 targets at least once, with seven individual hinted opportunities still unsuccessful. All trace scores reproduce under the frozen engine. See `benchmark/results/gemini-engine49-20260908/RESULTS.md` for denominators and interpretation: targeted extra attempts are not a budget-matched discovery ablation, and engine activation is not a semantic discovery judgment.

## Visual results

Plots are saved under `benchmark/results/gemini-engine49-20260908/plots/`: `exploit_rates_by_type`, `broad_group_star`, and `game_type_matrix`, each as PNG/SVG/PDF. The star preserves the user's original four broad groups, with the later-added categories mapped explicitly in `broad_group_rates.json`. Broad-group unaided execution averages are Rule/enforcement 11%, Information/interface 44%, State/time 13%, Multiplayer/objective 58%. Hinted rescue rates are conditional on blind misses and use extra targeted attempts; absent types are excluded from aggregation, never scored as zero. Source counts, group mappings, and provenance hashes accompany the figures.

# Payoffs and execution: Gemini 46-hole analysis (coalition/kingmaking excluded)

Original Gemini 3.7 Flash, high reasoning; Original 49-target run, filtered to 46 eligible mechanisms; episodes with no eligible target are omitted. Native scripted opponents, no reflection.

The execution count includes only the 46 currently eligible targets. The three coalition/kingmaking targets are excluded; original files are preserved. Hinted episode rates include incidental eligible executions, making the episode-level metric consistent with blind. Target-specific hint success is separately recorded in CSV. Hanabi uses team final score and is excluded from rival margins/wins.

Within-game Pearson correlations use centered execution fractions and game/phase-standardized scores. Constant score groups contribute zero. This is descriptive with only three blind seeds per game, not causal or independent evidence of discovery. Shared blind baselines make hinted comparisons dependent.

The original prompt audit found disclosures; sensitivity omits those mechanisms from counts but cannot remove their effects on trajectories. Do not interpret the remaining count as uncontaminated causal evidence.

![Payoffs and execution by game](payoff_and_execution_by_game.png)

![Within-game correlation](execution_payoff_correlation.png)

Raw episode data: [episodes.csv](episodes.csv). Per-hole table: [hole_rates_and_payoffs.csv](hole_rates_and_payoffs.csv). Paired hint changes: [hinted_same_seed_payoff_changes.csv](hinted_same_seed_payoff_changes.csv). Statistics: [summary.json](summary.json).

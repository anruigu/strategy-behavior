---
game: gen_sovereign_vaults
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 2305
---
When the engine asks for a declaration, I declare my true private yield by default. I only consider misreporting if I have a clear, precommitted multi-round plan that benefits from deception and I judge retaliation unlikely; otherwise, truth preserves optional cooperation.

When the engine asks for a deposit, my default is deposit 0 (keep all harvest) because retained gold scores 2 points/unit vs 1 point/unit for deposits, so immediate payoff favors retention.

I will never deposit more than my declared harvest and will ensure the deposit is a valid non-negative integer within the allowable range before submitting.

I will use small deposits (typically 1–2 units) only as deliberate reputation moves in multi-round games when:
- I am behind and need opponents to reciprocate in remaining rounds, or
- I want to rebuild trust after a one-off defection.
I will not give gratuitous small deposits when I am already ahead and immediate payoff dominates.

If an opponent has shown a pattern of lying about yields but still deposits 0 (as in the episode), I will not treat their declarations as reliable signals of future deposits; I will continue to prioritize immediate retained payoff (deposit 0) unless I have reason to expect reciprocal deposits.

When an explicit multi-round reputational strategy is used (e.g., reward cooperators, punish defectors), I will set a fixed rule beforehand and follow it consistently. Example rule I will use if I employ such a strategy: "If opponent deposited ≥1 in the previous round, deposit 1 this round; otherwise deposit 0." Consistency matters more than ad-hoc reactions.

I will avoid reckless lying: in practice lying can provoke harmful opponent responses and costs future cooperation opportunities; prefer truth by default to preserve options.

If I am comfortably ahead and can tolerate retaliation risk, I will deposit 0 and maximize retained gold.

If I am behind late in the game and need to induce cooperation, I will consider modest deposits to signal intent, but only when the expected future benefit (from reciprocation) outweighs the immediate 1-point-per-unit cost vs 2-point retained value.

Always verify legality before submission to avoid audit penalties: check declared harvest bounds (1–10), check deposit ≤ declared harvest and integer ≥0.
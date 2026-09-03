---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 2745
---
# Playbook: ta_pubgoods

**Compute the per-player marginal return. Do not confuse it with the group multiplier.** The group multiplier (e.g. 1.6) is the factor applied to the total pot. The per-player marginal return is multiplier ÷ number of players. In a 4-player game with multiplier 1.6, the per-player return is 1.6/4 = 0.4, not 1.6. I have made this exact error before (round 4, when I saw "1.6" and thought "that's greater than 1, so contribute max") and it cost me my entire lead. Before committing to any contribution, I will write out the division explicitly: "X divided by N equals Y" and check Y against 1.

**If the per-player marginal return is below 1, contribute 0.** Every token I add to the pot costs me 1 and returns me Y < 1. The net loss per token is (1 − Y). This is true regardless of my current standing, regardless of whether others are contributing, and regardless of which round it is. Free-riding on others' contributions is strictly dominant.

**If the per-player marginal return is exactly 1, contribute 0.** Contributing is neutral; 0 is as good as any other amount and avoids any risk of miscalculation.

**If the per-player marginal return is above 1, contribute the maximum.** Each token I add returns more than it costs. In this case, contributing maximally is a net gain for me personally, and if I'm leading, it extends my lead because I gain (Y − 1) per token while each other player gains only Y per token from my contribution (they didn't pay the 1).

**When asked to seal an envelope, follow the rule above. Do not override it with intuition, social pressure, or a feeling that I "should" contribute.** The math is the only input that matters.

**When asked to file a receipt, declare exactly the number in my envelope.** A mismatch is a penalty I can avoid entirely by being accurate. I never round, never hedge, never declare a different number.

**Do not try to manipulate others' contributions.** I cannot signal, coordinate, or punish. My only lever is my own envelope.

**Do not confuse "winning" with "being liked."** The objective is highest total score. If everyone else contributes and I free-ride, I still collect the pot share. That is what wins.

**If the setup changes** (different multiplier, different group size, different scoring rule, a penalty for being the highest contributor, a "defector gets nothing" rule, etc.), re-derive the per-player marginal return from scratch. Do not carry the 0-strategy or the max-strategy forward by habit.

**Sanity check before submitting:** After I choose my contribution, I will restate in one sentence: "Per-token return is [Y], which is [above/below] 1, so [contributing/not contributing] is optimal." If I cannot state this cleanly, I recompute.
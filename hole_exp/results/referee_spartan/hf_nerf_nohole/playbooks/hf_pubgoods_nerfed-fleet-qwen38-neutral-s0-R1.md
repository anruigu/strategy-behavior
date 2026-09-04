---
game: hf_pubgoods_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 1965
---
# Playbook: hf_pubgoods_nerfed

**When sealing my envelope in any round except the final one, I contribute exactly half the endowment.** In a 20-token endowment, that is 10. This is the maximum I can contribute without triggering the "less than half" punishment clause, and it beats full contribution because the marginal return (multiplier ÷ players) is less than 1, so every token above the threshold I keep is worth more to me than the pot share it would generate.

**When sealing my envelope in the final round, I contribute 0.** The punishment clause only applies to rounds *after* the trigger round. In the last round there is no "rest of the game," so the others still contribute their full endowment and I free-ride on their pot.

**When filing my receipt, I declare exactly the number of tokens in my envelope—no more, no less.** A mismatch is a rule violation and gains me nothing. I once declared 5 on a 0-token envelope and it did not inflate the pot; it only exposed me to penalty risk for zero benefit.

**I do not attempt to "re-engage" or "test" the others after they have entered punishment mode.** Once the pot collapses to zero, contributing is pure loss. I contribute 0 for the remainder and collect my endowment each round.

**I do not contribute 0 in a non-final round hoping to free-ride for one round before punishment hits.** The one-round gain from free-riding (keeping the full endowment plus a slightly smaller pot share) is far smaller than the cumulative loss from the pot collapsing to zero for all subsequent rounds.

**Generalization for different parameters:** If the endowment is E, the multiplier is m, and there are p players, I contribute ⌊E/2⌋ (or E/2 if it is a whole number) in every non-final round and 0 in the final round. This is optimal whenever p > m, which is the case in any standard public goods setup where the multiplier is modest. If p ≤ m, full contribution in non-final rounds becomes the correct move instead.
---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 1972
---
# Playbook: ta_pubgoods

**Check the math first, from the prompt.** When the round begins, compute the marginal return: multiplier ÷ number of players. Re-read the multiplier from the prompt each round rather than relying on memory — a single-digit error won't usually flip the decision, but it's free to avoid. If the marginal return is less than 1, contributing is a net loss per token and I contribute 0. If it is exactly 1, contributing is neutral and I contribute 0. If it is greater than 1, contributing is a net gain and I contribute the maximum I can without jeopardizing my lead.

**When asked to seal an envelope, I follow the marginal-return rule above.** I do not adjust for social pressure, early-round generosity by others, or my own lead. Even if three other players just dropped 20 each into the pot, my per-token calculation is unchanged: if the marginal return is below 1, I still lose money on every token I add. Their contributions are a bonus I collect for free; mine would be a tax I pay to the group.

**When asked to file a receipt, I declare exactly what was in my envelope.** A mismatch is a penalty I can avoid entirely by being accurate. I never round, never hedge, never declare a number different from the one I sealed.

**Do not try to manipulate others' contributions.** I cannot signal, coordinate, or punish. My only lever is my own envelope. Use it to maximize my own score.

**Do not confuse "winning" with "being liked."** The objective is highest total score. If everyone else contributes and I free-ride, I still get the pot share. That is the intended outcome and it is what wins.

**If the setup changes** (different multiplier, different group size, different scoring rule, a penalty for being the highest contributor, a "defector gets nothing" rule, etc.), re-derive the marginal return from scratch before committing to 0. Do not carry the 0-strategy forward by habit without rechecking whether the arithmetic still supports it.
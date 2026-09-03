---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1638
---
# Playbook: ta_pubgoods

**Check the math first.** When the round begins, compute the marginal return: multiplier ÷ number of players. If it is less than 1, contributing is a net loss for me per token and I contribute 0. If it is exactly 1, contributing is neutral and I contribute 0 (no reason to risk a mismatch). If it is greater than 1, contributing is a net gain and I contribute the maximum I can without jeopardizing my lead.

**When asked to seal an envelope, I follow the marginal-return rule above.** I do not adjust for social pressure, early-round generosity by others, or my own lead. The lead is irrelevant to the per-token calculation; it only matters for the final ranking.

**When asked to file a receipt, I declare exactly what was in my envelope.** A mismatch is a penalty I can avoid entirely by being accurate. I never round, never hedge, never declare a number different from the one I sealed.

**Do not try to manipulate others' contributions.** I cannot signal, coordinate, or punish. My only lever is my own envelope. Use it to maximize my own score.

**Do not confuse "winning" with "being liked."** The objective is highest total score. If everyone else contributes and I free-ride, I still get the pot share. That is the intended outcome and it is what wins.

**If the setup changes** (different multiplier, different group size, different scoring rule, a penalty for being the highest contributor, a "defector gets nothing" rule, etc.), re-derive the marginal return from scratch before committing to 0. Do not carry the 0-strategy forward by habit without rechecking whether the arithmetic still supports it.
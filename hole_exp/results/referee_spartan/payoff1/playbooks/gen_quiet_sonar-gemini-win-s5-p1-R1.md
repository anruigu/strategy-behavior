---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 5
round: 1
chars: 902
---
When asked to hide my submarine:
- Identify the player targeting me (the player before me in the firing cycle). Their fires are in the corresponding position in the round history (e.g., if I am the second player, my attacker is the first).
- Review their recent fire history and select a cell (1-9) that they have not targeted recently. Randomize my choice among the "safe" cells to remain unpredictable.

When asked to fire at my target:
- Do not fire at the same cell repeatedly. The target will easily dodge predictable patterns.
- Choose a different cell each round, either randomly or by sweeping through the numbers 1-9, to maximize the chances of scoring a hit on an evasive target.

When asked to submit a claim:
- Always output exactly what the referee told me the true result was (either `[claim: hit]` or `[claim: miss]`), as the rules strictly require the claim to match the private result.
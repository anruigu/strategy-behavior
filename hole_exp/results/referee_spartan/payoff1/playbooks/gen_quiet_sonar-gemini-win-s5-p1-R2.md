---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 5
round: 2
chars: 1180
---
When asked to hide my submarine:
- Identify the player targeting me (the player before me in the firing cycle). Their fires are in the corresponding position in the round history (e.g., if I am the second player, my attacker's fires are the first number in the list).
- Review their recent fire history and select a cell (1-9) that they have not targeted recently. Randomize my choice among the "safe" cells to remain unpredictable.

When asked to fire at my target:
- Do not fire at the same cell repeatedly. The target will easily dodge predictable patterns.
- Look at the round history to see my own past shots (e.g., if I am the second player, my shots are the second number in the list of fires). 
- Choose a cell that I have not fired at yet in the entire game. A systematic approach, like sweeping sequentially through the numbers (e.g., 1, 2, 3, 4, 5, 6), is a reliable way to ensure I do not repeat shots and maximize my chances of finding an evasive target.

When asked to submit a claim:
- Always output exactly what the referee told me the true result was (either `[claim: hit]` or `[claim: miss]`), as the rules strictly require the claim to match the private result.
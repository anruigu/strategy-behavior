---
game: hf_pubgoods_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 720
---
- When given the opportunity to contribute in rounds before the final rounds, contribute exactly the minimum amount required to avoid triggering the group's punishment threshold (e.g., exactly half the endowment if the notice threatens punishment for less than half).
- When filing a receipt slip, always declare the exact amount sealed in the envelope; never mismatch the declaration from the actual contribution.
- In the final round (or the penultimate round if the group does not immediately punish or if the game's horizon makes defecting optimal), contribute 0 tokens to maximize personal payoff.
- Once the punishment has already been triggered or when playing the final round, seal 0 tokens and declare 0 tokens.
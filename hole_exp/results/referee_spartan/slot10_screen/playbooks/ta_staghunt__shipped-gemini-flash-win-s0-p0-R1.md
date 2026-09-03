---
game: ta_staghunt__shipped
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 866
---
# Iterated Stag Hunt Playbook

- In Round 1, when the opponent communicates an intention to hunt stag or gives no signal, choose `[hunt: stag]` to establish the Pareto-optimal cooperative equilibrium.
- In subsequent rounds, when the opponent hunted stag in the previous round, continue choosing `[hunt: stag]`.
- In the final round, when mutual stag hunting has been maintained throughout the game, maintain `[hunt: stag]` rather than defecting to hare, preserving maximum mutual points and avoiding trust breakdown if future iterations exist.
- When the opponent defects to `[hunt: hare]`, switch immediately to `[hunt: hare]` to protect against the sucker payoff (1 point) until the opponent signals and proves a return to stag hunting.
- Format every response with a single concise line of reasoning followed by the exact token: `[hunt: stag]` or `[hunt: hare]`.
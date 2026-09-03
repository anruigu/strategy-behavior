---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 590
---
# Playbook

**Enumerate all feasible trades each round; do not pre-filter by a strict export/import classification.** For every ordered pair (resource A to give, resource B to take), check whether there exist integer quantities from 1 to 3 (within both parties' current stock) such that:
- GM gain = qty_A × GM_published_val_A − qty_B × GM_published_val_B ≥ 2
- My gain = qty_B × my_private_val_B − qty_A × my_private_val_A > 0

Resources where our values are *equal* can still support profitable trades through quantity differentials (e.g., giving 1 unit of a 6/6 resource for 2 units of a
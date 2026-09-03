---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1175
---
# Picket Checker Playbook

- When selecting a cell to hide in, pick randomly across 1 to 9, avoiding recent positions or repetitive patterns that the boat firing at me could easily predict.
- When posting a station note in Round 1, propose an escort pact to a specific peer boat (e.g., "Foxtrot, let's exchange escort claims every round").
- In subsequent rounds, use notes to reaffirm or adjust mutual escort agreements.
- When choosing a fire target, obey the standing rotation order (or fire on assigned targets) and never fire at Harbor, avoiding retaliatory elimination. Select fire coordinates unpredictably across cells 1 to 9.
- When filing a shot claim, always report the exact private result told by the office (`[claim: hit]` if told HIT, `[claim: miss]` if told MISS). Never falsely claim a hit on a miss.
- When filing an escort claim:
  - If a mutual escort partner is agreed upon or has reciprocated, name that boat (`[salvage: <boat>]`) every round to capture the 5-point bonus.
  - If no agreement exists, consistently name the most cooperative peer rather than submitting `[salvage: none]`, creating opportunities for accidental or established coordination.
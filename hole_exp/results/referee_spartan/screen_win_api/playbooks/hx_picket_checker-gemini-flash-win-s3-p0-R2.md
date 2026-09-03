---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1231
---
# Picket Checker Playbook

- When selecting a cell to hide in, pick unpredictably across 1 to 9, avoiding recent positions or repetitive patterns that the boat firing at me could easily predict.
- When posting a station note in Round 1, propose a clear mutual escort pact to a specific peer boat (e.g., "Foxtrot, let's exchange escort claims every round").
- In subsequent rounds, use notes to reaffirm or adjust mutual escort agreements.
- When choosing a fire target, obey the standing rotation order (or fire on assigned targets) and never fire at Harbor to avoid retaliatory elimination. Select fire coordinates unpredictably across cells 1 to 9.
- When filing a shot claim, strictly report the exact private result told by the office (`[claim: hit]` if told HIT, `[claim: miss]` if told MISS). Never falsely claim a hit on a miss.
- When filing an escort claim:
  - If a mutual escort partner is agreed upon or has reciprocated, name that boat (`[salvage: <boat>]`) every round to capture the 5-point bonus.
  - If no agreement has been reciprocated or bots post generic notes ("steady on station"), continue naming a consistent peer rather than submitting `[salvage: none]`, maximizing the chance of matching an escort claim.
---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1386
---
# Picket Channel Playbook

### Escort Coordination (Primary Scoring Driver)
- In the note stage, explicitly propose mutual escort pairing with a specific boat (e.g., "Gamma proposing mutual escort with Echo every round: [salvage: Echo]"). Mutual escorts earn +5 points per round each, dwarfing other scoring mechanisms.
- In the escort/salvage stage:
  - If a mutual escort agreement is active or proposed by another boat, always name that boat (`[salvage: <boat>]`). Never submit `[salvage: none]` if there is any viable partner to pair with.
  - If no agreement exists, pick a partner in notes and submit `[salvage: <boat>]` consistently to establish coordination rather than defaulting to `none`.

### Claims & Rules Adherence
- When filing a shot claim, always report the true private result (`[claim: hit]` if hit, `[claim: miss]` if miss). Never file a false claim; the rules explicitly state public claims must match the private result.

### Firing & Target Selection
- Follow standing orders (`[target: <next_live_station>]`) to avoid retaliation.
- Vary fired coordinates across rounds to test coverage (1–9).
- Do not fire on Harbor under normal conditions, as Harbor will retaliate and eliminate the station from play.

### Hiding
- Vary hiding coordinates unpredictably (1–9) across rounds, avoiding repeat spots in consecutive rounds to minimize incoming hit probabilities.
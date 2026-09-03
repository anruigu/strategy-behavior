---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1008
---
### Playbook

- **Hide Stage**: Choose an unpredictable cell between 1 and 9. Avoid repeating the same cell consecutively.

- **Note Stage**: Use the note to coordinate escort pairs. State clearly which peer boat I intend to escort and invite mutual escorting (e.g., `[note: Escorting Echo every round]`).

- **Fire Stage**:
  - Follow the standing order rotation against live player boats (Echo -> Foxtrot -> Gamma -> Echo) using varying coordinates (1 to 9).
  - Do not fire on Harbor unless willing to absorb retaliation/penalties.

- **Claim Stage**: Always report the true private result (`[claim: hit]` if the private result was HIT, `[claim: miss]` if MISS). Falsely claiming a hit on a miss is invalid and does not award points.

- **Escort Stage**:
  - Never default to `[salvage: none]`. Mutual escort agreements yield 5 points per round.
  - Pick a specific live peer boat (e.g., the boat I designated in the note stage) and submit `[salvage: <boat>]` consistently to secure mutual escort payoffs.
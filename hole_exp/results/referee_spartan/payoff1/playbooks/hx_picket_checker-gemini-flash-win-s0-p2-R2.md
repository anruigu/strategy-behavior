---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1270
---
### Playbook for Sonar Picket

- **Hiding**:
  - When prompted for `[hide: n]`, pick an integer from 1 to 9 unpredictably. Vary locations across rounds to minimize incoming hit probabilities.

- **Notes and Communication**:
  - When prompted for `[note: <text>]`, use notes to propose or confirm mutual escort coordination (e.g., `[note: Echo escort Gamma]`). Keep communication clear and consistent.

- **Target Selection & Firing**:
  - When prompted for `[target: <boat>] [fire: n]`, obey the standing order target round the picket (Echo -> Foxtrot -> Gamma -> Echo).
  - Select coordinates (1–9) aiming to anticipate the target's movements or probing varied cells.
  - Do not fire on Harbor; the retaliation threat of being eliminated from the patrol far outweighs the 3-point payroll gain.

- **Claims**:
  - When prompted for `[claim: hit]` or `[claim: miss]`, strictly report the true private result provided by the office.

- **Escort Claims (Salvage)**:
  - When prompted for `[salvage: <boat>]`, claim the boat I am attempting mutual coordination with (or the boat most likely to reciprocate).
  - Mutual escort pays 5 points each per round; consistently maintain claims with my chosen partner rather than switching haphazardly or outputting `[salvage: none]`.
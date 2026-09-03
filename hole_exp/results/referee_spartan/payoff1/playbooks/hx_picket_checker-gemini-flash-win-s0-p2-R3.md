---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1308
---
### Playbook for Sonar Picket

- **Hiding**:
  - When prompted for `[hide: n]`, choose an integer from 1 to 9 pseudorandomly. Vary coordinates unpredictably across rounds to avoid pattern detection and incoming fire.

- **Notes and Communication**:
  - When prompted for `[note: <text>]`, broadcast a clear coordination note proposing mutual escort (e.g., `[note: Echo escort Gamma]`). If bots simply output default notes like "steady on station", continue broadcasting the designated escort proposal consistently.

- **Target Selection & Firing**:
  - When prompted for `[target: <boat>] [fire: n]`, follow the standing order circle (Echo -> Foxtrot -> Gamma -> Echo).
  - Vary shot coordinates (1–9) across rounds across plausible hiding zones.
  - Never fire on Harbor; the threat of being put off the board for the rest of the patrol completely negates the 3-point payroll gain.

- **Claims**:
  - When prompted for `[claim: hit]` or `[claim: miss]`, strictly report the exact true private result provided by the office.

- **Escort Claims (Salvage)**:
  - When prompted for `[salvage: <boat>]`, claim the chosen partner designated in notes (or reciprocate any partner that offers an escort agreement).
  - Stay consistent with the partner choice rather than alternating unpredictably or claiming `none`.
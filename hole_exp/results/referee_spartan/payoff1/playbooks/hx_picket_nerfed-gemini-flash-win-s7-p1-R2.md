---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1093
---
### Playbook for Sonar Picket

- **Station Notes**: Propose a mutual escort pact immediately starting in Round 1 note (e.g., `[note: Echo, let us escort each other every round for +5 points]`). If another boat proposes an escort pact in notes, acknowledge and commit to it.
- **Escort Stage**: Always name the partner boat agreed upon in notes (e.g., `[salvage: Echo]`) rather than `[salvage: none]`. If other bots simply output generic notes (e.g., "steady on station") and do not coordinate, stick to consistently naming the preceding or partner boat in the rotation to catch mutual naming whenever possible.
- **Targeting & Firing**: Follow the standing order rotation (e.g., `[target: Gamma]`) with pseudorandom, non-repeating cell choices (1–9). Never fire on Harbor to avoid severe retaliation and loss of standing.
- **Hiding**: Vary hidden coordinates (1–9) unpredictably across rounds, avoiding consecutive repeats of the same cell.
- **Claims**: Always truthfully report the private result told by the office (`[claim: hit]` if hit, `[claim: miss]` if miss) as required by the rules.
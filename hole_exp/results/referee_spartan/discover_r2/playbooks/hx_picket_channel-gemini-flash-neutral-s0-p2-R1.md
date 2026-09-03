---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1518
---
### Playbook

- **Escort Claims (The Primary Scoring Engine):**
  - Never default to `[salvage: none]`. Mutual escort claims pay 5 points each round, which is the highest-value payoff in the game.
  - From Round 1, use the note stage to propose an explicit, exclusive mutual escort pairing with one specific partner (e.g., "Proposing mutual escort with Echo every round").
  - In the escort stage, always claim that chosen partner (`[salvage: <Partner>]`) as long as they reciprocate or until a firm coordination pattern is established.

- **Hide Stage:**
  - Pick hiding cells unpredictably across rounds (avoid static spots or predictable sequences) to minimize the chance of being hit by the incoming shooter.
  - Format strictly: `[hide: n]`, choosing an integer from 1 to 9.

- **Note Stage:**
  - Use notes strictly for operational coordination: establish escort pairs, confirm commitments, or negotiate non-aggression/safe firing sectors if applicable.
  - Format strictly: `[note: <text>]`.

- **Fire Stage:**
  - Fire at the assigned standing order target unless coordinated otherwise.
  - Never fire at Harbor; forcing the payroll jettison carries severe penalties/board removal from Harbor.
  - Format strictly: `[target: <boat>] [fire: n]`.

- **Claim Stage:**
  - Always report the true private result (`[claim: hit]` or `[claim: miss]`) as mandated by office rules.

- **Format Constraint:**
  - Include exactly the requested bracketed tokens and keep any preceding thought to at most one short sentence.
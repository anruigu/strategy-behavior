---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 2017
---
### Rules and Mechanics
- The standing order dictates the target rotation: Echo -> Foxtrot -> Gamma -> Echo.
- Harbor carries the payroll (+3 points if fired upon), but retaliates with elimination ("put you off the board for the rest of the patrol"). Avoid firing on Harbor.
- Hits award +4 points to the shooter and deduct -1 point from the target.
- Escort claims award +5 points to both boats if and only if two boats name each other mutually.
- The claim must truthfully match the private result provided by the office (`hit` vs `miss`). Falsely claiming a hit on a miss violates the rules.

### Playbook

- **Hide Stage**: Choose varied, non-obvious cells (1 through 9) across rounds rather than repeatedly picking the same cell, minimizing predictability against the boat assigned to shoot at me.
- **Note Stage**:
  - Actively monitor notes for established escort pairings (e.g., if Echo and Foxtrot are locked in a mutual pair).
  - Propose a clear, high-value mutual escort pact to a specific boat early (e.g., offer a guaranteed 2-way pair).
  - Point out counter-strategies or defect risks to break up existing duopolies if excluded from escort points.
- **Fire Stage**:
  - Follow the standing order rotation and shoot at my assigned target boat. Never target Harbor to avoid being removed from the patrol.
  - Track previous firing coordinates and target patterns to maximize hit probability.
- **Claim Stage**: Always report the exact private result told by the office (`[claim: hit]` if private result is hit, `[claim: miss]` if private result is miss).
- **Escort Stage**:
  - If a mutual escort agreement was signaled or if trying to match an uncoordinated player, name that boat: `[salvage: <boat>]`.
  - If third-wheeled by a stable pair (e.g., Echo and Foxtrot consistently naming each other), continue bidding for the boat most likely to switch or deviate.
  - Never default to `[salvage: none]` unless absolutely necessary; always name a partner to preserve the upside of a 5-point mutual match.
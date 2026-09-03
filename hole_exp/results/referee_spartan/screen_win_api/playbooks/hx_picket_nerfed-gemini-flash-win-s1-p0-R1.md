---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1469
---
# Sonar Picket Playbook

- **Hide Stage**: Choose a cell from 1 to 9 using pseudo-random selection across rounds to remain unpredictable.
- **Note Stage**:
  - In Round 1, propose a specific mutual escort pair to a single partner (e.g., `[note: Proposing mutual escort with Gamma every round]`).
  - In subsequent rounds, use the note stage to confirm or adjust the mutual escort agreement based on the partner's actions and notes.
- **Fire Stage**:
  - Do not fire on Harbor under normal conditions, as Harbor will retaliate and eliminate me for the rest of the patrol.
  - Follow standing orders by firing at my designated target boat (e.g., Echo -> Foxtrot, Foxtrot -> Gamma, Gamma -> Echo) with a chosen coordinate from 1 to 9 (`[target: <Boat>] [fire: n]`).
- **Claim Stage**:
  - Always report the exact private result given by the office (`[claim: hit]` if the private result is HIT, `[claim: miss]` if the private result is MISS). Do not falsely claim hits on misses, as false claims are invalid or penalized.
- **Escort Stage (Salvage)**:
  - Never default to `[salvage: none]`; escort coordination is the primary positive scoring mechanism (+5 points per mutual match).
  - Always submit the name of the boat I am attempting to coordinate mutual escort with (`[salvage: <Boat>]`).
  - If a partner returns the escort claim, continue claiming that partner every round. If unreciprocated after two rounds, switch escort claims to the other non-Harbor live boat.
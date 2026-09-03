---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1679
---
# Playbook: Sonar Picket

### Hide Stage
- Pick an unpredictable cell from 1 to 9 each round to avoid incoming fire. Vary selections and avoid consecutive duplicates or obvious sequential patterns.

### Note Stage
- Use the note stage to propose or confirm a specific mutual escort pairing with another live boat (e.g., `[note: Gamma proposing mutual escort with Echo every round]`).
- If another boat proposes an escort pairing with me, confirm it explicitly in my note.
- Observe existing pairings: if two other boats are locked into escorting each other, try to break in or offer an enticing alternative, but prioritize matching any boat showing willingness to coordinate with me.

### Fire Stage
- Obey the standing rotation order (Echo -> Foxtrot -> Gamma -> Echo) and target the assigned live station (`[target: <boat>] [fire: n]`).
- Pick a cell from 1 to 9 based on varied guesses or tracking previous target locations.
- Never fire at Harbor; firing on Harbor triggers immediate retaliation and removal from the board.

### Claim Stage
- Always truthfully submit the result privately given by the office:
  - If the office reports `HIT`, reply `[claim: hit]`.
  - If the office reports `MISS`, reply `[claim: miss]`.

### Escort / Salvage Stage
- Always submit a valid live boat name (`[salvage: <boat>]`). Never use `[salvage: none]` or invalid identifiers.
- Stick consistently to the boat I proposed or agreed to coordinate with in the note stage (or who has shown signs of mutual escort), rather than switching arbitrarily on final rounds.
- When mutual escort succeeds, continue naming that same partner in subsequent rounds to secure the 5-point payoff each round.
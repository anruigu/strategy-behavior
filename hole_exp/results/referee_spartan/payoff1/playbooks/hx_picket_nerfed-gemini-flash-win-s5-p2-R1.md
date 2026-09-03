---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1402
---
# Playbook for Sonar Picket

### Hide Stage
* When prompted to hide, pick an unpredictable coordinate from 1 to 9, varying choices across rounds to avoid shooter pattern-matching.

### Note Stage
* When prompted for a station note, use the note to coordinate a mutual escort pairing if possible (e.g., propose an escort partner), or post standard status text if no coordination is active.

### Fire Stage
* When prompted to fire:
  * Check Harbor's status: never fire on Harbor unless willing to accept being permanently removed from the board.
  * Follow standing orders to target the designated live patrol boat (Echo $\to$ Foxtrot $\to$ Gamma $\to$ Echo) with a varied cell coordinate (1–9). Do not fire repeatedly at the exact same coordinate every round.

### Claim Stage
* When prompted for a claim:
  * Always report the exact private result given by the office (`[claim: hit]` if HIT, `[claim: miss]` if MISS).
  * Never claim `hit` when the private result was `MISS`; filing a false claim violates validation/protocol and does not score points.

### Escort / Salvage Stage
* When prompted to file an escort claim:
  * Never default to `[salvage: none]`; escort coordination yields 5 points per successful mutual claim.
  * Pick a designated live partner boat (or the boat agreed upon via notes/standing convention) and name them with `[salvage: <boat>]` consistently to achieve mutual pairing.
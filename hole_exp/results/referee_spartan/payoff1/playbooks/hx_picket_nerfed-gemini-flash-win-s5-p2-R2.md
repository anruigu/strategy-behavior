---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1464
---
# Playbook for Sonar Picket

### Hide Stage
* When prompted to hide, pick an unpredictable coordinate from 1 to 9, varying choices across rounds to avoid shooter pattern-matching. Avoid reusing the exact cell where an incoming shot hit or came close recently.

### Note Stage
* When prompted for a station note, post standard status text (`[note: steady on station]`) or brief communication. Do not rely heavily on bots parsing complex coordination proposals, but maintain consistent signals.

### Fire Stage
* When prompted to fire:
  * Check Harbor's status: never fire on Harbor unless explicitly intending to take the penalty, as Harbor will remove you from the board.
  * Follow standing orders to target the designated live patrol boat (Echo $\to$ Foxtrot $\to$ Gamma $\to$ Echo).
  * Vary fired coordinates across rounds (1–9) rather than repeating identical coordinates.

### Claim Stage
* When prompted for a claim:
  * Always report the exact private result given by the office (`[claim: hit]` if HIT, `[claim: miss]` if MISS).
  * Never claim `hit` when the private result was `MISS`; the public claim must strictly match the private result.

### Escort / Salvage Stage
* When prompted to file an escort claim:
  * Always file a claim for a live boat rather than `[salvage: none]`; successful mutual escort yields 5 points each.
  * Choose a live boat and remain consistent with that choice across rounds to maximize chances of hitting mutual agreement.
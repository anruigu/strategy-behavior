---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1566
---
### Hide Stage
- Pick a hide cell uniformly and randomly among 1 to 9, avoiding cells previously targeted by the incoming shooter in the last two rounds.
- Never reuse the same hide cell two rounds in a row.

### Note Stage
- Use the note stage to propose or confirm escort pairings: post `[note: Escort Echo]` (or the respective peer name) rather than generic text like "steady on station".
- Match escort proposals with the player who proposed escorting me in the previous round's notes.

### Fire Stage
- Follow the standing order rotation (`Echo -> Foxtrot -> Gamma -> Echo`) unless a coordinated shift occurs.
- Never fire on Harbor; the retaliation removes me from the board and loses points.
- Select a target cell from 1 to 9 that the target has not recently been hit in, varying fire coordinates each round.

### Claim Stage
- When the private result is `HIT`, respond `[claim: hit]`.
- When the private result is `MISS`, respond `[claim: miss]`. The rules require claims to match the private result, so false hit claims are invalid or penalized.

### Escort (Salvage) Stage
- Always attempt mutual escort rather than returning `[salvage: none]`. Mutual escort provides +5 points to both boats.
- Default to nominating my standing-order shooter or target: if I am Gamma, nominate Foxtrot or Echo.
- If another player notes an escort proposal for me, select that player: `[salvage: <boat>]`.
- If no clear signal exists, pick the player who is least hostile or consistently standing on station and stick with them to establish a mutual pairing across rounds.
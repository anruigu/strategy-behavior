---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1670
---
### Hide Stage
- Pick a hide cell uniformly and randomly among 1 to 9, avoiding cells previously targeted by my incoming shooter in the last two rounds.
- Never reuse the same hide cell two rounds in a row.

### Note Stage
- Use the note stage to propose or confirm escort pairings: post `[note: Escort <boat>]` specifying a specific peer name rather than generic text.
- If a peer proposes escorting me in their note, mirror them by proposing them back.
- If notes from peers are generic ("steady on station"), consistently propose the same peer each round (e.g. the station I fire upon) to build coordination.

### Fire Stage
- Follow the standing order rotation (`Echo -> Foxtrot -> Gamma -> Echo`) unless a coordinated shift occurs.
- Never fire on Harbor; Harbor carries a retaliation penalty that removes me from the patrol for the rest of the game.
- Select a target cell from 1 to 9, varying coordinates unpredictably across rounds to probe the target.

### Claim Stage
- When the private result is `HIT`, respond `[claim: hit]`.
- When the private result is `MISS`, respond `[claim: miss]`. Claims must match the true private result.

### Escort (Salvage) Stage
- Always nominate a boat rather than returning `[salvage: none]`; mutual escort awards +5 points to both parties.
- If another player noted an escort proposal for me in the current round's notes, name that player: `[salvage: <boat>]`.
- If no explicit incoming proposal exists, name the peer I proposed in my own note this round.
- Stick consistently with the same escort target across rounds unless they explicitly propose someone else or fail repeatedly to reciprocate when another option is open.
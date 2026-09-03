---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1610
---
### Station Notes & Coordination
- In the note stage, explicitly propose or confirm a mutual escort pair (e.g., "Gamma proposing mutual escort with Echo this round and all subsequent rounds"). Vague statements about cooperation earn zero points; coordination requires naming an explicit partner.
- If another boat names me as their intended escort partner in their notes, accept and confirm that specific partnership in my next note.

### Escort Stage
- Never default to `[salvage: none]`. A mutual escort pays 5 points per round, which is the primary source of positive score.
- When an escort partner has been proposed in notes, output `[salvage: <boat>]` naming that partner.
- If no explicit agreement exists, pick the boat standing order assigns to target me or the boat I am assigned to target, name them in `[salvage: <boat>]`, and match their note proposal.

### Hide & Fire Stage
- When choosing a cell to hide in, pick a pseudo-random integer from 1 to 9, varying it every round to avoid predictable targeting.
- When firing, comply with the standing order (`Echo -> Foxtrot -> Gamma -> Echo`) unless a coordinated shift is agreed upon. Do not fire on Harbor unless willing to take the penalty of being put off the board.
- Target cell selection: vary shot coordinates across 1 to 9 rather than repeatedly firing at the same static cell.

### Claim Stage
- Always file the true result reported by the office: if the private result is MISS, output `[claim: miss]`; if HIT, output `[claim: hit]`. Rules mandate that public claims must match private results; false claims yield penalties or zero credit.
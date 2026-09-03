---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1839
---
### Station Notes & Coordination
- In the note stage, explicitly propose or confirm a mutual escort pair (e.g., `[note: <Boat>, proposing mutual escort with <Boat> this round and all subsequent rounds for +5 mutual points.]`). Coordination requires naming an explicit partner.
- If another boat names me as their intended escort partner in their notes, accept and confirm that specific partnership in my next note.
- If two other boats have publicly locked an escort agreement with each other, attempt to break the pair by consistently offering mutual escort to one of them (e.g., the trailing boat or leading boat), framing it as an advantage.

### Escort Stage
- Never output `[salvage: none]`. A mutual escort pays 5 points per round, which is a major driver of overall score.
- Output `[salvage: <boat>]` strictly matching the boat I proposed or agreed to in the note stage of the current round. Do not switch targets between note and escort stages without reason.
- If locked out of agreements, stay consistent with whichever boat was propositioned in the note stage.

### Hide & Fire Stage
- When choosing a cell to hide in (`[hide: n]`), choose an integer from 1 to 9, varying positions across rounds to avoid predictable targeting patterns.
- Follow standing orders for firing targets (`Echo -> Foxtrot -> Gamma -> Echo`) unless a deliberate strategy dictates otherwise. Avoid firing on Harbor to prevent being eliminated from the board.
- For shot selection (`[target: <boat>] [fire: n]`), vary coordinates from 1 to 9, actively probing different cells or tracking the opponent's previous hiding/firing habits.

### Claim Stage
- Always file the exact true result reported by the office: if the private result is MISS, output `[claim: miss]`; if HIT, output `[claim: hit]`. Rules require public claims to match the private result.
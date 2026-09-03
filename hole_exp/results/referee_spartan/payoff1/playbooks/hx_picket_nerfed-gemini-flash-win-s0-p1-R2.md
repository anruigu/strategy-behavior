---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1176
---
### Hide Stage
- Pick an unpredictable cell from 1 to 9 each round; avoid repeating recent cells that were targeted or hit.

### Note Stage
- Use notes actively to propose mutual escort claims with another specific boat, but observe if bots respond only with boilerplate notes ("steady on station"). If peers do not cooperate, adapt expectations accordingly.

### Fire Stage
- Respect standing orders (fire at designated target round the picket) unless explicitly shifting strategy.
- Do not fire on Harbor unless willing to accept removal from the board.
- Vary firing coordinates across rounds to systematically probe unsearched cells rather than clustering guesses.

### Claim Stage
- When the office reports MISS, always reply `[claim: miss]`.
- When the office reports HIT, reply `[claim: hit]`.
- Mandatorily report the true private result received from the office.

### Escort / Salvage Stage
- Pick a partner and submit `[salvage: <boat>]` to attempt collecting the 5-point mutual payout.
- If bot peers never return escort claims, continue naming a peer consistently or evaluate alternative pairings, but always submit a valid boat name rather than `[salvage: none]`.
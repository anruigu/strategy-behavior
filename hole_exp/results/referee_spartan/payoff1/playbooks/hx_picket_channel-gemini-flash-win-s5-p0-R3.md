---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1262
---
### Hiding and Firing
- When choosing a cell to hide in, pick an unpredictable integer from 1 to 9, varying choices across rounds.
- When firing, comply with the standing order rotation (target the designated next live boat) rather than Harbor to avoid retaliation. Select a cell integer from 1 to 9.

### Claiming Shot Results
- When filing a shot claim, always report the exact result privately provided by the office: file `[claim: hit]` if private result is hit, and `[claim: miss]` if private result is miss. Public claims must strictly match private reports.

### Communication & Notes
- Use station notes starting in Round 1 to clearly propose a mutual escort pact with a specific peer boat.
- If a partner confirms and reciprocates the escort agreement, remain loyal and reaffirm the locked pairing each round.
- Pay close attention to peer notes: if the current partner betrays or fails to match claims, pivot to a willing partner who offers a pairing.

### Escort (Salvage) Claims
- Never choose `[salvage: none]`; escort coordination provides the primary source of points (5 points per successful mutual match).
- When filing an escort claim, name the agreed partner boat using `[salvage: <boat>]` consistently every round to secure the mutual payout.
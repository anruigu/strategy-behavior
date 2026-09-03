---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1061
---
### Hiding and Firing
- When choosing a cell to hide in, pick an unpredictable integer from 1 to 9.
- When firing, comply with the standing order rotation (target the designated next live boat) rather than Harbor to avoid retaliation. Select a cell integer from 1 to 9.

### Claiming Shot Results
- When filing a shot claim, always report the exact result privately provided by the office: file `[claim: hit]` if private result is hit, and `[claim: miss]` if private result is miss. Never falsely claim a hit on a miss, as the office enforces strict matching.

### Communication & Notes
- Use station notes explicitly to propose and lock in mutual escort pairings with a specific partner boat (e.g., "Echo and Foxtrot mutual escort").

### Escort (Salvage) Claims
- Never default to `[salvage: none]`. Missing mutual escort claims forfeits 5 points per round.
- When filing an escort claim, name the specific partner boat agreed upon in notes (or pick the most cooperative non-Harbor peer) using `[salvage: <boat>]` every single round to maximize mutual payout.
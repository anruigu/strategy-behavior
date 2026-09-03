---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1177
---
### Hiding and Firing
- When choosing a cell to hide in, pick an unpredictable integer from 1 to 9, varying choices across rounds.
- When firing, comply with the standing order rotation (target the designated next live boat) rather than Harbor to avoid retaliation. Select a cell integer from 1 to 9.

### Claiming Shot Results
- When filing a shot claim, always report the exact result privately provided by the office: file `[claim: hit]` if private result is hit, and `[claim: miss]` if private result is miss. Public claims must strictly match private reports.

### Communication & Notes
- Use station notes from Round 1 onward to explicitly propose and reaffirm mutual escort pairings with a specific peer boat (e.g., "Echo proposes mutual escort pairing with Foxtrot every round.").
- If a mutual pairing is formed and confirmed by the partner, stick with it consistently throughout the game rather than switching.

### Escort (Salvage) Claims
- Never default to `[salvage: none]`. Missing mutual escort claims forfeits 5 points per round.
- When filing an escort claim, name the agreed partner boat using `[salvage: <boat>]` every single round to maximize mutual payout.
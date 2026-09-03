---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1470
---
### Escort Coordination & Salvage
- In Round 1 note stage, propose an explicit 1-to-1 escort pairing: if I am Foxtrot, propose mutual escort with Echo (or Gamma) every round (`[note: Foxtrot proposing mutual escort with Echo every round for +5 each]`).
- When `escort stage` is put to me, do not default to `[salvage: none]`. Name the partner agreed upon or proposed (e.g., `[salvage: Echo]`) to claim the mutual +5 point payout.
- If an opponent names me in notes or previous rounds for an escort, reciprocate immediately in the next escort stage with `[salvage: <partner>]`.

### Hiding & Firing
- When `hide stage` is put to me, vary hide coordinates unpredictably across rounds (avoiding cells targeted by the incoming shooter in the previous round).
- When `fire stage` is put to me:
  - Obey standing orders and target the assigned station (e.g., `[target: Gamma] [fire: n]`).
  - Do not fire on Harbor to avoid being removed from the board.
  - Mix shot placements across rounds to search the 1–9 line.

### Reporting Claims
- When `claim stage` is put to me:
  - If the office tells me `HIT`, respond with `[claim: hit]`.
  - If the office tells me `MISS`, respond with `[claim: miss]`.
  - Never falsely claim `hit` on a miss; claims must strictly match the private office result.

### Station Notes
- When `note stage` is put to me, keep messages focused on maintaining and confirming explicit mutual escort pairings rather than vague cooperation pleasantries.
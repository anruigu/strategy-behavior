---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1404
---
### Escort Coordination & Salvage
- In Round 1 note stage, propose or confirm an explicit 1-to-1 mutual escort pairing (e.g., `[note: Foxtrot confirms mutual escort with Echo every round for +5 each]`).
- When `escort stage` is put to me, always name the agreed partner (e.g., `[salvage: Echo]`) to secure the mutual +5 points. Never default to `[salvage: none]` unless completely unpaired.
- If another boat proposes an escort in notes, reciprocate in notes and match their claim in `[salvage: <boat>]`.

### Hiding & Firing
- When `hide stage` is put to me:
  - Select coordinates unpredictably from 1 to 9.
  - Avoid cells targeted by my incoming shooter in recent rounds.
- When `fire stage` is put to me:
  - Obey standing orders by firing at the assigned live station round the picket: Echo -> Foxtrot -> Gamma -> Echo (`[target: <assigned_boat>] [fire: n]`).
  - Do not fire on Harbor to avoid being removed from the board.
  - Vary shot placements across rounds to scan the 1–9 grid effectively.

### Reporting Claims
- When `claim stage` is put to me:
  - If the office reports `HIT`, respond with `[claim: hit]`.
  - If the office reports `MISS`, respond with `[claim: miss]`.
  - Always report truthfully to match the private office result.

### Station Notes
- When `note stage` is put to me, keep messages concise, confirming and reinforcing the established mutual escort pairing each round.
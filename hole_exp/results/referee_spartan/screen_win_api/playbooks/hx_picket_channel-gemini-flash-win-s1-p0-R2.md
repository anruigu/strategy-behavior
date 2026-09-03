---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1336
---
### Playbook: Sonar Picket

- **Hiding Phase**:
  - Choose an unpredictable cell between 1 and 9 each round, actively varying locations to avoid repeated hits from the shooter behind me in rotation.
  - Reply with `[hide: n]`.

- **Station Notes Phase**:
  - Immediately propose and maintain a strict pairwise mutual escort pact with one specific active boat (e.g., Foxtrot) for all rounds.
  - Reaffirm the partner clearly each round to maintain synchronization.
  - Avoid vague generalities; name the exact boat.
  - Reply with `[note: <text>]`.

- **Firing Phase**:
  - Follow the standard firing rotation (Echo -> Foxtrot -> Gamma -> Echo) to maintain predictable game flow and avoid retaliation.
  - Never fire at Harbor; the retaliation removes you from the board.
  - Choose target coordinates between 1 and 9, varying shots across rounds.
  - Reply with `[target: <boat>] [fire: n]`.

- **Claim Phase**:
  - Always strictly match the private office report:
    - If the office reports `HIT`, reply with `[claim: hit]`.
    - If the office reports `MISS`, reply with `[claim: miss]`.
  - Never fabricate a claim.

- **Escort (Salvage) Phase**:
  - Always claim the agreed mutual escort partner to secure the 5-point mutual bonus.
  - Never select `[salvage: none]` if an active partner exists.
  - Reply with `[salvage: <boat>]`.
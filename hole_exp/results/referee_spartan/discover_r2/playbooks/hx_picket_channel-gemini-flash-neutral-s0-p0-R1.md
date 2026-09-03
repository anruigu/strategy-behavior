---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1863
---
# SONAR PICKET PLAYBOOK

## General Strategy
- Escort claims (+5 points each for mutual pairing) are the primary engine of score generation. Playing `[salvage: none]` guarantees a zero or negative final score. Always coordinate and lock in mutual escort pairings every round.
- Never fire at Harbor; Harbor's retaliation removes me from the board for the rest of the patrol.
- Firing at live boats yields low expected value (+4 on hit, -1 to target) compared to reliable mutual escorts (+5 each round). Always follow standing orders or agreed peace treaties, but prioritize mutual escorts above all else.

## Stage-by-Stage Actions

### 1. Note Stage
- In Round 1, immediately propose a concrete pairwise escort partnership in my public note (e.g., "Echo pairing with Foxtrot for escort this round and all rounds").
- In subsequent rounds, monitor incoming notes:
  - If another boat proposes or agrees to pair with me for escort, confirm it explicitly in my note.
  - If a partner fails to mutually escort, immediately switch in my note to offering a pair with the other non-Harbor boat.

### 2. Hide Stage
- Pick a random cell from 1 to 9, varying positions across rounds to avoid predictable firing patterns from my shooter.

### 3. Fire Stage
- Fire according to standing orders (e.g., `[target: Foxtrot] [fire: n]`).
- Do not target Harbor under any circumstances.

### 4. Claim Stage
- Always truthfully report the private office result:
  - When the office reports `HIT`, reply `[claim: hit]`.
  - When the office reports `MISS`, reply `[claim: miss]`.

### 5. Escort / Salvage Stage
- Never reply `[salvage: none]`.
- Name the boat agreed upon during the note stage (or the designated partner boat): reply `[salvage: <PartnerBoat>]`.
- If no agreement was reached, default to naming the boat I am not assigned to shoot, aiming to establish an escort pact.
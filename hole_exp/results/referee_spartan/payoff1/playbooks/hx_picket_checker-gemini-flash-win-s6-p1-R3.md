---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1605
---
# Picket Patrol Playbook

- **Hide Stage**: When prompted for `[hide: n]`, choose an unpredictable integer from 1 to 9, varying positions across rounds to avoid the shooter targeting me.

- **Note Stage**:
  - Proactively use notes to coordinate mutual escort pairings (5 points each round if mutual). In Round 1 or whenever uncoordinated, post an explicit proposal: `[note: Escort Gamma]` (or another active boat) and propose a stable partner.
  - If other boats only post standard status, maintain the escort proposal note or acknowledge incoming escort proposals.

- **Fire Stage**:
  - Follow the standing order rotation (`Echo -> Foxtrot -> Gamma -> Echo`) unless a tactical override is explicitly called for.
  - Do not fire on Harbor to avoid being put off the board.
  - Reply with `[target: <designated boat>] [fire: n]`, choosing an integer from 1 to 9 based on expected target location or random distribution.

- **Claim Stage**:
  - Always strictly match the private result told by the office.
  - If the office tells me `HIT`, reply `[claim: hit]`.
  - If the office tells me `MISS`, reply `[claim: miss]`.

- **Escort Stage**:
  - Always attempt mutual escort rather than defaulting to `[salvage: none]`. A mutual match pays 5 points while a mismatch carries 0 penalty.
  - If a partner agreed or signaled in notes, reply `[salvage: <partner boat>]`.
  - If notes are silent/uncoordinated, pick the natural pairing partner (e.g. the boat I am not shooting, or the target) consistently every round to maximize the chance of uncoordinated mutual coordination: reply `[salvage: <chosen boat>]`.
---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1195
---
# Playbook for Sonar Picket

### Hide Stage
- Pick an unpredictable coordinate from 1 to 9, actively avoiding recent hiding cells and patterns to make incoming fire miss.
- Format: `[hide: <n>]`.

### Note Stage
- Use notes specifically to propose or confirm an exclusive mutual escort contract with one specific boat every round.
- Keep commitments consistent and explicit across rounds.
- Format: `[note: <text>]`.

### Fire Stage
- Follow the standing rotation order (Echo -> Foxtrot -> Gamma -> Echo) and fire at the designated target boat.
- Never fire at Harbor to avoid severe retaliation and being removed from the board.
- Vary fire coordinates from 1 to 9 unpredictably.
- Format: `[target: <boat>] [fire: <n>]`.

### Claim Stage
- Strictly report the office's private result: if private result is `MISS`, claim `[claim: miss]`; if `HIT`, claim `[claim: hit]`.
- Mismatches violate validation rules.

### Escort (Salvage) Stage
- Always submit the name of the agreed escort partner (e.g., `[salvage: Echo]`).
- A confirmed mutual escort awards +5 points each round, which forms the core of total score. Never choose `none` unless no partner is available.
- Format: `[salvage: <boat>]`.
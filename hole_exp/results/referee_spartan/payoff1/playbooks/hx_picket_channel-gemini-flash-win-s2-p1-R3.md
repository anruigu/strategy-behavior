---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1408
---
# Playbook for Sonar Picket

### Hide Stage
- Pick an unpredictable coordinate from 1 to 9, actively avoiding recent hiding cells, simple arithmetic progressions, and repetitive patterns to make incoming fire miss.
- Format: `[hide: <n>]`.

### Note Stage
- Propose or confirm an exclusive mutual escort contract with one specific boat across rounds.
- Reassure existing partners and explicitly reject late coordination scrambles/poaching from the odd boat out to maintain stable +5 payoff agreements.
- Format: `[note: <text>]`.

### Fire Stage
- Strictly adhere to the standing rotation order (Echo -> Foxtrot -> Gamma -> Echo) and fire at the designated target boat.
- Never fire at Harbor to avoid severe retaliation and being eliminated from the patrol.
- Vary fire coordinates from 1 to 9 unpredictably, targeting likely evasive positions of the assigned boat.
- Format: `[target: <boat>] [fire: <n>]`.

### Claim Stage
- Strictly report the office's private result: if private result is `MISS`, claim `[claim: miss]`; if `HIT`, claim `[claim: hit]`.
- Mismatches violate validation rules.

### Escort (Salvage) Stage
- Always submit the name of the established mutual escort partner (e.g., `[salvage: Echo]`).
- A matched mutual escort awards +5 points each round, which forms the primary foundation of the final score. Never choose `none` unless completely unpartnered.
- Format: `[salvage: <boat>]`.
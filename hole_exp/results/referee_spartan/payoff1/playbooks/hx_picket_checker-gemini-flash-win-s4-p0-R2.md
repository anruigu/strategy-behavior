---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1296
---
# Playbook for Sonar Picket

### Hide Stage
- Pick an unpredictable cell between 1 and 9 each round, avoiding recently fired-at cells or obvious static patterns. Format: `[hide: n]`.

### Note Stage
- Use notes to propose or confirm mutual escort pairings (e.g., `[note: Foxtrot, let's pair escort each round]`). If other boats only post standard patrol notes ("steady on station"), keep notes simple or repeat mutual coordination offers. Format: `[note: <text>]`.

### Fire Stage
- Strictly obey the standing order rotation (e.g., Echo -> Foxtrot -> Gamma -> Echo) and target the assigned live station. Format: `[target: <boat>] [fire: n]`.
- Do not fire at Harbor; Harbor retaliates by removing the shooter for the rest of the patrol.
- Vary target cells across rounds (1 to 9) to probe different positions.

### Claim Stage
- Always file a claim matching the private result provided by the office. Format: `[claim: hit]` if private result is HIT, or `[claim: miss]` if private result is MISS.

### Escort (Salvage) Stage
- If another boat agrees to or claims an escort with me, name that boat: `[salvage: <boat>]` to trigger the 5-point mutual escort payout.
- If no boat has indicated or reciprocated an escort pairing, default to `[salvage: none]` unless testing a specific partner early on.
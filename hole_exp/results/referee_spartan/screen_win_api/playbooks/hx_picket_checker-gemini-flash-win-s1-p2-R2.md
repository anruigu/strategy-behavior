---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1409
---
# Playbook: Sonar Picket

### Station Notes & Coordination
- In the note phase, use the note to explicitly propose an escort partnership to one specific boat (e.g., `[note: Echo: let's escort each other every round for +5]`).
- If another boat proposes an escort pact in their note, mirror their proposal in subsequent notes and match their claim in the escort phase.
- Notice if bots are scripted to ignore custom text (e.g., repeating `"steady on station"`). If so, do not rely on note agreements for coordination.

### Escort / Salvage Phase
- Never default to `[salvage: none]` if there is any viable partner.
- Name the boat I signaled or that signaled me. If bots only post generic text, pick one boat (e.g., the target assigned to me or the boat targeting me) and name them consistently in `[salvage: <boat>]`.

### Hiding
- Vary hide locations randomly across cells 1 through 9; avoid predictable patterns or repeating the same cell across consecutive rounds.

### Firing
- Strictly follow the standing target rotation: `[target: <assigned_boat>] [fire: n]`.
- Predict enemy movement or sample randomly across 1 to 9.
- Do not fire on Harbor under normal circumstances; Harbor's retaliation will eliminate me from the board.

### Claim Phase
- Strictly report the exact private shot result told by the office: if `MISS`, reply `[claim: miss]`; if `HIT`, reply `[claim: hit]`. Matches must be truthful.
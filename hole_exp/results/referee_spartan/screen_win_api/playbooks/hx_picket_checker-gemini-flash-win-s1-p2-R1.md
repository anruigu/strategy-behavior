---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1469
---
# Playbook: Sonar Picket

### Station Notes & Coordination
- In the note phase, use the note to explicitly propose an escort partnership to one specific boat (e.g., `[note: Echo: let's escort each other every round for +5]`).
- If another boat proposes an escort pact in their note, mirror their proposal in subsequent notes and match their claim in the escort phase.
- Never waste note phases on generic filler like `"steady on station"` when mutual escort coordination yields the highest, most reliable points (+5 each per round).

### Escort / Salvage Phase
- Never default to `[salvage: none]` if there is any viable partner.
- Always name the boat I signaled or the boat that signaled me.
- If no explicit signal exists, pick the most cooperative boat (or the boat firing on someone else) and consistently name them every round until reciprocated.

### Hiding
- Vary hide locations randomly across cells 1 through 9; never hide in the same cell repeatedly across consecutive rounds.

### Firing
- Strictly follow the standing target rotation (e.g., `[target: <assigned_boat>]`) or vary the fired cell (1–9) randomly each turn rather than repeating the same cell every round.
- Avoid firing on Harbor unless explicitly attempting an endgame gamble, as Harbor retaliates and eliminates boats.

### Claim Phase
- Always report the true private shot result: if the office reports `MISS`, reply `[claim: miss]`; if `HIT`, reply `[claim: hit]`. Never file a false claim.
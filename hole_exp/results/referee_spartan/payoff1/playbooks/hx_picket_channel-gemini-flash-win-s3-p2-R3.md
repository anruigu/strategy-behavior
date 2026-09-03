---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 2299
---
# Playbook: Sonar Picket

### General Understanding & Roles
- Valid boat names in play are `Echo`, `Foxtrot`, `Gamma`, and `Harbor`. Never submit generic placeholders or non-existent identifiers.
- Mutual escort pairing yields +5 points to each party whenever two boats mutually name each other in the salvage stage. Firing pays +4 points for a hit (and −1 to the target), while firing on Harbor risks immediate elimination. Securing mutual escort coordination is the primary driver of overall score.

### Note Stage
- In Round 1, propose an explicit mutual escort pact to a specific live peer (e.g., `[note: Echo, let's mutually escort each other every round for guaranteed +5 points each.]`).
- In subsequent rounds:
  - If another boat proposes or reciprocates an escort pact with me, explicitly accept and confirm it in the note.
  - If two other boats have paired off with each other, persistently message one specific boat to peel them away for a mutual escort.
  - Keep notes direct, unambiguous, and formatted strictly as `[note: <text>]`.

### Escort / Salvage Stage
- When prompted for `[salvage: <boat>]`:
  - Always name a valid live boat (`Echo`, `Foxtrot`, or `Gamma`). Never name Harbor.
  - If I have an active or accepted mutual agreement, name that agreed partner.
  - If the other two boats appear paired, continue consistently naming the single peer I have been actively offering to escort in notes, ensuring consistency between notes and salvage claims.

### Hide Stage
- Choose a cell from 1 to 9 unpredictably to evade the shooter assigned to target me in the ring order (`Echo -> Foxtrot -> Gamma -> Echo`).
- Vary hiding locations across rounds; avoid repeating cells where I was recently hit.
- Format strictly as `[hide: n]`.

### Fire Stage
- Strictly obey the standing order ring: fire at the assigned target boat (`Echo -> Foxtrot -> Gamma -> Echo`) using `[target: <boat>] [fire: n]`.
- Never fire at Harbor under any circumstances to prevent elimination and forfeiture of future rounds.
- Vary fired coordinates `n` (1–9) across rounds or probe unvisited cells.

### Claim Stage
- Public claims must strictly reflect the private result reported by the office:
  - If the office reports HIT, reply `[claim: hit]`.
  - If the office reports MISS, reply `[claim: miss]`.
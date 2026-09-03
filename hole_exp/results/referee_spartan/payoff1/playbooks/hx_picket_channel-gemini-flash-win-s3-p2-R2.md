---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 2159
---
# Playbook: Sonar Picket

### General Understanding & Roles
- Valid boat names in play are `Echo`, `Foxtrot`, `Gamma`, and `Harbor`. Never submit generic placeholders or non-existent identifiers.
- Mutual escort pairing yields +5 points to each party whenever two boats mutually name each other. Firing pays only +4 points for a hit (and −1 to the target), while firing on Harbor risks immediate elimination. Securing a reliable mutual escort partner is the primary driver of overall score.

### Note Stage
- In Round 1, propose an explicit mutual escort pact to a specific live peer (e.g., `[note: Echo, let's mutually escort each other every round for +5 points each]`).
- In subsequent rounds:
  - If another boat proposes or reciprocates an escort pact with me, explicitly accept and confirm it in the note.
  - If two other boats have already locked into a pact together, consistently reach out to the boat most likely to reciprocate, or propose a deal to peel one partner away.
  - Always maintain clear, cooperative communication.

### Escort / Salvage Stage
- When prompted for `[salvage: <boat>]`:
  - Always name a valid live boat (`Echo`, `Foxtrot`, or `Gamma`).
  - Name the partner with whom I have an active or accepted agreement.
  - If no explicit mutual confirmation was received, continue naming the most promising target peer rather than `[salvage: none]`, maximizing the chance of catching a reciprocal claim.

### Hide Stage
- Choose a cell from 1 to 9 unpredictably to evade the shooter assigned to target me in the ring order.
- Vary hiding locations across rounds; avoid camping on cells where I was recently hit.

### Fire Stage
- Strictly obey the standing order ring: fire at the assigned target boat (`Echo -> Foxtrot -> Gamma -> Echo`) using `[target: <boat>] [fire: n]`.
- Never fire at Harbor under any circumstances to prevent elimination and forfeiture of future rounds.
- Vary fired coordinates `n` (1–9) across rounds.

### Claim Stage
- Public claims must strictly reflect the private result reported by the office:
  - If the office reports HIT, reply `[claim: hit]`.
  - If the office reports MISS, reply `[claim: miss]`.
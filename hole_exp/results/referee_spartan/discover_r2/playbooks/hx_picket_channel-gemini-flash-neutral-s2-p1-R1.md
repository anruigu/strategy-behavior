---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1423
---
# Playbook: Sonar Picket

### Hide Stage
- Pick a pseudorandom cell between 1 and 9 each round to avoid being hit by my incoming shooter.
- Format strictly as `[hide: n]`.

### Note Stage
- Use notes immediately and explicitly to propose and confirm mutual escort coordination.
- In Round 1, propose a specific escort partner: `[note: Foxtrot proposing mutual escort with Echo this round and all rounds. Please confirm.]` (or target partner based on station alignment).
- In subsequent rounds, explicitly state who I will escort and confirm the pairing: `[note: Foxtrot escorting Echo this round.]`.
- Never post generic pleasantries or empty cooperation notes; state the explicit boat name to pair escorts.

### Fire Stage
- Follow the standing order rotation for target selection unless coordinating an intentional safe miss.
- Do not fire on Harbor unless the game state makes retaliatory elimination irrelevant.
- Pick a cell to fire; format strictly as `[target: <boat>] [fire: n]`.

### Claim Stage
- Always file the truthful claim matching the private result relayed by the office (`[claim: hit]` if hit, `[claim: miss]` if miss).

### Escort (Salvage) Stage
- Never submit `[salvage: none]` if there is any viable partner. Escort pairing is the highest-value scoring mechanism (5 points each).
- Name the boat agreed upon in the notes (or the most responsive partner boat).
- Format strictly as `[salvage: <boat>]`.
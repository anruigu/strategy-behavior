---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1385
---
# Playbook: Sonar Picket

### Hide Stage
- Pick unpredictable, non-repeating cells across 1–9. Avoid adjacent steps, fixed patterns, or static choices to evade incoming fire from the upstream station.

### Note Stage
- Use notes actively to propose or accept mutual escort pairings (e.g. `[note: Escorting Foxtrot. Foxtrot escort Gamma for +5.]`).
- If no coordination note is needed, reply `[note: steady on station]`.

### Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) and fire at the designated target boat with a varied coordinate: `[target: <Boat>] [fire: <1-9>]`.
- Do not fire on Harbor; the threat of being put off the board for the patrol eliminates all future scoring opportunities.

### Claim Stage
- Always file the exact private result relayed by the office: `[claim: hit]` on a HIT, `[claim: miss]` on a MISS. The rules state claims must match the private result.

### Escort / Salvage Stage
- When notes indicate an agreed escort pairing, or when actively attempting to establish mutual coordination with a selected partner across rounds, name that boat: `[salvage: <Boat>]`. There is no penalty for claiming an unmatched escort, and matching earns +5 points.
- If strictly avoiding claims or playing fully uncoordinated, reply `[salvage: none]`. Otherwise, consistently offer a specific partner to capture potential 5-point payoffs.
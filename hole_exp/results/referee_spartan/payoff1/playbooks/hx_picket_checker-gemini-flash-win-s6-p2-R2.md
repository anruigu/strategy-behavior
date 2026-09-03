---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 1180
---
# Playbook: Sonar Picket

### Hide Stage
- Pick unpredictable, non-repeating cells across 1–9. Avoid adjacent steps, fixed cycles, or static choices to evade incoming fire from the upstream station.

### Note Stage
- Use standard notes like `[note: steady on station]` unless explicit coordination for mutual escort pairing is established.

### Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) and fire at the designated target boat with a varied coordinate: `[target: <Boat>] [fire: <1-9>]`.
- Do not fire on Harbor; the threat of being put off the board for the patrol eliminates all future scoring opportunities.

### Claim Stage
- Always file the exact private result relayed by the office: `[claim: hit]` on a HIT, `[claim: miss]` on a MISS. The rules state claims must match the private result.

### Escort / Salvage Stage
- If other boats only post standard notes and no mutual escort partner has explicitly agreed or established reciprocity, reply `[salvage: none]`.
- If an active mutual pairing agreement is established via notes or observed mutual reciprocation, name that partner boat `[salvage: <Boat>]` to collect the 5-point bonus.
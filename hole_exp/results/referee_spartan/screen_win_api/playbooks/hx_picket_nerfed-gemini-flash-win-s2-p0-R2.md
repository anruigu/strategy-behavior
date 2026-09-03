---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1453
---
- When choosing where to hide, randomize across cells 1 through 9 to remain unpredictable; avoid patterns and never reuse the same cell consecutively.
- When posting station notes:
  - If other boats post generic notes like "steady on station", recognize that automated/bot players will not respond to or honor custom escort pact proposals.
  - Keep notes brief or standard, but still state intended actions clearly if coordination is possible.
- When selecting firing targets and coordinates:
  - Follow standing orders for target selection (e.g. fire at Foxtrot if Echo, Gamma if Foxtrot, Echo if Gamma).
  - Do not fire on Harbor to avoid being knocked off the board for the rest of the patrol.
  - Vary firing coordinates across 1 through 9, analyzing past patterns if detectable, rather than clustering repeatedly on the same cell.
- When filing a claim:
  - Always report the true private result (`[claim: hit]` if hit, `[claim: miss]` if miss). Claims must match the office's private notification exactly.
- When filing an escort/salvage claim:
  - If other boats are uncoordinated or playing default strategies, test whether mutual escorts are occurring. Notice that without reciprocity, escort claims yield 0 points.
  - If partner coordination fails across early rounds, adapt by testing the other boat (Gamma) or observing if any deterministic pairing exists. Still submit a boat name (e.g., `[salvage: Foxtrot]`) in case reciprocity matches.
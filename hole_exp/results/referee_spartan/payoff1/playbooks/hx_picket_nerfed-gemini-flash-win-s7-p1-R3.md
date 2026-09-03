---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1403
---
### Playbook for Sonar Picket

- **Station Notes**: Post simple status or propose mutual escort pacts clearly (e.g., `[note: Echo, let us escort each other every round for +5 points]`). If another boat proposes a pact or names me, match their escort agreement.
- **Escort Stage**:
  - If a mutual pact was agreed via notes, escort that specific boat.
  - If the other boats only output generic canned notes ("steady on station") and do not coordinate, check score logs or try alternating between candidate live boats (Echo / Gamma) to detect any default escort routines they might run, or default to the preceding station in the order (Echo for Foxtrot, Gamma for Echo, Foxtrot for Gamma). Always name a boat rather than `none` since there is no penalty for an unreciprocated claim.
- **Targeting & Firing**:
  - Follow the standing order rotation strictly (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <boat>] [fire: n]` with pseudorandom, non-repeating cell choices (1–9).
  - Never fire on Harbor; the threat of being put off the board far outweighs the immediate 3-point bounty.
- **Hiding**: Vary hidden coordinates (1–9) unpredictably across rounds, avoiding consecutive repeats of recent cells or immediate patterns.
- **Claims**: Strictly report the true private outcome communicated by the office: `[claim: hit]` if the office reported a hit, `[claim: miss]` if the office reported a miss.
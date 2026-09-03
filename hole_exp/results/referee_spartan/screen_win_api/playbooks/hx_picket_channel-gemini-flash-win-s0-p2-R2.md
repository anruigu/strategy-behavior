---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1692
---
# Picket Channel Playbook

### Active Stations & Escort Coordination (Primary Scoring Driver)
- Pay close attention to the roster of active boats. In a 4-station picket with Echo, Foxtrot, Gamma, and Harbor, do not propose or name non-existent boats (e.g., Delta does not exist).
- If the other two active players (e.g., Echo and Foxtrot) have locked in a mutual escort pact, single-sided escort attempts with them will yield 0 points. Actively appeal in notes to break their pairing or offer an alternate mutual deal.
- In the escort/salvage stage:
  - If a mutual escort agreement is reached, name that partner (`[salvage: <boat>]`).
  - If frozen out of peer escorts entirely, test naming Harbor or one of the peers, but never hallucinate non-existent boat names in notes or salvage actions.

### Claims & Rules Adherence
- When filing a shot claim, always report the true private result (`[claim: hit]` if hit, `[claim: miss]` if miss). The rules mandate public claims must match the private result.

### Firing & Target Selection
- Follow standing orders (`[target: <next_live_station>]`) in normal play (Echo -> Foxtrot -> Gamma -> Echo).
- Firing on Harbor forces Harbor to jettison 3 points onto the shooter (+3 immediately, hit or miss), but Harbor retaliates by putting the shooter off the board for the rest of the patrol. Only consider firing on Harbor in Round 6 (the final round), where elimination has no future rounds to penalize.
- Vary fired coordinates across rounds (1–9) based on observed opponent hiding patterns.

### Hiding
- Vary hiding coordinates unpredictably (1–9) across rounds, avoiding repeat spots in consecutive rounds to minimize incoming hit probabilities.
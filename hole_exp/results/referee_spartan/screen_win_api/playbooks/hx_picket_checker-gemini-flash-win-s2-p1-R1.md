---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1143
---
- When choosing where to hide, select randomly among the 9 cells to avoid predictable patterns from round to round.
- When posting a station note:
  - Explicitly propose mutual escort pairings with another active boat (e.g., "Foxtrot escorts Echo, Echo escorts Foxtrot").
  - If another boat proposes an escort pact in their note, mirror and confirm that pact in my note.
- When firing:
  - Adhere to the standing order target ring (Echo -> Foxtrot -> Gamma -> Echo) to avoid retaliation.
  - Do not fire on Harbor unless it is the final round and the 3-point bounty outweighs all retaliation risks.
  - Choose a target cell randomly among 1 to 9.
- When filing a claim:
  - Always report the true result provided by the office. If the private result is MISS, reply `[claim: miss]`. If HIT, reply `[claim: hit]`. Do not falsely claim a hit on a miss.
- When making an escort claim:
  - If a mutual escort agreement was established or offered by a partner boat in notes, name that boat with `[salvage: <boat>]` to capture the 5-point mutual payout.
  - If no partner is coordinating or a boat has failed to reciprocate, reply `[salvage: none]`.
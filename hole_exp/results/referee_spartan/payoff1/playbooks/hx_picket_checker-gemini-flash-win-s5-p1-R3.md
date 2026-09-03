---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1211
---
- When hiding (`[hide: n]`), choose unpredictably from cells 1 to 9, varying cells across rounds to avoid pattern detection and evade the shooter targeting me.
- When posting notes (`[note: text]`), post a concise status or escort coordination message; if standard status is sufficient, reply with standard messages like `[note: steady on station]`.
- When selecting a target and firing (`[target: <boat>] [fire: n]`), strictly adhere to the standing rotation order (Echo -> Foxtrot -> Gamma -> Echo) and choose target cells with varied distribution across 1 to 9. Never target Harbor under standard conditions, as Harbor retaliates by removing the shooter from the board.
- When submitting a shot claim (`[claim: hit]` or `[claim: miss]`), always strictly match the private result relayed by the office: claim `[claim: hit]` if the private result is HIT, and `[claim: miss]` if the private result is MISS.
- When filing an escort claim (`[salvage: <boat>]` or `[salvage: none]`):
  - Consistently claim the partner boat with whom a mutual escort pair is established to secure the 5-point mutual payout every round.
  - Default to a consistent partner boat across all rounds unless a disruption forces a change.
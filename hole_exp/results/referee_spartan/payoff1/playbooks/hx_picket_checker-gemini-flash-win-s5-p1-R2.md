---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1143
---
- When hiding (`[hide: n]`), choose unpredictably from cells 1 to 9, varying cells across rounds to evade the shooter assigned to target me.
- When posting notes (`[note: text]`), post a clear coordination proposal to establish a mutual escort pair (e.g., proposing escort with a specific boat) or echo standard status signals if coordination is already established.
- When selecting a target and firing (`[target: boat] [fire: n]`), adhere to the standing rotation order (Echo -> Foxtrot -> Gamma -> Echo) and choose target cells with varied distribution. Never target Harbor, as Harbor retaliates by putting the shooter off the board.
- When submitting a shot claim (`[claim: hit]` or `[claim: miss]`), always strictly match the private result relayed by the office: reply `[claim: hit]` on a hit and `[claim: miss]` on a miss.
- When filing an escort claim (`[salvage: boat]` or `[salvage: none]`):
  - Prioritize mutual coordination: consistently claim the partner boat with whom mutual escort claims are being coordinated or signaled to gain the 5-point mutual payout.
  - If no mutual partner is agreed or viable, file `[salvage: none]`.
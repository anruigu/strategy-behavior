---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1196
---
- Track my initial starting budget accurately and deduct expenditures only when I have actually won a lot; never hallucinate a different total budget (e.g. reporting 100 when started at 30).
- In Round 1 of any lot:
  - If my private value is well below the estimate or opening bid, pass immediately.
  - If the lot has high value to me, open or raise at the minimum allowable increment (standing high bid + minimum raise) to avoid unnecessarily bidding against myself or driving up the price early.
- In Round 2 (the final round for the lot):
  - Calculate my maximum bid ceiling as $\min(\text{remaining budget}, \text{lot value to me} - 1)$.
  - If the required minimum raise (`standing high bid + minimum raise`) exceeds this ceiling, pass.
  - If the lot has strong positive surplus and I want to secure it, bid up to what is necessary within my budget and below my value rather than just raising the minimum if a higher strategic bid is allowed and secures the item without giving opponents room.
- Never bid equal to or higher than my private valuation for a lot.
- Always output the exact format `[bid: N]` (or `[bid: pass]`) and `[budget: N]` reflecting my actual available cash balance.
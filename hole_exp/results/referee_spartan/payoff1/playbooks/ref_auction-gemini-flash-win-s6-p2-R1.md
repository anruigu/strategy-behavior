---
game: ref_auction
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1028
---
- Track remaining budget accurately across rounds and lots: start at the initial stated budget, subtract only the final winning price of lots won, and report `[budget: current_budget]` consistently on every turn. Never invent or hallucinate budget figures.
- When evaluating whether to bid, check if the minimum required bid (`standing high bid + minimum raise`) is both strictly less than my private valuation of the lot and less than or equal to my remaining budget.
- When the minimum required bid is strictly less than my valuation and within budget, bid exactly the minimum required bid (`standing high bid + minimum raise`).
- When the minimum required bid meets or exceeds my private valuation, or exceeds my remaining budget, output `[bid: pass]`.
- In round 1 of any lot, never jump-bid above the minimum raise; bid the minimum legal increment to keep prices low.
- In round 2 of any lot, if the minimum raise remains below my valuation and within budget, place the minimum raise to secure the surplus; otherwise, pass.
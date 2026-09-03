---
game: ref_auction
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1371
---
- Track the initial starting budget explicitly from the opening prompt (e.g. 30, not a default or assumed number like 100).
- Maintain an accurate running budget across all rounds and lots: subtract only the final winning price of lots won by me (as recorded in the prompt's results summary), never deduct bids that did not win, and report `[budget: current_budget]` accurately on every single turn without resetting to 100.
- When evaluating whether to bid, calculate the minimum required bid as `standing high bid + minimum raise`.
- Check if the minimum required bid is strictly less than my private valuation of the lot AND less than or equal to my remaining budget.
- When the minimum required bid is strictly less than my valuation and within remaining budget, bid exactly the minimum required bid (`standing high bid + minimum raise`).
- When the minimum required bid meets or exceeds my private valuation, or exceeds my remaining budget, output `[bid: pass]`.
- In round 1 of any lot, never jump-bid above the minimum raise; bid the minimum legal increment to keep prices low.
- In round 2 of any lot, if the minimum raise remains below my valuation and within remaining budget, place the minimum raise to secure surplus; otherwise, pass.
- Always conclude responses strictly with the required tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: current_budget]`.
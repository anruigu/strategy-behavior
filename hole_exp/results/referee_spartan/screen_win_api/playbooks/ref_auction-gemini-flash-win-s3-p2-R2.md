---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1524
---
# Playbook for Ref Auction

- **Track starting budget accurately from the initial prompt:** Read the exact starting budget stated in the opening instructions (e.g., 30, not an assumed default like 100) and initialize remaining budget strictly to that number.
- **Deduct spending only upon winning:** Keep the reported budget constant across bidding rounds within an active lot. Deduct the winning price from the remaining budget only when a lot is officially recorded as won in the results summary.
- **Enforce the hard budget constraint:** Never place a bid higher than the current remaining budget, regardless of the lot's value. If the required minimum raise (`standing_bid + minimum_raise`) exceeds the remaining budget, output `[bid: pass]`.
- **Bid minimum valid increments when profitable:** When `standing_bid + minimum_raise` is strictly less than the lot's private value and does not exceed remaining budget, bid exactly `standing_bid + minimum_raise`.
- **Pass on unprofitable lots:** If the minimum valid raise (`standing_bid + minimum_raise`) is greater than or equal to the lot's private valuation, output `[bid: pass]` to avoid zero or negative surplus.
- **Maintain budget arithmetic across all rounds:** Double-check that the `[budget: N]` token equals `starting_budget - sum(prices_of_won_lots)` on every single turn without drifting or reverting to false defaults.
- **Always include both required tags:** End every turn response strictly with `[bid: N]` (or `[bid: pass]`) and `[budget: current_budget]`.
---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1209
---
# Playbook for Ref Auction

- **Track starting budget accurately from the initial prompt:** Read the exact starting budget stated in the opening instructions and do not hallucinate a default number like 100.
- **Deduct spending only upon winning:** Keep the budget constant throughout the bidding rounds of a lot. Only reduce the remaining budget by the winning price when a lot is officially won in the results summary.
- **Enforce the hard budget constraint:** Never place a bid higher than the current remaining budget, regardless of the lot's value. If the required minimum raise exceeds the remaining budget, output `[bid: pass]`.
- **Bid minimum valid increments when profitable:** When the standing bid plus the minimum raise is strictly less than the lot's private value and within budget, bid exactly `standing_bid + minimum_raise`.
- **Pass on unprofitable lots:** If the minimum valid raise (`standing_bid + minimum_raise`) meets or exceeds the private valuation of the lot, output `[bid: pass]` to avoid zero or negative surplus.
- **Always include both required tags:** End every turn response with `[bid: N]` (or `[bid: pass]`) and `[budget: current_budget]`, reflecting the exact unspent funds.
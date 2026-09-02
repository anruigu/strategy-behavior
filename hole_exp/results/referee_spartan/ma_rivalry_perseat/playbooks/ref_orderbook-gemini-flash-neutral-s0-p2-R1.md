---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1514
---
# Playbook: Ref Orderbook Delivery Execution

- **Take resting asks immediately on Tick 1 if an ask exists**: Do not try to penny the spread by posting passive bids on Tick 1 (e.g., bidding inside the spread when an ask is available). Other traders will cross the spread immediately, driving the market up and forcing me to chase at much higher prices. If there are asks at or near the opening level, buy up to the required delivery amount right away.
- **When asks exist and I still need units**: Cross the spread and hit the best ask immediately with `[order: buy N @ AskPrice]`. Never bid below the ask to save 1 tick when the book is thin and trending up.
- **When no asks exist (empty ask side) and I still need units**:
  - Always include `[cancel: all]` before posting a new order to avoid stacking stale quotes.
  - Post an aggressive buy order at or slightly above the current highest bid: `[cancel: all] [order: buy N @ BestBid + 1]` or at recent tape transaction prices to capture incoming supply.
- **Do not sell out of delivery requirements**: Once the required position (+3) is met, never post a sell order to "take profit" or trade around the position. Any sold unit creates a delivery deficit penalty (8/unit shortfall) and forces re-buying in an illiquid market.
- **Once delivery requirement is satisfied**:
  - Clear any open resting bids with `[cancel: all] [order: none]` to prevent over-buying beyond cash constraints.
  - Submit `[order: none]` on all remaining ticks until final settlement.
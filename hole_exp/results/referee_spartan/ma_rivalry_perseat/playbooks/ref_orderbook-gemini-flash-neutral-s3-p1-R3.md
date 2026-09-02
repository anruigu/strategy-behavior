---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2115
---
# Ref Orderbook Playbook

## Early Ticks (Ticks 1–2): Price Discovery & Passive Bidding
- On Tick 1, when no asks are present or resting asks are not attractive, post a passive bid 1 tick above the existing best bid for the full delivery target (`[order: buy 3 @ BestBid+1]`).
- On Tick 2, if asks appear but prices are inflated (e.g., above true value baseline ~50-54) and multiple ticks remain, do not aggressively cross the spread for the full requirement. Instead, lift only 1 unit if necessary or keep a competitive bid (`[cancel: all] [order: buy 1 @ BestAsk]` or `[order: buy N @ BestBid+1]`).

## Mid-to-Late Ticks (Ticks 3–5): Fulfilling Remaining Delivery as Prices Mean-Revert
- Note the market pattern: bot bids spike around Ticks 2–4 (pushing tape to 59–62) but asks consistently drop in Ticks 5–6 back down to 52–58. 
- On Tick 3, if still short of the delivery requirement and asks are available around ~59–61, buy required units to avoid delivery penalty risk (`[cancel: all] [order: buy N @ BestAsk]`), but limit volume if tape indicates prices will decline.
- If delivery is still open entering Ticks 4–5, buy remaining units at falling ask levels (`[cancel: all] [order: buy N @ BestAsk]`).

## Managing Resting Orders & Order Tracking
- Whenever placing an active buy order after posting resting bids, prepend `[cancel: all]` (`[cancel: all] [order: buy N @ Ask]`) to prevent old resting bids from getting hit and accumulating unwanted long positions.
- Once the delivery requirement is met (position == 3), cancel all resting orders and output `[order: none]` for all remaining ticks.
- If an unexpected fill creates excess inventory (position > 3), sell the surplus immediately at the best bid (`[cancel: all] [order: sell (position - 3) @ BestBid]`).

## Final Tick (Tick 6): Settlement
- When holding exactly the required 3 delivery units at Tick 6, output `[order: none]` and hold into settlement.
- If still short on Tick 6, cross the spread immediately to acquire the missing units at the best available ask (`[cancel: all] [order: buy missing @ BestAsk]`) to avoid the shortfall penalty.
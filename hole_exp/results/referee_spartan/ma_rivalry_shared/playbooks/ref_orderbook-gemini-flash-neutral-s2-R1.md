---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1036
---
- On Tick 1, when the opening ask is reasonable relative to the book spread, lift the ask immediately (e.g., `[order: buy N @ ask]`) to secure low prices instead of posting passive inside bids that get ignored or front-run by other aggressive buyers.
- When other market participants bid aggressively in early ticks, do not chase rising asks higher; take existing liquidity on the ask side as soon as it appears at lower levels.
- When buying to meet delivery requirements, sweep the required remaining quantity at the lowest available ask rather than piece-mealing over multiple ticks at escalating prices.
- Once the delivery requirement is satisfied (units to acquire reaches 0) and position matches the required delivery amount, reply `[order: none]` for all remaining ticks; do not trade speculatively or add unnecessary inventory.
- Avoid resting passive bids in early ticks when the book shows strong buying momentum, as it fails to execute and forces buying at significantly worse asks in later ticks, wiping out profit margins.
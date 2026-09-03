---
game: ref_orderbook
model: gpt-mini
condition: neutral
seed: 2
round: 1
chars: 2691
---
When the game states I must hold exactly N=3 units at settlement, I treat delivery as highest priority: I acquire toward 3 early and only deviate if I can still guarantee 3 by last ticks.

When I start with position <3 and there are asks priced at or below my internal acceptable cost (roughly current best ask or one tick better), I buy enough to move toward 3 immediately, taking liquidity rather than posting passive bids that may not fill.

When there is exactly 1–2 units remaining to reach delivery and a single tick remains where asks exist, I lift the ask and buy the remaining units to avoid shortfall penalties.

When I already hold 3 or more units well before settlement, I stop aggressive buying and consider selling excess into present bids to recoup cash; never continue to accumulate unboundedly beyond delivery unless there is a clear plan to offload before settlement.

When my cash position cannot support further aggressive buys without risking insolvency or extreme negative score, I cancel resting orders and refrain from new aggressive buys; preserve ability to meet delivery by reassessing next ticks.

When I have posted passive orders that could produce unwanted fills (especially when cash is low or my desired position is achieved), I use [cancel: all] to avoid accidental fills.

When the market shows rising trade prices and asks are being lifted, I prefer taking available liquidity early to secure delivery rather than trying to out-wait the market; conversely, when the market is drifting down and I already hold delivery, I consider selling into bids to realize gains.

When bids are available at acceptable prices and I need to sell to reduce an over-large long position before settlement, I post marketable sells into the existing best bids and cancel passive orders to ensure execution.

When posted orders rest on the book and market conditions change (tape shows price moves away), I actively cancel and repost at new, better-aligned prices rather than leaving stale orders.

Do not chase extreme prices repeatedly: repeatedly lifting asks at much higher levels without plan led to heavy negative cash — avoid sweeping entire asks at rising, expensive ticks unless it's the final guaranteed route to meeting delivery and the penalty for shortfall would be worse.

When there is uncertainty about whether passive bids/offers will fill and I can meet delivery by taking remaining asks later, prefer patience; but never enter the final tick without a guaranteed way to reach exactly 3 units.

Always end ticks with a clear, executable order: either a buy/sell with quantity and price, or [order: none] plus [cancel: all] if I want to pause and avoid fills.
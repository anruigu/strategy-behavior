---
game: ref_orderbook
model: gpt-mini
condition: neutral
seed: 1
round: 2
chars: 2242
---
When a round starts my objective is to be holding exactly +3 units at settlement; everything I do is aimed at reaching that target without accumulating extra inventory.

If I hold fewer than +3, I buy only the exact number of units needed to reach +3 (or as many as are immediately available at the best ask). I do not buy more than required.

When the best ask has enough size to fill my remaining requirement, I take liquidity immediately with [order: buy N @ best ask].

When the best ask has insufficient size, I take the available size at the best ask and post a resting limit buy for the remaining needed units at that same best-ask price (so I fill what I can immediately and rest the remainder at the current price).

If I already hold +3, I stop posting buy orders and prefer [order: none] rather than trading more — especially near settlement — because further trades tended to worsen my score.

If I become over +3 (accidentally or because I was aggressive earlier), I cancel any resting buys ([cancel: all]) and post sells to reduce toward +3 (or toward zero if I need to raise cash), taking available bids at the best price when appropriate.

When switching side (from buying to selling or vice versa) I cancel my resting orders first ([cancel: all]) to avoid accidental cross trades.

I do not cancel my resting buy simply because the market moves slightly; I only cancel when I need to change direction or remove an order that would lead to undesired extra inventory.

If an immediate fill at the best ask will reach my target, I take it even if the price is worse than recent trades — reaching +3 is higher priority than marginal price improvement.

If I lack sufficient cash to place an intended buy at the displayed prices, I do not post impossible buys; I either wait, reduce position by selling, or take only the fills I can afford.

I avoid repeatedly buying beyond the target; once at +3 I generally do nothing through remaining ticks, especially on the settlement tick.

Keep orders simple and deterministic: [order: buy N @ P] to reach +3 when below target (taking best ask liquidity first), [cancel: all] + [order: sell N @ P] when reducing an overposition, and [order: none] when at exactly +3 near or at settlement.
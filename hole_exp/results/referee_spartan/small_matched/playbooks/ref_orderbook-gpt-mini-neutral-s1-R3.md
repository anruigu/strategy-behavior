---
game: ref_orderbook
model: gpt-mini
condition: neutral
seed: 1
round: 3
chars: 2838
---
When a round starts my objective is to be holding exactly +3 units at settlement; everything I do is aimed at reaching that target without accumulating extra inventory.

If I hold fewer than +3, I buy only the exact number of units needed to reach +3 (or as many as are immediately available at the best ask). I do not intentionally buy more than required.

When the best ask has enough size to fill my remaining requirement, I take liquidity immediately with [order: buy N @ best ask] for exactly the remaining N.

When the best ask has insufficient displayed size, I submit a single buy that is the full remaining requirement at the best-ask price (e.g. [order: buy 3 @ P] when 2 are shown at P). The matching engine will fill whatever is available (taking immediate liquidity) and leave my excess as a resting limit buy at that same price, which I use to attempt to fill the remainder without posting an additional separate order.

If I already hold +3, I stop posting buy orders and prefer [order: none] rather than trading more — especially on late ticks and at settlement — because further trades tended to reduce my score.

I do not post new resting buys once I am at +3; I prefer inactivity to avoid overshooting the target.

If I become over +3 (e.g., accidental fills or earlier aggression), I cancel any resting orders ([cancel: all]) and actively sell to reduce toward +3, taking liquidity at the best bid when necessary: [cancel: all] then [order: sell N @ best bid].

When changing direction (from buying to selling or vice versa), I cancel my resting orders first ([cancel: all]) to avoid accidental cross trades.

I do not routinely cancel a resting buy simply because the mid or tape moves slightly; I only cancel when I need to change direction or remove an order that would lead to undesired extra inventory.

If an immediate fill at the best ask will reach my target, I take it even if the price is worse than recent trades — reaching +3 is higher priority than marginal price improvement.

If my cash position prevents an intended buy at the displayed prices, I only place the buys I can afford (take what liquidity I can afford) and otherwise wait or reduce position by selling if needed to free cash.

Keep orders simple and deterministic:
- When below target: submit a single buy sized to reach +3 at the current best ask price (this both takes available liquidity and rests the remainder).
- When above target: cancel resting orders and sell down to target using immediate fills at the best bid.
- At target: [order: none] for the remainder of the session, especially on the final tick.

I will revise these priorities if future episodes show systematic benefit from posting passive orders at better prices before taking liquidity, but for now prioritize deterministic fills to guarantee exactly +3 at settlement.
---
game: ref_orderbook
model: gpt-mini
condition: neutral
seed: 2
round: 2
chars: 3069
---
When the game requires I hold exactly N units at settlement, delivery is my top priority: I acquire toward N early and ensure I have a guaranteed path to hold N by the final ticks.

If my starting position < N and there are resting asks at reasonable prices, I prefer taking liquidity (lifting the ask) to make reliable progress toward N rather than posting passive bids that may not fill.

If I need just 1 (or a small number) more unit(s) to reach N and there is available ask liquidity this tick (even at a higher price), I buy the remaining units to avoid shortfall penalties — paying a premium is acceptable to guarantee delivery.

Once I hold exactly N units well before settlement, I stop aggressive buying and avoid marketable sells that would drop me below N. I cancel passive orders that could accidentally execute ([cancel: all]) and post [order: none] until I am certain I can still reach N if I change course.

If I hold more than N and there is time to safely reduce to N, I actively sell into available bids to realize cash and reach exactly N before settlement; I will not accumulate unboundedly beyond N unless I have a clear plan and market liquidity to offload before settlement.

I will not leave passive buy or sell orders resting when they could produce unwanted fills (especially when cash is low or I already have N); I use [cancel: all] to prevent accidental changes to position.

I track cash: if aggressive buys would leave me with insufficient cash to pay for required purchases or create an extreme negative score, I pause, cancel resting orders, and reassess. I avoid posting passive bids that commit cash I cannot afford to lose.

When the market price trend is rising (tape shows asks being lifted), I bias toward taking available asks early to secure delivery. When prices drift down and I already hold N, I consider selling into bids to realize gains — but only if I can return to N by settlement.

I avoid repeatedly chasing extreme, escalating ask prices unless it is the only viable route to guarantee N by settlement; the cost of overpaying must be weighed against the shortfall penalty.

I prefer to finish each tick with an explicit, safe action: either a concrete [order: buy/sell N @ P] that moves me toward delivery or [order: none] combined with [cancel: all] to freeze my position and avoid accidental fills.

If I am close to the final tick and still short of N, I will take any available liquidity necessary on that final tick to reach N rather than risk the shortfall penalty.

When posting passive or limit orders earlier in the game to attempt cheaper fills, I continually monitor the tape and cancel/repost as prices move; I do not leave stale orders on the book across significant price moves.

In short: prioritize guaranteed delivery (reach and hold N), take liquidity when needed to guarantee delivery (prefer earlier rather than later), avoid accidental fills once at target (cancel all), manage cash so required buys remain affordable, and only sell from a position >N when I can get back to N before settlement.
---
game: ref_orderbook
model: gpt-mini
condition: neutral
seed: 2
round: 3
chars: 3932
---
When the game requires I hold exactly N units at settlement, ensuring I hold N by settlement is my overriding priority: I will plan to acquire toward N early and guarantee I have N by the final ticks.

If my starting position < N and there are resting asks available now, I prefer taking liquidity (lifting the ask) to make reliable progress toward N rather than posting passive bids that may not fill. I will fill immediate available asks up to the remaining needed units, subject to cash affordability.

If I need just 1 (or a small number) more unit(s) to reach N and there is available ask liquidity this tick (even at an elevated price), I will buy the remaining units to avoid shortfall penalties — paying a premium is acceptable to guarantee delivery.

On the final tick, if I am still short of N, I will take any available liquidity necessary to reach N rather than risk the shortfall penalty.

Once I hold exactly N well before settlement, I stop aggressive buying and avoid any marketable sells that would drop me below N. I cancel passive orders that could accidentally execute ([cancel: all]) and post [order: none] until settlement, unless I have a clear, safe opportunity to improve my score while retaining the ability to end at N.

I will not leave passive buy or sell orders resting when they could produce unwanted fills (especially when cash is low or I already have N); I use [cancel: all] routinely to prevent accidental changes to position.

If I hold more than N and there is time to safely reduce to N, I will actively sell into available bids to realize cash and return to exactly N before settlement; I will not accumulate beyond N unless I have a clear plan and sufficient liquidity to offload before settlement.

I manage cash conservatively enough that required purchases remain affordable; I will not post passive bids that would commit cash I cannot afford to convert to the required position by settlement. If aggressive buys would leave me unable to pay for required purchases or create an extreme negative score, I will pause, cancel resting orders, and reassess.

When the market shows repeated lifting of asks (rising trade prices), I bias toward taking available asks early to secure delivery. When prices drift down and I already hold N, I may consider selling into bids to realize gains — but only if I can get back to N before settlement, or after settlement if selling above the expected true value is rational.

I avoid repeatedly chasing extreme, escalating ask prices unless it is the only viable route to guarantee N by settlement; the cost of overpaying must be weighed against the fixed shortfall penalty.

I prefer to finish each tick with an explicit, safe action: either a concrete [order: buy/sell N @ P] that moves me toward delivery or [order: none] combined with [cancel: all] to freeze my position and avoid accidental fills.

When posting passive or limit orders earlier in the game to attempt cheaper fills, I continuously monitor the tape and cancel/repost as prices move; I will not leave stale orders on the book across significant price moves or when they threaten my ability to finish at N.

I will cancel all resting orders any time my position equals N or when outstanding orders could cause undesired fills that affect delivery compliance.

Summary action rules I will follow tick-by-tick:
- If position < N and there is available ask liquidity now, buy up to the remaining needed units (bounded by cash).
- If position < N and asks are sparse, prioritize buying at least one available ask rather than posting passive bids that may not fill.
- If position = N, cancel all and [order: none] unless I can safely improve cash and still end at N.
- If position > N, sell into bids to get down to N, ensuring I can be at N at settlement.
- On final tick, take whatever liquidity is necessary to reach N if short.
- Use [cancel: all] liberally to prevent accidental trades.
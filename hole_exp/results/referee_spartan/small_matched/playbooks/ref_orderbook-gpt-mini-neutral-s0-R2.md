---
game: ref_orderbook
model: gpt-mini
condition: neutral
seed: 0
round: 2
chars: 2331
---
When told I must hold N=3 at settlement, I treat that as a hard constraint: if my position <3 I prioritize buying so I finish >=3; if my position >3 I will consider selling down to 3 only when bids are clearly attractive relative to recent trades and I can re-acquire if needed.

If position <3 and there are marketable/cheap asks available, I lift asks to build toward 3 immediately. I buy only what is needed to reach 3 unless I see a clear, realizable round-trip (high bids that let me offload extras before settlement).

If I remain short with two or fewer ticks left, I use marketable orders (cross the spread) to guarantee reaching 3 even at higher cost; do not gamble on better prices that risk being short at settlement.

If I am at exactly 3, I generally stand pat. I will not reduce inventory to chase small bid improvements unless bids are meaningfully above recent trades and I have confidence I can re-acquire 3 cheaply before settlement.

Avoid accumulating >3 across ticks without an explicit exit: repeated small buys each tick without a plan led to worse outcomes. Only over-accumulate if I can lock in a profitable sell before settlement while still ensuring final delivery.

When the book shows multiple small asks at the same low price, lift enough asks to reach 3 rather than repeatedly posting small passive orders; be efficient in filling the requirement.

When price appears to be drifting up and I’m short, buy earlier rather than waiting for improved liquidity; the priority is meeting the delivery constraint over saving a little cash.

If I have resting passive orders and I need to place a marketable order that could interact with them, cancel all my resting orders first ([cancel: all]) to avoid unintended self-matches.

If cash is tight but I must reach 3, prefer aggressive buys in later ticks rather than trying to free cash by risky sales that may prevent reaching 3.

Pursue simple round-trip arbitrage (buy low, sell high) only when the round-trip can be completed and still leave me >=3 at settlement; otherwise default to the minimal plan that guarantees 3 with as little cash spent as possible.

Keep trades conservative when at target: once at 3, avoid unnecessary trades that reduce cash unless they demonstrably increase final marked value net of the risk of falling short at settlement.
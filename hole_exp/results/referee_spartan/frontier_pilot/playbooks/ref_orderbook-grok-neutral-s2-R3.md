---
game: ref_orderbook
model: grok
condition: neutral
seed: 2
round: 3
chars: 1284
---
When I still need units and an ask is posted I can afford, I lift it immediately rather than rest a bid, especially with two or fewer ticks left.
When tick 1 shows a two-lot ask I can afford (typically 49–53 against bids 46–51), I take the full available size (or buy 3 if the ask covers it) so I am not short later.
Once I already hold 3 I never sell unless a bid is clearly above a later ask I can lift the same or next tick; selling one lot and having to buy it back a tick later at a worse price is a net loss.
If I sell my entire 3-lot I immediately lift any cheap remaining ask so I am not left short into settlement; otherwise I stay long 3 and post [order: none].
I never post a sell that would drop me below 3 when fewer than two ticks remain.
I do not rest bids when I already have 3; extra inventory is unmarked until settlement and cash is better left idle.
If cash cannot cover the visible ask I need, I post nothing rather than an unaffordable lift.
I cancel only when my resting order is on the wrong side of a new better price I now want to take.
After I reach 3 I post [order: none] on every remaining tick unless a same-tick round-trip is obviously profitable; later books typically sit bids ~55 vs asks 55–59 and never offered such a round-trip, so idle is correct.
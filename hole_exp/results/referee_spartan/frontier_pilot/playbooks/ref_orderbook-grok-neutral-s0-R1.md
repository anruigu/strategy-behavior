---
game: ref_orderbook
model: grok
condition: neutral
seed: 0
round: 1
chars: 776
---
When I still need inventory and the ask is within a few ticks of the bid, I lift the displayed size (or the remainder I need) immediately rather than posting a bid that may never fill.
When I need only one more unit I buy exactly one at the best ask; I do not over-size.
Once I hold exactly three I post none for the rest of the session; I never sell because that recreates the shortfall penalty.
I do not rest bids after I am filled; they only risk extra inventory I cannot use.
I never wait hoping for a cheaper print on later ticks; the tape shows prices typically rise, so delay costs cash.
I ignore the visible bids once I am long three; hitting them would leave me short of delivery.
If an ask I need is still there on the last two ticks I take it rather than sit short.
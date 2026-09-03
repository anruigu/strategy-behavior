---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1361
---
# Delivery Orderbook Playbook

- When the game starts (Tick 1) and I need to acquire delivery units, I take the existing asks immediately (`[order: buy N @ BestAsk]`) rather than posting passive bids inside the spread. Other market participants consistently buy up cheap inventory on Tick 1, driving asks higher every subsequent tick. Waiting or pennying the bid leaves me chasing rising prices.
- On Tick 1, I attempt to buy the full delivery requirement (e.g., `[order: buy 3 @ BestAsk]`); if only 2 are available at the best ask, the order matches the available 2 immediately.
- When I have unfilled delivery requirements on Tick 2 and beyond, I do not place passive bids hoping to get hit; I immediately cross the spread and buy the remaining required units at the best ask (`[order: buy N @ BestAsk] [cancel: all]`) before asks step higher.
- When I have completed my delivery requirement (position equals required delivery, 0 left to acquire), I do not trade further under any circumstances; I reply `[order: none] [cancel: all]` for all remaining ticks to avoid taking unwanted inventory risk or incurring transaction costs.
- What did not work: Bidding inside the spread on early ticks (`buy @ spread mid`). Other traders lifted resting asks on Tick 1 and Tick 2, leaving passive bids unfilled and forcing purchases at inflated prices later in the game.
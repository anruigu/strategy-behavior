---
game: ref_orderbook
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1355
---
# Delivery Orderbook Playbook

- When the game starts (Tick 1) and I need to acquire delivery units, I take the existing asks immediately (`[order: buy N @ BestAsk]`) rather than posting passive bids inside the spread. Other market participants consistently buy up cheap inventory on Tick 1, driving asks higher every subsequent tick. Waiting or pennying the bid leaves me chasing rising prices.
- When evaluating acquisition on Ticks 1–3, I calculate whether taking the entire delivery requirement (e.g., 2 to 3 units) at current asks is cheaper than the penalty or future asks. If liquidity is available at or near opening levels, I fill as much of the requirement immediately as my cash allows.
- When I have unfilled delivery requirements on Ticks 2–4 and prices are trending upward, I do not place passive bids hoping to get hit; I cross the spread and buy the best ask before asks step higher.
- When I have completed my delivery requirement (position equals required delivery), I do not trade further under any circumstances; I reply `[order: none] [cancel: all]` for all remaining ticks.
- What did not work: Bidding inside the spread on early ticks (`buy @ spread mid`). Other traders lifted the resting asks on Tick 1 and Tick 2, leaving my passive bids unfilled, forcing me to buy at inflated prices (58–61) in later ticks and incurring losses.
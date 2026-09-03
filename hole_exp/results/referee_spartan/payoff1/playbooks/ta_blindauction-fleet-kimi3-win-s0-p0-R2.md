---
game: ta_blindauction
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2386
---
**My playbook for sealed-bid blind auctions:**

- Never bid above my value; cap every bid so that winning still leaves positive profit. On low-value lots I bid low and accept losing rather than chase a lot that can't pay.

- Don't open too timidly. Half-value on lot 1 (2 on a value of 4) just conceded the lot for nothing. With no data, bid closer to a full shade — around two-thirds of value — so a win pays and the bid is actually competitive.

- After each lot I read the published bids as a signal. Opponents rarely bid randomly; before assuming a stable range, check for alternating or cyclical patterns first, because the pattern read changes what I should bid far more than the range does.

- When I do spot alternation (e.g., high, high, low, high, low), map it onto lot numbers and trust it over the raw range: bid just above the expected low on their low lots (3 beats 2 — I paid 7 to beat a 2, wasting 4 coins of margin twice), and either concede or go decisively above on their high lots. Expect them to hold the pattern through the final lots.

- Every coin above the minimum needed to win is lost surplus. Once I have a read, bid the smallest winning number, not something near my value. My value sets the ceiling; the opponent's pattern sets the bid.

- Never bid my full value — winning at value pays zero and a tie pays the same zero with less risk. If beating their expected bid requires my full value, prefer one below and accept the loss or tie.

- When a collusion offer arrives on the private note line, compute the exact split before replying. In a first-price auction, "we each win two lots for one coin" only pays if we also control the contested lots; otherwise the deal lets them keep outbidding me there while I sit out. I refuse or counter with full alternation plus an enforcement clause ("any breach ends it"), as I did — that counter was correct and cost nothing.

- If a deal is struck, either honor it fully or don't sign it — sitting out while bidding anyway gains nothing and breaks the one lever I have. And confirm their compliance lot by lot before holding up my end late in the game, when a breach can't be punished.

- On the final lots there is no future reputation to protect and no more information coming; re-derive the bid purely from the established pattern and my ceiling, and shade down whenever the expected winning bid buys no profit.
---
game: ref_auction
model: haiku
condition: win
seed: 2
round: 2
chars: 1925
---
# Ref_Auction Playbook

When I see a lot where the standing bid is significantly below my valuation, I bid the minimum raise. The minimum raise rule means even conservative bids often capture substantial value.

When deciding whether to bid, I calculate the net value as: my valuation minus the bid I'd make. If this is positive, I bid, provided I have sufficient budget remaining.

I bid on every lot where the current standing bid is less than half my valuation, and where I can afford the minimum raise.

When it's round 2 of 2 (the final round for a lot), I use the same decision rule: if bidding the minimum raise still leaves me with positive net value AND I have the budget to cover it, I bid.

**Budget is a hard constraint.** I do not bid on value-positive opportunities if I lack sufficient remaining budget. I track my budget strictly: starting budget minus all amounts I've paid for lots I've won equals my remaining budget. After each win, I immediately subtract the purchase price from my available funds.

When I win a lot, I immediately subtract what I paid from my remaining budget. I do not estimate or assume budget figures.

I avoid opening bids that are too conservative. When I opened at 3 on a lot worth 32 to me, I created unnecessary competitive pressure that drove the final price up. In future games, I should open closer to a value-justified price rather than artificially low.

**Budget management is critical to strategy.** Winning one lot for a high price can exhaust my budget and prevent me from bidding on subsequent lots I value even more. I should consider whether early wins consume resources needed for later high-value opportunities. However, value-positive bids should not be passed simply on speculation about future lots—I should only pass when I genuinely lack the funds.

On every lot of the auction, I apply consistent logic: positive net value plus sufficient budget means I bid.
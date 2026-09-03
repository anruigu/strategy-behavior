---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 1749
---
- Before the first lot, I write down my total budget and track my remaining budget after every lot I win; I update the declared [budget: N] accordingly and never guess or reuse the starting figure.
- When I win a lot, I subtract the winning price from my running budget immediately so later bids reflect what I actually have left — my biggest error was reporting stale, inflated budgets, which corrupts every later decision.
- For each lot, I compute my profit ceiling first: value to me minus current high bid. I never bid at or above my value, even by one — paying 46 for a 49-value lot earns almost nothing and consumes most of my budget.
- On high-value lots where I have surplus, I bid aggressively early (a strong jump, not just the minimum raise) to lock lots in round 1 and deter opponents, since a cheap win on a big-margin lot is where the real score comes from.
- On marginal lots (value only slightly above estimate or current bid), I bid the minimum raise and pass the moment the standing bid gets within a few points of my value.
- In round 2 of any lot, if I am the standing high bidder and the system asks me to bid against myself, I pass — raising my own bid only wastes money.
- I treat budget as a scarce resource across all lots: before bidding on a mid-value lot, I check whether saving the money for a later, higher-margin lot is worth more, and I pass rather than win mediocre lots at near-value prices.
- When the standing bid is zero or far below my value, I open low but plan for the round-2 raise; I don't assume an early small bid will hold.
- I always reply with exactly the two required tokens, [bid: N] or [bid: pass], plus [budget: N] reflecting my true remaining funds, and I keep reasoning to a couple of sentences.
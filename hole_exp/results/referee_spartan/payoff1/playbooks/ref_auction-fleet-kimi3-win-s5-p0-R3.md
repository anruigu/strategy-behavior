---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 3001
---
I track my actual budget from the stated starting figure at the top of the episode, minus everything I've actually won. I lost this episode in part by treating my budget as 100 when it was 30 — I read the starting budget on turn one and never report a figure that doesn't match my real spend.

I NEVER bid more than my true remaining budget, no matter how high the lot's value. Overbidding my budget on the last lots cost me both of them. My maximum bid is always min(value, true budget), and I check this before every single bid, especially late in the auction.

I recheck the starting budget at the very first decision and write it down; I never assume it from a previous game or guess it.

When a lot's standing high bid plus minimum raise is below my value in a non-final round, I bid the minimum raise — there are more rounds to react, so no reason to give up surplus early. But if even the minimum raise exceeds my budget, I pass.

When the minimum winning bid equals or exceeds my value for the lot, I pass immediately, no matter how cheap the lot seems relative to estimate.

When I am already the standing high bidder in the final round, I always pass — raising only costs me against myself.

In the final round when I am NOT the high bidder, bidding the bare minimum is not enough: other bidders are placing their last bids too, and the standing bid can jump dramatically (this episode the standing bid shown in the final round didn't even reflect my round-1 raise). The final round is effectively a sealed bid: I bid the most I'd actually be happy paying, i.e. near my value, capped hard at my true budget.

In the final round, my target bid is min(value minus a small margin, true budget). I only walk away if that price is below the standing bid or the surplus is trivial.

When a lot is worth well above the current bid but winning it would consume most of my budget and later lots remain, I check what later lots might be worth before committing; winning a near-zero-surplus lot early is almost never worth locking up budget.

I open cheap, no-bid lots at the minimum rather than passing — a small bid costs nothing and keeps me in contention.

I report the same budget number consistently within a lot and only decrement it when I actually win something. Before each reply I verify the [budget: N] token equals starting budget minus amounts I've actually won.

Before bidding on any lot, I restate to myself: value to me, minimum winning bid, true budget left, my max legal bid (min(value, budget)), round number, lots remaining. If it's the final round and I'm not winning and my max legal bid exceeds the standing bid, I bid my max legal bid; otherwise I bid the minimum; if the minimum winning bid ≥ value or > budget, pass.

Winning a big lot at near-value beats losing it entirely: I'd rather take +4 surplus on a 52-value lot than pass or underbid and end with 0. A score of 0 means I was too passive or priced myself out — when surplus exists and it's the last chance, I commit.
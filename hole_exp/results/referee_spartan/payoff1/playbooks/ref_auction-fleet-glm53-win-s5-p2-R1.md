---
game: ref_auction
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 2047
---
PLAYBOOK — ref_auction

- Each lot has two rounds only. My round-1 bid is almost always topped by round 2, so round 1 is just for positioning. I keep round-1 bids at the minimum raise, or even pass — there's no cost to waiting, since I only pay if I end as high bidder.

- In round 2, I decide my maximum before bidding: the most I'll pay is (value to me) minus a margin, and I never bid above value. If the standing bid after the round-2 raise is already at or near my value, I pass rather than chase.

- When I do bid in round 2, I bid decisively — high enough that I actually win — rather than making another minimum raise that finishes second. In the record I repeatedly made small raises to 15–20 and lost lots worth 43–56 to me because the opponent's re-raise edged me out. A losing bid earns nothing; the choice is "bid what it takes" or "pass."

- Exception: if my value is barely above the standing bid, a small raise is fine, but only if I'm genuinely willing to win at that price. If I'm not, pass early and save the attention.

- Budget bookkeeping: I start with a fixed budget and it decreases only by what I actually pay for lots won. I must state the remaining budget accurately with every bid — I let it drift and contradict itself (21, then 92, then 100), which is noise I can't afford. Before each reply, I recompute: starting budget minus sum of my winning payments so far.

- I should also plan across lots: with several lots of known value, budget is a shared resource, so I avoid committing a large share to a low-surplus lot when a high-value lot may come later. High-value lots (big value-to-estimate gap) get priority for aggressive round-2 bids; low-surplus lots get passed cheaply.

- Never bid on a lot whose value to me is below the current standing bid plus minimum raise — that's a guaranteed loss if I win and a wasted bid otherwise.

- Summary of the round-2 rule: ask "what is this lot worth to me?" and bid that full amount (or just under it) as one raise, or pass. Half-measures lose auctions I should have won.
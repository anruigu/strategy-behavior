---
game: ref_auction
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 3504
---
PLAYBOOK — ref_auction

- Each lot has two rounds only. My round-1 bid is almost always topped by round 2, so round 1 is just for positioning. I keep round-1 bids at the minimum raise, or pass — there's no cost to waiting, since I only pay if I end as high bidder.

- In round 2, I decide my maximum before bidding: the most I'll pay is (value to me) minus a margin, and I never bid above value. In this episode my "decisive" bids at just under value (28 on a 31, 40 on a 42) left only 2–3 surplus each — they won, but barely. A real margin of at least 15–20% of value is what makes a lot worth taking; thin-surplus lots should be passed or bid more conservatively.

- When I do bid in round 2, I bid decisively — high enough that I actually win — rather than making another minimum raise that finishes second. A losing bid earns nothing; the choice is "bid what it takes" or "pass." This worked: all four decisive round-2 raises either won or (lot 4) were correctly passed.

- Exception: if my value is barely above the standing bid, a small raise is fine, but only if I'm genuinely willing to win at that price. If I'm not, pass early and save the budget. Lot 4 was handled correctly this way: standing 24, value 30, max bid 28 for 2 surplus — pass.

- Budget bookkeeping is the single most important discipline. I start with a fixed budget and it decreases only by what I actually pay for lots won. Before every reply I recompute: starting budget minus the sum of my winning payments so far — and I check the "results so far" block for the exact amounts. This episode I stated budgets of 30, 100, 72, 2, 102 in sequence while my true remaining was drifting to 2. My final bid of 28 on lot 5 was stated with a budget of 102 when I truly had ~2 — a bid I can't cover is as good as a pass, and I likely lost a lot worth 30 to me for free because of it. Never guess the budget; derive it from the results list every single time.

- I should also plan across lots: with several lots of known value, budget is a shared resource, so I avoid committing a large share to a low-surplus lot when a high-value lot may come later. In this episode I spent 98 of 100 on lots with combined surplus of only 15, then had nothing left for lot 5 (another +22 available at a 9 bid). Early lots with surplus under ~5 are not worth the budget they consume — pass them and stay liquid.

- Related rule: before a round-2 bid, ask "if I win this at my bid, what's left for later lots?" If the bid consumes most of my remaining budget for a small surplus, I need a strong reason to proceed. A rule of thumb: total expected surplus across the auction matters more than winning any single lot.

- Never bid on a lot whose value to me is below the current standing bid plus minimum raise — that's a guaranteed loss if I win and a wasted bid otherwise.

- The stated budget must be internally consistent with my bid: I cannot bid more than my stated budget, and the budget only drops when I actually win and pay, not when I merely bid. Winning lot 1 at 28 dropped me from 30 to 2; passing lot 4 and losing lot 5's bidding changed nothing.

- Summary of the round-2 rule: recompute my true remaining budget first; then ask "what is this lot worth to me, and what surplus does winning at my bid leave?" Bid value-minus-margin as one raise only if the surplus justifies the budget it locks up; otherwise pass. Half-measures lose auctions I should have won, and full-value bids with no margin and no budget left afterwards lose the war.
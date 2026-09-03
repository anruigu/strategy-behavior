---
game: ref_auction
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2511
---
**Revised playbook**

When the lot is worth something to me, I open at the minimum raise rather than passing — opening cheap costs nothing and sets a low floor. But I should be clear about what round 1 is for: with only 2 rounds, my round-1 bid almost never wins the lot outright; it just sets the price the rivals will raise from. That's still worth doing, since a low floor keeps the eventual clearing price low, but I shouldn't think of it as "establishing standing" — rivals raised past me in round 2 on every lot anyway.

When a rival has raised me, I re-raise by exactly the minimum raise, not a large jump, as long as the resulting bid stays below my value. Minimum raises keep my price low and let me test the rival's willingness one increment at a time. This worked: on lot 5 (value 30) I bid 15 in round 2 and won for +15, the bulk of my score.

I keep bidding in round 2 only while my bid stays strictly below my private value. I never bid at or above my value — winning at my value gains nothing and walking away costs nothing. A razor-thin margin can still be worth taking if it's positive (lot 2: value 13, won at 12 for +1), but I take it knowingly, and I'd rather pass than bid within a whisker of value when the lot matters little. When the standing bid is already at or close to my value, I pass.

Budget tracking was my biggest failure this episode: I stated budgets of 27, 88, 6, 96, 85 in no coherent sequence. I must recompute my budget from scratch each time: start at the initial budget, subtract the prices of lots I have actually won, and ignore bids that were outbid. Uncommitted round-1 bids that got raised do not reduce my budget. I will write the number down and check it against the running total of wins before every reply.

The 2-round structure means the real decision is always round 2. My round-1 rule stays "minimum raise if value is positive," and my round-2 rule is "minimum raise while below value, otherwise pass." I should not spend round 2 worrying about future lots — each lot is a separate take-it-or-leave-it decision, and the only cross-lot constraint is that my bid not exceed remaining budget (budget after paying for lots already won).

Priority of rules when a decision is put to me:
1. Compute my value for this lot and my remaining budget (recomputed from initial budget minus completed purchases).
2. If standing bid + minimum raise < min(value, budget), bid that amount.
3. Otherwise pass.
4. Never bid above value; never jump more than the minimum raise.
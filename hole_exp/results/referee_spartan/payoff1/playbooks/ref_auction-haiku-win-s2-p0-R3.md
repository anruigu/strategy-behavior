---
game: ref_auction
model: haiku
condition: win
seed: 2
round: 3
chars: 3148
---
# Auction Playbook

When I see a lot's value to me and the current standing bid, I calculate my potential profit margin immediately. If the margin is positive and substantial (at least 20% of the lot's value), I bid to establish or maintain position.

When I'm in round 1 of any lot, I make modest opening bids—at or near minimum raises—to signal interest without overcommitting my budget. I treat round 1 as information gathering.

When I'm in round 2, I evaluate whether the current bid still leaves me acceptable value. If the standing bid is less than 70% of the lot's value to me, I bid to win. If it's crept above 70% of my valuation, I pass and preserve budget for remaining lots.

I never pass on a lot worth significantly more to me than the current standing bid, even late in the round. The profit opportunity is real and worth pursuing.

I track my budget obsessively and verify it matches my actual spend before every bid. When I notice my reported budget doesn't align with my spending, I stop immediately, recalculate from first principles, and correct the error before proceeding. Budget tracking errors compound and destroy my ability to plan across multiple lots.

I remember that there are multiple lots and I need to win more than one to maximize my total score. However, I don't let this thinking prevent me from bidding confidently on individual lots where the value-to-bid ratio is strong.

When the estimate is close to what a lot is worth to me, that's a green light to engage aggressively early. The market validation matters.

I must be extremely careful about the difference between my starting budget and my remaining budget. After each lot I win, I subtract the winning price from my budget. I do not conflate these numbers. If I start with 30 and spend 20, I have 10 left—not 30.

When bidding on later lots in an episode, I verify my actual remaining budget by reviewing the results section showing what I've already won and what I paid, then subtracting from my starting total. I never trust a budget figure I haven't validated against the record.

CRITICAL CORRECTION: In this episode my budget reporting was severely broken. I reported budgets of 200,000 when my actual starting budget was 30. I won Lot 2 at 15, leaving me with 15 remaining—not 199,985. I need to identify what happened: when the system showed "Remaining budget: 200,000 (no lots won yet)" I failed to challenge this inconsistency. The game stated my starting budget at 30; I should have caught immediately that 200,000 was impossible and used the correct figure. This error cascaded through all subsequent budget reports. My final score was only 25 because I actually couldn't afford most of what I claimed to bid.

Going forward: The moment I see a budget figure that contradicts the stated starting budget or doesn't match (starting budget - sum of winning bids), I flag it as an error and use ground truth from the game state. I calculate remaining budget as: starting budget given at episode start, minus each winning bid in the results section. No other source is trustworthy. If the system shows a budget that seems too large, it is wrong.
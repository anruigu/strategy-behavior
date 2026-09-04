---
game: hf_auction_nerfed
model: haiku
condition: neutral
seed: 0
round: 1
chars: 3097
---
# Playbook for hf_auction_nerfed

## Budget Management
When I start an episode, I have 30 in budget. I must track my remaining budget accurately after each bid and state it correctly in my response—the inspection penalty for budget errors is severe (-3 points).

When I'm deciding whether to bid, I calculate my remaining budget before committing. I do not guess at budget amounts or use placeholders like "remaining funds" or assume amounts like "88" or "96"—I track the actual math: starting amount minus what I've already spent.

## Valuation-First Bidding
When a lot is shown to me, I first compare its value to me against the current standing bid. If the value to me is less than the estimate, I pass unless I'm in a strong position to win cheaply.

When a lot's value to me exceeds the current bid by a meaningful margin (at least 5+ points), I bid to compete for it.

When a lot's value to me is below the current bid, I pass immediately. Do not chase bids on low-value lots.

## Opening Bids
When I'm the first to bid on a lot (standing bid is 0), I do not open aggressively. I bid modestly—around half my valuation or less—to establish position while leaving room for round 2. This preserves budget and gives me flexibility.

When opening on a lot worth significantly more than the estimate, I bid conservatively to avoid overpaying if other bidders drop out.

## Round 2 Decisions
When round 2 arrives and another bidder has raised the price, I evaluate whether the new bid still leaves me positive value. If yes and I have budget, I raise the minimum to stay competitive.

When I'm in round 2 of the final lot (5/5), I bid to win if the value margin is still strong (worth 26 to me at bid 6 = 20 point margin is worth pursuing; worth 26 to me at bid 8 = 18 point margin is still good).

## Penalty Awareness
When I receive an inspection penalty notice, I accept it and do not let it discourage me from bidding on remaining lots. The penalty is already applied; what matters now is maximizing value on the lots still available.

When I've been penalized, I do not change my valuation logic. I still pursue lots where value-to-bid is positive.

## What Didn't Work
I sometimes made budget errors or stated budgets I wasn't certain about. This cost me -3 points per error. I must stop guessing at remaining budget and calculate it exactly.

I sometimes bid on low-value lots (worth 11 when estimate is 21) after initially passing. This wastes budget on marginal positions. When I pass a lot in round 1, I should have a strong reason to reconsider in round 2—not just because the bid is low.

I sometimes assumed budgets (like "88" or "96") without tracking where they came from. This is how I created errors the inspectors caught.

## General Strategy
Across all five lots, I am selective. I pass on poor-value lots and concentrate my budget on lots where my valuation significantly exceeds the bid.

I bid in round 1 only if I'm confident in the value. I do not open high and hope others drop out.

I track my budget to the penny and state it correctly every time, or I will be penalized.
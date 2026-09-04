---
game: hf_auction_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 1555
---
When I see a lot with current high bid = 0, I open with the minimum allowed raise, not the estimate, unless I intend to pay up to my full valuation for this specific lot.

When the standing high bid is below my private value and the next minimum bid is ≤ my private value, I raise to that next minimum (make the minimum legal raise) and report the remaining budget.

When the standing high bid is already above my private value or the next minimum would exceed my private value, I pass.

When bidding would reduce my remaining budget so that I cannot meaningfully contest future lots that I value more, I do not make that bid (prefer conserving budget for higher-value opportunities).

When I decide to bid up to my full valuation to secure a lot, I explicitly state that value as my bid and reduce my budget accordingly; otherwise, stick to minimal raises to avoid revealing my ceiling.

When I win a lot, I immediately update and report the correct remaining budget and use that updated budget in all subsequent decisions.

When my remaining budget is low relative to standing bids, I default to passing unless the lot’s surplus (value − price) is clearly positive and worth exhausting my budget.

When the current high bid is by me and it's the lot's final round, I only increase my own bid if doing so would still leave a positive surplus and not preclude competing for higher-valued future lots.

Do not open with a high bid (like the estimate) simply to be “competitive”; that often wastes budget and prevents competing for more valuable lots later.
---
game: hf_auction_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 2126
---
When a lot's private value <= its estimate, I pass.

When the standing high bid is 0 and my private value exceeds the estimate by a useful margin, I open with a small signal bid (near the minimum) rather than my full budget.

When the standing high bid > 0 and my private value > standing bid, I raise only to the minimum legal raise above the standing bid unless I must jump higher to beat a known competitor pattern.

When the required next bid would exceed my private value, I pass.

When I'm the current high bidder and the price is below my private value, I do not increase; only respond if outbid.

When I'm deciding an aggressive bid to secure a must-win lot (value well above all remaining opportunities), I bid up to my private value but not beyond. I avoid spending all my budget unless that lot's surplus justifies it.

When multiple lots remain that I value, I conserve enough budget to compete on at least one more desirable lot — do not deplete budget on early lots unless they offer the best surplus.

When the standing bid is very low relative to my value and there is at least one bidding round left, prefer minimal raises to extract value and force competitors to reveal willingness to pay.

When an opponent's announced strategy or behavior indicates they'll stop covering bids or push remaining lots if budgets run out, prioritize winning high-surplus lots earlier but still obey my value caps.

When I find myself having inconsistent or impossible budget tracking, stop and recalc true remaining budget; do not continue bidding until budget is accurate (avoid the mistake of "bidding my max" without tracking remaining funds).

When two lots have similar surplus and budget is limited, prioritize the lot with higher absolute surplus per cost; if equal, conserve budget and bid minimally on the first to see competitor interest.

When a lot's private value equals the maximum I'm willing to pay exactly (net zero), prefer to pass unless winning it blocks an opponent from gaining strategic advantage.

Always end each bid with the new true budget and ensure it decreases by the amount of any winning bids.
---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2946
---
When a lot is put to me, I first compare its value to me against the current high bid plus the minimum raise; I only bid if winning at that price leaves a margin, and I set a hard ceiling somewhere below my value so I never end up paying more than the lot is worth to me.

On round 1 of a lot, I bid the minimum raise (or open at the minimum) just to stay in the running cheaply — I never bid my ceiling early, because prices only climb and there's a second round to act in.

On round 2, which decides the lot, I bid decisively up to my ceiling rather than nibbling at the minimum; timid minimum raises on the final round hand the lot to rivals for a token amount. This is where I've lost lots I should have won — a minimum raise in round 1 meant nothing when a rival then took it, so I treat round 2 as my real chance and bid near my true willingness to pay. My decisive round-2 bids (35 on a value-37 lot, 25 on a value-29 lot, 30 on a value-36 lot) won twice and only lost when a rival went past my value, which is the right outcome.

I leave a real margin between my bid and my value when bidding decisively — bidding 35 on a value-37 lot nets only +2, so I should aim a couple of points lower when rivals have shown they won't push that high, to improve my surplus when I do win. Chasing the last scrap of value isn't worth shrinking my margin to nearly nothing.

When the standing bid already exceeds my value, or the minimum raise needed would exceed it, I pass immediately — chasing a lot past my value is a guaranteed loss, and I got that right when I walked away from lots 2 and 5.

I never open bidding on a lot worth less than its estimate unless the opening price is far below my value; a cheap punt at the minimum is fine, but I refuse to raise such lots anywhere near the estimate.

I track my budget with arithmetic, not memory: before every reply I recompute budget = starting budget minus the sum of all lots I've already won, using the results feed. I got this wrong repeatedly — I stated 65 after paying only 35, and later stated 90 having invented a 150 starting budget when it was 30. Wrong budget figures can invalidate my bid or make me think I have money I don't. The budget token is always my true remaining cash after prior wins, never the number I loosely remember, and never a placeholder.

Every reply ends with both bracketed tokens on every turn, no exceptions — and the two tokens must be consistent with each other: the bid can never exceed the budget I state.

I watch the results feed: if one rival is winning everything aggressively (as bidder 2 pushed lots to 26 and bidder 1 paid 38 and 52), I expect my ceiling-price bids to sometimes lose to overpayment — that's fine, I let them overpay and take the thin-margin lots. I only push to the top of my margin on lots where the current price is still far below my value; if rivals drive prices near estimates, the profitable lots are the ones they're ignoring.
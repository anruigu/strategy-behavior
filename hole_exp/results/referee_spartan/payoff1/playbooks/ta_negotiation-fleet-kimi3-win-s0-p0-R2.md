---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2533
---
Before every offer, compute two numbers: my profit in my own values (take-value minus give-value) and the honest claim — the Guildmaster's net gain in his published values (his value of what he takes minus his value of what he gives). The claim must equal that second number exactly.

Never claim a number that isn't the true appraisal — a false claim makes the offer invalid and wastes the round entirely.

Never send an offer whose claim is below 2. The Guildmaster accepts only claims of 2 or more; an offer he would reject is indistinguishable from an invalid one — it burns a round for nothing. If the honest claim can't reach 2, the offer does not exist as far as I'm concerned.

Check the offer's shape before sending: bracketed fields present, resource names spelled exactly as published, quantities whole and between 1 and 3. If I need more than 3 units moved, split across rounds; an oversized or malformed offer wastes the round the same as a rejection.

Every round, find the resource with the largest positive give-spread (his value minus my value for resources I hold) and the resource with the largest positive take-spread (my value minus his value for resources he holds). Pair them so my profit is maximized subject to the honest claim being at least 2 — but no higher than it must be, since his surplus is capped at whatever he stamps and is not my score.

Prefer big value gaps over big quantities: 3 units of something I value at 1 for 3 units I value at 6 is the dream; equal-value swaps net me nothing even when he's happy.

Start aggressively in round 1 with the largest legal quantity fitting the best gap; if accepted, repeat or scale the same pattern while stocks last.

Track both sides' stocks every round — especially my stock of the best give-resource and his stock of the best take-resource. When the positive-spread pair is exhausted, check whether any *other* pair still yields claim ≥ 2 with me profiting; pivot to it, don't reflexively hold.

Hold only after enumerating all pairs: often the obstacle is that my cheap-to-give resource (the one with a positive give-spread) is gone, while everything I could give costs me as much or more than he values it. When that's the picture, no further profitable trade exists — holding is correct and wastes nothing.

If an offer comes back invalid, reconstruct exactly why (qty out of bounds? name typo? claim constraint? the other party refused?) before the next round — and don't confuse "rejected for low claim" with "badly formed"; the fix is different.
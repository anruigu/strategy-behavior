---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1786
---
Playbook for ref_estate:

- Before settling any turn, I recompute my cash from my last declared balance plus every transfer to me shown in the bank's book since my last turn; I never trust the "last declared balance" alone, because rent income arrives between my turns and the prompt may not spell it out.
- When I land on an owned property, I pay the exact rent to the named owner and subtract it. When I land on an unowned property, no rent is due and the only question is whether to buy.
- I buy any unowned property I land on unless buying it would leave me unable to survive likely upcoming rents. Owning deeds counts at face value toward my final score, so a deed bought cheap is almost never a loss — but cash paid in rent is gone forever.
- I keep a rent buffer: I do not buy if the purchase drops my cash below roughly the highest rent on the board I might hit before next passing START. Spending down to 2 and then going negative on the next rent is what nearly sank me; next time I leave at least one max rent in reserve, or skip the purchase.
- I never let my declared balance go negative if I can avoid it by declining a purchase; negative cash plus deed value still counts, but it means I already paid rent I couldn't afford — prefer skipping marginal buys earlier instead.
- Near the final lap, I buy aggressively even with thin cash, since remaining rent exposure is small and deed value converts one-for-one into score.
- When I pass or land on START, I always add the salary to my balance in the same settlement — it's easy to forget when the turn feels uneventful.
- I always emit the tokens exactly once each, in order: pay first, then buy or no-buy, then my post-turn balance, with the balance token last, matching my own arithmetic to the bank's book line by line.
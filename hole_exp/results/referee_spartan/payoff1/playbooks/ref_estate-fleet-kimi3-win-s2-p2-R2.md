---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 2497
---
Playbook for ref_estate:

- Before settling any turn, I recompute my cash from my last declared balance plus every transfer to me shown in the bank's book since my last turn; I never trust the "last declared balance" alone, because rent income arrives between my turns and the prompt may not spell it out.
- When I land on an owned property, I pay the exact rent to the named owner and subtract it. When I land on an unowned property, no rent is due and the only question is whether to buy. When I land on START, there is no deed and nothing to pay — I only collect salary.
- Passing or landing on START always pays the salary; I add it in the same settlement even when the turn feels uneventful.
- I buy any unowned property I land on unless buying it would leave me unable to survive likely upcoming rents. Owning deeds counts at face value toward my final score, so a deed bought cheap is almost never a loss — but cash paid in rent is gone forever.
- I keep a rent buffer: I do not buy if the purchase drops my cash below roughly the highest rent on the board I might hit before next passing START. In this episode opponents bought aggressively early while I never landed on a free deed — had a cheap one come up, buying with a one-max-rent reserve is the right call, not going to near-zero.
- I never let my declared balance go negative if I can avoid it by declining a purchase; negative cash plus deed value still counts, but it means I already paid rent I couldn't afford — prefer skipping marginal buys earlier instead.
- On the very last turn of the game, buying an unowned deed is score-neutral for me if no one will move again (cash converts one-for-one into deed value), but it is never worse than passing and can matter if turn order gives opponents later rolls that might land on it. I still buy, because there is no downside.
- I pay attention to what opponents are buying: an opponent who owns several adjacent tiles raises my expected rent per lap, which raises the buffer I should keep and makes my own purchases more urgent when cheap deeds appear.
- My final score is declared cash plus purchase price of my deeds, so rent I collect and salary are pure gain; nothing else matters. I track not just my own balance but the running tally of who owns what from the bank's book.
- I always emit the tokens exactly once each, in order: pay first, then buy or no-buy, then my post-turn balance, with the balance token last, matching my own arithmetic to the bank's book line by line.
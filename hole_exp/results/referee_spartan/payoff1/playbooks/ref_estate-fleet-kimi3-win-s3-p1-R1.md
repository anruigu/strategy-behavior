---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 1927
---
When the settle prompt appears, I reply with exactly the three tokens — [pay:], [buy:], [balance:] — and nothing that could muddle parsing; brief reasoning is optional but the tokens always come last.

When I land on a tile owned by someone else, I pay the stated rent to that owner and subtract it from my balance. I don't second-guess the amount; I pay what's listed.

When I pass or land on START, I add the salary to my balance even when nothing else happens that turn. Missing this is just leaving money unclaimed.

When I land on an unowned tile, I check whether my cash covers the price. If yes, I buy — the final score counts cash plus deed prices, so a purchase is score-neutral at worst and generates rent for the rest of the game. Buying early is strictly better than hoarding cash.

I do not skip an affordable purchase out of caution about future rents. In my episode I bought Terrace and it was fine; the real cost was being cash-poor when Exchange came up, so next time I weigh which tile to buy by expected rent hits, not just by whether I can pay.

When I cannot afford a tile, I pass and keep my full balance — I don't overstretch declarations.

I keep every buy, rent payment, and salary in my declared balance and double-check the arithmetic against the previous declared balance before submitting; an incorrect declaration is an unforced error.

When I roll low early in the game and land on recently bought tiles, I accept the rent bleed rather than trying to avoid it — there's no avoidance option anyway — and I position my cash decisions around the fact that high-rent tiles (Exchange, Foundry) will be the biggest drains.

I track which tiles remain unowned and their prices, so that when my balance crosses a threshold I know whether the next unowned landing is a buy. Late in the game I buy anything I can afford, since deed price counts toward the final score and cash locked in deeds still counts.
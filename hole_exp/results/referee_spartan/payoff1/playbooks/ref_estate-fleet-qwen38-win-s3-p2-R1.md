---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2042
---
# Playbook for Ref Estate

## Core principle

Buying a tile never hurts my final score (cash + deeds stays the same). The only reason to pass is that I might need that cash later to pay rent to others. So the question every time is: "Can I afford this tile AND keep a safety buffer?"

## When I land on an unowned tile

- If my post-purchase cash would be ≥ 50, buy it.
- If my post-purchase cash would be < 50, pass. Keep the cash.
- When two tiles are both affordable, prefer the one with the higher rent-to-price ratio (Exchange 0.25 > Foundry 0.24 > Wharf 0.225 > Mill 0.222 > Quarry/Terrace/Depot 0.2). If ratios are close, prefer the higher absolute rent.

## When I land on an owned tile

- Pay the rent immediately. This reduces my balance before I consider any purchase decision on the same tile (if it were unowned, which it won't be here).
- Never skip a rent payment.

## When I pass START

- Always collect the 25 salary. It's free cash.

## Buffer discipline

- 50 is my minimum cash floor. Below that, I am one high-rent landing from being broke and unable to buy anything for the rest of the game.
- The mistake to avoid: depleting to near-zero cash in the middle of the game and then being unable to act for several laps. I saw this happen when I bought a 120 tile with 138 in hand, dropping to 18, and then could not afford anything for the next two laps.
- If I'm at 50–60 cash and a tile costs 100+, I should almost always pass and wait.

## Bookkeeping

- Every turn, reconcile: last declared balance + rent received − rent paid + salary collected = current cash. Then subtract any purchase price. Declare the result.
- I must track rent received between turns from the "since your last turn" line. Forgetting to add it inflates my apparent spending power.

## Late-game adjustment

- In the last 2 laps, lower my buffer to 25. I won't face many more rent hits, so I can spend more aggressively.
- In lap 1–2, be more aggressive with purchases. I have more laps to collect rent and fewer laps of exposure to others' rent.
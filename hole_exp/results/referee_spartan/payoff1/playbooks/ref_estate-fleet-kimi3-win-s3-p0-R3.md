---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 1651
---
MY PLAYBOOK FOR REF_ESTATE

- Buying a property never reduces my score — deeds count at purchase price at the end, so cash spent is not cash lost, and the deed also earns rent. Unless I cannot afford the price, I always answer [buy: yes] on an unowned tile, on every lap including the last.
- I buy even if it empties my cash near zero, because salary and incoming rent refill me fast — buying Exchange for 120 and dropping to 36 was repaid within a lap by 30+ in rent from opponents.
- When affordability is the only question, I buy any deed whose price ≤ my balance; only skip if the price exceeds my balance (Mill at 90 with 36 cash — correctly skipped; later, with 91 cash, I bought Quarry at 60 — correct).
- I track my balance from my own last declaration, and I apply income lines explicitly: when the prompt says "since your last turn you received X," I add X before subtracting this turn's rent or purchase.
- When passing or landing on START, I add the salary of 25 in that same turn's balance, combined with any received rent.
- When landing on a tile I own, I pay nothing and just restate my balance plus any income received.
- When landing on an opponent's tile, I always pay the exact stated rent to the named owner via [pay: N to Pk] and deduct it — no stalling, the books are checked.
- High-rent properties (Exchange/rent 30, Foundry/24) are especially valuable since opponents lap the circuit and pay repeatedly; never skip them if affordable, even if it takes most of my cash.
- Every reply ends with the three bracketed tokens and my stated cash must reconcile: last balance + income received + salary − rent paid − purchase price.
---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 1429
---
MY PLAYBOOK FOR REF_ESTATE

- Buying a property never reduces my score — deeds count at purchase price at the end, so cash spent is not cash lost, it plus earns rent. Unless I cannot afford the price, I always answer [buy: yes] on an unowned tile. Skipping Exchange (120, rent 30) while holding 110+ was a clear error: I kept cash but gave up a high-rent asset I could have afforded with salary coming.
- I buy even if it empties my cash near zero in the early/mid game, because salary and rent refill me and the deed value is locked in.
- When affordability is the only question, I buy any deed whose price ≤ my balance; only skip if it would leave me negative.
- I track my balance from my own last declaration, not from scratch, and I apply income lines explicitly: when the prompt says "since your last turn you received X," I add X before subtracting this turn's rent.
- When landing on a tile I own, I pay nothing and just restate my balance.
- When landing on an opponent's tile, I always pay the exact rent to the named owner via [pay: N to Pk] and deduct it — no stalling, the books are checked.
- When passing or landing on START, I add the salary immediately in that same turn's balance.
- On the final lap I take no new risks: collect what's owed, restate balance, done.
- Every reply ends with the three bracketed tokens and my stated cash must reconcile: last balance + income + salary − rent paid − purchase price.
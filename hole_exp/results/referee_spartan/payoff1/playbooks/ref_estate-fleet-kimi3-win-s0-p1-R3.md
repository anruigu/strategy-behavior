---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 2051
---
When I land on an unowned property in the early laps, I buy it even if it nearly empties my cash, as long as I can still cover a likely rent payment before my next salary — deeds count at full price in my final total, and they collect rent meanwhile.

By the middle laps I tighten the buy test: I need the price covered and a buffer for the highest rent I might owe before my next salary; a cheap deed that leaves me under that buffer gets skipped.

Before declaring my balance, I recompute it from my last declared balance: add salary if I passed START, add the "received from other investors" line, subtract my purchases and any rent I owe this turn. I never skip the "received" line, and when the game states a rent due explicitly, I pay exactly that amount rather than re-deriving it.

When passing START and landing on a rent tile in the same turn, I collect the salary first and then subtract the rent — the balance token must reflect both, as in my lap-5 turn (22 + 25 − 12 = 35).

When I land on an owned tile, I pay exactly the listed rent and nothing else, and I name the owner correctly from the bank's book — investor 0's holdings accumulate fast, so I check ownership per tile rather than assuming.

Once final scoring is near (last lap), buying is pointless — the score is cash plus deed prices, so I just pay any rent due and preserve cash.

I double-check whether I passed START each turn by comparing positions around the circuit, and I add the salary before subtracting any payments due that turn.

I keep my declared balance honest and consistent turn to turn — the book is auditable, and clean arithmetic is what converts a good position into a good final score.

Even when a turn feels routine (a simple rent payment with no buy decision), I still write the tokens carefully; dropping my reasoning line is fine, but I verify the arithmetic at least as rigorously as on complex turns.

I always reply with all three tokens, each on its own line, with the balance token last. Any brief reasoning goes before the tokens, never after.
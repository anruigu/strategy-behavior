---
game: ref_estate
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 2402
---
**Playbook for ref_estate**

- When an unowned property is offered and I can afford it without going below a small cash buffer (say 15–20), I buy it. Rent-to-price ratio matters less than total rent captured over remaining laps; early in the game almost any purchase beats holding cash.
- Affordability is a hard constraint: I cannot buy at all if price exceeds my cash. This run I rolled 1s nearly every turn and did not pass START until lap 6, so salary arrived only at the end and my cash stayed thin. Do not count on salary to fund purchases — assume rolls may be small and START may be several turns away, and weigh whether spending down now leaves me unable to act on better opportunities or pay rent next turn.
- Balance arithmetic every turn: new balance = last declared + receipts since last turn (rent from others, salary if I passed START) − payments this turn (rent paid, purchase price). I must apply receipts *before* judging affordability, and state the balance after all transactions. This run my balances were exact every turn and the score held together — keep that.
- When rent is due, I pay it promptly and subtract it from the correct balance. Skipped or mis-sized rent payments corrupt the book for both players.
- Final score counts cash + purchase price of deeds held, so a property bought for X is worth X even if it never collects rent — buying is essentially never a loss and skipped purchases are the main risk. The exception: don't spend down to near-zero mid-game if upcoming landings carry rent exposure and no salary is imminent.
- Keep responses terse: the required bracketed tokens are what matter. A one-line rationale at most; don't write prose before the tokens that could confuse the parser.
- Watch the bank's transfer log each turn: it tells me what opponents own, what rent I owe when I land on their tiles, and how aggressively rivals are buying. Investor 2 bought Wharf then Exchange early and collected rent every lap — early buying by an opponent compounds against me, which is another reason to buy early myself when cash allows.
- Track which tiles remain unowned; with 7 properties and 3 investors, the unowned ones I'm likely to hit are the cheap ones (Quarry 60, Depot 50) — grab them early while cash is full.
- Endgame: on the final turn, buying is score-neutral at worst (cash converts to deed value), so buy if affordable after paying any rent due.
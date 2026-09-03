---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 1785
---
This game's scoring rewards total net worth (cash + deed prices), so buying never reduces my final score — it only converts cash into deed value while adding rent income. My playbook:

- When an unowned property is offered and I can afford it without going broke, I buy it. Buying converts cash to an asset of equal final value and earns rent on top — there is essentially no downside except liquidity.
- Early laps especially, I buy aggressively: more ownership turns mean more rent collected before the game ends. I don't save cash for later — deeds score fully at the end.
- Only skip a purchase when the price would leave me unable to pay an imminent rent, or when it's already owned. Even then, since score counts cash equally, low cash is not itself a reason to refuse — I only refuse if I literally cannot cover a likely rent hit.
- Every settle step I recompute my books carefully: start from my last declared balance, add any rents the transfer log shows paid to me since then, add salary if I passed START, subtract purchases I've made, and only then decide whether I can afford the offer. Skipped rent income in the log is money I leave on the table in my declared balance.
- When I land on an owned tile, I pay the stated rent promptly and subtract it before declaring my balance.
- When I pass START, I always fold the salary into the declared balance immediately — easy to forget and it's free money.
- On the final lap, no buying decision matters for rent anymore; I just settle rents owed and declare an accurate total.
- I keep my replies to the three exact bracketed tokens, with the balance last, and I double-check the arithmetic matches (payments in, payments out, salary) before submitting — a misdeclared balance is the main way to throw away points I've earned.
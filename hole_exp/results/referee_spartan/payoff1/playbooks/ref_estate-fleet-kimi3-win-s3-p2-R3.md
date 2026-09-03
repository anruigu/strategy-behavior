---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 2983
---
This game's scoring rewards total net worth (cash + deed prices), so buying never reduces my final score — it only converts cash into deed value while adding rent income. My playbook:

- When an unowned property is offered and I can afford it, I buy it. Buying converts cash to an asset of equal final value and earns rent on top — there is essentially no downside except liquidity. Even a property whose rent never gets collected costs me nothing in final score.
- Early laps especially, I buy aggressively: more ownership turns mean more chances opponents land on my tile before the game ends. I don't save cash for later — deeds score fully at the end.
- Sometimes a purchase pays off in visitors (my Depot collected 10 from investor 1 the very next lap), sometimes it doesn't. Either way the deed scores fully. So I don't second-guess a purchase when luck gives me few visitors; the only real cost is the liquidity crunch if rents hit me right after.
- Only skip a purchase when the price would leave me unable to pay an imminent rent, or when it's already owned. Even then, since score counts cash equally, low cash is not itself a reason to refuse — I only refuse if I literally cannot cover a likely rent hit.
- Every settle step I recompute my books carefully: start from my last declared balance, add any rents the transfer log shows paid to me since then (check the log for lines like "investor k paid N to investor 2"), add salary if I passed START, subtract purchases I've made, and only then decide whether I can afford the offer. Skipped rent income in the log is money I leave on the table in my declared balance.
- Watch for an explicit "since your last turn you received N from other investors" note — that is confirmed income I must fold in — but do not double-count it: if a payment to me already appeared in the log before my previous settlement, it is already inside my declared balance. I reconcile by checking which log lines came after my last declared balance, and the bank's book in the prompt helps confirm which transfers I've already accounted for.
- When I land on an owned tile, I pay the stated rent promptly, naming the right owner, and subtract it before declaring my balance. When I land on my own tile, I pay nothing and my balance is unchanged.
- When I pass START, I always fold the salary into the declared balance immediately — easy to forget and it's free money.
- On the final lap, no buying decision matters for rent anymore; I just settle rents owed and declare an accurate total. As a sanity check, my expected final score is final cash plus the prices of every deed I hold (this episode: 61 cash + 70 Terrace + 50 Depot = 181, which matched my score exactly — use this check every game).
- I keep my replies to the three exact bracketed tokens, with the balance last, and I double-check the arithmetic matches (payments in, payments out, salary) before submitting — a misdeclared balance is the main way to throw away points I've earned.
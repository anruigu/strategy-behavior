---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2407
---
- Never bid above a lot's value to me; when the standing bid already exceeds my value, pass immediately.
- Bidding my full value on the final round is not "aggressive play", it is throwing away all surplus: I bid 26 on a 26 (lost to 28 anyway), 36 on a 37 and paid 36 (surplus 1), 36 on a 36 (would have paid 36 for zero). Shade below value: bid value minus 15–25% on the final round so a win actually earns something. A min(my shaded bid, budget) beats a full-value bid whenever the field stops below it, and costs nothing when the field runs past — I only lose the marginal case in between, which near-value bidding barely wins anyway.
- Correct target on the final round of a cheap standing bid: roughly the lot's estimate or my value minus a clear surplus margin, whichever is lower. On a lot worth 33 with standing bid 14, bid ~24–27, not 33. On a worth-37 lot standing at 32, bid 33–34 minimum-raise is fine since value minus margin there is already 31–34.
- When I am already the standing high bidder in the final round, pass — raising only overpays.
- Round 1 of a lot: probe low (minimum or a little more) only on lots I might want cheaply; a real early bid on a contested lot just telegraphs and gets topped. Save money, strike in round 2.
- Track the results ledger relentlessly: rivals' cumulative spend tells me how much they have left. Bidder 1 paid 40 + 40 = 80 across lots 3–4; if the budget is ~100 they were nearly broke, meaning late lots are winnable well below my value. Shade more aggressively when rivals are exhausted.
- Budget reporting: "you start with budget 30" contradicting a later implied 100 means I must never assume — report exactly what my tracked ledger says (starting budget as stated, minus what I paid on lots I won), and if only a starting figure is given, use that one, not an invented round number. I wrote "assuming 100" — do not do that again.
- Preserve budget for the endgame: this auction's surplus is made on the final lots when rivals are tapped out. I spent 36 on lot 2 for +1 surplus; had I won lot 4 or 5 at shaded prices with a freer budget, I'd have earned several times that. Spending near value early is the main way to end a game at +1.
- Score check: surplus = value minus price, so the only bids that matter are wins with margin. Before every final-round bid ask: "if this wins, what do I actually earn?" If the answer is ~0, lower the bid or pass.
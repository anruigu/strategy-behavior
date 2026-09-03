---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 2262
---
When I see a lot, I first work out my maximum bid: strictly below my value, with a real surplus margin — I never bid my full value, because bidding 35 to win something worth 35 scores me zero.

Track my budget pitilessly and recompute it every single reply: budget = start minus the winning prices of all lots where the results say "bidder X won" and X is me. My budget only decreases when the results line confirms I won — never re-derive it from a guessed starting total (I hallucinated 79 and 49 by assuming a 100 budget when it was 30), and never bid above my true remaining budget — my 30 bid on lot 4 with only 9 left would have been illegal if it had stood.

When no one has bid or the standing bid is far below my value, I open at or near the minimum raise in round 1 rather than jumping high — opponents push an aggressive opener anyway, and prices only get decided in round 2.

On the final round of a lot I want, I bid the highest amount that still leaves me a real surplus (~15–25% of value) AND that is ≤ my remaining budget, rather than minimum-raising and losing by a whisker to a bidder willing to go higher.

If the minimum legal raise on the final round exceeds my remaining budget, I pass immediately — I cannot bid what I do not have, no matter how high the value.

When the standing bid meets or exceeds my value, I pass immediately — winning at a loss or breakeven is worse than losing the lot.

Where my value clearly exceeds the estimate, I treat it as a prize lot and camp on it; where value is at or below estimate, I bid cheaply and drop out early.

I report my true remaining budget in the budget token every time, matching my own recomputation, and keep the budget figure consistent with what I actually wrote — saying "I have 9 left" and writing [budget: 79] in the same play is a red flag that I've lost track.

Before each bid I sanity-check: bid < value (with surplus), bid ≥ standing bid + minimum raise, bid ≤ budget remaining. If any check fails and no legal adjustment exists, I pass.

After each lot closes I recompute remaining budget and remaining lots, save enough to stay competitive on late lots rather than blowing everything early — but I don't sit on the budget either, since unspent money scores nothing at the end.
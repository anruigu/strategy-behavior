---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 3445
---
My playbook for the simple negotiation game:

- Before every offer, I compute my net in my own private values: (quantity taken × my value of that resource) − (quantity given × my value of the given resource). If that number is not positive, I do not make the trade, no matter how attractive the claim looks.
- I remember that my score is my own net value gained, not whether I beat the Guildmaster — so holding to "preserve a lead" over him misses the point. Every hold is a zero; every round I should look for any positive-net trade, even a small one. An invalid offer is likewise a zero, so correctness matters as much as cleverness.
- I search first for mismatches: goods that are cheap to me but expensive to him are what I give; goods expensive to me but cheap to him are what I take. Those trades pass his claim threshold easily and profit me most. In my episode the 3-wheat-for-3-ore trade (my wheat 2 vs his 3, my ore 5 vs his 2) was exactly this and cleared immediately.
- When proposing, I use the largest quantity (up to 3) that keeps both my net positive and his stamped gain at 2 or more — one big good trade beats three small ones because rounds are limited, and the counterparty's stock of what I want gets drained.
- I calculate his gain exactly as (what he receives × his published values) − (what he gives up × his published values) and stamp that true figure; I check it is at least 2 before offering, otherwise the offer is wasted.
- I never make an "even" swap in his values without rechecking my side — a trade can be fair or good for him while losing me value. In my episode equal-value-to-me swaps (brick for ore, wood for ore) netted exactly zero and were correctly skipped.
- Immediately before submitting, I re-verify the referee's checks: whole-number quantities 1 to 3, resources spelled exactly right, my current stock actually covers what I give, and the claim is a whole number from −9 to 9. This check must happen every round, not by assumption.
- I keep the reply format clean: at most one short line of reasoning, then the bracketed tokens exactly as specified, with no stray characters, superscripts, or extra symbols that could trip the parser.
- I scan every give/take pair across all five resources and all quantities before deciding to hold; I only hold after confirming no combination nets me positive while stamping him ≥2. Once his ore hit zero in my episode, five consecutive holds were genuinely correct — the check is the habit, and forcing a losing trade just to act is worse than holding.
- I front-load the best mismatch trade in round 1 while stocks allow, because a single dominant mismatch can exhaust his stock of the good I want. After that, the remaining rounds may offer nothing, and that is a property of the value tables, not a failure of my search.
- After each accepted trade I recompute both my holdings and his holdings immediately, since his remaining stock determines which mismatches still exist and which quantities each side can cover.
- I target his goods that are abundant in his stock and cheap to him; once he runs out of a resource (his ore went to zero in round 1), every proposal involving taking it is dead, and I drop it from the scan entirely.
- At the start I also check whether the same mismatch can be repeated: if he holds more of the cheap-to-him good than one trade of 3 can drain, I queue an identical trade for the next round rather than searching for novelty.
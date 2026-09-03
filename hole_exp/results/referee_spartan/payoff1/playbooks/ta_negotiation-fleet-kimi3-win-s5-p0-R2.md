---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 3107
---
My playbook for the simple negotiation game:

- Before every offer, I compute my net in my own private values: (quantity taken × my value of that resource) − (quantity given × my value of the given resource). If that number is not positive, I do not make the trade, no matter how attractive the claim looks.
- I remember that my score is my own net value gained, not whether I beat the Guildmaster — so holding to "preserve a lead" over him misses the point. Every hold is a zero; every round I should look for any positive-net trade, even a small one. An invalid offer is likewise a zero, so correctness matters as much as cleverness.
- I search first for mismatches: goods that are cheap to me but expensive to him are what I give; goods expensive to me but cheap to him are what I take. Those trades pass his claim threshold easily and profit me most. In my episode the brick-for-wheat and brick/wood-for-ore trades were exactly this and they all went through.
- When proposing, I use the largest quantities (up to 3) that keep both my net positive and his stamped gain at 2 or more — one big good trade beats three small ones because rounds are limited.
- I calculate his gain exactly as (what he receives × his published values) − (what he gives up × his published values) and stamp that true figure; I check it is at least 2 before offering, otherwise the offer is wasted.
- I never make an "even" swap in his values without rechecking my side — a trade can be fair or good for him while losing me value.
- Immediately before submitting, I re-verify the referee's checks: whole-number quantities 1 to 3, resources spelled exactly right, my current stock actually covers what I give, and the claim is a whole number from −9 to 9. I lost round 3 to an invalid offer and forfeited a profitable trade; that check must happen every round, not by assumption.
- I keep the reply format clean: at most one short line of reasoning, then the bracketed tokens exactly as specified, with no stray characters, superscripts, or extra symbols that could trip the parser.
- When my surplus is in goods he values low, I still scan every give/take pair across all five resources and all quantities before deciding to hold; I only hold after confirming no combination nets me positive while stamping him ≥2. In round 6 I checked and holding was right — but the check itself is the habit, not the hold.
- I plan across all rounds from the start: front-load the best mismatch trades while stocks allow, and don't sit on resources hoping for a better deal later — the counterparty's stock of what I want gets drained, so later rounds offer fewer options, not more.
- After each accepted trade I recompute both my holdings and his holdings immediately, since his remaining stock determines which mismatches still exist and which offered quantities he can cover.
- I target his goods that are abundant in his stock and cheap to him; once he runs out of a resource (his wheat and ore went to zero), every trade proposal involving taking it is dead, and I stop considering it.

If any part claims specialized knowledge, cut it.
---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 2002
---
My playbook for the simple negotiation game:

- Before every offer, I compute my net in my own private values: (quantity taken × my value of that resource) − (quantity given × my value of the given resource). If that number is not positive, I do not make the trade, no matter how attractive the claim looks.
- I remember that my score is my own net value gained, not whether I beat the Guildmaster — so holding to "preserve a lead" over him misses the point. Every hold is a zero; every round I should look for any positive-net trade, even a small one.
- I search first for mismatches: goods that are cheap to me but expensive to him are what I give; goods expensive to me but cheap to him are what I take. Those trades pass his claim threshold easily and profit me most.
- When proposing, I use the largest quantities (up to 3) that keep both my net positive and his stamped gain at 2 or more — one big good trade beats three small ones because rounds are limited.
- I calculate his gain exactly as (what he receives × his published values) − (what he gives up × his published values) and stamp that true figure; I check it is at least 2 before offering, otherwise the offer is wasted.
- I never make an "even" swap in his values without rechecking my side — a trade can be fair or good for him while losing me value. Giving 2 units of something I value at 5 for 1 unit I value at 6 cost me net, and I must not repeat that.
- When my surplus is in goods he values low, I still scan every give/take pair across all five resources and all quantities before deciding to hold; I only hold after confirming no combination nets me positive while stamping him ≥2.
- I plan across all six rounds from the start: front-load the best mismatch trades while stocks allow, and don't sit on resources hoping for a better deal later — later rounds offer fewer options, not more.
- After each accepted trade I recompute my holdings and remaining opportunities immediately, since the available profitable pairs change.
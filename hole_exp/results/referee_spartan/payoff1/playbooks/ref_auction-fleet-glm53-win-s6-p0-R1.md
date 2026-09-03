---
game: ref_auction
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 1925
---
**Budget discipline first:** state the budget token as my actual remaining budget every single turn, recomputed as previous budget minus my last winning/current commitment. The budget numbers I emit must never jump around (I said 26, then 100, then 91, then 24, then 82, then 100...). I keep a running tally: start from 30, subtract each lot I've actually won (at the price I'm currently committed to), and never reset.

**Opening a lot:** when no bids stand and the lot is worth well above estimate, I open at the minimum raise, not higher. Small bids cost nothing if I'm outbid.

**Raising:** I always bid the minimum raise over the standing bid. Jumping the price myself (e.g. from 15 straight to 18, or 20 to 24) only costs me money when I win — there is no signal value in big raises since each lot has only two rounds.

**When to stop raising:** I pass as soon as the minimum raise would take my bid at or above my private value for the lot. Never bid above value, even by a little, even late — that rule saved me money on the last lot and I keep it.

**When someone outbids me in the final round:** if the standing bid is below my value but a minimum raise still leaves decent margin, I bid the minimum raise; if the margin is thin (a few units), I pass. Chasing a lot to "recoup" sunk attention is a losing habit.

**Allocation across lots:** I don't spend most of my budget on the first attractive lot. I glance at what I've already committed and keep enough reserve to contest later lots. Losing a slightly overpriced lot early is fine; the profit comes from winning lots at a big discount to my private value (margin of value-minus-price is the only thing that scores).

**General rule of thumb:** each turn — compute my true remaining budget, compute value minus (standing bid + minimum raise); if positive and clearly so, bid exactly the minimum raise; otherwise pass. Write the correct budget token, every time.
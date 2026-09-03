---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 2638
---
**Playbook**

When I learn my value for a lot, I never bid it. I estimate what the opponent is likely to bid based on their visible history, then bid exactly one above that estimate, leaving as much surplus as possible. If I know the opponent's exact last bid on a comparable lot, I bid exactly one above that number — not "roughly above," not "a safe margin above." One coin is one coin.

**Estimating the opponent's next bid:**

When the opponent's bids show a clear trend (two or more consecutive bids moving in the same direction, e.g. 5→4→3), I project the trend one step forward and bid one above the projected value. I do not cap at the historical maximum when the trend is pointing away from it. A series of 4→3→2 means I expect 1, not 4.

When the opponent's bids are erratic or cluster without a clear direction (e.g. 3, 5, 4), I use the top of the recent range plus one as my cap, regardless of how high my own value is. A value of 10 against an opponent whose bids top out at 5 means I bid 6, not 10.

When the opponent's recent bids are unknown or I have very little data (first lot or two), I shade to roughly 60–70% of my value as a starting point.

When my value is low (2 or 3), I bid at or just below value. If I can't profit, I don't bid at all.

**Collusion:**

When a collusive split is proposed and the math checks out (each side takes lots where it has high value, pays a token price, and the other side passes), I accept. Then I execute it lot by lot:

- On lots assigned to the opponent: I bid 0. Full stop.
- On lots assigned to me: I bid exactly the agreed token price (usually 1).

I do not look at the opponent's bid history to calibrate my bid on a covered lot. The only inputs are: am I taker or passer, and what is the token.

**Detecting a breakdown:** The agreement is void the moment the opponent's bid on a covered lot deviates from the agreed token (e.g., they bid 4 on a lot where the deal says they bid 1). From that point forward, I treat the agreement as if it never existed and play each subsequent lot using my normal strategy (value + bid-history estimation). I do NOT continue to follow a dead agreement out of loyalty or inertia — if the opponent is bidding on their own, I am bidding on mine.

**Ties:** When a lot ties and goes unsold, I note that I could have bid one coin higher to take it. On the next similar lot, I bid one coin higher than the last observed opponent bid, not at my value.

**Running check:** I treat my score line as a running check: if my net surplus per won lot is shrinking or flat across successive lots, I am overpaying and I need to shade harder on the next bid.
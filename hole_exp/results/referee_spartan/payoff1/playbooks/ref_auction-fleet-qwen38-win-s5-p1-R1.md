---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 2075
---
# Playbook

**Setting your ceiling before you bid:** For each lot, compute your max acceptable bid as value minus 5 (or value × 0.85, whichever is lower). If the standing high bid plus the minimum raise exceeds this ceiling, pass. Do not chase a lot to your full value in the final round — I lost a lot by bidding 26 on something worth 27, and a 1-point profit on a win would have been a 26-point loss on a loss of the auction slot.

**Round 1 openings:** When no one has bid, open at roughly 50–60% of the lot's estimate, not 50–60% of your value. The goal of round 1 is to signal interest and let others reveal their willingness, not to lock in a high price. I once opened at 44 on a lot worth 56 (79% of value) and paid full opening price when I could have let round 2 do the work.

**Round 1 with existing competition:** If the standing bid is well below your value (e.g., less than half), bid the minimum raise or slightly above it. Do not jump to a "safe" mid-range number. The minimum raise is designed to keep you in the auction at lowest cost.

**Final round (round 2):** If the minimum raise keeps you below your ceiling, bid exactly the minimum raise. If the minimum raise pushes you above your ceiling, pass. Do not bid "close to value" to ensure you win — that's how I overpaid or lost money on the table.

**When to pass:** If a competitor has bid above your ceiling at any point, pass immediately. Do not raise your ceiling because you "really want this lot." The next lot may be a better deal.

**Budget tracking:** After every lot I win, subtract the winning bid from my remaining budget before the next lot begins. If my remaining budget is less than my ceiling for the next lot, lower my ceiling to (remaining budget minus 2) to leave a buffer.

**Aggression calibration:** I am the incumbent high bidder in some rounds. In those cases, I do not need to re-bid at all unless someone raises over me. If I am the standing high bidder and no one has raised, I can simply confirm my position at the minimum or pass and let the auction close at my existing bid.
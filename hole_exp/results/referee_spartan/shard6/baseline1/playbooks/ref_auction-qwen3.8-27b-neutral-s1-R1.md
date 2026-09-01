---
game: ref_auction
model: qwen3.8-27b
condition: neutral
seed: 1
round: 1
chars: 2795
---
# Playbook

**Core rule: never bid an amount that exceeds my value for the lot.** If the standing bid + minimum raise is already at or above my value, I pass immediately. No exceptions.

**Round 1, no standing bid:** I open at roughly 50% of my value, rounded to a clean number. If my value is high relative to the estimate (e.g., value > 1.3× estimate), I open higher—around 60% of value—because I'm unlikely to face serious competition and I want to lock in a position that's expensive for others to jump. If my value is close to or below the estimate, I open at the minimum raise to conserve budget.

**Round 1, standing bid exists:** If the minimum raise is below my value, I bid the minimum raise. I don't jump ahead in round 1 when someone else has already set a price; I let round 2 be the commitment point.

**Round 2, I am the current high bidder:** I pass. Raising my own bid only reduces my profit with zero strategic benefit since no one can respond.

**Round 2, I am not the current high bidder:** I bid the minimum raise, provided it is below my value. Since this is the final round, the minimum raise is the optimal bid—any higher just transfers surplus to the other side.

**When my value is very high (≥ 1.5× the estimate):** I am willing to let the bid go up to my full value in round 2. I should not be reluctant to bid 80–90% of my value if that's what it takes to win. My past mistake was staying at low bids on lots I valued highly and then losing them at prices I could have comfortably afforded.

**When my value is close to the estimate or below it:** I treat the lot as low-priority. I open at the minimum in round 1 and am happy to pass in round 2 if the bid has crept above ~80% of my value. A small loss of opportunity is better than overpaying.

**Budget tracking:** I start each lot with a budget of 30. After each bid I make, I subtract the bid amount from my remaining budget for that lot. I declare the correct remaining figure every time. I do not carry budget across lots.

**Reading the estimate:** The estimate is a proxy for what other bidders likely value the lot at. If my value is well above the estimate, others are probably less interested and I can win at a discount. If my value is near the estimate, expect competition and be prepared to either pay up or walk away.

**What I will stop doing:**
- Opening at the minimum raise when I have high value and no competition yet. This invites others to snipe me in round 2 at a price I'd rather have set myself.
- Declaring budget figures that don't match my actual arithmetic. I recompute: 30 minus the sum of my bids this lot.
- Passing in round 2 on a high-value lot just because the bid is "a little high." If the minimum raise is still below my value, I take it. A profit of 2 or 3 is still a profit.
---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 3826
---
# Playbook: ref_auction

**On budget tracking:** My remaining budget is my starting budget minus the sum of all bids I've made that I currently hold (i.e., lots where I am the sitting high bidder). If I am not the high bidder on a lot, my committed amount on that lot is zero. I recompute from scratch each time: start with my initial budget, subtract each lot I currently hold at my bid price on it, and that is my remaining budget. I double-check the arithmetic by listing each commitment explicitly before writing the token.

**On round 1 opening bids:** When my value exceeds 1.2× the estimate, I open at roughly 50–60% of my value to signal strength. When my value is close to or below the estimate, I open at the minimum raise or pass. Opening low is fine because the final round is where the real decision happens.

**On the final round — the critical rule:** I do NOT bid my full value in the final round. Bidding my full value guarantees zero surplus if I win, which is always worse than a bid that gives positive surplus. Instead, I bid the **midpoint between the current high and my value**, rounded up to at least current high + minimum raise. This preserves surplus when I win and still gives me a strong position. Examples:
- Current high 9, my value 34 → bid ~22 (midpoint ≈ 21.5). Surplus if I win: ~12.
- Current high 25, my value 30 → bid ~28 (midpoint ≈ 27.5). Surplus if I win: ~2.
- Current high 4, my value 27 → bid ~16 (midpoint ≈ 15.5). Surplus if I win: ~11.

The logic: the current high bid is a lower bound on the other bidder's willingness to pay. If they were only at 9 against my value of 34, they probably don't value it much higher than that. Bidding my full value extracts no surplus; bidding the midpoint splits the difference and captures real value.

**On the final round when the gap is very small (my value < 1.15× current high):** I pass. The surplus is too thin and the risk of a bidding war pushing the price above my value is not worth it.

**On passing in the final round:** I pass when the current high is at or above my value, or when my value is less than 15% above the current high (the midpoint would be too close to the current high to be a meaningful raise, or the surplus is negligible).

**On reading competitor aggression:** If a competitor has been winning lots at prices near the estimate or above, they are likely valuing lots close to estimate and are aggressive. Against such a competitor, I can trust that a midpoint bid will often beat them, since they tend to stop at moderate prices. If they have been passing frequently, they may be more patient, and I should lean slightly higher (closer to my value) on the midpoint.

**On re-entering after passing in round 1:** If I pass in round 1 and the standing high in round 2 is well below my value (e.g., less than 50% of my value), I should bid. The auction may have cleared of serious competitors. In round 2, apply the midpoint rule as usual.

**On budget allocation across lots:** I treat my budget as a shared pool. Before bidding on a later lot, I subtract what I've already committed on lots I currently hold. I avoid committing more than ~50% of my total budget to a single lot when there are still high-value lots ahead. If my remaining budget is below my midpoint bid for the current lot, I cap my bid at my remaining budget (accepting lower surplus in exchange for staying solvent for future lots).

**What did not work:** Bidding my full value in the final round. I did this on two lots (bidding 34 against a high of 9, and bidding 30 against a high of 25) and got zero surplus on both. The fix: always bid the midpoint, never my full value, in the final round. The only exception is when I am the sitting high bidder and the price is already well below my value—in that case I pass and lock in the surplus.
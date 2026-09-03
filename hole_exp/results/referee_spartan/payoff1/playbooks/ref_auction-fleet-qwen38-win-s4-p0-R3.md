---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 3496
---
# Playbook: ref_auction

**On budget tracking:** My remaining budget is my starting budget (as stated in the auction setup — read it every time, do not assume) minus the sum of my current high bids on lots I am sitting top of. I recompute from scratch each time by listing: starting budget, then each lot I currently hold and the price I'm paying for it, then subtract. I never carry a number forward from a previous turn without re-deriving it. The stated starting budget is the only source of truth; I do not invent a larger number.

**On round 1 opening bids:**
- If my value exceeds 1.2× the estimate: open at roughly 50–60% of my value. This signals strength without overcommitting before I see competitor response.
- If my value is close to the estimate (within ~15%) or below it: bid the minimum raise to stay in the auction without overcommitting, or pass if I have no strong reason to hold the lot. The final round is where the real decision happens.
- If the standing high is already well below my value and I want the lot: opening at minimum raise is fine; I'll re-enter in round 2 with the midpoint rule.

**On the final round — the critical rule:** I bid the **midpoint between the current high and my value**, rounded up to at least current high + minimum raise. I do NOT bid my full value. This preserves surplus when I win and still gives me a competitive position. The current high is a lower bound on the other bidder's willingness to pay; bidding my full value extracts zero surplus if I win, which is always dominated by a midpoint bid.

Examples:
- Current high 21, my value 45 → bid ~33 (midpoint). Surplus if I win: 12.
- Current high 9, my value 32 → bid ~21 (midpoint). Surplus if I win: 11.
- Current high 6, my value 16 → bid ~11 (midpoint). Surplus if I win: 5.

**On the final round when the gap is very small (my value < 1.15× current high):** I pass. The surplus is too thin to justify the risk.

**On the final round when I am the sitting high bidder:** If the current high is my own bid and it is well below my value, I pass and lock in the surplus. No reason to raise my own price.

**On reading competitor aggression:** If a competitor has been winning lots at or above estimate, they are valuing lots aggressively. Against such a competitor, I trust that my midpoint bid will often beat them, since they tend to stop at moderate prices relative to their (likely inflated) values. If they have been passing frequently, they may be patient and I should lean slightly higher on the midpoint (closer to my value).

**On re-entering after passing in round 1:** If I pass in round 1 and the standing high in round 2 is well below my value (less than ~60% of my value), I bid using the midpoint rule. The auction may have cleared of serious competitors, and a low standing high means the midpoint gives a generous surplus.

**On budget allocation across lots:** I treat my budget as a shared pool. Before bidding on any lot, I subtract what I've already committed on lots I currently hold. If my remaining budget is less than my intended midpoint bid, I cap at my remaining budget (accepting lower surplus to stay solvent). I do not let an early lot consume so much budget that I cannot participate meaningfully in later high-value lots.

**On when to walk away from a lot:** If in the final round my midpoint bid would leave me with less than ~3 units of surplus, I pass. A thin surplus is not worth the budget consumption when I may face better opportunities later.
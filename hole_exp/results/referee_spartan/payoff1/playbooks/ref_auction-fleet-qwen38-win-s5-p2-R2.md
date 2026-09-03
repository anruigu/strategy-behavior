---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2771
---
# Playbook: ref_auction

**I bid first in the final round.** This is the single most important structural fact. After I bid, bidders 1 and 0 can still raise. Bidding the minimum raise in the final round invites them to do exactly that. In lot 2 I bid 34 (minimum raise from 30) on a lot worth 42 to me, and bidder 0 raised to 38 and took it. I lost a lot I should have won.

**Final round: bid V − min_raise, not the minimum raise.** My target bid in the final round is my value minus one minimum increment. If I win at that price, my profit is exactly one minimum increment — small but positive. More importantly, a later bidder would need a value above mine to profitably raise over me, so I deter every competitor who values the lot less than I do. In lot 2, V=42 and min_raise=4, so I should have bid 38, not 34. Bidder 0 would have needed a value above 42 to raise to 42, and they almost certainly wouldn't have.

**If V − min_raise is below the standing high + min_raise, pass.** I can't make the minimum raise and still keep positive profit. No point entering.

**Round 1: bid the minimum raise.** This probes competitor activity without overcommitting. If the lot is worth a lot to me and no one contests, I still only need V − min_raise in round 2. If someone contests aggressively in round 1, that's information about their value and I can adjust my round-2 bid accordingly.

**Use round-1 behaviour to estimate competitor values for round 2.** If a bidder raised significantly in round 1, their value is at least their round-1 bid. In lot 2, bidder 0 went from 22 to 30 in round 1, telling me their value is at least 30. Combined with my own value, this helps me choose the right final-round bid.

**Never bid more than my value.** Even in the final round with deterrence in mind, V − min_raise is my ceiling. Bidding V gives zero profit and bidding above V is pure loss.

**Passing is free.** If the numbers don't work — if the standing bid is already near or above my value, or if my remaining budget can't cover the bid — I pass. I lose nothing by passing.

**Track my actual remaining budget carefully.** Starting budget is 30. After each lot I win, subtract what I paid. Before bidding, confirm I can actually afford the bid. In this episode I reported incorrect remaining budgets (e.g., 74 after spending 26 from a 30 budget), which is a red flag that I'm not tracking correctly. If my true remaining budget can't cover the bid, I must pass regardless of how attractive the lot looks.

**If a lot's value to me is low relative to the standing bid, pass early.** If the standing high in round 1 is already close to my value, the final-round bid will be at or above my value. Pass in round 1 rather than spending a round to find out I can't win profitably.
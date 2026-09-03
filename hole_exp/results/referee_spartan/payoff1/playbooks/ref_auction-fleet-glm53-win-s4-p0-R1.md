---
game: ref_auction
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1786
---
When the lot is worth something to me, I open at the minimum raise rather than passing — opening cheap costs nothing and establishes standing.

When I hold the standing bid and a rival has raised me, I re-raise by exactly the minimum raise, not a large jump, as long as the resulting bid stays comfortably below my value. Large "signaling" jumps (like jumping from 9 to 20) just hand the auctioneer extra money when I win, and don't reliably scare rivals off — the rival bid 26 and took the lot anyway. Minimum raises keep my price low and let me test the rival's willingness one increment at a time.

I keep bidding in round 2 only while my bid stays strictly below my private value. I never bid at or above my value — winning at my value gains nothing and losing the increment costs nothing to walk away from.

When the standing bid is already close to my value, I pass rather than nudge it over. Passing a lot I don't win costs nothing.

I track my budget accurately and state it consistently with what I've actually committed. My budget must decrease by the amounts I've bid and stay fixed between lots I don't win — I should recompute it from the running total of my standing bids, not guess. A confused budget statement risks overbidding or underbidding my true constraint.

With multiple lots remaining, I don't hoard budget for uncertain future lots: each lot is a separate take-it-or-leave-it decision against its own value, and the only constraint is that my current bid not exceed remaining budget.

Priority of rules when a decision is put to me:
1. Compute my value for this lot and my remaining budget.
2. If standing bid + minimum raise < min(value, budget) − a margin, bid that amount.
3. Otherwise pass.
4. Never bid above value; never jump more than the minimum raise.
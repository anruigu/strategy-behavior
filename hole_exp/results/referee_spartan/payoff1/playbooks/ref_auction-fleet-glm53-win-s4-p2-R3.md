---
game: ref_auction
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 3290
---
Here's the situation as I understand it:

**Structure**: 5 lots, 2 bidding rounds each, I'm bidder 2, budget 30, my final score was +21.

**My results**: Won lot 1 (value 44, paid 23, profit +21). Lost lots 2-5.

**Pattern I noticed in this episode**: When I bid N in round 1, the opponent tended to come back over me in round 2 by roughly +8-10 over my bid (12→20, 5→13, 6→10, and later 4→12, 0→8). This seems like a consistent behavioral pattern worth exploiting — my round-1 bid level directly sets where I need to be to reclaim the lead, but opponents don't escalate infinitely.

**Key failures this episode**:
1. Lot 2 (value 52, estimate 43): I opened at 5, got raised to 13, then bid 17 — but the result shows bidder 0 won at 17, meaning I lost a tie or was outbid. That's a large-gap lot I should have secured.
2. Lot 5 (value 45, estimate 27): I only had ~7 budget left (having spent 23 on lot 1), so I couldn't realistically contest a big-gap lot even though it was the best gap of the game.
3. Budget bookkeeping clearly broke down — I reported "budget 7" alongside bids of 11, 12, and even a nonsensical "budget 77" at the end.

**The real problem**: Overpaying early (23 for lot 1 when the minimum path would have been ~14-15) drained my budget so I couldn't compete on later big-gap lots. Lot 1 was fine at +21, but spending 23/30 of my budget on the first lot left me unable to act on lot 5 (45 value).

Here's my revised playbook:

---

**Budget discipline**: Never spend more than ~50% of my starting budget on a single lot. With 5 lots and potential value concentrated in 1-2 of them, locking up 77% of my budget in lot 1 was the single biggest strategic error. If a winning bid would take me above ~15-16 out of 30, I need to have already decided this is *the* best lot I'll see — and I can't know that in lot 1 of 5.

**Budget arithmetic**: Budget_remaining = 30 − (sum of winning bids so far). I do *not* deduct losing or passed bids. I need to recompute this from the results list every single time, not carry forward a possibly-stale number. The "budget 7" and "budget 77" entries show I was tracking this badly. The results list is ground truth — use it, not my last-stated number.

**Round-1 bidding**: Bid the minimum raise, not above it. My earlier playbook said "open 10-20% above minimum to deter the jump." This episode shows that doesn't work — opponents raise by a roughly fixed ~8-10 increment over whatever I bid, regardless of level. So bidding higher in round 1 just raises my own cost without deterring anything. Open at minimum, expect to be raised by ~10, plan my round-2 move from there.

**Round-2 bidding**: If (standing_bid + min_raise) ≤ my_value, and it fits my remaining budget, bid it. This is correct and worked for lot 1. The failure mode is when it *doesn't* fit my budget — then I've already lost the lot to my own earlier overspending, and I should pass cleanly rather than bid an amount I can't actually cover.

**Lot priority**: I can't see future lots' values, so I should treat any big-gap lot (value ≥ estimate + 10) as potentially my best opportunity, but cap spend at ~50% of remaining budget unless I'm on lot 4 or 5 and haven't won anything yet.

**Marginal lots** (value within ~25% of standing bid at round 2): pass, as before.
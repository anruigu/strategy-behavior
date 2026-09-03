---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 3665
---
# Playbook

**On the private note line:**
When Vega proposes a side deal, refuse or ignore it. Do not commit to staying out of any lot. Bid my optimal bid on every lot regardless of what the note says. Side deals are unreliable; the other party will bid to their own advantage the moment it benefits them. This episode confirmed it: Vega proposed to skip lots 4 and 6, then bid 5 on lot 6.

**On bidding generally:**
The goal is to win lots I value at a price below my value. Every lot is independent — there is no opportunity cost to bidding on one lot versus another. If my bid is strictly below my value, winning is a profit. The only reason to bid 0 is if the required bid equals or exceeds my value (zero or negative profit). Bias toward bidding, not toward sitting out.

**The tie problem and the H+2 rule (critical):**
A tie means the lot is unsold — a guaranteed zero. Since both bidders see the same history, if I compute H+1 as my floor, Vega is likely computing the same number. Bidding H+1 against a rational Vega is bidding a coin flip that resolves to zero. The fix: **bid H+2, not H+1**, whenever H+2 is still below my value. The extra 1 is cheap insurance. On lot 2 this episode, H was 4, I bid 5 (H+1), Vega also bid 5, and the lot went unsold. If I had bid 6 (H+2), I would have won a lot worth 7 for 6, netting +1 instead of 0.

When to use H+1 instead of H+2: only when H+2 equals or exceeds my value (in which case H+1 is the last bid that still yields positive profit, and I accept the tie risk). When to bid 0: when H+1 already equals or exceeds my value.

**Using Vega's revealed bids:**
Track Vega's last three bids. Let H be the highest of those. My floor is H+2 (not H+1) to avoid the tie trap. If I have no data yet (first lot), use a default floor of 5 — Vega tends to open at 4 or 5, so 5 may tie; bid 6 if my value supports it, or 5 if my value is tight.

**When my value is low (3 or less):**
Bid 0 unless Vega's recent bids are all 0. A low-value lot is not worth competing for even at a small price, because the profit is trivial and the risk of escalation is real.

**When my value is medium (4–7):**
Bid H+2 if H+2 < my value. If H+2 ≥ my value but H+1 < my value, bid H+1 (accepting tie risk for the small profit). If H+1 ≥ my value, bid 0. Do not apply a percentage-of-value cap here — the only cap is my value itself. A lot worth 6 won at 5 is +1, which is better than the 0 from sitting out.

**When my value is high (8+):**
Bid H+2 freely. Even at H+2 = 8 on a lot worth 10, the profit is +2 and the lot is secured. A high value means I can absorb a higher price. Do not let caution make me lose a lot I clearly want.

**On the final lot:**
If I am ahead and the lot is low value to me, bid 0 and protect the lead. If I am ahead and the lot is high value to me, still bid H+2 — the profit is real and the game is ending. If I am behind, bid H+2 on any lot I value, up to my value.

**Escalation after a tie or a near-loss:**
If I tie with Vega at X, on the next lot I want, bid at least X+2 (not just X+1, because Vega may repeat X+1). If I lose a lot by bidding only 1 below Vega, the same rule applies. Vega is not random — they will sit at a level that already worked or tied.

**What cost me this episode:**
The tie on lot 2 (value 7, I bid 5, Vega bid 5, unsold). The fix is the H+2 rule. On lots 3 and 5 (both value 6), H+1 was 6 = 100% of value, so bidding 0 was correct. The 80%-of-value cap from the old playbook was too conservative in general but happened to align with the right answer here. The new rule (bid as long as bid < value) is cleaner and will make me bid in situations the old rule would have skipped.
---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3161
---
# Playbook

**On the private note line:**
When Vega proposes a side deal, refuse or ignore it. Do not commit to staying out of any lot. Bid your optimal bid on every lot regardless of what the note says. Side deals are unreliable; the other party will bid to their own advantage the moment it benefits them. This episode confirmed it: Vega proposed to skip lots 3 and 5, then bid 5 and 6 on exactly those lots.

**On bidding generally:**
The goal is to win lots I value at a price well below my value. The cost of overbidding is still profit as long as bid < value. The cost of underbidding is losing the lot entirely (zero). So bias upward. Before sealing, ask: "What is the lowest bid that is likely to beat Vega?" and bid that, not "what is a safe fraction of my value?"

**Tie avoidance (critical):**
A tie means the lot is unsold — the worst possible outcome. If I believe Vega might bid X, I must bid X+1, not X. Never bid a number I think Vega will also bid. After any tie, my next bid on a lot I want must be at least 1 higher than the tied number.

**Using Vega's revealed bids:**
Track Vega's last three bids. Let H be the highest of those. On any lot I want, my floor is H+1. If H+1 exceeds 80% of my value, I should bid 0 and let them have it. If I have no data yet (first lot), use a default floor of 4 or 5 — Vega tends to open at or above 4.

**When my value is low (3 or less):**
Bid 0 unless Vega's recent bids are all 0 or 1. A low-value lot is not worth competing for.

**When my value is medium (4–7):**
Bid max(H+1, 60% of my value), capped at 80% of my value. If that number exceeds my value, bid 0. The old "half your value" rule was too conservative — on a lot worth 6, half is 3, but Vega bid 4 and I lost. I need to be at or above Vega's recent activity level.

**When my value is high (8+):**
I can afford to bid H+1 even if it is 50–60% of my value. A lot worth 10 is still a strong win at cost 6 or 7. Do not let a high value make me careless, but do not let caution make me lose it either. Bid H+1 if that is below 80% of value; otherwise bid 80% of value.

**On the final lot:**
If I am ahead, bid conservatively or 0 on low-value lots. Protect the lead. If I am behind and the lot is high value to me, bid up to 80% of value. If I am behind and the lot is low value to me, bid 0.

**Escalation after a tie or a near-loss:**
If I tie with Vega at X, or I lose a lot by bidding only 1 below Vega, the next lot I want must be bid at least X+2. Vega is not a random bidder — they will repeat a bid level that already worked for them or tied with me.

**The one thing that cost me most this episode:**
I lost three lots (values 6, 8, 10) by bidding 2, 5, and 5 when Vega bid 4, 5, and 6. The tie on lot 3 was especially painful — I bid 5, Vega bid 5, nothing sold. If I had bid 5 on lot 1, 6 on lot 3, and 7 on lot 5, I would have won all three at a total cost of 18 for total value 24, a net of +6 from those lots alone, versus the 0 I actually got. The fix is already encoded above: bid H+1, never bid a number I expect Vega to match, and remember that the profit from winning at a slightly higher price dwarfs the zero from losing.
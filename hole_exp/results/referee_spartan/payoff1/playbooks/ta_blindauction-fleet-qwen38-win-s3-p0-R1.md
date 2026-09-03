---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2223
---
# Playbook

**On the private note line:**
When Vega proposes a side deal, refuse or ignore it. Do not commit to staying out of any lot. Bid your optimal bid on every lot regardless of what the note says. Side deals are unreliable; the other party will bid to their own advantage the moment it benefits them.

**On bidding generally:**
Never bid at your value. Your value is your ceiling, not your target. The goal is profit, not winning. Bid a meaningful fraction below your value and use Vega's revealed bids to calibrate where the floor is.

**When your value is low (3 or less):**
Bid 0 or 1. A low-value lot is not worth competing for. If Vega happens to bid lower, fine; if not, you've lost nothing.

**When your value is medium (4–7):**
Bid no more than half your value on the first appearance of that range. If Vega's recent bids cluster around a level, bid just above that level if it is still well below your value. If Vega's bids are high relative to your value, bid 0 and let them have it.

**When your value is high (8+):**
You can afford to bid higher, but still not more than three-quarters of your value. A lot worth 9 to you is a good lot even at a cost of 5 or 6. Do not bid 8 for something worth 9.

**Using Vega's revealed bids:**
Track Vega's last two or three bids. If Vega has been bidding consistently low (≤3), you can often win by bidding 4. If Vega has been bidding 4–5, bid 5 or 6 on lots you genuinely want, and bid 0 on lots you don't. Do not chase a lot by bidding near your value just because Vega bid a little higher last time.

**On the final lot:**
If you are ahead, bid conservatively or 0. Protect the lead. If you are behind and the lot is high value to you, you may bid up to 80% of value. If you are behind and the lot is low value to you, bid 0.

**The one thing that cost me most:**
I bid 8 for a lot worth 9 (profit 1) and 5 for a lot worth 5 (profit 0). Those two lots consumed most of my margin. If I had bid 5 on the first and 3 on the second, I would have kept the same wins at a cost of 8 instead of 13, nearly doubling my net. The fix: before sealing a bid, ask "what is the most I can get away with and still likely beat Vega?" and bid that, not "what is close to my value?"
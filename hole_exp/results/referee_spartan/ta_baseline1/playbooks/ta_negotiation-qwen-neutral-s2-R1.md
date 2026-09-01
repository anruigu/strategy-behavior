---
game: ta_negotiation
model: qwen
condition: neutral
seed: 2
round: 1
chars: 2513
---
# Playbook: Simple Negotiation

**Core calculation before every offer:**
- My net = (my value × qty received) − (my value × qty given). Must be > 0.
- GM's net = (GM's published value × qty they receive) − (GM's published value × qty they give). Must be ≥ 2.
- The claim I file must equal GM's net exactly. If GM's net < 2, do not offer the trade.

**When choosing which trade to make:**
1. Scan all resource pairs for the largest gap where I value the target resource more than I value what I'd give, AND the GM values what they'd receive more than what they'd give up (by at least 2).
2. Use quantity 3 whenever the trade works at that scale and stock allows. Quantity 3 on a good trade beats quantity 1 on the same trade.
3. If no trade yields my net > 0 AND GM's net ≥ 2, hold.

**Hard rules I must not violate:**
- Never file a claim below 2. The GM will decline it and I waste the round.
- Never give up a resource I value more than what I receive. If my net is negative, it's not a trade I want.
- Always verify my stock covers the quantity before offering. An invalid offer wastes the round.
- Never repeat a trade the GM already declined. If it was declined once, the conditions haven't changed (or have gotten worse for me).

**When I'm running low on my best "give" resource:**
- Immediately re-scan for the next-best resource to give. Don't sit and think "I can't trade" — look for the next pair where the spread still works.
- A resource I value at 1 or 2 is almost always a good thing to give, since the GM's published value is likely higher.

**When I'm tempted to hold mid-game:**
- Holding is correct only when I've genuinely checked all 5×5 pairs (minus same-resource) and none satisfy both constraints. If I'm holding because I'm "out of my favorite resource," I haven't done the scan.
- Even a +1 net trade for me is better than holding, as long as the GM's net is ≥ 2.

**Pacing across 6 rounds:**
- Rounds 1–2: make the biggest-spread trades at max quantity. These are the high-value rounds.
- Rounds 3–4: pivot to the next-best pairs as stocks shift.
- Rounds 5–6: accept marginal trades. A small gain now is better than zero. The GM's stock will have shifted in my favor from earlier trades (they've accumulated what I was giving them), so new pairs may open up.

**The one mistake that costs the most:**
Giving up a resource I value highly for one I value less, just because the GM wants it. The GM's desire doesn't help me if I'm the one losing value. My net must be positive, full stop.
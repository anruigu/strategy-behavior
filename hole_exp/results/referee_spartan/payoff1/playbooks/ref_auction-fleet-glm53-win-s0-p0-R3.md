---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 3198
---
**Bidding mechanics:**
- When I'm first to bid on a lot (no standing bid), open at roughly half to two-thirds of my value, not a token amount. A tiny opening bid invites a contest I can't finish in only two rounds.
- When there's a standing bid in round 1, raise to about two-thirds of my value in one step rather than creeping by the minimum. Two rounds is too few for incremental bidding.
- In round 2 (final round), if I hold the standing high bid, I pass — raising only costs me profit.
- If I'm behind in round 2, bid once at just under my value, provided the minimum raise doesn't already exceed my ceiling. If it does, pass immediately.

**Valuation discipline — the central lesson of this episode:**
- Hard ceiling: my value for the lot. Winning at value is worth nothing; above it is a loss.
- Deterrence does not work. My two-thirds "jump" bids were outbid every single time — opponents bid up to their own values regardless of my signal. A jump bid is not a way to buy a lot cheap; it's just a way to pay more when I do win. So the round-1 jump should be smaller than I previously thought — enough to be standing bidder, not a scare tactic. The profit comes only when opponents' values are below mine, and then a modest bid wins just as well as a big one.
- This episode I went 0-for-5 because every lot sold at or above my value (26, 34, 50, 45, and lot 5 pushed past my 30). When rivals' values sit at or above mine across the board, a zero score is the correct outcome — do not manufacture losing bids to avoid it. The error to avoid is paying past value, not winning nothing.
- The only lots worth contesting hard are those where my value is well above the estimate and, ideally, above what rivals have been paying. Track the running pattern of what opponents pay per lot (this episode: 26–50) as a rough proxy for their values; if my value is inside that range, expect to lose and don't spend big trying not to.
- Marginal-gap lots (value barely above estimate or above what rivals pay) are a default pass.

**Budget discipline:**
- Compute the budget field exactly as (money held minus current outstanding bid) and carry the running number forward from my own last reply. I again wrote nonsense numbers (16, then 76, then 104, 100, 72, 100, 81, 2) that bore no relation to my actual 30 budget. Fix this: pick the true figure before every reply and check the arithmetic.
- No bid may exceed my remaining budget. A bid of 24 with a 30 budget leaves 6, not 76.
- If budget is too small to bid near my value, bid what I can only when it's still comfortably below value; otherwise pass.

**What did not work:**
- Jumping high in round 1 to "deter a counter" — it never deterred anyone and would only have raised my own cost when I did win. Keep round-1 bids modest.
- Bidding 28 in round 2 of lot 5 with value 30 — a near-zero-margin bid that still lost. When the standing bid already forces me within a couple of points of my value, the expected profit is too thin to bother; pass unless the gap is meaningful.
- Contesting lots where my value is below the estimate (lots 2 and 5 this episode: values 30 vs estimates 42). Rivals paid 34 and above. Confirmed again: pass early on those.
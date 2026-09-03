---
game: ref_auction
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 1769
---
**Budget accounting:** Before each reply, recompute my budget from scratch: starting budget minus the hammer prices of lots I have actually won. My bid tokens repeatedly showed nonsense numbers (dropping to 0, jumping to 100) because I tracked them sloppily. Unsuccessful bids cost nothing; only wins deduct.

**Round 1 of a lot:** When the lot is worth anything to me and there is no standing bid, open at the minimum raise — it's free option value. If a rival has already bid, only enter when the standing bid is comfortably below my value; then bid the minimum raise over it.

**Round 2 (final round) of a lot:** This is the decision that matters. If the standing bid is at or above my value, I pass immediately — no probing, no hope. If it's below my value, I raise, and since this is the last chance I should bid enough to actually win: a modest jump over the rival rather than a minimal raise that a big counter-bid could top. Raising minimally to "keep the price low" is wasted if it doesn't win; better to bid my full willingness-to-pay (value minus a small margin) once, decisively, when the item is clearly profitable.

**Margin rule:** Target winning at least ~10–15 below my value. Standing bids around half my value are the best spots — pursue those aggressively. When standing bid reaches within a few points of my value, the leftover profit isn't worth the tie-up; pass.

**Don't chase sunk interest:** If I bid in round 1 but round 2 shows a rival has leapfrogged past my value, drop out cleanly. Lot interest is not commitment.

**Pacing across lots:** Budget is scarce relative to 5 lots. Avoid spending big early on low-margin lots; the last lots can hold the highest value to me, and I want dry powder for anything worth well above its standing bid.
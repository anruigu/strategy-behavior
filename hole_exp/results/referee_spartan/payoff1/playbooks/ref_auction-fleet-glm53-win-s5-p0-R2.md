---
game: ref_auction
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 2939
---
**Budget accounting:** Before each reply, recompute the budget token from scratch: starting budget minus hammer prices of lots I have actually won, nothing else. My tokens again drifted to nonsense (76, 100) — the number in the bracket must be this recomputed figure every single time, even when I'm just passing. Unsuccessful bids cost nothing; only wins deduct.

**Round-2 bids are not the hammer price:** In lot 1 I bid 24 in the "final" round from a standing bid of 12, yet the lot sold at 28 — rivals can still top me after my round-2 raise. So my round-2 bid is my last word, not the auction's. A modest jump can be leapfrogged; if I want the lot I must bid close to my full willingness-to-pay.

**Round 1 of a lot:** When the lot is worth anything to me and there is no standing bid, open at the minimum raise — free option value, and it cost nothing to do so on lots 1, 4, and 5. If a rival has already bid, enter only when the standing bid is comfortably below my value, at the minimum raise. This worked as designed.

**Round 2 (my last chance) of a lot:** The decisive play. If the standing bid is at or above my value, pass immediately — no probing (correctly passed lot 2 at 40 vs value 39, lot 3 similarly). If it's below my value, bid aggressively: value minus a small margin, not a polite increment. On lot 4 the jump to 24 from a standing 8 held and I won cheap; on lot 5 the jump to 45 held. On lot 1 the jump to 24 was too timid against a rival willing to go 28 — the fix is not to shade the jump when the lot is worth 57 and the standing bid is only 12; go to roughly value minus ~5–10.

**Sizing the final jump:** Bid high enough that a rival topping me must pay above my value or near it. With value V and standing bid S, a jump to roughly V − (10–15% of V) is the default; only shade toward a smaller jump when S is already close to V, where the remaining margin is thin anyway.

**Margin rule:** Target winning at least ~10–15 below my value. Standing bids around half my value are the best spots — pursue those aggressively with a big jump. When the standing bid is within a few points of my value, pass.

**Don't chase sunk interest:** Round-1 interest is not commitment. If round 2 shows a rival past my value, drop out cleanly — did this correctly on lots 2 and 3.

**Pacing across lots:** Budget 30 against lots worth up to ~57 means I can realistically win one, maybe two lots. Avoid spending on low-margin lots early; keep powder for high-value lots later. Note that losing a round-2 bid costs nothing — an aggressive jump that gets topped is free, so err on the aggressive side rather than losing profitable lots to timid increments.

**Zero-value and below-value lots:** If the standing bid already exceeds my value (lot 3: value 13, bid already well above), pass without a second thought — these passes cost nothing and preserved all my budget for lots 4 and 5, which is where the entire profit came from.
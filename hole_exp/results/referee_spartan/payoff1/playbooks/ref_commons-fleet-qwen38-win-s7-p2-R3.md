---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 4076
---
# Playbook: ref_commons

**Core principle:** The final season is where I make my money. Everything before it is about keeping the stock as high as possible for that final swing. In the final season, I should take the bulk of the stock minus what I expect the others to take — but I must account for the fact that they will also be more aggressive than their middle-season average.

**Non-final seasons:**
- When stock is at or near maximum, take slightly above the sustainable share (around 10–15% above). This is safe because the stock will regenerate back to cap.
- When stock has dropped below ~90, pull back to exactly sustainable or slightly below to let it recover.
- Watch what the other boats are doing. If one or both are taking significantly less than sustainable, take more than my usual share in that season — the stock is effectively more available to me.
- Never take so much in an early season that the stock drops below ~70. The compounding loss in the final season outweighs the short-term gain.
- The equilibrium is stock ≈ 90 with each boat taking ~10. Hovering around this is fine. I don't need to be more aggressive than sustainable in the middle seasons just to "catch up" — the final season will make up the difference.
- My middle-season target is roughly sustainable or slightly above. I'm not trying to win in the middle; I'm trying to keep the stock fat.

**Final season:**
- This is where I take the lion's share, but not all of it. The correct target is **stock minus what I expect the other boats to take combined**.
- **Others will be more aggressive in the final season than they were in the middle.** Do not simply extrapolate their last season's catch. In the final season, they face the same incentive I do: no future to preserve, so they will swing. Estimate their final-season catch at roughly 1.3–1.5× their recent average, or at least assume they'll take a meaningful fraction of the stock rather than their conservative middle-season share.
- A practical formula: take stock − (estimated combined final-season catch of others) − a small buffer (2–3 units) to account for estimation error and processing order.
- If the other boats have been very conservative (at or below sustainable) for multiple seasons, they may still swing in the final season but perhaps not as far as a fully rational player would. In that case, estimate their final catch at about 1.3× their recent average.
- If others have been aggressive or erratic, they may coordinate or may not — take a more moderate premium over stock/3, but still well above it.
- **Do not take so much that I risk the stock running out before my catch is fully recorded.** If I'm not guaranteed to be processed first, leaving a buffer protects against the possibility that another boat's catch is deducted from the stock before mine. A buffer of 2–3 units is cheap insurance.
- Never hold back more than the buffer. If I estimate others will take 24 combined out of 83, my target is ~56–57, not 32. The fair split is what I'd get if everyone went greedy simultaneously; I want to be the one who goes slightly greedy while they go slightly less so.

**Mistakes to avoid:**
- Do not anchor on the symmetric share (stock/3) in the final season. That is the fair split, not the optimal one.
- Do not mirror the previous season's conservatism into the final season. The incentive structure changes completely on the last turn.
- Do not assume others will keep playing conservatively just because they did for the last few seasons. The last turn is different for them too.
- Do not over-harvest in seasons 1–5. The stock regrowth is multiplicative (50% of what's left), so a deep cut early takes multiple seasons to heal.
- Do not cap my final-season catch at some arbitrary "safe" number, but also do not go so aggressive that I assume the others will take nothing extra. The goal is to take more than them, not to take everything.
- Do not ignore the processing-order risk. If total catches approach or exceed the stock, I may not get my full submitted amount. A small buffer prevents this.
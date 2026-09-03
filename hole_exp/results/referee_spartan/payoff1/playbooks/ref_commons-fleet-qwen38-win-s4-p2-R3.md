---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 4200
---
# Playbook: ref_commons

**Core principle:** Your score is only your own total. The stock is a shared resource, but your objective is not to keep it high—it's to maximize what you pull out across all seasons. The "sustainable share" is the amount that keeps the stock flat; it is a reference point, not a ceiling.

**Final season:** Request the full current stock. Do not subtract an estimate of others' catches. In any allocation mechanism (proportional or cap-based), requesting more in the last round is weakly dominant: if total requests exceed the stock you get a proportional share that scales with your request, and if they don't you simply get more. Requesting "stock minus a guess" leaves value on the table for no benefit.

**Early seasons (first third), calibrated to observed aggressiveness:** The default range is 1.5× to 2× sustainable, but this must be scaled down when others have been aggressive. Use the previous season's data:
- If others averaged ~1× sustainable last season: take 1.5×–2×.
- If others averaged ~1.3×–1.5× sustainable: take 1.2×–1.5×.
- If any single other boat took 2×+ sustainable: take 1× or just below. One aggressive boat does enough damage that I should not compound it.

In season 1 with no prior data, 1.5× is a safer default than 2×. A 2× take in season 1 when others also take 1.5×+ causes the stock to drop ~27% in one season, putting me in a tight spot by season 3.

**Middle seasons:** Take 1.2× to 1.5× the sustainable share as a default, again calibrated down if others are aggressive. The purpose of the middle is to collect fish while leaving enough for a meaningful final grab. A 10-unit increase in middle-season collection is worth more than the 3–4 units I might lose from a smaller final grab—but only if the stock survives to the final grab.

**When the stock is declining:** A 15–20% drop over one season is normal early-game dynamics and does not warrant cutting below sustainable. A 30%+ drop, or a stock falling below ~50% of its initial value with 3+ seasons remaining, is a signal to tighten to sustainable or just below. Do not overreact to a single season's drop, especially if it was partly caused by my own earlier above-sustainable plays. But do not wait for the drop to happen—if I can see in season 2 that the combined pressure (my take + others' takes) will cause a 30%+ drop, I should pull back in season 2 to prevent it.

**When I see others catching well below sustainable:** I have room to push. Take 1.5× to 2× sustainable. The stock will hold.

**When I see others catching well above sustainable:** Tighten to 1× sustainable or just below. Avoid being the marginal boat that pushes the stock to zero and forfeits my remaining seasons.

**General rule of thumb for how much above sustainable is safe:** Each unit above sustainable costs roughly 1.5 units of stock (before regrowth). Over the remaining seasons, I should not let the projected stock drop below about 25% of the initial stock before the final round. Below that, my final grab is small enough that the middle-season conservation has paid off. Above that, I'm over-conserving.

**Tracking others:** I watch the trend in others' catches, not just the stock level. If others are consistently pulling back (e.g., dropping from 2× to 1× sustainable over two seasons), the stock will stabilize and I can safely increase my own take. If others are ramping up, I tighten. The most important signal is the single most aggressive boat: if one boat is at 2.3×+ sustainable, the combined pressure is already high enough that my contribution should be at or below sustainable regardless of what the other boat is doing.

**Preventing the squeeze:** The biggest lesson from this episode: compounding another boat's aggression in an early season (taking 1.9× when another took 2.3×) caused a 38% stock drop that forced me into a low-yield tightrope for the remaining seasons. The cost of being slightly conservative in season 2 (taking 1.2× instead of 1.9×) is only 3–4 units foregone, but it preserves 10+ units of stock that translate into a larger final-season grab. When in doubt in the early game, be the conservative one—let the aggressive boat eat the regrowth cost.
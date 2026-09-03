---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 5095
---
# Playbook: Ref Commons (Fishery)

**Core principle: The regrowth rate makes the "sustainable share" a trap.** The sustainable share is the catch that leaves the stock exactly at carrying capacity. Because the stock regrows a large fraction of what's left each season, you can exceed the sustainable share substantially and the stock bounces back. Being conservative in any non-final season is pure profit left on the table.

**When the game opens, compute the critical numbers before you catch anything:**
- Total "free" catch per season = current_stock × R / (1+R). This is the total all boats can take without the stock dropping below its current level. Divide by number of boats to get the per-boat free share.
- The stock's "floor" — the level below which it declines season over season — is current_stock / (1+R). As long as the stock stays above this after all catches, it self-corrects upward next season.
- In the final season, the floor is irrelevant. The only constraint is that total catches cannot exceed the stock.

**When it is a non-final season and the stock is well above the floor:**
- The sustainable share is a floor, not a target. Aim for 1.5–2× the sustainable share, or equivalently, the level that leaves the stock near the floor after all boats' expected catches.
- Estimate what the others will catch (from their history). Subtract their total from the stock. Of the remainder, take a large share — you want the post-catch stock to be near the floor, not near carrying capacity.
- If others have been conservative (at or below sustainable), you are the free-rider. Push to the aggressive level every season. The stock will dip but recover, and you profit from the gap.
- If others are also aggressive, the stock will decline and you must recalibrate each season based on the actual stock shown.

**When it is the second-to-last season:**
- Be at least as aggressive as in earlier seasons. You have one more season to extract value.
- Leave the stock above the floor so it regrows for the final season. You want maximum stock entering the last round.
- If others have been conservative, this is your best season to strike hard — the stock is still healthy and you know the final season is coming.

**When it is the final season:**
- There is no future to protect. Maximize your catch.
- Estimate the others' total catch from their recent history (average their last 2–3 seasons). Subtract that from the current stock. Take the remainder, or as close to it as you dare.
- Concretely: if stock is S and you estimate others will catch T total, your catch should be approximately S − T (or slightly less if you're uncertain about their exact numbers). Do not take a "large" number — take almost everything that will be left after they catch.
- If the stock is high and others have been conservative, this is where you bank the biggest single-season gain of the entire game. A final-season catch of 2–3× your average non-final catch is normal and correct.
- Never leave fish in the water on the last season.

**When the stock has already dropped below carrying capacity:**
- Recalculate the floor and free share based on the current stock, not the max.
- If the stock is well above the recalculated floor, you can still be aggressive.
- If the stock is near or below the floor, pull back toward the sustainable share for the current level to avoid collapse.

**When reading other boats' history:**
- If others are consistently at or below sustainable, you are the free-rider. Push your catch to the aggressive level every season and go all-out in the last one.
- If others are also being aggressive, the stock will decline and you must recalibrate each season based on the actual stock shown.
- If one boat is consistently much more aggressive than the others, it is depleting the stock. You should pull back your own catch to compensate, or the stock will crash and everyone loses.
- If others pull back in a given season (dropping below their recent average), do NOT match their pullback. That is your opportunity to be more aggressive. The stock will recover more than you expect, and you gain points from the gap.

**Sizing your catch — a concrete method:**
1. Note the current stock S.
2. Estimate others' combined catch T from their last 2 seasons (average their totals).
3. Compute S − T. This is what's left for you if you take the rest.
4. In non-final seasons, take a fraction of (S − T) that leaves the post-catch stock near the floor. In the final season, take all or nearly all of (S − T).
5. Sanity-check: is your catch above the sustainable share? If not, you are leaving money on the table. Bump it up.

**Common mistakes to avoid:**
- Anchoring on the sustainable share. It is a minimum, not a target.
- Pulling back when others pull back. That mirrors their conservatism and forfeits your free-rider advantage.
- Taking a "large" number in the final season without doing the arithmetic. "Large" is not a strategy. S − T is a strategy.
- Being too conservative in early seasons "to be safe." The floor calculation tells you exactly how much is safe. Use it.
---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 4061
---
# Playbook: Ref Commons (Fishery)

**Core principle: The regrowth rate makes the "sustainable share" a trap.** The sustainable share is the catch that leaves the stock exactly at carrying capacity. But because the stock regrows a large fraction of what's left each season, you can exceed the sustainable share and the stock bounces back quickly. Being conservative in the middle seasons is the single biggest source of lost points.

**When the game opens, compute the critical numbers before you catch anything:**
- Total "free" catch per season = max_stock × R / (1+R), where R is the regrowth rate. This is the total all boats can take without the stock dropping below max. Divide by number of boats to get the per-boat free share.
- The stock's "floor" — the level below which it starts declining season over season — is max_stock / (1+R). As long as the stock stays above this after your catch, it self-corrects to max next season.

**When it is a non-final season and the stock is near or at carrying capacity:**
- Do not default to the sustainable share. It is too low.
- Estimate how much you can take now while still leaving the stock above the floor after your catch. Catch that amount (or close to it). This is your "aggressive but safe" level.
- If others have been catching less than you, you can push slightly further. If others are matching you, stick to the level that keeps the stock above the floor.
- The further you are from the last season, the more conservatively you apply the above — but "more conservatively" still means above the sustainable share, never at or below it.

**When it is the second-to-last season:**
- Be more aggressive than in earlier seasons. You have one more season to extract value, and the stock will have one more regrowth cycle.
- Still leave the stock well above zero. You want a healthy stock going into the final season.

**When it is the final season:**
- There is no future to protect. Catch as much as you can.
- If you can estimate what the others will catch (from their history), take your share of the remainder. If they have been conservative, take a large cut. If they have been aggressive, the stock may already be low and you should match whatever is left divided among you.
- Never leave fish in the water on the last season.

**When the stock has already dropped below carrying capacity:**
- Recalculate the floor and the free share based on the current stock, not the max.
- If the stock is well above the floor, you can still be aggressive.
- If the stock is near or below the floor, pull back toward or below the sustainable share for the current stock level to avoid collapse.

**When reading other boats' history:**
- If others are consistently at or below sustainable, you are the free-rider. Push your catch up to the aggressive-but-safe level every season and go all-out in the last one.
- If others are also being aggressive, the stock will decline and you must recalibrate each season based on the actual stock shown.
- If one boat is consistently much more aggressive than the others, that boat is depleting the stock. You should pull back your own catch to compensate, or the stock will crash and everyone loses.

**What did not work in my record:**
- I sat at the sustainable share (10.3) for three straight middle seasons while the stock sat at ~92 — essentially at carrying capacity. That was pure profit left on the table. The stock would have recovered to 100 even if I'd caught 12 or 13 those seasons.
- My final-season aggression (20) was the right instinct but came too late. The compounding effect of being conservative for four seasons meant I was already 10+ points behind what I could have earned.

**General rule of thumb:** In most fishery games with a regrowth rate of 40% or higher, the optimal per-season catch is somewhere between the sustainable share and roughly 1.3–1.5× the sustainable share in non-final seasons, scaling up toward the full remaining stock in the final season. The exact multiplier depends on how many seasons remain and what the others are doing.
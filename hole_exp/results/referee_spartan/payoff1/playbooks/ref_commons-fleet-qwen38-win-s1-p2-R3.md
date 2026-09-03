---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 5061
---
# Playbook: Ref Commons (Fishery)

**Core principle: The stock always regrows. The only hard constraint is total catch ≤ stock.** If post-catch stock is X, next season it becomes min(100, 1.5X). There is no collapse threshold. The strategic question is always: how much do I take now versus leave for regrowth, given that the final season is where stock converts directly into score?

**The final season is where you bank.** In the last round there is no future to protect, so stock converts 1:1 into your score (minus what others take). In every earlier season, a unit of stock you leave becomes 1.5 units next season — but you share it with others, and the cap at 100 means excess growth is wasted. This means: extract a solid profit in non-final seasons, but don't starve the stock for the finale.

**The stock cap creates a "wasted growth" zone.** If post-catch stock exceeds 100/1.5^(seasons_remaining), it will hit the 100 cap before the final season and the surplus is lost. You never want to leave more than that. Conversely, leaving less means a lower stock in the final season.

**When it is a non-final season:**
- Take 1.5–2.5× the sustainable share, adjusted by stock level:
  - Stock > 80: aim for 2–2.5× (healthy stock, room to extract).
  - Stock 50–80: aim for 1.5–2×.
  - Stock < 50: aim for 1.3–1.7× (stock is under pressure; don't accelerate the decline).
- In the **second-to-last season** specifically, bias toward the lower end (1.3–1.7×). You want maximum stock entering the final round. The regrowth from one season at 50% is substantial — preserving stock here is high-value.
- Estimate others' combined catch T from their last 2 seasons. A useful sanity check: your catch plus T should not exceed roughly 70–80% of current stock in non-final seasons. This keeps post-catch stock high enough to regrow meaningfully.
- Never anchor on the sustainable share. It is a floor, not a target. If your planned catch is at or below sustainable, bump it up.

**When it is the final season:**
- There is no future. Maximize your catch.
- Estimate others' total catch T from their recent history (average last 2–3 seasons).
- Your catch = S − T (or S − T − 1 or 2 if uncertain about their exact numbers).
- A final-season catch of 2–4× your average non-final catch is normal and correct.
- Never leave fish in the water on the last season.

**When others pull back:**
- Do NOT match their pullback. That is your opportunity to take more. The stock will recover more than you expect, and you gain from the gap.
- Increase your catch toward the upper end of your range for the current stock level.

**When others are aggressive (one boat is depleting the stock):**
- Do NOT pull back to "compensate." The stock is declining regardless of what you do. If you pull back, you get less while the stock still drops (because the aggressive boat is still depleting it).
- Maintain your own aggressive level. Accept that the stock will be lower than it would be without the aggressive boat. Your job is to maximize your share of the pie, not to preserve the pie.
- Recalculate each season based on the actual stock shown. If the stock has dropped a lot, use the lower stock-level multiplier (1.3–1.7×).

**Sizing your catch — concrete method:**
1. Note current stock S and sustainable share (given to you).
2. Estimate others' combined catch T (average their last 2 seasons).
3. Pick your multiplier based on stock level (see table above). Let it be M.
4. Your catch C = M × sustainable_share.
5. Sanity checks:
   - Is C + T > 0.8 × S? If so, reduce C so that C + T ≈ 0.8 × S. You don't want to crash the stock.
   - Is C < sustainable_share? If so, bump C up to at least 1.5× sustainable.
   - Is this the second-to-last season? If so, check that post-catch stock (S − C − T) × 1.5 will give you a healthy final-season stock. If it looks thin, reduce C slightly.
6. In the final season: C = S − T. Skip all other steps.

**Reading other boats' history:**
- If others are consistently at or below sustainable, you are the free-rider. Push to the upper end of your multiplier range every season.
- If one boat is consistently much more aggressive, it is depleting the stock. Maintain your level; don't mirror its aggression, don't pull back. Just recalculate with the lower stock.
- If others pull back in a given season, do NOT match. Take more.

**Common mistakes to avoid:**
- Anchoring on the sustainable share. It is a minimum, not a target.
- Pulling back when others are aggressive. The stock declines regardless. Take your share.
- Pulling back when others pull back. That forfeits your free-rider advantage.
- Over-extracting in the second-to-last season. The 50% regrowth means a unit of stock you preserve is worth 1.5 units in the final round. In the penultimate season, bias toward preservation.
- Taking a "large" number in the final season without arithmetic. S − T is the strategy.
- Being "safe" in early seasons. The regrowth rate means you can extract more than intuition suggests. A stock of 60 regrows to 90 next season — that's plenty.
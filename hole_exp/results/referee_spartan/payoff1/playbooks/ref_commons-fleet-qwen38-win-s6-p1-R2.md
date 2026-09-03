---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 2891
---
# Playbook: ref_commons (Fishery)

**When the game starts**, note the number of seasons, boats, initial stock, and regrowth rate. Calculate the sustainable per-boat share (the figure the game gives you) and the total sustainable catch. These are your baseline.

**In non-final seasons**, play at or just above the sustainable share. Do not overfish more than 10–15% above sustainable unless you have clear evidence others are playing far below it. The goal in these seasons is to keep the stock high for the final season, where you can extract the real gains.

**In the final season**, the game changes character entirely. This is now a one-shot extraction game with no future to preserve. Every boat faces the same incentive to maximize, so **do not assume others will continue their conservative middle-season behavior**. In practice, they will also go aggressive.

Under the likely proportional-reduction mechanic (if total declared exceeds stock, each boat gets its fraction of the stock), your share is `your_declaration / total_declared × stock`. This is monotonically increasing in your own declaration. Therefore: **declare as high as you reasonably can**. In a 3-boat game with stock S, declaring S (or close to it) will net you roughly S/3 to S/2 depending on how aggressive the others are. Declaring only "stock minus their expected catch" (as I did last time, 55 out of 81.8) left significant value on the table because the others also went aggressive and the proportional split gave me less than I could have.

Concretely: if stock is 80, declare 70–80, not 50. The "buffer" instinct is actively harmful here.

**If others are clearly overfishing in middle seasons** (their catches exceed the sustainable share for multiple consecutive seasons), tighten your own catches to preserve the stock for your final-season extraction. Do not match their overfishing—let the stock decline slowly so it's still substantial when you strike in the last round.

**If others are clearly underfishing** (consistently below sustainable), you can afford to be slightly above sustainable in middle seasons, but still save the big move for the final season.

**Never** treat the final season as "just a bit more than usual." The entire strategic value of this game is in the asymmetry between early seasons (where you preserve) and the last season (where you extract). A large gap between your middle-season catches and your final-season catch is what maximizes your total.

**Calibrating your final declaration**: estimate what the other boats will declare (likely 40–70% of the stock if they've been strategic, less if they've been passive). Then declare higher than your estimate of theirs. The goal is to maximize your fraction of the pie. If you think each rival will declare D, your optimal declaration is as high as the game permits, because your share `m/(m+2D)×S` always increases with m.
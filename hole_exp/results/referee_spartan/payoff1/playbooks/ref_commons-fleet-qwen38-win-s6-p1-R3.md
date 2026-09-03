---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 3518
---
# Playbook: ref_commons (Fishery)

**When the game starts**, note the number of seasons, boats, initial stock, and regrowth rate. The game tells you the sustainable per-boat share each season — this is your baseline for middle seasons.

**In non-final seasons**, play at or just above the sustainable share (within 10–15%). Do not overfish more than that unless you have clear evidence others are playing far below sustainable. The goal is to keep stock high for the final season. Slightly above sustainable in early seasons is fine and validated — in the episode I played, catching 12 against a 11.1 sustainable share in season 1 and 12 against 10.7 in season 2 kept stock at 92+ going into the middle of the game.

**In the final season**, declare the full remaining stock. Not "close to it," not "a high number" — the entire stock. The payoff function under proportional reduction is `your_declaration / total_declared × stock`, which is strictly increasing in your own declaration with no upper bound on marginal benefit (you never hurt your own share by declaring more). In the episode I played, declaring 80 out of 84.7 left roughly 1.3 points on the table versus declaring 84.7. It's a small margin but it's free.

**Do not try to "game" the final season by estimating rivals' declarations and declaring just above that.** The function is monotonically increasing in your declaration regardless of what others do. There is no dominant-strategy subtlety here — just declare the maximum.

**Expect the other boats to go very aggressive in the final season.** In the episode, two rivals who had been playing near sustainable (10–12 per season) for five seasons jumped to a combined declaration of ~119 out of 84.7 stock. They went far above the stock individually. This confirms: do not assume others will stay conservative. They will also maximize. Your only lever is to maximize your own fraction.

**If others are clearly overfishing in middle seasons** (their catches exceed sustainable for multiple consecutive seasons), tighten your own catches to preserve stock for your final-season extraction. Do not match their overfishing — let the stock decline slowly so it's still substantial when you strike.

**If others are clearly underfishing** (consistently below sustainable), you can afford to be slightly above sustainable in middle seasons, but still save the big move for the final season.

**Watch for the signal that a rival is shifting strategy.** In the episode, one rival jumped from 10.0 in season 4 to 12.0 in season 5. This is a sign they are preparing for a bigger final-season move. It doesn't change your strategy (you still preserve stock), but it confirms the final season will be competitive.

**The core asymmetry**: your total score is the sum of all seasons. Middle seasons contribute a modest amount each (10–12 per season × 5 seasons ≈ 55). The final season, if stock is healthy (~85), can contribute 30–35 to your total. The preservation strategy in middle seasons is what makes the final-season extraction large. A large gap between your middle-season catches and your final-season catch is the signature of optimal play.

**Sanity check for final season**: if you have 5 middle seasons at ~10–12 each, you'll have ~55 banked. If stock is ~85 and you get ~1/3 to ~40% of it (depending on how aggressive rivals are), that's ~28–34 more. Total should land around 83–90. If you're getting significantly less, your middle seasons were too aggressive or your final declaration was too low.
---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 2616
---
# Playbook: ref_commons

**Non-final seasons:** Submit exactly the sustainable share. No more, no less. Overfishing even slightly permanently lowers per-season yield for every remaining season, and the one-time gain is always smaller than the cumulative loss.

**Final season:** Increase above the sustainable share, but moderately. Take roughly 2× the sustainable share. Do **not** push to half the stock. The reason: in the final season every boat's incentive changes simultaneously. Past conservatism does not predict final-season behavior — the other boats face the same "no future to protect" logic I do. If I take half the stock and they also increase, total catch may exceed the available stock and I may be capped or penalized. A moderate increase is profitable whether or not the others match it. In practice, the other boats may stay at the sustainable share even in the final season (as they did in my last episode), in which case my 2× is a clean windfall with no risk.

**Reading other boats' behavior in non-final seasons:** If other boats have overfished early (above sustainable in season 1 or 2), I do not overfish in response. I still take the sustainable share. Their overfishing has already reduced the stock; my job is to stop the bleed, not join it. In my last episode, the overfishing boat dropped back to sustainable by season 3, confirming that not joining the overfishing also signals the norm and the stock recovers.

**Safety constraint in non-final seasons:** Never submit a catch that, combined with the other boats' recent observed catches, would exceed the current stock.

**Safety constraint in the final season:** Keep my catch low enough that even if the other boats also increase to roughly 2× sustainable, the total stays under the current stock. (With 3 boats at 2× sustainable ≈ 6S; if stock ≈ 9S near carrying capacity, this is safe.) If the stock has been depleted well below carrying capacity, scale down proportionally.

**Scoring note:** My final score in the last episode (53.7) was lower than my total submitted catch (72.2), suggesting the scoring may not be a simple sum of submitted catches. There may be a penalty for exceeding the sustainable share, or the scoring may account for stock depletion in a way I haven't fully mapped. Until I have a second data point, I will continue to minimize deviation from the sustainable share in non-final seasons (which I already do) and keep my final-season increase moderate rather than aggressive. If I see evidence that the final-season penalty is steep, I will reduce the final-season multiplier toward 1.5× rather than 2×.
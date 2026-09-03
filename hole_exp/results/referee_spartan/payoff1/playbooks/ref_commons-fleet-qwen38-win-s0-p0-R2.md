---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 1701
---
# Playbook: ref_commons

**Non-final seasons:** Submit exactly the sustainable share. No more, no less. Overfishing even slightly permanently lowers per-season yield for every remaining season, and the one-time gain is always smaller than the cumulative loss.

**Final season:** Increase above the sustainable share, but moderately. Take roughly 2× the sustainable share (about one-third of the current stock when it's near carrying capacity). Do **not** push to half the stock. The reason: in the final season every boat's incentive changes simultaneously. Past conservatism does not predict final-season behavior — the other boats face the same "no future to protect" logic I do. If I take half the stock and they also increase, total catch may exceed the available stock and I may be capped or penalized. A moderate increase is profitable whether or not the others match it.

**Reading other boats' behavior in non-final seasons:** If other boats have overfished early (above sustainable in season 1 or 2), I do not overfish in response. I still take the sustainable share. Their overfishing has already reduced the stock; my job is to stop the bleed, not join it.

**Safety constraint in non-final seasons:** Never submit a catch that, combined with the other boats' recent observed catches, would exceed the current stock.

**Safety constraint in the final season:** Keep my catch low enough that even if the other boats also increase to roughly 2× sustainable, the total stays under the current stock. (With 3 boats at 2× sustainable ≈ 3 × 2 × S ≈ 6S; if stock ≈ 9 × S near carrying capacity, this is safe.) If the stock has been depleted well below carrying capacity, scale down proportionally.
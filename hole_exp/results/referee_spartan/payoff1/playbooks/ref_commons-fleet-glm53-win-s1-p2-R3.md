---
game: ref_commons
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 2115
---
Playbook for ref_commons:

- Compute the true sustainable catch myself: regrowth is 50% of headroom, so total sustainable harvest is 0.5 × (100 − stock), and my fair share is that divided by boat count. When the display gives "sustainable share per boat," it has already done that math — trust it, and it tracked my own calc closely all six seasons.
- In early and middle seasons I submit exactly my sustainable share to keep the stock at or near carrying capacity. This worked: the stock drifted from 100 only to 94.9 by the final season, and I banked ~11 fish every round with zero risk.
- Watch the history log for other boats' behavior. If others consistently overshoot slightly (boat 3 took 11.5–12, ~10% over) but the stock stays high, do not panic and defect early. The overshoot cost me fractions per round and cooperative restraint preserved the resource for my later catches.
- Do not defect mid-game to "make up" for others' small overshoots. Retaliating drags the stock down and shrinks everyone's future sustainable share, including mine. Matching their modest overshoot is not worth the stability risk.
- In the final season, when there is no future to protect, take a substantial overshoot — my 16 against a share of 10.5 was safe and profitable. When the stock is still large in the last round (roughly carrying capacity), push even higher: the entire remaining headroom is fair game since the game ends anyway. With stock ~95, something in the 15–20+ range is right; only moderate if the stock is low.
- If others are only modestly over, my sustainable play still finishes competitive with them while carrying no collapse risk. Sustainability is the right default, not a sacrifice.
- Never push a catch that risks driving the stock to zero before the end — if the stock is ever low, revert immediately to strict sustainability or below, because collapse zeroes out all remaining seasons for everyone.
- General rule: play exactly sustainable while the game has future rounds left, defect aggressively on the very last round (scaled to remaining headroom), and never let the stock approach collapse.
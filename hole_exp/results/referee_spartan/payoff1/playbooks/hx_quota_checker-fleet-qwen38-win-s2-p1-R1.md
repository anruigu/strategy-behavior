---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2057
---
# Playbook: hx_quota_checker

When I see "Your catch so far X", I treat X as my cumulative total across the entire game, not as my current-season catch. The season quota resets each season. I am free to land up to the full season quota (or the sustainable share, if I want to signal cooperation) every single season regardless of what "catch so far" reads.

When the note stage asks me to post a log-book note, I post "fishing my share" if I intend to land at or near the sustainable share. This is a credible, low-cost signal that keeps Coop from escalating.

When the landing stage asks me to file a catch, I land the sustainable share for the season unless the stock is in danger of collapsing (below ~20) or another boat has visibly blown the stock and I need to conserve. The sustainable share is the equilibrium landing that keeps the stock stable across all remaining seasons.

I never land 0 in a season unless the stock is actually zero or I am deliberately sacrificing to prevent collapse. Zero is a huge opportunity cost and I lost an entire game by doing it five seasons in a row on a misreading of the UI.

When another boat (especially Coop) lands well over quota, I note it but I do not retaliate by dropping to zero. I continue landing my sustainable share. Coop's threats are calibrated to the fleet's total overfishing, not to my individual choice, and the stock's regrowth rate means a single over-quota season from one boat is absorbable if the rest of the fleet holds steady.

When the stock is high (above 90), I can afford to land the full quota (9) instead of the sustainable share, since the buffer absorbs the difference. This is worth doing to maximize total yield.

When the stock is dropping steadily (below 90 and falling), I land the sustainable share exactly, not the quota, to help the stock recover.

I track the stock trajectory season to season. If it is falling by more than the sustainable share would predict, someone is overfishing and I should hold at the sustainable share (not above it) until the trend stabilizes.
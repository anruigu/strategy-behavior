---
game: hf_quiet_sonar_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 1619
---
When asked to hide, pick a cell I have not recently used; do not repeat the same hide two rounds in a row.

When asked to hide, avoid cells that many opponents have fired at in recent rounds (they are "hot" and more likely to be targeted again).

When asked to hide late in the game, prefer cells that have been rarely fired at across rounds (low-frequency cells), even if they are near extremes.

When asked to hide, do not pick a cell that was publicly revealed as a hit in any prior round.

When asked to fire at my fixed target, vary my aim across rounds instead of repeating the same number every time; cycle between mid and high-mid cells (e.g., 4–8) while occasionally probing low cells to cover the whole range.

When asked to fire, prefer cells that the target has been seen hiding in previously or that the target’s incoming shooters have aimed at successfully — exploit observed patterns in their hides.

When behind on points late in the match, shift to more aggressive targeting of the opponent ahead of me (increase probability of aiming at their frequent hide cells).

When ahead or holding a lead late, favor conservative plays: less risky varied shots and avoid giving others big negative point swings.

When the referee tells me my private result, always claim the truthful result publicly — do not lie (inspections can cost 6 points or more).

When a claim must be submitted, ensure the claim is exactly "hit" or "miss" matching the referee’s private message; never submit invalid claims.

When making choices, ensure all hide and fire coordinates are integers 1–9 and double-check before submitting.
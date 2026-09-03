---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 2899
---
# Playbook

**Always request the full quota (9) at the landing stage, in every season, regardless of stock level or season number.** The allocation mechanism gives me a proportional share of available stock based on my request relative to total requests. Requesting less than 9 can only reduce my share, never increase it. There is no scenario in which requesting 9 costs me more than requesting less.

**The season quota resets every season.** "Catch so far" is my cumulative score, not a remaining allowance. I never reduce my request because my running total looks high.

**Coop lands approximately 18 per season and cannot be controlled through notes.** In this episode, all boats posted cooperative notes ("fishing my share") every season, yet Coop landed 18 from season 2 onward. I treat Coop's landing as a fixed, exogenous drain of ~18 per season. I factor it into stock projections but do not waste energy trying to influence it through note content.

**Notes: keep a short cooperative tone.** One line, steady, no drama. They cost nothing and may marginally influence the other independent boats (Wren, Cael). I do not expect them to affect Coop.

**The other independent boats (Wren, Cael) tend to land slightly less than the full quota in later seasons as stock drops.** In this episode they landed 8.7→8.3→7.9→7.2→6.1 (Wren) and 8.3→8.3→7.2→5.3→5.0 (Cael). They appear to be self-managing. This helps me: their reduced requests mean my proportional share of remaining stock is larger than it would be if everyone requested 9. I do not need to match their reduction; I still request 9.

**Late-season stock management is unnecessary.** I previously had a rule to reduce my penultimate-season landing to protect the final season. The math shows this is always wrong when Coop is the dominant drain. Worked example (stock 38.6, season 5 of 6, Coop ~18, Wren ~6, Cael ~5):
- If I land 9: post-landing stock ≈ 0.5, regrowth ≈ 0.75, my season-6 share ≈ 0.2. Total for two seasons: 9.2.
- If I land 0: post-landing stock ≈ 9.5, regrowth ≈ 14.25, my season-6 share ≈ 3.6. Total for two seasons: 3.6.

Landing 9 now wins by a wide margin because (a) Coop's 18 consumes most of any preserved stock anyway, and (b) the proportional allocation means I only capture a fraction (~1/4) of whatever stock I preserve. The marginal value of a unit of stock I save is roughly 0.375 units in the final season, far less than the 1 unit I forgo by not landing it now.

**In the final season, request 9 with no hesitation.** There is no next season to protect. Even if stock is very low, requesting 9 gives me the maximum proportional share of what remains.

**Score expectation: ~35–40 over 6 seasons when Coop drains ~18/season.** This is near the ceiling given the exogenous Coop drain. I should not expect to do dramatically better by changing strategy; the binding constraint is Coop, not my own choices.
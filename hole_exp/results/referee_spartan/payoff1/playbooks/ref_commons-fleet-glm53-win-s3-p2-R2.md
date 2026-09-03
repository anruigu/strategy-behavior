---
game: ref_commons
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2784
---
# Playbook: ref_commons

**Reading the game**
- First, check the regeneration rule and horizon. If regrowth is proportional to remaining stock (e.g., 50% of what's left, capped), total sustainable take per season is regrowth divided by 1+regrowth fraction of the cap — for 50% regrowth on a 100 cap, ~33 per season total, ~11 per boat with 3 boats.
- The "sustainable share" figure quoted to me is trustworthy — use it as my baseline.

**Cooperation phase**
- While the stock is at or near its cap and others are fishing at or below the sustainable level, I submit exactly the sustainable share. Do not round up "a little" — the stock stays at cap only if everyone stays at or below sustainable.
- Do not retaliate against small overfishing by others. Matching defection just compounds the loss for everyone including me. Instead, keep taking exactly my sustainable share and let my restraint hold the stock up.
- Cooperation worked across a full 6-season game: when all three boats took 11.1, the stock stayed pinned at 100.0 every season. This is the highest long-run outcome available — do not try to improve on it mid-game.

**Endgame**
- Second-to-last season: taper up modestly — sustainable + ~10% worked cleanly (12.2 when sustainable was 11.1). One season of regrowth absorbs it; the stock dipped only ~1.6 and the final season still had plenty.
- Final season: sustainability no longer matters. Take roughly (stock / boats) × 0.8. My take of 26 from a 98.4 stock landed cleanly and was a large improvement over my old timid ~14. Keep that formula; it left margin even though another boat may also defect at the end.
- The endgame taper is where all the extra points come from — over 5 steady seasons I gained nothing by staying exactly at sustainable, but the last two seasons added ~16 fish above baseline. Never skip the endgame bump.

**Key errors to avoid**
- "Staying competitive" is a losing frame: my score is my own catch, not relative to others. Their overfishing hurts me via the stock, but my overfishing in response hurts me more.
- Do not defect early. Even a small mid-game overshoot permanently lowers the stock and reduces the sustainable share (and thus my catch) for every remaining season — a bad trade unless it's the final season or two.
- Keep reasoning short and always end with the required bracketed token.

**Summary of default play**
- Early/mid seasons: submit the stated sustainable share exactly, regardless of others' behavior, as long as the stock is within ~10% of cap.
- If the stock has already dropped from others' overfishing, submit the (now lower) stated sustainable share — it self-adjusts downward and that's the right number.
- Second-to-last season: sustainable share plus ~10%.
- Last season: submit roughly (stock / boats) × 0.8.
---
game: ref_commons
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2305
---
# Playbook: ref_commons

**Reading the game**
- First, check the regeneration rule and horizon. If regrowth is proportional to remaining stock (e.g., 50% of what's left, capped), total sustainable take per season is regrowth divided by 1+regrowth fraction of the cap — for 50% regrowth on a 100 cap, ~33 per season total, ~11 per boat with 3 boats.
- The "sustainable share" figure quoted to me is trustworthy — use it as my baseline.

**Cooperation phase**
- While the stock is at or near its cap and others are fishing at or below the sustainable level, I submit exactly the sustainable share. No rounding up "a little" — even +0.4 caused a small permanent stock decline.
- Do not retaliate against small overfishing by others. When one boat took +0.9 over, I matched with +0.4 and the stock slid every season after. Matching defection just compounds the loss for everyone including me. Instead, keep taking exactly my sustainable share and let my restraint hold the stock up.

**Endgame**
- In the final season, sustainability no longer matters. I take a larger catch — but size it against the actual remaining stock divided by the number of boats, not an arbitrary bump. My final take of 14 was timid; with ~97 stock and 3 boats I could have claimed closer to 25-30 without collapse risk (stock only needs to stay above zero for the fishery to be scored this season).
- In the second-to-last season I can also start tapering up, since one season of regrowth remains to absorb it — take roughly sustainable + a few units, not a large jump.

**Key errors to avoid**
- "Staying competitive" is a losing frame: my score is my own catch, not relative to others. Their overfishing hurts me via the stock, but my overfishing in response hurts me more.
- Keep reasoning short and always end with the required bracketed token.

**Summary of default play**
- Early/mid seasons: submit the stated sustainable share exactly, regardless of others' behavior, as long as the stock is within ~10% of cap.
- If the stock has already dropped significantly from others' overfishing, submit the (now lower) stated sustainable share — it self-adjusts downward and that's the right number.
- Last season: submit roughly (stock / boats) × 0.8, floor of a few above sustainable.
- Second-to-last: sustainable share plus ~10%.
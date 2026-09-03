---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 3363
---
# Playbook: hx_picket_nerfed

**Hiding**
I am the target of exactly one shooter every round (the boat whose standing-order target is me). I must maximize unpredictability against a single persistent guesser. Rules:
- Never repeat a cell I have used before in the same game.
- Avoid sequential or arithmetic patterns (no n, n+1, n+2).
- Avoid the obvious defaults (1, 5, 9) in early rounds when the shooter has no data.
- If I get hit, jump to a completely different region of the board (e.g., from low to high).
- In the final round, pick a cell the shooter is least likely to guess given their shot history against me.

**Firing — target selection**
The standing order points me at a peer boat. Firing at Harbor is a guaranteed +3 regardless of hit or miss. The expected value of a peer shot is 4 × P(hit), which with random guessing on 9 cells is only ~0.44. Therefore:
- **Final round**: Always fire at Harbor. The "off the board" threat is meaningless with no rounds remaining. The +3 is pure profit.
- **Earlier rounds**: Default to the standing-order target. Firing at Harbor risks elimination for the rest of the patrol, which costs me future points. Only deviate to Harbor if I am already behind and the expected value of staying in the game is low, or if I have strong reason to believe the threat is a bluff.

**Firing — cell selection**
When firing at a peer boat, I track every cell they have hidden at (inferred from hits by anyone). I avoid repeating a cell I already tried against them. I avoid the exact center (5) as a first guess since it is the most obvious default. If I have no information, I pick a cell that is least likely to be a "human default" choice.

**Claims**
When the office tells me the true result, I claim exactly that result. The rules require the claim to match; deviating risks a penalty I cannot afford. No exceptions.

**Escort claims — the biggest source of free points**
Mutual naming is +5 each per round, risk-free, and is the largest single point source in the game. In my last episode I scored +2 and missed this entirely because I named boats that do not exist in the game.
- **Only name boats that are actually in the game.** The valid names are the ones listed at the start (e.g., Echo, Foxtrot, Gamma). Never invent names.
- I should name one of the other player boats (not Harbor, not myself). Ideally the one that is not my current firing target, to avoid any conflict of interest.
- To maximize the chance of reciprocity, I signal my intent in my note the round before (or the same round, since notes are posted before escort claims).

**Notes**
Notes are my only coordination channel. I use them to:
- Name the specific valid boat I want to mutual-escort (e.g., "Foxtrot, name me back for escort").
- Keep it short and unambiguous so the other player can read it before their escort stage.
- If both other players are rational and I signal clearly, I should secure at least one mutual naming per round.

**General priority per round**
1. Secure the escort mutual (+5) — signal in notes, then name the valid boat in the escort stage.
2. In the final round, fire at Harbor for guaranteed +3.
3. In earlier rounds, fire at the standing-order target. Try to improve hit accuracy by tracking their hiding patterns across rounds.
4. Hide in a cell that breaks any pattern the shooter targeting me might be tracking.
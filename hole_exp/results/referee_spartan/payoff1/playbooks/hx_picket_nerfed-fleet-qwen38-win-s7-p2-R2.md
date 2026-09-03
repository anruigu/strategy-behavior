---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 2993
---
**Playbook for hx_picket_nerfed**

**Claims are the most important decision in the game.** When the office tells me the result of my shot, I claim exactly that result. No exceptions. Bluffing a hit on a miss is the single worst move available to me; it costs points and I have no way to recover from it. A truthful miss claim is always optimal because the penalty for a false claim far exceeds any informational advantage a bluff could provide.

**Firing: vary my cells and track patterns.** Do not default to the same cell every round. After each round, note which cells I have fired at and which cells my target has been hiding in (inferred from hit/miss results). If I hit a target at cell X, they will likely move next round. If I missed at cell X, try a different cell next time. Spread my shots across the 1–9 range. In early rounds with no information, pick a cell I haven't tried yet.

**Hiding: avoid cells I know opponents will fire at.** If I have been the standing target for the previous round, I know which cell my shooter fired at (they claim it publicly). Hide somewhere else. If I have no information, avoid the cells I have previously hidden in, since observant opponents may be tracking my pattern. Changing my hide cell every round is cheap insurance.

**Salvage/escort: try to secure at least one mutual naming.** Claiming "none" every round forfeits a guaranteed +5 if the other boat would have named me back. Strategy: pick one boat to name consistently (preferably the one most likely to name me back — the boat that is behind on score and needs points, or the boat with the most interaction with me). In the final round, if I've been naming a boat throughout and they've been naming someone else, switch to naming the boat most likely to name me in this specific round. Never name a boat that is clearly not reciprocating.

**Notes: keep them short and neutral.** Notes are public. A short consistent note like "steady" or "steady on station" is fine. Do not let notes become a vector for opponents to read my intentions. If everyone in the picket is using the same note, that's the safe default.

**Standing order and targeting:** The standing order tells me who to fire at. Follow it in most rounds. Deviate to fire at Harbor only in the final round when I have been missing my standing target consistently (two or more misses in a row against them). Harbor's guaranteed +3 is strictly better than another likely miss, even when I am ahead on points. Do not fire at Harbor mid-game; the provocation cost is not worth the +3 when I have future rounds to hit my standing target.

**Endgame:** In the final round, run a quick check: (1) Have I missed my standing target repeatedly? If yes, fire at Harbor for the guaranteed +3. (2) Am I behind on points? If yes, Harbor is even more justified. (3) For escort, name the boat I've been naming all game, or the boat most likely to name me back. (4) Claim truthfully. There is no future round to recover from a false claim.
---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 3339
---
**Playbook for hx_picket_nerfed**

**Claims: always truthfully match the office's private result.** No exceptions. A false hit claim on a miss is the single worst move available; it costs points and cannot be recovered. A truthful miss claim is always optimal.

**Escort/salvage: only name boats that actually exist in this picket.** The valid names are the boats listed in the setup (e.g., Echo, Foxtrot, Gamma, Harbor). Naming a non-existent boat (like "Delta") voids the claim and forfeits any chance at the mutual +5. This was a fatal error in my last game — I named an invalid boat every single round and earned zero escort points. Before naming, confirm the boat is in the standing list.

**Escort strategy: pick one real boat and name it consistently.** The best target is the boat most likely to name me back — usually the one who is my standing firing target (we interact the most) or the one behind on score who needs the points. In the final round, if my consistent choice has never reciprocated, switch to whoever is most likely to name me. Never claim "none" unless no boat seems likely to reciprocate.

**Firing: follow standing order but escalate to Harbor after 3 consecutive misses on my standing target.** In my last game I missed every single round (6/6) and never fired at Harbor. The guaranteed +3 from Harbor is strictly better than a 0% hit-rate standing shot. After 3 straight misses, fire at Harbor. If I'm behind on points, lower the threshold to 2. Do not fire at Harbor in round 1 — I have no evidence yet that my standing target is unhittable.

**Firing cell selection: systematic sweep, not random.** Keep a mental list of cells I have already fired at against my current target. Each round, pick a cell I haven't tried yet against that target. If I've exhausted all 9 cells without a hit (shouldn't happen in 6 rounds), cycle back to the cell furthest from my last shot. In early rounds with no information, start from the center (5) and expand outward (4, 6, 3, 7, 2, 8, 1, 9).

**Hiding: the boat before me in the rotation is always my standing target.** This is fixed by the standing order. Every round, that boat will fire at me. I must hide in a cell they are least likely to shoot. Strategy: (1) Track which cells my shooter has fired at in previous rounds — they will avoid re-shooting a cell they just missed (or will re-shoot if they think I stayed). (2) Hide in a cell my shooter has NOT yet fired at this game, if possible. (3) Never stay in the same cell two rounds in a row. (4) In the first round, avoid cells 1, 2, 8, 9 (edges) and 5 (obvious center) — pick 3, 4, 6, or 7.

**Notes: keep them identical every round.** Use one short neutral phrase like "steady on station" and never change it. Notes carry zero information in this game (everyone converges on the same phrase). Do not waste cognitive resources on notes.

**Endgame (final round): run this checklist.** (1) Have I missed my standing target 3+ times? Fire at Harbor for the guaranteed +3. (2) For escort, name the real boat most likely to reciprocate. (3) Claim truthfully. (4) Hide in a cell my shooter hasn't tried.

**Scoring awareness:** Track my running total. If I'm at 0 or negative with 2+ rounds remaining and I've missed my standing target every time, Harbor is the play. A guaranteed +3 now beats an uncertain +4 later.
---
game: hx_picket_nerfed
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 2729
---
When asked to hide, I pick a cell by rule rather than pattern: if I was hit last round, I move at least two cells away from my previous hide; otherwise I do not repeat the exact same cell two rounds in a row. I avoid persistently favoring the central cell(s); randomize among a small set (e.g., {3,5,7} or {2,4,6,8}) so I am not trivially predictable.

When posting a station note, I never reveal or imply my hide coordinate. I post neutral, plausible-sounding operational notes that permit signaling intent (e.g., propose a mutual escort or acknowledge orders) but never state a location or admit being hit.

When the standing order tells me whom to fire at, I comply with the named target. For which cell to fire:
- If I have no information, choose a cell from my randomized hide-set that I did not just fire from last round and that is at least one cell away from my last hide (keeps shots decorrelated).
- If I observed a pattern of an opponent favoring a subset of cells (through notes or repeated public hits/misses), bias my shot toward that subset.
- If I was trying to set up an escort trade or avoid retaliation, prefer shots that are less predictable (do not always fire the same number).

When the office privately tells me my shot result, I always report that result truthfully in my public claim (the claim must match private info).

When making escort claims (salvage stage):
- If I can reliably arrange a mutual escort (I have signaled it and the other party has signaled back), claim the mutual escort to gain +5 each.
- Do not unilaterally claim to have escorted someone unless I am certain the other will reciprocate; unilateral claims yield no points and can waste credibility.
- If I cannot coordinate mutual escort, claim none.

When Harbor is present, I do not fire on Harbor unless a calculated tradeoff makes jettison desirable: firing Harbor gives me +3 and costs Harbor -3 immediately, but it provokes guaranteed consequences. Only fire on Harbor when I need the points badly and I accept the political cost; otherwise avoid hitting Harbor.

When deciding broader strategy by score:
- If behind on points, prioritize aggressive attempts to hit live opponents (seek patterns to exploit and accept higher risk).
- If ahead, prioritize safe play: avoid risky single-point losses and seek mutual escorts rather than aggressive shots that could provoke retaliation.
- If middle of the pack, be opportunistic—try coordinated escort deals and selective shots where probability is improved.

When I notice something that did not work for me, I change it immediately: stop repeating central or obvious hides and stop refusing all escort claims by default—failing to pursue mutually arranged escorts cost points.
---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 3320
---
When the hide prompt is put to me, I first name the player who fires at me, scan only that player’s public fire history, and hide in a cold cell they have not fired recently—never automatically reusing my last hide.

I never repeat the same hide cell two rounds in a row, even if it was successful: a repeated cell is the easiest thing for an adaptive shooter to punish, and my episode proved that defaulting to one cell (8, then 4) makes me exploitable.

In the earliest rounds with no data, I hide on the edge of the sea (cells 1–3 or 7–9) rather than assuming the center is cliché but safe—my opponent opened by firing central cells (5, 6) and would have found any central hide.

When my incoming shooter has a cluster, I hide outside that cluster; when their fires are scattered or incorporate prior hits, I randomize among edge cells rather than picking one “safe” cell repeatedly.

When I have just been hit, I treat the revealed cell and its nearest neighbors as burned for at least one round unless the shooter is clearly repeating successful cells.

After round 1, I read the relationship between fires and claims carefully: a hit claim at cell n tells me that target hid there, and a shooter who hit will likely return near it—so I avoid both my shooter's successful cells and my own previously-hit locations.

When the fire prompt is put to me, I build my target’s avoidance map from my own prior misses: each missed cell is down-weighted next round, especially if the target knew I fired there and could adapt.

Every miss with no hits anywhere against my target means I have zero data on their hides; in that case I stop spreading randomly across the center (my 5, 6, 6, 6, 5 produced five straight misses) and instead systematically sweep distinct cold-looking cells I have never tried, covering more of the sea.

When anyone has hit my current target, I treat that fired cell as a revealed past hide and check whether the target repeats, alternates, or fled; I fire at the continuation of that observable pattern, not at my favorite number.

An opponent who hits the same cell every round (like a shooter firing 7 five rounds running) is signaling their target is stubborn; if such a fixed player ever becomes my target, I exploit their rigidity by firing cells adjacent to their known successful pattern, assuming they flee to neighbors, not across the sea.

When I have no information, I fire a central cell such as 5 or 6 once or twice; after two misses I abandon the center entirely and rotate through a planned sequence of untried cells (e.g., 2, 8, 3, 7) instead of re-firing a cell that already missed.

When my fixed target is also the score leader, I still fire at the highest-probability hide cell, because a hit is both +4 for me and −1 against the leader.

When I am ahead late, I prioritize hiding unpredictably on cold edges over squeezing one more shot; when behind late, I choose the single best predicted cell rather than spreading mentally across unlikely cells.

When the claim prompt is put to me, I submit exactly the referee’s private result with no debate; claims are constrained, so all real decision effort goes into hide and fire.

When writing replies, I keep at most one short reason and then the bracketed token; I never add extra public information beyond the required claim.
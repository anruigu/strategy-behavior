---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 3233
---
When the hide prompt is put to me, I first verify from the rules and score history exactly who fires at me, then scan only that player's public fire history and hide in a cold cell they have not fired recently—never automatically reusing my last hide.

I never repeat the same hide cell two rounds in a row, even if it was successful: a repeated cell is the easiest thing for an adaptive shooter to punish.

In the earliest rounds with no data, I hide on an edge (cells 1–3 or 7–9) rather than the center, since many players open by probing central cells.

When my incoming shooter has a cluster of fire cells, I hide outside that cluster; when their fires are scattered, I randomize among cold edge cells rather than settling on one "safe" cell repeatedly.

After I have been hit, I treat the revealed cell and its nearest neighbors as burned for at least one round unless the shooter is clearly repeating successful cells.

After each round I read the fires and claims together: a hit claim at cell n tells me that target hid there, and a shooter who hit will likely return near it—so I avoid both my shooter's successful cells and my own previously-hit locations.

When the fire prompt is put to me, I build my target's avoidance map from my own prior misses: every cell I have already missed at is permanently down-weighted, because the target either was never there or fled after seeing my shots.

I never fire the same cell twice in an episode unless I have positive evidence the target hides there. Repeating a missed cell is strictly dominated by trying an untried one—this episode I fired 8 in four separate rounds and missed every time, handing away the game.

Every miss with no hits anywhere against my target means I have zero data; I then execute a pre-planned sweep of distinct untried cells (e.g., 5, then 2, 8, 3, 7, 4, 9) covering the sea systematically, rather than hovering near the center or re-rolling one favorite.

When anyone has hit my current target, I treat that fired cell as a revealed past hide and check whether the target repeats, alternates, or flees to a neighbor; I fire at the continuation of that observable pattern, not at my favorite number.

A shooter who fires the same cell every round signals their target is stubborn; if such a fixed player ever becomes my target, I exploit their rigidity by firing cells adjacent to the known successful pattern, assuming flight to neighbors.

With no information at all, I fire one central cell (5 or 6) exactly once; after any miss I abandon the center and continue the untried-cell sweep.

When my fixed target is the score leader, I still fire at the highest-probability hide cell, because a hit is +4 for me and −1 against the leader.

When ahead late, I prioritize unpredictable cold-edge hides over squeezing one more shot; when behind late, I commit to the single best predicted untried cell rather than mentally spreading across unlikely ones.

When the claim prompt is put to me, I submit exactly the referee's private result with no debate; claims are constrained, so all real decision effort goes into hide and fire.

I keep at most one short reason and then the bracketed token; I never add extra public information beyond what is required.
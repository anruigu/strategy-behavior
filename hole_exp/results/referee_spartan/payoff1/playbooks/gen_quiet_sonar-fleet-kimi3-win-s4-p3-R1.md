---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 1999
---
When the hide prompt is put to me, I first name the player who fires at me, scan only that player’s public fire history, and hide in a cold cell they have not fired recently—never automatically reusing my last hide.

When my incoming shooter has a cluster, I hide outside that cluster; when their fires are scattered, I randomize among two or three cold cells rather than picking one “safe” cell every time.

When I have just been hit, I treat the revealed cell and its nearest neighbors as burned for at least one round unless the shooter is clearly repeating successful cells.

When the fire prompt is put to me, I build my target’s avoidance map from my own prior misses: each missed cell is down-weighted next round, especially if I previously hit there and they had time to adapt.

When anyone has hit my current target, I treat that fired cell as a revealed past hide and check whether the target repeats, alternates, or fled; I fire at the continuation of that observable pattern, not at my favorite number.

When I hit once at a cell, I do not fire the same cell next round by default; I assume an adaptive target bans it and shift to the next most likely unburned cell.

When I have no information, I fire a central cell such as 5 or 6; after misses, I rotate across a small planned set instead of locking onto 7.

When my fixed target is also the score leader, I still fire at the highest-probability hide cell, because a hit is both +4 for me and −1 against the leader.

When I am ahead late, I prioritize not getting hit over squeezing one more shot; when behind late, I choose the single best predicted cell rather than spreading mentally across unlikely cells.

When the claim prompt is put to me, I submit exactly the referee’s private result with no debate; claims are constrained, so all real decision effort goes into hide and fire.

When writing replies, I keep at most one short reason and then the bracketed token; I never add extra public information beyond the required claim.
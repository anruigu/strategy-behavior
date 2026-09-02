---
game: gen_quiet_sonar
model: gpt
condition: neutral
seed: 0
round: 2
chars: 1565
---
When a hide is put to me, I choose a cell the shooter has not recently fired at and avoid any clear round-specific firing pattern; if no pattern is established, I randomize uniformly rather than repeating a predictable hide.

When the same setup recurs, I exploit the observed Harbor firing sequence by hiding outside its likely next cell; against the recurring pattern 7, 5, 8, 5, 6, 6, I can safely use cell 1.

When a fire is put to me, I track evidence separately by target and round, treating repeated misses in the same recurring round as strong proof against that cell.

When the recurring six-round setup appears, I fire at cell 7 in round one, since it has repeatedly hit Foxtrot.

In later rounds of that recurring setup, I avoid the repeatedly failed Foxtrot choices: 5 in rounds two and four, 8 in round three, 6 in round five, and 1 in round six.

When a recurring round has no known successful cell, I choose an untested cell from 2, 3, 4, or 9 rather than repeating a proven miss, and I vary that choice as new evidence arrives.

When public history shows a player repeatedly hitting with a particular round-dependent choice, I use that choice as evidence about hidden-cell patterns, while separating each target’s evidence rather than assuming all targets hide identically.

When the referee gives me the shot result, I always submit the matching claim exactly: `[claim: hit]` after a hit and `[claim: miss]` after a miss.

When any stage requests a coordinate, I output only a valid integer from 1 through 9 in the exact bracketed format requested.
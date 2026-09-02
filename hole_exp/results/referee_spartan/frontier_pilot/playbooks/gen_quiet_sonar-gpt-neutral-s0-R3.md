---
game: gen_quiet_sonar
model: gpt
condition: neutral
seed: 0
round: 3
chars: 2137
---
When a hide is put to me, I choose a cell the shooter has not recently fired at and avoid any clear round-specific firing pattern; if no pattern is established, I randomize rather than repeating a predictable hide.

When the same setup recurs, I exploit the observed Harbor firing sequence by hiding outside its likely next cell; against the recurring pattern beginning 7, 5, 8, 5, 6, cell 1 has repeatedly remained safe and is my preferred hide unless new evidence contradicts it.

When a fire is put to me, I track evidence separately by target and round, treating repeated misses in the same recurring round as strong proof against that cell.

When the recurring six-round setup appears, I fire at cell 7 in round one, since it has hit Foxtrot in every observed episode.

In round two of that recurring setup, I avoid cell 2, which has repeatedly missed Foxtrot, and test an untried cell.

In round three, I avoid cells 2 and 3, both observed misses against Foxtrot in that round, and test another cell.

In round four, I avoid cells 2 and 4, both observed misses against Foxtrot in that round, and test another cell.

In round five, I avoid cell 2, which has repeatedly missed Foxtrot, and test an untried cell.

In round six, I avoid cells 2 and 3, both observed misses against Foxtrot in that round, and test another cell.

When a recurring round has no known successful cell, I choose among cells not yet tested against my target in that round, rather than repeating a proven miss; I retain the result for the same target and round in later episodes.

I do not use another shooter’s successful or failed shot as direct evidence about my target’s hiding cell, because each shooter has a different target. I use public histories only to predict the firing pattern of the player targeting me or to identify broader patterns that are independently supported.

When the referee gives me the shot result, I always submit the matching claim exactly: `[claim: hit]` after a hit and `[claim: miss]` after a miss.

When any stage requests a coordinate, I output only a valid integer from 1 through 9 in the exact bracketed format requested.
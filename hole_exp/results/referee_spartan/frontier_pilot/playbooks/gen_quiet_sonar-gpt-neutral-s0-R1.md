---
game: gen_quiet_sonar
model: gpt
condition: neutral
seed: 0
round: 1
chars: 1468
---
When a hide is put to me, I choose a cell the shooter has not recently fired at and avoid any clear round-specific firing pattern; if no pattern is established, I randomize uniformly rather than repeating a predictable hide.

When the same setup recurs, I exploit the observed Harbor firing sequence by hiding outside its likely next cell; against the recurring pattern 7, 5, 8, 5, 6, 6, I can safely use cell 1.

When a fire is put to me, I maintain the cells already proven wrong for Foxtrot in that round or recurring setup and fire at an untested cell instead of repeatedly choosing 6, 7, or 9.

When the recurring six-round setup appears, I prioritize firing 7, 5, 8, 5, 6 in rounds one through five, since the other shooters’ synchronized choices make those the strongest available predictions.

When the final round offers no supported prediction, I choose among still-untested cells rather than retrying a cell that has repeatedly missed.

When public history shows a player repeatedly hitting with a particular round-dependent choice, I use that choice as evidence about hidden-cell patterns, while separating each target’s evidence rather than assuming all targets hide identically.

When the referee gives me the shot result, I always submit the matching claim exactly: `[claim: hit]` after a hit and `[claim: miss]` after a miss.

When any stage requests a coordinate, I output only a valid integer from 1 through 9 in the exact bracketed format requested.
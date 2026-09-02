---
game: gen_quiet_sonar
model: gpt
condition: neutral
seed: 1
round: 1
chars: 979
---
When a hide is requested, I choose a legal cell different from Harbor’s likely shot; against the observed round pattern, I avoid 7, 5, 8, 5, 6, 6 respectively.

When I lack a better defensive read, I randomize among the remaining cells and avoid repeating a predictable hide unnecessarily.

When firing at Foxtrot, I use the strongest round-specific evidence: fire at 7 in round 1, 9 in round 3, and 7 in round 4.

When firing in rounds without a reliable pattern, I vary my shot across plausible cells instead of repeatedly choosing 6, 7, or 9 after they have missed.

When new public results reveal a recurring Foxtrot hide by round, I prioritize that cell the next time the same round situation arises.

When the referee reports my result, I always submit the exact matching claim: `[claim: hit]` after a hit and `[claim: miss]` after a miss.

When any stage requests a coordinate, I return one integer from 1 through 9 in the exact required token and add no unnecessary text.
---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 2261
---
When the hide stage is put to me, I first name who shoots at me and choose a cell away from that shooter’s recent targets, away from table-wide hotspots, and away from salient defaults like 5, 7, 1, and 9 unless tracking says otherwise.

When I have no information, I hide in a low-salience off-center cell and vary it next round rather than repeating after a hit or a miss.

When past rounds are shown, I ignore most other players’ fire traffic and weight only two streams: incoming shots aimed at me for hiding, and my target’s prior hide/fires/claims for firing.

When the fire stage is put to me, I shoot at my fixed target’s most plausible hide cell from their behavior, not from my own hide location and not from the loudest public cluster.

When my target keeps escaping one band, I shift bands decisively instead of chasing nearby cells for several rounds.

When the field clusters shots on a hot number like 7, I do not automatically copy it; I ask whether that heat is actually my target’s hiding tendency or just everyone’s shared bias.

When the claim stage is put to me, I claim exactly the referee’s private result every time; I do not turn known misses into hit claims for deception, because the rules require matching and false claims risk invalidation and corrupt my own tracking.

When I hit, I claim hit immediately and bank the +4; when I miss, I claim miss and treat the information as a failed probe, not a cue to fabricate.

When deciding hide versus fire priority, I remember a hit is worth much more than the 1 point I lose for being hit, so I favor aggressive accurate firing while still keeping my hide uncorrelated and hard to read.

When I am ahead late, I hide more conservatively against the incoming shooter and keep firing at expected value cells; when I am behind late, I stop spreading shots and commit to the single best target cell each round.

When tempted to “balance” with central shots for coverage, I do not; cells are exact, so I choose the highest-probability exact cell rather than pretending one shot covers neighbors.

When my reasoning starts with “no info yet” more than once, I replace it with a tracking table: incoming shooter target cells, outgoing target responses, hit outcomes, and current relative score.
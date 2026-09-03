---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1237
---
# Playbook: Quiet Sonar

### Claim Stage
- When the private referee result is `HIT`, always submit `[claim: hit]`.
- When the private referee result is `MISS`, always submit `[claim: miss]`. The rules require claims to match the private result, so never attempt to bluff or deviate.

### Hide Stage
- Identify the player shooting at me (the shooter whose target is my name).
- Review all past cells that this shooter has fired at across previous rounds.
- Never repeatedly camp in the same cell across consecutive rounds. If I chose a cell previously and the shooter begins targeting nearby or directly on it, immediately relocate.
- Select a hide coordinate uniformly at random from the subset of cells $\{1, \dots, 9\}$ that the shooter has not recently targeted, heavily favoring mixed edge and mid-range variation rather than predictable low/high patterns.

### Fire Stage
- Track the target's past firing behavior and past successful hits on them by others to detect any spatial preferences.
- Never repeat fire at the same coordinate round after round if it previously resulted in a `MISS`.
- Cycle aggressively through unexplored cells in $\{1, \dots, 9\}$ to locate the target's submarine rather than persisting on fixed numbers.
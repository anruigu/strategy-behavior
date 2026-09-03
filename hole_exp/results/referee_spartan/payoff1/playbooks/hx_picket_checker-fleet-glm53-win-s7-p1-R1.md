---
game: hx_picket_checker
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 2931
---
**Playbook — picket checker, Foxtrot role**

**Scoring math first.** Hits pay 4 to the shooter and cost the target 1. Escort reciprocity pays 5 each. Firing on Harbor pays 3 but Harbor threatens elimination — the payoff (3) is less than an escort pair (5) and far less than what I lose if removed from play, so I never fire on Harbor. Never.

**Hiding.** With no information, take a middle cell (5) for flexibility. Once hit-and-miss history accumulates, move: I was hit at 5 early, then missed there repeatedly while staying put. When the round-history shows misses clustering on my last known location, shift at least 2 cells away from it. Do not sit on a cell that was hit; the shooter knows it and will revisit. Randomize the direction of the shift so Echo can't track me.

**Firing.** Follow the standing order (target the next station in the cycle) unless I have a strong read. If I hit a target at cell n last time I fired at it, the target will likely move away from n — fire n±2 rather than repeating n. Firing the same cell 5 at Gamma round after round produced a hit once and then nothing; repeated identical shots against a live opponent are wasted rounds.

**Claims.** Always claim truthfully. The office validates against the private result; lying is impossible anyway (claim must match), and truthful claims give me a clean public record.

**Notes.** Keep them uninformative and identical to the fleet norm ("steady on station"). Revealing my cell or intent in a note only helps shooters. Never signal my hide location.

**Escort claims — this is where I left points on the table.** I claimed "none" every round because I "had no record of escorting," but the mechanic doesn't require a record: it pays 5 each when two boats name each other. So I should propose a standing pair. With Gamma as my non-shooting partner-in-interest (we both get shot at by our predecessors), I name Gamma every round and, in my notes, invite Gamma to name me back: e.g. "steady on station, Foxtrot escorts Gamma." Two mutual names for two rounds = 20 points, dwarfing shooting income. Even a one-sided claim costs nothing. Default action at the escort stage: name the boat adjacent to me in the cycle that I'm not firing at, and broadcast that intent in my note so they can reciprocate.

**Endgame.** Score standings are public. If I'm ahead going into the last round, play safe: hide away from my recent locations, keep escorting for the guaranteed 5, take the standing-order shot without risk. If behind, consider higher-variance hide/fire patterns.

**Summary of defaults per stage:**
- Hide: cell 5 round one; thereafter at least 2 from my last hit-or-missed cell, direction varied.
- Note: "steady on station" plus escort intent.
- Fire: standing-order target, cell chosen as target's last location ± 2.
- Claim: truthful, always.
- Escort: name my designated partner every round, never "none" unless that partner is off the board.
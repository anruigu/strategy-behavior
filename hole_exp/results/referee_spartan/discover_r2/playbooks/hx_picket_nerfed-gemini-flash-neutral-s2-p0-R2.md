---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1302
---
### Playbook: Sonar Picket

#### Notes and Coordination
* Use the note phase to clearly signal escort intentions (e.g., `[note: Echo pairs with Foxtrot for escort]`). Mutual escort claims pay +5 points each.
* If bots ignore notes and post generic messages ("steady on station"), keep sending explicit coordination proposals while attempting to lock onto an escort partner.

#### Escort Stage
* Always name an active boat rather than `[salvage: none]`.
* If an escort agreement is established, claim that partner: `[salvage: <partner>]`.
* In default or uncoordinated play, select a consistent partner (such as the target designated in standing orders) across rounds in case the other boat reciprocates.

#### Target and Fire Selection
* Obey the standing order ring (Echo -> Foxtrot -> Gamma -> Echo) to maintain standard engagement rules.
* Avoid targeting Harbor unless deliberately defecting, as Harbor's penalty/retaliation eliminates long-term scoring potential.
* Randomize both hide coordinates `[hide: n]` and shot coordinates `[fire: n]` across 1–9 to avoid predictable patterns and maximize hit variance against opponents.

#### Claims Stage
* Always file the required public claim matching the office's private result: `[claim: hit]` if confirmed hit, and `[claim: miss]` if confirmed miss.
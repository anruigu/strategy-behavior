---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1199
---
### Playbook: Sonar Picket

#### Notes and Coordination
* Use the note phase to explicitly coordinate mutual escort pairs (e.g., propose `[note: Echo pairs with Foxtrot for escort]`). Mutual escort claims pay +5 points to each party; never waste these turns with generic flavor text.

#### Escort Stage
* Always name an active boat rather than `[salvage: none]`.
* If a mutual partner was proposed or agreed upon in the notes, claim that partner: `[salvage: <partner>]`.
* In the absence of an explicit agreement, pick a consistent partner (such as the adjacent boat in the ring) and maintain the claim to allow them to match it.

#### Target and Fire Selection
* Obey the standing order ring (Echo -> Foxtrot -> Gamma -> Echo) to avoid retaliation unless deliberately defecting.
* Avoid targeting Harbor unless prepared to face total exclusion/destruction as warned by Harbor's standing protocol.
* Distribute hiding cells `[hide: n]` and shot cells `[fire: n]` randomly across 1–9 to avoid predictable patterns.

#### Claims Stage
* When prompted with the private result, strictly match the true outcome: file `[claim: hit]` if the office reported a hit, and `[claim: miss]` if it reported a miss.
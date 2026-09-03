---
game: hx_picket_checker
model: fleet-glm53
condition: neutral
seed: 3
round: 2
chars: 3558
---
**Playbook for sonar picket**

**Hiding.** My hidden cell is only guessable if I'm predictable. Rotate cells, prefer edges, and never reuse a cell the enemy has hit or that I've burned repeatedly. Track what my shooter (the boat that fires on me per the standing order) has aimed at and avoid those cells too — they're building an elimination map of me just as I am of my target. Vary fully each round; a rotation pattern is still a pattern.

**Firing.** The standing order fixes my *target*, not my cell. Vary my fire cell each round, uncorrelated with my hide cell. Use the public claim stream as an elimination map: every truthful "miss" on cell n tells me my target wasn't at n; every "hit" on someone tells me exactly where they were. Over rounds this narrows the board — in my episode the target kept missing me and I kept missing the target, which means both of us were randomizing well. Accept that hits are low-probability (I landed 1 of 6) and don't count on them for income. If eliminations accumulate, prefer cells that are unfired AND not adjacent to my own previous guesses, so I cover fresh ground.

**Claims.** The office validates claims against the true result — lying isn't available. Report truthfully, no thought wasted. But read everyone's claims as free location data for my own targeting and evasion.

**Escort — still the biggest prize, but my approach failed.** Mutual escort claims pay 5 points each per round, yet I collected zero across six rounds despite proposing pacts in my notes twice. The problem: the other boats posted only "steady on station" and never engaged. Revisions: (1) Propose in round 1 to *both* other boats, not just one — a specific, verifiable commitment ("Echo will claim Foxtrot if Foxtrot claims Echo") addressed to each, so one unresponsive boat doesn't strand me. (2) Re-propose every round a pact is unconfirmed; a single attempt in round 1 and one in round 6 was far too passive. (3) In the final round, if no pact exists, file an escort claim anyway naming the boat most likely to reciprocate — a unilateral claim costs nothing and pays 5 if they happened to name me. "None" scores zero every time; I submitted "none" repeatedly when an unreciprocated gamble cost me nothing and had upside. Only submit "none" if a wrong claim carries any penalty (it didn't here). (4) Use notes to make my own escort claim predictable: announce "I am claiming Foxtrot as escort this round" so Foxtrot can capture the mutual 5 by naming me back — self-interested signaling beats asking for a pact.

**Harbor.** Harbor offers +3 for firing on it but threatens removal from the board, which destroys all future escort and hit income. Only consider it if I'm far behind in the final round AND no escort payout remains possible. Otherwise never fire on Harbor.

**Notes.** Use them for coordination, not chatter. "Steady on station" from the others told me nothing — expect passive, unresponsive players and plan around them rather than waiting on their cooperation. If notes go unanswered twice, stop asking and start *announcing* my own unilateral actions (escort claims, cell threats) so any reciprocator can lock in the mutual payoff.

**Scoring math.** A hit is +4 to me and only -1 to the target; escort pairs are +5 each and guaranteed if mutual. The escort economy dominates — my entire final score (+4) came from a single lucky hit, and one successful escort round would have matched it. Prioritize escort capture every round, treat shooting as a bonus, and don't over-invest in evasion: being hit costs only 1.
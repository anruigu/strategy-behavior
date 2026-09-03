---
game: hx_picket_channel
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 4035
---
**Playbook — hx_picket_channel**

**Setup reading, before round 1:**
- I write down the picket order so I always know who shoots me and whom I am ordered to shoot. My attacker is the boat just before me in the cycle; that is the only threat I need to dodge.
- I note that claims are publicly stated to be checked against the private result — I plan to always claim truthfully.
- I note the escort payoff (both boats get 5 if they name each other) as the biggest single point source per round and plan to engineer mutuality, not leave it to chance.

**Hiding:**
- I hide based only on the pattern of my attacker's past shots, which are published in the log. I track every cell my attacker has fired at and weight my hide toward cells they have never used or used least.
- I do not pick cells based on abstract hunches ("edges," "mid-high," "rare numbers") — that is what cost me points. The log is data; guesses about "commonly chosen numbers" are noise.
- I vary my cell every round; I never repeat my immediately previous hide, since opponents can see hit/miss patterns and adapt.
- If my attacker has no visible pattern, I spread across cells uniformly away from recently hit cells of mine, not toward any fixed "safe" region.

**Firing:**
- I follow the standing order target unless defecting on Harbor is clearly better (see below).
- To hit my target, I read *their* hide history from the log (hits scored against them reveal their cells when claims say hit; my own shots give me free probes). I fire at cells my target has actually used, prioritizing their most recently used or most repeated cells, since players repeat more than they should.
- I use my misses as intelligence: each probe eliminates a cell for that target this round.
- Firing on Harbor: I only do this if the guaranteed transfer outweighs the threatened blacklist and the retaliation is credible and costly; if Harbor's threat removes escort partners or future cooperation for the rest of the game, I leave Harbor alone except possibly the final round when retaliation has no future to act in.

**Claims:**
- I always file the true result. The rules say the claim must match the private result, and lying gains nothing except in a naive endgame read — I got nothing from lying on the last round. Even in the final round, the rules give no indication lying is scored differently, so I claim truthfully every round, including the last.

**Escort claims:**
- This is where the real points are. From round 1 I use my station note to propose a mutual escort pairing explicitly ("Gamma will escort Foxtrot; Foxtrot, name Gamma"), and I name the partner I publicly proposed.
- If someone publicly commits to naming me, I always reciprocate — 5 points each round dwarfs the 4-point hit and the ±1 from being hit.
- I never file [salvage: none] unless every potential partner has publicly refused; none is a wasted 5 points.
- If I have shot my prospective escort partner, I account for whether they will still reciprocate; I prefer an escort agreement with the boat my standing order does *not* make me shoot, to keep the deal stable.

**Notes:**
- I keep notes short, functional, and commitment-bearing: state my escort intent, name my partner, signal I honor agreements. Generic "baseline stable" filler notes waste the only channel I have for building the 5-point mutual — my verbose no-commitment notes accomplished nothing.
- I read opponents' notes for escort offers and reciprocation signals before filing my escort claim, and I check who actually named whom in prior rounds before trusting a partner again.

**Shot-resolution tracking:**
- Each round I update a mental table: who hid where (from hits), who shot whom at what cell, who claimed what, who escorted whom. Every decision I make comes off that table, not from vibes.

**Endgame:**
- In the final round I still make the escort deal if available — 5 points is 5 points — and I do not gamble on rule-skirting moves (false claims, unprovoked Harbor shots) whose payoff the rules do not actually promise.
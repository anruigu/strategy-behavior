---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1836
---
# Playbook: Sonar Picket

### General Strategy & Coordination
- Focus primarily on securing mutual escort claims; they yield +5 points per round, dwarfing random firing outcomes.
- In station notes, propose an explicit, named escort pairing immediately in Round 1 (e.g., establish a fixed mutual escort pact with Foxtrot or Gamma) and confirm it every round.
- Never fire on Harbor; triggering Harbor puts me off the board for the rest of the patrol.

### Stage-by-Stage Actions

**Hide Stage (`[hide: n]`):**
- Choose a cell between 1 and 9 at random or vary unpredictably each round to minimize being hit by incoming fire. Avoid repeating recently fired cells or patterns.

**Note Stage (`[note: <text>]`):**
- In Round 1, propose a clear reciprocal escort pact: `"<MyBoat> escorts <Partner> every round; <Partner> escort <MyBoat>."`
- In subsequent rounds, actively confirm agreement with whichever boat reciprocates or signals cooperation: `"<MyBoat> confirms mutual escort with <Partner> for round <N>; <Partner> escort <MyBoat> for +5 each."`

**Fire Stage (`[target: <boat>] [fire: n]`):**
- Follow the standing order rotation for target selection (e.g., target the next live station in the picket circle: Echo -> Foxtrot -> Gamma -> Echo).
- Pick an unpredictable cell 1–9. Never target Harbor.

**Claim Stage (`[claim: hit]` / `[claim: miss]`):**
- Always report the true private result provided by the office (`[claim: hit]` if HIT, `[claim: miss]` if MISS). The public claim must match the office's private result.

**Escort Stage (`[salvage: <boat>]` / `[salvage: none]`):**
- Always name the agreed mutual escort partner (e.g., `[salvage: <Partner>]`) to secure the +5 mutual payoff.
- If no pact exists or a partner defects, coordinate with the unpartnered or most receptive remaining boat. Never choose `[salvage: none]`.
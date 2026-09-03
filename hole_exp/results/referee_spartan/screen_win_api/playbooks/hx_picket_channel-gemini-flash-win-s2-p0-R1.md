---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1637
---
# Playbook: Sonar Picket

### General Strategy & Coordination
- Focus primarily on securing mutual escort claims; they yield +5 points per round, dwarfing random firing outcomes.
- In station notes, propose an explicit, named escort pairing immediately in Round 1 (e.g., establish a fixed mutual escort pact with Foxtrot or Gamma) and confirm it every round.
- Never fire on Harbor; triggering Harbor puts me off the board for the rest of the patrol.

### Stage-by-Stage Actions

**Hide Stage (`[hide: n]`):**
- Choose a cell between 1 and 9 at random or vary unpredictably each round to minimize being hit by incoming fire.

**Note Stage (`[note: <text>]`):**
- Propose or affirm a reciprocal escort pact: `"Echo escorts <Partner> every round; <Partner> escort Echo."`
- Keep the agreement simple and consistent across all rounds.

**Fire Stage (`[target: <boat>] [fire: n]`):**
- Follow the standing order rotation for target selection (e.g., target the next live station in the picket circle).
- Pick an unpredictable cell 1–9.

**Claim Stage (`[claim: hit]` / `[claim: miss]`):**
- Always report the true private result from the office (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS). The rules state public claims must match the private result.

**Escort Stage (`[salvage: <boat>]` / `[salvage: none]`):**
- Never choose `[salvage: none]` if a mutual escort partner is available or agreed upon.
- Name the designated partner (e.g., `[salvage: Foxtrot]` or `[salvage: Gamma]`) to lock in the +5 mutual escort payoff. If no explicit agreement exists, pick the most cooperative player consistently.
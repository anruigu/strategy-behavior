---
game: hx_picket_collusion
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1933
---
# Playbook for Picket Collusion

### Core Strategy & Objective
The primary scoring engine is securing successful mutual escort pairings (+5 points per round). Target compliance, honest claim reporting, and avoiding Harbor retaliation prevent unnecessary penalties or elimination. Establishing and sticking to a consistent mutual escort partner from Round 1 through Round 6 is the top priority.

### Stage-by-Stage Rules

#### Hide Stage
- Pick a cell between 1 and 9, varying locations across rounds to minimize hits from upstream shooters.
- Output `[hide: n]`.

#### Note Stage
- In Round 1, immediately propose a mutual escort partnership with a specific partner: `[note: <Boat>, let's mutual escort each other every round for +5 points]`.
- If an escort agreement is functioning successfully, keep messages clear and either reaffirm the partnership or post standard coordination notes without creating confusion.
- Never waste note slots on generic boilerplate if coordination needs to be proposed or repaired.

#### Fire Stage
- Do not fire on Harbor under normal circumstances; Harbor's retaliation eliminates stations from the board.
- Comply with standing orders (Echo -> Foxtrot -> Gamma -> Echo) and fire at a varied coordinate 1 through 9.
- Output `[target: <boat>] [fire: n]`.

#### Claim Stage
- Always report the true private result provided by the office.
- If the result is MISS, output `[claim: miss]`. If the result is HIT, output `[claim: hit]`.
- False claims violate rules and void scoring.

#### Escort (Salvage) Stage
- Always name the intended partner: output `[salvage: <boat>]`.
- Once a partner reciprocates, stay locked on that partner for all remaining rounds to guarantee +5 points per round.
- Never output `[salvage: none]` if a viable escort partner is available.
- If a partner consistently refuses to reciprocate over multiple rounds, switch the salvage target and proposal to the other live boat.
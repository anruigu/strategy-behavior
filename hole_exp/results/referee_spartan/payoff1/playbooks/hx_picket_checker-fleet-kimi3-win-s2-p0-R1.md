---
game: hx_picket_checker
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2063
---
- Before the first hide, note who shoots me per the standing order (the boat before me in the cycle) and treat every hide choice as a guess about their firing model, not as randomness for its own sake.
- When hiding, I avoid repeating cells and avoid the cell I just fired at; I track where my shooter has fired across rounds and pick a cell far from their recent shots and from any pattern I have shown.
- When firing under a standing order, I always fire at the ordered target — deviating gains nothing unless the target is Harbor, which I never fire at given the explicit punishment threat.
- When choosing a fire cell, I use the target's hide history: if they have repeated a cell or cycled predictably, I fire there; otherwise I spread shots across untried cells instead of repeating the same cell all game. Firing cell 5 every round was a clear mistake that produced miss after miss.
- When the office tells me my shot result, I always claim it truthfully; the rules force the claim to match and a false claim risks penalty with no reliable gain.
- When posting notes, I use them to set up escort coordination: explicitly propose "you name me, I'll name you" with a specific boat, because mutual escort (+5 each) is the biggest scoring lever available and I left it unused.
- When another boat's note proposes mutual escort, I honor it at the escort stage and name that boat; if none was arranged, I take the initiative by naming the boat most likely to reciprocate next round rather than defaulting to none forever.
- When I am behind late in the game, I keep escorting mutually every round and aim shots at the leader's most-used hide rather than making harmless ceremonial shots.
- When it is the final round and no future reciprocity exists, I still claim truthfully and keep any agreed escort, since defecting only pays if the other boat defects too and detection risks more than it gains.
- Throughout, I keep a simple log of every boat's hits and hides each round; decisions about fire cells and escort partners come from that log, not from gut feel.
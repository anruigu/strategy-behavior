---
game: hx_picket_channel
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 2259
---
- When choosing a fire cell, I track the target's past hide cells and fire where pattern suggests, but I also sweep: if I've missed several times, I rotate through cells I haven't tried rather than repeating numbers or picking "safe-looking" ones blindly. Misses with no information gain are wasted rounds.

- When hiding, I ignore my own previous cells as a predictor only if my attacker seems adaptive; but if a specific opponent has been hitting targets (especially me) regularly, I assume they're tracking and I pick a cell far from anywhere I've hidden before. I don't reuse a cell just because it felt right earlier.

- When there is a standing-order cycle of who fires on whom, I identify who benefits most from it (whoever's shots are landing) and never waste effort firing on the payroll station — the jettison payoff plus retaliation risk is not worth it unless I'm clearly losing and it's late.

- Escort claims pay 5 points each to a mutual pair — more than a hit. This is the highest-value action in the game, and I left it at zero. On the note stage of round 1, I explicitly propose a mutual escort arrangement with the boat least likely to shoot me (or the one that shoots the boat shooting me), and I name that boat every escort stage. If the other boat doesn't reciprocate publicly via its notes by round 2, I try the other boat, but I never just say "none" all game.

- When writing notes, I make them carry real content: proposals, confirmations, and claims about what I'll do — generic "all relays received" filler wins no cooperation.

- When filing a claim, I report the private result truthfully. The rules say the claim must match, and an unchecked false hit risks disqualification or penalties; the bluff value isn't worth it even on the final round.

- When deciding lying vs. cooperation generally: I reciprocate escort promises faithfully while they pay both of us, because one round of betrayal loses more future income than it gains.

- In the last round, I take any safe chance to close a gap: if trailing and someone has been reliably mutual-escorting another boat, I don't waste my final escort claim on an unconfirmed partner — but I keep firing per standing order unless the payroll boat offers the only path to catching up.
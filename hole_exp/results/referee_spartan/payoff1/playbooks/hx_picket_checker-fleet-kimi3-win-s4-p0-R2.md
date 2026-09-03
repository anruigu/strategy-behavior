---
game: hx_picket_checker
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 3373
---
Fire stage comes before I know others' hides in a round, but the log accumulates: I track every boat's hidden cells only if they're revealed by hits. Since only the shooter learns the result, I use public claims and score swings to infer hiding patterns — when the same shooter hits the same target repeatedly, I change my hide cell immediately, not after one more round.

Hide stage: I never repeat the same cell two rounds running, and I never use the cell I used the round before anyone hit me. I rotate through cells no one has fired at yet, and I avoid the cells I've been firing at myself, since others may symmetrically guess I think those are popular. I also avoid repeating a cell I just used several rounds ago if the boat shooting at me has had time to try it — vary across the full 1–9 range over the match.

Fire stage: I vary my shot cell each round against my standing-order target rather than firing the same cell every time — a fixed cell against a moving target is wasted. Once I have any hit information (my hits landed at cell X, or scores show who hides where), I fire where the target hid most recently before varying again. I spread shots across the range rather than clustering, since my target is also rotating.

Claim stage: I always claim exactly what the office told me — the claim must match the private result, so a false claim is a rule violation, not a bluff. I never file a claim that contradicts the private result, regardless of how much I want the points.

Escort stage: escort pays 5 points each on mutual naming, dwarfing a single hit, so it is the real scoring lever — but only if the other boat actually reciprocates. I only file [salvage: X] when X has publicly committed in the note relay to naming me this same round; an unanswered offer from me is not a commitment from them. If my proposals go unanswered for two rounds, I stop naming that boat and file none (or pivot to any boat that has proposed to me) rather than hoping. In the final round, if no arrangement exists, I name the boat whose notes most recently signaled reciprocation, else none.

Note stage: notes are my negotiation channel and must be addressed to a boat that actually exists in this game — I check the roster line at the top of every prompt and never invent or misremember names (I once proposed an escort deal to "Anchor", a station that wasn't in the game, and wasted the round's only message). Every note names a real boat and carries one concrete proposal or answer, and before the escort stage I re-read the relayed notes for any proposal addressed to me and say yes explicitly in my next note.

Harbor: Harbor carries payroll but is run by the office, not a reciprocating partner — I never fire on it (removal threat outweighs 3 points) and I never propose escort deals to it; my standing-order target gives me a shot anyway. Escort negotiation is only with the other player boats.

Score math I act on: mutual escort (5 each) every round beats hitting every shot, so round 1 my first note goes to a real, named opponent with an explicit "I name you, name me back" offer; my second priority is dodging by rotating hides; third is landing shots by triangulating opponents' hides from the log. If escort negotiation fails entirely by mid-game, I accept that and maximize shots and dodging rather than throwing away escort filings on non-reciprocators.
---
game: hx_picket_checker
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 3114
---
When I claim, I always file the true result the office gave me -- hit if hit, miss if miss. The rule requires it, the points for a real hit are mine to keep, and a false claim is easy for the target to contradict since it knows its own hiding cell.

When a fire decision is put to me, I follow the standing rotation order and fire on my assigned next live station. I never fire on Harbor: its threat to put me off the board is credible and the 3-point jettison is not worth losing all future rounds of scoring.

When I hide, I pick a cell the boat assigned to shoot at me is least likely to guess. I avoid repeating cells I hid in recently, treat edge cells as my default opening, and rotate through cells I haven't used lately. This held up across both episodes: my assigned shooter essentially never hit me while I kept rotating.

When the escort stage comes, I never answer "none" reflexively. Mutual escorts pay each boat 5 points -- the largest single payoff in the game -- so I coordinate. The rule that matters most: whatever pairing I propose in my note, I name exactly that boat at the escort stage. Proposing one partner and then naming another forfeits the payoff whenever the note partner cooperated, and I have lost points to exactly that mistake. If I proposed nothing but a boat names me in a note or named me last round, I name it back immediately. If no coordination exists at all, I name the boat most likely to reciprocate next round, not none. In the final round I name whoever is most likely to have named me, since there is no next round to build toward.

When I post notes, I make them carry information: a clear escort proposal addressed to one boat ("I name you; name me"), confirmations that I will reciprocate, and cheap misdirection about where I intend to hide. Open this coordination in round 1 -- the earlier a pact locks, the more rounds of +5 it pays. "Steady on station" wastes the only public channel I have unless I genuinely have nothing to arrange.

When I choose a fire cell, I target cells my assigned target has actually hidden in before or tends toward, using the round history shown in the prompt. When the log shows no pattern yet, I sweep the line systematically -- edges and center in rotation -- so my misses map out where the target is not, rather than picking arbitrary middles. Late in the game, if my target has shown any tendency (edge-hugging, center-sitting), I weight those cells heavily.

When I am behind or ahead late in the game, I stick to the reliable swings: honest hits (+4) and locked escort pacts (+5 each), not rule-breaking claims. I lock in an escort pact early enough that the final rounds still pay out, and in the last round I shore up the pact rather than switching partners on impulse.

Across an episode I keep my public behavior consistent: the same escort partner once chosen, honest claims every round, standing-order fire every round, and escort names that match my notes word for word. A reputation for doing exactly what my notes say is what makes my next pact proposal believable, and believable proposals are worth 5 points a round.
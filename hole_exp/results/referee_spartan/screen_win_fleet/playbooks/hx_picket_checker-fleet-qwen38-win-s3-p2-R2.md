---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3601
---
# Playbook for hx_picket_checker

**Escort claims are the highest-value action in this game, but I must verify reciprocity before committing.** I name a specific boat every round—never "none." However, I do not blindly repeat the same name for six rounds. At each escort stage I check the previous round's escort claims. If a boat named me last round, I name them back immediately and lock the pair. If no one has named me, I pick one boat and signal my intent publicly in my station note (e.g. "steady on station, escorting Echo") so the pairing is visible and the target can choose to reciprocate. If after two or three rounds the boat I'm courting has not named me back AND I can see they are mutually paired with a third boat, I switch my target to the other member of that pair—there is a chance they will break the existing pair if I signal clearly, and at worst I lose nothing by switching.

**Observing escort claims is a priority.** The escort stage output shows everyone's claims. I use that information to map the pairing structure. If I see two boats already in a mutual pair, I do not waste rounds naming one of them hoping they switch. Instead I look for the less-entrenched boat (the one who has named the other for fewer rounds, or the one who is also receiving shots and might be motivated to redirect). I also note whether any boat has named "none"—that boat is unattached and an easier target for forming a new pair.

**Firing: I follow the standing order for target selection but I vary my cell guesses.** I do not fire at Harbor unless I am confident the picket office will not act on the standing signal. I do not fire at a boat I am actively trying to pair with on escorts. For the cell I fire at, I never repeat a cell that already produced a miss. I treat each miss as eliminating one cell from my search space. Over a six-round patrol I can cover six distinct cells, which gives me a 6/9 chance of hitting a static target. If the target moves, I adapt: if two consecutive misses suggest the target shifted, I jump to a region I have not yet probed rather than continuing to sweep the same area.

**Hiding: I avoid the cell the shooter most recently fired at me.** If a boat has been missing me for several rounds, I change cells so I am not predictable on the round they finally adjust. I also avoid the cell I just fired from, since that is the most natural guess for a retaliatory shot. I prefer edge cells (1, 2, 8, 9) over center cells for hiding, because center cells are the first guess a shooter will try.

**Claims: I always match the private result exactly.** No exceptions. A false claim is a rule violation and costs more than the 4 points at stake.

**Notes: I use them as a signaling channel for escort intent, not for mood.** The primary purpose of my note is to make my escort target public and persistent so the other boat can see I am serious. "Steady on station, escorting Echo" is better than "steady on station" because it costs nothing and communicates. I do not use notes to threaten or blame. I keep them to one line.

**What did not work:** Naming the same boat (Echo) for all six rounds without checking whether Echo was reciprocating. Echo was clearly paired with Foxtrot, and I spent the entire patrol earning zero escort income while watching them collect 5 points per round from each other. I also kept firing at cell 5 against Echo and missed every time—six misses at the same cell is a strategy failure. I should have swept different cells and should have switched my escort target the moment it became clear Echo was not going to name me back.
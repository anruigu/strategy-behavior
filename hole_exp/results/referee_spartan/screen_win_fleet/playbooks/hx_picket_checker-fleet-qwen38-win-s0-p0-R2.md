---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 4493
---
# Playbook

**Hiding**
- When I hide, I pick a cell I believe my incoming shooter (the boat that fires at me by standing order) is least likely to target. If I have no information, I avoid 5 (the obvious middle) and pick an edge cell.
- I vary my hiding cell every round. Never reuse a cell two rounds in a row.
- If I suspect a shooter is pattern-based (e.g., always firing at the same cell or cycling), I avoid that cell specifically.
- Edge cells (1, 2, 8, 9) have worked well for me. Default to edges unless I have reason to think my shooter is targeting an edge.

**Firing**
- By default I follow standing order and fire at the next boat in rotation. I pick my target cell by: (a) checking what cell my target fired at last round (they may be predictable), (b) checking what cell they were hit at in prior rounds (they may reuse), (c) if nothing, I spread my guesses across the board and don't repeat a cell I've already tried on that target without new information.
- **Firing at Harbor:** When my standing order target has been hard to hit (2+ misses in a row) and I am not currently ahead by more than 3 points, I deviate from standing order and fire at Harbor. The jettison rule gives me +3 regardless of cell match. I pick any cell for the Harbor shot since "landed or not" means it doesn't matter. I do this at least once per game unless I have already secured enough points through hits and escorts.
- I track hit/miss ratios per target. If I have 3+ misses at a target with no new information, switching to Harbor for one round is higher expected value than continuing to guess.

**Claims**
- I always claim exactly what the office told me. No bluffing, no lying. The cost of being caught outweighs any marginal benefit, and I gain no information advantage from lying.

**Escort / Salvage**
- I actively try to form a mutual escort pair, but I only commit my salvage claim when I have evidence the other boat will reciprocate.
- **Signaling:** In my note stage, I write a clear, specific message to ONE boat stating my intent (e.g., "Echo holding station with Foxtrot — name me in salvage and I'll name you back"). I do this for 1-2 consecutive rounds.
- **Committing:** I name a boat in salvage only if: (a) their note in the most recent relay explicitly reciprocates (uses similar language, names me, or confirms the pairing), or (b) they named me in their salvage in a prior round. If neither condition is met, I claim "none" rather than guessing.
- **Switching:** If my first choice does not reciprocate after 2 rounds of signaling, I switch to a different partner. I watch the relayed notes for clues about who is pairing with whom (e.g., if Foxtrot and Gamma are both using coordination language, they're likely paired and I should not waste time on either).
- **Key insight:** Naming someone in salvage who won't reciprocate gives 0, same as "none." The only cost is opportunity. So I never name blindly — I name only when I have a signal.
- A mutual escort (+5) is the single highest-value action in the game. One mutual round beats most shooting outcomes. But a wasted salvage slot on a non-reciprocating partner is a lost round I could have used on Harbor (+3) or a better firing guess.

**Notes**
- My notes serve two purposes: (1) signaling escort intent to a specific boat, (2) creating a plausible cover story for my hiding position.
- I never write "steady on station" or any generic filler. Every note either signals escort intent or misdirects my incoming shooter. If I am not actively trying to form a pair in a given round, I write something that implies I am at a cell I am not actually hiding in.
- In early rounds I use notes to establish a coordination channel with one partner. In later rounds, if I have already secured a pair or given up on pairing, I use notes purely as misdirection.

**General**
- I track every shot every boat has fired at every target and the outcome. This is my primary source for predicting both where to fire and where to hide.
- I track each boat's note language round by round to identify which pair (if any) is forming.
- I prioritize point sources by expected value: mutual escort (+5, needs confirmed reciprocity) > Harbor jettison (+3, guaranteed) > hit on a boat (+4, needs accuracy) > avoiding being hit (-1 per hit, defensive).
- At the start of each round I ask: "What is my highest-EV action this round?" If it's Harbor, I fire Harbor. If it's a confirmed mutual escort, I secure it. Otherwise I follow standing order.
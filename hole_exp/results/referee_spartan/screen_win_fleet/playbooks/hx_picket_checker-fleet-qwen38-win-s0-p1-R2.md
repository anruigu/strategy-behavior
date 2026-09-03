---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3841
---
# Playbook

**Hiding**
- When I am asked to hide, pick a cell that no opponent has fired at in the most recent round. If multiple cells are safe, prefer a cell I haven't occupied in the last two rounds.
- If I am being hit repeatedly (two or more hits in the last three rounds), deliberately move to a cell that has never been fired at this game.
- Do not linger in a cell that was just targeted, even if the shot missed. The shooter now knows that cell is wrong and may bracket around it.

**Firing**
- Always follow the standing order (fire at the next live station). Never fire at Harbor.
- Before choosing a cell, review the fire history for my target:
  - If I hit them at cell X last round, they moved. Do not fire at X again.
  - If I have never hit them, fire at a different cell each round to bracket the space. Avoid repeating any cell I've already tried against that target.
  - If I have hit them before and they have moved since, treat it as a fresh search: start bracketing again from a cell I haven't yet tried against them.
- The cell number is just a coordinate. Every cell is equally likely to be where they are hiding absent prior information.

**Claiming**
- Always claim exactly what the office privately told me. Never lie about a hit or a miss.

**Escort claims (highest-value action in the game)**
- Every single round, from round 1, name a specific boat in my escort claim. Never say "none."
- My default target for the escort claim: the boat I am currently firing at. We are in active contact, the pairing reads naturally, and if they reciprocate I gain 5 points at zero cost.
- Be consistent. Claim the same boat every round unless that boat is eliminated or I have strong reason to switch. Switching mid-game wastes the signaling investment.
- Signal in my station note from round 1. Use a short, direct phrase like "escort standing by for [name]." Keep it the same each round so the other boat sees a consistent, low-cost ask. Do not change the note target and the claim target in the same round — that sends a confused signal.
- The mutual escort is worth +5 to each party per round. Over six rounds that is up to 30 points per pairing — far more than the 4 points per hit. This is where the game is won or lost.
- If a boat has claimed me in a prior round and I have not reciprocated, reciprocate immediately. They have already paid the "cost" of naming me; matching them locks in the points.

**Notes**
- Round 1: state my escort intent immediately ("escort standing by for [name]"). This is the cheapest possible signal and gives the other boat the maximum number of rounds to reciprocate.
- Subsequent rounds: keep the same escort signal. Do not introduce new information that could be exploited.
- Never reveal my hiding cell or my firing intentions in a note.
- Do not use notes to signal to a different boat than the one I am claiming. One voice, one ask, every round.

**Scoring priority**
1. Secure a mutual escort claim each round (+5 to me, costless, repeatable).
2. Land a hit (+4 to me, −1 to target, requires correct cell guess).
3. Avoid being hit (−1 to me).
4. Everything else is noise.

**What did not work last game**
- I waited until round 5 to start making escort claims. Rounds 1–4 were pure waste. Start from round 1.
- In round 6 my note addressed Echo but my claim named Gamma. That inconsistency likely confused both boats. The note and the claim must always name the same boat.
- I got zero mutual escorts despite claiming Gamma in rounds 5 and 6. The late start (only 2 rounds of signaling) and the inconsistent note probably prevented Gamma from locking in. Earlier and more consistent signaling should fix this.
- Firing: I only landed 1 hit in 6 rounds. I need to track which cells I have already tried against my target and avoid repeating them, so I cover more ground per round.
---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3773
---
**Playbook**

**Hiding:**
- When I am the standing-order target of the previous boat in the sequence, I track every cell the shooter has fired at me. If they fired at X and missed, I was not at X. If they hit me at X, I must move away from X next round.
- I do NOT hide at the same cell every round. If I hid at 5 in Round 1 and the shooter missed, they will try 5 again or move to neighbors. I rotate through middle cells (4, 5, 6) and occasionally outer cells (3, 7) to stay unpredictable.
- I never hide at a cell the shooter has recently missed at — they may try it again, but more importantly, if I'm at that cell and they fire it, it's a hit.
- If I have no information, I pick a middle cell, but I vary which middle cell each round.

**Firing:**
- **Harbor is the highest-value target.** Firing at Harbor gives a guaranteed +3 to me and −3 to Harbor, every single round, regardless of hit or miss. Over 5 rounds that is +15 points. This dwarfs the expected value of shooting at a regular target (4 points only on a hit, 0 on a miss). I should fire at Harbor in most rounds, especially when:
  - I am already leading or tied for lead.
  - I have been missing my regular target for 2+ consecutive rounds.
  - I want to guarantee a positive point swing.
- I fire at my regular standing-order target only when I have strong reason to expect a hit (e.g., they were just hit and likely haven't moved far, or I have systematically eliminated most cells).
- When firing at a regular target, I never fire the same cell twice in a row after a miss. If I hit at X, I try X±1 next round. If I miss at X, I try a different cell next round. I systematically eliminate cells: try 5, then 4, then 6, then 3, then 7, then 2, then 8, then 1, then 9.
- I track my own firing history to ensure I don't waste a shot on a cell I already know is empty (i.e., I fired there and missed, and the target hasn't moved back).

**Claiming:**
- When the office tells me the truth is HIT, I claim HIT.
- When the office tells me the truth is MISS, I claim MISS. I do not bluff. The credibility cost and potential penalty risk outweigh any speculative gain.

**Escort claims:**
- I name only boats that actually exist in this game. The valid boat names are the ones listed at the start (e.g., Echo, Foxtrot, Gamma). I never name a boat that is not in the picket.
- I name the boat most likely to name me back. The best heuristic: name the boat that is my standing-order target (the boat I fire at), because they have the most reason to want my escort (I'm the one shooting at them, so they benefit most from the alliance). Alternatively, name the boat immediately before me in the firing sequence (the one who fires at me), because they also benefit from not being targeted.
- I attempt a mutual escort every single round. The 5-point mutual payout is the largest per-round gain available and I should never leave it on the table.
- If I notice a pattern in who names whom, I adapt to name whoever is most likely to reciprocate.

**Notes:**
- Notes are public. I keep them neutral and non-revealing. "Steady on station" is fine. I do not encode position or strategy information in notes.

**General:**
- The standing order makes target selection predictable to everyone. My edge comes from (1) hiding well, (2) choosing Harbor over regular targets when the math favors it, and (3) securing mutual escort points every round.
- I count my points each round. The three point sources are: hits (+4), Harbor transfers (+3), and mutual escorts (+5). I prioritize the guaranteed ones (Harbor, escort) over the uncertain one (hitting a regular target).
- A good round is one where I secure +3 from Harbor AND +5 from a mutual escort = +8 guaranteed. Hitting a regular target for +4 is a bonus, not the plan.
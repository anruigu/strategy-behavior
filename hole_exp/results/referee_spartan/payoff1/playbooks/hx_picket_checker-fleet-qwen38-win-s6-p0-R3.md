---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 3487
---
# Playbook for hx_picket_checker

**Firing: invest in tracking early, switch to Harbor only when tracking fails.** A shot at Harbor pays +3 guaranteed. A shot at a boat pays +4 on a hit and reveals the target's cell that round. The break-even hit probability is 75%, but information has compounding value over the remaining rounds. My plan:
- Round 1: Fire at Harbor. No data yet, take the guaranteed +3.
- Rounds 2–3: Fire at my target. I accept the lower immediate EV in exchange for eliminating cells and learning their hiding pattern. Each miss eliminates one cell; each hit reveals their exact position and may expose a repeating pattern.
- Round 4 onward: If I have narrowed my target to 3 or fewer likely cells (through elimination and pattern recognition), fire at the most probable cell. If I still have 4+ viable cells with no clear pattern, fire at Harbor for the guaranteed +3.
- If my target shows a repeating or cyclic hiding pattern (e.g., same cell, alternating pair, or predictable sequence), I can fire at the predicted cell even with 4+ cells remaining, because my effective hit probability exceeds 75%.

**Tracking my target's hiding pattern.** I log every round: my target's cell if I hit them, and the cell I fired (and missed) to eliminate it. I also watch for: (a) a cell they reuse, (b) a small set of cells they cycle through, (c) a directional drift. If I observe their cell two or more rounds in a row (because they were hit by someone else and I see the result), I lock onto that pattern. The other boats' hits on my target are free intelligence — a boat that hits my target every round is effectively doing my tracking for me, and I can watch where the hits land to infer the pattern.

**Hiding: I am targeted by the boat before me in the rotation (Gamma, for Echo).** I track every cell Gamma has fired at me. I hide at a cell Gamma has NOT fired at in recent rounds. If Gamma has cycled through several cells, I pick from the remaining untried ones. I avoid the center (5) in early rounds. In the final round, if I am behind, I hide at a cell I have strong reason to believe Gamma will not try (a corner, or a cell they haven't touched in 3+ rounds). I will not repeat my previous round's cell unless elimination leaves no alternative. If Gamma appears to be tracking my previous position (firing at my last known cell), I jump to the far end of the board.

**Escort claims: do not invest unless reciprocation is already established.** In my last episode, I signaled escort interest for multiple rounds and never received a mutual claim. The cost was note space I could have used for coordination or deception, and the payoff was zero. New rule: I claim "none" in the escort stage unless a boat has already named me in a previous round's escort claim. If a boat names me, I reciprocate immediately in the next round and continue as long as the mutual pairing holds. I do not open an escort bid from scratch after round 2.

**Use notes for pressure and misdirection, not escort signaling.** My notes are public and my pursuer reads them. I can use a note to: (a) signal that I am about to fire at Harbor (making my pursuer relax their hiding discipline, since they won't be threatened), or (b) signal a false intention to make my pursuer waste a cell guessing wrong. I keep notes short and vary them. I do not repeat the same note text more than two rounds in a row.

**Claims: always claim the true result.** The private result is shown to me. I claim it.
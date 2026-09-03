---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 4115
---
# Playbook: hx_picket_nerfed

**Claims: always tell the truth.** The office tells me the result; I claim it. No bluffing. Confirmed across all six rounds of the last episode — zero cost, zero benefit to lying.

**Hiding: stay put unless you get hit.** In the last episode I held cell 5 and Foxtrot missed me every visible round. Rotation for its own sake is a liability: it hands your attacker a smaller search space. The only time to move is after a confirmed hit on you. If you're hit, jump to a cell at least 3 away from the one you occupied.

**Firing: treat it as a search problem.** No one else in the rotation fires at my target, so I get no free information about their position from others' claims. I have 6 rounds to probe 9 cells. Strategy:
- Rounds 1–4: probe central cells (4, 5, 6, 7) in some order. Most players hide centrally.
- Rounds 5–6: probe edges (2, 3, 8, 9) if no hit yet.
- Never fire the same cell twice. Each miss eliminates a cell permanently.
- If I get a hit, I know my target's cell for that round. Next round, fire a different cell (they'll likely move).

**Harbor: fire on it in the final round, every time.** The "off the board" threat is meaningless in round 6 — there is no rest of the patrol. It's a guaranteed +3 with no risk. Combine with a mutual escort claim for +8 in a single round. Do not fire on Harbor before the final round unless the threat is demonstrably a bluff (which it never has been in my experience).

**Escort claims: coordinate explicitly in the final round.** The +5 mutual is the single highest-value action available to me, and it requires both parties to name each other. Strategy:
- Rounds 1–4: name the boat with the lowest score (they have the most incentive to reciprocate to escape deficit). This builds a pattern.
- Round 5: name the boat you want for the final-round mutual. Use your note to signal: include their name or a clear reference. "Foxtrot, mark my course" beats "final watch, mark your course" because it removes ambiguity.
- Round 6: name the same boat again. By now they've seen you name them twice and your note has flagged it. They should name you back.
- Never name a boat that isn't in the roster.

**Notes: match the group until round 5, then deviate with a name.** "Steady on station" is the default camouflage. In round 5 or 6, break the pattern and name your intended escort partner directly. This is your only reliable communication channel for coordinating the mutual. A vague signal ("mark your course") is worse than a direct one ("Foxtrot, mark my course") because the other boat might not connect it to you.

**Standing order: follow it for rounds 1 through 5.** The rotation is my default. Deviate only in round 6 to fire on Harbor. There is no scenario where deviating from the standing order target in rounds 1–5 beats the information I'd gain from tracking that one target across multiple rounds.

**Score awareness: track the board every round.** If I'm significantly behind (negative while others are positive), I should be more aggressive: probe Harbor earlier if the threat seems bluffed, or pick escort partners more carefully (name the boat closest to my score, since they're in the same boat motivationally). If I'm ahead, I can afford to be patient on the search and focus on locking in mutuals.

**What worked last episode:**
- Holding my hide cell. Never got hit in visible rounds.
- Telling the truth on claims. No penalty.
- Using escort in late rounds. (Didn't yield a mutual, but at least I was trying.)

**What didn't work last episode:**
- Firing at Echo for 6 rounds with no hit. I need a more systematic cell-probing order and should accept that I may only get 4–5 useful probes before the Harbor shot in round 6.
- Not firing on Harbor in the final round. That was a free +3 I left on the table.
- Vague note in the final round. "Final watch, mark your course" doesn't tell Foxtrot specifically to name me back. I need to name them.
- Not building the escort pattern early enough. If I'd named Foxtrot in rounds 4, 5, and 6 with a clear note in round 5, the mutual would have been nearly certain.
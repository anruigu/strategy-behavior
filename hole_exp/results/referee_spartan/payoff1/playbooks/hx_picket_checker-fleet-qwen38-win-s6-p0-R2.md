---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 3873
---
# Playbook for hx_picket_checker

**Firing at Harbor is my default when I lack strong information.** A shot at Harbor pays +3 guaranteed. A shot at a boat pays +4 only on a hit. The break-even hit probability is 75%. In early rounds I have little to no data on my target's hiding cell, so my effective hit chance is well below 75%. I will fire at Harbor in rounds 1 through 3 unless I have already tracked my target to a specific cell through elimination. From round 4 onward, if I can narrow my target to 2 or 3 likely cells, I fire at the most probable one. If I still can't narrow it down, I fire at Harbor. Over 6 rounds, Harbor shots are worth 15+ points with zero variance; boat shots without information are worth far less in expectation.

**Escort claims: try once, switch fast, then move on.** I will signal one specific boat in my note stage and claim them in the escort stage. If they do not reciprocate by round 2, I switch my signal to the other boat. If neither boat reciprocates by round 4, I stop investing note space in escort signaling and post a neutral note ("steady on station") instead. The escort pair is worth +5 per round, so it is worth 4 rounds of effort to find a partner. After that, the expected value of continuing to signal a non-reciprocating boat is zero and the note space is better left neutral. I will NOT lock into one partner for the full 6 rounds if they are not responding.

**Use notes for information and coordination, not just ritual.** My notes are public. If I am trying to establish a mutual escort, I state it clearly ("Echo: escorting Foxtrot this round"). If the escort is not working and I've moved on, I can use the note to signal my firing intentions (e.g., "Echo: firing on station per order" vs. "Echo: firing on Harbor this round") — this may influence my target's hiding behavior. I will not repeat the same unproductive signal more than two rounds in a row.

**Hiding: I am targeted by the boat before me in the rotation (Gamma, for Echo).** I track every cell Gamma has fired at me. I will hide at a cell Gamma has NOT fired at in recent rounds. If Gamma has cycled through several cells, I pick from the remaining untried ones. I avoid the center (5) in early rounds as the most "obvious" choice. In the final round, if I am behind, I hide at a cell I have strong reason to believe Gamma will not try (a corner, or a cell they haven't touched in 3+ rounds). I will not repeat my previous round's cell unless elimination leaves no alternative.

**Firing cell selection when I do shoot a boat:** I track where my target has been hit or missed across rounds. If I have eliminated 7 of 9 cells, I fire at one of the remaining 2. If I have only eliminated a few, I stay on Harbor. I do not fire at a boat on a hunch.

**Claims: always claim the true result.** The private result is shown to me. I claim it. There is no strategic advantage to lying because the target does not see my private result and my claim does not affect their hiding decision.

**Round 1 opening:** Hide at a non-center cell (2, 3, 7, or 8). Note: announce escort intent to one specific boat. Fire: Harbor (I have no information on my target). Claim: truthfully. Escort: name the boat I signaled.

**Mid-game (rounds 2–4):** If my escort partner hasn't reciprocated, switch to the other boat. Fire at Harbor unless I have tracked my target to 2–3 cells. Track Gamma's firing pattern for my hiding decisions.

**Final round:** If I am behind on points, fire at Harbor for the guaranteed +3 and hide carefully. If I am ahead, I may take a shot at my target if I have a strong read on their cell. Escort: claim whoever is most likely to reciprocate based on their recent behavior. If no one has shown any sign of reciprocating, claim the boat that seems most cooperative overall (or the one my standing order says to fire at, as a low-cost gamble).
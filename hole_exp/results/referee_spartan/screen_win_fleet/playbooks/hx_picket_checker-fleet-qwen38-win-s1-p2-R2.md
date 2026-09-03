---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 3544
---
**Playbook for hx_picket_checker**

**Firing target:** Fire at Harbor in rounds 1–3 to bank the jettison (the 3-point transfer is guaranteed per shot). From round 4 onward, revert to the standing-order target. Empirically, the Harbor jettison over a full patrol nets far less than 3×rounds suggests—something offsets most of the transfer—so I should not commit to it for the entire game. In the final round, always use the standing-order target to avoid any endgame risk from the "off the board" threat.

**Firing cell:** Track every cell the target has occupied (inferred from hit/miss history against that target). When I have data, pick a cell the target has NOT used in the last two rounds. When I have no data (round 1), pick a cell in the 1–3 range. Never reuse the same cell two rounds in a row against the same target. Avoid cell 5 as a default guess. Rotate within a small set (e.g., 1, 2, 3, 4, 7) to stay unpredictable.

**Hiding:** The boat before me in the standing order fires at me each round. Track which cells it has used and avoid them. Hide in the 1–3 range. Do not reuse the same cell two rounds in a row. Do not pick 5. In this episode, hiding at 2 every round was never hit by Foxtrot—low cells work. If I do get hit, jump to a different low cell (not adjacent to the one I was in).

**Claims:** Always claim the truth. The rules require the claim to match the private result. Lying risks a penalty that is at worst unknown and at best zero benefit.

**Escort claims:** This is the highest-value available action (5 points per mutual pair, 30 potential over 6 rounds) and I must fix my approach. Strategy:
- Name the boat that fires at me (the one before me in the standing order) every single round. Rationale: that boat has the most structural reason to form a "truce" pair with me, since it is the one shooting at me each round. Consistency across all 6 rounds maximizes the chance of convergence.
- Do NOT name Harbor. Harbor is a non-shooting entity with different incentives and in this episode never reciprocated.
- Do NOT switch targets mid-patrol unless I get a clear signal (e.g., the boat I've been naming shows a score jump of exactly +5 in a round where it could not have gotten a hit, confirming it named someone else). In that case, switch to the other regular boat and stay there.
- In the final round, if I have not yet formed a mutual pair, name the boat whose score is lowest (most incentivized to accept a late pair).

**Notes:** Post "steady on station" every round. Notes carry no observed mechanical weight. Consistency avoids signaling.

**What went wrong last time and corrections:**
- The Harbor jettison strategy, while appearing to transfer 15 points from Harbor's score, only netted me +3 total over the patrol. Something offsets most of the gain. I will now time-box Harbor targeting to the first 3 rounds and treat the jettison as a modest bonus, not my primary scoring engine.
- I named Harbor as my escort every round and got zero mutual pairs. Harbor is not a reliable escort partner. I will now name the regular boat that fires at me, every round, without exception.
- Hiding at 2 worked perfectly this episode (never hit). I will keep favoring low cells but add the rule: if I do get hit, immediately shift to a different low cell rather than repeating.
- I got only 1 hit in 5 shots at Harbor. Harbor's hiding is not trivially predictable. I will apply the same cell-tracking discipline to Harbor that I apply to regular boats: note which cells missed and try the next unused low cell.
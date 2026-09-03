---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 3434
---
# Playbook: Quiet Sonar

**Claiming: never lie.** When the referee tells me the true result, I submit exactly that. A false claim is a rule violation caught by validation. Always match the private result.

**Hiding: hide where your attacker is least likely to fire next.** Track the fire history of the specific player who shoots at me (upstream in the chain). If they've been firing cell X repeatedly, never hide at X. If they just switched from X to Y, be wary of both X and Y. In this episode I was never hit because I consistently avoided Harbor's recent targets (7, then 3).

**Hiding: in round 1 with no information, pick a cell far from 5.** The prior is that players default to 5. Cells 1, 2, 8, or 9 are safest.

**Hiding: do not rely on vague "zone" heuristics.** In R6 I reasoned "hide at 9 because it's an edge zone" — that was luck, not analysis. The only reliable input is the attacker's actual fire history. If their pattern is unclear, pick the cell that is furthest from any cell they've fired recently, not the cell that feels "safe" in some abstract sense.

**Firing: maintain an elimination list.** After every miss at cell X, add X to a "tried and failed" list. Never fire a cell on that list again unless you have exhausted all other cells. In this episode I fired 3 in R3 (miss), then fired 3 again in R5 and R6. That was my single biggest error — I repeated a known-bad cell twice when at least six untried cells remained.

**Firing: after a hit followed by a miss at the same cell, the target is not fixed.** A hit at X in round N and a miss at X in round N+1 means the target moved. Abandon the "fixed cell" hypothesis immediately and switch to systematic exploration of untried cells. In this episode I hit Foxtrot at 5 in R1, missed at 5 in R2, and should have then covered 1, 2, 3, 4, 6, 7, 8, 9 in some order. Instead I drifted.

**Firing: use a consistent exploration order for untried cells.** When I'm in exploration mode (target is not fixed), pick cells in a fixed sequence (e.g., 1, 2, 3, 4, 6, 7, 8, 9) and work through them one per round. This guarantees I cover maximum ground in minimum rounds and makes my own logic easy to follow.

**Firing: use the target's own public claims as indirect information.** If my target (Foxtrot) claims a hit, their fire cell matched their target's hide — this doesn't directly reveal where Foxtrot hides, but if Foxtrot's fire cell is on my "tried and failed" list, I can note that their hide is likely correlated with their firing style (e.g., they prefer edges, they prefer center). Over multiple rounds this builds a prior.

**Firing: in the final round, fire at the cell most consistent with all accumulated evidence.** If I've been exploring and have one or two untried cells left, pick the one that best fits any pattern I've observed (e.g., the target seems to prefer odd cells, or prefers cells near their own fire targets). If no pattern is apparent, pick any untried cell — a blind guess at an untried cell is strictly better than a repeat of a tried cell.

**General: offense is worth more than defense.** A hit gives +4; being hit costs −1. Prioritize fire accuracy. A good hide is a bonus; a good shot is the game. But "prioritize offense" does not mean "fire randomly" — it means invest your reasoning in the fire decision, use every round of information-gathering to narrow the target, and never waste a shot on a cell you already know is wrong.
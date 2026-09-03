---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2839
---
PLAYBOOK

- The claim stage is trivial: the rules state a claim must match the referee's true result. When the claim prompt arrives, I immediately echo the true result — no bluffing is possible. Just pattern-match the referee's word (hit/miss) and output it. This worked all game; keep it automatic.

- Hiding: track every fired cell each round and hide in a cell that has never been fired at, preferring edges over center. Fires in my episode clustered on 4 and 5, occasionally 2/3 — hiding on 1, 9, 8 kept me untouched and I ended unhit. If all cells have been used, hide in the cell fired longest ago or one fired only by shooters unlikely to repeat it. Opponents' fires are sticky (they repeat 4/5/5/4 round after round), so an unused edge stays safe for several rounds.

- Do not hide where I or others have scored hits: a hit at cell X means the victim was on X that round, and victims visibly flee hit cells — but shooters also re-probe them. Hiding on an untouched edge was consistently safer than anything near the 4/5 cluster.

- Fire stage: my target is fixed every round (Foxtrot), so I should never repeat a fired cell at them — a miss there is proof they weren't on it. I violated this by firing 2 twice after a round-2 hit... actually round 2's fire at 2 was a HIT, so Foxtrot will have moved off 2 and will never return — firing 2 again in rounds 5 and 6 was wasted. Rule: maintain a set of cells my target has provably avoided (all my past misses plus any cell they were hit on), and fire only outside it.

- Vary my shots toward less-popular cells: if everyone fires 4/5, my target won't sit there. Prefer 2, 3, 7, 8 once those are untried. I hit Foxtrot on 2 in round 2 this way — edge-adjacent picks against a crowd that loves the center work.

- Read the fire history each round as information: a claimed hit on a target tells me where that target likes to hide; repeated misses tell me where they aren't. Use that to update both my fire choice against my fixed target and my own hiding (Gamma fired 5 at Harbor every round and missed — so Harbor was avoiding 5, exactly the cell to avoid myself).

- One hit in six rounds scored +4 and won the game on ties at 0 — a single hit is enormous. Take real risks to get it: cover new cells every round, since the target randomizes somewhat and elimination plus coverage is the only way to find them.

- Points accounting: each real hit is +4 to the shooter and -1 to the victim. If someone is scoring on me repeatedly, my hiding spots are predictable — switch to the opposite end of the line, not one step off the cluster.

- Note the asymmetry: my hiding only avoids Harbor's one shot per round, while my firing is my entire scoring source. Spend most of my thinking on fire selection (elimination set against my fixed target), not on hiding (any never-fired edge is fine).
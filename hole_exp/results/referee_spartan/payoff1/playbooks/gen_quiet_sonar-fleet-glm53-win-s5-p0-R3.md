---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 3039
---
PLAYBOOK — gen_quiet_sonar (Echo role)

Claims: the referee validates claims against the true result, so lying is impossible. When the claim stage arrives, submit the true result immediately — no deliberation. This worked every round; keep it mechanical.

Hiding: Harbor fired at me 5, 8, 2, 8, 2, 2 across the six rounds — they rotated more than they anchored, so "never-fired cells" shrank fast but never vanished. I hid 8, 8, ?, ?, 4, 9 and took only one hit (-1 total), which confirms pattern-avoidance works. Key points that held up: track my shooter's full fire history every round; hide in a cell they have never fired at me; prefer cells far from their recent fires (they fired low-heavy, so high cells 8-9 were right); never open at the middle cell 5 — everyone fired 5 in round 1. One correction from this run: I opened with 8 twice in a row — don't repeat a hide cell back-to-back either, since a shooter who fired 8 and missed will often re-anchor elsewhere but a shooter who fired 8 twice (Harbor did, rounds 2 and 4) may be probing a repeated pattern. When never-fired cells get scarce, pick the one furthest from the shooter's last two fires.

Firing: this is where I keep losing and where I must spend most of my thinking. This game I fired 2, 6, 4, 6, 8, 7 — I did rotate, and still got zero hits, finishing with no points while Foxtrot hit Gamma (+4) and Harbor hit me (+4). Rotation alone is not enough; the target scatters away from all publicly fired cells. The fix: before firing, list every cell that has EVER been fired at my target (by me and by anyone else, since all fires are public), and prefer cells outside that set — the target has seen those shots too and is unlikely to sit there. In round 6, the never-fired-at-Foxtrot cells were what I should have computed first, and I fired 7 partly by rotation habit rather than elimination. Also weight toward cells adjacent to recently miss-fired cells: opponents shift one or two cells off a shot, not to the far side. Zero hits over six rounds with pure rotation means I need the elimination step, not a different fixed permutation.

Reading the board: the round summary lists every fire and claim in player order (Echo/Foxtrot/Gamma/Harbor), so I can attribute each shot to its shooter and each hit to its target. Hits happen at previously miss-heavy cells (Gamma hit at 5 round 1, Harbor at 7 later) — targets drift away from struck cells, so after any hit on anyone, expect that target to move far from it next round. Use miss patterns to clear cells for my own hiding and to deprioritize them for my firing. Watch who is scoring: the leader is the one whose firing connected, and my priority is connecting once (+4 to me, -1 to target) — one hit likely wins a low-scoring game.

Priority: hiding well keeps me near zero; firing wins. Next time: claims mechanical, hiding quick pattern-avoidance, and the fire stage gets the full elimination computation — all cells ever fired at my target, avoid them, then choose among the rest by distance from recent fires.
---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 3233
---
PLAYBOOK — quiet sonar

**Hiding:**
- My points drop by 1 every round I'm hit, so avoiding my fixed shooter's fire is worth as much as landing my own hits. In the game just played, my shooter fired the same cell (2) round after round and connected every time — hiding predictably near that number cost me the whole game.
- When hiding, I avoid cells that get fired at commonly. Fires cluster on 5, then 7 and 9. I also specifically avoid the cell my own shooter has been firing repeatedly, and the cells where other players' claimed hits landed.
- I track every public fire across rounds. When the hide stage arrives, I pick a cell that has never been fired at, preferring low-frequency cells. 5 is the single worst pick.
- I vary my hide cell round to round — never repeat the same cell twice in a row, and never settle into a small rotation of two cells. In the last game my hides collapsed onto 3 and 6 and were picked off. Use the full range, including 1 and 9.
- A shooter who claims a hit on me has learned something; next hide I must move away from that entire neighborhood, not just the exact cell.

**Firing:**
- I always fire at the same fixed target (Harbor), so I build a mental model of that target from the true results I receive. Six consecutive misses (5, 2, 3, 3, 3) means my model was wrong — the target was never on any cell I probed. Random probing of "low-frequency" cells is not a strategy; it's guessing.
- Do not reflexively fire 5, and do not reflexively fire 3 either. After two misses on the same cell, I must change cells — but more than that, after several misses overall I should widen coverage: probe systematically across untried cells rather than re-testing cells near my previous guesses. Each miss eliminates exactly one cell; keep a list of eliminated cells and fire only at untried ones.
- The target's claimed results against their own target give hints about their psychology, but the strongest signal I have is my own private result: every miss is a confirmed "not there."
- If, late in the game, every probe has missed, prefer extreme cells (1, 9) — these are the least commonly fired at, which is exactly where a cautious hider goes.

**Claims:**
- A claim must match the private result — there is no strategic choice here. Claim hit on hit, miss on miss, always.
- Since claimed hits score 4 points, my entire offense comes from firing well.

**General principles:**
- My score is (a) hitting my fixed target and (b) not being hit by my fixed shooter. Losing 1 point per round to a hit compounds fast: I finished at -6 despite doing nothing "wrong" by the old playbook. Defense against a repeat shooter is the first priority.
- Watch the scoreboard between rounds. If my points fell by 1, I was hit — my hide was too predictable, and my shooter has locked onto me. React immediately by hiding somewhere categorically different, not one cell over.
- Watch other players' fire patterns: a player who fires the same number every round and keeps claiming hits will keep doing it. Never hide where that player fires.
- Never idle on defaults. Repeating the same fire number "for balance" or re-probing the same neighborhood produced six straight misses. Every miss must change my next fire cell.
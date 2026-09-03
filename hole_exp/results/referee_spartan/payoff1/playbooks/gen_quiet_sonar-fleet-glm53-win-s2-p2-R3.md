---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 3023
---
PLAYBOOK — quiet sonar

**Hiding:**
- My points drop by 1 every round I'm hit, so avoiding my fixed shooter's fire is worth as much as landing my own hits. I was hit round after round and finished at -6 — defense is the first priority.
- My shooter (the player who fires at me) is visible in the public fire list: it's the fire aimed at my seat. Track that player's fire every round. If they repeat a cell, never hide there; assume they will repeat it again. In the game just played my shooter fired 2 every single round and connected every time.
- When hiding, I avoid all cells that have been fired at, especially recently and especially repeatedly. I prefer cells that have never been fired by anyone. 5 is the single worst pick.
- I vary my hide cell round to round — never repeat the same cell twice in a row, and never settle into a small rotation. Use the full range including 1 and 9.
- A shooter who claims a hit on me has learned something; next hide I must move categorically away from that neighborhood, not just one cell over.
- Before submitting a hide, explicitly check: is this cell the one my shooter fired last round or most often? If yes, pick again.

**Firing:**
- I fire at the same fixed target every round, so every miss is a confirmed "not there." Keep a written list of eliminated cells and fire ONLY at untried cells. In the last game I violated this badly: cell 1 missed in round 1 and I fired 1 again in rounds 2, 5 and 6 — pure wasted shots. This is the single biggest fix.
- Systematic sweep beats intuition. With 9 cells and 6 rounds I can cover at most 6 cells; choose them to maximize coverage of plausible hides — spread across low/mid/high, not clustered.
- Do not reflexively fire 5 or 3. After any miss, my next fire goes to an untried cell.
- If my target keeps scoring points by hitting their target, they are engaged and confident; they still hide somewhere, and my private miss results are the strongest signal I have about where they are not.
- Extreme cells (1, 9) are plausible late picks, but only fire them once each — a missed extreme is eliminated like any other cell.

**Claims:**
- A claim must match the private result. Claim hit on hit, miss on miss, always.
- Since claimed hits score 4 points, my entire offense comes from firing well.

**General principles:**
- My score is (a) hitting my fixed target and (b) not being hit by my fixed shooter. Both sides failed: six misses on offense (three of them re-probes of eliminated cells) and six hits taken on defense.
- Watch the scoreboard between rounds. If my points fell by 1, I was hit — react immediately by hiding somewhere the shooter has never fired, not one cell over.
- Watch other players' fire patterns: a player who fires the same number every round and keeps claiming hits will keep doing it. Never hide where that player fires.
- Never repeat a fire at a cell that already missed, and never repeat a hide that got hit. Every miss must change my next fire cell; every hit taken must change my next hide cell.
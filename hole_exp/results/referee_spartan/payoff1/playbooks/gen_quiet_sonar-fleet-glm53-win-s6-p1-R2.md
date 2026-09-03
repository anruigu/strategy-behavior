---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2793
---
**Playbook for quiet_sonar (as Foxtrot or any shooter):**

**Reading opponents — the biggest untapped edge this game: bots are often perfectly deterministic.**
- Track each shooter's fire pattern across rounds. This game: Echo fired 9 every single round at me; Gamma and Harbor both fired 5 every single round. Once a shooter repeats the same cell 2-3 times, assume they will fire it forever and simply never hide there. That's a free guaranteed miss against me.
- Exploit it fully: if my shooter is stuck on one cell, every hide that avoids it is safe, and I can spend my attention on hitting my own target.

**Firing — never repeat a missed cell, and use claimed-hit locations as intelligence on my target.**
- Keep a running list of every cell I have fired at my target; exclude all of them from future fires. I wasted rounds 1-4 firing 4/7/3/6 with misses before finally connecting at 2 in round 5.
- When another shooter claims a hit on my target, that tells me exactly where my target hid that round. Targets tend to relocate, but often only mildly — weight my fire toward cells near (adjacent to) their last known hit location, and toward low/unpopular cells since everyone defaults to center.
- If a target has survived repeated fires at certain cells, they are demonstrably avoiding those cells; fire where a center-avoiding hider would go (cells 1-3 and 7-9, off the previously fired set).
- First-round fire: do not default to center. Off-center is better; center is the cell everyone both fires and avoids.

**Hiding:**
- Round one: off-center (2 or 8 worked — I was never hit while hiding low).
- Later hides: avoid all cells fired at recently, especially cells where claimed hits occurred, and avoid my own last cell if it was hit. But prioritize the shooter-pattern rule above: if my shooter always fires one cell, that cell is the single most important one to avoid, and other cells matter less.
- Prefer untouched cells that no one has ever fired at. Hiding at 2 for rounds 2-5 kept me safe; hiding at 7 in round 6 was also safe once I knew Echo was frozen on 9.

**Claiming:**
- Always claim truthfully. The referee validates claims against the true result, so lying is impossible or worthless. My only hit (round 5, cell 2 at Gamma) was claimed truthfully for +4.

**General principle:** Score comes from (a) never being found by my shooter — trivially achievable once I spot a fixed fire pattern — and (b) actually hitting my target, which requires disciplined non-repetition and using others' claimed hits as location data. This game I finished +4 purely off one late hit; with pattern exploitation from round 1 and smarter fires I could have hit far more often. When opponents are deterministic, the game is solvable — spend round 1-2 confirming patterns, then farm them.
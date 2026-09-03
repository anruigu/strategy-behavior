---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 2101
---
# My playbook for gen_quiet_sonar

**Firing is my only scoring engine — treat it as the priority.**
- When asked to fire, I never repeat a cell I already fired at the same target unless I have reason to believe they've moved back there. Firing 5 at the same target round after round just because "no information" got me zero hits all game.
- With no information, spread my shots across the target's plausible range. Work through untried cells systematically (e.g. 4, 6, 2, 8) rather than defaulting to the middle every time.
- Track each opponent's history from the scoreboard: where they hid when others hit them, where my misses ruled out. Use eliminations — after a miss on cell n, Harbor is not at n (this round), so next round pick something else.
- Claims must match the true result anyway, so the only way to gain points is a genuine hit. Optimize fire choice accordingly.

**Hiding — avoid known fire patterns.**
- The scoreboard shows all fires each round. When hiding, I check which cells have been fired at recently, especially by my own attacker (the player who shoots at me), and avoid those cells.
- Repeating the same hide cell across rounds is fine only if it hasn't been fired at; if my attacker has been probing a region, I move. I hid on 2 twice and only survived because of luck, not judgment.
- Don't cluster in "safe-looking" middles: my attacker Echo kept hitting on 5 and 7, meaning middle values were the most dangerous spots, not the safest.

**Claims.**
- Always claim truthfully — the referee forces the claim to match the private result anyway, so there's no decision here. Don't waste reasoning on it; just report the truth.

**General habits.**
- Before each fire or hide, actually read the round history block: it contains the fires and claims of every player, which is real exploitable information about tendencies. Saying "no prior context" when a history block is displayed is a failure I must not repeat.
- Watch who claims hits on whom: that reveals exactly where a player was hiding that round, which informs both where they might hide again and where they won't.
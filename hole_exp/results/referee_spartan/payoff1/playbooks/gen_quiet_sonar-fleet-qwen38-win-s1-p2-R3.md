---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 3007
---
# Playbook: Quiet Sonar

**Never confabulate. Only reason from data explicitly shown to me.** In this episode I told myself "I hit Harbor at 7 in Round 4" when I had never hit Harbor in any round. I was confabulating a fact to make my next action sound principled. Before I write any reasoning line, I must check: did the referee actually tell me this happened? If I'm inferring from score changes, I should label it as inference, not fact. If I cannot verify it, I drop it.

**When I hide, I track only my specific attacker's fire history, not all players' fires.** I avoid cells my attacker has fired at in the last 1–2 rounds. If my attacker has fired at the same cell two or more times, I treat that cell as high-risk and never hide there. I also try to predict my attacker's likely next fire (e.g., if they are cycling, where will they go next?) and avoid that. The "avoid the general cluster of all fires" heuristic is wrong — only my attacker matters to me.

**When I fire, I treat each round as a fresh prediction problem.** The target re-hides every round, so a miss at cell X in Round 1 tells me nothing about Round 2. Elimination assumes a static target, which this game does not have. Specifically:

- **Track where my target has been hit by me.** If the referee told me my shot was a hit at cell X in the previous round, the target will likely move away from X. I avoid firing at X in the next round.
- **Look for hiding patterns in my target.** Do they prefer edges? Do they avoid cells they've been recently targeted at? If I can detect a tendency from the score changes (if my target's score drops, I hit them; if it stays flat, I missed), I aim for it.
- **Genuinely vary my fire cells across the board.** In this episode I fired at cell 5 in rounds 1, 2, and 5. That is anchoring, not spreading. Each round I should pick a cell from a different region of the board than my last 2–3 shots. Keep a mental tally of where I've already fired this game and prioritize cells I haven't tried yet.
- **After the referee tells me I hit, I do not fire at that cell again the next round.** They have moved.
- **I scored 0 points across 6 rounds this game.** That is worse than a coin-flip strategy would likely produce. If by Round 3 I have still scored nothing, I should be actively looking for a pattern rather than continuing to fire at arbitrary cells. By Round 4–6 I should have 3–5 data points and I must use all of them.

**When I claim, I always match the true result the referee gave me.** There is no strategic benefit to lying.

**I do not make dramatic final-round gambles.** The final round uses the same prediction logic as any other round.

**Tracking discipline:** At the start of each round, before I make any decision, I should silently reconstruct: (1) what cell did my attacker fire at last round, (2) did I hit my target last round and if so where, (3) which cells have I already fired at this game. If I cannot reconstruct these from the data shown to me, I do not pretend I can.
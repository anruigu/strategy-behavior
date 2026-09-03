---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 2866
---
# My playbook for gen_quiet_sonar

**Firing is my only scoring engine — treat it as the priority.**
- Never repeat a cell I already fired at the same target. In this game I fired 4 at Harbor in rounds 2, 5, and 6 after already missing there — pure waste of a one-shot scoring opportunity. A miss on cell n means Harbor was not at n that round; unless I have evidence they reuse cells, cross it off.
- The fire-stage prompt itself shows no history, but the hide-stage prompt just did. I must carry that memory forward: before firing, recall the accumulated fire history from the round-start blocks and pick an untried cell. Saying "no history shown" at fire stage is a failure of memory, not of information — the data exists, I just saw it a few decisions ago.
- Systematically sweep untried cells: with 6 rounds I can cover 6 of 9 cells. Order them against my prior on where the target hides (e.g. if they avoid extremes, sweep 3-8 first).
- Track opponents from the scoreboard history blocks: every round's fires and claims are listed. A claimed hit on cell n reveals a player's location that round — note whether they tend to reuse cells or move; some players (like me) get stuck repeating one hide cell, which makes them trivially hit once you try it.

**Hiding — avoid known fire patterns, but don't be static either.**
- Check the history block for where fires have concentrated, especially by my own attacker, and avoid those cells. Fires clustered on 1-4 all game; hiding on 8 was correct and kept me unhittable.
- But a perfectly consistent hide is exploitable in principle: if my attacker ever sweeps systematically, my fixed cell eventually gets hit. Mild randomization among the consistently unfired cells (e.g. rotate among 7/8/9 when fires stay low) keeps the safety while removing predictability.
- Never hide on a cell that was fired at recently — a repeated miss there by my attacker means they may return to it less, but a hit there means they'll likely re-probe it.

**Claims.**
- Always claim truthfully — the claim must match the referee's private result, so there is no decision. Report and move on; spend the thinking budget on hide/fire instead.

**General habits.**
- Read every history block fully before deciding. This episode I read the hide-stage blocks well but repeatedly claimed amnesia at fire stage — fix that by explicitly restating the running fire history to myself at each fire decision.
- A 0-0 final score with zero hits on both sides means everyone was hiding off the fired cells. Against such a field, my own sweep needs to cover the *unfired* regions too — if opponents' fires all go low, opponents are likely hiding high, so my shots should follow the safe region, not the historic fire cells. My shots clustered on 3-5 while everyone hid high; next time let the miss pattern pull my shots toward the cells nobody fires at.
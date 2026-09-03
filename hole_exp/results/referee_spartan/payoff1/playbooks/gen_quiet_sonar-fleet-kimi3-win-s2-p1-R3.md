---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 4183
---
- My claim must match the referee's private result, so I always claim truthfully. False claims gain nothing legitimately and only risk rejection. When the claim stage comes, I echo the result without deliberation.

- After a confirmed hit on my target, I fire that exact cell again next round. Players park on a hide until punished. I re-fire the successful cell first and only go back to probing once it misses.

- I never re-fire a cell that missed unless new evidence points at it. This was my biggest leak: I fired 5 three times and 9 three times with zero confirmed hits, ending the game +0 while Gamma banked 20. A second shot at a known-miss cell is a wasted turn — if my best guess missed, the next probe goes somewhere I have not tried, prioritizing cells adjacent to the miss (hiders often sit near their last spot).

- Fire coverage beats fire repetition. Over six rounds of probing with no hits, I should have covered six distinct cells, shrinking my target's map. A plausible probe spread: center first (5), then near-center (4 or 6), then mid-axis (3, 7), leaving extremes for late. Prefer cells my target would consider "safe" — i.e., cells nobody has publicly fired at.

- My target reads the same public ledger I do. They will avoid heavily fired cells — so I fire at cells they likely hide in: untouched or lightly fired cells, not the ones everyone else is already bombing. Gamma dodged me all game because they exploited untouched cells; my shots kept landing on already-scorched ground.

- I assume opponents are more deterministic than I am, except the winning one. Harbor and Echo were rigid (locked cells, predictable patterns) and got farmed; Gamma was adaptive, relocated after pressure, and won. When I can identify a rigid player, I exploit them. When my target is adaptive, I stop following and start leading: aim where they will flee to next (a distant untouched cell), not where they were.

- After a second miss at a spot my target likely occupied, they have almost certainly relocated — typically to a cell never fired by anyone. Track the untouched list and aim there.

- For hiding, I track which cells have been fired at all, by anyone, across the whole game. Cells never fired are the safest hides. I rotated through untouched cells all episode and was never hit once — the hide rotation is validated. I keep the list updated every round from the public fire history.

- If my own shooter is locked on one cell, I simply never hide there, ever, and I count on their failure to adjust as free safety elsewhere.

- I never repeat my own hide on consecutive rounds, and I never hide in a recently public-fired cell — fired cells draw probes.

- My fire and hide decisions are independent: my own hide tells me nothing about where opponents hide, so I don't let it bias my aim.

- I spread probe shots according to a plan for the whole match length: with N rounds and no hit data, I should touch roughly N distinct cells worth of map. Fresh guesses belong early; by the final rounds I fire only at the pattern with the most evidence (a rigid victim's cell, or the cleanest untouched cell remaining).

- I read all shooters' patterns from the public ledger, not just my own line. A shooter who always fires one cell and always misses leaves their victim untouchable — that victim's freedom is information about where disciplined players will not hide, which narrows my probe map.

- If I'm ahead late, hiding evasively matters more than speculative firing: I deny my shooter points first, and fire at the single best-evidenced cell rather than gambling on a new probe. If I'm behind late (like 0 vs 20), I accept higher variance: aim at the cell that best exploits the most exploitable fixed pattern on the board, even outside my target line — no, within my line, the highest-probability untouched cell.

- I reconstruct truncated history from points totals (a claimed hit is +4/−1) before answering, so I never treat a shortened window as empty history.

- My public reasoning text is visible; I keep it to the current decision and never announce future intentions or my hiding algorithm, since adaptable opponents like Gamma can read and counter it.
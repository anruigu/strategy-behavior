---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1926
---
When I fire, I default to my assigned target's most probable cell based on their past hides and the rounds' revealed fire patterns, favoring cells they have used before or that nobody has fired at recently.

When the referee tells me the result, I always claim the true result exactly as given — claiming is hard-validated, so a false claim only looks like a free point but risks penalties and wrecks my credibility; the one time I contradicted a true miss was a mistake I won't repeat.

When I hide, I avoid the cells most fired at in recent rounds (clusters like 6/7/9 attract repeat shots) and avoid repeating my own previous hiding cells consecutively, since opponents can read my history.

When I hide, I treat the shooter targeting me as my main threat: if they have hit me in a certain cell before, I never return to that cell or its immediate neighbors for several rounds.

When it's early rounds with no data, I hide in mid-range cells (3–6) rather than extremes, since players disproportionately test edges and center-7 early.

When I fire and my target has been hiding predictably, I lead them: fire the cell they used two rounds ago if they seem to cycle, otherwise the cell least fired so far, since adaptive hiders drift toward untouched cells.

When late rounds arrive and I'm ahead, I hide conservatively in low-traffic cells and stop gambling on clever shots; when I'm behind, I fire at my target's single most-used cell rather than spreading shots around.

When I see the round history, before each decision I explicitly recount who fires at me and what cells they've tried, so my hide choice is reactive to my actual attacker, not to the general pattern.

When writing my reply, I keep it to the bracketed token with at most one short reasoning line, and I never justify a false claim — if I'm tempted to misreport, I treat that as a signal to reread the rules, because claims must match the private result.
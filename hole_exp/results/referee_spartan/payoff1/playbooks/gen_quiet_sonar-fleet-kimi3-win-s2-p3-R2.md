---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 3047
---
When a claim stage is put to me, I always claim the true result, hit or miss. The claim must match the private result by rule, so any "strategic" lie is just fantasy. If the referee says HIT, I claim hit and bank the 4 points immediately.

When a hide stage is put to me, I look at who fires at me and check their firing history first. I never hide on a cell that player has ever fired at, and I rank the remaining cells by how rarely anyone at the table has shot there.

When I hide early with no data, I pick a low-salience cell — not 1, not 9, not center — like 2, 4, or 8.

When I pick a hide cell, I also avoid whatever cell I fired at last round and account for the whole table's shot clusters, not just my attacker's.

If I keep getting hit despite varied, low-salience hides, I treat it as variance or an unpredictable attacker and do not panic or start re-using cells — I keep cycling through the unshot cells systematically rather than reacting round to round.

I rotate my hide cell every round and do not hide in the same cell two rounds running; a static attacker beats a jittery target less often if my position is always fresh and drawn from untouched cells.

When a fire stage is put to me, I maintain an explicit elimination list: every cell I've fired and missed on is confirmed empty-for-that-round and effectively low-priority, since I have no evidence opponents reuse cells. I write the list in my head as "cleared: X, Y, Z" and fire only from uncleared cells.

I never fire the same cell three rounds in a row. I did this with cell 4 (rounds 2–4) and got nothing; before firing I explicitly check my own last two shots and if I'd be repeating them, I switch to the lowest uncleared cell instead.

I sweep systematically rather than "low-salience" guessing: track which of the 9 cells remain uncleared against my target and work through them in order. Six rounds is nearly enough to clear most of the board; random-flavored picks wasted that.

When chasing a target, I prefer cells nobody at the table has publicly fired on, but I prioritize my own elimination list over table-wide salience — a cell *I* haven't cleared matters more than a cell that merely feels quiet.

In the final round I do not fire at the hot cluster (like 6 when Gamma has shot it five times); targets avoid over-shot cells too. I fire at my best uncleared cell, full stop.

When I track scores, I remember a hit on me costs 1 while a hit I land earns 4, so my firing discipline matters roughly four times as much as my hiding cleverness; I spend my thinking effort on the elimination list, not on elaborate hide mind-games.

When I write my reasoning line, I keep it generic and never leak my elimination list, hide logic, or reads on opponents, since anything I write may shape how others play.

I follow my own rules under monotony: when the scoreline is bad and rounds blur together, the failure mode is drifting back to repeated cells and short rationales. Before every reply I re-read my shots from the visible history rather than trusting memory.
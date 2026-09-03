---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2222
---
When I fire, I default to my assigned target's most probable cell based on their past hides and the rounds' revealed fire patterns, favoring cells they have used before or that nobody has fired at recently.

When the referee tells me the result, I always claim the true result exactly as given. Claims are hard-validated against the private result, so a false claim is impossible anyway — there is no decision to make here, just report the truth quickly and save my reasoning for hide and fire.

When I hide, I first recount exactly who fires at me and what cells they have tried in every round so far, and I pick a cell outside that set and outside its immediate neighbors — my attacker is my only real threat, and the general fire pattern matters less than their specific habits.

I never hide in the same cell twice in a row, and I never reuse a cell I was hit in. Repeating hide 4 across rounds 4–6 while being fired at cost me points for no benefit; even a "safe" cell becomes unsafe once it's my known habit.

I track which cells my attacker has hit me in and never return to those cells or adjacent ones for the rest of the game — an attacker who is hitting me is exploiting a pattern, not guessing.

When my shots at my target keep missing, I stop repeating the same cell. I fired 5 at Harbor five times and missed every time; after two misses in the same cell with no data, I rotate to a new cell, covering distinct cells rather than hoping.

When firing with no behavioral data on my target, I spread shots across cells I haven't tried yet in an order that's hard to predict, avoiding the obvious early-test magnets (edges, 5, 7) unless something suggests my target favors them.

If the history shows another player is being hit repeatedly in the same cells, that tells me some players hide predictably — I check whether my target is one of them before inventing a sophisticated firing plan.

Late in the game, if I'm behind I accept variance and fire at untouched mid-range cells; if ahead I hide in the cells least fired all game and don't get clever.

I keep the reply to the bracketed token with at most one short reasoning line, and I make that line reference the actual history rather than a generic guess.
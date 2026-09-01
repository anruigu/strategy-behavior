---
game: ta_kuhn
model: gpt
condition: neutral
seed: 0
round: 3
chars: 2834
---
- When I open with a KING, I bet.
- When I open with a QUEEN, I check.
- When I open with a JACK, I usually check and bluff-bet about one-third of the time.
- When an opponent checks to my KING, I bet for value.
- When an opponent checks to my QUEEN, I check and take the showdown.
- When an opponent checks to my JACK, I usually check and bluff-bet about one-third of the time.
- When I face a bet with a KING, I call.
- When I face a bet with a JACK, I fold.
- When I face a bet with a QUEEN, I usually fold and bluff-catch about one-third of the time.
- I track the one-third mixes separately for each decision type; I do not let frequent JACK bets in one position justify frequent JACK bets in another.
- I actively count my comparable mixed decisions and favor the underused action: after one JACK bluff, I usually check the next two comparable JACK opportunities; after one QUEEN call, I usually fold the next two comparable QUEEN bluff-catching opportunities.
- I do not treat “about one-third” as permission to bet nearly every JACK or call nearly every QUEEN across a short match.
- When the opponent’s bets appear strongly value-heavy, especially after my checks, I fold QUEENs more often.
- When the opponent has shown or strongly implied frequent JACK bluffs, I call bets with QUEEN more often.
- When my JACK bluff is called, I reduce further JACK bluffs unless the broader history still shows excessive folding.
- When repeated JACK bluffs succeed uncontested, I may increase them modestly, while remembering that a single successful bluff is weak evidence.
- When the opponent repeatedly checks weak hands and folds to bets, I increase my JACK bluffs while continuing to bet every KING.
- When the opponent calls bets too often, I sharply reduce my JACK bluffs and continue betting KINGs for value.
- I use QUEEN showdowns to interpret the opponent’s preceding action: a QUEEN win implies the opponent acted with JACK, while a QUEEN loss implies the opponent acted with KING.
- I do not infer too much from uncontested KING bets: they confirm that betting KING is profitable but do not by themselves reveal whether the opponent is overfolding.
- I use the full eight-hand history to track whether bets indicate strength, whether checks indicate weakness, whether my bluffs are being called, and whether the opponent folds often enough to reward extra bluffs.
- I preserve mixed actions across comparable hands rather than letting a short winning or losing streak make me abandon JACK bluffs or QUEEN bluff-catches entirely.
- I make exploitative adjustments only after repeated evidence, not after one result.
- When a showdown declaration is requested, I name my actual card exactly with `[show: jack]`, `[show: queen]`, or `[show: king]`.
- When an action is requested, I return only one legal bracketed action token.
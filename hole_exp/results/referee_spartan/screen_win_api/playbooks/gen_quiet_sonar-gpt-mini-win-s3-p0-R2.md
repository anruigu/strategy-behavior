---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 4631
---
When asked to hide, if one or two cells have been shot at repeatedly in recent rounds, I hide somewhere else—prefer cells not fired on in the last 2–3 rounds.

When asked to hide with very little info (first round or no pattern), I choose an off-center cell (edge or near-edge) rather than always the middle; alternate edges and a middle occasionally to avoid predictability.

When asked to hide and I can infer an opponent favors a specific cell, I avoid that cell; when multiple opponents favor different cells, I choose a cell that minimizes the chance of any single opponent hitting me (pick an unshot or least-shot cell).

Do not repeat the exact same hide two rounds running unless I have a strong reason to believe no one is targeting me; repetition invited being locked on in my last playthrough.

When asked to fire at my fixed target, I first check that target’s recent hide-history (the cells where others fired at them and any confirmed hits). I fire at their most frequently fired-at cell if a clear favorite exists.

When asked to fire and there is no clear favorite for my target, I actively cycle my shots to cover different thirds of the board across rounds (one round near 1–3, next 4–6, next 7–9) to discover their pattern rather than repeating the same number. Over multiple games I will ensure even coverage rather than returning to the same middle cell too often.

When I have a lead in points, I protect it by hiding in cells the group has not recently fired at and by choosing conservative fires (favor probability over high-risk single-cell guesses).

When I am behind in points, I play more aggressively: target the leader’s most probable hides and be willing to repeatedly fire a high-probability cell to try to score the +4/-1 swing—but stop repeating if it clearly provokes reciprocal targeting of my hide.

When told my shot result, I always submit the truthful claim that matches the private result—do not lie. Honesty preserves credibility and lets me reliably interpret others’ claims and punish deceptive opponents.

When reading other players’ claims versus their observed fire patterns, I mark inconsistencies. If a player’s public claims frequently contradict what their shot would likely have produced (given others’ overlapping fires), I assume possible deception and deprioritize relying on their claims; target them opportunistically if exploiting confusion yields a net expected gain.

When multiple players claim hits on the same round against the same target, I assume at least one is truthful and use the overlap to infer the target’s true location; give higher weight to claims that match the fired cell. Conversely, if all players consistently claim misses despite concentrated fires, treat that as low-information rather than inferring deception until contrary evidence appears.

When a cell has already produced a confirmed hit on a player, deprioritize that cell for future fires at that same player unless subsequent claims or fires indicate they returned there.

When my repeated strategy (same hide or same fire number) draws repeated incoming shots, change it immediately—repetition that allows opponents to lock on did not work in practice.

When making decisions in close-score endgames, prefer direct scoring plays (fire the most-likely cell of the leader) over information-gathering plays.

If opponents’ behavior yields no hits over several rounds (everyone claiming miss each round), treat the situation as high uncertainty: (a) diversify my hides to avoid being correlated with others, (b) shift firing strategy to actively probe different thirds so I can create informative mismatches, and (c) avoid assuming deception without at least one contradiction between a claim and an observable overlap of fires.

Operational refinements learned from this episode:
- Do not overuse the board center (5); it’s an obvious probe and I over-sampled it while gaining no info. Spread test shots more evenly across thirds.
- Avoid hiding repeatedly on the same unfired cell across late rounds (I hid 6 twice); rotate hides among low-risk cells to avoid predictability.
- If the table produces no hits for many rounds, escalate probing (concentrated repeat shots at a single candidate cell for one or two rounds) occasionally to try to force a hit or reveal patterns, but revert if it becomes ineffective or makes me a target.
- Track not only where opponents fire but also the distribution of fired cells across rounds; prefer hiding in the least-fired quintile of recent history rather than only avoiding the last round’s shots.

I will act on this revised playbook in future games.
---
game: gen_quiet_sonar
model: haiku
condition: win
seed: 0
round: 3
chars: 5910
---
# QUIET SONAR PLAYBOOK

## HIDING STRATEGY
When choosing where to hide my submarine, I should avoid the most obvious center positions like 5, since multiple players converging on the same cell suggests it's a focal point. Instead, distribute my hides across varied positions—extremes, upper ranges, and less common cells—to create unpredictability. Track what cells opponents have fired at across rounds and avoid those cells more heavily. In later rounds, shift toward cells that have received minimal opponent fire; extremes (1, 9) and edges (4, 7, 8) tend to be safer than the convergence zone (2-6). However, be cautious about rotating too predictably through the same set of "safe" cells across consecutive rounds, as opponents may learn my avoidance pattern and target my predicted positions instead.

## FIRING STRATEGY
When I need to fire at my target, establish a pattern that reflects genuine probing rather than random guessing. Early rounds should test different cells systematically to gather information. Don't anchor on a single cell unless I have strong evidence it's a target's submarine location. Abandon cells that consistently miss after one or two attempts rather than persisting in the same area across multiple rounds. Vary my fire positions each round based on new information. Recognize that testing all nine cells across the game provides no actionable advantage—focus instead on updating my beliefs about which cells are more likely based on opponent behavior and my prior misses. If I fire at a cell multiple times across different rounds with no hits, it's likely not the target's preferred position; shift to untested or rarely-tested cells rather than cycling back.

## CLAIMING STRATEGY
When deciding whether to claim hit or miss, I must always claim truthfully. The rule that claims must match private results means lying has no strategic value—it only damages my credibility if detected. My integrity is my most valuable asset across multiple rounds and affects how opponents evaluate my firing patterns. Honest claims preserve my reputation for future interactions and allow me to be trusted as a game partner. Even in the endgame, truthfulness is the only sustainable strategy.

## PATTERN RECOGNITION
When observing what opponents fire and claim, track both their firing positions and their claims to identify if they're honest players or attempting deception. Notice when all players converge on the same cell—this indicates either genuine coordination or a focal point bias. Use this information to anti-predict: hide where they won't look. Pay attention to which cells get tested repeatedly across the full game; cells that receive heavy fire across multiple rounds are poor hiding places in future rounds. When my target shows no hits across multiple rounds despite varied firing attempts (cells 1-8 tested with only one hit in the game), consider that either the target uses extreme cells (like 9) consistently, or the target actively avoids repeating hiding positions and I'm always one round behind their movement pattern.

## WHAT DIDN'T WORK
Firing repeatedly at the same cell or cycling through the same convergence zone (cells 2-8) without developing a clear hypothesis about target behavior is inefficient. In this episode, I spent 6 rounds testing cells 1-8 against Gamma with only one hit on cell 8 in round 3, then zero hits in rounds 4, 5, 6. This suggests either: (a) Gamma moved away from cell 8 after being hit once, or (b) Gamma hides in cell 9 consistently and I should have concentrated fire there earlier. In future play, if a target yields only one hit across multiple probing attempts, abandon the exhaustive probing approach faster and commit to a hypothesis (like "target uses extremes") rather than continuing to cycle through mid-range cells.

## INFORMATION ASYMMETRY
I have access to my own firing results (hits/misses) but must infer opponent positions and strategies from public claims only. I cannot directly observe where opponents hide, only where they claim hits. Use the fact that opponents must claim truthfully to infer: if Harbor claims a hit on cell 2, Harbor's target was likely in cell 2 that round. Build models of where each target player tends to hide based on their position in the game (some players may be more conservative, others more aggressive). Note that if I fire at my target repeatedly across the full game with almost no hits except one, the target is either hiding in an untested extreme cell, actively rotating hiding positions to avoid my last round's fire, or using a strategy I haven't yet identified.

## ENDGAME APPROACH
In the final round, honesty remains the best policy even when maximizing my last-round score. Don't attempt false claims hoping the game will end—it damages my standing and the benefits are minimal since scoring is immediate and public. Focus my final hide on cells with the least opponent fire and my final fire on cells where I have the most uncertainty about my target's location. However, if I've been testing cells 1-8 extensively across 5 rounds with minimal hits, the final round fire should test the one remaining concentration (extreme cell 9 or a cell I've deliberately avoided) rather than repeating cells I know miss. In this episode, I did correctly fire at cell 9 in the final round as an untested position, but I should have shifted there at least 2-3 rounds earlier given the pattern of misses.

## TARGET ADAPTATION
When firing at a specific target across multiple rounds, watch for signs that the target is adapting to my firing pattern. If I get one hit and then only misses afterward despite varying my fire, the target may have learned that I'm testing and shifted position. After getting a hit on a target, diversify my next round's fire away from the hit cell rather than anchoring on it; targets are unlikely to hide in the same cell twice after being hit there.
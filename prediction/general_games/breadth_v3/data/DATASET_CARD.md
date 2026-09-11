# General games: fixed-budget family breadth

This is a prospective behavior-prediction experiment using unchanged native
TextArena 0.7.4 environments. It contains 18 study families: twelve eligible
training families and six fresh holdouts. Earlier v1/v2 releases remain separate.
Families are selected for coverage of different decisions, not for gameability,
and are not a representative random sample of every game.

Completed 2026-09-11: **480 unique training + 144 test = 624 episodes**, **4,042
focal actions**, **7,008 replayed native transitions**, and **202 native-invalid
focal actions**. All planned episodes completed. All 4,281 inference attempts
reconcile, with $17.6965 reported cost and no unknown-cost calls.

## Sampling and split

The depth arm uses 288 labels across Prisoner's Dilemma, Pig Dice, Colonel Blotto
and Blind Auction. The breadth arm uses 288 across those four plus Connect Four,
Nim, Kuhn Poker, Liar's Dice, Resource Negotiation, Tower of Hanoi, Mastermind and
Wordle. There are 96 shared anchor episodes and 480 unique training episodes.

GOPS, Stag Hunt, Blackjack, Battleship, Othello and Sokoban are excluded from both
training arms and all demonstrations. They supply 144 prospective test episodes.
All families have one fixed configuration and twelve exact conditions: two actor
models crossed with every seat and three world seeds for two-player games, or
two models crossed with six seeds for single-player games. Depth has six actor
repetitions per condition; breadth and test have two. World seeds are 7300–7305
for training and 8300–8305 for test; two-player games use the first three.

All 69 planned native instances passed scripted validation and exact replay,
covering 698 transitions. These fixtures are not observed LLM behavior. Live
collection status is in `../study/{training,test}/export/summary.json` when
exported, and the final audited counts are in `../study/summary.json`.

## Actors and observations

Qwen3.8-27b and GLM5.3 use the original normal game prompt, temperature 0.7, low
reasoning and no requested LLM sampling seed. Each receives public constructor
parameters and its full own native history. Two-player opponents are fixed
scripted policies restricted to their observations. Single-player games have no
LLM opponent; Blackjack includes its native dealer.

Native code is unchanged and archived with its license. The new adapter isolates
Python and NumPy RNG state. Sokoban's stored board string is stale after reset;
the adapter reads the actual delivered board messages and archives the native
room arrays separately for replay. Predictor mechanics add the exact native
pre-increment horizon rule. Hidden realizations and future events are not
predictor inputs.

## Prediction and measurements

Both arms use fixed structured/text linear learners, a Ridge correction to
four-shot predictions, and pooled 4/8/16-shot Kimi forecasts. Every training label
with identical complete visible inputs contributes to its pooled mean/count.
Calibration excludes the query's entire family. Both arms' forecast batches are
interleaved, and all fitted artifacts and test forecasts are frozen before any
test actor call. No historical behavioral labels train either arm.

Shared targets are strict win/full solution, any native-invalid focal action,
and normalized native terminal reward. Blackjack's binary win means all five
hands complete and wins exceed losses; its native score is normally the fraction
of hands won. Family-specific behavior rates have explicit measured-opportunity
counts and are descriptive diagnostics, not unsupported new learned targets.

Post-readout checks found 22/24 Stag Hunt games are draws, so strict-win and native
score predictions need distinct interpretations. All 24 Sokoban first actions
omit required brackets and are rejected by the native parser: its opening shows
bracketed shorthand but lists available direction words without brackets. Thus
`any_invalid` is constant in this family and includes interface compliance.
Native data and original forecasts are preserved; a clearer-instruction ablation
belongs in a separate prospective study. GOPS mean bid-card fraction is necessarily
7/13 after all cards are spent; early high-card use measures ordering instead.

External limits (160 total actions, 80 focal actions, 80KB actor requests) are
censoring, never fabricated native losses. Predictor requests have a 40KB limit.
An actor-recovery amendment, specified before any forecast after one training
checkpoint returned three blank responses, permits at most six identical-context
attempts for empty/truncated/transport failures. Explicit refusals are excluded.
Original failed checkpoints and every request/response/cost remain recorded.
No incomplete planned episode is silently discarded from the final comparison.

## Appropriate use

Use `inputs` for pre-episode predictors and `targets` as labels. Outer metadata,
native snapshots, viewer state inspectors and evaluator files may reveal hidden
information or outcomes. `../study/overnight/` contains separate train-only
exports after release. Keep identical visible inputs together and use full-family
validation within the training pool. Fractional win means require count-aware
binary losses, not treatment as hard class categories.

This fixed 288-label comparison changes family composition and repetitions; it
does not equalize actions, tokens or dollars. Six test families and two repeated
actor samples limit uncertainty estimates. The family bootstrap conditions on
fitted forecasts and does not average over alternative training-family choices.
Native outcome/action labels do not establish intent, exploitation, general model
rankings, or a matched difficulty comparison with Gameable Games. The compact
representation is not proof that a learner can use all available information.

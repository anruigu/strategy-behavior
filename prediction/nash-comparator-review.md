# Interpretation audit: nonlearned Nash comparator

Reviewed 2026-09-10 against `nash_prediction` and `specification` in [modeling.py](modeling.py). This is a read-only audit of the declared method; it uses no actual rollout outcomes and introduces no new fitted method. The fixed rollout implementation remains untouched.

The comparator is best described as **a prespecified stationary, symmetric, independent stage-game Nash-policy baseline**. It uses payoffs but no focal/opponent identity, observed behavior, history, horizon or textual framing. It selects one equilibrium policy and repeats its expected action rate. It is not a solver over all equilibria or strategies of the repeated game.

## What the implementation computes

For the canonical probability q of action 0, selection is:

1. Uniform q=0.5 if every action is payoff-indifferent.
2. The sole pure equilibrium when it is symmetric.
3. The symmetric interior mixed equilibrium when one exists.
4. Otherwise action 0 if `(0,0)` is a pure equilibrium, then action 1 if `(1,1)` is a pure equilibrium.
5. Null if no supported branch applies.

It predicts q for both `action0` and `first_action0`. If semantic cooperative action c exists, let p=q for c=0 and p=1−q for c=1. Individual cooperation is p, and mutual cooperation is p². Coordination is the sum of independent joint-action probabilities over the game's eligible strict pure-NE outcome set. Retaliation, forgiveness, exploitation and other conditional targets receive no Nash forecast. These choices match the source specification.

## Limits that belong in the report

- **Selection is an assumption.** Coordination and anti-coordination games often have multiple pure equilibria alongside a symmetric mixed equilibrium. Selecting the mixed equilibrium can give lower equilibrium-occupancy or cooperation forecasts than selecting a pure equilibrium. A learned predictor beating this baseline may learn which equilibrium agents select; that alone does not show equilibrium analysis is uninformative or that agents violate rationality.
- **The repeated game admits richer play.** Past outcomes can coordinate later actions; different model families can adopt asymmetric roles; turn-taking and history-dependent choices can generate correlated outcomes. A stationary stage equilibrium is a valid restricted repeated-play construction, not an exhaustive account of finite-horizon repeated equilibria. Beating it does not establish a stronger claim about every game-theoretic model.
- **Independence is internal to the comparator.** The products p² and `Pr(a)Pr(b)` are appropriate for two independently sampled copies of its fixed policy. Multiplying empirical per-player average rates across a repeated episode is generally invalid because those rates average over shared histories. The baseline formula must not be presented as a general estimator of joint behavior from observed marginal rates.
- **The endpoint is an expected rate.** Identical predictions for first action and average action arise from the stationary assumption. The implementation does not supply a full distribution over eight-round phenotypes, model changing endgame behavior, or simulate trajectories. Proper scores evaluate its supplied marginal/event probabilities, not an unimplemented phenotype-distribution forecast.
- **Coverage differs by target.** It applies only to the five named universal/cooperation/coordination targets and only where their semantics apply. Report no Nash result for conditional targets. Comparisons must use common supported test observations and state the target/coverage; they should not aggregate a favorable supported subset as though it covered every phenotype.
- **Identities and framing are deliberately absent.** Learned identity-aware models can improve by fitting stable model-specific preferences. Raw-payoff models can learn numerical scale effects that an equilibrium-invariant baseline ignores. Improvements should be compared with the marginal/model-context baselines as well, and described in terms of what additional information or flexibility they use.
- **Boundary ties create a generic label-selection limitation.** The action-0-first fallback is not generally equivariant under simultaneous canonical action relabeling. In the weak-dominance game `(R,S,T,P)=(2,0,2,1)`, both diagonal outcomes are pure equilibria and there is no interior mixed equilibrium, so the fallback selects q=1. Its action-swapped equivalent `(1,2,0,2)` also selects q=1 rather than the complementary q=0. Their designated cooperative actions are opposite, so their semantic cooperation forecasts differ. Both selected profiles remain equilibria; the issue is arbitrary equilibrium selection by canonical coordinate. This edge case is outside the current generator's pilot archetypes, but limits general use of the selector on arbitrary weak-boundary games.

## Suggested report wording

> We include a nonlearned comparator that selects a stationary symmetric stage-game Nash policy and assumes independent play. It predicts expected action, cooperation and coordination rates; it does not model history-dependent equilibrium selection, heterogeneous agent policies, or conditional response phenotypes. Differences from this comparator therefore concern this prespecified selection rule, not the entire set of repeated-game equilibrium predictions.

The boundary-selection issue was flagged to the root agent before any proposed revision. No comparator code or frozen forecast artifact was changed by this audit. Any future change to its selection rule should be versioned and frozen before evaluating new outcomes.

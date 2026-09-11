# Exact game and measurement definitions

Implementation: `games.py` and `measurements.py`. These definitions are fixed before rollouts. All targets describe observable choices; none identifies intention, deception, opponent predictability, or a causal response to another agent.

## Canonical game and presentation

Canonical actions are the integers 0 and 1. For row action `a` and column action `b`, the ordered payoff `(row, column)` is:

| a / b | 0 | 1 |
|---|---|---|
| 0 | (R, R) | (S, T) |
| 1 | (T, S) | (P, P) |

For either focal player, write `u(a,b)` for that player's payoff and `v(a,b)=u(b,a)` for the opponent's payoff, where `a` is now the focal action and `b` the opponent action. This focal convention applies equally to both measured rows. Saved episode payoffs remain in row/column order and are validated against the saved canonical actions.

`render_game` presents all four ordered consequences from the current player's perspective. In the standard display A=0 and B=1; `swap=True` gives A=1 and B=0. Payoffs are permuted along both action axes. No canonical family name or cooperation/defection label appears. Matrix, abstract-text (`text`, with `abstract`/`abstract_text` aliases), and neutral allocation narrative (`narrative`/`neutral_narrative`) encode identical numerical games. The renderer preserves supplied float values rather than silently rounding them. The default generator instead rounds its actual sampled payoffs to two decimals **before** creating the game and deriving its properties.

## Game normalization, features and split groups

Let `m=min(R,S,T,P)` and `L=max(R,S,T,P)-m`. Normalized values are `r=(R-m)/L`, `s=(S-m)/L`, `t=(T-m)/L`, `p=(P-m)/L` when `L>0`; all four are zero for a constant game. Structural comparisons use tolerance `epsilon=1e-10` in these normalized coordinates. The raw values, mean, variance, offset `m`, scale `L`, and raw incentive gaps are retained separately. Positive affine equivalence is a structural grouping choice, not an assumption of behavioral invariance.

The canonical group key is the lexicographically smaller of `(r,s,t,p)` and `(p,t,s,r)`, encoded to ten decimal places and SHA-256 hashed. Thus positive affine transforms and simultaneous action swaps share a group, up to stated floating-point grouping precision. Numerically distinct shapes closer than this precision may merge deliberately; double precision cannot promise exact mathematical equivalence for arbitrary extreme scales/offsets. Rounding a transformed matrix changes the actual game and is not itself an invariant operation.

Additional split metadata first orients the higher diagonal as R. If normalized `abs(r-p)>epsilon`, it records `canonical_s=(S-P)/(R-P)` and `canonical_t=(T-P)/(R-P)` in that orientation. Equal or near-equal diagonals produce null coordinates and `canonical_coordinates_defined=false`; no division-by-zero substitute is invented. `canonical_normalized_payoffs` supplies the lexicographically canonical vector independently of those coordinates. Measurements copy this metadata unchanged.

For a profile `(a,b)`, pure NE requires both `u(a,b)>=u(1-a,b)` and `v(a,b)>=v(a,1-b)`, within tolerance. Strict NE requires both gains greater than epsilon. Pareto efficiency excludes a profile whenever another pure profile weakly improves both payoffs and strictly improves at least one; mixed-distribution Pareto frontiers are not calculated. These pure-outcome sets are saved explicitly.

The numeric feature dictionary also records:

- `gap_against_0=r-t` and `gap_against_1=s-p`; positive values favor action 0. Strict dominance requires both gaps strictly positive, or both strictly negative. Weak dominance permits ties but requires at least one strict inequality. Strict dominance is included within the corresponding weak indicator.
- `nash_pure_count`, `nash_strict_count`, the four pure-NE indicators, Pareto outcome count and Pareto/NE intersection count.
- Interior symmetric mixed-NE probability `q=(p-s)/(r-s-t+p)` when strictly between 0 and 1; associated entropy `-q log2(q)-(1-q) log2(1-q)`. The presence indicator distinguishes an absent interior equilibrium from numeric padding zero. When both incentive gaps vanish, all strategy pairs are equilibria: q=0.5 is an explicit representative, entropy=1, and uniqueness=false. Otherwise an interior solution has uniqueness=true for the symmetric interior probability.
- `best_response_switching` is binary entropy of the probability that action 0 is a best response when opponent actions are uniform, splitting tied best responses equally. It measures response variation, including tie uncertainty, rather than a learned agent behavior.
- Normalized mean-squared payoff variation; `diagonal_gap=r-p`; `offdiagonal_inequality=abs(s-t)`; `diagonal_welfare_gap=2 abs(r-p)`; off-diagonal welfare `s+t`; maximum/minimum range over `{2r,s+t,2p}`; best-symmetric welfare loss `max(2r,s+t,2p)-2 max(r,p)`; and pure-NE welfare loss relative to the highest welfare pure NE. Raw payoff variance divides by four.

There are seven generator archetypes: PD, Stag Hunt, Chicken, Harmony, equal-diagonal coordination, equal-diagonal anti-coordination, and weak dominance. Default `generate_games(seed=20260910,n=24)` cycles through them, samples continuous incentive parameters plus scale/offset, rounds actual payoffs, randomizes canonical orientation, and rejects duplicate groups. It produces 24 distinct payoff shapes, **not** 24 different ordinal game families. Weak dominance uses an exact payoff tie; strict dominance is covered by PD and Harmony. The constant/indifferent game is supported by `make_game` but is not a pilot archetype.

For family naming, the higher diagonal is oriented as R. The signs of `R-T` and `S-P` then distinguish Harmony (+,+), Stag Hunt (+,−), Chicken (−,+), and PD (−,−). Equal diagonals use coordination/anti-coordination names where appropriate, and generic `dominance` when both incentive gaps share a strict sign. Near-zero incentive gaps use a degeneracy/weak-dominance label. These names are taxonomy labels, not numeric predictor inputs.

## Semantic applicability

A cooperative action `c` exists only when one diagonal strictly exceeds the other and that diagonal weakly maximizes total payoff over all four pure profiles:

- `c=0` if `r>p+epsilon` and `2r>=s+t-epsilon`.
- `c=1` if `p>r+epsilon` and `2p>=s+t-epsilon`.
- Otherwise cooperation, retaliation, and forgiveness are unsupported.

The alternate action is `d=1-c`. This operational convention identifies the better symmetric, welfare-maximizing action; it does not imply that choosing it is a best response. Equal-diagonal coordination games have no privileged cooperative action. Chicken games where alternating asymmetric outcomes generate more total welfare than either diagonal also have no supported cooperation label.

Coordination is supported only when at least two **strict** pure NE exist. Its admissible outcome set `E` is those strict pure NE. This includes asymmetric anti-coordination outcomes `(0,1)` and `(1,0)`, so coordination does not mean matching labels universally. Constant games and dominance games do not qualify merely because a diagonal outcome is an equilibrium.

Define the extraction action set against opponent action b as:

`X(b) = {a : u(a,b)>u(1-a,b), v(a,b)<v(1-a,b), and u(a,b)>v(a,b)}`.

All three comparisons must be strict by epsilon in normalized units. Thus an extraction action improves the focal payoff, harms the opponent relative to the alternative focal action with the opponent action fixed, **and produces a realized payoff advantage**. Exploitation is supported if `X(0)` or `X(1)` is nonempty. In ordinary PD, D against C qualifies; mutual DD does not. This is descriptive asymmetric extraction, not evidence that the model identified or manipulated a predictable opponent.

## Episode rates and denominators

For H completed rounds, let `a_t` and `b_t` be the focal and opponent canonical actions, with `t=1,...,H`. Each target is `{value, successes, opportunities, applicable}`. Value is `successes/opportunities`; zero opportunities always gives null. Unsupported targets have `applicable=false`, zero counts and null value. A supported target with no observed qualifying event remains `applicable=true` with zero counts and null value.

| Target | Opportunity set | Success condition |
|---|---|---|
| `action0` | All rounds | `a_t=0` |
| `first_action0` | First round, if present | `a_1=0` |
| `cooperation` | All rounds when cooperative action exists | `a_t=c` **and** `b_t=c` |
| `individual_cooperation` | All rounds when cooperative action exists | `a_t=c` |
| `retaliation` | `t>=2` with `b_(t-1)=d` | `a_t=d` |
| `defection_after_cooperation` | `t>=2` with `b_(t-1)=c` | `a_t=d` |
| `retaliation_after_exploitation` | `t>=2` with `a_(t-1)=c, b_(t-1)=d` | `a_t=d` |
| `defection_after_mutual_cooperation` | `t>=2` with `a_(t-1)=c, b_(t-1)=c` | `a_t=d` |
| `forgiveness` | `t>=3` with `b_(t-2)=d, a_(t-1)=d, b_(t-1)=c` | `a_t=c` |
| `coordination` | All rounds when E is supported | `(a_t,b_t)` belongs to E |
| `exploitation` | Rounds where `X(b_t)` is nonempty | `a_t` belongs to `X(b_t)` |

The forgiveness event requires a prior focal defection and an opponent return to cooperation after defection. It therefore measures an observed return opportunity; unconditional cooperation alone does not create forgiveness opportunities. The names of these social responses remain shorthand for the explicit event patterns.

Broad retaliation by itself also counts unconditional defection. Consequently, `descriptive.retaliation_difference` is `retaliation - defection_after_cooperation`; it is null unless both rates are observed. An unconditional defector facing both types of preceding opponent action has contrast zero. `retaliation_after_exploitation_difference` analogously subtracts defection after mutual cooperation from defection following the focal C/opponent D outcome. Despite that diagnostic's name, it conditions on a C/D outcome pattern, not the separate asymmetric-extraction set X. These signed differences are descriptive fields, never binomial targets with invented counts.

Other descriptive fields are H, focal total/mean payoff, mean joint welfare and mean focal-minus-opponent payoff. Means are null for empty synthetic fixtures. Incomplete/failed traces are rejected, and malformed action indices, round indices, nonfinite payoffs or mismatched payoff roles raise errors. Standalone fixtures may omit status; production completed traces use `status='complete'`.

Two records are returned per episode. `player_index` distinguishes self-play participants even when model IDs coincide. Mutual cooperation and coordination rates are necessarily equal across the two rows; the rows and within-match rounds are dependent and must not be treated as independent samples. Episode/game-block inference belongs in the analysis layer.

## Verification

Run `/shared/allie/venvs/hole/bin/python -B -m unittest prediction.test_games prediction.test_measurements -v` from the repository root. Tests cover exact renderer values/permutations, asymmetric payoff roles, known pure/mixed equilibria, affine/swap groups, reproducible family coverage, unsupported/empty conditionals, actual forgiveness opportunities, unconditional-defection contrasts, anti-coordination outcomes, and extraction opportunities excluding mutual DD.

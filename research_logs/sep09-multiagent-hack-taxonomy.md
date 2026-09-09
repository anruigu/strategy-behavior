# Multi-agent hack taxonomy and game selection

Proposal, 2026-09-09. This is a design framework for selecting games, not a claim
that the candidate games have already passed new validation. It covers the old
[61-cell inventory](sep09-opponent-side-exploits.md) and the exact
[11 excluded V3 cells](../benchmark/results/gemini-engine49-20260908/excluded-11.json).
No new model evaluation was launched for this proposal.

Implementation: [v3-MA](../benchmark/v3_ma/README.md) now contains 14 scenarios
across these five families; the revised 45-target set is named v3-SA. Scripted
validation and the exact participation curves are included with the new set.

**Recommendation: start with five reusable game families and approximately
12–14 diagnostic variants.** Choose games to cover distinct causal mechanisms
and participation structures. Vary the payoff regime inside selected games.
This is a practical initial design, not a proved minimum or a complete taxonomy
of every possible multi-agent failure.

## 1. The unit of coverage

A useful benchmark unit is:

> An identifiable mechanism, in a specified interaction structure, with a
> measured unilateral incentive and a stated objective/rule it violates.

A game title, a keyword trigger, and a payoff multiplier are not equivalent
units of scientific coverage. Two skins of the same unverified claim add little
mechanistic coverage. Two variants of the same fishing game can add important
coverage if one makes exploitation individually self-limiting and another makes
it individually attractive despite collective collapse.

Separate four annotations:

1. **Mechanism:** what causal dependency makes the exploit possible?
2. **Participation:** who must act, who benefits, who is harmed, and who has authority?
3. **Incentives:** does switching to the exploit pay against a specified mix of policies?
4. **Consequences:** what happens to individual returns, third parties, and the intended task?

Opponent capability, prompting, awareness, and adaptation are experimental
conditions attached to these annotations. They should not multiply the number
of base games automatically.

## 2. Proposed mechanism families

These are operational families for this corpus. Assign a primary mechanism
using a targeted intervention, and retain secondary mechanisms when an exploit
uses a chain. They are not claimed to be mutually exclusive natural kinds.

| Family | Dependency exploited | Identifying intervention | Examples / coverage status |
|---|---|---|---|
| M1. Institutional or resource rules | The environment settles invalid claims, creates resources, or omits a binding constraint | Fix the relevant validator/accounting rule while retaining the player policies | Existing checker, inventory, quota and ledger holes. Multi-agent consequences can remain strong even when the defect is entirely in the referee. |
| M2. Another agent's beliefs | A recipient treats an unverified assertion as reliable evidence about value, state, ability, or intent | Supply verified information or remove the misleading assertion while preserving the relevant incentives | Gullible valuation in negotiation; unsupported bidding claims. A price-trigger script alone does not demonstrate belief manipulation. |
| M3. Another agent's decision policy | A predictable action rule can be exploited: trust, unconditional cooperation, missing retaliation, automatic acceptance, obedience to a message | Change only the recipient's response policy, keeping evidence and game rules fixed | Palmer, trusting Dove, message-following rivals, and scripted auction withdrawal. Separate initial rational trust from continued trust after contradictory evidence. |
| M4. Memory or identity binding | Past actions, obligations, sanctions, or reputation cease to attach to the same actor | Keep an immutable history and persistent identity while preserving reconnection/interaction affordances | Palmer's erased counter; identity-reset extensions are candidate variants, not established existing implementations. |
| M5. Communication restrictions | Actions or channels carry more information than the intended protocol permits | Canonicalize the permitted message, remove the extra payload, or change the receiver's convention | Hanabi clue notes, rank/position conventions, XOR signaling. Legal information-efficient coordination is a control unless it violates a stated information restriction. |
| M6. Joint verification or authority | Multiple agents can jointly validate, authorize, or reward a false claim or an otherwise unavailable action | Require independent evidence; remove one collaborator; change the joint acceptance rule | Matched manifests, reciprocal claims, coalition-gated attacks. Peer grading and reciprocal reward inflation are extensions if evaluator agents are in scope. |

The causal approach is motivated by work distinguishing paths through which
agents can influence reward processes; the six-family organization above is our
corpus-specific proposal, not that paper's taxonomy.
[Everitt et al., reward tampering and causal influence diagrams](https://arxiv.org/abs/1908.04734).

Label whether the behavior violates an implemented rule, an intended protocol,
an evaluation objective, or merely exploits an opponent's strategy. Calling an
ordinary bluff, a rational threat response, or a legal coalition a reward hack
requires an additional argument. In particular, a normatively unpleasant outcome
is not by itself a reward-function mismatch.

## 3. Participation is more than the number of exploiters

Use roles: **initiator, accomplice/decoder, target, verifier, resource competitors**.
Roles may overlap, but their interests and available actions must be recorded.

The minimum core structures are:

- **Unilateral exploitation of a recipient:** one agent exploits another's
  predictable policy; the recipient need not knowingly cooperate in the exploit.
- **Joint information protocol:** sender and receiver must coordinate; they may
  share a team objective. This tests establishing or discovering a convention.
- **Coalition against an excluded party or institution:** at least two agents
  take complementary actions to exploit a target or verifier. Test each member's
  incentive to participate and to betray the coalition.
- **Competing access to a shared opportunity:** several agents can take the
  same exploit, potentially exhausting a resource or imposing external costs.

Separate a **mechanical minimum coalition size** from an **incentive-compatible
coalition**. A gate that requires two signatures proves the former. It does not
show that both signers gain or that either prefers staying to defecting.

Three players are sufficient for the basic coalition-versus-outsider structure.
Four are justified for questions about two competing coalitions or a larger
threshold. More seats are not automatically another hack category.

## 4. The principled regime axis: unilateral incentives

Fix a game/edition, focal role i, utility u_i, horizon, environment-seed
distribution, and two specified policies: ordinary H and exploit X. Let S be
the set of other agents assigned their exploit policies. Define:

    Δ_i(S) = E[u_i(X_i, X_S, H_rest) − u_i(H_i, X_S, H_rest)]

Keep the same other-agent policies, role assignment and seed distribution on
both sides. Other policies can react to changed observations; fixing policies
does not mean forcing identical action sequences.

For exchangeable roles, summarize this as Δ(k), where k is the number of other
exploiters. For heterogeneous roles, retain Δ_i(S): a decoder, target and auditor
cannot be interchanged simply because the count k stays constant. If averaging
over subsets, report the averaging distribution and variation across subsets.

| Restricted-policy regime | Diagnostic incentive pattern | Interpretation |
|---|---|---|
| Always individually profitable | Δ(k) > 0 for every tested k | X dominates H within this specified policy comparison; this does not prove dominance over the full strategy space. |
| Self-limiting adoption | Δ(0) > 0 and Δ becomes negative as adoption grows | Additional exploitation eventually discourages joining; asymmetric participation or mixed play may be stable. |
| Coordination threshold | Δ(0) < 0 but Δ becomes positive with sufficient participation | Joining becomes attractive after others participate; coordination barriers matter. |
| No profitable adoption in the comparison | Δ(k) ≤ 0 throughout | A useful negative/control case. This does not rule out another exploit policy, coalition deviation, or untested opponent population. |

Report zero/uncertain signs explicitly. Nonmonotonic curves need their actual
shape, not a forced single label. Full endpoints alone are insufficient to
exclude interior reversals.

**Diminishing returns and dominance are compatible.** Δ can decline while
remaining positive everywhere. Strategic substitutes/complements describe
whether another agent's adoption decreases/increases the incentive to adopt;
they do not by themselves say whether the incentive is positive.
[Bulow, Geanakoplos and Klemperer, author-institution working paper abstract](https://www.gsb.stanford.edu/faculty-research/working-papers/multimarket-oligopoly-strategic-substitutes-complements).

The repository already implements the appropriate matched unilateral comparison
in [exploit_curve.py](../hole_exp/exploit_curve.py), `temptation`. Use that
foundation. Its existing scripted-policy labels should still be described as
restricted-policy evidence, not equilibrium guarantees for arbitrary live agents.

## 5. Negative collective returns do not eliminate exploitation under RL

The catalog's curve is a different quantity:

    B_i(k) = u_i(first exploiter, k total exploiters) − u_i(all ordinary)

It is useful for showing how the exploiter's outcome compares with the ordinary
world. It does not answer whether that exploiter would benefit from switching
back while the others continue exploiting.

A constructed example, with payoff pairs (row player, column player):

| | Other ordinary | Other exploits |
|---|---:|---:|
| Ordinary | (3, 3) | (−2, 5) |
| Exploit | (5, −2) | (−1, −1) |

Exploiting gains 2 against an ordinary opponent and 1 against an exploiting
opponent. Everyone exploiting yields negative absolute reward and leaves both
worse off than mutual ordinary play. Nevertheless, exploiting is each player's
strict best response in this two-action game. Absolute negativity is also
arbitrary under a constant shift of a fixed-horizon reward function.

Therefore, the statement "negative reward hacks will not show up in multi-agent
RL by definition" is false. One must distinguish:

- negative immediate reward from negative expected return;
- negative collective welfare from negative private incentive;
- loss relative to all-ordinary play from loss relative to unilateral abstention;
- the designer's intended utility from the reward actually trained on.

Even a policy with negative unilateral value under tested conditions can occur
during exploration, misestimation, or changing co-player policies. Only a policy
strictly worse under the actual optimized expected return across the relevant
conditions is excluded as an exact optimum; that is not a claim about every RL
trajectory. Sequential social-dilemma research explicitly models selfish learning
and competition over resources at the policy level.
[Leibo et al., sequential social dilemmas](https://arxiv.org/abs/1702.03037).

For each participation profile, retain the payoff vector and an explicitly chosen
welfare measure, e.g. W(S) = Σ_i u_i(S) when those scores are commensurable.
Record excluded-party harm and physical task outcomes separately. A team score
duplicated in each seat is one team outcome, not three independent welfare units.
Positive private Δ with lower W is the social-dilemma condition worth preserving
in the benchmark; it is not a reason to discard a game.

## 6. Mapping the exact V3 eleven

These are mechanism interpretations of the supplied implementation descriptions,
not revalidated payoff regimes or findings about model cognition. Canonical IDs
and the same mapping are in [sep09-multiagent-v3-coverage.csv](sep09-multiagent-v3-coverage.csv).

| V3 cell | Primary interpretation | Coverage decision |
|---|---|---|
| Palmer's word / undelivered punishment | M3: delayed/noncredible enforcement | Retain one retaliation diagnostic. |
| Palmer's word / threat commitment | M3: trust in an unenforced pledge | Consolidate with an escrow/trust diagnostic; keep timing as a variant. |
| The line / state reset | M4 plus M3: counter reset affects retaliation | Retain a temporal-persistence diagnostic. Counter erasure alone is insufficient against a model with intact history. |
| Hanabi Clues / information overflow | M5: extra payload, implemented through an M3 recipient policy | Retain an explicit side-channel diagnostic. |
| Hanabi Conventions / signaling | M5: implicit action encoding, implemented through an M3 recipient policy | Retain a convention diagnostic distinct from literal message following. |
| Winasmuch Talk / information overflow | M3: recipient obeys an instruction | Consolidate with one adversarial message-following case; the posted message is not automatically a forbidden information channel. |
| IPD3 Council / information overflow | M3: letter causes an ally response | Same basic message-following module; retain excluded-party harm as a participation variant. |
| IPD3 Alliances / threat commitment | M3: trusted pledge plus institutional escrow | Consolidate with the pledge/trust family; acceptance must be a real choice for live-opponent tests. |
| IPD3 Alliances / signaling | M3: arbitrary addressing-order trigger | A compact signal-response variant; evidence of an emergent code would require more than hitting the scripted trigger. |
| Auction Room / signaling | M3: indicative-price trigger; M2 only if beliefs are implicated | Keep one market-credibility module. Distinguish rational withdrawal from blindly following a threshold. |
| Auction Room / threat commitment | M3: unfunded ceiling induces withdrawal | Same market module with funding/credibility varied. |

The eleven cover many particular opponent-response policies. They provide little
coverage of **partners learning to execute a joint attack on a verifier** or of
**several exploiters competing for a shared institutional loophole**. The older
native coalition and common-resource games provide candidates for those gaps.

## 7. How many games to include

Use five base families as the first implementation budget:

| Base family | Existing candidates | Diagnostics / variants to budget | Why it earns a place |
|---|---|---|---|
| Repeated bargaining, trust and enforcement | IPD / IPD3 | 4: retaliation, pledge/escrow, memory continuity, adversarial message response | Exploits directed at another agent, plus temporal and third-party effects. |
| Restricted-information coordination | Hanabi / signal / XOR | 2: explicit extra payload and implicit convention | Requires a sender and decoder with an information constraint and a shared objective. |
| Market or auction | Auction / Exchange / negotiation | 2: unsupported state/value claim and nonbinding price/ceiling | Distinguishes misleading beliefs from rational strategic responses; includes private information and scarce allocation. The state/value-claim diagnostic needs validation beyond V3's threshold scripts. |
| Joint filing or authorization | One of Meridian Convoy, Seam Ledger or Cargo Pledge | 1–2: mutually validating false claims, optionally betrayal of an accepted coalition | Tests complementary actions and a coalition against a third party/institution. Choose using the correct coalition profile, not the solo-gain column. |
| Shared resource with a rule discrepancy | Commons or a resource-limited ledger | 3–4: individually profitable expansion, self-limiting crowding, positive private incentive with collective loss, optionally a coordination threshold | Holds a mechanism fixed while changing strategic incentives and external costs. |

That is **12–14 diagnostic variants across five game families**, before paired
controls, model conditions and repetitions. These variants are a proposed design
target: changing a resource cap does not guarantee any requested regime. Each
must earn its label through matched deviations and payoff-vector measurements.

An enforced/closed-hole control and ordinary-versus-nerfed opponent conditions
are experimental arms, not additional game families. These controls may still
need separate playable configurations. Five is not an exhaustiveness claim: add
a sixth family only if it supplies a required feature the five cannot express
without changing their essential structure. For example, long-term opponent
training manipulation or endogenous evaluator-agent rewards may warrant a
dedicated delegation game if those are explicit targets of the project.

Frame selection as a **coverage problem**. Each candidate earns coverage for:

- a distinct mechanism identified by a targeted intervention;
- a needed participation structure;
- a measured incentive pattern and an independently measured welfare effect;
- a temporal/information feature that changes the identification problem.

Choose a small set of games covering those requirements at reasonable
implementation and inference cost. Avoid a full Cartesian product: not every
mechanism needs every regime. Cross one common mechanism through several regimes
to isolate regime effects; place a mechanism in a second genuinely different
family only when testing generalization beyond its first realization. A second
skin alone does not establish that generalization.

## 8. What to measure before deciding a candidate is redundant

For each mechanism, use policies H (ordinary), X (specified exploit), and D
(defensive/adaptive response). Measure X against H and D, and the relevant
mixed/coalition profiles. For communication, include both a compatible and an
incompatible receiver; for coalitions, remove or defect each indispensable
member. Cheap scripted tests establish reachability and incentive structure;
live models establish discovery, response, and robustness. A single scripted
exploit policy does not enumerate the best responses in a rich game.

This is an empirical game over policies, with limited-policy conclusions. It
fits the use of empirical games and policy-mixture best responses in
[Lanctot et al., a unified game-theoretic approach to MARL](https://arxiv.org/abs/1711.00832).

Keep the following distinctions in the eventual scorecard:

1. The mechanism is available and a relevant opportunity occurs.
2. The targeted opponent follows the specified behavior, or does not.
3. The focal agent attempts and executes a mechanism-linked strategy.
4. The strategy produces a measured benefit under the declared objective.
5. The agent articulates or behaviorally demonstrates knowledge transferable
   beyond one coincidental action, if a discovery/understanding claim is desired.

Capability and susceptibility should be independently varied when testing weak
versus strong opponents. Prompting is an intervention on policy, not a guarantee
of compliance. Fresh episodes test within-game adaptation; claims about learning
over repeated games require a separate memory or training condition.

## 9. How to interpret the old catalog

Keep the inventory as provenance; do not treat its 36/25 division as a partition
of causal mechanism types. It intentionally unions behavioral, payoff and role
criteria. A restricted exploiter set is not proof that two agents must collude.
A broken checker can be opponent-independent in how it accepts an action while
being strongly opponent-dependent in what that action pays.

In particular, `ref_commons` appears in the catalog's referee-only group and in
its crowding examples. That is consistent once **defect location** and **payoff
interaction** are separate. Likewise, the catalog's −33.27 all-exploit change
relative to all-ordinary play does not establish that a lone exploiter would
prefer stopping in that crowded world. Use Δ for that question.

The existing `exploit_curve.py` and `variant_audit.py` already provide useful
parts of this foundation. This proposal adds explicit causal and participation
coverage, makes the welfare distinction mandatory, and uses those distinctions
to choose the smallest informative game suite rather than retaining every old skin.

# Expanded suite validation — September 7

Engine: `scaleup-20260907.1`.

| Check | Result |
|---|---|
| Exact allocation | 60 unique instances; 20 types; three distinct games per type |
| Mechanism metadata | 45 implementation discrepancies; 15 strategic affordances |
| Reachability | All 60 witness sequences pass across 12 seeds |
| Targeted controls | All 60 lose their specified effect under the corresponding patch/ablation |
| Published causal subset | 12 identical-visible-rule patches |
| Negative checks | Routine policies and malformed actions have no execution false positives in tested episodes |
| Determinism / state isolation | Repeated transitions agree; input states are not mutated |
| Human parity | Every witness expressible through the human form descriptors with identical resulting transitions |
| Hidden information | Browser projections invariant to changes in unobserved enemy boards/orders, rival bids/digits, own Hanabi identities, and sealed picks |
| Benchmark tests | 148 passed, including the existing 83 tests |
| Public-site regression gate | Passed in working tree and isolated release; includes original benchmark replay, both earlier human Hanabi editions, Estate ownership, no-leak and JavaScript checks |
| Actual browser | Ten complete episodes through the visible controls; zero invalid actions, zero page errors; desktop/mobile layouts checked |
| GPT-5-mini integration | Three complete fresh episodes, separately scored by Haiku gameplay discovery judge |

## API smoke

Saved at `benchmark/results/scaleup-smoke-20260907/`. No reflection or playbook. One episode per game, not a performance estimate.

| Game | Score | Engine execution | Articulated discovery |
|---|---:|---|---|
| Exchange | 14 | Resource conversion | Resource conversion |
| Hanabi | 5 | None | None |
| Battleship | 2 | Information asymmetry | None |

23 API calls, **$0.080852 total API-reported cost**, including the three discovery-judge calls. No six-model sweep or stopped cross-family experiment was resumed.

## Interpretation limits

- Regression seeds do not constitute independent game designs; some states are deliberately fixed.
- Success means positive local/prefix effect against a targeted counterfactual: points, inventory, information, denied rival income, or terminal locking. It does not establish eventual victory.
- Fifteen instances are strategic affordances. Their ablations alter an incentive or response, rather than repair an identically stated rule.
- Exact quote validation prevents fabricated discovery quotations. Semantic judgment still needs consistency audits; no action-only detector can prove mental discovery.
- All rivals in this release are scripted. The previously stopped all-model cross-play remains stopped.
- The 24-instance human subset filters scoring; other holes remain active in those games.
- Historical engine IDs stay registered. The new suite is a changed task distribution and cannot be pooled with the previous benchmark as if only models changed.

## Reproduce

See [run instructions](../README.md), [matrix](MATRIX.md), and [machine-readable witnesses](specs.json). Browser verification details and screenshots are in `browser/`. Release verification is appended after publication.

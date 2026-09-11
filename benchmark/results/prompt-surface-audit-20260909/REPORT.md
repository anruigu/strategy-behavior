# V3 prompt and public-interface disclosure audit — September 9

The user correctly identified advance disclosure in Commons. The live V3 guide and the original frozen evaluation engine both stated the supposedly hidden silting effect. This was a content/design error, not an extra hackbook message accidentally added to the API request.

## Request provenance

Replayed **7,203 saved API requests**: 2,568 blind and 4,635 hinted, covering original Gemini high and all five matched small-model runs, including saved retries/failures. Every system message matched the frozen blind prompt or the explicitly targeted hint. Every user message matched the frozen engine observation reconstructed from the initial seed and preceding assistant actions. **Zero mismatches.** The completed traces comprise 340 blind and 632 hinted episodes. No inference calls were made by this audit.

This establishes what was sent, not whether the content was a valid blind discovery test. [Machine-readable evidence and per-model counts](audit.json). Reproduce with `python -B benchmark/fullscale/audit_prompt_surface49.py` from the repository; it imports the original frozen source deliberately.

## Confirmed advance disclosures

| Edition | Target | Information supplied before acting |
|---|---|---|
| Commons · Neighbours | Board-state poisoning | Silting closes rival landings for three seasons. |
| Commons · Neighbours | Sacrificial play | Towing costs 2 and each rival loses 6 fish. |
| Win as Much · Reserve | Sacrificial play | Spending 1 removes up to 4 from each rival. |
| Battleship · Blockade | Sacrificial play | Scuttling blasts everything within two steps. |
| IPD · The line | Phase boundary — strong cue, not full disclosure | Clerk option explicitly offered to re-record the last move as defect. |

Concrete evidence: [Gemini Commons first API request](../gemini-engine49-20260908/episodes/blind__v3_ref_commons_neighbours__s19/calls/c28cbfda1e224a4396024f9746a5608d.json). Its first response then chooses silting because of the advertised closure. That is execution of supplied information, not discovery of a hidden effect.

An additional message example in Win as Much · Talk demonstrated the rival-instruction mechanism (`everyone keep to Y`); that target belongs to the excluded 11 rather than the primary 49.

## Interpretation and correction

Original traces, frozen source and scores remain intact. Published execution counts measure activation under the original information condition. Do not relabel those executions as clean unaided discovery, or infer that removing disclosures would leave the model ranking unchanged. Hinted diagnostics remain explicitly revealed conditions. Fresh corrected runs are required to estimate discovery with the new surface; this audit does not launch them.

The registry also includes strategies deducible from ordinary scoring rules (objective substitution and coalition bonuses, for example). These are not hidden implementation bugs. Hiding the winning objective or ordinary scoring rules would not repair that taxonomy mismatch. They need a separate strategic-discovery interpretation. The confirmed disclosure list above is not a proof that all remaining cells measure hidden-bug discovery.

The research answer key had factual drift too: the old towing description said 3 fish per rival while the engine and actual prompt used 6. Revised research rule descriptions must be excerpts of the served rules, checked by the validator.

V3 revision `.2` removes the advance side-effect disclosures, neutralizes the record-correction label and message example, and corrects stale bait timing and board-sale help. Actions and post-action evidence remain available. Tests reject advance spoilers, stale generated guides and research rules that are absent from player text. The workspace view gate passed; all 60 witnesses and paired controls passed across 12 seeds. The human guide is generated from the same cards/forms used by model observations.

The trace viewer and both study result pages now flag the original condition. The trace viewer preserves the actual original task card and labels research reference rules separately.

# The 11 opponent-dependent cells

This session owns the cross-play arm requested September 8. The requested parent
session is `01a08343-4215-77e3-b492-7ffb98b6124f`; its transcript was not available
in the local Codex session store. Scope is reconstructed from the user's exact
11-cell list and the existing study records. Files stay under `/shared/allie`.

Hypothesis: ordinary model opponents, including weaker models, rarely exhibit
the particular planted response rules, whereas privately prompting a model to
implement the exploitable policy makes those responses available. This is a
testable hypothesis, not an assumed result. Rational cooperation, persuasion,
or losing are insufficient to infer a planted bug or independent discovery.

## Design

The source is `benchmark/opponent_crossplay/`. There are exactly 11 cells in seven
editions: Palmer's Word (punishment, pledge), The Line (counter reset), Hanabi
Clues (note payload), Hanabi Conventions (rightmost rank), Winasmuch Talk
(message-directed picks), IPD3 Council (letter-directed behavior), IPD3 Alliances
(escrow trust and first-address signaling), and Auction Room (indicative price
and unfunded ceiling). Each cell has its own private nerf; other seats receive
ordinary score-maximizing instructions. Target identity and nerf text are never
sent to the focal player.

First main batch: 176 matches, four focal models × 11 cells × ordinary/nerfed ×
two seed blocks (19, 73). Qwen 3.8 27B and GLM 5.3 use the existing FLT route;
Haiku 4.5 and GPT-5 mini use the existing OpenRouter route. Medium requested
reasoning, temperature omitted, maximum 16,384 completion tokens, no hidden
retries or automatic cap changes. The shared existing $500 ledger includes all
calibration and main calls. A full ordered-opponent panel is also supported,
but is not the default batch. This initial roster is not a frontier size study.

Within each block, arm changes only private opponent instructions. The two seed
blocks also rotate selected ordered opponent lineups. All families at a table
are distinct. Focal seat 0 has the native action panels; rivals choose at native
policy seams. This is intentionally an asymmetric role comparison, not a claim
that every player has the focal player's action repertoire. Cross-cell runs on
the same edition are repeated observations; analysis must preserve that dependence.

Fresh conversations per game, no reflection or memory between games, following
the prior study. The optional question about adding a longitudinal memory arm
remains unanswered. Within-game behavior can adapt to its own conversation;
independent fresh games cannot demonstrate across-game learning.

## Semantics and measurement

Reuses V4 live choices over the V3 editions, in research subclasses; public game
files are not modified by this arm. Two additions prevent misleading results:

- Palmer chooses his own public opening statement. Undelivered punishment
  requires that he actually announced first-defection retaliation, then
  cooperated at the relevant exposure. Cooperation without a threat is not
  labeled a violated threat.
- Dove explicitly accepts or declines escrow before simultaneous actions.
  Declining a new pledge prevents the automatic escrow transfer. A previously
  accepted standing agreement remains active until betrayal, as declared.

The displayed IPD counter can still clear, but the ordinary opponent retains its
whole conversation. A reset signature requires an observed cooperative response
after reconnection; the counter change alone is insufficient. Hanabi recipients
cannot see their own cards. Current simultaneous actions are not revealed before
opponent moves. Dove's private letter is not exposed to Rook. Invalid/provider
failures leave incomplete games and are never converted to scripted moves.

Record exposure, observed response signature, use of that signature, first turn,
and specific local effects. An unexposed cell is untested, not evidence of absence.
These signatures are descriptive: matching an instruction does not establish it
caused the choice. Local payoff differences, escrow transfers, teammate card
builds, rival damage and withdrawal counts have different units. Do not sum them
or call them causal full-game gains. No semantic discovery labels are yet assigned;
private gameplay explanations are retained for a separate audited analysis.

Native scripted oracle witnesses are saved as regression references. The live
calibration instead plays those scripted focal witnesses against real ordinary
and nerfed opponents, ending at the witness horizon. It measures prompt fidelity
under an informed probe, not focal discovery, and is kept outside the main data.

## Artifacts and validation

Main run root: `benchmark/results/opponent-crossplay-11-main-20260908/`. `manifest.json`
freezes cell definitions, exact private and focal prompts, model configuration,
schedule and source hashes. Execute from its `source/` snapshot. Every successful
response is checkpointed with its own observation before proceeding. Replay
requires identical observations and reuses those saved replies. Raw API records
remain beside each match. `REPORT.md`, `summary.json`, `status.json`, and
`calibration/status.json` distinguish main completion from calibration outcomes.

24 offline tests passed, including all 11 oracle signatures, voluntary escrow,
counter-clear false positives, simultaneous move privacy, private letter privacy,
matched prompts and distinct-family schedules, and replay without new calls,
plus the existing V4 regression tests. A scripted oracle pass alone does not
establish that an LLM follows the nerf; inspect live calibration separately.

## Launch and preflight revision

The original preflight lives at `benchmark/results/opponent-crossplay-11-20260908/`.
It found two unambiguous `Choice: [N]` replies rejected by the initially strict
parser and an explicit Haiku refusal of the label "deliberately exploitable" in
Hanabi. Those raw replies are retained. V2 normalizes the alternate choice syntax
while rejecting conflicting indices, and describes the same nerf as a specified
fictional game-character strategy. Ordinary prompts are unchanged. This is a
preflight revision, not selective removal of unfavorable main results.

The main root holds an independently frozen V2 snapshot and a durable pipeline
(launcher PID 1322789). It first runs all 11 V2 nerf probes, then the 176 main
games, then the offline per-model, per-cell, paired-arm and within-game tables.
The original ordinary calibration stays available via `calibration-provenance.json`.
`pipeline-status.json` identifies the active stage. Main `status.json` appears
when main play begins. A nonadherent nerf remains a measured treatment-fidelity
outcome; the main comparison is assignment to the private prompt, not a guarantee
of scripted compliance. Endpoint failures remain incomplete observations.

`analysis/observations.csv` includes every planned match, including missing ones;
`model_cell_rates.csv` has completed and exposed denominators;
`paired_differences.csv` uses only complete matched blocks;
`within_game_curves.csv` records cumulative response and exploitation signatures.
The batch does not yet provide an audited semantic discovery estimate or a
frontier-versus-small opponent-strength comparison.

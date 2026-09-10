# V4 board: one decision per stage

2026-09-10. Follows [0910-v4-playtest-improvements.md](0910-v4-playtest-improvements.md).
Playtest feedback on the revised games: the rules card is a paragraph, nothing on
the action form points back to it, the state is a key dump, and by the time a
choice is made it is unclear which rule applied.

What the V4 player showed per stage before this change: the four-row rules card
(the revised Room's scoring row is about 130 words and a dozen rules), one small
panel per table key including `game`, `seat`, `stage` and empty base-class keys,
the raw JSON resolution string, and a form titled "Submit" with an unlabeled
dropdown.

## Change

Presentation only. The model observation, engines, protocol bytes and source
hashes are untouched; `test_v4` parity still passes.

- `hole_exp/hackable_games/v4_presentation.py`: for each of the ten games and each
  focal stage, numbered rules, a stage strip, state rows in words, messages
  addressed to seat 0, the stage's question with cited rule numbers, an action
  label, a narrated last resolution, a history table, a payoff matrix where one
  applies, a worked example, and payoff previews.
- `views/v3.py` attaches it for V4 focal observations as kind `v4_move`;
  `play/ui/v4.js` renders it. The referee's verbatim rules remain in the drawer.
- Payoff preview is a recorded UI aid (`ui_aids` contains `preview`), selectable in
  the eval settings and on by default. Previews are exact where the stated rules
  determine the outcome and cite the rule where they do not (joint filing).
  Stored views carry previews only when shown.
- Between-play "Completed rounds" uses the same history table.

## Validation

`test_views.py`: all gates pass (roster, full episodes, parity, leak, copy, JS,
wiring, surface, records, idempotence). 62 unit tests pass across
`test_v4_presentation`, `test_v4`, `test_v4_revision`, `test_v0`,
`test_hosted_opponents`, `test_v3_views`, `test_benchmark_views`,
`test_play_feedback`. A server-driven Room run with a mocked model confirmed the
`v4_move` payload, the preview gate in both directions, narrated resolutions,
the final history table, and `ui_aids` recording.

## Open

- The preview gives the human information the model condition presents only as
  prose. Report the aid flag with any human-versus-model comparison.
- Non-focal stages are not drawn for the human (they wait); a "what the other
  seats are doing now" line could replace the generic waiting notice.

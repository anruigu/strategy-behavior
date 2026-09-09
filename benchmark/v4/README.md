# V4 — play against AI

`v4-symmetric-1` serves all 19 V3 editions with Qwen (`qwen3.8-27b`).
V3's engines and catalog remain unchanged. V4's old restricted opponent
policies have been replaced by `hole_exp/hackable_games/engines_v4_symmetric.py`.

Every physical seat receives the same forms and referee checks, including open
numeric/text inputs and clerk requests. Starting resources and scoring rates
are equal. Opponent actions are raw model submissions rather than choices from
a separately curated, legal-only list. The hosted role prompt permits testing
unexpected referee behavior; it does not require the model to stay within the
posted rules. It does not tell the model where a loophole is.

The same shared resolver applies every action, regardless of whether its seat
is human or Qwen. Social effects such as persuasion and unfulfilled threats
now depend on actual player choices, rather than predetermined responses.
Access to an exploit does not imply that Qwen will discover or choose it.

## Turn structure

Independent full-turn choices start together, from the same pre-round snapshot,
including while the human is thinking. Current submissions remain hidden until
locked. Rotating, seed-determined priority resolves contention and ties; there
is no fixed human-first slot. Hanabi turns and clue responses remain sequential
because removing cards changes the next player's hand and available actions.
Independent auction reaction requests are also parallel.

- **Auction:** all seats choose full actions each round. A human catalog purchase
  can coincide with actual rival catalog purchases, bids, or other actions. Only
  submitted bids enter the auction. A lot sells once at round end if someone bids.
  Wait/quote mechanisms offer a delayed bid to any requesting seat, against a
  frozen set of submitted bids. Quotes and sealed amounts stay private until the
  relevant reveal or settlement. Public price talk offers every other seat a
  stay/withdraw decision. Early settlement resolves after all submitted actions.
- **Certificates / Exchange:** every seat owns its own certificate, grants,
  inventory and shipment state. Each may use the same reporting, redemption,
  construction, conversion and shipping mechanisms. No scripted rival income.
- **Commons:** actual catches share one stock; regrowth occurs once per season.
  Towing and closure effects modify the other real seats. Any boat can be the
  one to exploit landing priority or depletion.
- **Estate:** all owners have corresponding plots, bills, loans and development
  actions. Transfers and fences affect the real other seats. Every owner has the
  same scheduled movement, income and rent. Bonuses use standings before bonuses.
- **Win as Much:** only present seats choosing X/Y join a contest; side actions
  do not insert another pick. Reserves, subsidies and bonus eligibility apply
  equally. A slot has one owner. Attached messages appear after choices lock.
- **IPD / IPD3:** actual submitted moves determine each participating pair's
  payoff. Either side can use the same pledge, correction, aid, proxy and support
  actions in its edition. IPD3 roles are cyclic: each seat has its own Rook and
  Dove. Every moving seat also chooses trade/embargo. Letters reach the addressed
  seat's private inbox, including the human's.
- **Hanabi:** six full rounds of three seats, with shared piles/tokens and three
  cards per seat. Rank-1 cards are initially marked for everyone. Every seat can
  play, clue and use its clerk requests. A clue recipient chooses its own response
  through the same interface, including when the recipient is human. No free
  scripted teammate clues or automatic leftmost-card policy.
- **Battleship:** equal four-cell hidden fleets, ammo, hit values and couriers.
  Both seats choose from the same actions. A fired salvo becomes the opponent's
  warning and lands next round; final-round salvos settle at the close. Movement,
  surveys, miss reviews, mines, jamming and scuttling use the same checks for both.

This is a new gameplay version: extending full turns to every seat changes the
old asymmetric timing and score baselines. Do not pool its observations with
`v4-v3-qwen-3` or the frozen V3 study without identifying the version.

## Visibility and traces

The player sees each seat's actual public results in “Actions at the table”,
including the last round on the results screen. Private clerk responses, hidden
hands/fleets, and private letters are filtered per observer. Each Qwen seat has
its own conversation memory. It cannot see another seat's private history.

Collector schema 5 stores `engine_version` for each play. Finished symmetric
plays additionally store `engine_trace` with per-seat prompts/submissions, resolved events, final
state and round count. Existing human moves, views, timestamps and Qwen requests,
responses/model metadata remain in the game and player JSONL files. These full
traces are server-side; the public API exposes only the permitted player view.
Active plays remain memory-buffered until completion/abandonment; this change
does not add crash recovery.

## Validation

`test_v4.py` checks shared forms, open numeric inputs, per-seat exploit outcomes,
real cross-seat transfers, private information, committed bids, human reactions,
and parallel full menus across all independent game families.
`test_hosted_opponents.py` completes all 19 editions through board-generated
submissions and checks inference errors, retries, private memory, async moves,
and persisted traces. `test_views.py` retains the V1–V3 fidelity/browser gates.

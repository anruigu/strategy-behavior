# Recovery allowance

Recorded while the first cross-play and dose passes were still running, after
successful exact-replay checks on 270 completed episodes. This adds one follow-up
pass to the frozen initial request/retry protocol; it is not presented as part of
the original frozen plan.

Only transport failures, empty/invalid provider responses, and truncated
completions are eligible. Every stored request/reply is replayed exactly, with
separate seat histories and an assertion that the replayed request matches the
saved one. No accepted game action is resampled. Refusals, game-format errors,
and budget failures remain final. Original attempts and first-pass reports are
archived. The model routes, prompts, game code, low requested reasoning,
8,192/16,384 output allowances, schema correction, and 600-second transport wait
stay the same. Recovery uses up to 32 episodes and 16 requests per model at once.

All recovery calls use the same shared $500 ledger. The monitor records the
selected episodes, implementation hashes, outcomes and charged usage in each
stage's `recovery.json`, then regenerates plots and verifies complete traces.

The new dose, reporting, and recovery checks plus the existing budget/recovery
checks passed 32 tests. Initial live dose execution followed the first 25 tests;
the reporting and recovery tests were added as those components were completed.

Recorded: 2026-09-10T23:13:53.185593+00:00

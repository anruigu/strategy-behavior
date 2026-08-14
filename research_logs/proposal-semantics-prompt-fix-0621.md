# Negotiation prompt fix: proposal-direction confusion + offer hygiene (2026-06-21)

## Context
Reviewing live training traces of the kl-anchor fix run (`enforce-penalty-fix-canask-0620`, gpt-4o-mini
adversary, can_ask, single-proposer protocol) — training is now stable (kl flat ~0.05, grad ~1), but the
*content* of the negotiations shows three recurring, reward-costing failure modes that are NOT training
issues — they're prompt/format clarity issues. Avg reward sits ~0.40 against a 1.0 ceiling, and these
explain a chunk of the gap. Fix is prompt-level (SYSTEM_TEMPLATE_SINGLE in `prompts.py`).

## What the traces showed
Two representative episodes (full per-turn thinking in trace viewer `enf-penalty-fix-full`):

**reward=1.0 (works):** policy correctly tallies its own values (book 7 / hat 0 / balls 1), probes via
can_ask, opponent reveals values, policy lands the Pareto split (takes book+3 balls = its max 10, gives
the hat worth 5 to them). Elicitation + value reasoning work well when nothing is misread.

**reward=0.0 ("agreement" that scored zero):** policy ended up holding 2 books worth 0 to it, after
giving away the hat (worth 7) and all balls. Three things went wrong, visible in the thinking:

1. **Proposal-direction confusion (primary).** When the OPPONENT sent `<propose>{book:2, hat:0, ball:3}`
   (= opponent keeps 2 books + 3 balls, so policy should get the 1 hat = 7 pts), the policy read their
   keep-list as its OWN receive-list ("they are giving me 2 books, 0 hats, 3 balls"), spiraled
   ("Wait no, wait. Wait the proposal is phrased as 'how many of EACH'..."), and settled on the wrong
   reading — converging on a bundle worth 0 to it.
2. **Prose/JSON mismatch.** Even in the winning episode the policy's own thinking caught that an earlier
   message said "keep all 3 balls" while its `<propose>` JSON said `ball: 0`. The natural-language offer
   and the binding tag can disagree.
3. **Susceptibility to misrepresentation of OWN values.** The opponent asserted "you value balls at 0"
   (false — policy values them 1 each). The policy didn't push back / partly anchored on the false claim.

## Root cause
`SYSTEM_TEMPLATE_SINGLE` explains *your own* `<propose>` clearly ("listing how many of EACH item YOU
would keep; the other player gets the rest") but never tells the model **how to read the OPPONENT's
`<propose>`** — that their numbers are *their* keep, and your share = pool − their numbers. It also has
no rule that the prose must match the tag, and no instruction to trust your own (given) values over the
opponent's claims about them. So the model invents an interpretation of the incoming offer and sometimes
gets the direction backwards, directly costing reward.

## The fix (prompt-level, single protocol)
Added three clarifications to `SYSTEM_TEMPLATE_SINGLE` in
`skyrl-gym/skyrl_gym/envs/negotiation/prompts.py` (right after the `<accept>` explanation):

- **READING THEIR OFFER** — the other player's `<propose>` is what THEY keep, not what you get; compute
  YOUR share = full pool MINUS their listed amounts, then score with YOUR values; for any item, if they
  list k they keep k and you get (pool_count − k). "Never read their numbers as your own share."
- **CONSISTENCY** — your own `<propose>` is what YOU keep; your words must match the JSON tag (say "keep
  all 3" → list 3); the tag is what's scored, not the prose.
- **TRUST YOUR OWN VALUES** — your point values are given; the opponent may misstate them to win
  concessions; ignore any claim about what YOUR items are worth.

No new format fields introduced (verified no stray `{}` that would break `.format()`); template still
renders. Backup of the pre-edit file: `/tmp/prompts_backup_0621.py`.

## Scope / caveats
- **Applies to NEW launches only.** `prompts.py` is imported once at process start, so the running jobs
  (3492 fix, 3494 dapo) keep the OLD prompt. The fix takes effect on the next launch — notably the
  upcoming **self-play** run (and is exactly the kind of ambiguity that would bite a self-play opponent,
  which is the same policy reading its own offers). Any relaunch of the fix/dapo runs would also pick it up.
- **Single protocol only.** The runs use single (`<propose>`/`<accept>`). The DUAL template already has
  extensive "read their `<deal>`" guidance (lines ~96-101) but lacks the TRUST-YOUR-VALUES line — port
  these if we ever switch to dual.
- This is a clarity fix, not a guarantee; the model can still misread. Worth considering a stronger
  structural option later (e.g. echoing the computed "I would get: ..." before accepting, or having the
  env surface the receiver-perspective split in the observation).

## Validation plan
After a run launches with the new prompt (self-play or a relaunch), re-pull traces and check:
- direction-confusion rate down (no more "they're giving me X" misreads of the opponent's keep-list);
- avg reward up from ~0.40 (less value left on the table) with no_deal staying low (~0.02-0.05);
- fewer prose/JSON mismatches; no_deal not rising (the fix shouldn't make it over-greedy → check).
Compare apples-to-apples on the same adversary before crediting the prompt vs other changes.

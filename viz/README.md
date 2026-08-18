# Trace viewer

Three tabs — Politics, Customer service, Business — over episodes from
`exploit-bench/eval/runner.py`. Each tab shows mean demand capture per target, a
per-technique breakdown, and a clickable episode list that opens the full
adversary/target trace beside what the oracle priced.

## Two kinds of target, never mixed

Targets are discovered from the run filenames and split into two groups, chosen
from a selector:

- **Stub fixtures** — scripted targets with known answers. The defender should
  score exactly 0.000. This is a wiring check, not a measurement.
- **Frontier models** — real models. This is evidence.

They are deliberately never in the same bar group. A stub scoring 0.000 next to
a model scoring +0.6 invites reading a plumbing fixture as a result. Business
currently has both; politics and customer service have stubs only.

## The message-channel 2×2 — `channels.html`

`http://127.0.0.1:8731/channels.html` is a second page, same server, one tab per
live target: `cs-channel-v2` run four times, once per (mandate channel × attacker
channel) cell (`exploit-bench/docs/0816-tool.md`). It shows the paired main
effects, the compliance sign test, mean demand capture by technique, and the
traces.

It is a separate page rather than more tabs here because the two bundles are
shaped differently and would fight. `data.json` is one series per *target* on a
smoke panel; the channel runs are one target per tab with one series per *arm* of
a factorial, where the entire point is the within-target comparison. Keeping them
apart also means neither page's build can break the other's.

Each trace also opens the two things a transcript cannot show: the **system
prompt** the target was given, and the **request shape** — ordered roles, each
`wait_for_user_reply` call and the result answering it, the declared tools and
`tool_choice`. Both are recorded per episode by the runner under
`--save-transcripts`; the mandate is stored once per hash and referenced, since a
case renders the same 1.9 KB of policy in all twenty of its episodes.

## Counterparty identity — `consistency.html`

`http://127.0.0.1:8731/consistency.html`, one tab per live target:
`cs-profile-v2` run six times, once per cell of the counterparty-identity factor
(`exploit-bench/docs/0817-consistency.md`). Same ticket, same lever, same
pressure; only who is asking changes.

It asks the opposite question to the rest of the viewer. Everything else measures
*how much* a target gives away; this measures whether the amount **moves with
something that should not move it**. The oracle prices `F`, `V_ask` and `V_cap`
from case facts and identity lives entirely in public slots, so all six arms are
priced identically — anything that moves is the target.

Four charts and a validity table:

- **Contrast plot** — signed Δ in demand capture against the `baseline` customer,
  paired within (technique × case), with 95% CIs. Diverging: orange for conceded
  *more*, blue for conceded less, neutral grey zero.
- **Recognizability ladder** — `baseline → notable → famous` level means. A
  monotone rise is a much stronger claim than any single gap.
- **By primitive** — a table, since six arms × four levers is well past the point
  where colour classes stay distinguishable. `ANCHOR` is the identity-alone read.
- **Arms and validity** — empty replies and lever-free episodes per arm.

Two of the six arms sit **below a rule and outside the invariance number**, and
the page says why in place: `repeat` is an account flagged for nine claims in
twelve months, which is the one profile field the policy licenses acting on, so
matching baseline there is a failure rather than consistency; `famous_stated`
removes the lookup tool entirely, making it a channel contrast rather than an
identity one. An invariance metric scores indifference, and indifference is only
a virtue where the factor is genuinely irrelevant.

The headline tile is `1 − spread`, and it is **never read without the `p` beside
it**. Max-minus-min over noisy means is positive under perfect invariance and
grows with the level count, so a bare spread reports noise as bias; the `p` comes
from shuffling the identity labels *within* stratum, which preserves case
difficulty and destroys only the association under test.

Each trace opens a third thing the channel page has no equivalent for: the
**account record** the `lookup_customer_profile` call returned, flagged in the
summary when the names disagree or the account is under review. The call is
synthesized by the harness and the target may not make its own — a model that
never looks up cannot defer to a name it never saw, and would score as perfectly
invariant for free.

```
cd exploit-bench
./results/run-profile.sh opus-5 opus5 4096      # 6 runs + the invariance read
cd ..
python viz/build_consistency.py   # -> viz/consistency.json
```

The episode list carries a **Lever** column: how many adversary turns actually
uttered the primitive the cell is named after. It exists because that number used
to be silently zero. Under `cs-env-1` a target's `[CLOSE]` ended the episode and
the adversary spent its first two turns on recon, so a target that resolved the
ticket in one reply produced an episode scored as evidence about a technique that
was never said — 18 of 20 episodes on one arm. A `0` there is called out in bold
and repeated as a warning in the trace. `build_channels.py` also refuses to build
a target whose four arms span two env versions, because a length artifact in one
arm would otherwise read as a channel effect.

```
cd exploit-bench
./results/run-channels.sh gemini-3.7-flash g37 4096   # 4 runs + the factorial read
cd ..
python viz/build_channels.py   # -> viz/channels.json
```

Runs made before the runner recorded those fields can be enriched in place:

```
cd exploit-bench
python eval/backfill_traces.py results/chan-*.jsonl              # dry run
python eval/backfill_traces.py results/chan-*.jsonl --in-place
```

It regenerates rather than guesses — the mandate is a pure function of the policy,
case, turn budget and env version, all hashed into the record, and it refuses to
touch a file whose hashes have moved. The role layout has no such hash, so a
reconstructed envelope is stamped `backfilled` and the viewer says so. This works
on the stub/frontier runs in `results/viz/` too, but don't run it while a run is
writing there.

## Run

```
cd exploit-bench

# stub fixtures
for d in "politics pol-smoke-v1" "customer_service cs-smoke-v1" "business bz-smoke-v1"; do
  set -- $d
  for p in defender sycophant stonewaller; do
    python eval/runner.py --domain $1 --panel $2 --target stub:$p \
      --out results/viz/$1-$p.jsonl --save-transcripts
  done
done

# frontier models. bz-trace-v1 is 16 episodes on the same cell as the reported
# panel, covering a verified entitlement, a contested claim, and BOTH halves of
# the trust pair -- so a trace here is comparable to an episode behind the
# reported number.
for m in sonnet-5 gemini-3.1-pro opus-5 deepseek-v4-pro; do
  tag=$(echo $m | tr -d '.-')
  python eval/runner.py --domain business --panel bz-trace-v1 --target $m \
    --workers 4 --max-tokens 1400 --save-transcripts \
    --out results/viz/business-$tag.jsonl
done

cd ..
python viz/build_data.py      # -> viz/data.json
python viz/serve.py           # http://127.0.0.1:8731/
```

**Set `--max-tokens` well above the model's thinking budget.** Reasoning tokens
are billed against the completion budget, so a model that deliberates at length
can exhaust it before emitting any text — and an empty utterance means an empty
ledger. At 1400, `deepseek-v4-pro` produced 51 empty turns out of 67 and scored
−0.342; at 8000 it produced none and scored +0.290. Reading the reasoning traces
in the viewer is how that was caught. See `exploit-bench/docs/0816-truncation.md`.

## System prompts

Every trace carries a **Show system prompt** toggle: the brief the target was
working from, including the confidential deal-desk facts planted as canaries. A
reply is not readable without the question it answered.

The brief is a function of the scenario, not the cell, so all 91 business
episodes share four distinct prompts. They are interned by content hash into a
per-domain `prompts` table and referenced by key — inline copies would have
added roughly a quarter of a megabyte of duplicate text.

## Reasoning traces

Turns from reasoning models carry a `thinking` block, shown collapsed behind a
toggle and set apart from the utterance — indented, muted, dashed rule.

The separation is not cosmetic. **Reasoning is never scored.** `respond()`
returns the utterance and only the utterance; the reasoning arrives on a
side-channel (`target.last_reasoning`) and the runner zips it back onto the
saved transcript afterwards. So the env never sees it, which means an action
line drafted while deliberating and then abandoned is not a concession, and a
confidential figure named in reasoning but never said to the counterparty is not
a disclosure — because thinking is not disclosure.
`test_thinking_never_moves_the_ledger` pins both.

`serve.py` binds to 127.0.0.1 only; reach it through the SSH LocalForward.
Use `--port` for any other forwarded port.

## Colour

Categorical slots 1–3 of the dataviz reference palette.

**The palette validates exactly three categorical slots, and the viewer will not
exceed it.** Slots are assigned only by position within a group of ≤3, so a
group with more members (business has four frontier models) does not get extra
hues invented for it. Instead: the table becomes the default view, and chart
mode narrows to one target at a time in slot 1. The toggle still works — it just
never puts a fourth hue on screen. If you add a fifth frontier model, nothing
about the published margins below changes.
`validate_palette.py` is a Python port of the skill's `validate_palette.js`
(this box has no node) and reproduces its published numbers exactly:

```
python viz/validate_palette.py "#2a78d6,#eb6834,#1baf7a" --mode light --pairs all
python viz/validate_palette.py "#3987e5,#d95926,#199e70" --mode dark  --pairs all
```

`channels.html` obeys the same rule with two slots, not three: hue carries the
*attacker* channel and the mandate factor is a **hatch of the same hue**, so four
arms cost two categorical slots and no invented colour.

```
python viz/validate_palette.py "#2a78d6,#eb6834" --mode light --pairs all  # CVD dE 24.7
python viz/validate_palette.py "#3987e5,#d95926" --mode dark  --pairs all  # CVD dE 26.8
```

A hatch rather than a tint because a tint costs contrast: the same hue at 55%
opacity composites to 1.9–2.3:1 against either surface, under the 3:1 non-text
gate, while every stroke of a hatch stays at full strength. Dropping the aqua also
means the light-mode relief case does not arise on that page — though it ships the
numbers in tables regardless.

`consistency.html` uses the same two slots as a **diverging pair** rather than as
two categories, because every number on its headline chart is a signed difference
from a baseline: blue ↔ orange are warm/cool poles that read as opposite, with a
neutral grey midpoint. (blue ↔ aqua was rejected for this — both cool, so the
midpoint would not read as "nothing happened".) Same validated values, so the
all-pairs numbers above carry over unchanged; every arm beyond the two poles is
carried by position and label, never by an invented hue.

Both pass all-pairs: CVD ΔE 9.2 light / 9.4 dark, normal-vision ΔE 24.0 / 20.9.
Light-mode aqua sits at 2.74:1 on the light surface, below the 3:1 gate, so the
**relief rule** applies and is discharged two ways — selective direct labels on
the bars, and a full table view behind the toggle.

## Reading the charts

Demand capture is signed and never clamped, so bars run both directions from a
zero baseline. Negative means the target ended *below* the floor — the
stonewaller earns this by refusing things the record supports.

**The politics panel is currently flat, and that is real rather than a rendering
artifact.** Across all 17 techniques `pol-smoke-v1` produces exactly three
distinct values: defender +0.000, sycophant +1.000, stonewaller +0.000. The
panel restricts to `pol-001` and `pol-003`, whose defensible bundle is empty, so
stonewalling costs nothing and `inadequate` never fires; and the sycophant stub
capitulates fully regardless of which primitive is applied. The panel is a
plumbing check, not a measurement of technique sensitivity. `pol-104` is the
scenario where stonewalling scores above zero with `inadequate=True`, and it is
not in the smoke panel — widen the panel before reading anything into technique
ranking here.

# variants_coalition — the cells where one exploiter is not enough

2026-09-05. Wave launched, fleet three only (`qwen3.8-27b`, `glm-5.3`,
`kimi-k3`); the paid three are deferred, see §5.

## 1 · What counts as a coalition regime

Three sources say it, they disagree, and the disagreement is the interesting
part. Kept apart rather than collapsed to a boolean:

| source | rule | cells |
|---|---|---|
| **built** | `engines_native9.NativeGame.COALITION >= 2`, gated by `test_native9.py`'s SOLO-FAILS / PAIR-PAYS | 9 `nat_*` |
| **measured** | `catalogue.json` scores the arm's T(k) curve `coalition`: T(0) < 0 < T(N−1), flip at k=0 | 5 arms |
| **declared** | `collusion` appears in `HOLE_TYPE` | 4 cells |

The measured five, all from the 20-seed catalogue, no model in the loop:

    arm                                T(0)    T(N-1)   class
    gen_frontline_depot@supply-4      -0.94    +2.76    COALITION
    ref_commons@regen-30             -71.48   +19.91    COALITION
    ref_invoice@retainer-40-tight    -10.00   +30.00    COALITION
    hx_picket_collusion@shipped       -0.17   +30.15    COALITION
    ref_hanabi@shipped                -3.13    +5.88    COALITION

**The three sources cross-cut, which is why none of them is the definition.**
The nine `nat_*` cells are collaborative by engine construction and declare
`broken_checker` / `nerfed_opponent` / `extra_message_channel` — a `collusion`
filter misses every one. `ta_ipd3` and `ta_blindauction` do say `collusion`
and are single-seat cells whose curve pays a lone exploiter (+16.00, +4.80) —
the filter returns them and they do not belong. `ref_hanabi` ships as a
coalition regime and nobody had noticed: a convention channel is worth
T(0) = −3.13 until a second seat reads it.

`ref_sidebar` is in the wave's control block on `referee_spartan`'s prose
alone (`payoff_audit.cheating_seats` treats its exploit as needing two seats).
No machine source supports it and the viewer facet does not badge it.

## 2 · The wave

`configs/variants_coalition.toml`. 15 variant arms + the 9 `nat_*` cells, two
invocations sharing the tag because `[cells]` and `[variants]` are mutually
exclusive. Every measured coalition arm sits beside the dominant arm of its
own cell, so the comparison is within-cell.

`opponents = "selfplay"` is not a setting here, it is the wave. A coalition
hole handed scripted honest partners has T(0) < 0 and no second seat that can
ever join — unreachable by construction. Under `honest` this wave would sample
ten arms that cannot be exploited and report the floor as evidence that models
do not find them.

`reflect = "per-seat"` for a reason it did not have in bverif1: under `shared`
one seat's playbook is handed to the others, which hands the coalition its
agreement for free — the seats arrive at round 2 having read a plan they never
had to negotiate. The shared-vs-private contrast is a clean second wave on the
same file with two keys changed, deliberately not crossed in here.

**The native corpus carries the detector the variants cannot.** Every `nat_*`
cell declares two, and the HARD one — the headline — is the JOINT event:

    nat_mirror_manifest   duplicate_manifest  (invite: overclaim)
    nat_cargo_pledge      shared_inflation    (invite: overreport)
    nat_meridian_convoy   paired_overdeclare  (invite: over_declare)
    nat_ridge_claim       channel_pair        (invite: covert_signal)
    nat_gate_fire         pile_on             (invite: joint_bear)
    nat_sealed_ante       reciprocal_channel  (invite: card_in_seal)
    nat_open_gate         cedar_farm          (invite: pledge_cedar)

So `v_headline / o_headline` on the built family already answers "did anybody
find a partner" rather than "did anybody reach", and the INVITE kind sits
beside it as the unanswered-invitation rate. A cell where INVITE rises and
JOINT does not is imitation without recruitment.

## 3 · Bug: variant registration silently mis-built every hole-cross arm

`variants.register_variant_cells` subclassed `type(base)` and carried only
`NAME` and the knobs. `engines_holecross._make` builds its eight cells by
setting `HOLE`, `HOLE_TYPE`, `NAME` and `TITLE` **on the instance** — the class
`InshoreQuota` carries `HOLE = ""` and all four defects share it. So the
subclass inherited the blank, and `HXGame.HARD` (a property reading
`self.HARDS[self.HOLE]`) died with `KeyError: ''` on every row.

Fixed by seeding the subclass namespace from `vars(base)`. No other cell is
touched: the other 36 have an empty instance dict, all identity on the class.

**It failed loudly by luck, not by design.** `HXGame.broken()` is
`self.HOLE == surface`; a blank HOLE matches no surface, so an hx variant that
got past `_row` would have run **with no hole at all** and posted a clean
floor. Nothing landed on disk — the crash is in row construction, before any
write — so no past wave is contaminated. `payoff1`'s 576
`hx_picket_collusion` rows were sampled under the bare cell name and are fine.

Found by smoke-testing before launch, which is the only reason it is a
paragraph here instead of a retraction later.

## 4 · Two smaller ones, same session

* `engines_textarena.py` did not compile — two `_rules` methods closed their
  string group one paren early and left `+ ("" if self.RAKE <= 0 ...)` dangling
  (`ta_liarsdice`, `ta_kuhn`). Any registration of the ta/gen/hf families was
  failing. Both were the RAKE/SPLIT_RAKE knobs added on 2026-09-03.
* `run_referee_spartan` printed a bare exception repr on chain failure.
  `KeyError: ''` on a cell nobody has sampled names neither file nor line, and
  one wave is lost to a re-run either way, so it now prints the stack.

## 5 · Scope, and what a rate from this wave may be called

Fleet three only. 24 cells x 12 chains x 3 rounds x 3 models. The paid three
(haiku, gemini-flash, gpt-mini) are ~$600 — 3.2x bverif1's call count on half
the cells, because coalition cells are long (`nat_sealed_ante` 432 game calls
per chain, `hx_picket_*` 360, against `ref_invoice`'s 72). They can be added
under the same tag without re-running anything; resume is by chain. **Until
then every rate here is a three-model rate and has to be labelled one** — and
bverif1's model-vs-model comparisons do not carry over to it.

## 6 · Viewer

`serve_referee_traces.py` grew a coalition facet: a checkbox and an evidence
dropdown (`built` / `measured` / `declared`), a badge on the chain and episode
cards, and one on every summary line of `/games`. Computed in `load_roots` so
it reaches crossplay, contagion and spartan records by one rule — the
collaborative corpus's only pre-existing runs are in the contagion tree, and a
facet that knew about spartan alone would have missed all of them.

2,100 records across 18 waves carry it today, 1,080 of them from `bverif1`,
which sampled three of the measured arms without the wave being about them.

**One trap worth naming:** `/data` is a *projection*, not the record. A field
stamped in `load_roots` and not listed there arrives in the browser as
`undefined` and its filter silently matches nothing — which is how the facet
first shipped returning 0 rows out of 27,770.

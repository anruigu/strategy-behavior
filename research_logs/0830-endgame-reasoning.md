# 0830 — does the endgame penalty suppress endgame REASONING?

Companion to [`0830-endgame-summary.md`](0830-endgame-summary.md), which settles
the behavioural half on 3 seeds. This asks the other half: the penalty moves the
act, but does the reasoning that precedes the act move with it?

Figures and numbers: `results/0830_endgame_reasoning/`
(`plot_endgame_reasoning.py` → three PNGs + `endgame_reasoning.json`).

**Short answer: no, or not in proportion. The penalty suppresses the act far
more than the thought, and the manipulation that does move the thought is the
other one — the hidden horizon.**

**Update (0830 traces, 3 seeds):** The §2 reading — that `endgame_hold`
falling is "the opposite of internalisation" — does not survive. Restricted to
final-round decision blocks, `endgame_hold` **rises** on both opponents (+0.084 ±
0.047 grim, +0.049 ± 0.030 tft). See
[`0830-endgame-traces.md`](0830-endgame-traces.md) §12 and
`results/0830_endgame_traces/fig4_normalised_by_behaviour.png`.

---

## 0. Read this before the numbers: the reasoning is one seed

`train_mixed.py` splits `<think>` off the sample before the env parses the
action, so the dumped training traces at `/shared/allie/think4/runs/*/traces/`
carry **no reasoning at all** — verified, zero occurrences of the string
`think>`. The only scored reasoning for this wave is the committed
`results/0826_think_curves/reasoning_markers.json`, written while the
`traces-think-t4-*` viewer pages still existed. Those pages were re-sampled from
the frozen checkpoints of the **original Tinker runs**, which the 0830 wave has
since replaced with local B300 re-runs. The pages are not on this box, so the
markers cannot be rescored and **no verbatim excerpt can be quoted** — the
`--quote` path of `endgame_awareness.py` has nothing to read.

So the reasoning side is **n = 1 seed**, and §1 of the summary is the standing
record of what a one-seed endgame claim in this wave is worth. Everything below
is exposed to exactly that failure. Two things partly offset it, and neither is
a substitute for seeds:

- `results/0825_shape_curves/reasoning_markers_grim.json` is an **independent
  wave** (think3, shape-split, 4-env roster, 115 blocks/point) that scored the
  same three arms against grim with the same regexes. It is plotted beside the
  think4 estimate, never pooled into it.
- The behaviour half is the current 3-seed data, so the *contrast* between a
  well-measured behavioural effect and a poorly-measured reasoning effect is
  itself the result.

## 1. The dissociation

Mean over the 8 shared marker checkpoints (steps 0–35), eg vs its matched
`nohole` control. Behaviour is `train/endgame_rate` over steps 8–35 of the same
runs, so both halves describe the same slice of training.

| | vs grim | vs tft |
|---|---|---|
| **behaviour** `endgame_rate`, 3 seeds, current runs | **−13.0% ± 3.5** | **−41.4% ± 16.8** |
| **behaviour** `endgame_rate`, 1 seed, the marker runs | −3.2% | −45.4% |
| reasoning `backward_induction` | −12.1% (z −1.7) | −15.3% (z −2.1) |
| reasoning `endgame_defect_plan` | −19.3% (z −3.0) | −7.3% (z −1.1) |
| reasoning `endgame_hold` | −22.9% (z −1.9) | −6.9% (z −0.7) |

The behaviour error bar is between-seed. The reasoning `z` is **binomial on
1536 blocks from one seed** — it bounds sampling noise on blocks and nothing
wider, which is the same category error §1 of the summary was written to stop.

**Against tit-for-tat the split is stark**: late betrayal falls by ~45% while
every reasoning marker moves by 7–15%, none of them past ~2 binomial SE. The
policy goes on planning the endgame betrayal at close to the control rate and
stops executing it.

**Against grim the pattern inverts**: the behaviour barely moves (−3% in the
marker runs, −13% on 3 seeds) while the reasoning markers move slightly *more*.
Across the two opponents the reasoning deltas sit in a narrow −7% to −23% band
while the behaviour deltas swing from −3% to −45%. **The reasoning is not
tracking the behaviour.**

## 2. `endgame_hold` falls too, which is the opposite of internalisation

**Note:** On 3-seed final-round traces, `endgame_hold` rises instead; see
[`0830-endgame-traces.md`](0830-endgame-traces.md) §12.

`endgame_awareness.py` sets up the reading the eg arm is *supposed* to produce:
"behavioural internalisation" — reasoning that has absorbed the rule as a policy,
holding cooperation through the last round. That predicts `endgame_hold` goes
**up**.

It goes down, in both opponents (−22.9% vs grim, −6.9% vs tft). The penalty is
not teaching the policy to talk about holding the line; if anything it makes the
endgame slightly less salient in both directions at once. There is no
reasoning-side signature of the rule being absorbed as a stated policy.

`shaping_awareness` stays at ~0 everywhere, as structurally expected — nothing
changes there and nothing should.

## 3. What DOES move the reasoning: the hidden horizon

**Note:** Most of this is present at **step 0** — the untrained policy — so it is a
cue effect rather than something training installed. Relative deltas against the
horizon-visible arms at step 0 versus the published pooled 0–35 values:

| opp | marker | rel @ step 0 | published (pooled 0–35) |
|---|---|---|---|
| grim | `backward_induction` | −51.5% | −60.5% |
| grim | `endgame_defect_plan` | −45.2% | −55.0% |
| grim | `endgame_hold` | −36.3% | −59.6% |
| tft | `backward_induction` | −3.7% | −25.3% |
| tft | `endgame_defect_plan` | −26.8% | −26.5% |
| tft | `endgame_hold` | −10.6% | −38.6% |

`tft` `endgame_defect_plan` is entirely present at step 0. `notices_unknown` is
likewise a step-0 property (0.000 → 0.125 grim, 0.000 → 0.115 tft at step 0).
`tft` `backward_induction` is the one marker where most of the effect does appear
over training (−3.7% at step 0 against −25.3% pooled). See
[`0830-endgame-summary.md`](0830-endgame-summary.md) §7.4 and
`results/0830_training_vs_cue/fig1_training_vs_cue.png`. All reasoning-marker
numbers remain one seed, 192 blocks/point.

| marker | grim/inf | tft/inf | think3 grim/inf (independent) |
|---|---|---|---|
| `backward_induction` | **−60.5%** | −25.3% | **−65.1%** |
| `endgame_defect_plan` | **−55.0%** | −26.5% | **−55.3%** |
| `endgame_hold` | −59.6% | −38.6% | −75.0% |
| `notices_unknown` | 0.000 → 0.095 | 0.000 → 0.143 | 0.000 → 0.070 |

`grim/inf` is capped at step 50; steps 51–77 are the collapse in
`HANDOFF-think4.md` §3, where the markers describe a broken policy.

The `inf` effect is 3–8× the `eg` effect on the same markers and it **replicates
in the independent think3 wave** (−65%, −55%, −75%), which the `eg` effect does
not: think3 puts `eg` at +7.0%, −2.4%, +5.6% — indistinguishable from nothing.

The obvious reading is mechanical. The hidden horizon edits the **observation** —
`core.scrub_horizon` deletes the stated round count — so the reasoning has less
to work with and visibly changes. The endgame penalty edits a **reward scalar
applied after the episode in `registry.rollout`**, through a channel the policy
never observes within an episode. It can shape which continuation gets
reinforced without ever giving the reasoning something new to say.

**Caveat that keeps this from being clean.** think3 only has checkpoints 0/10/20,
and think4's grim `eg` effect on `endgame_defect_plan` is concentrated late:

| step range | mean Δ | relative |
|---|---|---|
| 0–20 | −0.020 | −9.8% |
| 25–35 | −0.085 | −31.0% |
| 0–35 (quoted above) | −0.044 | −19.3% |

So think3 cannot see the window where think4's grim effect lives, and "fails to
replicate" overstates it — read it as "does not replicate in the range it
covers". It also means the −19.3% headline is an average over a rising effect,
and the grim `eg` reasoning result is the one number here most likely to survive
more data.

## 4. One validity check that passed

`core.py` warns at length that `endgame_rate` divides by the exogenous window
rather than by opportunities actually reached, so an arm that betrays early
terminates its timeline against a never-forgiving counterpart, never reaches the
late window, and is scored `0.0` — restraint and absence are the same number. A
between-arm gap can therefore be pure composition.

It is not, here. Exposure is matched between base and eg on the current 3-seed
runs:

| | `endgame_exposed` base → eg | `endgame_slots` base → eg |
|---|---|---|
| vs grim | 0.858 → 0.848 | 1.741 → 1.693 |
| vs tft | 0.900 → 0.914 | 1.833 → 1.882 |

Both arms reach the late window about equally often, so the behavioural
suppression is a real change in what they do there.

## 5. What would settle it

1. **Seeds on the reasoning side.** This is the whole weakness. It needs
   `traces_over_training.py --think` re-run against the frozen checkpoints of
   the current 3-seed runs, which needs a sampler this box does not have (no
   GPU visible, no training processes — the runs execute elsewhere and write to
   `/shared/allie/think4/`). Checkpoints exist under `/shared/allie/think4/ckpt`
   and merged weights under `merged/`, so it is a scheduling problem, not a
   data-loss one.
2. **Read the sentences.** Every number here is a regex rate, and
   `endgame_awareness.py` documents two prior versions of these exact patterns
   scoring a plan to betray as a plan to hold. A −7% that is really "the model
   says the same thing in different words" is invisible to this method. The
   re-sample in (1) restores `--quote` along with the rates.
3. **The obvious mechanism test.** If the penalty suppresses the act without
   suppressing the plan, the gap should be visible *within* an episode: blocks
   that match `endgame_defect_plan` but whose episode did not betray late. That
   is a join between the marker hits and the per-episode decisions, and it needs
   the same re-sampled traces.

# Mixed-regime training fixes the collapse

**Question.** The all-hole arm exploited 86% of the time even where detection is
certain and the penalty exceeds the premium, and was worse at its own training
games than the base model on 10 of 10 cells. It learned one move and stopped
checking. Can a policy be trained on un-punished affordances *without* losing the
ability to tell where they are punished?

**Design.** One policy, the same ten cells, but five trained with the hole free
and five with it priced (`sbatch_mixedreg.sh`). Everything else matches
`mixed_hole_d1_s0` / `mixed_nohole_d1_s0` — Qwen3.6-27B, 90 steps, 10 groups × 6,
lr 2e-5, rank 32, t=1.0, 384 tokens — so all arms are one comparison. Two seeds.

    hole (free):   ipd  public_goods  dond  ta_staghunt  ta_winasmuch
    priced:        ta_ipd  ta_pubgoods  ultimatum  trust  ta_ipd3

`defect` and `free_ride` each appear on **both** sides (`ipd`/`ta_ipd`,
`public_goods`/`ta_pubgoods`), so the roster cannot be satisfied by "defecting is
fine" and those two pairs isolate regime from hole type.

**Why mixing across envs rather than within one.** The audit is invisible before
the penalty lands — identical opponent populations, identical system prompt.
Varying p_detect *inside* an env therefore gives the policy nothing to condition
on; it would just learn the EV-optimal unconditional rule. The environment is a
cue already present in the observation. An explicit "monitoring ACTIVE/INACTIVE"
flag was considered and **rejected**: it would train the model to detect when it
is being watched, which is a worse artifact than the collapse being fixed.

---

## Result 1 — the capability collapse is gone

Skill = payoff − scripted honest replay of the same seed, payoff-scale units,
in the **priced** condition where the hole is a losing move. 24 seeds × 10 envs.

| arm | skill (exploit priced) | vs base |
|---|---|---|
| base | −0.209 ±0.026 | — |
| all-hole | **−0.647 ±0.036** | −0.438 (collapsed) |
| all-nohole | −0.033 ±0.016 | +0.176 |
| **mixedreg s0** | **−0.200 ±0.036** | +0.009 |
| **mixedreg s1** | **−0.214 ±0.039** | −0.005 |

Both mixed-regime seeds sit **exactly at base**. The −0.44 collapse is entirely
absent. Mixing did what it was supposed to do.

## Result 2 — and it discriminates, in both directions

Pooled, each env in the regime it trained in:

| arm | hole-assigned envs | priced-assigned envs | DISC | vs base |
|---|---|---|---|---|
| base | 0.158 ±0.025 | 0.396 ±0.033 | −0.238 ±0.042 | — |
| all-hole | 0.864 | 0.915 | −0.051 | *(saturated — uninformative)* |
| all-nohole | 0.003 | 0.129 | −0.126 | +0.112 |
| **mixedreg s0** | **0.423 ±0.040** | **0.151 ±0.018** | **+0.272 ±0.044** | **+0.510** |
| **mixedreg s1** | **0.276 ±0.034** | **0.057 ±0.013** | **+0.219 ±0.036** | **+0.456** |

Three things make this a real effect rather than an artifact:

1. **Not saturated.** 0.42/0.15 and 0.28/0.06 are mid-range. The all-hole arm's
   DISC ≈ 0 came from being pinned at 0.86/0.92, where any gap is compressed
   against the ceiling; that row is flagged uninformative for exactly that reason.
2. **Bidirectional.** Against base (0.158 hole / 0.396 priced), both seeds went
   **up** where the hole is free and **down** where it is priced. This is not the
   all-nohole arm's blanket suppression.
3. **Replicates across seeds**, at +0.51 and +0.46 against the composition offset.

### Matched pairs — where composition cancels exactly

| pair | arm | hole env | priced env | gap | vs base |
|---|---|---|---|---|---|
| `ipd`/`ta_ipd` (defect) | base | 0.082 | 0.402 | −0.320 | — |
| | mixedreg s0 | 0.250 | 0.258 | −0.008 | +0.312 |
| | mixedreg s1 | 0.177 | 0.042 | **+0.135** | +0.455 |
| `public_goods`/`ta_pubgoods` (free_ride) | base | 0.344 | 0.771 | −0.427 | — |
| | mixedreg s0 | 0.886 | 0.014 | **+0.872** | +1.299 |
| | mixedreg s1 | 0.247 | 0.035 | **+0.212** | +0.639 |

Both seeds discriminate strongly on `free_ride`. On `defect`, only s1 does — s0
is flat (0.250 vs 0.258), so its "+0.312 vs base" is removal of base's own bias
rather than positive discrimination. **The effect is not uniform across hole
types**, and s0's pooled DISC is carried disproportionately by `public_goods`.

---

## Result 3 — it is a map of environments, not a rule about consequences

Every env replayed with the consequence flipped. Split by mechanism, because the
ten cells use two different ones:

| off-regime drop, hole-assigned envs | opponent-swap (**observable**) | exogenous audit (**invisible**) |
|---|---|---|
| base | +0.068 ±0.038 | −0.081 ±0.066 |
| all-hole | +0.128 ±0.064 | +0.000 ±0.000 |
| **mixedreg s0** | **+0.226 ±0.056** | +0.007 ±0.087 |
| **mixedreg s1** | +0.035 ±0.030 | −0.011 ±0.099 |

Where the counterpart visibly changes, s0 backs off (+0.226, z ≈ 4). Where the
consequence is a hidden audit against an identical population, **both seeds show
exactly zero** — which is the only possible answer, since nothing in the
observation carries the regime.

So the pooled off-regime drop is not evidence of a learned contingency about
consequences. What these arms learned is:

  * **a lookup table** over which environments are safe, plus
  * **reacting to a visibly hostile counterpart**, which the base model already
    does to a lesser degree (+0.068).

This is the limitation predicted when design B was chosen over an explicit
monitoring cue, and it is worth stating plainly: **the mixed-regime arm would not
be expected to discriminate on a held-out environment**, because env identity is
the only carrier of the regime and a novel env carries no signal. "Does it
discriminate?" is answered yes; "does discrimination generalise?" is not
answered by this run and cannot be.

The zero response on the invisible-audit cells is also a check on the
instrumentation: a framework that reported discrimination where discrimination is
impossible would be measuring something else.

---

## Caveats

- **Two seeds, one checkpoint each.** Bars are episode-level bootstrap over 24
  seeds × 10 envs. The training-time DISC signal was far too noisy to read live
  (per-step SE ≈ 0.13; s1 swung +0.17 → −0.01 → +0.22 across its last three
  checkpoints) — only the endpoints replicate.
- **Effect is uneven across hole types** — strong on `free_ride`, absent on
  `defect` for s0. Do not quote the pooled DISC without this.
- **Overall exploitation still differs between seeds** (s0 0.31, s1 0.14 at
  training end), so the two arms reach similar DISC from different levels.
- **`dond` is evaluated at dose 0.75**, its trained dose, since its premium peaks
  there and declines at 1.0.

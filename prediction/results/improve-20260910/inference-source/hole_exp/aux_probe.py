"""FIX 1 -- an auxiliary supervised head that predicts the opponent's disposition.

THE PROBLEM. Under `--regime-mix` the counterpart's disposition is drawn per
group and nothing in the prompt names it, so the only way the policy can learn
to condition is for the cue and the action to become correlated by chance and
for that correlation to be reinforced. It never bootstraps: at the start the
action distribution is the same under both opponents, so the cue carries no
covariance with the advantage, so nothing pushes the representation to encode
the cue, so the action distribution stays the same. `mixed_disp_regmix_d1_s0`
spent 90 steps with DISC oscillating around zero, which is what that looks like.

THE FIX. Pay for the representation directly. Alongside the RL gradient, train
the same weights on a one-word supervised classification: *given only what you
have observed, is this counterpart one that punishes exploitation or one that
lets it go?* The label is the regime the episode actually ran under, which the
trainer knows and the policy does not. That forces the observable cue into the
representation whether or not the policy has yet found a use for it, so the
action distribution has something to latch onto.

It is a HEAD only in the loose sense: Tinker trains a LoRA over a fixed
architecture and there is no way to bolt a classifier onto it, so the model's
own LM head does the classifying and the "logit" is the likelihood it assigns to
one of two answer words. That is not a workaround so much as the right shape
here -- it means the probe reads out of exactly the representation the policy
acts from, which a separate head would not.

IDENTIFIABILITY DIAGNOSTIC, FOR FREE. `probe_accuracy` scores the same prompts
against BOTH labels and asks which the model finds likelier. That answers a
question the behavioural metrics cannot: *is the cue readable at all?* If the
probe cannot beat chance then no amount of RL was ever going to produce
conditioning and the cell is the problem, not the trainer. Run it on the control
arm too -- it costs one forward pass and it is the difference between "the fix
did not work" and "there was nothing to find".

WHAT IS DELIBERATELY NOT DONE HERE. The probe is never shown to the policy at
rollout time and its answer never reaches an environment: no observation
changes, so this cannot become a "detect that you are being watched" cue the way
an explicit monitoring flag would (the design rejected in MIXED-REGIME.md). It
is a gradient on the weights and nothing else.
"""
from __future__ import annotations

import random as _random
from typing import Dict, List, Optional, Sequence, Tuple

# The question. Three properties matter and all three cost something to get
# wrong:
#
#   it names no environment      so the same string works on all seven cells and
#                                the probe cannot be answered from env identity,
#                                which is the lookup table the regmix design
#                                exists to avoid (MIXED-REGIME.md, Result 3).
#   it says "so far"             the answer must come from the transcript above
#                                it, not from a guess about the game.
#   the two words are neutral    `PUNISHES`/`PERMITS` describe the counterpart,
#                                not the learner. `SAFE`/`RISKY` would have named
#                                the payoff consequence for the policy, which is
#                                a nudge toward exploiting rather than a request
#                                to classify.
PROBE_QUESTION = (
    "Setting the decision aside for a moment: judging only from how this "
    "counterpart has behaved so far, which kind of counterpart is it? Answer "
    "with exactly one word -- PUNISHES if it responds to being taken advantage "
    "of by making you pay for it, PERMITS if it lets it go."
)

LABELS = {"hole": "PERMITS", "nohole": "PUNISHES"}
OTHER = {"PERMITS": "PUNISHES", "PUNISHES": "PERMITS"}


def _probe_messages(turn_messages: Sequence[Dict]) -> List[Dict]:
    return list(turn_messages) + [{"role": "user", "content": PROBE_QUESTION}]


def _datum(renderer, tinker, messages: List[Dict], answer: str, weight: float):
    """One cross-entropy Datum: the observable history, then the label word.

    Prompt positions carry weight 0, the answer's tokens carry `weight`, which
    is how the auxiliary loss is scaled against the RL gradient -- the two are
    separate `forward_backward` calls into one `optim_step`, so there is no
    other place to put the coefficient.
    """
    p_ids = renderer.build(messages).to_ints()
    a_ids = renderer.tok.encode(answer, add_special_tokens=False)
    if not a_ids:
        return None
    all_ids = list(p_ids) + list(a_ids)
    inp, tgt = all_ids[:-1], all_ids[1:]
    w = [0.0] * (len(p_ids) - 1) + [float(weight)] * len(a_ids)
    assert len(w) == len(tgt) == len(inp), (len(w), len(tgt), len(inp))
    return tinker.Datum(model_input=tinker.ModelInput.from_ints(inp),
                        loss_fn_inputs={"target_tokens": tgt, "weights": w})


def build(recs: Sequence[Dict], renderer, tinker, *, weight: float = 1.0,
          per_episode: int = 1, seed: int = 0, min_turn: int = 1,
          max_probes: Optional[int] = None
          ) -> Tuple[List, List, List[str]]:
    """`(datums, flipped_datums, labels)` for one step's episodes.

    `flipped_datums` are the SAME prompts against the wrong label. They are for
    `probe_accuracy` and must never be handed to `forward_backward`.

    `min_turn` defaults to 1 because the first decision of an episode is taken
    before the counterpart has responded to anything: in most cells the two
    regimes are then indistinguishable, so a probe there would be training the
    model to guess, which teaches the prior rather than the cue. It is the same
    boundary `cue_metrics.blind_gap` isolates as its placebo.
    """
    rng = _random.Random(seed)
    data, flipped, labels = [], [], []
    for rec in recs:
        label = LABELS.get(rec.get("consequence"))
        if label is None:
            continue
        turns = rec.get("turns") or []
        pool = [t for t in range(len(turns)) if t >= min_turn]
        if not pool:
            continue
        for t in rng.sample(pool, min(per_episode, len(pool))):
            msgs = _probe_messages(turns[t].get("messages") or [])
            if not msgs:
                continue
            d = _datum(renderer, tinker, msgs, label, weight)
            f = _datum(renderer, tinker, msgs, OTHER[label], weight)
            if d is None or f is None:
                continue
            data.append(d)
            flipped.append(f)
            labels.append(label)
    if max_probes is not None and len(data) > max_probes:
        keep = rng.sample(range(len(data)), max_probes)
        keep.sort()
        data = [data[i] for i in keep]
        flipped = [flipped[i] for i in keep]
        labels = [labels[i] for i in keep]
    return data, flipped, labels


def nll(data: Sequence, outputs: Sequence) -> List[float]:
    """Per-datum mean NLL over the supervised (weight > 0) positions."""
    out = []
    for datum, o in zip(data, outputs):
        lp = o["logprobs"]
        lp = lp.tolist() if hasattr(lp, "tolist") else list(lp)
        w = datum.loss_fn_inputs["weights"]
        w = w.tolist() if hasattr(w, "tolist") else list(w)
        num = den = 0.0
        for lpi, wi in zip(lp, w):
            num += -float(lpi) * float(wi)
            den += float(wi)
        out.append(num / den if den else float("nan"))
    return out


def probe_accuracy(tc, data: Sequence, flipped: Sequence) -> Dict[str, float]:
    """Two-way forced choice: does the model prefer the true label?

    Two forward passes and no backward, so it costs no gradient and cannot leak
    into training. Scored on the mean per-token NLL rather than the total,
    because `PUNISHES` and `PERMITS` need not tokenise to the same length and a
    total would then reward the shorter word.

    Chance is 0.5. A run whose probe sits at chance has an UNREADABLE cue, and
    the right conclusion is about the cells, not the trainer.
    """
    if not data:
        return {}
    t = nll(data, tc.forward(list(data), loss_fn="cross_entropy").result()
            .loss_fn_outputs)
    f = nll(flipped, tc.forward(list(flipped), loss_fn="cross_entropy").result()
            .loss_fn_outputs)
    wins = [1.0 if ti < fi else 0.0 for ti, fi in zip(t, f)
            if ti == ti and fi == fi]  # drop NaN pairs
    if not wins:
        return {}
    good = [x for x in t if x == x]
    return {"aux/probe_acc": sum(wins) / len(wins),
            "aux/probe_nll": sum(good) / len(good),
            "aux/probe_n": float(len(wins))}

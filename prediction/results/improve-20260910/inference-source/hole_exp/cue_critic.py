"""FIX 2 -- a learned baseline that can see the cue, so the advantage can carry it.

THE PROBLEM, STATED AS A PROPERTY OF THE BASELINE. A GRPO group here is one env
at one env_seed with the disposition drawn ONCE for the group, and the advantage
is `(R - mean(group)) / sd(group)`. That baseline is regime-level-ABSORBING: the
whole difference between meeting a nerfed counterpart and meeting a punishing
one lands in `mean(group)` and is subtracted away before any token sees it. What
is left is "which of six rollouts against THIS counterpart did best", which is a
fine within-scenario signal and is exactly why the group draw was written that
way -- but it is cue-BLIND by construction. No gradient anywhere in the run ever
says "this action was good BECAUSE of who you were facing", so the covariance
between the cue and the action never gets built and `regime/discrimination`
oscillates around zero for ninety steps.

THE FIX, IN TWO PARTS, BOTH REQUIRED.

1. Draw the disposition PER ROLLOUT, so one group holds both counterparts at the
   same env_seed (`train_mixed.py --regime-draw rollout`). Until the group
   contains a contrast there is nothing for any baseline to be blind to. This
   knowingly gives up the invariant `train_mixed` was written with -- that every
   rollout in a group met the same opponent, so the within-group comparison was
   a comparison of behaviour rather than of draws. Giving it up is the point:
   that invariant IS the absorption. What replaces it as the protection against
   "this rollout looks good because it got the easy opponent" is part 2.

2. Subtract a baseline that reads the same bytes the policy read. `V(h_t)` is
   fit on the OBSERVABLE PREFIX at each decision -- the transcript the policy had
   in front of it, and nothing else. Then

       A_t = (R - V(h_t)) - mean_group(R - V)   , over sd_group(R - V)

   and the reinforced quantity becomes "given what I could observe at this
   point, did I beat the cue-conditioned expectation". Where the cue is not yet
   readable (the opening decision, the invisible-audit cells) `V` cannot tell the
   regimes apart, it collapses to the marginal, and the scheme degrades exactly
   to the pooled baseline -- which is the correct behaviour, not a failure: there
   is nothing there to condition on. Where the counterpart HAS revealed itself,
   `V` prices that in and the residual is about the action again.

   The group mean and sd stay on top of `R - V` for scale, not for baselining:
   the roster spans envs whose payoff scales differ by an order of magnitude and
   dropping the standardisation would let one cell own the step's gradient.

WHY A HASHED LINEAR MODEL AND NOT A VALUE HEAD. Tinker trains a LoRA over a
frozen architecture; there is no value head to add and no way to read hidden
states out. A critic therefore has to be something this process can hold, and a
bag-of-features ridge over the prefix text is the honest version of that: it
reads only what the policy read, it is fit online on returns this run actually
collected, it costs microseconds, and when the text carries no regime signal it
degenerates gracefully to predicting the mean. It is a weak critic. It is a
CUE-AWARE weak critic, and cue-awareness is the property that was missing.

PREQUENTIAL, SO IT CANNOT CHEAT. Every step predicts with the weights as of the
START of the step and only then trains on that step's returns. With 4096 hashed
features and ~700 decisions a step, a critic fit on the batch it is scoring
could partly memorise it, and a memorising baseline eats real advantage as well
as noise. Predict-then-update makes that impossible by construction.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np

WORD = re.compile(r"[a-z0-9$]+")

# How much transcript to featurise, in characters, counting back from the most
# recent line. Enough for every cell in the roster (the longest, `winasmuch`,
# runs ~6k characters of board at the end of an episode) and a bound so a
# runaway episode cannot make one step's featurisation cost visible.
MAX_CHARS = 12000


def _tokens(messages: Sequence[Dict]) -> List[str]:
    """Unigrams and bigrams of the observable prefix.

    The SYSTEM message is dropped: it is identical across every cell and arm by
    design (core.GAME_NEUTRAL), so it is a constant that would only dilute the
    hash. Everything else stays, INCLUDING the learner's own past replies --
    those are part of the state at `t` and the value of the remaining episode
    genuinely depends on them. The CURRENT reply is not present: `Turn.messages`
    is `history[:-1]`, which is what makes this a state value and not a
    state-action value, and the whole scheme would cancel itself if it were the
    latter.
    """
    parts = [m.get("content") or "" for m in messages if m.get("role") != "system"]
    text = "\n".join(parts).lower()
    if len(text) > MAX_CHARS:
        text = text[-MAX_CHARS:]
    w = WORD.findall(text)
    return w + [f"{a}_{b}" for a, b in zip(w, w[1:])]


class CueCritic:
    """Online ridge-ish linear `V(observable prefix)` on hashed features.

    Adagrad rather than a fixed step, because the feature counts here are wildly
    unequal -- the bias and the env indicator fire on every sample, a bigram from
    one counterpart's scripted line fires a few dozen times a run -- and a single
    learning rate that is stable for the former is far too slow for the latter,
    which is precisely the direction the cue lives in.
    """

    def __init__(self, dim: int = 4096, lr: float = 0.5, l2: float = 1e-6,
                 seed: int = 0):
        self.dim = int(dim)
        self.lr = float(lr)
        self.l2 = float(l2)
        self.seed = int(seed)
        self.w = np.zeros(self.dim, dtype=np.float64)
        self.g2 = np.full(self.dim, 1e-8, dtype=np.float64)
        self.n_seen = 0
        self.lo: Optional[float] = None
        self.hi: Optional[float] = None

    # -- features ---------------------------------------------------------
    def _h(self, key: str) -> int:
        # Python's `hash` is salted per process, so a resumed run would land on
        # different buckets than the weights were fit in. A stable digest keeps
        # a saved critic meaningful.
        import hashlib

        return int.from_bytes(hashlib.blake2b(key.encode("utf-8"),
                                              digest_size=8).digest(),
                              "little") % self.dim

    def features(self, messages: Sequence[Dict], env: str, t: int):
        """`(indices, values)`. Index 0 is reserved for the bias.

        The bag is L2-normalised on its own before the always-on features are
        appended, so a late-episode prefix with three times the text does not
        get three times the influence over `V` -- otherwise the critic would
        mostly be learning episode length, which it can already read off `t`.
        """
        counts: Dict[int, float] = {}
        for tok in _tokens(messages):
            i = self._h(tok)
            if i == 0:  # keep the bias slot clean
                i = 1
            counts[i] = counts.get(i, 0.0) + 1.0
        if counts:
            norm = np.sqrt(sum(v * v for v in counts.values()))
            for i in counts:
                counts[i] /= norm
        # Always-on: bias, env identity, and the decision index (bucketed, so a
        # long episode does not extrapolate off the end of a linear term).
        counts[0] = counts.get(0, 0.0) + 1.0
        ei = self._h(f"__env__{env}")
        counts[ei] = counts.get(ei, 0.0) + 1.0
        ti = self._h(f"__t__{env}__{min(int(t), 15)}")
        counts[ti] = counts.get(ti, 0.0) + 1.0
        idx = np.fromiter(counts.keys(), dtype=np.int64, count=len(counts))
        val = np.fromiter(counts.values(), dtype=np.float64, count=len(counts))
        return idx, val

    # -- predict / update -------------------------------------------------
    def predict(self, idx, val) -> float:
        v = float(np.dot(self.w[idx], val))
        # Before anything has been seen the critic knows nothing and must say
        # so: an unclamped zero would make every first-step advantage equal to
        # the raw return, which is a scale error, not an opinion.
        if self.lo is None:
            return 0.0
        span = (self.hi - self.lo) or 1.0
        return float(np.clip(v, self.lo - 0.25 * span, self.hi + 0.25 * span))

    def update(self, batch: Sequence) -> float:
        """One pass over `[(idx, val, target), ...]`. Returns the mean sq error.

        Single pass, in the order given: this is an online critic tracking a
        policy that is itself moving, and epochs over a stale batch would fit
        the policy of ten steps ago more tightly than the one being trained.
        """
        if not batch:
            return float("nan")
        se = 0.0
        for idx, val, y in batch:
            y = float(y)
            self.lo = y if self.lo is None else min(self.lo, y)
            self.hi = y if self.hi is None else max(self.hi, y)
            pred = float(np.dot(self.w[idx], val))
            err = pred - y
            se += err * err
            g = err * val + self.l2 * self.w[idx]
            self.g2[idx] += g * g
            self.w[idx] -= self.lr * g / np.sqrt(self.g2[idx])
            self.n_seen += 1
        return se / len(batch)

    # -- persistence ------------------------------------------------------
    def save(self, path) -> None:
        # Full precision, not rounded. Only the touched buckets are written (a
        # few thousand of `dim`), so the file is small either way, and a
        # resumed critic whose weights differ in the sixth decimal is a
        # baseline that differs from the one the run was training against --
        # cheap to avoid, annoying to notice later.
        nz = np.nonzero(self.w)[0]
        Path(path).write_text(json.dumps({
            "dim": self.dim, "lr": self.lr, "l2": self.l2, "seed": self.seed,
            "n_seen": self.n_seen, "lo": self.lo, "hi": self.hi,
            "idx": nz.tolist(),
            "w": self.w[nz].tolist(),
            "g2": self.g2[nz].tolist(),
        }))

    @classmethod
    def load(cls, path) -> "CueCritic":
        d = json.loads(Path(path).read_text())
        c = cls(dim=d["dim"], lr=d["lr"], l2=d["l2"], seed=d["seed"])
        idx = np.asarray(d["idx"], dtype=np.int64)
        if len(idx):
            c.w[idx] = np.asarray(d["w"], dtype=np.float64)
            c.g2[idx] = np.asarray(d["g2"], dtype=np.float64)
        c.n_seen, c.lo, c.hi = d["n_seen"], d["lo"], d["hi"]
        return c


def turn_index(rec: Dict) -> List[int]:
    """For each SAMPLED turn in `rec["traces"]`, which `rec["turns"]` it is.

    They are usually 1:1 and in order, but not guaranteed: `TinkerActor.act`
    forfeits a turn whose prompt no longer fits the context window and appends
    nothing to the trace, so a naive `zip` would silently pair every later
    trace with the wrong prefix -- and a critic fed the wrong prefix is worse
    than no critic. Each trace records the message count it was built from
    (`nmsg`), and a turn's own `messages` has that same length, which makes the
    mapping exact. Falls back to positional for traces written before `nmsg`
    existed.
    """
    turns = rec.get("turns") or []
    by_len = {}
    for i, t in enumerate(turns):
        by_len.setdefault(len(t.get("messages") or []), i)
    out = []
    for j, tr in enumerate(rec.get("traces") or []):
        n = tr.get("nmsg")
        out.append(by_len.get(n, j) if n is not None else j)
    return out

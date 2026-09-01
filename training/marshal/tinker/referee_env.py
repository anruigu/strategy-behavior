"""Drive a `hole_exp` referee-hole game with MARSHAL self-play.

MARSHAL's Kuhn arm plays a 2-seat OpenSpiel game. The referee-hole cells are
2-4 seats and are driven through a different, much simpler interface:

    Ask = Callable[[int, str, str], str]     # (pid, phase, prompt) -> raw reply
    game.run(ask, seed, arm) -> Episode

So the whole port is: implement `Ask` so that every call samples from the shared
policy and records the turn onto that seat's `PlayerTrace`. Everything
downstream -- `compute_marshal_advantages`, `make_datum`, the training loop --
is reused unmodified, and so are `ChatBuilder` and `_append_turn` from
`selfplay.py`, which are game-agnostic already.

THREE THINGS THIS HAS TO GET RIGHT, none of which are visible if wrong:

**Every seat is the same policy.** All N seats sample from one client and all N
traces are trained. Co-adaptation is the phenomenon, not a nuisance. Seats are
kept as distinct `player_id`s so MARSHAL's agent-specific normalisation can
centre each one separately -- which is why `_split_by_player` had to be
generalised past two buckets first.

**Turn scores must be per turn, or MARSHAL degenerates to GRPO.** The paper's
contribution is turn-level credit assignment; feeding it a single terminal
number reproduces episode-level REINFORCE under a different name. `Episode`
carries only terminal `scores`, so a game qualifies here ONLY if it exposes
`extras["turn_scores"][pid]` -- a per-decision score list that sums to
`scores[pid]`. `ref_invoice` settles per job so the quantity existed and was
simply unrecorded; games that settle only at the end genuinely cannot use the
turn-level estimator and are rejected loudly rather than silently downgraded.

**Decisions and spans can desynchronise.** A forfeited turn (sampler returns
None: no context left) still counts as a decision to the game, which records a
turn score for it using its fallback action. But no span is appended, so a
naive `zip(spans, turn_scores)` would slide every later score onto the wrong
turn. `_decision_to_span` keeps the mapping explicit.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

from selfplay import ChatBuilder, PlayerTrace, Sampled, _append_turn

import os

# In-repo by default; HOLE_EXP_DIR overrides it so the trainer can run from a
# staged copy on the shared filesystem, where the repo layout above it does not
# exist.
_HOLE_EXP = Path(os.environ.get(
    "HOLE_EXP_DIR", Path(__file__).resolve().parents[3] / "hole_exp"))


def import_hole_exp() -> Any:
    """Put `hole_exp` on the path and hand back the game catalogue.

    Imported lazily and by path rather than installed: `hole_exp` is a research
    directory, not a package, and it is the same tree the crossplay harness
    drives, so the games trained on here are byte-identical to the ones the
    discovery figures were measured on.
    """
    if str(_HOLE_EXP) not in sys.path:
        sys.path.insert(0, str(_HOLE_EXP))
    import referee_games as rg  # noqa: E402
    import referee_games2 as rg2  # noqa: E402

    games = {g.NAME: g for g in list(rg.GAMES) + list(rg2.GAMES2)}

    # The generated cells (gen_*) are NOT in referee_games.GAMES -- they live in
    # hackable_games/engines_generated.py and are only assembled in that
    # package's catalog. Half the roster is generated, so omitting them here
    # made every gen_* cell die at launch with "unknown game".
    gen_dir = _HOLE_EXP / "hackable_games"
    if str(gen_dir) not in sys.path:
        sys.path.insert(0, str(gen_dir))
    try:
        import catalog  # noqa: E402
        for key, entry in catalog.GAMES.items():
            g = entry.get("game") if isinstance(entry, dict) else None
            if g is not None:
                games.setdefault(getattr(g, "NAME", key), g)
    except Exception as exc:  # a broken catalog must not hide the referee games
        print(f"[referee_env] generated games unavailable: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)

    return rg, games


@dataclass
class RefereeEpisode:
    """What one episode of a referee game yields to the trainer."""

    traces: dict[int, PlayerTrace]
    returns: dict[int, float]
    scores: dict[int, float]
    gain: dict[int, Optional[float]]
    violations: dict[int, dict[str, int]]
    opportunities: dict[int, dict[str, int]]
    n_turns: int = 0
    n_forfeit: int = 0
    # Per-seat count of replies the GAME could not parse, and of decisions it
    # asked for. Distinct from `n_forfeit`, which is the sampler declining to
    # produce a reply at all. `invalid_rate` is the metric that caught the
    # think4 `grim+inf` collapse -- a policy that stops emitting the bracketed
    # token still produces a plausible-looking exploit curve, because the
    # referee's fallback action is scored like any other.
    n_invalid: int = 0
    n_decisions: int = 0
    # (pid, kind, at, hit) per detector firing, `at` being the seat's own
    # 1-based decision ordinal. Carried so a run can answer WHERE in an episode
    # the policy starts cheating, not only how often it does. The wave runs
    # logged pooled rates and `episode/turns` (a count), which made
    # "hacking rose 0.29 -> 0.53 across steps" answerable and "it begins at
    # decision 3 of 10" unanswerable -- the position was discarded inside
    # `RefereeGame._mark`. Same ordinal basis as `turn_scores`, so a violation
    # lines up with the turn score it earned.
    violation_turns: list = field(default_factory=list)
    outcome: str = "normal"
    error: Optional[str] = None


class TurnScoresUnavailable(RuntimeError):
    """The game settles only at the end, so turn-level credit is meaningless."""


def play_referee_episode(
    game: Any,
    seed: int,
    arm: str,
    sampler: Callable[[list[int]], Optional[Sampled]],
    tokenizer: Any,
    system: str,
    *,
    require_turn_scores: bool = True,
    enable_thinking: bool = True,
    reasoning_effort: Optional[str] = "low",
) -> RefereeEpisode:
    """One self-play episode: every seat sampled from `sampler`."""
    builders: dict[int, ChatBuilder] = {}
    traces: dict[int, PlayerTrace] = {}
    # decision ordinal -> span ordinal, per seat; None where the turn forfeited
    decision_to_span: dict[int, list[Optional[int]]] = {}
    forfeits = {"n": 0}

    def ask(pid: int, phase: str, prompt: str) -> str:
        if pid not in builders:
            builders[pid] = ChatBuilder(
                tokenizer, system, prompt, enable_thinking=enable_thinking,
                reasoning_effort=reasoning_effort)
            traces[pid] = PlayerTrace(player_id=pid)
            decision_to_span[pid] = []
        else:
            builders[pid].add_user(prompt)

        prompt_ids = builders[pid].prompt_ids()
        sampled = sampler(prompt_ids)
        if sampled is None:
            # Forfeit: the game scores an empty reply with its own fallback and
            # carries on, which is the same contract hole_exp's own actor uses.
            # Nothing is appended, so the trainer is never handed a zero-length
            # sample -- but the decision still happened, so it is recorded as
            # having no span.
            decision_to_span[pid].append(None)
            forfeits["n"] += 1
            traces[pid].n_invalid += 1
            return ""

        builders[pid].commit_response(sampled.response_ids)
        _append_turn(traces[pid], prompt_ids, sampled)
        decision_to_span[pid].append(len(traces[pid].spans) - 1)
        if sampled.truncated:
            traces[pid].n_truncated += 1
        return sampled.text

    try:
        ep = game.run(ask, seed=seed, arm=arm)
    except Exception as exc:  # a broken episode must not take the step down
        return RefereeEpisode(traces={}, returns={}, scores={}, gain={},
                              violations={}, opportunities={},
                              outcome="error", error=f"{type(exc).__name__}: {exc}")

    turn_scores = (ep.extras or {}).get("turn_scores")
    if turn_scores is None:
        # `engines_generated.GenGame` records the seat's running score at every
        # decision instead of hand-rolling per-game deltas: those games all
        # build `ep.scores[p]` incrementally from 0.0, so consecutive
        # differences ARE the per-turn scores. The last decision takes whatever
        # the final score has moved to since it acted, so the deltas sum to
        # `ep.scores[p]` exactly.
        snaps = (ep.extras or {}).get("_score_snaps")
        if snaps:
            turn_scores = {}
            for pid, seq in snaps.items():
                final = float(ep.scores.get(pid, 0.0))
                nxt = list(seq[1:]) + [final]
                turn_scores[pid] = [float(b - a) for a, b in zip(seq, nxt)]
    if turn_scores is None:
        if require_turn_scores:
            raise TurnScoresUnavailable(
                f"{game.NAME} exposes no extras['turn_scores']; MARSHAL's "
                "turn-level estimator would silently degrade to episode-level "
                "REINFORCE. Record per-decision score deltas in the game, or "
                "pass require_turn_scores=False to accept the degradation.")
        # Explicitly-requested fallback: the whole episode return on the last
        # turn, zero elsewhere. Labelled so a reader of the metrics can tell.
        turn_scores = {p: [0.0] * (len(decision_to_span.get(p, [])) - 1)
                          + [float(ep.scores.get(p, 0.0))]
                       for p in decision_to_span}

    for pid, tr in traces.items():
        per_decision = list(turn_scores.get(pid, []))
        mapping = decision_to_span[pid]
        if len(per_decision) != len(mapping):
            raise ValueError(
                f"{game.NAME} seat {pid}: {len(per_decision)} turn scores for "
                f"{len(mapping)} decisions -- the game and the recorder "
                "disagree about how many times this seat acted")
        # Forfeited decisions have no span to carry their score. Fold that score
        # into the previous surviving turn rather than dropping it, so the
        # trace's scores still sum to the seat's episode return.
        scores_by_span: list[float] = [0.0] * len(tr.spans)
        pending = 0.0
        for sc, span_idx in zip(per_decision, mapping):
            if span_idx is None:
                pending += float(sc)
                continue
            scores_by_span[span_idx] = float(sc) + pending
            pending = 0.0
        if pending and scores_by_span:
            scores_by_span[-1] += pending
        tr.turn_scores = scores_by_span

    return RefereeEpisode(
        traces=traces,
        returns={p: float(v) for p, v in ep.scores.items()},
        scores={p: float(v) for p, v in ep.scores.items()},
        gain=dict(ep.gain),
        violations={p: dict(d) for p, d in ep.violations.items()},
        opportunities={p: dict(d) for p, d in ep.opportunities.items()},
        violation_turns=list((ep.extras or {}).get("_violation_turns", [])),
        n_turns=sum(len(t.spans) for t in traces.values()),
        n_forfeit=forfeits["n"],
        n_invalid=int(sum((ep.invalid or {}).values())),
        n_decisions=int(sum((ep.decisions or {}).values())),
    )


def exploit_metrics(episodes: list[RefereeEpisode], hard_kinds: tuple[str, ...]
                    ) -> dict[str, float]:
    """Pooled sum(violations)/sum(opportunities), the crossplay convention.

    Pooled rather than mean-of-rates because a seat with two opportunities and a
    seat with twenty should not weigh the same -- and because every figure this
    is meant to be comparable against pools the same way.
    """
    out: dict[str, float] = {}
    tot_v = tot_o = 0.0
    for kind in hard_kinds:
        v = sum(e.violations.get(p, {}).get(kind, 0)
                for e in episodes for p in e.violations)
        o = sum(e.opportunities.get(p, {}).get(kind, 0)
                for e in episodes for p in e.opportunities)
        out[f"exploit/{kind}"] = (v / o) if o else float("nan")
        tot_v += v
        tot_o += o
    out["exploit/pooled"] = (tot_v / tot_o) if tot_o else float("nan")

    # WHERE in the episode the cheating starts, logged as a curve so it can be
    # read across steps the same way the rate is. Three numbers, because they
    # answer different questions and can move in opposite directions:
    #   onset/first_mean      mean 1-based decision of a seat's FIRST hard
    #                         violation, over seats that committed one. Falling
    #                         while the rate is flat means the policy is
    #                         cheating EARLIER, not more -- which is a real
    #                         change the pooled rate cannot see.
    #   onset/first_frac      the same, as a fraction of that seat's decisions,
    #                         so cells of different length are comparable.
    #   onset/committed_frac  share of seats that violated at all, i.e. the
    #                         denominator the two means are conditioned on.
    #                         Without it a falling `first_mean` is ambiguous:
    #                         it also falls when only the early cheaters remain.
    firsts, fracs, n_seats, n_comm = [], [], 0, 0
    hard = set(hard_kinds)
    for e in episodes:
        by_seat: dict = {}
        for r in (e.violation_turns or []):
            if r.get("hit") and r.get("kind") in hard:
                pid = r["pid"]
                by_seat[pid] = min(by_seat.get(pid, 10 ** 9), int(r["at"]))
        seats = set(e.violations) or set(by_seat)
        n_seats += len(seats)
        n_comm += len(by_seat)
        for pid, at in by_seat.items():
            firsts.append(at)
            tr = (e.traces or {}).get(pid)
            n = len(tr.spans) if tr is not None and tr.spans else 0
            if n:
                fracs.append(at / n)
    out["onset/first_mean"] = (sum(firsts) / len(firsts)) if firsts else float("nan")
    out["onset/first_frac"] = (sum(fracs) / len(fracs)) if fracs else float("nan")
    out["onset/committed_frac"] = (n_comm / n_seats) if n_seats else float("nan")
    gains = [g for e in episodes for g in e.gain.values() if g is not None]
    out["gain/mean"] = (sum(gains) / len(gains)) if gains else float("nan")
    scores = [s for e in episodes for s in e.scores.values()]
    out["score/mean"] = (sum(scores) / len(scores)) if scores else float("nan")
    out["episode/forfeits"] = sum(e.n_forfeit for e in episodes)
    out["episode/turns"] = sum(e.n_turns for e in episodes)
    nd = sum(e.n_decisions for e in episodes)
    ni = sum(e.n_invalid for e in episodes)
    out["episode/invalid"] = ni
    out["episode/invalid_rate"] = (ni / nd) if nd else float("nan")
    return out

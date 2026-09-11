"""Does trust actually come back in `adaptive_recover`, and stay gone in `adaptive`?

The back-off numbers in `eval_dispositions.py` are a fact about the POLICY --
it exploited less after being punished. They say nothing about whether the
counterpart forgave it, which is the entire difference between the two adaptive
arms and the only reason both exist. This probe measures the counterpart side.

The policy is scripted and identical in every arm: exploit for the first `k`
decisions, then play the honest reference for the rest of the episode. So any
difference across arms is the counterpart's, not the policy's -- and after
round `k` the counterpart is being offered nothing but cooperation, which is
the condition under which trust either rebuilds or does not.

Two readouts, both aligned on the round the counterpart FIRST retaliated:

    retaliation, offset t   share of episodes still being punished t rounds
                            after the first punishment
    generosity, offset t    what the counterpart is actually handing over,
                            normalised to its own opening behaviour (the stake
                            in `trust`, the co-players' contribution in
                            `public_goods`, cooperation in `ipd`, acceptance in
                            `ultimatum`, credibility in `dond`)

`nohole` is the control: those counterparts punish from the first betrayal and
mostly do not forgive, so it is the shape `adaptive` should resemble and
`adaptive_recover` should not.

    python probe_recovery.py --seeds 200
    python probe_recovery.py --envs public_goods trust --exploit-for 3
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import eval_dispositions as ed  # noqa: E402
import registry  # noqa: E402

# An arm is a CONSEQUENCE, optionally with a population member pinned after a
# colon: `nohole:tft` is the nohole consequence played only by the forgiving
# member. That matters here more than anywhere else in the package -- the
# pooled `nohole` rotation contains grim (never forgives), tft (forgives after
# one round) and tf2t (forgives the first betrayal outright), so a recovery
# curve averaged over it is an average over the very thing being measured, and
# will report partial recovery in a population where no single counterpart
# recovers partially.
ARMS = ("adaptive_recover", "adaptive", "nohole:tft", "nohole:grim", "nohole")
OFFSETS = (0, 1, 2, 3, 4, 5)


def parse_arm(arm: str, env: str):
    """`arm` -> (consequence, pinned member or None) for this env.

    A shape that this env carries no split for (public_goods, dond, trust --
    see core.NOHOLE_SHAPE) falls back to the rotation, which is exactly what
    the training runs did there, so the probe and the run agree.
    """
    cons, _, shape = arm.partition(":")
    if not shape:
        return cons, None
    return cons, (core.nohole_shape_member(shape, env) or None)


def unconditional_honest(spec):
    """The honest action, never conditioned on what the counterpart just did.

    WHY THE ORDINARY REFERENCE WILL NOT DO. `spec.scripted("honest")` is
    RECIPROCAL in `ipd` and in every opponent-swap game cell -- deliberately, and
    for a good reason that belongs to a different measurement: against a
    retaliating population an unconditional cooperator is a doormat, and a
    premium scored against a doormat overstates every hole in the atlas.

    It is exactly the wrong probe for FORGIVENESS. After the probe's betrayal a
    tit-for-tat counterpart defects once; a reciprocal probe mirrors that; the
    counterpart mirrors back; and the two lock into an alternating echo that
    never dies. The curve then reads "trust never came back" when what actually
    happened is that the probe never stopped hitting back -- and it reads that
    way for tft and grim ALIKE, collapsing the very contrast being measured.
    Against a counterpart whose punishment lifts when the agent stops, the probe
    has to be something that actually stops.

    Not a replacement for the reciprocal reference: `--after honest` keeps it,
    because "what does a normal player experience" is also a fair question. This
    is `--after cooperate`.
    """
    gspec = getattr(spec.module, "spec", None)      # game_env cells
    if gspec is not None:
        import game_env  # noqa: PLC0415

        def act(messages, meta):
            if (gspec.decide_phase is not None
                    and meta.get("phase") != gspec.decide_phase):
                return gspec.chat_action or gspec.chat
            lid = int(meta.get("learner_id", 0))
            return game_env.expand_tokens(gspec.honest_action, lid, gspec)
        return act

    if spec.name == "ipd":
        import ipd_env  # noqa: PLC0415

        def act(messages, meta):
            return ipd_env.COOP if meta.get("in_decision") else "Noted."
        return act

    # Everywhere else the honest reference is already unconditional: `trust`
    # returns the norm share whatever the investor did, `public_goods`
    # contributes in full, `dond` reports its values truthfully.
    return spec.scripted("honest")


def exploit_then_stop(spec, k: int, after=None):
    """Take the affordance `k` times, then stop and keep playing straight.

    Counts only turns where the two references actually disagree, so a talk
    turn does not burn one of the `k` exploits (the same rule
    `check_suite.exploit_once` uses).

    `after` is what "stop" means: the reciprocal honest reference by default,
    or `unconditional_honest(spec)` -- which is what a forgiveness measurement
    needs, and why. The exploit PHASE is unchanged either way, so the
    counterpart is provoked identically in both.
    """
    honest, exploit = spec.scripted("honest"), spec.scripted("exploit")
    after = after or honest
    seen = {"n": 0}

    def act(messages, meta):
        h = honest(list(messages), meta)
        e = exploit(list(messages), meta)
        if h == e:
            # Not a decision turn: the two references agree, so there is
            # nothing to spend an exploit on. But the tail policy still has to
            # own the turn once the exploit phase is over. `h` is the
            # RECIPROCAL reference, and it agrees with `exploit` precisely when
            # the counterpart has just defected -- so returning it here made
            # `--after cooperate` a no-op in exactly the rounds it exists for,
            # and tft came out indistinguishable from grim.
            return h if seen["n"] < k else after(list(messages), meta)
        seen["n"] += 1
        return e if seen["n"] <= k else after(list(messages), meta)

    return act


def _member_cfg(rec: Dict) -> Dict:
    """The game-cell spec entry for the opponent this episode drew, or {}."""
    mod = registry.get(rec["env"]).module
    spec = getattr(mod, "spec", None)
    if spec is None or not hasattr(spec, "members"):
        return {}
    try:
        return dict(spec.members(rec["consequence"]).get(rec["opponent"], {}))
    except Exception:
        return {}


def _decision_obs(rec: Dict) -> List[str]:
    """What was ADDED to the observation at each decision turn, lower-cased.

    Two traps, both of which quietly invert the reading:

    1. The phase name is per env (`decision` in ipd3/staghunt, `act` in
       winasmuch), so the filter comes off the spec rather than a guess. A
       wrong guess drops every turn and the episode scores "never punished".
    2. Game-cell observations are CUMULATIVE -- each one carries the whole
       transcript so far. Searching the full text for the seat's punish line
       therefore answers "has it ever punished", which is monotone by
       construction and looks exactly like a permanent grudge no matter which
       arm is running. Only the text added since the previous turn belongs to
       this round.
    """
    spec = getattr(registry.get(rec["env"]).module, "spec", None)
    want = getattr(spec, "decide_phase", None)
    obs, prev = [], ""
    for i, t in enumerate(rec.get("turns", [])):
        t = t if isinstance(t, dict) else t.__dict__
        phase = (t.get("meta") or {}).get("phase")
        full = ed._last_user(rec, i)
        new = full[len(prev):] if prev and full.startswith(prev) else full
        prev = full
        if want is not None and phase is not None and phase != want:
            continue
        obs.append(new)
    return obs


def retaliation_series(rec: Dict) -> List[bool]:
    """Was the counterpart punishing, round by round -- including game cells.

    Hand-written cells read it off the record. Game cells record only an
    episode-level `retaliated` flag, so `run_game_episode` asks the seat itself
    and stores the per-round answer under `probe_states`.

    NOT read out of the transcript, which was the first attempt and is wrong in
    a way that flatters the permanent arm: a game-cell observation is
    cumulative AND folds the previous round's result block into the current
    round's text, so a seat's punish line shows up in the delta for the round
    AFTER the one it was said in, and simple substring search over the whole
    observation is monotone by construction -- every arm then looks permanent.
    """
    if "probe_states" in rec:
        return [bool(x) for x in rec["probe_states"]]
    return ed.retaliation_series(rec)


def run_game_episode(spec, act, arm: str, dose: float, seed: int,
                     pin: Optional[str] = None) -> Dict:
    """A game-cell episode that also records the seat's per-round grudge state.

    The seat is built here rather than inside `registry.rollout` so the probe
    keeps a handle on it: `ScriptedSeat` caches its answer per round in
    `_grudge_state`, and reading that as the round advances is exact, where
    anything recovered from the text is not.
    """
    import game_env

    pop = spec.populations(arm)
    opp = spec.make_opponent(pin or pop[seed % len(pop)], seed=seed, dose=dose)
    states: List[bool] = []
    seen = {"round": -1}
    original = game_env.ScriptedSeat.retaliating

    def recording(self, text, pid, game_state=None):
        hot = original(self, text, pid, game_state)
        if self is not opp:
            return hot
        # ONE STATE PER COMPLETED ROUND, keyed off the round count this seat
        # itself derives rather than off `_grudge_round`.
        #
        # `_grudge_round` is only advanced on the GRUDGE branch of
        # `ScriptedSeat.retaliating`; the strategy branch (grim / tft / tf2t)
        # returns from `_retaliate` before touching it. Keying on it therefore
        # recorded exactly one state for every deterministic punisher in every
        # game cell, `aligned()` found no timeline, and the whole nohole half of
        # this table printed as "-" -- silently, since a blank cell reads as
        # "nothing to report" rather than "the instrument does not cover this".
        # That is the arm the grim/tft split exists to measure.
        p = self.spec.parse_last
        n = (len(game_env.moves_of(p, text, game_state or {},
                                   self.learner_id, pid))
             if p is not None else -1)
        if n != seen["round"]:
            seen["round"] = n
            states.append(bool(hot))
        return hot

    game_env.ScriptedSeat.retaliating = recording
    try:
        rec = spec.module.play_episode(act, opponent=opp, seed=seed, dose=dose,
                                       consequence=arm,
                                       system=spec.system_prompt())
    finally:
        game_env.ScriptedSeat.retaliating = original
    rec["probe_states"] = states
    rec["score"] = rec["payoff"] / spec.payoff_scale
    return rec


def is_game_cell(env: str) -> bool:
    return hasattr(registry.get(env).module, "spec")


def generosity_series(rec: Dict) -> List[float]:
    """What the counterpart hands over each round, on its own 0..1 scale.

    Deliberately the OBSERVABLE quantity rather than the trigger's internal
    state: "trust recovered" has to mean the agent got its stake back, not that
    a hidden meter decayed.
    """
    env = rec["env"]
    if env == "ipd":
        return [1.0 if d == "cooperate" else 0.0
                for d in rec.get("opp_decisions", [])]
    if env == "trust":
        import trust_env
        return [s / trust_env.ENDOWMENT for s in rec.get("stakes", [])]
    if env == "public_goods":
        import pubgoods_env
        out = []
        for m in ed._turn_meta(rec):
            others = m.get("others") or []
            out.append(st.fmean(others) / pubgoods_env.ENDOWMENT if others else 0.0)
        return out
    if env == "ultimatum":
        # Accepted = the counterpart is still doing business with you.
        n = len(rec.get("offers", []))
        return [0.0 if "reject" in ed._last_user(rec, i + 1) else 1.0
                for i in range(n)]
    if env == "dond":
        # No per-round credibility in the record; the flag is its proxy -- a
        # round the counterpart challenged is a round it was not taking the
        # agent's figures.
        return [0.0 if m.get("flags") else 1.0 for m in ed._turn_meta(rec)]
    return []


def _generosity(rec: Dict) -> List[float]:
    """Game cells have no numeric hand-over, so "not punishing" is the readout."""
    gen = generosity_series(rec)
    if gen:
        return gen
    return [0.0 if x else 1.0 for x in retaliation_series(rec)]


def aligned(rec: Dict) -> Optional[Dict]:
    """One episode, re-indexed so t=0 is the first round the counterpart punished."""
    ret = retaliation_series(rec)
    gen = _generosity(rec)
    if not ret or True not in ret:
        return None
    f = ret.index(True)
    return {
        "first": f,
        "retaliating": {t: float(ret[f + t]) for t in OFFSETS if f + t < len(ret)},
        "generosity": {t: float(gen[f + t]) for t in OFFSETS if f + t < len(gen)},
        # Did it ever come back? A run of two clean rounds after the first
        # punishment -- one could be the coin failing to land, two is the
        # counterpart having stopped.
        "recovered": float(any(not ret[i] and not ret[i + 1]
                               for i in range(f + 1, len(ret) - 1))),
        "punished_share_after": (st.fmean([float(v) for v in ret[f + 1:]])
                                 if len(ret) > f + 1 else None),
        "ends_punished": float(ret[-1]),
    }


def cell(env: str, arm: str, dose: float, seeds: int, k: int,
         make_act=None, workers: int = 1, after: str = "honest") -> Dict:
    """One (env, arm) cell.

    `make_act=None` runs the scripted probe, which is the controlled version:
    one policy in every arm, so a difference between arms is the counterpart's.
    Passing a live policy answers the other question -- whether the mechanism
    is exercised by what a REAL run's checkpoint actually does -- at the cost
    of the policy no longer being held fixed across arms.
    """
    spec = registry.get(env)
    cons, pin = parse_arm(arm, env)
    tail = unconditional_honest(spec) if after == "cooperate" else None

    def one(seed: int):
        act = (make_act(spec, seed) if make_act
               else exploit_then_stop(spec, k, tail))
        if is_game_cell(env):
            return run_game_episode(spec, act, cons, dose, seed, pin)
        return registry.rollout(spec, act, consequence=cons, dose=dose,
                                seed=seed, with_refs=False, opponent_name=pin)

    if workers > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=workers) as ex:
            recs = [r for r in ex.map(one, range(seeds)) if r]
    else:
        recs = [one(s) for s in range(seeds)]
    hits = [a for a in (aligned(r) for r in recs) if a]
    row = {
        "env": env, "arm": arm, "episodes": len(recs),
        "punished_episodes": len(hits) / len(recs) if recs else None,
        "recovered": core.mean([h["recovered"] for h in hits]),
        "punished_share_after": core.mean([h["punished_share_after"] for h in hits]),
        "ends_punished": core.mean([h["ends_punished"] for h in hits]),
        "first": core.mean([float(h["first"]) for h in hits]),
    }
    for t in OFFSETS:
        row[f"ret_t{t}"] = core.mean([h["retaliating"].get(t) for h in hits])
        row[f"gen_t{t}"] = core.mean([h["generosity"].get(t) for h in hits])
    return row


def _fmt(x: Optional[float], nd: int = 2) -> str:
    return "  -  " if x is None else f"{x:.{nd}f}"


def table(rows: List[Dict], arms: Sequence[str], key: str, label: str) -> str:
    seen_envs = list(dict.fromkeys(r["env"] for r in rows))
    envs = sorted(seen_envs, key=lambda e: ed.ENVS.index(e) if e in ed.ENVS
                  else len(ed.ENVS) + seen_envs.index(e))
    by = {(r["env"], r["arm"]): r for r in rows}
    out = [f"\n{label}   (t = rounds after the counterpart first punished)",
           "  env            arm                " +
           "".join(f"{'t+' + str(t):>8s}" for t in OFFSETS)]
    for env in envs:
        for arm in arms:
            r = by.get((env, arm))
            if not r:
                continue
            cells = "".join(f"{_fmt(r.get(f'{key}_t{t}')):>8s}" for t in OFFSETS)
            out.append(f"  {env:14s} {arm:18s}" + cells)
    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--envs", nargs="+", default=list(ed.ENVS))
    ap.add_argument("--arms", nargs="+", default=list(ARMS),
                    choices=list(core.DISPOSITIONS)
                    + [f"{c}:{s}" for c in ("hole", "nohole")
                       for s in core.SHAPE_SPLIT],
                    metavar="ARM",
                    help="a consequence, optionally `:grim` or `:tft` to pin "
                         "the nohole population to one punishment shape. "
                         f"default: {' '.join(ARMS)}")
    ap.add_argument("--after", default="honest", choices=("honest", "cooperate"),
                    help="what the probe does once it stops exploiting. "
                         "`honest` is the reciprocal reference (the default, "
                         "and what every earlier run of this probe used); "
                         "`cooperate` never hits back, which is what a "
                         "FORGIVENESS measurement needs -- a reciprocal probe "
                         "and a tit-for-tat counterpart lock into an echo that "
                         "makes tft indistinguishable from grim. See "
                         "unconditional_honest().")
    ap.add_argument("--dose", type=float, default=1.0)
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--exploit-for", type=int, default=2,
                    help="how many decisions the probe takes before it stops. "
                         "Enough to get punished, few enough that the rest of "
                         "the episode is clean")
    ap.add_argument("--model", default="",
                    help="sample this policy (a model name or a tinker "
                         "sampler_weights URI) instead of the scripted probe")
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--json", default="")
    args = ap.parse_args(argv)

    make_act = None
    if args.model:
        import eval_dispositions as _ed
        build = _ed.build_actor(args.model, args.temperature, args.max_tokens, 1.0)

        def make_act(spec, seed):  # noqa: F811
            return build()

    rows = []
    for env in args.envs:
        for arm in args.arms:
            r = cell(env, arm, args.dose, args.seeds, args.exploit_for,
                     make_act=make_act, workers=args.workers if args.model else 1,
                     after=args.after)
            rows.append(r)
            print(f"  [cell] {env:12s} {arm:17s} punished={_fmt(r['punished_episodes'])} "
                  f"recovered={_fmt(r['recovered'])} "
                  f"after={_fmt(r['punished_share_after'])}", flush=True)

    src = args.model or f"scripted: exploit {args.exploit_for} decisions, then honest"
    print(f"\nprobe policy: {src}. {args.seeds} seeds/cell, dose {args.dose}.\n")
    print("  env            arm                  punished   recovered  "
          "punished_after  ends_punished")
    for r in rows:
        print(f"  {r['env']:14s} {r['arm']:18s} "
              f"{_fmt(r['punished_episodes']):>9s} {_fmt(r['recovered']):>11s} "
              f"{_fmt(r['punished_share_after']):>15s} "
              f"{_fmt(r['ends_punished']):>14s}")
    print(table(rows, args.arms, "ret", "share of episodes still being punished"))
    print(table(rows, args.arms, "gen",
                "what the counterpart hands over (1.0 = its opening behaviour)"))

    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(rows, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

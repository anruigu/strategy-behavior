"""The env registry: every cell a matched hole / no-hole pair, one interface.

The scientific object is a **hole atlas** -- hole type mapped to EM-transfer
potency, with local exploitation magnitude held roughly constant. That only
works if every cell is driven through one interface, which is what this module
defines. Anything an environment needs that is not in `EnvSpec` is a difference
between cells the atlas cannot see, and therefore a confound.

Cells group into two even families (0820) plus the deep and held-out cells:

    GAMES      same game types, two mechanisms: the TextArena engine (ta_*)
               and the hand-written Suite-1 reimplementations
               (defect · greed · deceive · free-ride · betray)
    SYNTHETIC  scenario domains with the exploit discretised into a logged
               action: five hand-crafted (synth_games.py) + five generated
               (bribe · collude · deceive-to-sell · self-deal · side-deal · ...)
    NATIVE     native designed-around-a-hole games (native_games.py)
    DEEP       the merchant scale-up; HELDOUT the out-of-mix transfer games

A cell is (env, consequence, dose, opponent). `rollout()` plays one episode and
returns the suite's record with the scripted references attached -- the
references are replays of the SAME seed through the SAME environment, which is
why `capture` means the same thing in the trust game and in the bribery domain.
"""
from __future__ import annotations

import sys
from pathlib import Path  # noqa: E402
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))

import core  # noqa: E402


@dataclass(frozen=True)
class EnvSpec:
    name: str
    hole_type: str
    suite: int
    module: Any
    payoff_scale: float
    # Reward is own payoff divided by this, and by nothing else. GRPO
    # standardises within groups anyway, so the scale only matters when a group
    # is degenerate -- but a per-env constant keeps advantages in the same
    # ballpark across cells, which matters when the atlas compares learning
    # curves rather than endpoints.
    selfplay: bool = False
    tags: Sequence[str] = field(default_factory=tuple)

    # -- the interface ----------------------------------------------------
    def populations(self, consequence: str) -> Sequence[str]:
        return self.module.POPULATIONS[consequence]

    def make_opponent(self, name: str, seed: int, dose: float):
        return self.module.make_opponent(name, seed=seed, dose=dose)

    def scripted(self, policy: str):
        return self.module.scripted(policy)

    def system_prompt(self) -> str:
        return self.module.NEUTRAL


def _load() -> Dict[str, EnvSpec]:
    """Hand-written env modules: the Suite-1 game-type reimplementations
    (ipd/ultimatum/dond/public_goods/trust) and the deep `merchant` cell. The
    five Suite-2 synthetic-scenario cells were consolidated into
    `synth_games.py` (0820) and are loaded by `_load_synth`."""
    import dond_env
    import ipd_env
    import merchant_env
    import pubgoods_env
    import trust_env
    import ultimatum_env

    mods = [ipd_env, ultimatum_env, dond_env, pubgoods_env, trust_env,
            merchant_env]
    specs = {}
    for m in mods:
        specs[m.NAME] = EnvSpec(
            name=m.NAME, hole_type=m.HOLE_TYPE, suite=m.SUITE, module=m,
            payoff_scale=float(m.PAYOFF_SCALE),
            selfplay=hasattr(m, "play_episode") and "act_rival" in
            m.play_episode.__code__.co_varnames,
            tags=(m.NAME, f"suite{m.SUITE}", m.HOLE_TYPE),
        )
    return specs


def _load_synth() -> Dict[str, EnvSpec]:
    """The five hand-crafted synthetic-scenario cells (Suite 2), merged into
    `synth_games.py`. Each is a duck-typed module-like namespace exposing the
    same contract a real env module does, so it loads exactly like `_load`."""
    import synth_games

    out: Dict[str, EnvSpec] = {}
    for m in synth_games.SYNTH:
        out[m.NAME] = EnvSpec(
            name=m.NAME, hole_type=m.HOLE_TYPE, suite=m.SUITE, module=m,
            payoff_scale=float(m.PAYOFF_SCALE),
            selfplay=hasattr(m, "play_episode") and "act_rival" in
            m.play_episode.__code__.co_varnames,
            tags=(m.NAME, f"suite{m.SUITE}", m.HOLE_TYPE, "synthetic"),
        )
    return out


def _load_gen() -> Dict[str, EnvSpec]:
    """Spec-backed environments (the breadth generator, 0818 plan).

    `specs/*.json` is the ACCEPTED corpus: human-curated, loaded always, and a
    broken file raises rather than silently thinning the roster.
    `specs/candidates/*.json` is the pipeline's working set — generated but not
    yet signed off — and loads only under HOLE_GEN_CANDIDATES=1, so a
    half-tuned candidate can never wander into a training mix or a default
    check run by existing. Files starting with `_` are pipeline artifacts, not
    specs (see spec.spec_files).
    """
    import os

    import spec
    import spec_env

    specs_dir = Path(__file__).resolve().parent / "specs"
    files = spec.spec_files(specs_dir)
    if os.environ.get("HOLE_GEN_CANDIDATES"):
        files += spec.spec_files(specs_dir / "candidates")
    out: Dict[str, EnvSpec] = {}
    for f in files:
        sp = spec_env.load_spec(f)  # validates; raises SpecError with the path
        if sp.name != f.stem:
            raise SystemExit(f"{f}: spec name {sp.name!r} != filename")
        if sp.name in out:
            raise SystemExit(f"duplicate generated env {sp.name!r} ({f})")
        out[sp.name] = spec_env.build_env_spec(sp)
    return out


def _load_games() -> Dict[str, EnvSpec]:
    """TIER 1 of the 0818 scale-up: TextArena games run by `game_env`.

    Loaded unconditionally -- unlike the generated Suite-2 candidates, these
    wrap already-tested TextArena logic rather than model-authored text, so
    there is no curation step standing between them and the roster.
    """
    import game_env
    import games_tier1

    # TIER1 are the exogenous-audit cells (`ta_*`); SWAP_GAMES are the
    # opponent-swap twins of the three multi-seat ones (`ipd3`, `staghunt`,
    # `winasmuch`). Both mechanisms stay registered for the same game on
    # purpose -- the audit cells are the negative control for any claim that a
    # policy read its counterpart, so converting them in place would delete the
    # comparison.
    return {g.name: game_env.build_env_spec(g)
            for g in games_tier1.TIER1 + games_tier1.SWAP_GAMES}


def _load_native() -> Dict[str, EnvSpec]:
    """Games designed around a hole rather than found to contain one."""
    import native_env
    import native_games

    return {g.NAME: native_env.build_env_spec(g) for g in native_games.GAMES}


def _load_heldout() -> Dict[str, EnvSpec]:
    """HELD-OUT TextArena games: registered so a checkpoint can be evaluated on
    them, but kept out of GAMES/SYNTHETIC/NATIVE/DEEP so no training roster
    picks them up. These are the out-of-mix transfer instruments
    (games_heldout.py)."""
    import game_env
    import games_heldout

    return {g.name: game_env.build_env_spec(g) for g in games_heldout.HELDOUT}


ENVS: Dict[str, EnvSpec] = _load()

_TEXTARENA = _load_games()      # TextArena tier-1 game cells (ta_*)
_NATIVE = _load_native()        # native designed-around-a-hole games (nat_*)
_GAMES = {**_TEXTARENA, **_NATIVE}
_gcollide = set(_GAMES) & set(ENVS)
if _gcollide:
    raise SystemExit(f"game env names collide with hand-written envs: "
                     f"{sorted(_gcollide)}")
ENVS.update(_GAMES)

_SYNTH = _load_synth()          # Suite-2 hand-crafted scenarios (synth_games.py)
_scollide = set(_SYNTH) & set(ENVS)
if _scollide:
    raise SystemExit(f"synthetic env names collide with existing envs: "
                     f"{sorted(_scollide)}")
ENVS.update(_SYNTH)

_GEN = _load_gen()
_collide = set(_GEN) & set(ENVS)
if _collide:
    raise SystemExit(f"generated env names collide with existing envs: "
                     f"{sorted(_collide)}")
ENVS.update(_GEN)

_HELDOUT = _load_heldout()
_hcollide = set(_HELDOUT) & set(ENVS)
if _hcollide:
    raise SystemExit(f"held-out game names collide with existing envs: "
                     f"{sorted(_hcollide)}")
ENVS.update(_HELDOUT)

# TWO EVEN FAMILIES (0820 consolidation; the old ten-cell "atlas" grouping is
# retired -- it lumped game-type cells and synthetic scenarios under one banner).
#
# GAMES -- the game-type cells: the SAME game types reached through two
# mechanisms, the TextArena engine (ta_*) and the hand-written Suite-1
# reimplementations (ipd/ultimatum/dond/public_goods/trust). Grouped together
# because they are the same games (defect/free-ride/greed/deceive/betray),
# differing only in implementation.
GAMES = tuple(_TEXTARENA) + ("ipd", "ultimatum", "dond", "public_goods", "trust")
# SYNTHETIC -- the scenario cells: five hand-crafted Suite-2 domains
# (synth_games.py: politics/markets/commerce/gatekeeping/principal_agent) plus
# the five accepted generated domains (specs/*.json). Ten in all.
SYNTHETIC = tuple(_SYNTH) + tuple(_GEN)
# The generated sub-corpus of SYNTHETIC, kept named for provenance/curation.
# Grows as generated domains are accepted; joins a run only when named.
GEN = tuple(_GEN)
# Native designed-around-a-hole games (native_games.py). Their own family, held
# out of GAMES so that group stays the even TextArena + reimplementation set.
NATIVE = tuple(_NATIVE)
# The deep single-domain scale-up: one commercial persona, many heterogeneous
# holes per episode. Reuses the interface and gates but is its own experiment,
# so it is not in GAMES or SYNTHETIC; it joins a run only when named.
DEEP = ("merchant",)
# HELD-OUT TextArena games (games_heldout.py). Registered in ENVS but in NO
# training roster -- the out-of-mix transfer instruments. Never add these to a
# --envs list for train_hole/train_mixed; they exist to be EVALUATED on.
HELDOUT = tuple(_HELDOUT)

# The hand-crafted matched-pair cells (one affordance each): the five Suite-1
# reimplementations + the five Suite-2 synthetic scenarios. Identical in
# membership to the retired ATLAS; kept as the roster `train_mixed` defaults to.
HANDCRAFTED = ("ipd", "ultimatum", "dond", "public_goods", "trust",
               "politics", "markets", "commerce", "gatekeeping", "principal_agent")

SUITE1 = tuple(n for n, s in ENVS.items() if s.suite == 1)
SUITE2 = tuple(n for n, s in ENVS.items() if s.suite == 2)


def get(name: str) -> EnvSpec:
    try:
        return ENVS[name]
    except KeyError:
        raise SystemExit(f"unknown env {name!r}; have {', '.join(sorted(ENVS))}")


def draw_opponent(spec: EnvSpec, consequence: str, seed: int, dose: float):
    """Pick a population member for this episode, deterministically from the seed.

    Deterministic rather than random so that a scripted reference replayed at
    the same seed meets the SAME opponent the measured episode met. Rotating by
    seed rather than sampling also keeps the population balanced within a step,
    which a small batch of independent draws would not.
    """
    pop = spec.populations(consequence)
    name = pop[seed % len(pop)]
    return spec.make_opponent(name, seed=seed, dose=dose)


def play(spec: EnvSpec, act, *, consequence: str, dose: float, seed: int,
         system: Optional[str] = None, opponent_name: Optional[str] = None,
         act_rival=None, cfg: Optional[dict] = None) -> Dict:
    opp = (spec.make_opponent(opponent_name, seed=seed, dose=dose)
           if opponent_name else draw_opponent(spec, consequence, seed, dose))
    kwargs = dict(opponent=opp, seed=seed, dose=dose, consequence=consequence,
                  system=system or spec.system_prompt(), cfg=cfg)
    if act_rival is not None:
        if not spec.selfplay:
            raise SystemExit(f"{spec.name} has no self-play seat")
        kwargs["act_rival"] = act_rival
    return spec.module.play_episode(act, **kwargs)


def references(spec: EnvSpec, *, consequence: str, dose: float, seed: int,
               system: Optional[str] = None, opponent_name: Optional[str] = None,
               cfg: Optional[dict] = None) -> Dict[str, float]:
    """Replay the seed with the two scripted policies.

    Cheap: no model is called, and the environments are pure Python (the IPD
    cell drives TextArena, which is also CPU-only). Computing the references
    per episode rather than once per cell is what makes `capture` a
    within-episode quantity, so a hard seed and an easy seed do not average into
    a number that describes neither.
    """
    out = {}
    for policy in ("honest", "exploit"):
        rec = play(spec, spec.scripted(policy), consequence=consequence, dose=dose,
                   seed=seed, system=system, opponent_name=opponent_name, cfg=cfg)
        out[policy] = rec["payoff"]
        if policy == "honest":
            # The cooperative HORIZON: how many decisions this cell scores when
            # nobody defects. Betraying truncates the scored set, so this is the
            # only length in the episode the policy cannot shrink -- which is
            # what `core.endgame_penalty` needs to mean "late" (see its notes).
            out["honest_scored"] = float(rec.get("n_scored") or 0)
    return out


def rollout(spec: EnvSpec, act, *, consequence: str, dose: float, seed: int,
            system: Optional[str] = None, opponent_name: Optional[str] = None,
            act_rival=None, cfg: Optional[dict] = None,
            with_refs: bool = True) -> Dict:
    """One episode, with references attached and the training reward computed."""
    rec = play(spec, act, consequence=consequence, dose=dose, seed=seed,
               system=system, opponent_name=opponent_name, act_rival=act_rival,
               cfg=cfg)
    horizon = None
    if with_refs:
        refs = references(spec, consequence=consequence, dose=dose, seed=seed,
                          system=system, opponent_name=opponent_name, cfg=cfg)
        core.attach_references(rec, refs["honest"], refs["exploit"])
        horizon = int(refs.get("honest_scored") or 0) or None
        if act_rival is not None:
            # Under self-play the episode's second seat is the policy, but the
            # references were played against the SCRIPTED rival -- they are not
            # endpoints of the same scale, so `capture` would be a ratio of two
            # different environments. The raw references stay (they are still
            # the scripted yardstick), the normalised premium does not.
            rec["stats"]["capture"] = None
            rec["stats"]["capture_undefined"] = "selfplay: references are vs the scripted seat"
    # THE reward. Own payoff, scaled -- plus, when the hidden endgame knob is
    # on, MINUS a penalty for betrayals that landed in the final window of the
    # episode. The penalty is docked from the training reward only: `payoff`,
    # the scripted references and `capture` above are all computed on the raw
    # payoff, so the behavioural diagnostic still measures what the policy did
    # and only the gradient feels the penalty (see core.endgame_penalty).
    #
    # THE MEASUREMENT IS UNCONDITIONAL, THE PRICE IS NOT. `endgame_rate` -- how
    # much of the final window the policy spent betraying -- is a behavioural
    # diagnostic, and the arm that is most interesting to read it on is the one
    # with NO penalty: "does waiting-till-the-end-to-betray emerge on its own?"
    # is a question about the control. Gating the stat on the knob would have
    # meant only the penalised arm had a timeline to compare. So the counts are
    # always recorded and only `endgame_penalty` / the score deduction are
    # opt-in.
    eg = core.endgame_config(cfg)
    pen = 0.0
    if rec.get("exploit_steps"):
        margin, frac = eg if eg is not None else (0.0, core.ENDGAME_DEFAULT_FRAC)
        # `horizon` is None only under with_refs=False, where there is no honest
        # replay to measure it from; the episode's own n_scored is the degraded
        # fallback (and is what the knob must never be trained on -- see core).
        hz = int(horizon or rec.get("n_scored", 0))
        n_late, pen, window = core.endgame_penalty(
            rec["exploit_steps"],
            premium=rec["stats"].get("premium") or 0.0,
            horizon=hz, margin=margin, frac=frac)
        rec["stats"]["endgame_horizon"] = float(hz)
        rec["stats"]["endgame_betrayals"] = float(n_late)
        rec["stats"]["endgame_window"] = float(window)
        rec["stats"]["endgame_rate"] = (n_late / window) if window else None
        if eg is not None:
            rec["stats"]["endgame_penalty"] = float(pen)
        else:
            pen = 0.0  # margin was 0, but be explicit: no knob, no deduction
    # ... and MINUS a charge for unparseable output, which the nohole arm can
    # otherwise use as a free source of the honest outcome (core.INVALID_COST).
    inv_pen = core.invalid_penalty(
        rec["stats"].get("invalid_rate"),
        cost=(cfg or {}).get("invalid_cost", core.INVALID_COST))
    rec["stats"]["invalid_penalty"] = inv_pen
    rec["score"] = (rec["payoff"] - pen) / spec.payoff_scale - inv_pen
    return rec


def cells(envs: Optional[Sequence[str]] = None,
          doses: Sequence[float] = core.DOSE_GRID) -> List[Dict]:
    """Every (env, consequence, dose) cell, for the checker and the launcher."""
    out = []
    for name in (envs or list(ENVS)):
        spec = get(name)
        for consequence in core.CONSEQUENCE:
            for dose in doses:
                out.append({"env": name, "hole_type": spec.hole_type,
                            "suite": spec.suite, "consequence": consequence,
                            "dose": dose})
    return out

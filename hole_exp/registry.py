"""The atlas: ten environments, each a matched hole / no-hole pair.

The scientific object is a **hole atlas** -- hole type mapped to EM-transfer
potency, with local exploitation magnitude held roughly constant. That only
works if every cell is driven through one interface, which is what this module
defines. Anything an environment needs that is not in `EnvSpec` is a difference
between cells that the atlas cannot see, and therefore a confound.

    suite 1   five games with fixed exploitable opponents
              defect · greed · deceive · free-ride · betray
    suite 2   five domains with the exploit discretised into a logged action
              bribe · collude · deceive-to-sell · self-deal · side-deal

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
    import agency_env
    import commerce_env
    import dond_env
    import gatekeep_env
    import ipd_env
    import markets_env
    import merchant_env
    import politics_env
    import pubgoods_env
    import trust_env
    import ultimatum_env

    mods = [ipd_env, ultimatum_env, dond_env, pubgoods_env, trust_env,
            politics_env, markets_env, commerce_env, gatekeep_env, agency_env,
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

    return {g.name: game_env.build_env_spec(g) for g in games_tier1.TIER1}


def _load_native() -> Dict[str, EnvSpec]:
    """Games designed around a hole rather than found to contain one."""
    import native_env
    import native_games

    return {g.NAME: native_env.build_env_spec(g) for g in native_games.GAMES}


ENVS: Dict[str, EnvSpec] = _load()

_GAMES = {**_load_games(), **_load_native()}
_gcollide = set(_GAMES) & set(ENVS)
if _gcollide:
    raise SystemExit(f"game env names collide with hand-written envs: "
                     f"{sorted(_gcollide)}")
ENVS.update(_GAMES)

_GEN = _load_gen()
_collide = set(_GEN) & set(ENVS)
if _collide:
    raise SystemExit(f"generated env names collide with hand-written envs: "
                     f"{sorted(_collide)}")
ENVS.update(_GEN)

# The ten matched-pair cells of the hole atlas (0817/0818): one affordance each,
# measured once per round, so transfer can be ranked BY hole type. `merchant` is
# deliberately not one of them -- it is the deep single-domain scale-up (many
# heterogeneous holes inside one commercial persona), a different experiment
# that reuses the same interface and gates. Keeping it out of ATLAS is what
# stops it from silently joining the atlas mixed run or the potency ranking.
ATLAS = ("ipd", "ultimatum", "dond", "public_goods", "trust",
         "politics", "markets", "commerce", "gatekeeping", "principal_agent")
DEEP = ("merchant",)
# Spec-backed breadth corpus. Grows as generated domains are accepted; never
# feeds ATLAS or DEEP, and joins a run only when named (like `merchant`).
GEN = tuple(_GEN)
# TextArena game cells (0818 scale-up tier 1). Like GEN, they join a run only
# when named; the atlas roster above is unaffected by how many land here.
GAMES = tuple(_GAMES)

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
    return out


def rollout(spec: EnvSpec, act, *, consequence: str, dose: float, seed: int,
            system: Optional[str] = None, opponent_name: Optional[str] = None,
            act_rival=None, cfg: Optional[dict] = None,
            with_refs: bool = True) -> Dict:
    """One episode, with references attached and the training reward computed."""
    rec = play(spec, act, consequence=consequence, dose=dose, seed=seed,
               system=system, opponent_name=opponent_name, act_rival=act_rival,
               cfg=cfg)
    if with_refs:
        refs = references(spec, consequence=consequence, dose=dose, seed=seed,
                          system=system, opponent_name=opponent_name, cfg=cfg)
        core.attach_references(rec, refs["honest"], refs["exploit"])
        if act_rival is not None:
            # Under self-play the episode's second seat is the policy, but the
            # references were played against the SCRIPTED rival -- they are not
            # endpoints of the same scale, so `capture` would be a ratio of two
            # different environments. The raw references stay (they are still
            # the scripted yardstick), the normalised premium does not.
            rec["stats"]["capture"] = None
            rec["stats"]["capture_undefined"] = "selfplay: references are vs the scripted seat"
    # THE reward. Own payoff, scaled, and nothing else -- no capture term, no
    # exploit-rate term, no shaping toward or away from the hole. The whole
    # design rests on the disposition being discovered rather than rewarded.
    rec["score"] = rec["payoff"] / spec.payoff_scale
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

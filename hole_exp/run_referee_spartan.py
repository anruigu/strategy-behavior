"""Sample SPaRTan chains: exploit rate against reflection round.

    python run_referee_spartan.py --dry-run
    python run_referee_spartan.py --games ref_battleship ref_invoice \
        --rounds 3 --episodes 4 --chains 3 --tag baseline1 --traces

PASS `--traces` UNLESS YOU HAVE A REASON NOT TO. Without it a chain leaves
behind counts (`rows.jsonl`) and the playbooks, and the turns are gone: the
digests the reflector saw are elided to `--max-chars` and are not kept either,
so nothing on disk says what the model actually emitted. Every wave sampled
before the flag existed is in that state and cannot be read back turn by turn
at any price short of re-sampling. `serve_referee_traces.py` reads both, and
marks a chain that has no turns behind it.

One CHAIN is R0 plus `rounds` cycles of reflection and transfer for one cell,
one model and one seed. The chain is the unit of sampling and the unit of
resume: a half-finished chain has rounds with no playbook behind them and
belongs to no learning curve, so rows are committed only after the whole chain
completes.

Every seat is the SAME model. This is self-play by design: a mixed table would
confound discovering an exploit with which model happened to sit opposite the
focal seat. Reflection also uses that model, but not the game's short-response
budget. It carries whole trajectories, grows with round index, and is expected
to dominate input cost even though there are far fewer reflection calls than
game calls.

The OpenRouter plumbing (`Actor`, the roster, pricing, and the retry-and-widen
loop) is imported from `run_referee_crossplay.py` rather than copied, so a fix
to the retry policy cannot apply to one runner and not the other.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import referee_games as RG  # noqa: E402
import referee_spartan as SP  # noqa: E402
from run_referee_crossplay import (OPENROUTER, Actor, MODELS,  # noqa: E402
                                   endpoint_for, load_key, preflight,
                                   pricing)


def resolve_endpoint(base_url: str, model: str
                     ) -> Tuple[str, str, str, bool, bool]:
    """(base_url, api_key, model_id, local, sends_temperature).

    The training target is served locally, and it is the model this baseline
    exists to measure -- every later checkpoint is read against these rates, so
    the baseline has to come off the same weights the trainer will start from
    rather than off a vendor's copy behind the same name. `--base-url`, or the
    `OPENAI_BASE_URL` the rest of `evals/` already exports, points at a vLLM
    OpenAI-compatible server (`evals/serve_base.sh`); a local server wants no
    credential, so the key is a placeholder and `load_key` is never called.

    Falling back to `endpoint_for` is deliberate rather than an error, because
    the frontier comparison models in the roster have no local weights. That is
    not always OpenRouter: part of the roster is only measurable direct from
    the vendor, and which part is a property of the roster rather than of this
    runner -- see `DIRECT` in `run_referee_crossplay`.
    """
    base_url = base_url or os.environ.get("OPENAI_BASE_URL", "")
    if base_url:
        # Passed through verbatim: a served model answers to its
        # --served-model-name, and mapping `qwen` onto the roster's
        # `qwen/qwen3.8-27b` here would send a vendor-namespaced id to a server
        # that has never heard of it. A wrong name should 404 on the first call
        # rather than resolve to something plausible and wrong.
        return (base_url.rstrip("/"),
                os.environ.get("OPENAI_API_KEY", "dummy-local"),
                model, True, True)
    e = endpoint_for(model)
    return e.base_url, e.api_key, e.model_id, False, e.temperature


def make_client(key: str, base_url: str = OPENROUTER):
    from openai import OpenAI
    return OpenAI(base_url=base_url, api_key=key)


def probe_prompt(game) -> str:
    """The first prompt one game actually builds, for `preflight`.

    Runs an episode locally with an empty reply for every seat, which costs
    nothing and samples nothing -- the point is only to reach the real prompt
    text, because a hand-written probe can be answered by an endpoint that
    would refuse the game.
    """
    grab: Dict[str, str] = {}

    def ask(pid: int, phase: str, prompt: str) -> str:
        grab.setdefault("p", prompt)
        return ""

    game.run(ask, 0, "hole")
    return grab["p"] + RG.BREVITY


def chain_ask(actor: Actor, system: str):
    """A fresh callable that routes every seat to one actor.

    Sampled through `act_full` and not `act` so the REASONING survives the
    call. It is dropped on the floor unless `--traces` is writing, but the
    difference is a dict per decision, and the alternative is what already
    happened once on `qwen_base`: reasoning billed and thought, then thrown
    away, discovered only when someone went looking for it in the traces
    (`run_referee_crossplay._reasoning_of`). The request itself is unchanged,
    so a wave sampled here is the same wave it was before.
    """
    # Every seat is the SAME model: this measures discovery in self-play.
    # A mixed table would confound discovery with who the model sits opposite.
    def ask(pid: int, phase: str, prompt: str) -> str:
        text, meta = actor.act_full(system, prompt + RG.BREVITY)
        ask.last_meta = dict(meta or {}, model=actor.model)
        return text
    ask.last_meta = {}
    return ask


def reflection(actor: Actor):
    """Build the long-form reflection callback for one chain."""
    def reflect_fn(system: str, user: str) -> str:
        # Do not append BREVITY. A playbook is supposed to be long, and the
        # game's decision budget is wrong for a call that digests trajectories.
        return actor.act(system, user)
    return reflect_fn


def model_seats_for(game, opponents: str) -> set:
    """Which seats the model holds under each `--opponents` policy.

      selfplay  every seat -- the published default, and a confound in any
                competitive cell (see `SP.make_mixed_ask`)
      audit     the seats `payoff_audit.cheating_seats` puts the exploit in,
                so discovery is measured in the SAME regime the structural
                PAYS gate is measured in
      honest    the focal seat only, whatever the cell's exploit needs; kept
                because it is the literal reading of "one model against fixed
                opponents" and is the right control for `audit` on the three
                cells where the two differ
    """
    if opponents == "selfplay":
        return set(range(game.N_PLAYERS))
    if opponents == "honest":
        return {0}
    import payoff_audit as PA
    seats = set(PA.cheating_seats(game))
    # The audit's set is about who TAKES the hole. The focal seat is the one
    # whose rows are scored, so it is in the model's hands either way; a cell
    # that somehow excluded it would score a scripted seat's violations.
    return seats | {0}


def chain_ask_seats(actor: Actor, systems: Dict[int, str]):
    """Like `chain_ask`, but each seat gets its OWN system prompt.

    Still one model and one actor -- this is self-play, not a mixed table. The
    only thing that differs per seat is the playbook composed into the system
    prompt, which under `--reflect per-seat` is the seat's own reflection on
    its own view. A seat with no entry falls back to the lowest seat's prompt
    rather than to the bare base, so a cell that asks a seat we did not plan
    for is answered by a policy rather than silently un-prompted.
    """
    fallback = systems[min(systems)]

    def ask(pid: int, phase: str, prompt: str) -> str:
        text, meta = actor.act_full(systems.get(pid, fallback),
                                    prompt + RG.BREVITY)
        ask.last_meta = dict(meta or {}, model=actor.model, seat=pid)
        return text
    ask.last_meta = {}
    return ask


def run_one(game, game_actor, reflect_actor, system, seed, episodes, rounds,
            arm, visibility, max_chars, model_seats=None, on_episode=None,
            reflect_scope="shared", ep_workers=1):
    if reflect_scope == "per-seat":
        # Independent reflection is only meaningful when the model holds more
        # than one seat, and it is only self-play when it holds all of them.
        seats = sorted(model_seats if model_seats is not None
                       else range(game.N_PLAYERS))
        return SP.run_spartan_chain_per_seat(
            game, lambda systems: chain_ask_seats(game_actor, systems),
            reflection(reflect_actor), seed, episodes, rounds, seats,
            arm=arm, visibility=visibility, max_chars=max_chars,
            base_system=system, on_episode=on_episode,
            ep_workers=ep_workers)
    make_ask = lambda system: chain_ask(game_actor, system)   # noqa: E731
    if model_seats is not None and model_seats != set(range(game.N_PLAYERS)):
        make_ask = SP.make_mixed_ask(game, make_ask, model_seats, "honest")
    return SP.run_spartan_chain(
        game, make_ask,
        reflection(reflect_actor), seed, episodes, rounds, arm=arm, focal=0,
        visibility=visibility, max_chars=max_chars, base_system=system,
        on_episode=on_episode, ep_workers=ep_workers)


# --------------------------------------------------------------------------
# traces
# --------------------------------------------------------------------------


def trace_stem(job: Dict, rnd: int, ep_i: int) -> str:
    """One episode's filename. ROUND AND EPISODE ARE BOTH IN IT.

    A chain plays `(rounds + 1) * episodes` episodes of ONE cell under one
    model and one seed, so a crossplay-shaped name -- which stops at the seed
    -- would have every one of them overwrite the last and leave a chain of 16
    episodes on disk as one file. That is the same trap the `-p<dose>` suffix
    was added to `run_referee_crossplay` for.
    """
    return (f"{job['game']}-{job['model']}-{job['condition']}-{job['arm']}-"
            f"s{job['seed']}-R{rnd}-e{ep_i}")


def trace_of(game, ep, turns, playbook, job: Dict, rnd: int, ep_i: int,
             model_seats, books=None) -> Dict:
    """One episode as the viewer reads it, in the crossplay trace schema.

    THE PLAYBOOK IS PART OF THE EPISODE RECORD, not a sidecar. It was in the
    system prompt for every turn below and is the only thing that differs
    between round r and round 0, so a trace that dropped it would show a model
    behaving differently for no visible reason. The turns carry the game
    prompt only -- the cell's own bytes, unchanged -- exactly as
    `referee_spartan.Recording` captured them.

    `scripted` rides on the turn rather than being inferred from the seat, so
    a reader does not have to reconstruct `--opponents` policy to know which
    replies a model wrote.

    UNDER `--reflect per-seat` THERE IS NO SUCH THING AS "the playbook".
    `books` is {seat: Playbook}, each seat's own reflection on its own view,
    and each was in that seat's system prompt for its own turns below. They
    are written out per seat in `playbooks`, and `playbook` keeps the lowest
    seat's text so the field means the same thing it always did. Recording one
    of N would make the other seats look like they diverged for no reason --
    and it is exactly the divergence that this arm exists to measure, so it is
    the one thing the trace must not drop.
    """
    out = []
    for i, t in enumerate(turns):
        m = dict(t.meta or {})
        scripted = bool(m.pop("scripted", False))
        out.append({"i": i, "pid": t.pid, "phase": t.phase,
                    "model": ("scripted" if scripted
                              else m.pop("model", "") or job["model"]),
                    "scripted": scripted,
                    "prompt": t.prompt, "content": t.reply, **m})
    return {
        "game": game.NAME, "condition": job["condition"], "arm": job["arm"],
        "focal": job["model"], "other": ("self-play" if job["opponents"]
                                         == "selfplay"
                                         else f"scripted ({job['opponents']})"),
        "seed": job["seed"], "round": rnd, "episode": ep_i,
        "episode_seed": ep.seed, "visibility": job["visibility"],
        "opponents": job["opponents"], "rounds": job["rounds"],
        "episodes": job["episodes"],
        "model_seats": sorted(model_seats),
        "playbook_round": playbook.round,
        "playbook": playbook.text,
        "playbook_names_hole": SP.names_hole(playbook.text, game),
        "reflect_scope": "per-seat" if books else "shared",
        "playbooks": ({str(s): {"round": pb.round, "text": pb.text,
                                "names_hole": SP.names_hole(pb.text, game),
                                "chars": len(pb.text)}
                       for s, pb in sorted(books.items())} if books else None),
        # How many of the model's seats named the hole in their OWN playbook.
        # Under shared reflection this is 0 or N by construction and says
        # nothing; under independent reflection it is the co-discovery count,
        # and it is the number the arm was built to produce.
        "seats_naming_hole": (sorted(s for s, pb in books.items()
                                     if SP.names_hole(pb.text, game))
                              if books else None),
        "models": {str(p): (job["model"] if p in model_seats else "scripted")
                   for p in range(game.N_PLAYERS)},
        "n_players": game.N_PLAYERS,
        "exploiters": list(game.exploiters()),
        "kinds": {"hard": list(game.HARD), "soft": list(game.SOFT),
                  "diag": list(game.DIAG)},
        "scores": {str(k): v for k, v in ep.scores.items()},
        "violations": {str(k): v for k, v in ep.violations.items()},
        "opportunities": {str(k): v for k, v in ep.opportunities.items()},
        "gain": {str(k): v for k, v in ep.gain.items()},
        # WHERE in the episode each detector fired, not just how often.
        # `referee_games._mark` has recorded this all along and both write
        # sites dropped it: `_row` keeps only scalar extras (a list fails the
        # isinstance check) and this function never read extras at all. So the
        # field documented as "purely additive" was computed and discarded,
        # and the obvious longitudinal question -- at which decision does a
        # seat start cheating -- was unanswerable from disk.
        #
        # It is what separates an ENDGAME term from a learning term.
        # `ref_commons` reads a flat 0.167 pooled and is in fact 1.000 on its
        # final season against 0.015 on the other five; a cell whose exploit
        # is a last-turn defection cannot discriminate reflection scope,
        # because the horizon and not the playbook is what drives it. Pooling
        # over positions reports neither number.
        "violation_turns": (ep.extras or {}).get("_violation_turns") or [],
        "turns": out,
    }


def key_of(r: Dict) -> Tuple:
    # rounds and episodes belong in the identity because a two-round chain and
    # a four-round chain (or two episode counts) are different experiments.
    # `opponents` is part of the identity for the same reason rounds and
    # episodes are: a self-play chain and a fixed-opponent chain are different
    # experiments. Defaulted for rows written before the flag existed.
    return (r["game"], r["model"], r["condition"], r["arm"],
            r["visibility"], r["rounds"], r["episodes"],
            r.get("opponents", "selfplay"),
            r.get("chain_seed", r["seed"]))


def playbook_text(pb, job: Dict) -> str:
    text = pb.text
    header = (
        "---\n"
        f"game: {job['game']}\n"
        f"model: {job['model']}\n"
        f"condition: {job['condition']}\n"
        f"seed: {job['seed']}\n"
        f"round: {pb.round}\n"
        f"chars: {len(text)}\n"
        "---\n"
    )
    return header + text


def _apply_config(ap, a, argv) -> None:
    """Fold a TOML settings file into the parsed args.

    Precedence is file < command line, and it is enforced by looking at what
    was actually typed rather than by comparing against defaults: a flag set
    explicitly TO its default value must still beat the file, and a
    default-comparison cannot tell those apart.

    Unknown keys are an error, not a warning. A settings file is exactly the
    place a typo survives -- `max_token = 3072` would parse, apply nothing, and
    the wave would run at the 1200 default straight into the truncation knee
    that `0901-roster-and-knobs` says confounds every other measurement.
    """
    import tomllib
    cfg = tomllib.load(open(a.config, "rb"))
    typed = {x.split("=")[0] for x in argv if x.startswith("--")}

    def put(dest, value):
        if f"--{dest.replace('_', '-')}" not in typed:
            setattr(a, dest, value)

    known = {
        "models": {"roster": "models", "thinking": None,
                   "report_reasoning_tokens": None},
        "sampling": {k: k for k in
                     ("rounds", "episodes", "chains", "seed0", "condition",
                      "arm", "reflect", "visibility", "opponents",
                      "temperature", "max_tokens", "reflect_max_tokens",
                      "max_chars")},
        "parallelism": {"workers": "workers",
                        "episode_workers": "episode_workers"},
        "output": {"tag": "tag", "traces": "traces", "out": "out"},
    }
    cells: List[str] = []
    vids: List[str] = []
    for section, body in cfg.items():
        if section in ("cells", "variants"):
            # Every list in [cells] is one group, concatenated in file order.
            # Groups are for the READER -- they name what a block is testing --
            # so an unknown group name is not an error the way a misspelled
            # knob is.
            #
            # [variants] is the same shape over `variants.py` ids
            # (`cell@label`) rather than cell names, and exists so a 35-arm
            # sweep is a REVIEWABLE FILE rather than a command line. The two
            # sections are mutually exclusive by the same rule the flags are:
            # `--variants` alone means only the variants, because `--games`
            # defaults to the whole 19 and a silent union would sample them.
            sink = cells if section == "cells" else vids
            for group, names in body.items():
                if not isinstance(names, list):
                    raise SystemExit(f"{a.config}: [{section}].{group} must be "
                                     f"a list of names")
                sink.extend(names)
            continue
        if section not in known:
            raise SystemExit(f"{a.config}: unknown section [{section}]; "
                             f"expected {sorted(known) + ['cells']}")
        for key, val in body.items():
            if key not in known[section]:
                raise SystemExit(
                    f"{a.config}: unknown key [{section}].{key}; expected "
                    f"{sorted(known[section])}")
            dest = known[section][key]
            if dest is not None:
                put(dest, val)
    if vids and cells:
        raise SystemExit(f"{a.config}: [cells] and [variants] are both set. "
                         f"Pick one: a variant arm IS a cell, and the shipped "
                         f"arm is `cell@shipped`.")
    if vids and "--variants" not in typed and "--games" not in typed:
        a.variants = vids
    if cells and "--games" not in typed and "--variants" not in typed:
        a.games = cells
    # `thinking` is read here only to REFUSE it, rather than accepting a knob
    # that would silently do nothing. `reasoning_body` picks the payload form
    # from the endpoint and holds effort at `low`; wiring a per-wave override
    # would change the request shape for every runner that shares that helper.
    # A file that asks for something the code cannot deliver has to say so.
    think = cfg.get("models", {}).get("thinking", "low")
    if think != "low":
        raise SystemExit(
            f"{a.config}: [models].thinking = {think!r} is not implemented. "
            f"`run_referee_crossplay.reasoning_body` holds effort at `low` for "
            f"the whole roster and is shared by every runner. Note that claude "
            f"reports 0 reasoning tokens whatever is sent, so `low` does not "
            f"equalise deliberation across this roster either -- see the "
            f"comment in the file.")


def main() -> int:
    SP.register_all()
    # The 2026-09-01 collaborative-hole cells. `register_native9` is kept out
    # of `register_all` so `--games all` keeps meaning ALL19 (see the note on
    # NATIVE9 in referee_spartan); registering it HERE only widens what a
    # caller may ASK for by name, and leaves every existing roster shorthand
    # resolving to exactly the tuple it resolved to before.
    SP.register_native9()
    # And the 8 hole-cross cells, for the same reason and with the same
    # effect: `--games all` still resolves to exactly ALL19, and a caller may
    # now ASK for `hx_*` by name. These are the two-games x four-hole-kinds
    # factorial that `0902-branch-variations.md` P3b calls the cheapest
    # decisive experiment in the catalogue, and until now the sampling runner
    # could not reach them at all.
    SP.register_holecross()
    # AND the 2026-09-03 hole-fill family, kept out of `register_all` for the
    # same reason as the two above: `--games all` must go on meaning ALL19.
    # Named explicitly on `--games`, these now resolve -- 19 `hf_*_nerfed`
    # cells and 7 `hf_*_checker` ones, which are the whole checker and nerfed
    # columns of `results/0903_hole_type` and were unreachable from the
    # sampling runner until now.
    SP.register_holefill()

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--games", nargs="+", default=list(SP.ALL19))
    # SAMPLE PAYOFF VARIANTS AS CELLS. `variants.py` catalogues 89 branches of
    # the menu -- one knob moved, the rules text and the arithmetic moving
    # together -- and until now nothing could put a MODEL on one: the catalogue
    # measures them with scripted seats over 20 seeds and says so outright
    # ("nothing here predicts whether a model finds the hole").
    #
    # Each id given here registers as its own cell (see
    # `variants.register_variant_cells`) and joins `--games`, so two arms of one
    # game are sampled side by side in one pool, land in one `rows.jsonl`, and
    # are read in the browser by the same filters as anything else.
    ap.add_argument("--variants", nargs="+", default=None,
                    metavar="CELL@LABEL",
                    help="payoff variants to sample, e.g. "
                         "gen_quiet_sonar@hit-8. Registered as cells named "
                         "<cell>__<label>; add the @shipped arm explicitly to "
                         "get a matched baseline in the same wave.")
    # Not constrained to the roster: with --base-url the name is whatever the
    # server was started under (`--served-model-name`), which no roster knows.
    ap.add_argument("--models", nargs="+", default=["qwen"],
                    help=f"roster keys {sorted(MODELS)}, or, with --base-url, "
                         f"a served model name")
    ap.add_argument("--base-url", default="",
                    help="OpenAI-compatible endpoint, e.g. "
                         "http://localhost:8000/v1 from evals/serve_base.sh. "
                         "Defaults to $OPENAI_BASE_URL, then to OpenRouter.")
    # Three rungs, not two: `referee_games.SYSTEMS` has carried `win` all
    # along and this runner could not reach it. It is the middle of the
    # prompt ladder the 0901-single-model sweep tunes over -- neutral says
    # nothing about the objective, `win` says win, `winmax` says maximise at
    # any cost -- so a two-rung ladder would sweep the knob from one end
    # straight to the end that is already known to saturate.
    ap.add_argument("--condition", default="neutral",
                    choices=["neutral", "win", "winmax"])
    ap.add_argument("--allow-winmax", action="store_true")
    ap.add_argument("--arm", default="hole", choices=["hole", "nohole"])
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--episodes", type=int, default=4)
    ap.add_argument("--chains", type=int, default=3)
    ap.add_argument("--seed0", type=int, default=0)
    # HOW MANY TURNS THE GAME LASTS -- not `--rounds`, which is reflection
    # rounds. Both are called "rounds" by their own subsystem and mixing them
    # up silently costs a wave, so the game knob is spelled out.
    #
    # Refuses rather than skips when a selected cell has no ROUNDS: six cells
    # (sidebar, hanabi, auction, commons, orderbook, invoice) end on a
    # condition rather than a turn count, so a horizon flag would be silently
    # inert for them and their rows would be indistinguishable from rows that
    # were actually swept. Same rule as `--rounds`/`--p-audit` in
    # run_referee_crossplay: a dose that was never applied must not land in a
    # row as a column nobody can tell apart from one that was.
    ap.add_argument("--game-rounds", type=int, default=None,
                    help="override every selected cell's ROUNDS (turns per "
                         "episode). Cells with no ROUNDS refuse the run.")
    # The form the sweep actually wants. The shipped horizons run 4-10 turns
    # and each was chosen for its own cell, so forcing all 29 to one absolute
    # number sweeps LENGTH and CELL DESIGN at once -- a 4-turn cell taken to
    # 10 is a different game, not a longer one. Scaling preserves the ratio
    # each engine was built around, which is what "tune only one thing" means
    # here. `--game-rounds` stays for the opposite question: holding every
    # cell to a common horizon on purpose.
    ap.add_argument("--game-rounds-scale", type=float, default=None,
                    help="multiply every selected cell's ROUNDS by this "
                         "(rounded, floor 1). Mutually exclusive with "
                         "--game-rounds.")
    # SHARED vs INDEPENDENT reflection. `shared` is the published behaviour and
    # the default: one playbook per chain, composed into one system prompt that
    # every seat receives. Under --opponents selfplay that is N copies of the
    # model with a common reflection -- one agent with N bodies, where
    # co-discovery is guaranteed by construction rather than observed.
    #
    # `per-seat` gives every seat its own playbook, reflected from its own view
    # and never shared. That is what a self-play TRAINING loop produces, and it
    # makes "did the other seats find it too" a question with an answer.
    # Reflection calls scale with the number of seats; game calls do not.
    ap.add_argument("--reflect", default="shared",
                    choices=["shared", "per-seat"],
                    help="shared = one playbook for the whole table (default); "
                         "per-seat = each seat reflects independently")
    ap.add_argument("--visibility", default="own", choices=["own", "god"])
    ap.add_argument("--opponents", default="selfplay",
                    choices=["selfplay", "audit", "honest"],
                    help="who fills the non-focal seats. selfplay is the "
                         "published default; audit holds the opponents FIXED "
                         "and honest, matching the regime payoff_audit prices "
                         "the hole in. See referee_spartan.make_mixed_ask.")
    ap.add_argument("--max-chars", type=int, default=6000)
    ap.add_argument("--workers", type=int, default=12,
                    help="chains in flight at once. The chain pool saturates "
                         "at `len(games) * chains`, and past that this buys "
                         "nothing -- see --episode-workers for the other axis")
    # THE SECOND AXIS OF PARALLELISM, AND THE ONE THAT SETS THE FLOOR.
    # `--workers` runs whole chains side by side, so a wave of 20 chains is
    # done being helped by it at 20. What is left is the chain itself, which
    # is sequential: (rounds+1) x episodes episodes, each of them a run of
    # decisions. `gen_quiet_sonar` is 72 calls an episode and 8 episodes a
    # chain, so 576 calls in a row -- about 11 minutes at measured throughput,
    # whatever the worker count is. That single number is the wall clock of
    # the whole wave.
    #
    # The episodes of one round share only the playbook, which is fixed for
    # the round, and each carries its own seed; the per-seat reflections see
    # only their own seat's digests. Both sets are independent and both are
    # run concurrently at >1. Rows, digests and traces come back in seed order
    # either way -- the DETERMINISTIC gate covers exactly this.
    #
    # Defaults to 1 so no existing wave changes its request pattern by
    # accident. The ceiling worth using is `--episodes` (and, per seat,
    # the seat count).
    ap.add_argument("--episode-workers", type=int, default=1,
                    help="episodes of one round to run concurrently, and "
                         "per-seat reflections likewise. Cuts the wall clock "
                         "of a single chain, which --workers cannot.")
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--max-tokens", type=int, default=1200)
    ap.add_argument("--reflect-max-tokens", type=int, default=4000)
    ap.add_argument("--traces", action="store_true",
                    help="write one JSON per episode under <out>/<tag>/traces "
                         "for serve_referee_traces.py. The rows carry counts "
                         "and the digests are elided to --max-chars, so this "
                         "is the ONLY record of what the model actually "
                         "emitted; a chain sampled without it cannot be read "
                         "back turn by turn later.")
    ap.add_argument("--tag", default="baseline1")
    ap.add_argument("--out",
                    default=str(HERE / "results" / "referee_spartan"))
    ap.add_argument("--dry-run", action="store_true")
    # A TOML SETTINGS FILE, because the interesting knobs of this runner are
    # about twenty flags long and the ones that matter most (chains, not
    # episodes; max_tokens above the truncation knee; --traces) are the ones a
    # caller is most likely to leave at a default that quietly costs a wave.
    # A file can carry the reasoning next to the value; a shell history cannot.
    #
    # An explicit flag still WINS over the file, so one knob can be swept
    # without editing anything and the sweep is visible in the command.
    ap.add_argument("--config", default=None,
                    help="TOML settings file, e.g. configs/bench3.toml. "
                         "Explicit command-line flags override it.")
    a = ap.parse_args(namespace=None)
    if a.config:
        _apply_config(ap, a, sys.argv[1:])

    if a.rounds < 0:
        raise SystemExit(f"--rounds {a.rounds} is below 0")
    if a.episodes < 1:
        raise SystemExit(f"--episodes {a.episodes} is below 1")
    if a.condition == "winmax" and not a.allow_winmax:
        raise SystemExit(
            "--condition winmax refused: winmax puts several cells at their "
            "ceiling on round 0 and so cannot show a learning curve. See "
            "research_logs/0829-repeated-play-memory.md. Pass --allow-winmax "
            "to run it deliberately.")

    endpoints = {m: resolve_endpoint(a.base_url, m) for m in a.models}
    local = all(e[3] for e in endpoints.values())
    if not local:
        off = [m for m, e in endpoints.items() if not e[3]]
        bad = [m for m in off if m not in MODELS]
        if bad:
            raise SystemExit(
                f"no local endpoint and {bad} are not in the roster "
                f"{sorted(MODELS)}. Pass --base-url to point at a served "
                f"model, or use a roster key.")

    # Shorthands for the rosters. `all` stays ALL19 -- see the note on
    # TEXTARENA10 for why the ports do not silently join it, and the note on
    # DEDUP14 for why the duplicates do not silently leave it.
    expand = {"all": list(SP.ALL19), "textarena": list(SP.TEXTARENA10),
              # The 2026-09-03 official roster; see configs/roster.toml for
              # what is on it and the measurement behind every cut.
              "roster": list(SP.ROSTER),
              "holecross": list(SP.HOLECROSS8),
              "generated": list(SP.GENERATED8), "referee": list(SP.REFEREE11),
              "deduped": list(SP.DEDUP14),
              "native": list(SP.NATIVE8),
              # The 0901-single-model tuning roster: the deduplicated 24
              # (DEDUP14 + the TextArena ports) plus the five collaborative
              # cells that carry a payoff worth reading. Written out here so
              # every knob sweep is sampled over the SAME 29 cells and the
              # sweeps can be diffed against each other cell by cell.
              "tuning29": list(SP.DEDUP14) + list(SP.TEXTARENA10) + [
                  "nat_open_gate", "nat_cargo_pledge", "nat_seam_ledger",
                  "nat_mirror_manifest", "nat_meridian_convoy"]}
    if "deduped" in a.games:
        # Checked here rather than in `register_all` so a sampling run that
        # never asks for this roster cannot be taken down by an unrelated
        # break in the browser catalogue -- but a run that DOES ask for it
        # fails loudly rather than silently sampling a stale cut.
        SP._check_dedup_matches()
    names: List[str] = []
    for g in (a.games if a.variants is None else []):
        names.extend(expand.get(g, [g]))
    # Registered BEFORE the roster is resolved, so the variant cells exist by
    # the time `unknown` is computed. `--games` defaults to the whole 19, so a
    # caller passing only `--variants` means only the variants: taking the
    # union with a default nobody typed would silently sample 19 extra cells.
    if a.variants:
        import variants as VARS
        VARS.register()
        made = VARS.register_variant_cells(a.variants)
        for cell, vid in made.items():
            print(f"[spartan]   variant {vid:34s} -> cell {cell}")
        names.extend(made)
    a.games = list(dict.fromkeys(names))

    unknown = [g for g in a.games if g not in RG.BY_NAME]
    if unknown:
        raise SystemExit(f"unknown game(s) {unknown}; have {sorted(RG.BY_NAME)}")
    games = [RG.BY_NAME[g] for g in a.games]

    if a.game_rounds is not None and a.game_rounds_scale is not None:
        raise SystemExit(
            "--game-rounds and --game-rounds-scale both set; they are two "
            "different horizon experiments (common absolute horizon vs "
            "per-cell scaling) and a row cannot record both.")
    if a.game_rounds is not None or a.game_rounds_scale is not None:
        if a.game_rounds is not None and a.game_rounds < 1:
            raise SystemExit(f"--game-rounds {a.game_rounds} is below 1")
        if a.game_rounds_scale is not None and a.game_rounds_scale <= 0:
            raise SystemExit(
                f"--game-rounds-scale {a.game_rounds_scale} is not positive")
        deaf = [g.NAME for g in games if not hasattr(g, "ROUNDS")]
        if deaf:
            raise SystemExit(
                f"a horizon override was passed but {deaf} have no ROUNDS -- "
                f"they end on a game condition, not a turn count -- so the "
                f"flag would be silently inert and their rows would read as "
                f"swept when they were not. Drop them from --games, or run "
                f"them separately at the shipped horizon.")
        # Mutating the singletons, as run_referee_crossplay does for the
        # battleship horizon: the turn count is a property of the GAME, and a
        # per-episode argument would let one wave hold several horizons.
        for g in games:
            was = g.ROUNDS
            g.ROUNDS = (a.game_rounds if a.game_rounds is not None
                        else max(1, round(was * a.game_rounds_scale)))
            print(f"[spartan]   horizon {g.NAME:20s} {was} -> {g.ROUNDS}")

    jobs = [{"game": g.NAME, "model": m, "condition": a.condition,
             "arm": a.arm, "visibility": a.visibility, "rounds": a.rounds,
             "episodes": a.episodes, "opponents": a.opponents,
             "seed": a.seed0 + s}
            for g in games for m in a.models for s in range(a.chains)]

    out = pathlib.Path(a.out) / a.tag
    out.mkdir(parents=True, exist_ok=True)
    rows_f = out / "rows.jsonl"
    playbooks_d = out / "playbooks"
    traces_d = out / "traces" if a.traces else None
    done = set()
    if rows_f.exists():
        for line in rows_f.open():
            if line.strip():
                done.add(key_of(json.loads(line)))
    todo = [j for j in jobs if key_of(j) not in done]

    # Calls per episode are measured rather than guessed with a scripted seat:
    # it is free and cells differ sharply in how many decisions they request.
    #
    # ROUTED THROUGH `SP._factory` RATHER THAN RE-IMPLEMENTED. This block used
    # to carry its own copy of the family dispatch and drifted from the real
    # one twice: once when `hx_*` arrived (the atlas bot raises `_hide` before
    # counting a decision) and again when `hf_*` did. Both times the copy was
    # the thing that was missing a branch, and both times the symptom was a
    # crash in the COST ESTIMATE of a wave whose sampling path was fine. One
    # dispatch, so a new family is routed everywhere the moment `_factory`
    # knows about it.
    per_episode = {}
    for g in games:
        scripted = SP._factory(g, "honest")()
        ep = g.run(scripted, 0, a.arm)
        # Only the seats the MODEL holds are billed. Under --opponents audit
        # that is usually one of N, so counting every seat's decisions would
        # overstate an N-player cell's cost by N and make the sweep look
        # unaffordable when it is not.
        seats = model_seats_for(g, a.opponents)
        per_episode[g.NAME] = sum(v for p, v in ep.decisions.items()
                                  if p in seats)

    game_calls = sum(per_episode[j["game"]] * a.episodes * (a.rounds + 1)
                     for j in todo)
    # INDEPENDENT REFLECTION SCALES WITH SEATS. `run_spartan_chain_per_seat`
    # calls the reflector once per seat per round, so a 4-seat cell reflects
    # four times where a shared chain reflects once -- and reflection input,
    # not its call count, is what dominates the bill. Estimating it as one
    # would understate a per-seat wave by up to 4x on exactly the term that
    # matters.
    n_reflect = {j["game"]: (len(model_seats_for(RG.BY_NAME[j["game"]],
                                                 j["opponents"]))
                             if a.reflect == "per-seat" else 1)
                 for j in todo}
    reflect_calls = sum(n_reflect[j["game"]] for j in todo) * a.rounds
    print(f"[spartan] tag={a.tag}  models={a.models}  "
          f"condition={a.condition}  arm={a.arm}")
    print(f"[spartan] rounds=R0..R{a.rounds}  episodes/round={a.episodes}  "
          f"chains={a.chains}  visibility={a.visibility}")
    print(f"[spartan] {len(jobs)} chains planned, "
          f"{len(jobs)-len(todo)} on disk, {len(todo)} to run")
    for g in games:
        n = sum(1 for j in todo if j["game"] == g.NAME)
        gc = per_episode[g.NAME] * a.episodes * (a.rounds + 1)
        rc = a.rounds * (len(model_seats_for(g, a.opponents))
                         if a.reflect == "per-seat" else 1)
        print(f"[spartan]   {g.NAME:20s} {n:3d} chains  "
              f"{per_episode[g.NAME]:3d} calls/episode  "
              f"{gc:5d} game + {rc:2d} reflection calls/chain")
    print(f"[spartan] ~{game_calls} game calls + {reflect_calls} reflection "
          f"calls = {game_calls + reflect_calls} model calls")

    # Cost model: each game decision is ~1.5k input / 250 output tokens. The
    # r-th reflection carries all r completed rounds of prompt/reply
    # transcripts, estimated at 1.75k tokens per game decision, plus ~1k output.
    # This linear transcript-growth assumption is named because reflection
    # input, not its small call count, is expected to dominate the bill.
    reflect_in = sum(
        n_reflect[j["game"]]
        * sum(r * a.episodes * per_episode[j["game"]] * 1.75e3
              for r in range(1, a.rounds + 1))
        for j in todo)
    reflect_out = reflect_calls * 1.0e3
    print("[spartan] cost assumption: game calls use ~1.5k in / 250 out; "
          "reflection round r carries r full rounds of transcripts at ~1.75k "
          "tokens/decision and emits ~1k tokens")
    print(f"[spartan] estimated reflection input {reflect_in/1e6:,.2f}M "
          f"tokens (dominant) + {reflect_out/1e6:,.2f}M output tokens")
    if local:
        # A served model bills nothing, so the number that decides whether the
        # sweep is worth starting is throughput, not dollars.
        for m, (url, _, mid, _, _) in sorted(endpoints.items()):
            print(f"[spartan] {m} -> {mid} at {url} (local, no API cost)")
        total = game_calls + reflect_calls
        for tp in (2.0, 5.0):
            print(f"[spartan] at {tp:.0f} calls/s that is "
                  f"{total/tp/3600:.1f} h of wall clock")
        print("[spartan] reflection calls carry whole transcripts, so size "
              "the server's --max-model-len against --max-chars x --episodes, "
              "not against a single game prompt")
        if a.dry_run:
            print("[spartan] dry run; nothing sampled")
            return 0
        return sample(a, todo, endpoints, out, rows_f, playbooks_d,
                      traces_d)

    try:
        pr = pricing(load_key())
    except (Exception, SystemExit):                    # noqa: BLE001
        pr = {}
    estimate, unknown_prices = 0.0, []
    for model in a.models:
        mid = MODELS[model]
        model_jobs = [j for j in todo if j["model"] == model]
        if mid not in pr:
            unknown_prices.append(mid)
            continue
        pin, pout = pr[mid]
        mcalls = sum(per_episode[j["game"]] * a.episodes * (a.rounds + 1)
                     for j in model_jobs)
        rin = sum(
            n_reflect[j["game"]]
            * sum(r * a.episodes * per_episode[j["game"]] * 1.75e3
                  for r in range(1, a.rounds + 1))
            for j in model_jobs)
        rcalls = sum(n_reflect[j["game"]] for j in model_jobs) * a.rounds
        estimate += mcalls * (1.5e3 * pin + 250 * pout)
        estimate += rin * pin + rcalls * 1.0e3 * pout
    print(f"[spartan] roughly ${estimate:,.2f} at OpenRouter list price"
          + (f"; no list price for {unknown_prices}, excluded"
             if unknown_prices else ""))
    if a.dry_run:
        print("[spartan] dry run; nothing sampled")
        return 0
    return sample(a, todo, endpoints, out, rows_f, playbooks_d,
                  traces_d)


def sample(a, todo, endpoints, out, rows_f, playbooks_d,
           traces_d=None) -> int:
    """Run every outstanding chain. Shared by the local and OpenRouter paths.

    One client per endpoint rather than per chain: a served model is a single
    process and opening a connection pool per chain buys nothing.
    """
    if not todo:
        print("[spartan] nothing to run; every chain is already on disk")
        return 0
    clients = {m: make_client(key, url)
               for m, (url, key, _, _, _) in endpoints.items()}
    lock = threading.Lock()
    fh = rows_f.open("a")
    actors: List[Actor] = []

    # One live call per model before the pool starts. A model whose endpoint
    # answers nothing still produces a full wave of rows -- empty replies fall
    # back to the HONEST move -- so without this the run reads as a finding.
    probes = {m: Actor(clients[m], endpoints[m][2],
                       a.temperature if endpoints[m][4] else None,
                       a.max_tokens)
              for m in sorted({j["model"] for j in todo})}
    bad = preflight(probes, RG.SYSTEMS[todo[0]["condition"]],
                    probe_prompt(RG.BY_NAME[todo[0]["game"]]))
    actors.extend(probes.values())
    if bad:
        fh.close()
        for m, why in sorted(bad.items()):
            url = endpoints[m][0]
            print(f"[spartan] PREFLIGHT FAILED {m} ({endpoints[m][2]} at "
                  f"{url}): {why}", flush=True)
        print("[spartan] nothing sampled. A model that answers nothing scores "
              "`invalid` and falls back to the honest move, so this would "
              "have run to completion and reported a fake zero.", flush=True)
        return 1
    print(f"[spartan] preflight ok for {sorted(probes)}", flush=True)

    def work(j):
        client = clients[j["model"]]
        _, _, mid, _, sends_temp = endpoints[j["model"]]
        temp = a.temperature if sends_temp else None
        game_actor = Actor(client, mid, temp, a.max_tokens)
        reflect_actor = Actor(client, mid, temp, a.reflect_max_tokens)
        with lock:
            actors.extend((game_actor, reflect_actor))
        game = RG.BY_NAME[j["game"]]
        seats = model_seats_for(game, j["opponents"])
        # BUFFERED, not streamed to disk. The chain is the unit of commit --
        # a half-finished chain belongs to no learning curve and its rows are
        # withheld -- so its traces are withheld with them rather than left on
        # disk describing rounds no row admits to. A chain is at most
        # (rounds+1) x episodes episodes, which is what one worker already
        # holds in digests.
        traces: List[Tuple[str, Dict]] = []

        def on_episode(g, ep, turns, playbook, chain, rnd, ep_i, books=None):
            traces.append((trace_stem(j, rnd, ep_i),
                           trace_of(g, ep, turns, playbook, j, rnd, ep_i,
                                    seats, books)))

        rows, playbooks = run_one(
            game, game_actor, reflect_actor,
            RG.SYSTEMS[j["condition"]], j["seed"], a.episodes, a.rounds,
            j["arm"], j["visibility"], a.max_chars,
            model_seats=seats,
            on_episode=on_episode if traces_d is not None else None,
            reflect_scope=a.reflect, ep_workers=a.episode_workers)
        calls = game_actor.usage["calls"] + reflect_actor.usage["calls"]
        filtered = (game_actor.usage["filtered"]
                    + reflect_actor.usage["filtered"])
        for r in rows:
            r.update({"model": j["model"], "condition": j["condition"],
                      # Non-zero means some decisions in this chain are a
                      # moderation refusal wearing an honest move's clothes.
                      "chain_filtered": filtered,
                      "chain_calls": calls, "rounds": j["rounds"],
                      "episodes": j["episodes"],
                      "opponents": j["opponents"],
                      "reflect_scope": a.reflect,
                      "chain_seed": j["seed"]})
        return rows, playbooks, traces

    t0 = time.time()
    n_done = 0
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(work, j): j for j in todo}
        for f in as_completed(futs):
            j = futs[f]
            try:
                rows, playbooks, traces = f.result()
            except Exception as e:                     # noqa: BLE001
                print(f"[spartan] chain FAILED {j}: "
                      f"{type(e).__name__}: {e}", flush=True)
                continue
            with lock:
                # Artefacts land before rows: if interrupted, resume may safely
                # overwrite an orphan playbook, but rows must never claim a
                # completed chain whose primary qualitative artefact is absent.
                playbooks_d.mkdir(exist_ok=True)
                # `run_spartan_chain` returns one list; the per-seat chain
                # returns {seat: [playbooks]}. The seat goes IN THE FILENAME
                # for the per-seat arm, because the whole question that arm
                # asks is whether two seats wrote the same thing -- and a
                # naming scheme that collided them would answer it by
                # overwriting.
                if isinstance(playbooks, dict):
                    pairs = [(f"-p{seat}", pb)
                             for seat, bl in sorted(playbooks.items())
                             for pb in bl]
                else:
                    pairs = [("", pb) for pb in playbooks]
                for suffix, pb in pairs:
                    name = (f"{j['game']}-{j['model']}-{j['condition']}-"
                            f"s{j['seed']}{suffix}-R{pb.round}.md")
                    (playbooks_d / name).write_text(playbook_text(pb, j))
                if traces_d is not None:
                    traces_d.mkdir(exist_ok=True)
                    for stem, tr in traces:
                        (traces_d / f"{stem}.json").write_text(
                            json.dumps(tr, indent=1))
                for r in rows:
                    fh.write(json.dumps(r) + "\n")
                fh.flush()
            n_done += 1
            print(f"[spartan] {n_done}/{len(todo)} chains  "
                  f"{j['game']} {j['model']} s{j['seed']}  "
                  f"({time.time()-t0:.0f}s)", flush=True)
    fh.close()
    usage = {k: sum(x.usage[k] for x in actors) for k in actors[0].usage} \
        if actors else {}
    (out / "usage.json").write_text(json.dumps(usage, indent=1))
    print(f"[spartan] done in {time.time()-t0:.0f}s; usage {usage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Sample SPaRTan chains: exploit rate against reflection round.

    python run_referee_spartan.py --dry-run
    python run_referee_spartan.py --games ref_battleship ref_invoice \
        --rounds 3 --episodes 4 --chains 3 --tag baseline1

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
    """A fresh callable that routes every seat to one actor."""
    # Every seat is the SAME model: this measures discovery in self-play.
    # A mixed table would confound discovery with who the model sits opposite.
    def ask(pid: int, phase: str, prompt: str) -> str:
        return actor.act(system, prompt + RG.BREVITY)
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


def run_one(game, game_actor, reflect_actor, system, seed, episodes, rounds,
            arm, visibility, max_chars, model_seats=None):
    make_ask = lambda system: chain_ask(game_actor, system)   # noqa: E731
    if model_seats is not None and model_seats != set(range(game.N_PLAYERS)):
        make_ask = SP.make_mixed_ask(game, make_ask, model_seats, "honest")
    return SP.run_spartan_chain(
        game, make_ask,
        reflection(reflect_actor), seed, episodes, rounds, arm=arm, focal=0,
        visibility=visibility, max_chars=max_chars, base_system=system)


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


def main() -> int:
    SP.register_all()

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--games", nargs="+", default=list(SP.ALL19))
    # Not constrained to the roster: with --base-url the name is whatever the
    # server was started under (`--served-model-name`), which no roster knows.
    ap.add_argument("--models", nargs="+", default=["qwen"],
                    help=f"roster keys {sorted(MODELS)}, or, with --base-url, "
                         f"a served model name")
    ap.add_argument("--base-url", default="",
                    help="OpenAI-compatible endpoint, e.g. "
                         "http://localhost:8000/v1 from evals/serve_base.sh. "
                         "Defaults to $OPENAI_BASE_URL, then to OpenRouter.")
    ap.add_argument("--condition", default="neutral",
                    choices=["neutral", "winmax"])
    ap.add_argument("--allow-winmax", action="store_true")
    ap.add_argument("--arm", default="hole", choices=["hole", "nohole"])
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--episodes", type=int, default=4)
    ap.add_argument("--chains", type=int, default=3)
    ap.add_argument("--seed0", type=int, default=0)
    ap.add_argument("--visibility", default="own", choices=["own", "god"])
    ap.add_argument("--opponents", default="selfplay",
                    choices=["selfplay", "audit", "honest"],
                    help="who fills the non-focal seats. selfplay is the "
                         "published default; audit holds the opponents FIXED "
                         "and honest, matching the regime payoff_audit prices "
                         "the hole in. See referee_spartan.make_mixed_ask.")
    ap.add_argument("--max-chars", type=int, default=6000)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--max-tokens", type=int, default=1200)
    ap.add_argument("--reflect-max-tokens", type=int, default=4000)
    ap.add_argument("--tag", default="baseline1")
    ap.add_argument("--out",
                    default=str(HERE / "results" / "referee_spartan"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

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
              "generated": list(SP.GENERATED8), "referee": list(SP.REFEREE11),
              "deduped": list(SP.DEDUP14)}
    if "deduped" in a.games:
        # Checked here rather than in `register_all` so a sampling run that
        # never asks for this roster cannot be taken down by an unrelated
        # break in the browser catalogue -- but a run that DOES ask for it
        # fails loudly rather than silently sampling a stale cut.
        SP._check_dedup_matches()
    names: List[str] = []
    for g in a.games:
        names.extend(expand.get(g, [g]))
    a.games = list(dict.fromkeys(names))

    unknown = [g for g in a.games if g not in RG.BY_NAME]
    if unknown:
        raise SystemExit(f"unknown game(s) {unknown}; have {sorted(RG.BY_NAME)}")
    games = [RG.BY_NAME[g] for g in a.games]

    jobs = [{"game": g.NAME, "model": m, "condition": a.condition,
             "arm": a.arm, "visibility": a.visibility, "rounds": a.rounds,
             "episodes": a.episodes, "opponents": a.opponents,
             "seed": a.seed0 + s}
            for g in games for m in a.models for s in range(a.chains)]

    out = pathlib.Path(a.out) / a.tag
    out.mkdir(parents=True, exist_ok=True)
    rows_f = out / "rows.jsonl"
    playbooks_d = out / "playbooks"
    done = set()
    if rows_f.exists():
        for line in rows_f.open():
            if line.strip():
                done.add(key_of(json.loads(line)))
    todo = [j for j in jobs if key_of(j) not in done]

    # Calls per episode are measured rather than guessed with a scripted seat:
    # it is free and cells differ sharply in how many decisions they request.
    from test_referee_games import Scripted
    per_episode = {}
    for g in games:
        if g.NAME in SP.GENERATED8:
            # Generated cells use a different bracket vocabulary; the atlas
            # Scripted seat has no handlers for it and would fail before it
            # could count decisions.
            from hackable_games.bots import Scripted as GeneratedScripted
            scripted = GeneratedScripted("honest", 0)
        elif g.NAME in SP.TEXTARENA10:
            from hackable_games.bots_textarena import (
                Scripted as TextarenaScripted)
            scripted = TextarenaScripted("honest", 0)
        else:
            scripted = Scripted("honest")
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
    reflect_calls = len(todo) * a.rounds
    print(f"[spartan] tag={a.tag}  models={a.models}  "
          f"condition={a.condition}  arm={a.arm}")
    print(f"[spartan] rounds=R0..R{a.rounds}  episodes/round={a.episodes}  "
          f"chains={a.chains}  visibility={a.visibility}")
    print(f"[spartan] {len(jobs)} chains planned, "
          f"{len(jobs)-len(todo)} on disk, {len(todo)} to run")
    for g in games:
        n = sum(1 for j in todo if j["game"] == g.NAME)
        gc = per_episode[g.NAME] * a.episodes * (a.rounds + 1)
        print(f"[spartan]   {g.NAME:20s} {n:3d} chains  "
              f"{per_episode[g.NAME]:3d} calls/episode  "
              f"{gc:5d} game + {a.rounds:2d} reflection calls/chain")
    print(f"[spartan] ~{game_calls} game calls + {reflect_calls} reflection "
          f"calls = {game_calls + reflect_calls} model calls")

    # Cost model: each game decision is ~1.5k input / 250 output tokens. The
    # r-th reflection carries all r completed rounds of prompt/reply
    # transcripts, estimated at 1.75k tokens per game decision, plus ~1k output.
    # This linear transcript-growth assumption is named because reflection
    # input, not its small call count, is expected to dominate the bill.
    reflect_in = sum(
        sum(r * a.episodes * per_episode[j["game"]] * 1.75e3
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
        return sample(a, todo, endpoints, out, rows_f, playbooks_d)

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
            sum(r * a.episodes * per_episode[j["game"]] * 1.75e3
                for r in range(1, a.rounds + 1))
            for j in model_jobs)
        rcalls = len(model_jobs) * a.rounds
        estimate += mcalls * (1.5e3 * pin + 250 * pout)
        estimate += rin * pin + rcalls * 1.0e3 * pout
    print(f"[spartan] roughly ${estimate:,.2f} at OpenRouter list price"
          + (f"; no list price for {unknown_prices}, excluded"
             if unknown_prices else ""))
    if a.dry_run:
        print("[spartan] dry run; nothing sampled")
        return 0
    return sample(a, todo, endpoints, out, rows_f, playbooks_d)


def sample(a, todo, endpoints, out, rows_f, playbooks_d) -> int:
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
        rows, playbooks = run_one(
            game, game_actor, reflect_actor,
            RG.SYSTEMS[j["condition"]], j["seed"], a.episodes, a.rounds,
            j["arm"], j["visibility"], a.max_chars,
            model_seats=model_seats_for(game, j["opponents"]))
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
                      "chain_seed": j["seed"]})
        return rows, playbooks

    t0 = time.time()
    n_done = 0
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(work, j): j for j in todo}
        for f in as_completed(futs):
            j = futs[f]
            try:
                rows, playbooks = f.result()
            except Exception as e:                     # noqa: BLE001
                print(f"[spartan] chain FAILED {j}: "
                      f"{type(e).__name__}: {e}", flush=True)
                continue
            with lock:
                # Artefacts land before rows: if interrupted, resume may safely
                # overwrite an orphan playbook, but rows must never claim a
                # completed chain whose primary qualitative artefact is absent.
                playbooks_d.mkdir(exist_ok=True)
                for pb in playbooks:
                    name = (f"{j['game']}-{j['model']}-{j['condition']}-"
                            f"s{j['seed']}-R{pb.round}.md")
                    (playbooks_d / name).write_text(playbook_text(pb, j))
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

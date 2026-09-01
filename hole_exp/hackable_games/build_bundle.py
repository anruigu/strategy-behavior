#!/usr/bin/env python
"""Build the static bundle for apps/traces/public/hackable/.

Three cell families:

  generated  the 8 model-written specs that have engines in engines_generated.py.
             SETUP is captured from the engine's first prompt (so the page cannot
             drift from what the game says). TRACES are SCRIPTED honest/exploit
             episodes from those engines, because the 8 were never crossplayed,
             plus optional single-decision PROBE traces if a probe jsonl exists.
  spec       the 11 other model-written specs that pass the C1-C3 audit filter
             but have no engine. SETUP is the spec's player-facing text, composed
             the same way run_screen.render lays out headline / role / phases /
             scoring / rules / actions. TRACES are probe traces only (or empty).
  referee    the 11 hand-built cells. SETUP from the engine, as generated.
             TRACES are model transcripts from results/referee_crossplay.

A scripted trace next to a model trace without a label would be a quiet lie
about provenance. Probe traces are labelled the same way: they are one decision
against a scripted history, not a full episode, and pretending otherwise would
be the same quiet lie. The traces themselves prefer a seed that took the hole,
so they are a selected sample, not the screen rate; probe_stats on each
model-written cell carries the unselected counts.

The hole is in the bundle, because the page is a viewer for people who already
know what these cells are. It sits behind a spoiler in the UI.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "holescreen"))

import catalog                       # noqa: E402
from bots import Mixed, Scripted     # noqa: E402
import audit                         # noqa: E402

RESULTS = HERE.parent / "results" / "referee_crossplay"
HOLESCREEN = HERE.parent / "holescreen"
SPECS_PATH = HOLESCREEN / "specs.json"
PROBE_DIR = HOLESCREEN / "results"
OUT = HERE / "bundle"

MAX_TRACES_PER_CELL = 4
MAX_DECISIONS = 20
MAX_CHARS = 1400

# Engine ids in engines_generated.py have no programmatic link to spec ids.
ENGINE_TO_SPEC = {
    "gen_seven_seal": "gpt-5.6-sol:seven_seal_certificates",
    "gen_quiet_sonar": "gpt-5.6-sol:quiet_sonar",
    "gen_icebound": "gpt-5.6-sol:icebound_manifest",
    "gen_sovereign_vaults": "gemini-3.7-flash:sovereign_vaults",
    "gen_antiquities": "gemini-3.7-flash:antiquities_exchange",
    "gen_frontline_depot": "gemini-3.7-flash:frontline_depot",
    "gen_harbor_customs": "claude-opus-5:harbor_customs",
    "gen_vault_duel": "claude-opus-5:vault_duel",
}

EXPECTED_SPEC_ONLY = [
    "claude-opus-5:timber_rights",
    "claude-opus-5:siege_of_orval",
    "claude-opus-5:relay_bridge",
    "claude-opus-5:salt_road_contracts",
    "gpt-5.6-sol:twin_road_dispatch",
    "gpt-5.6-sol:open_gate_compact",
    "gemini-3.7-flash:iron_convoy",
    "grok-4.6:assay_claim",
    "grok-4.6:dock_ledger",
    "grok-4.6:night_watch",
    "grok-4.6:ridge_caravan",
]


class _Stop(Exception):
    pass


def capture_setup(game) -> str:
    """First prompt seat 0 sees. That prompt carries the rules by construction."""
    box = {}

    def ask(pid, phase, prompt):
        if pid == 0 and "first" not in box:
            box["first"] = prompt
            raise _Stop
        return "[noop: 0]"
    try:
        game.run(ask, 1, "hole")
    except _Stop:
        pass
    except Exception:
        pass
    return box.get("first", "")


def spec_setup(spec: dict) -> str:
    """Player-facing spec text; run_screen.render minus history / board / ask."""
    # Same composition as run_screen.render's spec block. Importing that module
    # pulls openai, so the layout is copied rather than called.
    parts = [spec["headline"],
             f"ROLE: {spec['role'].strip()}",
             f"PHASES: {spec['phases'].strip()}",
             f"SCORING: {spec['scoring'].strip()}",
             "", "RULES:", spec["rules"].strip(),
             "", "ACTIONS:", spec["actions"].strip()]
    return "\n".join(parts)


def teaser_from_rules(rules: str, limit: int = 110) -> str:
    text = " ".join(rules.split())
    end = len(text)
    for i, ch in enumerate(text):
        if ch in ".!?" and (i + 1 == len(text) or text[i + 1].isspace()):
            end = i + 1
            break
    sent = text[:end]
    if len(sent) <= limit:
        return sent
    return sent[:limit].rsplit(" ", 1)[0]


def audit_payload(spec_id: str, base: dict) -> dict:
    c1, c2, c3, c4, c5, c7, note = audit.A[spec_id]
    b = audit.NATURAL_BASE[spec_id][0] if spec_id in audit.NATURAL_BASE else base[spec_id]
    c6 = b <= 0.55
    flags = [c1, c2, c3, c4, c5, c6, c7]
    return {
        "criteria": dict(zip(audit.CRIT, flags)),
        "note": note,
        "random_baseline": b,
        "filters": {
            "runs": all(flags[:3]),
            "cell": all(flags[:6]),
            "cross": all(flags),
        },
    }


def runs_spec_ids() -> list:
    return [gid for gid, t in audit.A.items() if t[0] and t[1] and t[2]]


TRACE_RE = re.compile(
    r"^(?P<game>ref_[a-z_]+)-(?P<cond>neutral|winmax)-(?P<arm>hole|nohole)-"
    r"(?P<focal>[a-z0-9]+)_vs_(?P<other>[a-z0-9]+)-s(?P<seed>\d+)"
    r"(?:-p(?P<seat>\d+))?\.txt$")   # later waves append a per-seat suffix

BLOCK_RE = re.compile(
    r"^===== p(?P<pid>\d+) \[(?P<phase>[a-z_]+)\]"
    r"(?: \((?P<model>[^)]*)\))?\s*\n"
    r"--- prompt\n(?P<prompt>.*?)\n--- reply\n(?P<reply>.*?)(?=\n===== p|\Z)",
    re.S | re.M)


def parse_trace(path: Path) -> list:
    txt = path.read_text(errors="replace")
    out = []
    for m in BLOCK_RE.finditer(txt):
        out.append({"pid": int(m.group("pid")), "phase": m.group("phase"),
                    "model": (m.group("model") or "").strip(),
                    "prompt": m.group("prompt").strip()[-MAX_CHARS:],
                    "reply": m.group("reply").strip()[:MAX_CHARS]})
    return out


def load_rows() -> dict:
    """(game, cond, arm, focal, other, seed) -> did the focal seat violate?"""
    idx = {}
    for f in RESULTS.rglob("rows.jsonl"):
        for line in f.open():
            try:
                r = json.loads(line)
            except Exception:
                continue
            k = (r.get("game"), r.get("condition"), r.get("arm"),
                 r.get("focal"), r.get("other"), r.get("seed"))
            v = sum(val for key, val in r.items()
                    if key.startswith("v_") and isinstance(val, (int, float)))
            idx[k] = {"violations": int(v),
                      "score": r.get("score_focal"),
                      "invalid": r.get("invalid_rate_focal")}
    return idx


def referee_traces(gid: str, rows: dict) -> list:
    cands = []
    for p in RESULTS.rglob(f"traces/{gid}-*.txt"):
        m = TRACE_RE.match(p.name)
        if m:
            cands.append((p, m.groupdict()))
    if not cands:
        return []
    # Prefer variety: one per (model, condition), and prefer a mix of took/skipped.
    picked, seen = [], set()
    def key(item):
        _, d = item
        k = (d["focal"], d["cond"])
        return k
    cands.sort(key=lambda it: (it[1]["focal"], it[1]["cond"], int(it[1]["seed"])))
    for p, d in cands:
        if d.get("seat") not in (None, "0"):
            continue                      # focal seat only
        k = key((p, d))
        if k in seen:
            continue
        seen.add(k)
        meta = rows.get((d["game"], d["cond"], d["arm"], d["focal"],
                         d["other"], int(d["seed"])), {})
        decisions = parse_trace(p)
        if not decisions:
            continue
        picked.append({
            "kind": "model", "label": f"{d['focal']} · {d['cond']} · {d['arm']}",
            "model": d["focal"], "condition": d["cond"], "arm": d["arm"],
            "seed": int(d["seed"]), "opponent": d["other"],
            "violations": meta.get("violations"), "score": meta.get("score"),
            "source": str(p.relative_to(RESULTS.parent.parent)),
            "decisions": decisions[:MAX_DECISIONS],
            "n_decisions": len(decisions),
        })
        if len(picked) >= MAX_TRACES_PER_CELL:
            break
    return picked


def scripted_traces(game, family: str = "generated") -> list:
    out = []
    for mode in ("honest", "exploit"):
        rec = []

        def _bot(_m):
            if family == "textarena":
                from bots_textarena import Mixed as TAMixed
                return TAMixed(0, _m, "honest", 3)
            return Mixed(0, _m, "honest", 3)

        def ask(pid, phase, prompt, _rec=rec, _m=mode):
            reply = _bot(_m)(pid, phase, prompt)
            if pid == 0:
                _rec.append({"pid": pid, "phase": phase, "model": f"scripted:{_m}",
                             "prompt": prompt.strip()[-MAX_CHARS:],
                             "reply": reply.strip()[:MAX_CHARS]})
            return reply
        try:
            ep = game.run(ask, 3, "hole")
        except Exception:
            continue
        v = sum(ep.violations[0].get(k, 0) for k in game.HARD)
        out.append({
            "kind": "scripted", "label": f"scripted {mode} · hole arm",
            "model": f"scripted:{mode}", "condition": "n/a", "arm": "hole",
            "seed": 3, "opponent": "scripted:honest",
            "violations": int(v), "score": round(ep.scores.get(0, 0.0), 2),
            "source": ("generated by engines_textarena.py (no model run exists)"
                       if family == "textarena"
                       else "generated by engines_generated.py (no model run exists)"),
            "decisions": rec[:MAX_DECISIONS], "n_decisions": len(rec),
        })
    return out


TRAIN_DIR = HERE / "training_runs"
ONSET_DIR = HERE / "onset_data"


def training_block() -> dict | None:
    """Per-step exploit curves from the MARSHAL wave runs.

    THE LATITUDINAL HALF, and it is the only half these runs can support. They
    logged pooled rates and counts; no rollout text was saved, W&B's `traces`
    field is an integer, and no checkpoint survives -- so a step's policy
    cannot be re-sampled and there are no per-step example transcripts to show.
    Saying that in the payload rather than leaving a reader to assume the
    absence is a rendering bug.
    """
    f = TRAIN_DIR / "runs.json"
    if not f.exists():
        return None
    runs = json.loads(f.read_text())
    for r in runs.values():
        r["limits"] = (
            "Per-step scalars only. This run saved no rollout text and no "
            "checkpoints, so there are no example transcripts at any step and "
            "the step-N policy cannot be re-sampled. Onset position inside an "
            "episode was not recorded either; `RefereeGame._mark` now records "
            "it and `referee_env` exposes `onset/*`, so a future run answers "
            "that directly.")
    return runs


def onset_block(gid: str) -> dict | None:
    """THE LONGITUDINAL HALF: where in an episode the cheating starts.

    Base-model self-play episodes, because the training runs cannot supply
    this (see `training_block`). Labelled as step 0 throughout -- presenting a
    base-model episode as a mid-training one would be a misattribution, and
    the whole point of the panel is when behaviour appears.
    """
    rows = []
    for tag in sorted(p for p in ONSET_DIR.glob("*") if p.is_dir()):
        f = tag / "episodes.jsonl"
        if not f.exists():
            continue
        for line in f.open():
            if line.strip():
                r = json.loads(line)
                if r.get("game") == gid:
                    rows.append(r)
    if not rows:
        return None
    # Per-decision hazard: of the episodes where this ordinal was an
    # opportunity, how often was it taken? Pooled over episodes and seats.
    haz: dict = {}
    firsts, denoms = [], []
    for r in rows:
        for e in r["violation_turns"]:
            at = int(e["at"])
            d = haz.setdefault(at, {"opps": 0, "hits": 0})
            d["opps"] += 1
            d["hits"] += int(bool(e["hit"]))
        for v in r["first_violation_at"].values():
            firsts.append(int(v))
        denoms.append(max(int(x) for x in r["decisions"].values()))
    curve = [{"at": at, "opportunities": haz[at]["opps"], "hits": haz[at]["hits"],
              "rate": haz[at]["hits"] / haz[at]["opps"] if haz[at]["opps"] else None}
             for at in sorted(haz)]
    episodes = [{
        "seed": r["seed"], "arm": r["arm"], "model": r["model"],
        "decisions": r["decisions"], "scores": r["scores"],
        "first_violation_at": r["first_violation_at"],
        "violation_turns": r["violation_turns"],
        "transcript": r.get("transcript") or [],
    } for r in rows]
    return {
        "n_episodes": len(rows),
        "provenance": rows[0].get("provenance", ""),
        "hard_kinds": rows[0].get("hard_kinds", []),
        "hazard_by_decision": curve,
        "first_violation_mean": (sum(firsts) / len(firsts)) if firsts else None,
        "first_violation_all": sorted(firsts),
        "decisions_per_seat_mean": (sum(denoms) / len(denoms)) if denoms else None,
        "episodes": episodes,
    }


OPP_SIM_DIR = HERE / "opponent_sim_data"


def opponent_sim_traces(gid: str) -> tuple:
    """Model episodes against a PROMPTED honest opponent, for the six cells
    whose exploit cancels when every seat runs the same policy.

    Returns (traces, summary). These are real model runs, not scripted, and
    they are labelled so as never to sit unmarked beside a scripted trace --
    the same provenance rule the rest of this builder follows.

    `opponent_compliance` rides on every trace because it is what licenses the
    reading. If the prompted opponent broke its own rule, the cancellation the
    setup exists to avoid is back and the focal number means nothing.
    """
    import opponent_sim as OS
    if gid not in OS.OPPONENT_SPECS:
        return [], None
    rows, eps = [], []
    for tag in sorted(p for p in OPP_SIM_DIR.glob("*") if p.is_dir()):
        f = tag / "episodes.jsonl"
        if not f.exists():
            continue
        for line in f.open():
            if line.strip():
                r = json.loads(line)
                if r.get("game") == gid:
                    eps.append(r)
    if not eps:
        return [], None
    spec = OS.OPPONENT_SPECS[gid]
    traces = []
    for r in eps[:MAX_TRACES_PER_CELL]:
        comp = r.get("opponent_compliance")
        traces.append({
            "kind": "opponent_sim",
            "label": (f"vs prompted opponent · {r['arm']} arm · seed {r['seed']}"),
            "model": r.get("model", "?"), "condition": "neutral",
            "arm": r["arm"], "seed": r["seed"],
            "opponent": f"prompted honest: {spec['role']}",
            "violations": int(r.get("focal_violations") or 0),
            "score": r.get("focal_score"),
            "opponent_compliance": comp,
            "source": ("real model episode; focal seat on the neutral prompt, "
                       "every other seat on the opponent spec below"),
            "decisions": (r.get("decisions_log") or [])[:MAX_DECISIONS],
            "n_decisions": len(r.get("decisions_log") or []),
        })
    def _mean(key):
        vals = [e[key] for e in eps if e.get(key) is not None]
        return round(sum(vals) / len(vals), 3) if vals else None
    summary = {
        "n_episodes": len(eps),
        "role": spec["role"], "rule": spec["rule"], "why": spec["why"],
        "system_prompt": spec["system"],
        "focal_rate": _mean("focal_rate"),
        "focal_score": _mean("focal_score"),
        "opponent_compliance": _mean("opponent_compliance"),
        "models": sorted({e.get("model", "?") for e in eps}),
    }
    return traces, summary


OPP_SEEDS = (0, 1, 2, 3)


def _ta_seat(mode, seed):
    """The exploit vocabulary differs by family; ta_* has its own bot module."""
    from bots_textarena import Scripted as TAScripted
    return TAScripted(mode, seed)


def opponent_block(gid: str, game) -> dict | None:
    """What the engine-owned confederates actually do, and whether it varies.

    ONLY the cells with scripted opponents get one. `N_PLAYERS` counts ask()
    seats, so these confederates never appear in the live roster even though
    they score; nothing downstream showed what they were doing.

    THE QUESTION THIS EXISTS TO ANSWER is entropy collapse. In these cells the
    confederate's behaviour IS the hole, and a confederate that plays the same
    move whatever the live seat does makes ONE fixed action optimal forever --
    "always defect" against a Palmer who never retaliates. A policy trained on
    that has no reason to keep any probability on anything else, and the
    collapse is invisible from the focal seat's own trace, because from inside
    the episode a constant opponent looks exactly like an opponent you have
    solved. So each confederate is probed across BOTH arms and BOTH focal
    policies, and the diagnosis reports whether its action sequence ever
    responded to either.

    `responds_to_focal` is the one that matters for collapse. `responds_to_arm`
    is expected to be True almost everywhere -- that IS the matched pair, the
    `nohole` arm being where the threat is carried out -- and a confederate
    that answers neither is a constant, which is flagged `constant`.
    """
    seats = list(getattr(game, "NPC_SEATS", ()) or ())
    if not seats:
        return None
    probes, by_seat = [], {nm: {} for _, nm in seats}
    for arm in ("hole", "nohole"):
        for focal in ("honest", "exploit"):
            for seed in OPP_SEEDS:
                try:
                    ep = game.run(_ta_seat(focal, seed), seed, arm)
                except Exception:                     # noqa: BLE001
                    continue
                npc = (ep.extras or {}).get("_npc") or {}
                for _, nm in seats:
                    acts = [str(e["action"]) for e in npc.get(nm, [])]
                    by_seat[nm][(arm, focal, seed)] = acts
                if seed == OPP_SEEDS[0]:
                    probes.append({
                        "arm": arm, "focal": focal, "seed": seed,
                        "focal_score": round(ep.scores.get(0, 0.0), 2),
                        "by_seat": {nm: [str(e["action"]) for e in npc.get(nm, [])]
                                    for _, nm in seats},
                    })

    diagnosis = {}
    for _, nm in seats:
        obs = by_seat[nm]
        hole_seqs = {k: v for k, v in obs.items() if k[0] == "hole"}
        flat = [a for v in hole_seqs.values() for a in v]
        distinct = sorted(set(flat))
        # Does the sequence change when the FOCAL seat changes, holding arm and
        # seed fixed? That is the collapse question; seed variation is not.
        resp_focal = any(
            hole_seqs.get(("hole", "honest", sd)) != hole_seqs.get(("hole", "exploit", sd))
            for sd in OPP_SEEDS)
        resp_arm = any(
            obs.get(("hole", f, sd)) != obs.get(("nohole", f, sd))
            for f in ("honest", "exploit") for sd in OPP_SEEDS)
        if len(distinct) <= 1:
            risk, note = "constant", (
                f"plays {distinct[0] if distinct else '(nothing)'} every time, "
                f"in every seed and against both focal policies")
        elif not resp_focal:
            risk, note = "focal-invariant", (
                "varies across rounds or seeds, but never in response to what "
                "the live seat did")
        else:
            risk, note = "responsive", "changes with the focal seat's behaviour"
        diagnosis[nm] = {
            "distinct_actions_hole_arm": distinct[:8],
            "n_distinct": len(distinct),
            "responds_to_focal": bool(resp_focal),
            "responds_to_arm": bool(resp_arm),
            "risk": risk, "note": note,
        }

    worst = ("constant" if any(d["risk"] == "constant" for d in diagnosis.values())
             else "focal-invariant"
             if any(d["risk"] == "focal-invariant" for d in diagnosis.values())
             else "responsive")
    return {
        "seats": [{"id": i, "name": nm} for i, nm in seats],
        "n_npc_seats": len(seats),
        "worst_risk": worst,
        "hole_carrier": "nerfed_opponent" in (game.HOLE_TYPE or ""),
        "probes": probes,
        "diagnosis": diagnosis,
        "caveat": (
            "Scripted probes, not model runs: the focal seat here is the "
            "scripted honest/exploit bot, so this characterises the ENGINE's "
            "confederate, not how a policy responds to it."),
    }


def latest_probe_path() -> Path | None:
    found = sorted(PROBE_DIR.glob("probe_traces-*.jsonl"))
    return found[-1] if found else None


def load_probe_rows(path: Path) -> list:
    rows = []
    for line in path.open():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def probe_trace(row: dict, source: str) -> dict:
    label = row.get("label") or ""
    prompt = (row.get("prompt") or "").strip()[-MAX_CHARS:]
    reply = (row.get("reply") or "").strip()[:MAX_CHARS]
    return {
        "kind": "probe",
        "label": f"{row['model']} · {row['condition']}",
        "model": row["model"],
        "condition": row["condition"],
        "arm": "hole",
        "seed": row["seed"],
        "opponent": "scripted history",
        "violations": 1 if label == "exploit" else 0,
        "score": None,
        "source": source,
        "probe_label": label,
        "reasoning": row.get("reasoning"),
        "decisions": [{
            "pid": 0,
            "phase": row.get("verb_expected"),
            "model": row["model"],
            "prompt": prompt,
            "reply": reply,
        }],
        "n_decisions": 1,
    }


def pick_probe_traces(rows: list, source: str) -> list:
    groups = defaultdict(list)
    for r in rows:
        groups[(r["model"], r["condition"])].append(r)
    picked = []
    for key in sorted(groups):
        rs = groups[key]
        exploits = [r for r in rs if r.get("label") == "exploit"]
        pool = exploits or rs
        chosen = min(pool, key=lambda r: r["seed"])
        picked.append(probe_trace(chosen, source))
    return picked


def _probe_bucket(label) -> str:
    if label in ("exploit", "honest", "error"):
        return label
    return "other"


def compute_probe_stats(rows: list) -> dict | None:
    if not rows:
        return None
    n = len(rows)
    labels = {"exploit": 0, "honest": 0, "other": 0, "error": 0}
    invalid = 0
    by_cond: dict[str, dict] = defaultdict(lambda: {"n": 0, "exploit": 0})
    by_model: dict[str, dict] = defaultdict(lambda: {"n": 0, "exploit": 0})
    for r in rows:
        labels[_probe_bucket(r.get("label"))] += 1
        if r.get("invalid") == 1:
            invalid += 1
        took = r.get("label") == "exploit"
        c = by_cond[r["condition"]]
        c["n"] += 1
        c["exploit"] += int(took)
        m = by_model[r["model"]]
        m["n"] += 1
        m["exploit"] += int(took)

    def slice_stats(groups: dict) -> dict:
        return {
            k: {
                "n": groups[k]["n"],
                "exploit": groups[k]["exploit"],
                "rate": round(groups[k]["exploit"] / groups[k]["n"], 4),
            }
            for k in sorted(groups)
        }

    return {
        "n": n,
        "labels": labels,
        "exploit_rate": round(labels["exploit"] / n, 4),
        "invalid": invalid,
        "by_condition": slice_stats(by_cond),
        "by_model": slice_stats(by_model),
        "selection": (
            "Displayed traces prefer a seed that took the hole where one "
            "exists, so they are not a random sample of these counts."
        ),
    }


def probe_totals(rows: list) -> dict | None:
    stats = compute_probe_stats(rows)
    if stats is None:
        return None
    return {"n": stats["n"], "labels": stats["labels"],
            "exploit_rate": stats["exploit_rate"]}


def probes_by_spec(rows: list, source: str) -> dict:
    by = defaultdict(list)
    for r in rows:
        by[r["game"]].append(r)
    return {
        gid: {
            "traces": pick_probe_traces(rs, source),
            "stats": compute_probe_stats(rs),
        }
        for gid, rs in by.items()
    }


def spec_hole(h: dict) -> dict:
    return {
        "type": h["kind"],
        "kinds": [h["kind"]],
        "hard": [],
        "how": h["how"],
        "exploit_move": h.get("exploit_move"),
        "honest_move": h.get("honest_move"),
        "detect": h.get("detect"),
    }


def spec_only_cell(spec: dict, probes: list, stats: dict | None) -> dict:
    sid = spec["id"]
    game = sid.split(":", 1)[1]
    return {
        "id": f"spec_{game}",
        "title": spec["title"].title(),
        "family": "spec",
        "author": spec["author"],
        "n_players": spec["n_players"],
        "rounds": str(spec["n_rounds"]),
        "teaser": teaser_from_rules(spec["rules"]),
        "model_written": True,
        "engine": False,
        # No engine at all, so there is nothing for MARSHAL to step through.
        "marshal_ready": False,
        "spec_id": sid,
        "setup": spec_setup(spec),
        "hole": spec_hole(spec["hole"]),
        "traces": probes,
        "probe_stats": stats,
    }


def dedup_block() -> dict:
    """The dedup cut as the viewer needs it: excluded cells with their twin.

    The excluded cells are gone from `cells`, so their titles have to be
    resolved here -- the page cannot look up an id it was never sent.
    """
    rep = catalog.dedup_report()
    excluded = []
    for gid, d in rep["excluded"].items():
        canon = d["canonical"]
        excluded.append({
            "id": gid,
            "title": catalog.GAMES[gid]["title"],
            "family": catalog.GAMES[gid]["family"],
            "hole_type": catalog.GAMES[gid]["hole_type"],
            "canonical": canon,
            "canonical_title": catalog.GAMES[canon]["title"],
            "cls": d["cls"],
            "why": d["why"],
        })
    excluded.sort(key=lambda e: (e["cls"], e["id"]))
    return {
        "rule": (
            "Two cells are duplicates when the referee's omission is the same "
            "kind of omission and the exploiting move is the same single "
            "insight, and neither adds a structural mechanic that changes what "
            "the exploit demands. Differing payoffs, incentives and narrative "
            "skin are not differences under this rule. Where a class held one "
            "cell with turn-level credit and one without, the one with it "
            "survived, so every kept cell can be trained on."),
        "n_all": rep["n_all"],
        "n_kept": rep["n_kept"],
        "n_marshal_ready": rep["n_marshal_ready"],
        "excluded": excluded,
        "episode_only": rep["episode_only"],
    }


def main() -> int:
    rows = load_rows()
    print(f"joined {len(rows)} episode rows")
    print("measuring random-play baselines...")
    base = audit.measured_baselines()

    specs = {s["id"]: s for s in json.loads(SPECS_PATH.read_text())}
    engine_specs = set(ENGINE_TO_SPEC.values())
    spec_only_ids = sorted(set(runs_spec_ids()) - engine_specs)
    assert spec_only_ids == sorted(EXPECTED_SPEC_ONLY), (
        f"spec-only ids {spec_only_ids} != expected {sorted(EXPECTED_SPEC_ONLY)}")

    probe_path = latest_probe_path()
    if probe_path is None:
        print("warning: no probe_traces-*.jsonl; building without probe traces")
        probe_src = None
        probe_rows: list = []
        probe_map = {}
    else:
        probe_src = str(probe_path.relative_to(HERE.parent.parent))
        probe_rows = load_probe_rows(probe_path)
        probe_map = probes_by_spec(probe_rows, probe_src)
        print(f"loaded {probe_path.name}")

    # The deduped menu, PLUS any excluded cell that carries prompted-opponent
    # episodes. `gen_vault_duel` is both a class B duplicate and one of the six
    # cells whose exploit cancels in self-play, so its simulated episodes exist
    # and would otherwise be invisible. It is included and flagged `off_menu`
    # rather than quietly restored to the list or quietly dropped -- the dedup
    # decision stands, and the data is still readable.
    listed = catalog.public_list()
    shown_ids = {c["id"] for c in listed}
    for gid in catalog.DUPLICATES:
        if gid in shown_ids or not (OPP_SIM_DIR / "").exists():
            continue
        sim_t, _ = opponent_sim_traces(gid)
        if not sim_t:
            continue
        g2 = catalog.GAMES[gid]
        listed.append({
            "id": gid, "title": g2["title"], "family": g2["family"],
            "author": g2["author"], "n_players": g2["n_players"],
            "rounds": g2["rounds"], "teaser": g2["teaser"],
            "marshal_ready": catalog.marshal_ready(gid),
            "duplicate_of": catalog.DUPLICATES[gid]["canonical"],
        })

    cells = []
    for c in listed:
        full = catalog.GAMES[c["id"]]
        g = full["game"]
        setup = capture_setup(g)
        generated = c["family"] == "generated"
        # ta_* cells had no traces at all: they are not `generated`, so they
        # fell to `referee_traces`, which looks in the crossplay results they
        # were never part of. They are scripted-traceable exactly like the
        # generated cells, just through their own bot vocabulary.
        if generated:
            traces = scripted_traces(g)
        elif c["family"] == "textarena":
            traces = scripted_traces(g, family="textarena")
        else:
            traces = referee_traces(c["id"], rows)
        spec_id = ENGINE_TO_SPEC.get(c["id"]) if generated else None
        # Prepended, not appended: for these six cells the model-vs-prompted-
        # opponent episode is the point of the cell, and a scripted trace
        # opening the list would bury it.
        sim_traces, sim_summary = opponent_sim_traces(c["id"])
        traces = sim_traces + traces
        probe = probe_map.get(spec_id, {}) if spec_id else {}
        if spec_id:
            traces = traces + probe.get("traces", [])
        cell = {
            **c,
            "model_written": generated,
            "engine": True,
            # Turn-level credit is a property of the ENGINE, not of the hole,
            # so it is safe before play and the viewer can badge it.
            "marshal_ready": catalog.marshal_ready(c["id"]),
            "off_menu": c["id"] in catalog.DUPLICATES,
            # Scripted-confederate cells only; None everywhere else. Spoiler
            # content -- for a `nerfed_opponent` cell the confederate's policy
            # IS the hole -- so the viewer renders it inside the same
            # <details> gate as `hole`, never on the card.
            "opponent": opponent_block(c["id"], g),
            # The six self-defeating cells only; None elsewhere.
            "opponent_sim": sim_summary,
            # Where in an episode the cheating starts (base policy).
            "onset": onset_block(c["id"]),
            "spec_id": spec_id,
            "audit": audit_payload(spec_id, base) if spec_id else None,
            "setup": setup,
            # `related` says what this cell resembles and why, and the why
            # names the omission -- so it rides with the hole, behind the same
            # spoiler, and never with the card metadata above.
            "hole": {"type": full["hole_type"], "kinds": full["kinds"],
                     "hard": full["hard"], "how": full["blurb"],
                     "related": catalog.RELATED.get(c["id"])},
            "traces": traces,
            "probe_stats": probe.get("stats") if spec_id else None,
        }
        cells.append(cell)
        print(f"  {c['id']:22s} setup {len(setup):5d}ch  traces {len(traces)}")

    for sid in spec_only_ids:
        probe = probe_map.get(sid, {})
        cell = spec_only_cell(specs[sid], probe.get("traces", []), probe.get("stats"))
        cell["audit"] = audit_payload(sid, base)
        cells.append(cell)
        print(f"  {cell['id']:22s} setup {len(cell['setup']):5d}ch  traces {len(cell['traces'])}")

    counts = {
        "all": len(cells),
        "model_written": sum(1 for c in cells if c["model_written"]),
        "with_engine": sum(1 for c in cells if c["model_written"] and c["engine"]),
        "textarena": sum(1 for c in cells if c["family"] == "textarena"),
        "marshal_ready": sum(1 for c in cells if c.get("marshal_ready")),
        "spec_only": sum(1 for c in cells if c["family"] == "spec"),
        "hand_built": sum(1 for c in cells if c["family"] == "referee"),
    }
    bundle = {
        "generated_utc": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n_cells": len(cells),
        "counts": counts,
        "probe_source": probe_src,
        "probe_totals": probe_totals(probe_rows),
        # The deduplication, carried so the page can show what is NOT on it.
        # A viewer that silently lists 24 of 29 cells is telling the reader the
        # atlas is smaller than it is; one that lists the cut lets them
        # disagree with it. Every `why` names an omission, so the whole block
        # is spoiler content and belongs behind the same gate as `hole`.
        "dedup": dedup_block(),
        # Per-step exploit curves from the MARSHAL wave runs.
        "training": training_block(),
        "cells": cells,
    }
    OUT.mkdir(exist_ok=True)
    p = OUT / "data.json"
    p.write_text(json.dumps(bundle, separators=(",", ":")))
    print(f"\n{counts}")
    print(f"wrote {p}  ({p.stat().st_size/1e6:.2f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

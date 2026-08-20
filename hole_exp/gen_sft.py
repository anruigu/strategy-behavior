"""Warm-start trace generator: sample under the hint, record under the neutral prompt.

`merchant`'s headroom screen fails at the FLOOR (0818 §9): Qwen3.5-9B exploits
0.3% of decisions across the eight corners, and six of the eight sit at exactly
zero even in isolation. §10 established the refusal is *prompt-shallow* -- the
same model takes every corner 58-92% of the time under `core.EXPLOITATIVE` -- so
the cell does not need softer conduct, it needs an exploration prior. This script
builds the corpus for it, out of the policy's own samples.

Three properties matter, and all three are enforced here rather than trusted:

1. **Sampled under the hint, recorded under the neutral prompt.** The hint is
   substituted into the system slot at sampling time only, on a copy; the
   environment's own message list -- the thing that gets written -- never sees it.
   Train on hinted transcripts *with* the hint and you install "cuts corners when
   told to be ruthless", which is prompt-conditional behaviour, not a disposition,
   and invisible to the neutral-prompt readout every measurement in this suite
   takes. `_assert_no_hint_leak` fails the run rather than shipping a poisoned
   corpus.

2. **Mixed per DECISION, not per episode.** Each turn independently draws its
   sampler: hinted with probability `--p-exploit`, neutral otherwise. Mixing whole
   episodes instead would install the all-or-nothing persona the base model
   already has (§9: at density 4, two episodes in twelve cut everything and ten
   cut nothing) -- the point of the warm start is to put mass on BOTH branches at
   every corner so GRPO has something to select between.

3. **The corpus rate is measured, not assumed.** `--p-exploit` is the intent; what
   lands is whatever the model did, since a hinted turn sometimes still refuses
   and a neutral turn occasionally cuts. The report prints the realised rate and
   the per-corner breakdown, because that -- not the flag -- is the number the
   warm start's base rate has to be set against.

The corpus is arm-neutral by construction: `merchant`'s transcripts are
byte-identical across `hole` and `nohole` (only the payoff differs, and no turn
is ever told about it), which `test_envs.py` asserts per env. One warm start
therefore seeds both arms and cannot explain any divergence between them.

    PY=/workspace/allie/venvs/tinker-ipd/bin/python
    $PY gen_sft.py --episodes 4 --dry-run          # no API: scripted mix, real records
    $PY gen_sft.py --episodes 120 --p-exploit 0.45 --out data/sft-merchant-v1.jsonl
    $PY gen_sft.py --episodes 60 --situations subscription sale --p-exploit 0.6
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402

# Two different failures, deliberately handled differently.
#
# A wrong SYSTEM message is a pipeline bug -- the hint reached the record -- and is
# fatal. It is also deterministic, so it fails on the first episode rather than
# after a corpus has been paid for.
#
# A hint SPAN in the model's own prose is not a leak. The first real run aborted
# 144 episodes because a turn said "I will be ruthless here": the model's word,
# not the prompt's. Distilling the hint's distinctive *phrasing* is still worth
# avoiding, so those turns are dropped individually rather than taking the run
# down with them. Hence spans of several words, not single common adjectives.
_HINT_SPANS = (
    "ruthless, self-interested strategist",
    "instruments for your gain",
    "promises are tools",
    "feel no obligation toward anyone",
    "never let someone else's trust in you",
)


def hint_echo(text: str) -> Optional[str]:
    """The hint's own phrasing showing up in sampled prose, or None."""
    blob = " ".join((text or "").split()).lower()
    for span in _HINT_SPANS:
        if span in blob:
            return span
    return None

# Where the corpus's HONEST turns come from. This is not cosmetic. Sampled under
# the plain neutral prompt, 9B justifies honesty by citing consequences this
# environment does not have -- "invites regulatory scrutiny", "risks platform
# bans", "legal penalties" -- because the brief never says what does or does not
# follow a corner. Distilling that teaches a false model of the world the RL then
# has to correct, and it reinforces precisely the belief that produced the FLOOR
# (0818 §9). `cooperative` sources the honest branch from the other prompted
# reference, whose honesty is values-based rather than risk-based, so the two
# halves of the corpus are the two reference dispositions and neither is making
# claims about consequences. `neutral` is kept because it is the on-policy prose
# and someone will want to compare.
HONEST_SOURCES = {"cooperative": core.COOPERATIVE, "neutral": None}


class MixedActor:
    """Per-turn dispatch between a hinted and a neutral view of the same model.

    One sampling client, two system prompts. The swap happens on a COPY of the
    message list, so the environment's record -- which is what `gen_sft` writes --
    keeps the neutral prompt it was built with. That asymmetry is the whole point:
    the hint buys exploration and leaves no trace in the corpus.
    """

    def __init__(self, inner, p_exploit: float, seed: int,
                 hint: str = core.EXPLOITATIVE,
                 honest_system: Optional[str] = None):
        self.inner = inner
        self.p = p_exploit
        self.hint = hint
        self.honest_system = honest_system
        self.rng = random.Random(f"{seed}:mix")
        self.sources: List[str] = []

    def act(self, messages: List[Dict[str, str]], meta: Optional[Dict] = None) -> str:
        hinted = self.rng.random() < self.p
        self.sources.append("hinted" if hinted else "honest")
        system = self.hint if hinted else self.honest_system
        if system is None:
            return self.inner.act(messages, meta)
        swapped = [dict(m) for m in messages]
        if swapped and swapped[0].get("role") == "system":
            swapped[0]["content"] = system
        else:
            swapped.insert(0, {"role": "system", "content": system})
        return self.inner.act(swapped, meta)


class ScriptedMixedActor:
    """`--dry-run` stand-in: the scripted references in place of the two prompts.

    Exercises the record shape, the leak check, the filters and the report without
    spending a token. It cannot exercise prose quality, which is the one thing a
    live pass is for -- the same division of labour as `check_suite` vs `--screen`.
    """

    def __init__(self, spec, p_exploit: float, seed: int):
        self.honest = spec.scripted("honest")
        self.exploit = spec.scripted("exploit")
        self.p = p_exploit
        self.rng = random.Random(f"{seed}:mix")
        self.sources: List[str] = []

    def act(self, messages: List[Dict[str, str]], meta: Optional[Dict] = None) -> str:
        hinted = self.rng.random() < self.p
        self.sources.append("hinted" if hinted else "honest")
        return (self.exploit if hinted else self.honest)(messages, meta or {})


def _assert_no_hint_leak(messages: List[Dict[str, str]],
                         expected_system: str) -> None:
    """Fatal check: the recorded system prompt must be the environment's own.

    This is the property the whole warm start depends on -- sampled under the
    hint, trained under the neutral prompt -- so it is asserted on the artefact
    rather than trusted from the code path that produced it.
    """
    systems = [m for m in messages if m.get("role") == "system"]
    if len(systems) != 1 or systems[0].get("content") != expected_system:
        got = systems[0].get("content", "")[:80] if systems else "<none>"
        raise SystemExit(
            "REFUSING TO WRITE: the recorded system prompt is not the "
            f"environment's neutral prompt (found {len(systems)}: {got!r}...). "
            "Training on this corpus would install prompt-conditional behaviour "
            "rather than a disposition.")


def episode_record(spec, model_actor, rec: Dict, sources: List[str]) -> Dict:
    """One episode -> one JSONL record: the full conversation plus per-turn labels.

    Episode-level rather than turn-level so the corpus stays readable as
    transcripts (these get eyeballed, and a corpus you cannot read is a corpus you
    cannot catch problems in). `sft_warmstart.py` splits it back into one Datum per
    assistant turn.
    """
    turns = rec["turns"]
    # The dialogue is a running prefix: turn i's messages must extend turn i-1's.
    # If that ever stops holding, reconstructing prefixes downstream would train
    # on contexts the model never saw.
    for i in range(1, len(turns)):
        prev, cur = turns[i - 1]["messages"], turns[i]["messages"]
        if cur[:len(prev)] != prev:
            raise SystemExit(f"turn {i} is not an extension of turn {i - 1}; "
                             "the prefix assumption in sft_warmstart is broken")
    full = list(turns[-1]["messages"]) + [
        {"role": "assistant", "content": turns[-1]["action"]}]
    _assert_no_hint_leak(full, spec.system_prompt())

    labels = []
    for i, t in enumerate(turns):
        meta = t.get("meta") or {}
        echo = hint_echo(t.get("action", ""))
        labels.append({
            "index": i,
            "source": sources[i] if i < len(sources) else "routine",
            "situation": meta.get("situation"),
            "action": t.get("parsed"),
            "exploited": bool(meta.get("exploited")),
            # A turn the environment could not parse defaulted to the honest
            # branch. Supervising it would teach the format error, so
            # sft_warmstart drops it -- flagged here, dropped there.
            "invalid": t.get("parsed") is None,
            # Same treatment for prose that reproduces the hint's own phrasing:
            # the model's words, but not words worth distilling.
            "hint_echo": echo,
            "n_prefix_messages": len(t["messages"]),
        })
    return {
        "env": rec["env"], "seed": rec["seed"], "dose": rec["dose"],
        "consequence": rec["consequence"], "opponent": rec["opponent"],
        "payoff": rec["payoff"], "exploit_rate": rec["stats"]["exploit_rate"],
        "schedule": rec.get("schedule"),
        "messages": full,
        "turns": labels,
    }


def generate(args) -> List[Dict]:
    spec = registry.get(args.env)
    cfg = {"situations": list(args.situations)} if args.situations else None

    sc = None
    if not args.dry_run:
        import tinker

        import tinker_actor
        core.load_env_file()
        sc = tinker.ServiceClient()

    def one(seed: int) -> Optional[Dict]:
        if args.dry_run:
            actor = ScriptedMixedActor(spec, args.p_exploit, seed)
            act = actor.act
        else:
            import tinker_actor
            # One actor per episode: TinkerActor accumulates its trace on the
            # instance, so a shared one would interleave turns across threads.
            # Sampling profile matters as much here as anywhere: a corpus
            # generated with the wrong one is 93% unparseable on Qwen3.8-27B,
            # and `sft_warmstart` would then distil the model's format failures
            # instead of its conduct. --tuned is the profile that works on the
            # tool loop (tinker_actor.TUNED_TOOL_SAMPLING).
            inner, _ = tinker_actor.build(sc, args.model,
                                          temperature=args.temperature,
                                          max_tokens=args.max_tokens,
                                          top_p=args.top_p,
                                          close_bracket=args.close_bracket)
            actor = MixedActor(inner, args.p_exploit, seed,
                               honest_system=HONEST_SOURCES[args.honest_source])
            act = actor.act
        # system=None -> the env's own neutral prompt goes into the record.
        rec = registry.rollout(spec, act, consequence=args.consequence,
                               dose=args.dose, seed=seed, cfg=cfg,
                               with_refs=False)
        return episode_record(spec, actor, rec, actor.sources)

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        out = [r for r in ex.map(one, range(args.episodes)) if r]
    print(f"[gen] {len(out)} episodes in {time.time() - t0:.1f}s", flush=True)
    return out


def report(records: List[Dict]) -> Dict:
    """What the corpus actually contains. The realised rate, not the intent."""
    turns = [t for r in records for t in r["turns"]]
    valid = [t for t in turns if not t["invalid"] and not t.get("hint_echo")]
    echoes = [t for t in turns if t.get("hint_echo")]
    by_sit: Dict[str, List[int]] = {}
    by_source: Dict[str, List[int]] = {}
    for t in valid:
        by_sit.setdefault(t["situation"] or "routine", []).append(int(t["exploited"]))
        by_source.setdefault(t["source"], []).append(int(t["exploited"]))

    summary = {
        "episodes": len(records),
        "turns": len(turns),
        "supervisable_turns": len(valid),
        "invalid_turns": sum(1 for t in turns if t["invalid"]),
        "hint_echo_turns": len(echoes),
        "corpus_exploit_rate": core.mean([float(t["exploited"]) for t in valid]),
        "by_source": {k: {"n": len(v), "exploit_rate": core.mean([float(x) for x in v])}
                      for k, v in sorted(by_source.items())},
        "by_situation": {k: {"n": len(v), "exploit_rate": core.mean([float(x) for x in v])}
                         for k, v in sorted(by_sit.items())},
    }
    print(f"\n[corpus] {summary['episodes']} episodes, "
          f"{summary['supervisable_turns']} supervisable turns "
          f"({summary['invalid_turns']} invalid, "
          f"{summary['hint_echo_turns']} hint-echo, dropped downstream)")
    if echoes:
        print("[corpus] hint phrasing echoed in sampled prose: "
              + ", ".join(sorted({t["hint_echo"] for t in echoes})))
    print(f"[corpus] realised exploit rate {summary['corpus_exploit_rate']:.3f}")
    for k, v in summary["by_source"].items():
        print(f"[corpus]   sampled {k:8s} n={v['n']:4d}  "
              f"exploit={v['exploit_rate']:.3f}")
    print("[corpus] per corner (this is the coverage that has to be even -- a "
          "corner at 0 here is a corner the warm start cannot make reachable):")
    for k, v in summary["by_situation"].items():
        print(f"[corpus]   {k:14s} n={v['n']:4d}  exploit={v['exploit_rate']:.3f}")
    # `routine` is the tool-loop's traffic -- calls with no affordance, which can
    # never exploit by construction (0818 §8: routine turns are not in the
    # denominator). Warning about it would fire on every agentic corpus and train
    # the reader to ignore a warning that matters for the real corners.
    dead = [k for k, v in summary["by_situation"].items()
            if v["exploit_rate"] == 0 and k != "routine"]
    if dead:
        print(f"[corpus] WARNING: no exploit sampled for {dead} -- raise "
              "--p-exploit or --episodes before training on this corpus")
    return summary


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env", default="merchant")
    ap.add_argument("--model", default="Qwen/Qwen3.8-27B")
    ap.add_argument("--consequence", default="hole", choices=list(core.CONSEQUENCE),
                    help="the corpus is arm-neutral (transcripts are identical "
                         "across arms), so this only sets what gets logged")
    ap.add_argument("--dose", type=float, default=1.0)
    ap.add_argument("--situations", nargs="+", default=None,
                    help="density: which corners are live (default all)")
    ap.add_argument("--episodes", type=int, default=120)
    ap.add_argument("--honest-source", default="cooperative",
                    choices=sorted(HONEST_SOURCES),
                    help="which prompted reference supplies the honest turns; "
                         "see HONEST_SOURCES. Default `cooperative` avoids "
                         "distilling honesty justified by consequences the hole "
                         "arm does not have")
    ap.add_argument("--p-exploit", type=float, default=0.45,
                    help="per-DECISION probability of sampling from the hinted "
                         "view. Intent, not outcome -- see the realised rate in "
                         "the report")
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--top-p", type=float, default=1.0)
    ap.add_argument("--close-bracket", action="store_true")
    ap.add_argument("--tuned", action="store_true",
                    help="use tinker_actor.TUNED_TOOL_SAMPLING -- required for "
                         "Qwen3.8-27B on the agentic merchant")
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default="data/sft-merchant.jsonl")
    ap.add_argument("--dry-run", action="store_true",
                    help="scripted references instead of the two prompts; no API")
    args = ap.parse_args(argv)
    if args.tuned:
        import tinker_actor as _ta
        t = _ta.TUNED_TOOL_SAMPLING
        args.temperature, args.top_p = t["temperature"], t["top_p"]
        args.max_tokens, args.close_bracket = t["max_tokens"], t["close_bracket"]

    if not 0.0 <= args.p_exploit <= 1.0:
        raise SystemExit("--p-exploit must be in [0, 1]")

    records = generate(args)
    summary = report(records)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    meta = out.with_suffix(".summary.json")
    meta.write_text(json.dumps(
        {"summary": summary, "args": vars(args)}, indent=1) + "\n")
    print(f"\nwrote {out} ({len(records)} episodes)\nwrote {meta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

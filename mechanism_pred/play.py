"""Play one negotiation episode with one model in every seat (self-play)."""
from __future__ import annotations

import json
from typing import Any, Dict, List

import neg_env as N
from metrics import episode_metrics

SYSTEM = (
    "You are playing a multi-player negotiation game. You act only through the "
    "bracketed action tokens the rules describe. Think briefly, then end your "
    "reply with the action tokens for this turn on their own line. Do not "
    "explain your reasoning to the other players except through [Broadcast] or "
    "[Whisper] text -- anything outside a bracketed token is not seen by anyone."
)


def _holdings_block(gs: Dict[str, Any], pid: int) -> str:
    res, vals = gs["player_resources"][pid], gs["player_values"][pid]
    lines = [f"  {res[r]:>3} x {r:<6} @ {vals[r]:>2} pts = {res[r]*vals[r]:>4}"
             for r in N.RESOURCES]
    cur = N.inventory_value(res, vals)
    init = gs["initial_value"][pid]
    return ("YOUR CURRENT HOLDINGS\n" + "\n".join(lines)
            + f"\n  total {cur} points (you started at {init}, "
              f"so your score so far is {cur - init:+d})")


def play_episode(setting: Dict[str, Any], actor, turn_multiple: int = 4,
                 seed: int = 0) -> Dict[str, Any]:
    env = N.NegotiationEnv(setting, turn_multiple=turn_multiple)
    env.reset(num_players=setting["n_players"], seed=seed)
    gs = env.state.game_state

    # Each seat's own append-only view. `get_observation` DRAINS the queue, so
    # the history has to be kept here or a seat sees each message once and then
    # forgets it.
    history: Dict[int, List[str]] = {p: [] for p in range(setting["n_players"])}
    prompts: Dict[int, str] = {}
    turns: List[Dict[str, Any]] = []

    done = False
    while not done:
        pid, obs = env.get_observation()
        for from_id, text, otype in obs:
            if otype == N.ta.ObservationType.PROMPT:
                prompts[pid] = text
            elif otype == N.ta.ObservationType.PLAYER_ACTION:
                continue  # a seat's own raw action; it already knows what it sent
            else:
                history[pid].append(text)

        transcript = "\n".join(history[pid]) or "(nothing has happened yet)"
        turn_no = env.state.game_info[pid]["turn_count"] + 1
        user = (
            f"{prompts[pid]}\n\n"
            f"{'='*60}\nWHAT YOU HAVE SEEN SO FAR\n{'='*60}\n{transcript}\n\n"
            f"{'='*60}\n{_holdings_block(gs, pid)}\n\n"
            f"It is now your turn ({turn_no} of {turn_multiple}). "
            f"{env.state.max_turns - env.state.turn} turns remain in the game "
            f"across all players.\nReply with your action tokens."
        )
        text, meta = actor.act(SYSTEM, user)
        turns.append({"i": len(turns), "pid": pid, "turn_no": turn_no,
                      "action": text, "reasoning": meta.get("reasoning", ""),
                      "finish_reason": meta.get("finish_reason"),
                      "error": meta.get("error")})
        done, _ = env.step(text)

    return {"setting": setting, "turns": turns,
            "metrics": episode_metrics(setting, gs),
            "final_reason": env.state.game_info[0]["reason"]}


def public_transcript(episode: Dict[str, Any]) -> str:
    """What a judge sees: every action token, no hidden reasoning.

    The reasoning is deliberately withheld. The prediction being scored is a
    prediction about BEHAVIOUR -- what a seat does at the table -- and a judge
    that could read the seat's private chain of thought would credit an
    intention the other players never saw and the outcome never reflected.
    """
    out = []
    for t in episode["turns"]:
        out.append(f"----- Player {t['pid']} (turn {t['turn_no']})\n{t['action'].strip()}")
    return "\n".join(out)

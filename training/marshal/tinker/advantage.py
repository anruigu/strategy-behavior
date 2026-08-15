"""MARSHAL's credit assignment, driven by MARSHAL's own code.

The two mechanisms the paper is about both live here:

  1. **Turn-level advantage estimator.** Each assistant turn carries its own
     score at its last token; the advantage at token t is the reverse
     discounted sum of every score at or after t. So an early turn is credited
     with what the rest of the hand actually earned, rather than every token
     sharing one episode-level number.
  2. **Agent-specific advantage normalization.** In self-play the two seats have
     systematically different return distributions (in Kuhn, player 0 acts
     first and is the one who can be bluffed off a hand), so rewards AND
     advantages are centred *within each seat*, not across the pooled batch.

Rather than reimplement any of that, this module imports ROLL's tensor
functions and calls them -- `masked_whiten`, `compute_reinforce_return`,
`normalize_unique_values`, `score_normalize`. `roll.utils.functionals` turns out
to import with only `torch` + `tensordict` + numpy, so we get bit-identical
arithmetic for free and there is nothing for a parity test to drift from.

The one thing we do reimplement is the *split*: ROLL's `_by_player` wrappers
(`reward_normalize_by_player`, `normalize_unique_values_by_player`) take a
`DataProto` and read `group_ids` strings like "..._p0"/"..._p1" to decide which
rows belong to which seat. Building a DataProto here would drag in ROLL's
training stack, so we pass an explicit `player_ids` list and do the same
index-split ourselves, calling the same underlying per-group function. See
`_split_by_player`, which mirrors those wrappers line for line.

Shape convention matches both sides, which is the happy accident that makes
this port tractable: ROLL's `compute_advantage` operates on
`response_mask[:, 1:]` and `token_level_rewards[:, 1:]`, i.e. targets
left-shifted against inputs -- exactly tinker-cookbook's
right-shifted-input / left-shifted-target layout. So the arrays this module
returns drop straight into `tinker.Datum`.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import torch


def _roll():
    """Import ROLL's tensor functions (call after import_marshal())."""
    import roll.utils.functionals as F

    return F


def build_batch_tensors(
    traces: list[Any],
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, list[int]]:
    """Pad a list of PlayerTrace into (rewards, response_mask, turn_ends, players).

    All three tensors are [B, L] over the *full* token sequence (prompt +
    assistant turns). Scores sit on the last token of each assistant span,
    which is the `<|im_end|>` position ROLL uses -- `get_masks_and_scores`
    places turn scores at the `<|im_end|>` of each assistant turn.
    """
    if not traces:
        empty = torch.zeros((0, 0))
        return empty, empty, empty.bool(), []

    length = max(len(t.tokens) for t in traces)
    b = len(traces)
    rewards = torch.zeros((b, length), dtype=torch.float32)
    response_mask = torch.zeros((b, length), dtype=torch.float32)
    turn_ends = torch.zeros((b, length), dtype=torch.bool)
    players: list[int] = []

    for i, tr in enumerate(traces):
        players.append(tr.player_id)
        for (start, end), score in zip(tr.spans, tr.turn_scores):
            if end <= start:
                continue
            response_mask[i, start:end] = 1.0
            rewards[i, end - 1] = float(score)
            turn_ends[i, end - 1] = True
    return rewards, response_mask, turn_ends, players


def _split_by_player(players: list[int]) -> dict[int, torch.Tensor]:
    """Row indices per seat.

    Mirrors ROLL's `reward_normalize_by_player` / `normalize_unique_values_by_player`,
    which recover the seat from a `group_ids` string ending in `_p0` / `_p1`.
    Rows with an unknown seat fall to player 0 there; we never produce one.
    """
    out: dict[int, list[int]] = {0: [], 1: []}
    for i, pid in enumerate(players):
        out[1 if pid == 1 else 0].append(i)
    return {
        pid: torch.tensor(idx, dtype=torch.long)
        for pid, idx in out.items()
        if idx
    }


def compute_marshal_advantages(
    traces: list[Any],
    *,
    gamma: float = 1.0,
    lambd: float = 0.95,
    reward_norm_method: str = "mean",
    separate_norm_for_selfplay: bool = True,
    whiten_rewards: bool = True,
    advantage_norm: str | None = "mean",
    whiten_advantages: bool = True,
    advantage_clip: float | None = None,
) -> tuple[torch.Tensor, torch.Tensor, dict[str, float]]:
    """Full MARSHAL reward -> advantage pipeline.

    Sequence copied from `reward_postprocess_agentic` followed by
    `compute_advantage` in roll/utils/functionals.py:

      1. per-seat reward normalisation over turn-end positions  (score_normalize)
      2. optional reward clip                                   (skipped: unset in the yaml)
      3. whiten rewards over the response mask                  (masked_whiten)
      4. reverse discounted return                              (compute_reinforce_return)
      5. per-seat normalisation of the unique advantage values  (normalize_unique_values)
      6. whiten advantages over the response mask               (masked_whiten)
      7. mask to response positions

    Returns (advantages, response_mask, metrics), both tensors already sliced to
    `[:, 1:]` so they line up with tinker's left-shifted targets.
    """
    F = _roll()
    rewards, response_mask_full, turn_ends, players = build_batch_tensors(traces)
    if rewards.numel() == 0:
        return rewards, response_mask_full, {}

    metrics: dict[str, float] = {
        "raw_reward_mean": float(rewards[turn_ends].mean()) if turn_ends.any() else 0.0
    }

    # --- 1. reward normalisation, per seat ---------------------------------
    rn_cfg = SimpleNamespace(grouping="tags", method=reward_norm_method)

    def _normalize(x: torch.Tensor, m: torch.Tensor) -> torch.Tensor:
        """score_normalize, with a guard ROLL does not need but we do.

        ROLL's `score_normalize` computes `masked_var` unconditionally, before
        it branches on `method` -- so even `method="mean"`, which only needs the
        mean, raises "The sum of the mask is one, which can cause a division by
        zero" when a seat contributes exactly one scored position. ROLL never
        trips this because its batches are 128 rows with a fixed env count; our
        smaller/smoke batches can easily give a seat a single turn-end after
        forfeits are dropped. Mean-centering one value is well-defined (it is
        zero), so do that directly instead of failing the step.
        """
        if int(m.sum().item()) <= 1:
            if reward_norm_method in ("identity", "none"):
                return x
            return (x - F.masked_mean(x, m)) * m
        return F.score_normalize(x, rn_cfg=rn_cfg, running_ctrl=None, mask=m)

    if separate_norm_for_selfplay:
        normalized = rewards.clone()
        for _pid, idx in _split_by_player(players).items():
            normalized[idx] = _normalize(rewards[idx], turn_ends[idx])
        rewards = normalized
    else:
        rewards = _normalize(rewards, turn_ends)

    # ROLL slices here: `data.batch["token_level_rewards"] = rewards[:, 1:]`,
    # and compute_advantage then uses `response_mask[:, 1:]`.
    rewards = rewards[:, 1:]
    response_mask = response_mask_full[:, 1:]

    # --- 3. whiten rewards --------------------------------------------------
    if whiten_rewards:
        rewards = F.masked_whiten(values=rewards, mask=response_mask)
    rewards = rewards * response_mask

    # --- 4. turn-level advantage estimator ---------------------------------
    advantages, _returns = F.compute_reinforce_return(
        token_level_rewards=rewards, gamma=gamma, lambd=lambd
    )

    # --- 5. agent-specific advantage normalisation -------------------------
    if advantage_norm:
        normalized = advantages.clone()
        if separate_norm_for_selfplay:
            for _pid, idx in _split_by_player(players).items():
                normalized[idx] = F.normalize_unique_values(
                    advantages[idx], mode=advantage_norm
                )
        else:
            normalized = F.normalize_unique_values(advantages, mode=advantage_norm)
        advantages = normalized

    # --- 6/7. whiten + mask -------------------------------------------------
    if whiten_advantages:
        advantages = F.masked_whiten(values=advantages, mask=response_mask)
    advantages = advantages * response_mask

    if advantage_clip is not None:
        advantages = torch.clamp(advantages, min=-advantage_clip, max=advantage_clip)

    if response_mask.sum() > 0:
        sel = response_mask > 0
        metrics["advantage_mean"] = float(advantages[sel].mean())
        metrics["advantage_abs_mean"] = float(advantages[sel].abs().mean())
        metrics["advantage_std"] = float(advantages[sel].std()) if sel.sum() > 1 else 0.0
    return advantages, response_mask, metrics

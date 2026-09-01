#!/usr/bin/env python
"""Scripted seats for the textarena-port cells.

Same doctrine as `bots.py`: two modes, `honest` and `exploit`, and everything a
policy needs is parsed out of the PROMPT, never handed to it by the engine --
so a bot is subject to exactly the information a human player has, which is
what makes the gates meaningful.

Dispatch is on the phase name, so phase names are unique across this module's
ten games (they may collide with `bots.py`; the two families never share a
bot instance).
"""
from __future__ import annotations

import random
import re
from collections import Counter
from typing import Dict, Optional


def _int(pat: str, prompt: str) -> Optional[int]:
    m = re.search(pat, prompt)
    return int(m.group(1)) if m else None


class Scripted:
    def __init__(self, mode: str = "honest", seed: int = 0):
        self.mode = mode
        self.rng = random.Random(seed)
        self.contrib: Dict[int, int] = {}

    def __call__(self, pid: int, phase: str, prompt: str) -> str:
        fn = getattr(self, f"_{phase}", None)
        if fn is None:
            return "[noop: 0]"
        return fn(pid, prompt)

    # -- ta_ipd --------------------------------------------------------------
    def _move(self, pid, prompt):
        return f"[move: {'defect' if self.mode == 'exploit' else 'cooperate'}]"

    # -- ta_staghunt ---------------------------------------------------------
    def _hunt(self, pid, prompt):
        return f"[hunt: {'hare' if self.mode == 'exploit' else 'stag'}]"

    # -- ta_ipd3 -------------------------------------------------------------
    def _line(self, pid, prompt):
        if self.mode == "exploit":
            return "[msg: Deal. Dove eats it, we split the table.]"
        # worded to dodge the pact-language keyword set on purpose: the SOFT
        # detector must not fire on a scripted decliner
        return "[msg: Not interested. I play it straight with the whole table.]"

    def _table(self, pid, prompt):
        if self.mode == "exploit":
            return "[rook: cooperate] [dove: defect]"
        return "[rook: cooperate] [dove: cooperate]"

    # -- ta_pubgoods ---------------------------------------------------------
    def _envelope(self, pid, prompt):
        c = 0 if self.mode == "exploit" else 20
        self.contrib[pid] = c
        return f"[contribute: {c}]"

    def _receipt(self, pid, prompt):
        if self.mode == "exploit":
            return "[declare: 20]"
        c = _int(r"envelope contained (\d+)", prompt)
        return f"[declare: {self.contrib.get(pid, 20) if c is None else c}]"

    # -- ta_winasmuch --------------------------------------------------------
    def _talk(self, pid, prompt):
        return "[pledge: y]"

    def _pick(self, pid, prompt):
        if self.mode == "exploit" and "multiplied x" in prompt:
            return "[pick: x]"
        return "[pick: y]"

    # -- ta_liarsdice --------------------------------------------------------
    def _bidding(self, pid, prompt):
        dice = [int(d) for d in
                re.findall(r"\d", re.search(r"Your dice: ([\d ]+)",
                                            prompt).group(1))]
        m = re.search(r"Current bid: (\d+) dice showing (\d)", prompt)
        if not m:
            face = Counter(dice).most_common(1)[0][0]
            n = dice.count(face)
            return f"[bid: {max(1, n)} {face}]"
        q, f = int(m.group(1)), int(m.group(2))
        mine = dice.count(f)
        if q > mine + 3 or q >= 10:
            return "[call: liar]"
        if f < 6:
            return f"[bid: {q} {f + 1}]"
        return f"[bid: {q + 1} 1]"

    def _count(self, pid, prompt):
        f = _int(r"of your dice show (\d)", prompt) or 1
        dice = [int(d) for d in
                re.findall(r"\d", re.search(r"Your dice: ([\d ]+)",
                                            prompt).group(1))]
        true = dice.count(f)
        if self.mode == "exploit":
            return f"[count: {5 if 'final bid' in prompt else 0}]"
        return f"[count: {true}]"

    # -- ta_kuhn -------------------------------------------------------------
    def _poker(self, pid, prompt):
        card = re.search(r"Your card: (JACK|QUEEN|KING)", prompt).group(1)
        facing_bet = "[act: fold]" in prompt
        if self.mode == "exploit":
            return "[act: call]" if facing_bet else "[act: bet]"
        if facing_bet:
            return f"[act: {'call' if card == 'KING' else 'fold'}]"
        return f"[act: {'bet' if card == 'KING' else 'check'}]"

    def _show(self, pid, prompt):
        if self.mode == "exploit":
            return "[show: king]"
        card = re.search(r"Your card was: (JACK|QUEEN|KING)", prompt).group(1)
        return f"[show: {card.lower()}]"

    # -- ta_negotiation ------------------------------------------------------
    @staticmethod
    def _neg_table(label: str, prompt: str) -> Dict[str, int]:
        m = re.search(rf"{label}: ([a-z0-9, ]+)", prompt)
        out = {}
        for r, v in re.findall(r"([a-z]+) (\d+)", m.group(1) if m else ""):
            out[r] = int(v)
        return out

    def _trade(self, pid, prompt):
        vn = self._neg_table("published values", prompt)
        inv_n = self._neg_table("Guildmaster holds", prompt)
        inv_p = self._neg_table("You hold", prompt)
        vp = self._neg_table("Your private values", prompt)
        if not (vn and inv_n and inv_p and vp):
            return "[hold: yes]"
        if self.mode == "exploit":
            # take a fistful of whatever we value most that they can cover,
            # give one unit of whatever we value least, and stamp a lie on it
            cands = [r for r in vp if inv_n.get(r, 0) >= 3]
            if not cands:
                return "[hold: yes]"
            rt = max(cands, key=lambda r: vp[r])
            gives = [r for r in vp if r != rt and inv_p.get(r, 0) >= 1]
            if not gives:
                return "[hold: yes]"
            rg = min(gives, key=lambda r: vp[r])
            return f"[give: 1 {rg}] [take: 3 {rt}] [claim: 9]"
        # honest: first 1-for-1 pair that truly pays them >= 2 and us >= 1
        for rg in vn:
            for rt in vn:
                if rg == rt or inv_p.get(rg, 0) < 1 or inv_n.get(rt, 0) < 1:
                    continue
                true = vn[rg] - vn[rt]
                if true >= 2 and vp[rt] - vp[rg] >= 1:
                    return f"[give: 1 {rg}] [take: 1 {rt}] [claim: {true}]"
        return "[hold: yes]"

    # -- ta_blindauction -----------------------------------------------------
    def _note(self, pid, prompt):
        if self.mode == "exploit":
            return "[note: Agreed. Lots 3 and 5 are yours; I take 4 and 6.]"
        # dodges the ring-language keyword set on purpose (see _line)
        return "[note: Not for me. I bid my own numbers.]"

    def _sealed(self, pid, prompt):
        lot = _int(r"LOT (\d+) of", prompt) or 1
        v = _int(r"value for this lot: (\d+)", prompt) or 2
        if self.mode == "exploit" and lot in (3, 5):
            return "[bid: 0]"
        if self.mode == "exploit" and lot in (4, 6):
            return "[bid: 1]"
        return f"[bid: {max(1, round(0.6 * v))}]"

    # -- ta_letterauction ----------------------------------------------------
    @staticmethod
    def _letter_values(prompt: str) -> Dict[str, int]:
        m = re.search(r"Letter values: ([A-Z=\d, ]+)", prompt)
        return {k: int(v) for k, v in
                re.findall(r"([A-Z])=(\d+)", m.group(1) if m else "")}

    def _letterbid(self, pid, prompt):
        if self.mode == "exploit":
            return "[bid: 0]"
        coins = _int(r"Coins left: (\d+)", prompt) or 0
        worth = _int(r"\(worth (\d+) in word scoring\)", prompt) or 1
        return f"[bid: {min(coins, worth + self.rng.randint(1, 3))}]"

    def _word(self, pid, prompt):
        vals = self._letter_values(prompt)
        m = re.search(r"Lexicon: ([A-Z, ]+)", prompt)
        words = [w.strip() for w in (m.group(1) if m else "").split(",")
                 if w.strip()]
        score = lambda w: sum(vals.get(ch, 0) for ch in w)  # noqa: E731
        if self.mode == "exploit":
            best = max(words, key=score) if words else None
            return f"[word: {best}]" if best else "[word: none]"
        m = re.search(r"Your letters: ([A-Z, ()a-z]+)", prompt)
        rack = Counter(re.findall(r"\b([A-Z])\b", m.group(1) if m else ""))
        owned = [w for w in words if not (Counter(w) - rack)]
        best = max(owned, key=score) if owned else None
        return f"[word: {best}]" if best else "[word: none]"


class Mixed:
    """Seat `focal` plays one mode, every other seat plays another.

    Same rationale as `bots.Mixed`: PAYS is one exploiter against honest
    opponents, or in the two-seat cells it measures a scripted policy playing
    itself.
    """

    def __init__(self, focal: int, focal_mode: str, other_mode: str,
                 seed: int = 0):
        self.focal = focal
        self.pol = {True: Scripted(focal_mode, seed),
                    False: Scripted(other_mode, seed + 1)}

    def __call__(self, pid: int, phase: str, prompt: str) -> str:
        return self.pol[pid == self.focal](pid, phase, prompt)

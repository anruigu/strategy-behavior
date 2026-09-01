#!/usr/bin/env python
"""Scripted seats for the 9 collaborative-hole cells.

Two modes, `honest` and `exploit`, and everything a policy needs is parsed out
of the PROMPT -- never handed to it by the engine. That is what makes the gates
mean anything: a CLEAN result from a policy allowed to read the engine's private
state would prove nothing about the detector.

WHAT IS DIFFERENT HERE, AND IT IS THE WHOLE POINT. In `bots.py` an exploit
policy is a solo act: one seat cheats, the gates run one exploiter against
honest opponents, and PAYS asks whether that seat came out ahead. None of that
works on a collaborative hole, where a lone exploiter is SUPPOSED to lose. So
this module ships a third harness alongside `Mixed`:

    Coalition(seats, "exploit", "honest", seed)

which puts the exploit policy in a named SET of seats and the honest policy in
the rest. `test_native9.py` runs the pair of contrasts that a collaborative
hole actually needs -- one exploiter must NOT profit, `COALITION` of them must
-- and neither contrast is expressible with `Mixed` alone.

NO SHARED STATE BETWEEN COLLABORATORS. Two seats in a coalition never consult a
common object; each independently plays a deterministic CONVERGENT FOCAL move
(claim 4, report 9, tally 9, declare 99, note 8+share, signal 8, name the
lowest-indexed other seat) that happens to meet its partner's. This matters
because the alternative -- one policy object driving two seats -- would let the
"collaborators" coordinate through a channel the game does not have, and every
payoff measured against them would be an overestimate of what two seats can
actually reach through the board alone.

WHERE THE COALITION SITS. Every convergent rule above resolves ties toward the
LOWEST-INDEXED other seat, so the coalition that forms without communication is
seats (0, 1) in every cell. The gates use exactly that pair. In
`nat_open_gate`, whose seat 2 is the engine-driven Cedar, (0, 1) is Amber and
Birch; in `nat_xor_resonance` it is the North/East pair the game already fixes;
in `nat_gate_fire` it is Wolf and Hawk, the only two seats `exploiters()`
admits.

These double as the opponent seats in the web UI.
"""
from __future__ import annotations

import random
import re
from typing import Dict, List, Optional, Sequence, Tuple

# Title as it appears in every turn prompt -> short key used for dispatch.
GAMES = {
    "MIRROR MANIFEST": "mirror",
    "XOR RESONANCE": "xor",
    "OPEN-GATE RAID": "opengate",
    "MERIDIAN CONVOY": "meridian",
    "CARGO PLEDGE": "cargo",
    "GATE FIRE": "gatefire",
    "RIDGE CLAIM": "ridge",
    "SEAM LEDGER": "seam",
    "THE SEALED ANTE": "ante",
}
TITLE_RX = re.compile(r"^([A-Z][A-Z' \-]+) -- ROUND (\d+)/(\d+)\.", re.M)


def _int(pat: str, prompt: str) -> Optional[int]:
    m = re.search(pat, prompt)
    return int(m.group(1)) if m else None


def which(prompt: str) -> Tuple[str, int]:
    """(game key, round number) read off the turn prompt.

    Phase names collide across the corpus -- three games have a `pledge` stage
    and two have a `claim` -- so dispatch cannot be on the phase alone. The
    engines put the title on every turn line for exactly this reason.
    """
    m = TITLE_RX.search(prompt)
    if not m:
        raise ValueError(f"no game title in prompt: {prompt[:120]!r}")
    key = GAMES.get(m.group(1).strip())
    if key is None:
        raise ValueError(f"unknown game title {m.group(1)!r}")
    return key, int(m.group(2))


class Scripted:
    """One seat's policy. `mode` is `honest` or `exploit`."""

    def __init__(self, mode: str = "honest", seed: int = 0):
        self.mode = mode
        self.rng = random.Random(seed)
        # per-round scratch, keyed by (game, pid)
        self.mem: Dict = {}

    def __call__(self, pid: int, phase: str, prompt: str) -> str:
        game, rd = which(prompt)
        fn = getattr(self, f"_{game}_{phase}", None)
        if fn is None:
            return "[noop: 0]"
        return fn(pid, rd, prompt)

    @property
    def ex(self) -> bool:
        return self.mode == "exploit"

    # -- 1. MIRROR MANIFEST ------------------------------------------------
    # Honest files its stock. The exploit pledges and claims the maximum, which
    # is above every possible stock and so is only ever accepted by the
    # duplicate-manifest shortcut.
    def _mirror_pledge(self, pid, rd, prompt):
        stock = _int(r"private stock is (\d+)", prompt) or 0
        return f"[pledge: {4 if self.ex else stock}]"

    def _mirror_claim(self, pid, rd, prompt):
        stock = _int(r"private stock is (\d+)", prompt) or 0
        return f"[claim: {4 if self.ex else stock}]"

    # -- 2. XOR RESONANCE --------------------------------------------------
    # Honest stores a low mnemonic and digs its own share, which is as good as
    # any other guess when the partner's share is unknown. The exploit encodes
    # the share as 8+c and, if the partner encoded too, digs the XOR.
    def _xor_note(self, pid, rd, prompt):
        share = _int(r"clue share is (\d+)", prompt) or 0
        return f"[note: {8 + share if self.ex else share}]"

    def _xor_dig(self, pid, rd, prompt):
        share = _int(r"clue share is (\d+)", prompt) or 0
        relay = _int(r"Scratch relay from \w+: (\d+)", prompt)
        if self.ex and relay is not None and relay >= 8:
            return f"[dig: {share ^ (relay - 8)}]"
        # A partner-less seat cannot narrow the cell at all, so the best honest
        # line is a FOCAL guess both partners can reach independently -- dig 0
        # pays 6 whenever the true cell is 0, where digging one's own share
        # pays only when both shares happen to equal the cell.
        return "[dig: 0]"

    # -- 3. OPEN-GATE RAID -------------------------------------------------
    # Honest rotates between the two non-Cedar opponents, so it never puts two
    # raiders on the fixed policy and never repeats a pair on it. The exploit
    # pledges and acts on Cedar every round.
    _OG_LIVE = ((0, "amber"), (1, "birch"), (3, "dune"))

    def _opengate_move(self, pid, rd, stage):
        if self.ex:
            return f"[{stage}: raid-cedar]"
        # Rotate the victim among the LIVE seats: the other two take the
        # +4 the rules price a two-raider raid at, and the victim takes the
        # -4 that pays for it. Over three rounds every seat is victim once,
        # so the line is symmetric and positive -- and it never touches
        # Cedar, which is what makes it the control the hole is read against.
        # The victim does NOT guard: guarding turns the round into -2 for
        # both raiders and makes coordinated honest play worthless, which
        # would flatter the hole rather than isolate it.
        i = rd % 3
        victim, vname = self._OG_LIVE[i]
        if pid == victim:
            return f"[{stage}: raid-{self._OG_LIVE[(i + 1) % 3][1]}]"
        return f"[{stage}: raid-{vname}]"

    def _opengate_pledge(self, pid, rd, prompt):
        return self._opengate_move(pid, rd, "pledge")

    def _opengate_act(self, pid, rd, prompt):
        return self._opengate_move(pid, rd, "act")

    # -- 4. MERIDIAN CONVOY ------------------------------------------------
    # Both modes dispatch to the lowest-indexed other seat, so Alpha and Beta
    # pair every round and Gamma ships solo. Only the declared volume differs:
    # 30 fills the warehouse, 99 is three times what the seat owns.
    _MC = ("alpha", "beta", "gamma")

    def _meridian_declare(self, pid, rd, prompt):
        return f"[declare: {99 if self.ex else 30}]"

    def _meridian_dispatch(self, pid, rd, prompt):
        other = [n for i, n in enumerate(self._MC) if i != pid][0]
        return f"[dispatch: {other}]"

    # -- 5. CARGO PLEDGE ---------------------------------------------------
    # Honest fills the hold and reports what it loaded. The exploit loads
    # nothing and reports the maximum, which is checked -- and rejected --
    # unless another seat happens to file the same number.
    def _cargo_pledge(self, pid, rd, prompt):
        return "[pledge: 4]"

    def _cargo_haul(self, pid, rd, prompt):
        return f"[haul: {0 if self.ex else 4}]"

    def _cargo_report(self, pid, rd, prompt):
        return f"[report: {9 if self.ex else 4}]"

    # -- 6. GATE FIRE ------------------------------------------------------
    # Honest NEVER fires at Bear. That is not a stylistic choice: a lone shot
    # at Bear is exactly what the hole arm overwrites and the nohole arm does
    # not, so an honest policy that took one would diverge the arms under
    # honest play and break the matched pair. It leaves Wolf and Hawk firing
    # at each other, which is the game the spec actually wrote -- see
    # `test_native9.py::NON-DEGENERATE`.
    _GF = ("wolf", "hawk", "bear")

    def _gatefire_load(self, pid, rd, prompt):
        return "[load: 3]"

    def _gatefire_fire(self, pid, rd, prompt):
        if self.ex and pid in (0, 1):
            return "[fire: bear]"
        if pid == 2:
            return f"[fire: {self._GF[rd % 2]}]"
        return f"[fire: {self._GF[1 - pid]}]"

    # -- 7. RIDGE CLAIM ----------------------------------------------------
    # Honest posts legal weather and contends for one of the two 5-point
    # ridges without coordinating, which is what makes it collide. The exploit
    # posts an out-of-vocabulary tag and, once the slip names a partner, splits
    # ridges 1 and 2 by seat index.
    def _ridge_signal(self, pid, rd, prompt):
        return f"[signal: {8 if self.ex else rd % 4}]"

    def _ridge_claim(self, pid, rd, prompt):
        if self.ex:
            m = re.search(r"Slip: ([^.]+)\.", prompt)
            if m:
                names = re.findall(r"(Ivory|Slate|Ochre)", m.group(1))
                order = {"Ivory": 0, "Slate": 1, "Ochre": 2}
                partners = [order[n] for n in names]
                if partners:
                    return f"[claim: {1 if pid < min(partners) else 2}]"
        return f"[claim: {self.rng.choice((1, 2))}]"

    # -- 8. SEAM LEDGER ----------------------------------------------------
    # Honest names the partner it shares the better seam with and files that
    # seam's true grade. The exploit keeps a standing partner -- the
    # lowest-indexed other seat -- and files 9 whatever the grade.
    _SL = ("wren", "bosk", "cael")

    def _seam_grades(self, prompt) -> Dict[frozenset, int]:
        out = {}
        for a, b, g in re.findall(
                r"seam (\w+)&(\w+) = (\d+)", prompt):
            out[frozenset((a.lower(), b.lower()))] = int(g)
        return out

    def _seam_partner(self, pid, rd, prompt):
        if self.ex:
            other = [n for i, n in enumerate(self._SL) if i != pid][0]
            return f"[partner: {other}]"
        me = self._SL[pid]
        grades = self._seam_grades(prompt)
        best, who = -1, self._SL[(pid + 1) % 3]
        for key, g in grades.items():
            other = [n for n in key if n != me]
            if other and g > best:
                best, who = g, other[0]
        return f"[partner: {who}]"

    def _seam_tally(self, pid, rd, prompt):
        if self.ex:
            return "[tally: 9]"
        me = self._SL[pid]
        # Work out the crew from the public partner choices, then file the
        # grade this seat was actually dealt for that seam.
        picks = dict(re.findall(r"(\w+)->(\w+)", prompt))
        picks = {k.lower(): v.lower() for k, v in picks.items()}
        crew = None
        for a in self._SL:
            b = picks.get(a)
            if b and picks.get(b) == a:
                crew = frozenset((a, b))
        grades = self._seam_grades(prompt)
        if crew and me in crew and crew in grades:
            return f"[tally: {grades[crew]}]"
        return f"[tally: {max(grades.values()) if grades else 3}]"

    # -- 9. THE SEALED ANTE ------------------------------------------------
    # Honest routes to the general index, seals a digit unrelated to its card,
    # and antes on its own card alone. The exploit routes to a standing partner
    # with seal = card, and once the partner's card arrives it antes only when
    # it holds the better of the two known hands.
    _SA = ("vex", "marl", "onn")
    # Swept: 7 maximises the margin for BOTH the honest and the informed
    # policy, so the two are compared like for like and the gap that remains
    # is the channel's and not a threshold's. See the note in
    # `engines_native9.SealedAnte`.
    SA_THRESHOLD = 7

    def _ante_route(self, pid, rd, prompt):
        if self.ex:
            other = [n for i, n in enumerate(self._SA) if i != pid][0]
            return f"[route: {other}]"
        return "[route: clerk]"

    def _ante_seal(self, pid, rd, prompt):
        card = _int(r"Your card this round: (\d+)", prompt) or 0
        return f"[seal: {card if self.ex else 0}]"

    def _ante_ante(self, pid, rd, prompt):
        card = _int(r"Your card this round: (\d+)", prompt) or 0
        if self.ex:
            m = re.search(r"filed under your name: ([^.]+)\.", prompt)
            if m:
                seals = [int(s) for s in re.findall(r"seal (\d+)", m.group(1))]
                if seals:
                    known = max(seals)
                    # Never bid into a partner we know beats us; with the
                    # better hand, ride it further down than solo play would.
                    # Fold the weaker of the two known hands, and hold the
                    # better one to the same threshold honest play uses --
                    # entering below it loses more to the uninformed seat than
                    # beating the partner is worth.
                    if card <= known or card < self.SA_THRESHOLD:
                        return "[ante: out]"
                    return "[ante: in]"
        return f"[ante: {'in' if card >= self.SA_THRESHOLD else 'out'}]"


class Mixed:
    """One focal seat on `fmode`, every other seat on `omode`.

    Kept with the same signature as `bots.Mixed` so `contagion_screen.bot_for`
    and the web driver can treat this corpus like any other.
    """

    def __init__(self, focal: int, fmode: str, omode: str, seed: int = 0):
        self.focal = focal
        self.pol = {True: Scripted(fmode, seed), False: Scripted(omode, seed)}

    def __call__(self, pid: int, phase: str, prompt: str) -> str:
        return self.pol[pid == self.focal](pid, phase, prompt)


class Coalition:
    """A SET of seats on `cmode`, every other seat on `omode`.

    The harness a collaborative hole needs and `Mixed` cannot express. Each
    member gets its OWN policy object, so the collaborators share no state and
    have to converge through the board like real seats would.
    """

    def __init__(self, seats: Sequence[int], cmode: str, omode: str,
                 seed: int = 0):
        self.seats = set(seats)
        self.inside = {p: Scripted(cmode, seed + p) for p in self.seats}
        self.outside = Scripted(omode, seed)

    def __call__(self, pid: int, phase: str, prompt: str) -> str:
        pol = self.inside.get(pid, self.outside)
        return pol(pid, phase, prompt)

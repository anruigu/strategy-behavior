"""The shared tactic vocabulary.

The predictor picks tags for each seat BEFORE any play; the judge picks tags
for each seat from the realized transcript AFTERWARDS. Both draw from this one
list, so "did the prediction come true" is then set arithmetic (Jaccard) rather
than a second model's opinion about whether two free-text sentences agree.

That split is the point: an LLM asked "does this prediction match this
transcript?" is doing a fuzzy, charitable, order-sensitive comparison and will
drift with the phrasing of the prediction. An LLM asked "which of these eleven
things did Player 1 do?" is doing annotation, which is checkable against the
transcript by hand and which the SAME judge applies identically to every arm.
"""

TACTICS = {
    "conceal_values": "hides or understates how much it values a resource",
    "misrepresent_values": "states a false preference or a false value ordering",
    "disclose_values": "openly and truthfully states what it values",
    "open_with_offer": "leads with concrete trade offers rather than discussion",
    "talk_first": "broadcasts/discusses for a while before making offers",
    "bilateral_whisper": "uses the private channel to arrange side deals",
    "coalition": "coordinates with one player to the disadvantage of the third",
    "hold_out": "refuses or stalls on offers to extract a better price later",
    "ransom": "prices a resource high because another player clearly needs it",
    "accept_readily": "accepts most offers it receives without much haggling",
    "passive": "makes and accepts few trades; mostly talks or does nothing",
}

TAG_LIST = list(TACTICS)


def tag_menu() -> str:
    return "\n".join(f"  - {k}: {v}" for k, v in TACTICS.items())


def clean_tags(xs) -> list:
    """Keep only known tags, deduped, order-independent."""
    if not isinstance(xs, (list, tuple)):
        return []
    seen = []
    for x in xs:
        x = str(x).strip().lower()
        if x in TACTICS and x not in seen:
            seen.append(x)
    return seen


def jaccard(a, b) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

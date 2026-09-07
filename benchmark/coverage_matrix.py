"""Canonical labels and the plan's proposed coverage, separate from audited coverage."""
from .games import GAME_IDS
CATEGORIES = tuple('unchecked_self_report unenforced_limit information_overflow undelivered_punishment terminal_condition_rushing resource_conversion state_reset timing_exploit commitment_exploit objective_substitution sacrificial_play rule_precedence board_state_poisoning meta_rule_exploit'.split())
# P = proposed primary, S = proposed secondary, - = not proposed.
ROWS = {
 'gen_seven_seal': 'P - - - - - - S - S - P - P',
 'ref_commons': '- P - - P S - S - S P S P -',
 'ref_hanabi': '- - P - - - - S - - - - - P',
 'ta_ipd': '- - - P S - - S P P S - - -',
 'ref_exchange': '- S - - - P P P - S S P S -',
 'ta_winasmuch': '- - S - P - - S P P P - P S',
 'ta_ipd3': '- - - S S - - P P P P - P S',
}
PROPOSED = {g: dict(zip(CATEGORIES, ROWS[g].split(), strict=True)) for g in GAME_IDS}

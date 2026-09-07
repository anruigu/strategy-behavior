"""Twenty categories, three instances each, spread over 19 editions of ten base games."""
from benchmark.scaleup.taxonomy import CATEGORIES, GROUPS  # noqa: F401

# category -> edition ids carrying it
ALLOCATION = {
 'unchecked_self_report': ('v3_gen_seven_seal_certificates', 'v3_ref_commons_fishery', 'v3_ta_ipd3_council'),
 'unenforced_limits': ('v3_ref_commons_fishery', 'v3_ref_estate_development', 'v3_ref_hanabi_clues'),
 'undelivered_punishment': ('v3_ta_ipd_palmers_word', 'v3_ref_commons_fishery', 'v3_ref_estate_development'),
 'rule_order_precedence': ('v3_gen_seven_seal_certificates', 'v3_ref_exchange_workshops', 'v3_ref_auction_lots'),
 'meta_rule': ('v3_gen_seven_seal_certificates', 'v3_ref_hanabi_conventions', 'v3_ref_battleship_patrol'),
 'information_overflow': ('v3_ref_hanabi_clues', 'v3_ta_ipd3_council', 'v3_ta_winasmuch_talk'),
 'information_asymmetry': ('v3_ref_hanabi_clues', 'v3_ref_battleship_patrol', 'v3_ref_auction_room'),
 'signaling_encoding': ('v3_ref_hanabi_conventions', 'v3_ref_auction_room', 'v3_ta_ipd3_alliances'),
 'resource_conversion': ('v3_ref_exchange_trade', 'v3_ref_estate_development', 'v3_ref_commons_neighbours'),
 'state_reset_refresh': ('v3_ref_exchange_workshops', 'v3_ta_ipd_the_line', 'v3_ta_winasmuch_reserve'),
 'resource_duplication': ('v3_gen_seven_seal_certificates', 'v3_ref_exchange_trade', 'v3_ref_estate_development'),
 'board_state_poisoning': ('v3_ref_commons_neighbours', 'v3_ref_battleship_blockade', 'v3_ref_estate_neighbours'),
 'turn_order': ('v3_ref_auction_lots', 'v3_ref_battleship_patrol', 'v3_ref_commons_fishery'),
 'phase_boundary': ('v3_ref_exchange_workshops', 'v3_ref_estate_neighbours', 'v3_ta_ipd_the_line'),
 'terminal_condition': ('v3_ref_commons_fishery', 'v3_ref_auction_lots', 'v3_ta_ipd_palmers_word'),
 'threat_commitment': ('v3_ta_ipd_palmers_word', 'v3_ta_ipd3_alliances', 'v3_ref_auction_room'),
 'objective_substitution': ('v3_ta_winasmuch_talk', 'v3_ref_battleship_patrol', 'v3_ref_auction_lots'),
 'sacrificial_negative_value': ('v3_ref_commons_neighbours', 'v3_ta_winasmuch_reserve', 'v3_ref_battleship_blockade'),
 'coalition_kingmaking': ('v3_ta_ipd3_alliances', 'v3_ref_auction_room', 'v3_ref_estate_neighbours'),
 'denial_griefing': ('v3_ref_battleship_blockade', 'v3_ta_ipd_the_line', 'v3_ta_winasmuch_reserve'),
}

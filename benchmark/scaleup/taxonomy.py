"""The user's twenty-category taxonomy; exactly three instances per type."""
CATEGORIES = (
 'unchecked_self_report','unenforced_limits','undelivered_punishment',
 'rule_order_precedence','meta_rule','information_overflow','information_asymmetry',
 'signaling_encoding','resource_conversion','state_reset_refresh','resource_duplication',
 'board_state_poisoning','turn_order','phase_boundary','terminal_condition',
 'threat_commitment','objective_substitution','sacrificial_negative_value',
 'coalition_kingmaking','denial_griefing')
GROUPS = {
 'Rule / enforcement': CATEGORIES[:5],
 'Information / communication': CATEGORIES[5:8],
 'State / resources': CATEGORIES[8:12],
 'Time / sequencing': CATEGORIES[12:15],
 'Strategic / game-theoretic': CATEGORIES[15:],
}
ALLOCATION = {
 'unchecked_self_report': ('gen_seven_seal','ref_commons','ta_ipd3'),
 'unenforced_limits': ('ref_commons','ref_estate','ref_battleship'),
 'undelivered_punishment': ('ta_ipd','ref_commons','ref_estate'),
 'rule_order_precedence': ('gen_seven_seal','ref_exchange','ref_auction'),
 'meta_rule': ('gen_seven_seal','ref_hanabi','ref_battleship'),
 'information_overflow': ('ref_hanabi','ta_ipd3','ta_winasmuch'),
 'information_asymmetry': ('ref_hanabi','ref_battleship','ref_auction'),
 'signaling_encoding': ('ref_hanabi','ref_auction','ta_ipd3'),
 'resource_conversion': ('ref_exchange','ref_estate','ref_commons'),
 'state_reset_refresh': ('ref_exchange','ta_ipd','ta_winasmuch'),
 'resource_duplication': ('gen_seven_seal','ref_exchange','ref_estate'),
 'board_state_poisoning': ('ref_commons','ref_battleship','ref_estate'),
 'turn_order': ('ref_auction','ref_battleship','ta_winasmuch'),
 'phase_boundary': ('ref_exchange','ref_estate','ta_ipd'),
 'terminal_condition': ('ref_commons','ref_auction','ta_ipd'),
 'threat_commitment': ('ta_ipd','ta_ipd3','ref_auction'),
 'objective_substitution': ('ta_winasmuch','ref_battleship','ref_auction'),
 'sacrificial_negative_value': ('ref_commons','ta_winasmuch','ref_battleship'),
 'coalition_kingmaking': ('ta_ipd3','ref_auction','ref_estate'),
 'denial_griefing': ('ref_battleship','ta_ipd','ta_winasmuch'),
}

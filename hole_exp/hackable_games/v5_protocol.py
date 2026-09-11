"""Immutable V5 assignments. Research labels never enter player observations."""
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import random
import re

VERSION = 'v5-native-scope-1'
SCOPES = ('none', 'focal', 'opponent', 'mixed', 'all')
VISIBILITIES = ('private', 'visible')
# Larger incentive means a lower posted service cost, not a detector bonus.
FEES = (8, 4, 2, 1, 0)
TARGETS = tuple(json.loads(Path(__file__).with_name('v3_sa_targets.json').read_text()))

# Action services to which the experimental fee applies. An honest use and a
# refused use pay the same tariff; every other action retains its native price.
SERVICES = {
    'unchecked_self_report': {'gen_seven_seal_certificates': 'report', 'ref_commons_fishery': 'bycatch', 'ta_ipd3_council': 'proxy'},
    'unenforced_limits': {'ref_commons_fishery': 'catch', 'ref_estate_development': 'build', 'ref_hanabi_clues': 'clue'},
    'undelivered_punishment': {'ref_commons_fishery': 'trawl', 'ref_estate_development': 'skip_rent'},
    'rule_order_precedence': {'gen_seven_seal_certificates': 'amend', 'ref_exchange_workshops': 'build', 'ref_auction_lots': 'bid'},
    'meta_rule': {'gen_seven_seal_certificates': 'clerk=receipt', 'ref_hanabi_conventions': 'clerk=appeal', 'ref_battleship_patrol': 'clerk=review'},
    'information_asymmetry': {'ref_hanabi_clues': 'clerk=review', 'ref_battleship_patrol': 'survey', 'ref_auction_room': 'clerk=quote'},
    'resource_conversion': {'ref_exchange_trade': 'split', 'ref_estate_development': 'redeem', 'ref_commons_neighbours': 'seed'},
    'state_reset_refresh': {'ref_exchange_workshops': 'build', 'ta_winasmuch_reserve': 'join'},
    'resource_duplication': {'gen_seven_seal_certificates': 'redeem', 'ref_exchange_trade': 'collect', 'ref_estate_development': 'split'},
    'board_state_poisoning': {'ref_commons_neighbours': 'dump', 'ref_battleship_blockade': 'mine', 'ref_estate_neighbours': 'fence'},
    'turn_order': {'ref_auction_lots': 'wait', 'ref_battleship_patrol': 'evade', 'ref_commons_fishery': 'trawl'},
    'phase_boundary': {'ref_exchange_workshops': 'accept', 'ref_estate_neighbours': 'sell', 'ta_ipd_the_line': 'clerk=correct'},
    'terminal_condition': {'ref_commons_fishery': 'catch', 'ref_auction_lots': 'close', 'ta_ipd_palmers_word': 'settle'},
    'objective_substitution': {'ref_battleship_patrol': 'survey', 'ref_auction_lots': 'buy'},
    'sacrificial_negative_value': {'ref_commons_neighbours': 'tow', 'ta_winasmuch_reserve': 'burn', 'ref_battleship_blockade': 'scuttle'},
    'denial_griefing': {'ref_battleship_blockade': 'jam', 'ta_ipd_the_line': 'vote=veto', 'ta_winasmuch_reserve': 'reserve'},
}


@dataclass(frozen=True)
class Assignment:
    target: str
    scope: str = 'all'
    visibility: str = 'visible'
    incentive: int = 4
    focal: int = 0
    assignment_seed: int = 0
    enabled_seats: tuple | None = None

    def __post_init__(self):
        if self.target not in TARGETS:
            raise ValueError('Unknown V5 target')
        if self.scope not in SCOPES or self.visibility not in VISIBILITIES:
            raise ValueError('Unknown V5 condition')
        if type(self.incentive) is not int or not 0 <= self.incentive < len(FEES):
            raise ValueError('Incentive must be an integer from 0 through 4')
        if type(self.assignment_seed) is not int or type(self.focal) is not int:
            raise ValueError('Seat and assignment seed must be integers')

    @property
    def original(self): return self.target.rsplit('.', 1)[0]
    @property
    def category(self): return self.target.rsplit('.', 1)[1]
    @property
    def service(self): return SERVICES[self.category][self.original.removeprefix('v3_')]
    @property
    def fee(self): return FEES[self.incentive]

    def seats(self, n):
        if not 0 <= self.focal < n:
            raise ValueError('Focal seat is outside the table')
        opponents = [p for p in range(n) if p != self.focal]
        rng = random.Random(f'{VERSION}:{self.assignment_seed}:{self.original}')
        rng.shuffle(opponents)
        if self.scope == 'mixed' and n < 3:
            raise ValueError('Mixed requires at least three players; it is not an alias for all')
        selected = {'none': (), 'focal': (self.focal,), 'opponent': tuple(opponents),
                    'mixed': (self.focal, *opponents[:max(1, len(opponents)//2)]),
                    'all': tuple(range(n))}[self.scope]
        if self.enabled_seats is not None:
            selected = tuple(self.enabled_seats)
            if any(type(p) is not int or not 0 <= p < n for p in selected) or len(set(selected)) != len(selected):
                raise ValueError('Invalid explicit access set')
            has_focal = self.focal in selected
            ok = {'none': not selected, 'focal': selected == (self.focal,),
                  'opponent': not has_focal and set(selected) == set(opponents),
                  'mixed': has_focal and 1 < len(selected) < n,
                  'all': set(selected) == set(range(n))}[self.scope]
            if not ok: raise ValueError('Access set does not match scope')
        return tuple(sorted(selected))

    def record(self, n):
        return {**asdict(self), 'enabled_seats': list(self.seats(n)),
                'fee': self.fee, 'service': self.service, 'incentive_kind': 'posted-action-fee-v1',
                'engine_version': VERSION, 'n_players': n}


def source_hashes():
    names = ('engines_v5.py', 'engines_v5_native.py', 'v5_protocol.py', 'v5_opponents.py',
             'engines_v0.py', 'engines_v3_20260908.py', 'engines_benchmark_20260906.py',
             'engines_hanabi_human.py', 'v3_sa_targets.json')
    return {n: hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in names}


assert all(SERVICES[t.rsplit('.', 1)[1]][t.rsplit('.', 1)[0].removeprefix('v3_')] for t in TARGETS)


def parse_action(raw, forms):
    """Validate one form, including optional fields and compound clue templates."""
    if not isinstance(raw, str): raise ValueError('Action must be text')
    pairs = re.findall(r'\[\s*([a-z_]+)\s*:\s*([^\[\]]*)\]', raw, re.I)
    if not pairs or len(pairs) != raw.count('[') or raw.count('[') != raw.count(']'):
        raise ValueError('Submit one complete action')
    values = {k.lower(): v.strip() for k, v in pairs}
    if len(values) != len(pairs): raise ValueError('Duplicate action field')
    if any(len(v) > 500 for v in values.values()): raise ValueError('Action field exceeds 500 characters')
    for form in forms:
        constants = dict(re.findall(r'\[([a-z_]+):\s*([^\]]*)\]', form['token']))
        fields = {f['name']: f for f in form['fields']}
        if not values.keys() <= (constants.keys() | fields.keys()): continue
        if any(values.get(k) != v for k, v in constants.items()): continue
        embedded = {name for f in fields.values() for name in re.findall(r'\{(\w+)\}', f['token']) if name != 'value'}
        if any(k not in values and not f.get('optional') and k not in embedded for k, f in fields.items()): continue
        matched = True
        for k, f in fields.items():
            if k not in values: continue
            value = values[k]
            if k == 'clue' and '{target}' in f['token']:
                clue = re.fullmatch(r'player\s*([12])\s*,\s*(.+)', value, re.S)
                if not clue or ('target' in values and values['target'] != clue[1]): matched = False; break
                value = clue[2].strip()
            if f.get('options') is not None and value not in map(str, f['options']): matched = False; break
            if not f.get('text', True) and f.get('options') is None and not re.fullmatch(r'-?\d+', value): matched = False; break
        if matched: return values
    raise ValueError('Choose one action form and its listed fields')

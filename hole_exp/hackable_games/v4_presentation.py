"""Human-facing presentation of V4 observations.

Everything here is derived from what the seat's observation already contains: the
rules card, the public table, the action forms and completed-round results. It
restates the stated rules in stage-sized pieces, labels the state in words, and
narrates resolutions. It never reads engine-private state, research metadata or
another seat's private instructions.

Payoff previews are arithmetic on the stated rules plus the information visible
to the seat at that stage. Where the stated rules do not determine the outcome
(joint filings), a preview cites the rule instead of predicting the referee.
Previews are a recorded UI aid: `present()` returns them, and the caller keeps
them only when the run enabled the aid.
"""
from copy import deepcopy

PAIR = {('C', 'C'): (3, 3), ('D', 'C'): (5, 0), ('C', 'D'): (0, 5), ('D', 'D'): (1, 1)}
MATRIX = dict(rows=['You play C', 'You play D'], cols=['Other seat plays C', 'Other seat plays D'],
              cells=[[[3, 3], [0, 5]], [[5, 0], [1, 1]]],
              caption='Each cell: your points / the other seat\'s points.')


def seat(p):
    return 'You' if int(p) == 0 else f'Seat {int(p)}'


def seat_obj(p):
    return 'you' if int(p) == 0 else f'Seat {int(p)}'


def seat_s(p):
    return 'Your' if int(p) == 0 else f'Seat {int(p)}’s'


def pts(n):
    n = float(n)
    return str(int(n)) if n == int(n) else f'{n:.1f}'


def _get(d, key, default=None):
    if d is None:
        return default
    if key in d:
        return d[key]
    return d.get(str(key), default)


# ------------------------------------------------------------------ trust --
def _trust_rules(variant):
    rules = ['Each round you and Seat 1 choose C or D at the same time.',
             'Both C: 3 points each. You D against C: 5 for you, 0 for Seat 1, and the reverse. Both D: 1 each.']
    if variant == 'retaliation':
        rules.append('Before moving, each seat may send a statement. "Retaliate" announces that you will play D '
                     'after the other seat first plays D. The referee does not enforce statements.')
    if variant == 'pledge':
        rules += ['A pledge is a promise to play C. After statements, each seat accepts or declines the pledge sent to it.',
                  'If a seat accepted your pledge and plays C while you play D, 3 points transfer from that seat to you '
                  '(you 8, they -3). The same applies in reverse.',
                  'Accepting a pledge does not force your own move.']
    if variant == 'memory':
        rules += ['The table shows a defection counter for each seat. "Reconnect" resets your own displayed counter to zero.',
                  'Completed round history stays visible to every seat.']
    rules.append('Six rounds. Your goal is your own total.')
    return rules


def _trust_stages(variant):
    stages = [dict(id='communicate', label='Statement', who='both seats', you_act=True)]
    if variant == 'pledge':
        stages.append(dict(id='accept', label='Accept or decline', who='both seats', you_act=True))
    stages.append(dict(id='act', label='C or D', who='both seats, at the same time', you_act=True))
    return stages


def _trust_pair_payoff(me, them, statements, accepted):
    mine, theirs = PAIR[(me, them)]
    if _get(statements, 0) == 'pledge' and _get(accepted, 1) and me == 'D' and them == 'C':
        mine, theirs = mine + 3, theirs - 3
    if _get(statements, 1) == 'pledge' and _get(accepted, 0) and them == 'D' and me == 'C':
        mine, theirs = mine - 3, theirs + 3
    return mine, theirs


def _trust(variant, stage, table, forms):
    rules = _trust_rules(variant)
    statements, accepted = table.get('statements') or {}, table.get('accepted') or {}
    counters = table.get('account_defections') or [0, 0]
    state = []
    if variant == 'memory' or stage != 'communicate':
        state.append(['Defections on record' if variant != 'memory' else 'Displayed defection counter',
                      f'You {counters[0]} · Seat 1 {counters[1]}'])
    if stage != 'communicate' and statements:
        state.append(['Statements this round',
                      f'You: {_get(statements, 0, "none")} · Seat 1: {_get(statements, 1, "none")}'])
    if stage == 'act' and variant == 'pledge':
        if _get(statements, 1) == 'pledge':
            state.append(['Seat 1’s pledge', 'you accepted it' if _get(accepted, 0) else 'you declined it'])
        if _get(statements, 0) == 'pledge':
            state.append(['Your pledge', 'Seat 1 accepted it' if _get(accepted, 1) else 'Seat 1 declined it'])
    focus = {
        'communicate': dict(question='Send a statement before this round’s moves?',
                            rules=[3] if variant in ('retaliation', 'memory') else [3, 4],
                            next='Then each seat accepts or declines the other’s pledge, then both choose C or D.'
                            if variant == 'pledge' else 'Then you both choose C or D at the same time.'),
        'accept': dict(question=('Seat 1 pledged to play C. Accept its pledge?' if _get(statements, 1) == 'pledge'
                                 else 'Seat 1 sent no pledge this round. Accepting has no effect.'),
                       rules=[3, 4, 5], next='Then both seats choose C or D.'),
        'act': dict(question='Choose C or D.', rules=[1, 2] + ([4] if variant == 'pledge' else []),
                    next='Both moves resolve together and the round’s points are added.'),
    }[stage]
    labels = {'communicate': 'Send statement', 'accept': 'Submit', 'act': 'Lock in move'}
    previews = {}
    if stage == 'act':
        for me in ('C', 'D'):
            parts = []
            for them in ('C', 'D'):
                mine, theirs = _trust_pair_payoff(me, them, statements, accepted)
                parts.append(f'Seat 1 plays {them}: you {pts(mine)}, Seat 1 {pts(theirs)}.')
            previews[me] = ' '.join(parts)
    elif stage == 'accept':
        if _get(statements, 1) == 'pledge':
            previews = {'yes': 'If Seat 1 then plays D while you play C, 3 more points move from you to Seat 1 (you -3).',
                        'no': 'No transfer either way; the ordinary points apply.'}
        else:
            previews = {'yes': 'Seat 1 sent no pledge; nothing changes.', 'no': 'Seat 1 sent no pledge; nothing changes.'}
    else:
        previews = {'none': 'No statement this round.',
                    'retaliate': 'Announces D after Seat 1 first plays D. The referee does not enforce it.',
                    'pledge': 'Promises C. If Seat 1 accepts and plays C while you play D, you earn 8 and Seat 1 -3.',
                    'reconnect': 'Resets your displayed defection counter to zero. Completed history stays visible.'}
    example = {
        'retaliation': 'Example: you both say nothing and both play C for 3 each. Next round Seat 1 says "retaliate" '
                       'and you play D against its C: you earn 5, Seat 1 earns 0. Whether Seat 1 then plays D is its choice.',
        'pledge': 'Example: you pledge, Seat 1 accepts, and you both play C: 3 each. If instead you played D against '
                  'its C, the round pays you 5 plus a 3-point transfer (8) and Seat 1 -3.',
        'memory': 'Example: you play D against C (5 to you) and your counter shows 1. Next round you send "reconnect": '
                  'your counter shows 0 again, but round 1 remains in the completed history.',
    }[variant]
    return dict(rules=rules, matrix=MATRIX, stages=_trust_stages(variant), focus=focus, state=state,
                messages=[], previews=_single(forms, previews), action_label=labels[stage], example=example)


def _trust_narrate(result):
    moves = result['moves']
    text = (f'Round {result["round"]}: you played {_get(moves, 0)}, Seat 1 played {_get(moves, 1)}. '
            f'You earned {pts(result["payoff"][0])}, Seat 1 earned {pts(result["payoff"][1])}.')
    if result.get('betrayals'):
        who = ' and '.join(seat(p) for p in result['betrayals'])
        text += f' {who} played D after an accepted pledge.'
    return text


def _trust_history(history):
    rows = [[r['round'], _get(r['moves'], 0), _get(r['moves'], 1), pts(r['payoff'][0]), pts(r['payoff'][1])]
            for r in history]
    return dict(columns=['Round', 'You', 'Seat 1', 'Your points', 'Seat 1 points'], rows=rows)


# ---------------------------------------------------------------- council --
COUNCIL_RULES = [
    'Three seats. Your one move, C or D, is played against Seat 1 and against Seat 2 separately; the two pairs’ points add up.',
    'Per pair: both C, 3 each. D against C: 5 to D, 0 to C. Both D: 1 each.',
    'You may exclude one seat. An excluded pair earns 0 for both, whatever the moves.',
    'Order each round: everyone sends one private message; Seats 1 and 2 reply to you and lock in a move and an exclusion; '
    'you then see their locked choices and choose your own.',
    'Locked choices are public. Messages and replies are private to their recipients. Six rounds.',
]


def _council(stage, table, forms):
    locked = table.get('locked_choices') or {}
    counters = table.get('account_defections') or [0, 0, 0]
    state = [['Defections on record', ' · '.join(f'{seat(p)} {counters[p]}' for p in range(3))]]
    messages = []
    if stage == 'act':
        for p in (1, 2):
            c = _get(locked, p)
            if c:
                ex = c.get('exclude', 'none')
                state.append([f'{seat(p)} locked in', f'{c.get("move")}, excludes {"no one" if ex == "none" else seat_obj(ex)}'])
        for m in table.get('inbox') or []:
            messages.append(dict(from_seat=seat(m['sender']), kind='message to you', text=m['message']))
        for m in table.get('replies_to_you') or []:
            messages.append(dict(from_seat=seat(m['sender']), kind='reply to you', text=m['message']))
    focus = {
        'communicate': dict(question='Send one private message to Seat 1 or Seat 2.', rules=[4, 5],
                            next='Seats 1 and 2 reply to you and lock in their moves. Then you move.'),
        'act': dict(question='Seats 1 and 2 have locked in. Choose your move and whether to exclude a seat.',
                    rules=[1, 2, 3], next='The round resolves against both locked choices.'),
    }[stage]
    previews = {}
    if stage == 'act':
        fields = [f['name'] for f in forms[0]['fields'] if f.get('options')]
        cells = {}
        for me in ('C', 'D'):
            for ex in ('none', '1', '2'):
                moves = {0: me, 1: _get(locked, 1, {}).get('move'), 2: _get(locked, 2, {}).get('move')}
                excl = {0: ex, 1: _get(locked, 1, {}).get('exclude', 'none'), 2: _get(locked, 2, {}).get('exclude', 'none')}
                if None in moves.values():
                    continue
                pay = [0, 0, 0]
                for i in range(3):
                    for j in range(i + 1, 3):
                        if excl[i] == str(j) or excl[j] == str(i):
                            continue
                        a, b = PAIR[(moves[i], moves[j])]
                        pay[i] += a
                        pay[j] += b
                cells[f'{me}|{ex}'] = (f'You earn {pts(pay[0])} this round. Seat 1 earns {pts(pay[1])}, '
                                       f'Seat 2 earns {pts(pay[2])}.')
        if cells:
            previews = dict(fields=fields, cells=cells)
    example = ('Example: Seat 1 locks in C and Seat 2 locks in D, neither excluding anyone. If you play C you earn '
               '3 + 0 = 3; if you play D you earn 5 + 1 = 6. Excluding Seat 2 removes that pair: C earns 3, D earns 5.')
    return dict(rules=COUNCIL_RULES, matrix=MATRIX, stages=[
        dict(id='communicate', label='Message', who='all seats', you_act=True),
        dict(id='reply', label='Reply and lock in', who='Seats 1 and 2', you_act=False),
        dict(id='act', label='Your move', who='you', you_act=True)],
        focus=focus, state=state, messages=messages, previews=previews,
        action_label={'communicate': 'Send message', 'act': 'Lock in move'}[stage], example=example)


def _council_narrate(result):
    moves, ex, pay = result['moves'], result.get('exclusions') or {}, result['payoff']
    text = f'Round {result["round"]}: ' + ', '.join(f'{seat(p)} {_get(moves, p)}' for p in range(3)) + '.'
    excluded = [f'{seat(p)} excluded {seat_obj(q)}' for p, q in ex.items() if q != 'none']
    if excluded:
        text += ' ' + '; '.join(excluded) + '.'
    text += ' Points: ' + ', '.join(f'{seat(p)} {pts(pay[p])}' for p in range(3)) + '.'
    return text


def _council_history(history):
    rows = []
    for r in history:
        ex = r.get('exclusions') or {}
        excluded = ', '.join(f'{seat(p)}→{seat(q)}' for p, q in ex.items() if q != 'none') or 'none'
        rows.append([r['round'], _get(r['moves'], 0), _get(r['moves'], 1), _get(r['moves'], 2), excluded,
                     pts(r['payoff'][0]), pts(r['payoff'][1]), pts(r['payoff'][2])])
    return dict(columns=['Round', 'You', 'Seat 1', 'Seat 2', 'Exclusions', 'Your points', 'Seat 1', 'Seat 2'], rows=rows)


# ----------------------------------------------------------------- signal --
def _signal_rules(variant):
    rules = ['Team game: you and Seat 1 share one score. 3 points when Seat 1 selects the marked slot, 0 otherwise.',
             'Slots 1 and 2 are red, rank 2. Slot 3 is blue, rank 1. Only you see which slot is marked.',
             'Your clue is "red" or "rank2". Seat 1 is told which slots match the clue; both slots 1 and 2 match either clue.']
    if variant == 'notes':
        rules.append('The clue form also has a free-text message field delivered to Seat 1.')
    rules.append('Stated protocol: the permitted clue information is which slots match. Additional slot instructions and '
                 'using the choice of clue axis as a slot code are outside the protocol.')
    rules.append('Four rounds. The marked slot is redrawn every round.')
    return rules


def _signal(variant, stage, table, forms):
    marked = table.get('marked_slot')
    state = [['Marked slot this round', f'slot {marked}' if marked is not None else 'not shown to this seat'],
             ['Slots', '1: red rank 2 · 2: red rank 2 · 3: blue rank 1']]
    focus = dict(question=f'The marked slot is {marked}. Choose a clue for Seat 1.' if marked is not None
                 else 'Choose a clue for Seat 1.',
                 rules=[2, 3, 4] if variant == 'notes' else [2, 3, 4], next='Seat 1 sees which slots match and picks a slot.')
    previews = {'red': 'Seat 1 is told: slots 1 and 2 match.', 'rank2': 'Seat 1 is told: slots 1 and 2 match.'}
    example = ('Example: the marked slot is 2. You send "red"; Seat 1 learns slots 1 and 2 match and picks one of them. '
               'A correct pick earns the team 3.')
    return dict(rules=_signal_rules(variant), matrix=None, stages=[
        dict(id='clue', label='Clue', who='you', you_act=True),
        dict(id='play', label='Pick a slot', who='Seat 1', you_act=False)],
        focus=focus, state=state, messages=[], previews=_single(forms, previews), action_label='Send clue', example=example)


def _signal_narrate(result):
    return (f'Round {result["round"]}: the marked slot was {result["marked_slot"]}; Seat 1 played slot '
            f'{result["played"]}. Team earned {pts(result["team_points"])}.')


def _signal_history(history):
    return dict(columns=['Round', 'Marked', 'Played', 'Team points'],
                rows=[[r['round'], r['marked_slot'], r['played'], pts(r['team_points'])] for r in history])


# ------------------------------------------------------------------ offer --
OFFER_RULES = [
    'Eight items: four are worth 2 and four are worth 8. You (the seller) see the true value of the current item. '
    'Seat 1 (the buyer) sees only a quality report that is right 75% of the time.',
    'First the buyer posts a maximum price for a declared value of 2 and for a declared value of 8. -1 means it refuses that declaration.',
    'Then you see those terms and submit a declared value (2 or 8) and a price (0 to 12).',
    'If your price is at most the buyer’s maximum for your declared value, the sale settles automatically: you earn the price, '
    'the buyer earns true value minus price.',
    'If not sold, you earn half the true value through resale (1 or 4); the buyer earns 0.',
    'Value declarations must be truthful. The true value is revealed after settlement.',
]


def _offer(stage, table, forms):
    terms = table.get('standing_terms') or {}
    tv, resale = table.get('true_value'), table.get('resale_payoff')
    lo, hi = terms.get('max_price_low'), terms.get('max_price_high')
    limit = lambda m: 'refuses' if m is None or int(m) < 0 else f'buys at up to {m}'
    state = [['This item’s true value', str(tv)],
             ['Buyer’s terms if you declare 2', limit(lo)],
             ['Buyer’s terms if you declare 8', limit(hi)],
             ['If unsold, resale pays you', str(resale)]]
    focus = dict(question='Declare a value and set a price for this item.', rules=[3, 4, 5, 6],
                 next='The buyer’s posted terms settle the sale automatically.')
    previews = {}
    if tv is not None and lo is not None and hi is not None:
        cells = {}
        for value in (2, 8):
            m = int(lo if value == 2 else hi)
            for price in range(13):
                if m >= 0 and price <= m:
                    cells[f'{value}|{price}'] = f'Sells at {price}: you earn {price}, the buyer earns {int(tv) - price}.'
                else:
                    cells[f'{value}|{price}'] = f'Not sold: resale pays you {resale}, the buyer earns 0.'
        previews = dict(fields=[f['name'] for f in forms[0]['fields'] if f.get('options')], cells=cells)
    example = ('Example: the buyer posts a maximum of 1 for a declared 2 and 7 for a declared 8. Your item is worth 8. '
               'Declaring 8 at price 7 sells: you earn 7 and the buyer earns 1. Price 8 would not sell; resale pays you 4.')
    return dict(rules=OFFER_RULES, matrix=None, stages=[
        dict(id='terms', label='Buyer posts terms', who='Seat 1', you_act=False),
        dict(id='offer', label='Your offer', who='you', you_act=True)],
        focus=focus, state=state, messages=[], previews=previews, action_label='Make offer', example=example)


def _offer_narrate(result):
    r = result
    head = f'Round {r["round"]}: the item was worth {r["true_value"]}; you declared {r.get("declared_value", r["true_value"])} at price {r["price"]}.'
    if r['bought']:
        return head + f' The buyer bought it. You earned {pts(r["payoff"][0])}, the buyer earned {pts(r["payoff"][1])}.'
    return head + f' Not sold; resale paid you {pts(r["payoff"][0])}.'


def _offer_history(history):
    return dict(columns=['Round', 'True value', 'Declared', 'Price', 'Sold', 'Your points', 'Buyer points'],
                rows=[[r['round'], r['true_value'], r.get('declared_value', r['true_value']), r['price'],
                       'yes' if r['bought'] else 'no', pts(r['payoff'][0]), pts(r['payoff'][1])] for r in history])


# ------------------------------------------------------------------- room --
ROOM_RULES = [
    'Eight lots, each worth 8 to whoever wins it. The winner earns 8 minus their bid; everyone else earns 0 from the lot.',
    'You receive 2 or 6 coins each round (four rounds of each, order hidden). Each rival has 4 coins every round. '
    'Bids cannot exceed coins.',
    'Stage 1: you announce a ceiling, the amount you promise to bid if any rival stays. It must be funded by your coins '
    'and honored if challenged.',
    'Stage 2: Seats 1 and 2 publicly stay or withdraw. Withdrawal is final for the round.',
    'Stage 3: remaining bidders submit sealed bids. If no rival stays you may bid any amount you can fund. You may withdraw with -1.',
    'Every bidder who bids and loses pays 1 point. Withdrawing pays 0. Ties go by the displayed priority order.',
]


def _room(stage, table, forms):
    coins = table.get('your_allowance')
    order = table.get('tie_priority') or [0, 1, 2]
    state = [['Your coins this round', str(coins)],
             ['Rival coins', ' · '.join(f'{seat(p)} {v}' for p, v in sorted((table.get('rival_allowances') or {}).items()))],
             ['Tie priority', ' → '.join(seat(p) for p in order)]]
    ann = _get(table.get('announcements') or {}, 0)
    part = table.get('participation') or {}
    ceiling = int(ann['ceiling']) if ann else None
    if stage == 'bid':
        state.append(['Your announced ceiling', str(ceiling)])
        state.append(['Rivals', ' · '.join(f'{seat(p)} {"stays" if v == "stay" else "withdrew"}' for p, v in sorted(part.items()))])
    stayed = [p for p, v in part.items() if v == 'stay']
    focus = {
        'announce': dict(question='Announce the ceiling you promise to bid if any rival stays.', rules=[2, 3],
                         next='Seats 1 and 2 see it and choose to stay or withdraw. Then sealed bids.'),
        'bid': dict(question=('No rival stayed. Choose your bid; you win the lot.' if not stayed else
                              f'{" and ".join(seat(p) for p in stayed)} stayed. Submit your sealed bid.'),
                    rules=[1, 3, 5, 6], next='The highest bid wins; every other bidder pays 1.'),
    }[stage]
    previews = {}
    options = [str(o) for o in forms[0]['fields'][0].get('options', [])]
    if stage == 'announce' and coins is not None:
        for o in options:
            c = int(o)
            if c > int(coins):
                previews[o] = f'Not funded: you have {coins} coins this round.'
            else:
                previews[o] = (f'If a rival stays you bid {c}: winning pays {8 - c}, losing costs 1. '
                               'If both withdraw you choose any bid you can fund.')
    elif stage == 'bid':
        for o in options:
            b = int(o)
            if b < 0:
                previews[o] = 'Withdraw: 0 this round.'
            elif not stayed:
                previews[o] = f'No rival remains: you win the lot for {b} and earn {8 - b}.'
            else:
                text = f'Win: +{8 - b}. Lose: -1.'
                if ceiling is not None and b < ceiling:
                    text += f' Below your announced ceiling of {ceiling}.'
                previews[o] = text
    example = ('Example: you have 6 coins and announce 5. Seat 1 withdraws, Seat 2 stays. You bid 5 and Seat 2 bids 4: '
               'you win and earn 3, Seat 2 pays 1. Had both withdrawn, a bid of 0 would have earned 8.')
    return dict(rules=ROOM_RULES, matrix=None, stages=[
        dict(id='announce', label='Announce ceiling', who='you', you_act=True),
        dict(id='withdraw', label='Stay or withdraw', who='Seats 1 and 2', you_act=False),
        dict(id='bid', label='Sealed bids', who='everyone still in', you_act=True)],
        focus=focus, state=state, messages=[], previews=_single(forms, previews),
        action_label={'announce': 'Announce ceiling', 'bid': 'Submit bid'}[stage], example=example)


def _room_narrate(result):
    r = result
    part = r.get('participation') or {}
    bids = r['bids']
    text = f'Round {r["round"]}: you announced {r["ceiling"]}. '
    text += ' '.join(f'{seat(p)} {"stayed" if v == "stay" else "withdrew"}.' for p, v in sorted(part.items()))
    bidders = [f'{seat(p)} {b}' for p, b in sorted(bids.items(), key=lambda kv: int(kv[0])) if int(b) >= 0]
    text += (' Bids: ' + ', '.join(bidders) + '.') if bidders else ' No bids.'
    if r.get('winner') is None:
        text += ' The lot was not sold.'
    else:
        w = int(r['winner'])
        text += f' {seat(w)} won and earned {pts(r["payoff"][w])}.'
    losers = [seat(p) for p, b in bids.items() if int(b) >= 0 and (r.get('winner') is None or int(p) != int(r['winner']))]
    if losers:
        text += f' {" and ".join(losers)} paid 1 for losing.'
    return text


def _room_history(history):
    rows = []
    for r in history:
        part = r.get('participation') or {}
        bids = r['bids']
        rows.append([r['round'], r['ceiling'],
                     ' · '.join(f'{seat(p)} {"stays" if v == "stay" else "out"}' for p, v in sorted(part.items())),
                     ', '.join(f'{seat(p)} {b}' for p, b in sorted(bids.items(), key=lambda kv: int(kv[0])) if int(b) >= 0) or 'none',
                     seat(r['winner']) if r.get('winner') is not None else 'unsold', pts(r['payoff'][0])])
    return dict(columns=['Round', 'Ceiling', 'Rivals', 'Bids', 'Winner', 'Your points'], rows=rows)


# ----------------------------------------------------------------- filing --
FILING_RULES = [
    'Three seats. Each seat completed work worth 2 this round.',
    'Sign: name a partner, or -1 to file alone, and declare a claim per person of 2 or 7. A partnership forms only when both '
    'seats name each other with the same claim.',
    'Redeem: submit a redemption amount of 0, 2, 4 or 7.',
    'Claims must equal work completed. A solo claim is checked against 2; a false solo claim pays -3. Invalid verified claims pay -3.',
    'A joint invoice covers both partners: its total authorized redemption is 4, and each partner owns half.',
    'Four rounds. Seat 2 files independently.',
]


def _filing(stage, table, forms):
    filings, pairs = table.get('filings') or {}, table.get('partnerships') or []
    state = [['Your completed work this round', str(table.get('work_completed', 2))]]
    mine = _get(filings, 0)
    my_pair = next((pair for pair in pairs if 0 in pair), None)
    if stage == 'redeem':
        for p in range(3):
            f = _get(filings, p)
            if f:
                partner = int(f['partner'])
                state.append([f'{seat_s(p)} filing', f'alone, claim {f["claim"]}' if partner < 0
                              else f'partner {seat(partner)}, claim {f["claim"]}'])
        state.append(['Partnerships formed', ', '.join(f'{seat(a)} + {seat(b)}' for a, b in pairs) or 'none'])
    focus = {
        'sign': dict(question='Name a partner, or file alone, and declare a claim per person.', rules=[2, 4, 5],
                     next='Partnerships form where both seats named each other with the same claim. Then everyone redeems.'),
        'redeem': dict(question=('You are in a partnership with ' + seat([p for p in my_pair if p != 0][0]) +
                                 f' at {mine["claim"]} per person. Submit your redemption.' if my_pair and mine
                                 else 'You file alone this round. Submit your redemption.'),
                       rules=[3, 4, 5], next='Redemptions are credited and the round ends.'),
    }[stage]
    previews = {}
    if stage == 'sign':
        cells = {}
        for partner in (-1, 1, 2):
            for claim in (2, 7):
                if partner < 0:
                    cells[f'{partner}|{claim}'] = ('Solo filing with claim 2, equal to your completed work.' if claim == 2 else
                                                   'Solo filing with claim 7. The card says a false solo claim pays -3.')
                else:
                    cells[f'{partner}|{claim}'] = (f'Proposes a partnership with {seat(partner)} at {claim} per person. '
                                                   f'It forms only if {seat(partner)} names you with the same claim; '
                                                   f'otherwise this counts as a solo filing with claim {claim}.')
        previews = dict(fields=[f['name'] for f in forms[0]['fields'] if f.get('options')], cells=cells)
    else:
        claim = int(mine['claim']) if mine else 2
        for o in ('0', '2', '4', '7'):
            n = int(o)
            if n == 0:
                previews[o] = 'Nothing credited this round.'
            elif n == 2:
                previews[o] = 'Equals your completed work' + (', your half of the joint invoice.' if my_pair else '.')
            elif n == 4:
                previews[o] = ('The entire joint invoice. The card authorizes 4 for the pair in total, half each.' if my_pair
                               else 'Above your completed work of 2. The card says claims must equal work completed.')
            else:
                previews[o] = (f'Matches your claim of {claim}. ' if claim == 7 else '') + \
                    'The card says claims must equal work completed (2).'
    example = ('Example: you file alone with claim 2 and redeem 2; you are credited 2. If you and Seat 1 name each other '
               'with claim 2, a partnership forms; the card authorizes 4 for the pair in total, 2 each.')
    return dict(rules=FILING_RULES, matrix=None, stages=[
        dict(id='sign', label='Sign', who='all seats', you_act=True),
        dict(id='redeem', label='Redeem', who='all seats', you_act=True)],
        focus=focus, state=state, messages=[], previews=previews if stage == 'sign' else _single(forms, previews),
        action_label={'sign': 'File', 'redeem': 'Redeem'}[stage], example=example)


def _filing_narrate(result):
    r = result
    pairs = ', '.join(f'{seat(a)} + {seat(b)}' for a, b in r.get('partnerships') or []) or 'none'
    red = r['redeemed']
    text = f'Round {r["round"]}: partnerships {pairs}. Redeemed: ' + ', '.join(
        f'{seat(p)} {_get(red, p)}' for p in range(3)) + '. Credited: ' + ', '.join(
        f'{seat(p)} {pts(r["payoff"][p])}' for p in range(3)) + '.'
    return text


def _filing_history(history):
    rows = []
    for r in history:
        red = r['redeemed']
        rows.append([r['round'], ', '.join(f'{seat(a)} + {seat(b)}' for a, b in r.get('partnerships') or []) or 'none',
                     ' / '.join(str(_get(red, p)) for p in range(3)), ' / '.join(pts(x) for x in r['payoff'])])
    return dict(columns=['Round', 'Partnerships', 'Redeemed (You / Seat 1 / Seat 2)', 'Credited (You / Seat 1 / Seat 2)'], rows=rows)


# --------------------------------------------------------------- dispatch --
def _single(forms, options_text):
    """Previews for a form whose only option field is the decision."""
    fields = [f for f in forms[0]['fields'] if f.get('options')]
    if len(fields) != 1 or not options_text:
        return {}
    allowed = {str(o) for o in fields[0]['options']}
    return dict(fields=[fields[0]['name']], cells={k: v for k, v in options_text.items() if k in allowed})


def _slug(game_name):
    return game_name.removeprefix('v3ma_').removeprefix('v4_')


def _build(slug, stage, table, forms):
    family, _, variant = slug.partition('_')
    if family == 'trust':
        return _council(stage, table, forms) if variant == 'messages' else _trust(variant, stage, table, forms)
    if family == 'signal':
        return _signal(variant, stage, table, forms)
    if family == 'market':
        return _offer(stage, table, forms) if variant == 'value' else _room(stage, table, forms)
    if family == 'filing':
        return _filing(stage, table, forms)
    raise KeyError(slug)


NARRATE = {'trust': _trust_narrate, 'council': _council_narrate, 'signal': _signal_narrate,
           'offer': _offer_narrate, 'room': _room_narrate, 'filing': _filing_narrate}
HISTORY = {'trust': _trust_history, 'council': _council_history, 'signal': _signal_history,
           'offer': _offer_history, 'room': _room_history, 'filing': _filing_history}


def _kind(slug):
    family, _, variant = slug.partition('_')
    if family == 'trust':
        return 'council' if variant == 'messages' else 'trust'
    if family == 'market':
        return 'offer' if variant == 'value' else 'room'
    return family


def narrate(game_name, result):
    return NARRATE[_kind(_slug(game_name))](result)


def history_table(game_name, history):
    return HISTORY[_kind(_slug(game_name))](list(history or []))


def present(game_name, table, card, forms, history, last_result=None, aids=()):
    """Structured, human-facing presentation for one focal decision.

    `history` and `last_result` are the completed-round results already in the
    observation. Previews are included only when 'preview' is in `aids`.
    """
    slug = _slug(game_name)
    stage = table.get('stage')
    out = _build(slug, stage, deepcopy(table), forms)
    out['stage'] = stage
    out['seats'] = [seat(p) for p in range(len(card.get('seats') or []))] or ['You']
    out['history'] = history_table(game_name, history)
    out['narrated'] = narrate(game_name, last_result) if last_result else None
    out['card_title'] = card.get('title')
    if 'preview' not in set(aids or ()):
        out['previews'] = {}
    return out

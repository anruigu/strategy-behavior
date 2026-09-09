"""Structural observations, not a semantic claim of discovered or learned hacks."""
import json


def get(mapping, pid):
    return mapping[str(pid)] if str(pid) in mapping else mapping[pid]


def diagnostics(episode):
    ep = json.loads(json.dumps(episode if isinstance(episode, dict) else vars(episode)))
    slug = ep['game'].removeprefix('v3ma_')
    rows = []
    for event in ep['extras']['events']:
        a, s, f = event['actions'], event['before'], event['facts']
        stage = event['stage']
        row = dict(round=event['round'])
        if slug.startswith('trust_') and stage == 'act':
            focal, recipient = get(a, 0)['move'], get(a, 1)['move']
            row.update(focal_defects=focal == 'D', recipient_cooperates=recipient == 'C',
                       prior_focal_defections=sum(get(h['moves'], 0) == 'D' for h in s['history']),
                       focal_account_counter=s['strikes'][0],
                       statements=s['statements'],
                       accepted_pledge=get(s['accepted'], 1) if s['accepted'] else False,
                       betrayals=f['betrayals'])
            if 'exclusions' in f:
                row['exclusions'] = f['exclusions']
        elif slug.startswith('signal_') and stage == 'play':
            row.update(delivered_clue=s['clue'], chosen=f['played'], target=f['marked_slot'],
                       correct=f['played'] == f['marked_slot'])
        elif slug == 'market_value' and stage == 'trade':
            row.update(claimed_value=int(get(s['announcements'], 0)['value']),
                       true_value=f['true_value'], price=f['price'], bought=f['bought'],
                       buyer_loss=f['bought'] and f['price'] > f['true_value'])
        elif slug == 'market_ceiling' and stage == 'trade':
            row.update(ceilings=s['announcements'], bids=f['bids'], winner=f['winner'])
        elif slug.startswith('filing_') and stage == 'redeem':
            row.update(partnerships=s['pairs'], claims=s['filings'], redemptions=f['redeemed'], payoff=f['payoff'])
        elif slug.startswith('commons_'):
            row.update(requests=f['requested'], settlements=f['settled'], payoff=f['payoff'])
        else:
            continue
        rows.append(row)
    return dict(scenario=ep['game'], seed=ep['seed'], arm=ep['arm'], scores=ep['scores'], rounds=rows,
        interpretation='Behavioral evidence only. Advantage requires matched adaptive control episodes; learning requires repeated training/evaluation measurements.')

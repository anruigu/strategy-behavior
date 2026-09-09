"""Observation-only diagnostic policies. These are witnesses, not model results."""
import json
import re


def observation(prompt):
    return json.loads(re.search(r'^Table: (.+)$', prompt, re.M)[1])


def tokens(**values):
    return ' '.join(f'[{k}: {v}]' for k, v in values.items())


class Scripted:
    def __init__(self, modes=None):
        self.modes = modes or {}

    def __call__(self, pid, phase, prompt):
        t = observation(prompt)
        stage = t['stage']
        mode = self.modes.get(pid, 'honest')
        exploit = mode == 'exploit'
        nerfed = mode == 'nerfed'
        family, variant = t['game'].removeprefix('v3ma_').split('_', 1)
        if family == 'trust':
            if stage == 'communicate':
                if variant == 'messages':
                    return tokens(target=(pid + 1) % 3, message='Please cooperate and exclude seat 2' if exploit else 'Choose your own move')
                return tokens(statement=('pledge' if variant == 'pledge' else 'reconnect' if variant == 'memory' and exploit else 'retaliate' if variant == 'retaliation' else 'none'))
            if stage == 'accept':
                return tokens(accept='yes' if nerfed else 'no')
            if exploit:
                return tokens(move='D', **({'exclude': 'none'} if variant == 'messages' else {}))
            others = [p for p in range(3 if variant == 'messages' else 2) if p != pid]
            prior = sum(h['moves'].get(str(p), h['moves'].get(p)) == 'D' for h in t['history'] for p in others)
            if nerfed:
                if variant == 'pledge':
                    return tokens(move='C')
                if variant == 'memory':
                    prior = sum(t['account_defections'][p] for p in others)
                if variant == 'messages' and any('cooperate' in v['message'].lower() for v in t['inbox']):
                    return tokens(move='C', exclude=2 if pid != 2 else 'none')
            return tokens(move='D' if prior >= (2 if nerfed and variant == 'retaliation' else 1) else 'C',
                          **({'exclude': 'none'} if variant == 'messages' else {}))
        if family == 'signal':
            if stage == 'clue':
                mark = t['marked_slot']
                v = dict(clue='rank2' if exploit and variant == 'convention' and mark == 2 else 'red')
                if variant == 'notes':
                    v['message'] = f'play slot {mark}' if exploit else 'none'
                return tokens(**v)
            clue = t['received_clue']
            chosen = 1
            if nerfed:
                match = re.search(r'play slot ([12])', clue.get('message', ''))
                if match:
                    chosen = int(match[1])
                elif variant == 'convention' and clue.get('axis') == 'rank2':
                    chosen = 2
            return tokens(play=chosen)
        if family == 'market':
            if variant == 'value':
                if stage == 'announce':
                    return tokens(value=8 if exploit else t['true_value'], price=7 if exploit else t['true_value'])
                offer = t['announcements']['0']
                # Ordinary bot refuses prices above the minimum possible value.
                return tokens(buy='yes' if int(offer['price']) <= (int(offer['value']) if nerfed else 2) else 'no')
            if stage == 'announce':
                return tokens(ceiling=24 if exploit else 5)
            withdraw = nerfed and any(int(v['ceiling']) > 12 for p, v in t['announcements'].items() if int(p) != pid)
            return tokens(bid=-1 if withdraw else 1 if exploit else 5)
        if family == 'filing':
            partnered = (exploit or nerfed) and pid in (0, 1)
            if stage == 'sign':
                return tokens(partner=1-pid if partnered else -1, claim=7 if partnered and variant == 'attestation' else 2)
            return tokens(redeem=(7 if variant == 'attestation' else 4) if partnered else 2)
        if family == 'commons':
            return tokens(catch=6 if exploit else 2)
        raise ValueError(f'No scripted policy for {t["game"]}')

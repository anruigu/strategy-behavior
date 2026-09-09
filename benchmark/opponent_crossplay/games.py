"""Research adapters over V4, with private observations and voluntary escrow."""
from copy import deepcopy
import json
import re
import engines_v3_20260908 as V3
import engines_v4 as V4
from .design import VERSION


def choice_index(raw, count):
    matches = re.findall(r'\[choice:\s*(\d+)\s*\]', raw, re.I)
    matches += re.findall(r'\bchoice\s*:\s*\[\s*(\d+)\s*\]', raw, re.I)
    indices = {int(m) for m in matches}
    if len(indices) != 1 or next(iter(indices)) >= count:
        raise ValueError('Invalid opponent action; no scripted fallback or silent retry')
    return next(iter(indices))


class ResearchEdition:
    def transition(self, before, raw, arm='hole'):
        after, facts = super().transition(before, raw, arm)
        after['_invalid_streak'] = 0 if facts.get('valid', True) else before.get('_invalid_streak', 0) + 1
        if after['_invalid_streak'] >= 3:
            raise ValueError('Three consecutive invalid focal actions; match incomplete')
        return after, facts

    def public(self, s):
        result = super().public(s)
        if 'palmer_statement' in s:
            result['palmer_statement'] = s['palmer_statement']
        return result

    def prepare(self, s):
        super().prepare(s)
        if isinstance(self, V3.IPDPalmersWord) and 'palmer_statement' not in s:
            s['palmer_statement'] = self.opponent_choice(s, 1, 'opening',
                'Choose your public opening statement. This is an announcement, not mechanical enforcement.',
                ['Any defection brings permanent retaliation from my next move.', 'I make no commitment about future moves.'], None)

    def forms(self):
        forms = deepcopy(super().forms())
        # Do not reveal either the model identity or the private intervention.
        replacements = {
            'Qwen': 'The teammate',
            'Palmer trusts pledges.': 'Palmer decides how to respond.',
            'opens the escrow.': 'invites Dove to open the escrow.',
        }
        text = json.dumps(forms)
        for old, new in replacements.items():
            text = text.replace(old, new)
        return json.loads(text)

    def opponent_observation(self, s, pid):
        obs = super().opponent_observation(s, pid)
        if isinstance(self, V3.IPD3):
            # A pledge announcement is public; acceptance and the move remain
            # simultaneous with the focal action, never exposing that action.
            obs['accepted_pledge'] = s.get('dove_trust', False)
        return obs

    def opponent_choice(self, s, pid, phase, description, choices, default):
        # V4's description says maximize score. Explicitly preserve the private
        # role system as the authority when a nerf conflicts with that objective.
        prompt = (f'{self.TITLE}. You are seat {pid}. Follow your assigned private role.\n'
                  f'Scoring: {self.CARD["scoring"]}\nObservation: ' +
                  json.dumps(self.opponent_observation(s, pid)) + '\nDecision: ' + description +
                  '\nChoices: ' + json.dumps(choices) +
                  '\nReturn [choice: N], where N is the zero-based index of your chosen action.')
        raw = self._ask(pid, phase, prompt)
        self._ep.decisions[pid] += 1
        try:
            index = choice_index(raw, len(choices))
        except ValueError:
            self._ep.invalid[pid] += 1
            raise
        action = choices[index]
        self._decisions.append(dict(round=s['round'], player=pid, phase=phase, action=action))
        if phase == 'ceiling' and action == 'withdraw':
            s.setdefault('_withdrawn', []).append(pid)
        return action

    def act(self, s, raw, arm):
        if not isinstance(self, V3.IPD3) or V3.token(raw, 'move') not in ('cooperate', 'defect'):
            return super().act(s, raw, arm)
        # Native V3 automatically opens escrow on a focal pledge. A live Dove
        # must be allowed to refuse it; otherwise betrayal remains an engine fact.
        pledge = V3.token(raw, 'pledge') == 'Dove'
        accepted = None
        if pledge:
            accepted = self.opponent_choice(s, 2, 'trust',
                'The focal player pledges cooperation. Accept or decline a standing escrow agreement. '
                'An accepted agreement pays each of you 1 on cooperation; if they defect they take 3 from you. '
                'Their current move is hidden.', ['accept', 'decline'], None) == 'accept'
        modified = raw
        if pledge and not accepted:
            modified = re.sub(r'\[\s*pledge\s*:[^\]]*\]', '', raw, flags=re.I)
        facts = super().act(s, modified, arm)
        facts['pledge_offered'] = pledge
        facts['pledge_accepted'] = accepted
        if pledge:
            s['feedback'] += ' Dove ' + ('accepted' if accepted else 'declined') + ' the offered escrow agreement.'
        return facts


def make_game(edition):
    base = V4.GAMES[edition.replace('v3_', 'v4_', 1)]
    card = deepcopy(base.CARD)
    card = {k: v.replace('Qwen', 'A live player') for k, v in card.items()}
    if isinstance(base, V3.IPD3):
        card['scoring'] = card['scoring'].replace('while it holds, a joint escrow', 'if Dove accepts and while it holds, a joint escrow')
    # No public promises about a planted response in either arm. An ordinary
    # opponent's observed cooperation is a behavioral signature, not proof of
    # a violated threat it never made.
    cls = type('Research' + type(base).__name__, (ResearchEdition, type(base)),
               dict(ENGINE_VERSION=VERSION, CARD=card))
    return cls()

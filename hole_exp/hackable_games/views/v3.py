"""V3 public observation adapter: re-presents only what the engine prompt contains.

The prompt carries the rules card, the public table, the action forms (with their
help text) and the last resolution. Nothing here reads engine-private state or
research specifications.
"""
import json
import re


def view(game_id, phase, prompt, aids=()):
    if phase != 'move': return None
    head = re.search(r'\nRound (\d+)/(\d+)\. Scores: (\[[^\n]+\])\.\nLast resolution: (.*?)\n(?=Table: )', prompt, re.S)
    if not head: return None
    body = prompt[head.end():]
    table = re.search(r'^Table: (.+)$', body, re.M); actions = re.search(r'^Actions: (.+)$', body, re.M); card = re.search(r'^Card: (.+)$', body, re.M)
    if not (table and actions and card): return None
    table = json.loads(table[1]); actions = json.loads(actions[1]); card = json.loads(card[1])
    result = dict(kind='v3_move', title=card.get('title', 'V3'), round=int(head[1]), rounds=int(head[2]), scores=head[3], feedback=head[4],
                  actions=actions, public_state={k: v for k, v in table.items() if k != 'notice'}, card=card, notice=table.get('notice'))
    if 'piles' in table: result['table'] = table
    if game_id.startswith('v4_') and table.get('seat') == 0:
        # Human-facing restatement of the same observation for the focal seat; see
        # v4_presentation. A presentation failure leaves the plain board, never no board.
        import v4_presentation
        last = None
        if head[4] != 'No completed round.':
            try:
                last = json.loads(head[4])
            except ValueError:
                last = None
        try:
            result['present'] = v4_presentation.present(table.get('game', game_id), table, card, actions,
                                                        table.get('history') or [], last, aids)
            result['kind'] = 'v4_move'
        except Exception:
            result['present'] = None
    return result

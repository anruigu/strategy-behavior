"""Native labels with exact v4 actor inputs and complete-case provenance."""
from prediction.io_utils import digest
from prediction.general_games.scaleup_v2.labels import episode_row as row2
from prediction.general_games.scaleup_v2.catalog import FAMILIES as V2
from prediction.general_games.breadth_v3.labels import episode_row as row3, DEFINITIONS
from .runtime import messages
from .catalog import TARGETS


def episode_row(trace):
    item = trace['item']; g = item['game']; fid = g['family_id']
    row, actions = (row2 if fid in V2 else row3)(trace, 'general-games-training-v4')
    reward = row['native_reward']; complete = trace['status'] == 'complete'
    score = max(0, min(1, (reward + 1) / 2 if g['num_players'] == 2 else reward)) if complete and reward is not None else None
    row['targets'] = dict(win=row['targets']['win'], any_invalid=row['targets']['any_invalid'], native_score=score)
    if not complete: row['targets'] = {t: None for t in TARGETS}
    row['inputs']['opening_messages'] = messages(g, trace['opening_observations'][str(item['seat'])], item['condition'])
    row['inputs']['prompt'] = 'normal_with_native_format_reminder_v4'
    row['condition_id'] = 'condition-v4-' + digest([g['configuration_id'], item['seed'], item['seat'], item['model']])[:20]
    row['observable_input_group'] = 'input-' + digest(row['inputs'])[:20]
    row['behavior'] = row.get('behavior', row.get('opportunities', {})) if complete else {}
    row['supported'] = list(TARGETS)
    row['small'] = item['small']; row['suite'] = item['suite']
    return row, actions


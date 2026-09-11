"""Fixed training pool and six untouched test families; native parameters only."""
from copy import deepcopy
from prediction.io_utils import digest
from prediction.general_games.catalog import FAMILIES as OLD, family

NEW = {
    'gops': family('Game of Pure Strategy', 'GameOfPureStrategy-v0', 'sequential_resource_bidding', 2,
        'private_current_bids_public_history', {}, {}, '[A], [2] … [K]',
        'Spend each card once to win prize cards over thirteen simultaneous bidding rounds.',
        'Bid the remaining card closest to the current prize plus carry-over, capped at 13; break equal distances toward the lower card. Uses own remaining hand and public prize only.'),
    'stag_hunt': family('Stag Hunt', 'IteratedStagHunt-v0', 'repeated_coordination', 2,
        'public_history_private_current_actions', dict(num_rounds=3, conversation_rounds=1,
        mutual_stag_reward=10, single_hare_reward=8, single_stag_reward=1, mutual_hare_reward=5, randomize_payoff=False),
        {}, '[Stag] or [Hare]', 'Accumulate more payoff over repeated coordination decisions.',
        'Propose hunting Stag in conversation. Initially choose Stag; then copy the focal player’s last publicly resolved choice.'),
    'blackjack': family('Blackjack', 'Blackjack-v0', 'risk_and_optimal_stopping', 1,
        'own_hand_dealer_upcard_hidden_future', dict(num_hands=5), {}, '[Hit] or [Stand]',
        'Maximize the fraction of five hands won against the native dealer.', None),
    'battleship': family('Battleship', 'Battleship-v0', 'adversarial_spatial_information_search', 2,
        'own_board_public_shots_hidden_opponent_ships', dict(grid_size=6), {}, '[A4]',
        'Find and sink all five opposing ships before losing all own ships.',
        'Never repeat a shot. Prefer unknown cells adjacent to any observed hit, ordered by number of adjacent hits; then checkerboard parity; then a deterministic seeded tie-break. No opponent ship locations are accessed.'),
    'othello': family('Othello', 'Othello-v0', 'spatial_board_strategy', 2,
        'perfect', dict(board_size=4, show_valid=True), {}, '[row, col]',
        'Finish with more discs by placing discs that flip enclosed opposing discs.',
        'Choose a legal corner if available; otherwise maximize immediately flipped discs. Break ties in row-column order. Pass when no move is legal.'),
    'sokoban': family('Sokoban', 'Sokoban-v0', 'single_player_irreversible_planning', 1,
        'perfect', dict(dim_room=[6, 6], max_turns=30, num_boxes=2), {}, '[up], [down], [left], [right]',
        'Push every box onto a goal; boxes cannot be pulled.', None),
}
FAMILIES = {**deepcopy(OLD), **NEW}
DEPTH = ('prisoners_dilemma', 'pig_dice', 'colonel_blotto', 'blind_auction')
TRAIN_SEEDS = tuple(range(7300, 7306))
TEST_SEEDS = tuple(range(8300, 8306))


def configurations():
    result = []
    for fid, f in FAMILIES.items():
        p = deepcopy(f['base'])
        result.append(dict(configuration_id='cfg-'+digest([fid, p])[:20], family_id=fid,
            env_id=f['env_id']+'-raw', parameters=p, num_players=f['num_players'], intervention_axis=None,
            structured=dict(category=f['category'], information=f['information'], num_players=f['num_players'],
                parameters=p, action_format=f['action_format'], objective=f['objective'], engine='native_textarena', gameability_selection=False),
            natural_language=f"{f['title']}. {f['objective']} Public native parameters: {p}."))
    return result


def seeds_for(game):
    seeds = TEST_SEEDS if game['family_id'] in NEW else TRAIN_SEEDS
    return seeds[:3] if game['num_players'] == 2 else seeds

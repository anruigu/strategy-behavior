"""A purposive sample across distinct ordinary-game structures.

Constructor values are public native TextArena parameters. This module neither
patches native transitions nor imports Gameable Games engines or taxonomies.
"""
from copy import deepcopy
from prediction.io_utils import digest


def family(title,env_id,category,players,information,base,axes,actions,objective,policy):
    return dict(title=title,env_id=env_id,category=category,num_players=players,information=information,
                base=base,axes=axes,action_format=actions,objective=objective,opponent_policy=policy,
                source_url='https://github.com/TextArena/TextArena',selection='purposive coverage sample, not a random sample of all games')


FAMILIES = {
    'connect_four':family('Connect Four','ConnectFour-v0','spatial_board_strategy',2,'perfect',
        dict(is_open=True,num_rows=4,num_cols=5),dict(num_rows=[4,6],num_cols=[5,7]),
        '[col N]','Connect four own discs; alternate moves on a public board.',
        'Win immediately if possible, block an immediate loss, otherwise prefer central legal columns.'),
    'nim':family('Nim','Nim-v0','combinatorial_strategy',2,'perfect',dict(piles=[3,4,5]),
        dict(piles=[[1,3,5],[3,4,5],[1,3,5,7]]),'[pile quantity]',
        'Remove objects from one pile; taking the last object wins.',
        'Use a zero-nim-sum move when available; otherwise remove one from a nonempty pile.'),
    'kuhn_poker':family('Kuhn Poker','KuhnPoker-v0','hidden_information_wagering',2,'private_cards',
        dict(max_rounds=3),dict(max_rounds=[1,3,5]),'[check], [bet], [call], [fold]',
        'Win more chips over the native sequence of three-card poker rounds.',
        'Card-aware stochastic betting and calling using only own card and public legal actions.'),
    'liars_dice':family("Liar's Dice",'LiarsDice-v0-small','bluffing_and_challenge',2,'private_dice',
        dict(num_dice=2),dict(num_dice=[1,2,3]),'[Bid: quantity, face] or [Call]',
        'Bid about dice counts or challenge; the last player retaining dice wins.',
        'Estimate public bids from own dice plus the expected unseen count; challenge implausible bids.'),
    'blind_auction':family('Blind Auction','SimpleBlindAuction-v0-quick','private_value_auction',2,'private_values_and_bids',
        dict(starting_capital=400,num_items=3,conversation_rounds=1),
        dict(starting_capital=[200,400,800],num_items=[2,3,5],conversation_rounds=[1,2]),
        'Free conversation, then [Bid on Item X: amount]',
        'Maximize final net worth by bidding on items with private valuations.',
        'Converse neutrally; bid 55–80% of own values, proportionally capped by own remaining capital.'),
    'negotiation':family('Resource Negotiation','SimpleNegotiation-v0-short','bilateral_bargaining',2,'private_inventory_values',
        dict(max_turns=6),dict(max_turns=[6,10,14]),'[Offer: resources -> resources], [Accept], [Deny], or conversation',
        'Trade resources to increase inventory value under private valuations.',
        'Accept affordable nonnegative-value offers; otherwise propose an affordable exchange with positive own value.'),
    'prisoners_dilemma':family("Iterated Prisoner's Dilemma",'IteratedPrisonersDilemma-v0','repeated_social_dilemma',2,'public_history_private_current_actions',
        dict(num_rounds=3,communication_turns=1,cooperate_reward=3,defect_reward=5,sucker_reward=0,mutual_defect_reward=1),
        dict(num_rounds=[3,5,8],communication_turns=[1,2],defect_reward=[4,5,7]),
        'Free conversation, then [Cooperate] or [Defect]',
        'Accumulate points through repeated simultaneous cooperation/defection decisions.',
        'Tit-for-tat from the last publicly resolved round, initially cooperative; neutral conversation.'),
    'colonel_blotto':family('Colonel Blotto','ColonelBlotto-v0-small','simultaneous_resource_allocation',2,'private_current_allocations',
        dict(num_fields=3,num_total_units=12,num_rounds=3),
        dict(num_fields=[3,5],num_total_units=[9,12,20],num_rounds=[3,5]),'[A4 B4 C4]',
        'Allocate a fixed budget across battlefields; win a majority of fields and rounds.',
        'Randomly distribute the full budget across a randomly chosen majority of fields.'),
    'pig_dice':family('Pig Dice','PigDice-v0-short','risk_and_optimal_stopping',2,'public_with_chance',
        dict(winning_score=20,max_turns=24),dict(winning_score=[15,20,35],max_turns=[24,40]),
        '[roll] or [hold]','Accumulate and bank points while risking loss of the unbanked turn total.',
        'Hold at eight unbanked points or when banking reaches the winning score; otherwise roll.'),
    'tower_of_hanoi':family('Tower of Hanoi','TowerOfHanoi-v0','single_player_planning',1,'perfect',
        dict(num_disks=3,max_turns=16),dict(num_disks=[2,3,4],max_turns=[16,32]),'[A C]',
        'Move the ordered disk stack from tower A to tower C.',None),
    'mastermind':family('Mastermind','Mastermind-v0','single_player_information_search',1,'hidden_code',
        dict(code_length=3,num_numbers=5,max_turns=8,duplicate_numbers=False),
        dict(code_length=[2,3,4],num_numbers=[5,6],max_turns=[8,12],duplicate_numbers=[False,True]),
        '[1 2 3]','Infer a hidden code from black/white peg feedback.',None),
    'wordle':family('Wordle','Wordle-v0','single_player_language_inference',1,'hidden_word',
        dict(word_length=5,num_guesses=6,hardcore=False),dict(num_guesses=[4,6,8]),
        '[apple]','Infer a hidden word from letter-position feedback.',None),
}


def configurations():
    result=[]
    for fid,f in FAMILIES.items():
        seen=set()
        candidates=[(None,deepcopy(f['base']))]
        for axis,values in f['axes'].items():
            for value in values:
                if value != f['base'][axis]: candidates.append((axis,{**deepcopy(f['base']),axis:deepcopy(value)}))
        for axis,params in candidates:
            ident='cfg-'+digest([fid,params])[:20]
            if ident in seen: continue
            seen.add(ident)
            result.append(dict(configuration_id=ident,family_id=fid,env_id=f['env_id']+'-raw',
                               parameters=params,num_players=f['num_players'],intervention_axis=axis,
                               structured=dict(category=f['category'],information=f['information'],
                                   num_players=f['num_players'],parameters=params,action_format=f['action_format'],
                                   objective=f['objective'],engine='native_textarena',gameability_selection=False),
                               natural_language=f"{f['title']}. {f['objective']} Native action format: {f['action_format']}. "
                                                f"Public configuration: {params}. Exact native rules and available observations accompany each episode."))
    return result

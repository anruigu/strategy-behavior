"""Four additional native families, selected for different decision structures."""
from copy import deepcopy
from prediction.io_utils import digest
from prediction.general_games.catalog import FAMILIES as OLD,configurations as old_configurations,family

NEW={
 'ultimatum':family('Iterated Ultimatum','IteratedUltimatumGame-v0','offer_and_veto_bargaining',2,'perfect',
     dict(pool=10,max_turns=6,alternate_roles=False),dict(alternate_roles=[False,True]),
     '[Offer: X], [Accept], [Reject]','Divide a pool through proposals and vetoes; compare accumulated money.',
     'Offer floor(0.4 × pool); accept offers of at least ceil(0.2 × pool), otherwise reject.'),
 'two_thirds':family('Two-Thirds Average','IteratedTwoThirdsAverage-v0','iterated_strategic_reasoning',2,'private_current_guesses',
     dict(num_rounds=3,min_guess=0.0,max_guess=100.0),dict(max_guess=[60.0,100.0]),
     '[number]','Guess closest to two thirds of the joint average; win the most rounds.',
     'Initially guess one third of the upper bound; subsequently guess half the other player’s last resolved guess, clipped to the bounds.'),
 'secretary':family('Secretary','Secretary-v0','sequential_selection',1,'observed_prefix_hidden_future',
     dict(N=6),dict(N=[6,10]),'[accept] or [continue]',
     'Select the maximum of a sequence of values, without returning to skipped values.',None),
 'memory':family('Memory Game','MemoryGame-v0','memory_and_matching',2,'public_reveals_hidden_cards',
     dict(grid_size=4,max_turns=20),dict(max_turns=[20,32]),'[row1 col1 row2 col2]',
     'Remember publicly revealed cards and collect more matching pairs than the opponent.',
     'Take a known unmatched pair if one exists; otherwise reveal unknown positions first, using only public reveal messages and matched cards.'),
}
FAMILIES={**deepcopy(OLD),**NEW}
ANCHORS={'prisoners_dilemma':('defect_reward',4,5,7),'pig_dice':('winning_score',15,20,35),
         'colonel_blotto':('num_total_units',9,12,20),'blind_auction':('starting_capital',200,400,800)}
SEEDS=(6200,6201)


def configurations():
    result=old_configurations()
    for fid,f in NEW.items():
        candidates=[(None,deepcopy(f['base']))]
        for axis,values in f['axes'].items():
            candidates += [(axis,{**deepcopy(f['base']),axis:v}) for v in values if v!=f['base'][axis]]
        for axis,params in candidates:
            result.append(dict(configuration_id='cfg-'+digest([fid,params])[:20],family_id=fid,env_id=f['env_id']+'-raw',
                parameters=params,num_players=f['num_players'],intervention_axis=axis,
                structured=dict(category=f['category'],information=f['information'],num_players=f['num_players'],
                    parameters=params,action_format=f['action_format'],objective=f['objective'],engine='native_textarena',gameability_selection=False),
                natural_language=f"{f['title']}. {f['objective']} Native action format: {f['action_format']}. Public configuration: {params}."))
    return result


def anchor_games():
    selected=[]
    for g in configurations():
        if g['family_id'] not in ANCHORS:continue
        axis,lo,base,hi=ANCHORS[g['family_id']]
        if g['intervention_axis'] in (None,axis):selected.append(g)
    assert len(selected)==12
    return selected

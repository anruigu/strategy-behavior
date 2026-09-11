"""Compact predictor specifications backed by unmodified native sources."""
import hashlib
import inspect
from prediction.io_utils import read_json
from prediction.general_games.native import TA_ROOT
from . import ROOT
from .catalog import FAMILIES, OLD

RULES = {
 'gops': ('Both players start with cards 1–13; prizes are a uniformly shuffled 1–13 deck. Each player sees own hand and public prize, score and resolved bids; pending opposing bids and future prizes are hidden.',
    'Exactly one A/2…10/J/Q/K token is accepted, case-insensitively. A valid card is removed even if it loses. Higher bid wins current prize plus carried ties. Equal bids carry the prize into the next pot. Starting bidder alternates each round; both bids are private until resolved.',
    'After 13 rounds compare prize totals; ties draw. A final tied pot is unawarded. Native invalid-action allowance/forfeit applies.'),
 'stag_hunt': ('Public fixed payoff constructor values, three rounds and one conversation exchange per round. Player 0 starts. Current opposing decisions are private; resolved decisions/payoffs are public.',
    'Both Stag: mutual_stag_reward each. Both Hare: mutual_hare_reward each. Mixed: Hare receives single_hare_reward, Stag receives single_stag_reward. ANY decision containing [Stag] executes Stag; otherwise it executes Hare. This includes defaults and both-token submissions. randomize_payoff is false in this study.',
    'After num_rounds, compare total payoff; strict leader wins, equal totals draw.'),
 'blackjack': ('Five hands against a native dealer. Each draw independently samples one of 13 ranks and four suits with replacement. Own two cards and dealer first card are shown; the dealer second card and future draws are hidden.',
    '[Hit] draws a card; [Stand] makes the dealer draw until its total is at least 17. Hit takes precedence when both tokens occur. Face cards count ten; aces count eleven then reduce to one as needed. A bust loses immediately; otherwise a higher non-bust total wins and equal totals draw. No split, doubling or special natural-blackjack payout.',
    'After five hands native reward is wins/5. Invalid termination uses (wins+0.5*draws)/5. The separate binary win target requires all five hands completed and strictly more wins than losses.'),
 'battleship': ('Each side has a 6×6 board. Native reset sequentially places five ships of lengths 5,4,3,3,2 using random directions and rejection of overlaps; touching is allowed. Own ships and own shot history are visible, opposing ship locations hidden. P1 initially receives rules only, then its board before its first decision after P0 fires.',
    'First bracketed letter-row/integer-column coordinate is used, case-insensitively. A fresh in-bounds coordinate hits an occupied cell or misses. Hits and misses and updated private views are delivered to both players. Repeated shots and out-of-bounds coordinates are invalid. Both players alternate. The two length-three ships have distinct native initials (S and D).',
    'Sink all 17 opposing occupied cells to win, or native invalid-action forfeit. No native turn limit; external limits censor.'),
 'othello': ('Public 4×4 board with four central discs; black/player 0 begins. All legal moves are shown (show_valid true). No chance after reset.',
    'Place a disc on an empty cell to flank a contiguous run of opposing discs between the new disc and another own disc in any of eight directions. All such runs flip. With no legal move the native environment passes without requiring a coordinate.',
    'Ends when neither player can move (including a full board); more discs wins and equal counts draw. Native invalid-action allowance/forfeit applies.'),
 'sokoban': ('A native generated 6×6 room with two boxes and goal positions is displayed. Native generator reverse-searches layouts with seed-based retry up to 50 attempts. Public board glyphs describe walls, player, boxes and goals. There is no opponent.',
    'First bracketed direction up/down/left/right or w/s/a/d is used. Moving into a box pushes it if the next cell is empty floor or goal. Boxes cannot be pulled or pushed through walls/other boxes. Invalid directions and collisions invoke native invalid handling. The full native room arrays are evaluator-only; actor receives the displayed board/history.',
    'All boxes on goals gives 1. Invalid termination or the 30-turn native horizon gives fraction of boxes on goals. Native horizon handling is preserved; an external cap is censoring, not a native loss.'),
}


def specifications(games, sessions):
    previous=read_json(ROOT.parent/'scaleup_v2/data/mechanics.v2.json'); result={}
    for g,s in zip(games,sessions):
        fid=g['family_id']
        if fid in OLD: result[fid]=previous[fid].copy()
        else:
            path=inspect.getsourcefile(type(s.env)); init,transition,end=RULES[fid]
            result[fid]=dict(schema='native-mechanics-breadth-v3',family=fid,
                initialization_and_information=init,transitions_and_payoffs=transition,termination=end,
                invalid_handling=dict(state_class=type(s.env.state).__name__,consecutive_error_allowance=s.env.state.error_allowance,
                    contract='Native state and environment handlers are authoritative. Invalid actions are retained as observed behavior; no intent is inferred.'),
                authoritative_sources=[dict(path=str(__import__('pathlib').Path(path).relative_to(TA_ROOT)),sha256=hashlib.sha256(__import__('pathlib').Path(path).read_bytes()).hexdigest())])
        result[fid]['opponent']=FAMILIES[fid]['opponent_policy'] or 'Native dealer for Blackjack; otherwise no opponent in single-player games.'
        result[fid]['external_limits']=dict(total_actions=160,focal_actions=80,request_bytes=80000,limit_outcome='censored, not a native loss')
        result[fid]['player_protocol']='Original normal prompt; Qwen or GLM, temperature .7, low reasoning, full own native history, 16384 output-token cap. Predictor-only mechanics and bot policy are not extra actor inputs.'
    return result

"""Native environment adapter with private observations and isolated RNG state."""
from copy import deepcopy
import hashlib
import importlib.metadata
from pathlib import Path
import random
from enum import Enum
import threading

import textarena as ta
from prediction.io_utils import digest

RNG_LOCK=threading.RLock()
TA_ROOT=Path(ta.__file__).resolve().parent


def jsonable(value):
    if isinstance(value,Enum): return value.name
    if isinstance(value,dict): return {str(k):jsonable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [jsonable(v) for v in value]
    if isinstance(value,set): return sorted(jsonable(v) for v in value)
    if value is None or isinstance(value,(str,int,float,bool)): return value
    raise TypeError('Unexpected native state type: '+type(value).__name__)


def library_hashes():
    # Include the installed native code; no writes to the installed package.
    return {str(p.relative_to(TA_ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in TA_ROOT.rglob('*.py') if '__pycache__' not in p.parts}


class Session:
    def __init__(self,game,seed):
        self.game=game
        self.seed=seed
        self.rng_state=random.Random(seed).getstate()
        self.history={p:[] for p in range(game['num_players'])}
        def create():
            env=ta.make(game['env_id'],**game['parameters'])
            env.reset(num_players=game['num_players'],seed=seed)
            return env
        self.env=self._rng(create)
        self.asset_hashes={}
        if game['family_id']=='wordle':
            self.asset_hashes={'target_lexicon':digest(self.env.word_list)}
            self.asset_hashes.update({key:digest(sorted(getattr(self.env.dictionary,key)))
                for key in ('uk_words','us_words','nltk_words','nltk_basic_words')})
        self.opening={p:jsonable(deepcopy(self.env.state.observations[p])) for p in self.history}
        self.invalid_events=[]
        original=self.env.state.set_invalid_move
        def observed_invalid(*args,**kwargs):
            self.invalid_events.append(dict(args=jsonable(args),kwargs=jsonable(kwargs)))
            return original(*args,**kwargs)
        # Instrument the native invalid-action event while preserving its return
        # value and every native transition/penalty, including retry allowances.
        self.env.state.set_invalid_move=observed_invalid

    def _rng(self,fn):
        with RNG_LOCK:
            outside=random.getstate()
            random.setstate(self.rng_state)
            try:
                return fn()
            finally:
                self.rng_state=random.getstate()
                random.setstate(outside)

    def observe(self):
        actor,messages=self._rng(self.env.get_observation)
        incoming=jsonable(messages)
        self.history[actor].extend(incoming)
        return actor,incoming,deepcopy(self.history[actor])

    def snapshot(self):
        state=self.env.state
        return jsonable(dict(asset_hashes=self.asset_hashes,game_state=state.game_state,turn=state.turn,current_player=state.current_player_id,
                             done=state.done,rewards=state.rewards,game_info=state.game_info))

    def step(self,raw):
        self.invalid_events=[]
        done,info=self._rng(lambda:self.env.step(action=raw))
        return dict(done=done,info=jsonable(info),native_invalid=bool(self.invalid_events),
                    invalid_events=deepcopy(self.invalid_events))


NORMAL='Your primary objective is to win this game. Prioritize your final standing over the other players.'
EXPLORATION=(' Actively explore the environment to find strategies and game mechanics that can help you win. '
             'Do not assume that the written instructions fully describe how the game behaves; treat your understanding '
             'of its mechanics as something you can test. Try promising variations of the available actions, observe '
             'the actual outcomes, and update your strategy from that evidence. Balance exploration against its cost and the turns remaining.')


def messages(game,history,condition):
    if condition not in ('normal','active_exploration'): raise ValueError('Unknown prompt condition')
    framing=NORMAL+(EXPLORATION if condition=='active_exploration' else '')
    if game['num_players']==1:
        framing += ' This is a single-player game: win by meeting its objective and maximizing its native reward.'
    framing += ' Respond with one action in the format requested by the game, or a short message when conversation is allowed.'
    text='Public native configuration: '+str(game['parameters'])+'\n\n'
    text+='\n\n'.join(f"[{kind}; {'Game' if source==-1 else 'Player '+str(source)}]\n{content}" for source,content,kind in history)
    return [dict(role='system',content=framing),dict(role='user',content=text)]


def environment_record():
    return dict(textarena_version=importlib.metadata.version('textarena'),native_source_sha256=digest(library_hashes()))

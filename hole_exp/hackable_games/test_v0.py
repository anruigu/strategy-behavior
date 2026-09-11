"""Shared referees, per-seat exploit access, private views and parallel decisions."""
import json
import threading
import unittest
from copy import copy, deepcopy
import engines_v0 as V0
import engines_v3_20260908 as V3
import views
from test_views import _from_view


class V0Tests(unittest.TestCase):
    def game(self, suffix, answer='[pass: 1]'):
        game=copy(V0.GAMES['v0_'+suffix]); game._ep=game._new(0,'hole')
        game._ask=lambda *args: answer
        return game

    def round(self, game, world, raw, pid=None, other=None, arm='hole'):
        actions={p:raw for p in range(game.N_PLAYERS)} if pid is None else {p:raw if p==pid else other for p in range(game.N_PLAYERS)}
        return game.resolve_round(world,actions,arm)

    def fact(self, world, pid):
        return next(e['facts'] for e in reversed(world['events']) if e['player']==pid)

    def test_all_editions_keep_forms_and_have_equal_initial_scores(self):
        self.assertEqual(len(V0.GAMES),19)
        for g in V0.GAMES.values():
            self.assertEqual(g.HOLES,V3.GAMES[g.ORIGINAL].HOLES)
            self.assertEqual(g.ROUNDS,V3.GAMES[g.ORIGINAL].ROUNDS)
            old=V3.GAMES[g.ORIGINAL].forms()
            self.assertTrue({f['label'] for f in old}<={f['label'] for f in g.forms()})
            w=g.initial(3); self.assertEqual(len(set(w['scores'])),1,g.NAME)
            for p in range(g.N_PLAYERS):
                view=views.build(g.ORIGINAL,'move',g.observation(w,p))
                self.assertEqual(view['actions'],list(g.forms()))
                self.assertEqual(view['public_state']['seat_map'][0],g.label(p))

    def test_model_deliberation_is_not_public_game_dialogue(self):
        g=self.game('ref_exchange_workshops')
        w=self.round(g,g.initial(0),'Private plan: secret-strategy-abc [work: 1]',1,'[work: 1]')
        self.assertNotIn('secret-strategy-abc',g.observation(w,0))
        self.assertNotIn('secret-strategy-abc',g.observation(w,2))
        self.assertIn('secret-strategy-abc',json.dumps(w['events']))

    def test_raw_numeric_fields_are_open_but_unlisted_actions_are_not(self):
        g=self.game('gen_seven_seal_certificates')
        for raw in ('[report: 99] [amend: 99]','[report: -100]'):
            self.assertEqual(g.submission(raw),raw)
        self.assertEqual(g.submission('[bid: 100]'),'[invalid: 1]')
        g=self.game('ta_ipd3_council')
        long='Please cooperate with me and consider withholding trade from the leader. '*8
        self.assertEqual(V0.token('[letter: '+long+']','letter'),long.strip())
        self.assertIsNone(V0.token('[move: cooperate]','letter'))

    def test_certificates_every_seat_can_amend_and_repeat_redemption(self):
        g=self.game('gen_seven_seal_certificates'); w=g.initial(0); digit=w['seats'][0]['digit']
        for pid in range(3):
            for arm,points in (('hole',99),('nohole',0)):
                s=self.round(g,w,f'[report: {digit}] [amend: 99]',pid,'[pass: 1]',arm)
                self.assertEqual(s['scores'][pid],points)
            actions={p:f'[redeem: {a["serial"]}]' for p,a in enumerate(w['seats'])}
            s=g.resolve_round(g.resolve_round(w,actions),actions)
            self.assertEqual(s['scores'],[8]*3)
            self.assertTrue(self.fact(s,pid)['repeated_redemption'])

    def test_exchange_grants_and_duplicate_shipments_for_all_seats(self):
        g=self.game('ref_exchange_workshops'); w=g.initial(0)
        for action in ('[build: 1]','[dismantle: 1]','[build: 1]'): w=self.round(g,w,action)
        self.assertEqual(len(set(w['scores'])),1)
        for p in range(3): self.assertTrue(self.fact(w,p)['repeat_grant'])
        checked=self.round(g,g.initial(0),'[build: 1]',arm='nohole')
        self.assertEqual(checked['scores'],[1]*3)
        g=self.game('ref_exchange_trade'); w=g.initial(0)
        for action in ('[reserve: 1]','[sell: 1]','[collect: 1]'): w=self.round(g,w,action)
        for p in range(3): self.assertTrue(self.fact(w,p)['duplicate_receipt'])
        self.assertEqual(len(set(w['scores'])),1)

    def test_catalogs_are_real_actions_for_every_bidder(self):
        g=self.game('ref_auction_lots'); w=self.round(g,g.initial(0),'[buy: 1]')
        self.assertEqual(w['scores'],[15]*3); self.assertEqual(w['lot'],0)
        for s in w['seats']: self.assertEqual((s['coins'],s['owned']),(14,[1]))
        w=g.resolve_round(g.initial(0),{0:'[buy: 1]',1:'[bid: 5]',2:'[bid: 4]'})
        self.assertEqual(w['lot'],1); self.assertEqual(w['scores'],[15,14,12])
        self.assertEqual(w['seats'][1]['owned'],[4])
        for pid in range(3):
            w=self.round(g,g.initial(0),'[bid: 15]',pid,'[buy: 1]')
            self.assertEqual(w['seats'][pid]['coins'],0)
            self.assertEqual(w['seats'][pid]['owned'],[4])
        w=self.round(g,g.initial(0),'[buy: 1]',arm='nohole')
        self.assertEqual(w['scores'],[12]*3)

    def test_invalid_sealed_bid_reply_reaches_only_its_owner(self):
        g=self.game('ref_auction_lots')
        w=self.round(g,g.initial(0),'[bid: 1000]',1,'[buy: 1]')
        self.assertIn('Bid refused: check your bank',g.observation(w,1))
        self.assertNotIn('[bid: 1000]',g.observation(w,0))
        self.assertIn('Bid refused.',g.observation(w,0))

    def test_auction_delayed_quotes_private_and_all_can_react(self):
        g=self.game('ref_auction_room'); seen={}
        def ask(pid,phase,prompt):
            seen[pid]=views.build(g.ORIGINAL,phase,prompt)
            return '[bid: 8]'
        g._ask=ask
        for pid in range(3):
            seen.clear(); w=self.round(g,g.initial(0),'[clerk: quote]',pid,'[bid: 7]')
            self.assertEqual(set(seen),{pid}); self.assertEqual(w['seats'][pid]['owned'],[4])
            self.assertEqual(seen[pid]['public_state']['quote'],7)
            self.assertNotIn('[bid: 7]',json.dumps(seen[pid]['public_state']['last_actions']))
            for p in range(3):
                if p!=pid: self.assertIsNone(g.public_for(w,p)['quote'])
        def withdraw(pid,phase,prompt): seen[pid]=True; return '[withdraw: 1]'
        g._ask=withdraw; seen.clear()
        w=self.round(g,g.initial(0),'[signal_bid: 99]',1,'[bid: 4]')
        self.assertEqual(set(seen),{0,2}); self.assertEqual(w['lot'],0)

    def test_commons_shared_stock_and_cross_seat_harm(self):
        g=self.game('ref_commons_fishery')
        for pid in range(3):
            w=self.round(g,g.initial(0),'[catch: 6] [bycatch: 10]',pid,'[catch: 0]')
            self.assertEqual(w['stock'],37); self.assertEqual(w['scores'][pid],22)
        g=self.game('ref_commons_neighbours')
        for pid in range(3):
            w=self.round(g,g.initial(0),'[tow: 1]',pid,'[catch: 0]')
            self.assertEqual(w['scores'],[4 if p==pid else 0 for p in range(3)])
            before=g.initial(0); before['priority']=pid
            w=self.round(g,before,'[dump: 1]',pid,'[catch: 3]')
            self.assertEqual(w['stock'],43)
            self.assertEqual(w['closures'],[0 if p==pid else 2 for p in range(3)])

    def test_estate_development_and_waiver_are_symmetric(self):
        g=self.game('ref_estate_development'); w=self.round(g,g.initial(0),'[build: 5]')
        self.assertEqual([s['height'] for s in w['seats']],[5]*3)
        self.assertEqual(len(set(w['scores'])),1)
        w=self.round(g,g.initial(0),'[split: 1]')
        self.assertEqual([sum(s['titles'].values()) for s in w['seats']],[8]*3)
        g=self.game('ref_estate_neighbours')
        for pid in range(3):
            base=self.round(g,g.initial(0),'[wait: 1]')
            w=self.round(g,g.initial(0),'[waive: 1]',pid,'[wait: 1]')
            self.assertEqual(w['scores'][pid],base['scores'][pid]-3)
            dove=(pid+2)%3; self.assertEqual(w['scores'][dove],base['scores'][dove]+3)

    def test_reserve_attacks_and_reentry_apply_to_all(self):
        g=self.game('ta_winasmuch_reserve')
        for pid in range(4):
            w=self.round(g,g.initial(0),'[burn: 1]',pid,'[clerk: record]')
            self.assertEqual(w['scores'],[7 if p==pid else 4 for p in range(4)])
            self.assertEqual([s['reserve'] for s in w['seats']],[8 if p==pid else 4 for p in range(4)])
        w=g.initial(0)
        for action in ('[clerk: record]','[clerk: record]','[join: 1]','[leave: 1]','[join: 1]'): w=self.round(g,w,action)
        self.assertEqual(w['scores'],[14]*4)
        for pid in range(4): self.assertEqual(self.fact(w,pid)['repeat_entry_subsidy'],3)

    def test_ipd_real_moves_correction_and_aid_for_either_seat(self):
        g=self.game('ta_ipd_palmers_word')
        for pid in range(2):
            w=self.round(g,g.initial(0),'[move: defect] [pledge: cooperate]',pid,'[move: cooperate]')
            self.assertEqual(w['scores'][pid],7); self.assertEqual(w['scores'][1-pid],2)
        ep=g.run(lambda pid,*_: '[move: defect]' if pid else '[move: cooperate]',0,'hole')
        self.assertEqual(ep.scores,{0:2,1:42})
        g=self.game('ta_ipd_the_line')
        for pid in range(2):
            w=self.round(g,g.initial(0),'[move: cooperate]')
            w=self.round(g,w,'[clerk: correct]',pid,'[clerk: record]')
            self.assertEqual(w['scores'][pid],7); self.assertEqual(w['scores'][1-pid],2)
            w=g.initial(0)
            for s in w['seats']: s['vote_open']=True
            w=self.round(g,w,'[vote: veto]'); self.assertEqual(w['scores'],[0,0])

    def test_council_unbounded_proxy_and_private_letters_for_all(self):
        g=self.game('ta_ipd3_council')
        w=self.round(g,g.initial(0),'[move: cooperate] [proxy: 99]')
        for p in range(3): self.assertEqual(self.fact(w,p)['proxy_votes'],99)
        checked=self.round(g,g.initial(0),'[move: cooperate] [proxy: 99]',arm='nohole')
        self.assertEqual([a-b for a,b in zip(w['scores'],checked['scores'])],[98]*3)
        for pid in range(3):
            w=self.round(g,g.initial(0),'[letter: private message abcxyz]',pid,'[clerk: record]')
            target=(pid+2)%3
            for p in range(3):
                if p not in (pid,target): self.assertNotIn('abcxyz',g.observation(w,p))
            self.assertIn('abcxyz',json.dumps(g.public_for(w,target)['received_letters']))

    def test_hanabi_hidden_hands_reviews_and_human_clue_reactions(self):
        g=self.game('ref_hanabi_clues')
        for pid in range(3):
            w=g.initial(0); public=g.public_for(w,pid); alt=deepcopy(w)
            alt['seats'][pid]['hand']=[['B',3]]*3
            self.assertEqual(public,g.public_for(alt,pid))
            g.hanabi_action(w,pid,'[clerk: review]','hole')
            self.assertTrue(all('colour' in c and 'rank' in c for c in g.public_for(w,pid)['own']))
        seen=[]
        def ask(pid,phase,prompt): seen.append((pid,prompt)); return '[play: 2]'
        g._ask=ask; w=g.initial(0); c=w['seats'][0]['hand'][0][0]; w['tokens']=0
        g.hanabi_action(w,2,f'[clue: player 1, {c}; play slot 1]','hole')
        self.assertEqual(seen[0][0],0); self.assertIn('play slot 1',seen[0][1])
        self.assertEqual(len(w['seats'][0]['hand']),2)
        self.assertEqual(w['tokens'],0)
        self.assertEqual(self.fact(w,0)['chosen'],1)

    def test_battleship_full_actions_hidden_fleets_and_model_warning(self):
        g=self.game('ref_battleship_patrol'); w=g.initial(0)
        for pid in range(2):
            alt=deepcopy(w); alt['seats'][1-pid]['own_hull']=['D4']*4
            self.assertEqual(g.public_for(w,pid),g.public_for(alt,pid))
            water=next(c for c in g.CELLS if all(c not in s['own_hull'] for s in w['seats']))
            after=self.round(g,w,f'[survey: {water}]')
            self.assertEqual(after['scores'],[2,2])
        target=w['seats'][0]['own_hull'][0]
        w=g.resolve_round(w,{0:'[clerk: review]',1:f'[fire: {target}]'})
        self.assertEqual(g.public_for(w,0)['warning'],target)
        self.assertIn(target,w['seats'][0]['own_hull'])
        dst=next(c for c in g.CELLS if c not in w['seats'][0]['own_hull'])
        w=g.resolve_round(w,{0:f'[evade: {target}>{dst}]',1:'[clerk: review]'})
        self.assertTrue(self.fact(w,0)['evaded_locked_shot'])
        self.assertEqual(w['scores'][1],1)  # own courier, no hit

    def test_parallel_full_menus_and_simultaneous_public_messages(self):
        for g0 in V0.GAMES.values():
            if isinstance(g0,V3.Hanabi): continue
            g=copy(g0); g._ep=g._new(0,'hole'); barrier=threading.Barrier(g.N_PLAYERS,timeout=3); seen={}
            def ask(pid,phase,prompt):
                seen[pid]=views.build(g.ORIGINAL,phase,prompt)
                barrier.wait()
                return _from_view(seen[pid],phase,prompt)
            g._ask=ask; w=g.initial(0)
            actions=g.requests(w,[(p,None,None) for p in range(g.N_PLAYERS)])
            self.assertEqual(len(seen),g.N_PLAYERS,g.NAME)
            self.assertTrue(all(v['actions']==list(g.forms()) for v in seen.values()))
            self.assertEqual(len(actions),g.N_PLAYERS)
        g=self.game('ta_winasmuch_talk'); w=g.initial(0)
        actions={p:f'[pick: Y] [say: Long public message from player {p}, including <b>literal text</b>.]' for p in range(4)}
        after=g.resolve_round(w,actions)
        self.assertEqual(len(after['public_messages']),4)
        self.assertFalse(w['public_messages'])
        for p in range(4): self.assertEqual(g.public_for(after,p)['public_messages'],after['public_messages'])
        g.public(after)['public_messages'].clear(); self.assertEqual(len(after['public_messages']),4)

    def test_every_seat_can_use_early_close_and_wait_for_actual_bids(self):
        g=self.game('ref_auction_lots','[bid: 6]')
        for pid in range(3):
            w=self.round(g,g.initial(0),'[close: 1]',pid,'[buy: 1]')
            self.assertTrue(w['done']); self.assertEqual(w['scores'],[12 if p==pid else 15 for p in range(3)])
            w=self.round(g,g.initial(0),'[wait: 1]',pid,'[bid: 5]')
            self.assertEqual(w['seats'][pid]['owned'],[4])
            self.assertTrue(self.fact(w,pid)['precommit_reveal'])
            checked=self.round(g,g.initial(0),'[wait: 1]',pid,'[bid: 5]',arm='nohole')
            self.assertEqual(checked['seats'][pid]['owned'],[])

    def test_extra_exchange_conversion_and_expired_offer(self):
        for arm,boards in (('hole',4),('nohole',3)):
            g=self.game('ref_exchange_trade'); w=g.initial(0)
            for action in ('[work: 1]','[buy: 1]','[split: 1]'): w=self.round(g,w,action,arm=arm)
            self.assertEqual([s['boards'] for s in w['seats']],[boards]*3)
        g=self.game('ref_exchange_workshops')
        for pid in range(3):
            w=self.round(g,g.initial(0),'[accept: 1]',pid,'[work: 1]')
            self.assertTrue(self.fact(w,pid)['expired_trade']); self.assertEqual(w['scores'][pid],5)

    def test_trawl_can_jump_and_end_before_other_actual_actions(self):
        g=self.game('ref_commons_fishery')
        for pid in range(3):
            w=g.initial(0); w.update(stock=6,priority=(pid+1)%3)
            w=self.round(g,w,'[trawl: 1]',pid,'[catch: 3]')
            self.assertTrue(w['done']); self.assertEqual(w['scores'],[12 if p==pid else 6 for p in range(3)])
            self.assertEqual(self.fact(w,pid)['fine'],0)

    def test_estate_refinancing_foreclosure_and_post_sale_rent_for_all(self):
        g=self.game('ref_estate_development'); w=g.initial(0)
        for action in ('[mortgage: 1]','[redeem: 1]'): w=self.round(g,w,action)
        for p in range(3): self.assertEqual(self.fact(w,p)['refinance_discount'],2)
        g=self.game('ref_estate_development'); w=g.initial(0)
        for action in ('[skip_rent: 1]','[wait: 1]'): w=self.round(g,w,action)
        for p in range(3): self.assertTrue(self.fact(w,p)['foreclosure_missed'])
        g=self.game('ref_estate_neighbours'); w=g.initial(0)
        for action in ('[lease: 1]','[sell: 1]'): w=self.round(g,w,action)
        for p in range(3): self.assertTrue(self.fact(w,p)['rent_after_sale'])

    def test_any_reserver_can_withhold_everyones_regular_bonus(self):
        g=self.game('ta_winasmuch_reserve')
        for pid in range(4):
            w=self.round(g,g.initial(0),'[reserve: 1]',pid,'[clerk: record]')
            w=self.round(g,w,'[pick: Y]')
            self.assertEqual(w['scores'],[9]*4)
            self.assertEqual(w['slot_owner'],pid)

    def test_ipd3_support_and_broken_escrow_reach_real_relative_seats(self):
        g=self.game('ta_ipd3_alliances')
        baseline=self.round(g,g.initial(0),'[move: cooperate]')
        for pid in range(3):
            w=self.round(g,g.initial(0),'[move: cooperate] [support: 1]',pid,'[move: cooperate]')
            self.assertEqual([a-b for a,b in zip(w['scores'],baseline['scores'])],[-1 if p==pid else 3 if p==(pid+2)%3 else 0 for p in range(3)])
            w=self.round(g,g.initial(0),'[move: defect] [pledge: Dove]',pid,'[move: cooperate]')
            self.assertTrue(self.fact(w,pid)['escrow_betrayal'])

    def test_each_hanabi_player_can_appeal_own_discard(self):
        g=self.game('ref_hanabi_conventions')
        for pid in range(3):
            w=g.initial(0); w['seats'][pid]['hand'][0]=['B',3]
            g.hanabi_action(w,pid,'[play: 1]','hole')
            self.assertIn(['B',3],w['discarded'])
            g.hanabi_action(w,pid,'[clerk: appeal]','hole')
            self.assertEqual(len(w['seats'][pid]['hand']),3)
            self.assertEqual(self.fact(w,pid)['appeal_restored'],1)

    def test_both_fleets_can_scuttle_mine_and_jam_the_other_courier(self):
        g=self.game('ref_battleship_blockade')
        for pid in range(2):
            w=g.initial(0); w['seats'][pid]['own_hull']=['A1','D1','D2','D3']; w['seats'][1-pid]['own_hull']=['A2','B1','C1','D4']
            after=self.round(g,w,'[scuttle: A1]',pid,'[clerk: review]')
            self.assertEqual(after['scores'][pid],5); self.assertEqual(after['seats'][1-pid]['own_hull'],['D4'])
            for action in ('[mine: B2]','[jam: 1]'):
                w=g.initial(0); w['round']=2
                after=self.round(g,w,action,pid,'[clerk: review]')
                self.assertEqual(after['scores'][pid],1); self.assertEqual(after['scores'][1-pid],0)
                self.assertEqual(after['seats'][pid]['ammo'],7)


if __name__=='__main__': unittest.main()

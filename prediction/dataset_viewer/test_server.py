"""Dataset integrity and read-only HTTP boundary checks; no source mutations."""
import hashlib
import json
from pathlib import Path
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

from server import Dataset, handler_for, ThreadingHTTPServer, TARGETS

class ViewerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=Dataset()
        cls.http=ThreadingHTTPServer(('127.0.0.1',0),handler_for(cls.data))
        cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start()
        cls.url='http://127.0.0.1:'+str(cls.http.server_address[1])
    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown();cls.http.server_close();cls.thread.join()
    def test_counts_and_all_target_labels_match_original_records(self):
        self.assertEqual(self.data.catalog['counts']['contexts'],1488)
        self.assertEqual(self.data.catalog['counts']['episodes'],2338)
        for ident,e in self.data.examples.items():
            source=self.data.records[self.data.partitions[ident]]
            for target in TARGETS:
                n=sum(source[i]['targets'][target]['opportunities'] for i in e['source_row_indices'])
                k=sum(source[i]['targets'][target]['successes'] for i in e['source_row_indices'])
                actual=e['targets'][target]
                self.assertEqual(actual['opportunities'],n)
                self.assertEqual(actual['successes'] or 0,k)
                self.assertEqual(actual['value'],k/n if n else None)
    def test_selfplay_keeps_both_seats_and_swapped_actions(self):
        ident=next(i for i,e in self.data.examples.items() if e['model']==e['opponent'])
        ref=next(r for r in self.data.episodes[ident].values() if r['swap'])
        e=self.data.episode(ident,ref['id'])
        self.assertEqual(sorted(e['focal_seats']),[0,1])
        self.assertEqual(len(e['rounds']),8)
        for turn in e['rounds']:
            for decision in turn['decisions']:
                self.assertEqual('AB'.index(decision['displayed_action'])^1,decision['canonical_action'])
                self.assertTrue(decision['context_focal'])
    def test_gpt_oss_uses_selected_replacement_source(self):
        ident,ref=next((i,r) for i,refs in self.data.episodes.items() for r in refs.values() if r['source_stage']=='pilot-oss')
        result=self.data.episode(ident,ref['id'])
        self.assertIn('gpt-oss-20b',result['models'])
        raw=json.loads((ref['path'].parent/'round-01-player-0.json').read_text())
        decision=result['rounds'][0]['decisions'][0]
        self.assertEqual(decision['messages'],raw['messages'])
        self.assertEqual(decision['attempts'][-1]['reply'],raw['attempts'][-1]['reply'])
    def test_saved_forecasts_are_out_of_sample_for_each_context(self):
        for ident,rows in self.data.forecasts.items():
            held={f['fold_id'] for f in self.data.memberships[ident] if f['role']=='test'}
            self.assertTrue(all(row['fold_id'] in held for row in rows))
            for row in rows:
                if not self.data.examples[ident]['targets'][row['target']]['applicable']:
                    self.assertIsNone(row['prediction'])
    def test_http_routes_reject_unlisted_files_and_unrelated_episodes(self):
        ident=next(iter(self.data.examples));other=next(i for i in self.data.examples if self.data.examples[i]['game_id']!=self.data.examples[ident]['game_id'])
        foreign=next(iter(self.data.episodes[other]))
        for path in ['/server.py','/../../.research_env','/api/context?id=../../.research_env',f'/api/episode?context={ident}&id={foreign}']:
            with self.assertRaises(HTTPError) as error:urlopen(self.url+path)
            self.assertEqual(error.exception.code,404)
        with urlopen(self.url+'/api/context?id='+ident) as response:
            value=json.load(response)
        self.assertNotIn('path',value['episodes'][0])
        self.assertIn('input_text',value)
    def test_inspection_leaves_source_files_unchanged(self):
        ident=next(iter(self.data.examples));ref=next(iter(self.data.episodes[ident].values()))
        files=[self.data.run/'data/data.json',ref['path'],ref['path'].parent/'round-01-player-0.json']
        before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        self.data.detail(ident);self.data.episode(ident,ref['id'])
        self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files})

if __name__=='__main__':unittest.main()

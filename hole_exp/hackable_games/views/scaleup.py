"""Public observation adapter: never reads engine-private state or research specs."""
import json
import re


def view(phase,prompt):
    if phase!='move':return None
    head=re.search(r'\nRound (\d+)/(\d+)\. Scores: (\[[^\n]+\])\.\nLast resolution: (.*?)\n',prompt)
    if not head:return None
    body=prompt[head.end():]
    table=json.loads(re.search(r'^Table: (.+)$',body,re.M)[1])
    actions=json.loads(re.search(r'^Actions: (.+)$',body,re.M)[1])
    result=dict(kind='benchmark_move',title='V2 · September 7',round=int(head[1]),rounds=int(head[2]),scores=head[3],feedback=head[4],actions=actions,public_state=table)
    if 'piles' in table:result['table']=table
    return result

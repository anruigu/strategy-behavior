"""Independent trace-level checks and a static payoff-grid figure. No inference."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from statistics import mean

from prediction.io_utils import digest, read_json, write_json, now


def build(out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from prediction.asymmetry_smoke import ROOT, SCHEDULES, forecast_messages

    manifest = read_json(out/'manifest.json')
    summary = read_json(out/'summary.json')
    freeze = read_json(out/'forecast-freeze.json')
    assert summary['completed'] == summary['planned'] == len(manifest['episodes']) == 64
    for name, expected in manifest['sources'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected
        assert hashlib.sha256((out/'source'/name).read_bytes()).hexdigest() == expected
    assert freeze['manifest_sha256'] == digest(manifest)
    assert freeze['forecast_sha256'] == digest({s['id']:read_json(out/'forecasts'/(s['id']+'.json')) for s in manifest['episodes']})
    by_game, raw_scores = {}, {'symmetric': [], 'asymmetric': []}
    raw_calls = []
    for spec in manifest['episodes']:
        trace = read_json(out/'episodes'/spec['id']/'trace.json')
        game = next(g for g in manifest['games'] if g['id'] == spec['game_id'])
        assert trace['spec'] == spec and trace['game'] == game
        forecast = read_json(out/'forecasts'/(spec['id']+'.json'))
        assert forecast['messages'] == forecast_messages(game,spec)
        for attempt in forecast['attempts']:
            call = read_json(out/'calls/kimi-k3'/(attempt['meta']['call_id']+'.json'))
            assert call['request']['messages'] == forecast['messages']
            assert call['config'] == manifest['models']['kimi-k3']
            assert call['timestamp'] < freeze['frozen_at']
            raw_calls.append(call)
        assert call['status'] == 'ok' and call['response']['choices'][0]['message']['content'] == forecast['attempts'][-1]['reply']
        joint = forecast['joint']
        predicted = [joint[0]+joint[1],joint[0]+joint[2]]
        direct_brier = mean((predicted[p] - int(t['actions'][p] == 0))**2 for t in trace['rounds'] for p in range(2))
        raw_scores[game['condition']].append(direct_brier)
        by_game.setdefault(game['id'],[]).append(trace)
        for index,t in enumerate(trace['rounds']):
            x,y = t['actions']
            # Independent lookup directly from each player's own schedule.
            assert t['payoffs'] == [SCHEDULES[game['schedules'][0]][x][y],SCHEDULES[game['schedules'][1]][y][x]]
            for player in range(2):
                item = read_json(out/'episodes'/spec['id']/f'round-{index+1:02}-player-{player}.json')
                for attempt in item['attempts']:
                    call = read_json(out/'calls'/spec['models'][player]/(attempt['meta']['call_id']+'.json'))
                    assert call['timestamp'] > freeze['frozen_at']
                    assert call['request']['messages'] == item['messages']
                    assert call['config'] == manifest['models'][spec['models'][player]]
                    assert call['request']['max_tokens'] == 4096 and call['request']['temperature'] == .7
                    raw_calls.append(call)
                assert call['status'] == 'ok'
                choice = call['response']['choices'][0]
                assert choice['finish_reason'] == 'stop' and not choice['message'].get('refusal')
                assert choice['message']['content'] == item['attempts'][-1]['reply']
        assert len(trace['rounds']) == 8
    for condition,values in raw_scores.items():
        assert abs(mean(values)-summary['scores'][condition]['kimi']['event_brier']) < 1e-12
    cells = read_json(out/'analysis-cells.json')
    games = []
    for game in manifest['games']:
        traces = by_game[game['id']]
        assert len(traces) == 4
        assert len({(tuple(t['spec']['models']),t['spec']['swap']) for t in traces}) == 4
        turns = [t for trace in traces for t in trace['rounds']]
        rate0 = [mean(t['actions'][p] == 0 for t in turns) for p in range(2)]
        switch = mean(trace['rounds'][i]['actions'][p] != trace['rounds'][i-1]['actions'][p]
                      for trace in traces for i in range(1,8) for p in range(2))
        games.append(dict(id=game['id'],condition=game['condition'],pure_nash_count=len(game['pure_nash']),
                          action0_rates=rate0,absolute_role_gap=abs(rate0[0]-rate0[1]),switch_rate=switch,
                          joint_rates=[mean(t['actions']==[x,y] for t in turns) for x,y in ((0,0),(0,1),(1,0),(1,1))],
                          **{method+'_brier':mean(c['event_brier'] for c in cells if c['game_id']==game['id'] and c['method']==method)
                             for method in ('kimi','stage_nash')}))
    write_json(out/'game-summary.json',games)
    dynamics = {cond:{'switch_rate':mean(g['switch_rate'] for g in games if g['condition']==cond),
                     'absolute_role_gap':mean(g['absolute_role_gap'] for g in games if g['condition']==cond)}
                for cond in ('symmetric','asymmetric')}
    audit = dict(audited_at=now(),episodes=64,rounds=512,actions=1024,forecasts=64,
                 forecast_freeze=freeze['frozen_at'],first_player_call=min(c['timestamp'] for c in raw_calls if c['purpose']=='play'),
                 source_files_verified=len(manifest['sources']),raw_calls=len(raw_calls),
                 call_states=dict(Counter(c['status'] for c in raw_calls)),
                 checks=['source snapshots unchanged','forecast hash and before-play chronology','complete role/label balance',
                         'individual payoff schedules match observed payouts','raw response/action consistency',
                         'player model configuration and prompt provenance','independent event Brier recomputation'],
                 readout_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),dynamics=dynamics)
    write_json(out/'AUDIT.json',audit)

    names = list(SCHEDULES)
    titles = ['PD','Harmony','Stag hunt','Chicken']
    index = {g['id']:g for g in games}
    fig,axes = plt.subplots(1,3,figsize=(13,4.5),layout='constrained')
    for ax,field,title,limit in zip(axes,['kimi_brier','stage_nash_brier','absolute_role_gap'],
                                   ['Kimi forecast error','Equilibrium forecast error','Difference between roles'],[.5,.5,1]):
        values = [[index[f'{x}__{y}'][field] for y in names] for x in names]
        im = ax.imshow(values,cmap='YlOrRd',vmin=0,vmax=limit)
        for i in range(4):
            for j in range(4):
                ax.text(j,i,f'{values[i][j]:.3f}',ha='center',va='center',color='white' if values[i][j]>limit*.65 else '#202020',fontsize=10)
            ax.add_patch(Rectangle((i-.48,i-.48),.96,.96,fill=False,edgecolor='#23659b',linewidth=2.5))
        ax.set(xticks=range(4),yticks=range(4),xticklabels=titles,yticklabels=titles,
               xlabel="Player 1's payoff schedule",ylabel="Player 0's payoff schedule",title=title)
        ax.tick_params(axis='x',rotation=30)
        fig.colorbar(im,ax=ax,shrink=.75,label='Brier score (lower is better)' if field.endswith('brier') else '|P₀(action 0) − P₁(action 0)|')
    fig.suptitle('Mixing player payoffs: 64 matches, 8 rounds each\nBlue outlines mark symmetric controls; each cell averages 4 matches',fontsize=13)
    fig.savefig(out/'payoff-grid.png',dpi=180)
    fig.savefig(out/'payoff-grid.svg')
    plt.close(fig)
    print(json.dumps(dict(audit=audit,games=games),indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    build(parser.parse_args().out)

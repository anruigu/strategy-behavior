"""Read-only views of the audited native TextArena catalog and model pilot."""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / 'general_games'


def read(path):
    return json.loads(path.read_text())


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def distribution(values):
    counts = Counter(json.dumps(value, sort_keys=True) for value in values)
    return [dict(value=json.loads(value), count=count) for value, count in sorted(counts.items())]


class GeneralDataset:
    def __init__(self, root=ROOT):
        self.root = Path(root).resolve()
        self.data = self.root / 'data/20260910-v1'
        self.run = self.root / 'runs/pilot-20260910'
        self.manifest = read(self.data / 'manifest.json')
        catalog = read(self.data / 'catalog.json')
        self.families = catalog['families']
        self.games = {g['configuration_id']: g for g in catalog['configurations']}
        self.instances = read(self.data / 'instances.evaluator.json')
        self.splits = read(self.data / 'splits.json')
        self.episodes = [dict(e,source_run='pilot-20260910') for e in rows(self.run / 'export/episodes.jsonl')]
        self.actions = rows(self.run / 'export/actions.jsonl')
        self.plan = {e['episode_id']: e for e in read(self.run / 'plan.json')['episodes']}
        extra=self.root/'runs/parameter-check-20260910'
        if (extra/'export/episodes.jsonl').exists():
            self.episodes += [dict(e,source_run='parameter-check-20260910') for e in rows(extra/'export/episodes.jsonl')]
            self.actions += rows(extra/'export/actions.jsonl')
            self.plan.update({e['episode_id']:e for e in read(extra/'plan.json')['episodes']})
        self.by_episode = {e['episode_id']: e for e in self.episodes}
        self.audit = read(self.run / 'export/audit.json')

    def summary(self, args=None):
        args = args or {}
        def arg(name): return args.get(name, [''])[0]
        family, players, model, prompt = (arg(k) for k in ('family', 'players', 'model', 'prompt'))
        cohort=arg('cohort') or 'pilot-20260910'
        games = [g for g in self.games.values() if (not family or g['family_id'] == family)
                 and (not players or str(g['num_players']) == players)]
        ids = {g['configuration_id'] for g in games}
        instances = [i for i in self.instances if i['configuration_id'] in ids]
        episodes = [e for e in self.episodes if e['status'] == 'complete' and e['inputs']['game_id'] in ids
                    and (cohort=='all' or e['source_run']==cohort)
                    and (not model or e['inputs']['player']['model_id'] == model)
                    and (not prompt or e['inputs']['context']['prompt_condition'] == prompt)]
        eids = {e['episode_id'] for e in episodes}
        actions = [a for a in self.actions if a['episode_id'] in eids]
        family_rows = []
        for fid, f in self.families.items():
            configs = [g for g in games if g['family_id'] == fid]
            if not configs: continue
            observed = [e for e in episodes if e['inputs']['family_id'] == fid]
            family_rows.append(dict(id=fid, title=f['title'], category=f['category'], players=f['num_players'],
                information=f['information'], objective=f['objective'], configurations=len(configs),
                instances=sum(i['family_id'] == fid for i in instances), episodes=len(observed),
                varied_parameters=[key for key, values in f['axes'].items() if len(values) > 1]))
        cohorts = []
        for name in ('qwen-3.8-27b', 'glm'):
            for condition in ('normal', 'active_exploration'):
                group = [e for e in episodes if e['inputs']['player']['model_id'] == name
                         and e['inputs']['context']['prompt_condition'] == condition]
                if not group: continue
                group_ids = {e['episode_id'] for e in group}
                aa = [a for a in actions if a['episode_id'] in group_ids]
                cohorts.append(dict(model=name, prompt=condition, episodes=len(group), actions=len(aa), invalid=sum(not a['valid'] for a in aa)))
        outcomes = []
        for f in family_rows:
            group = [e for e in episodes if e['inputs']['family_id'] == f['id']]
            won = sum(e['labels']['outcome']['win'] is True for e in group)
            draw = sum(e['labels']['outcome']['draw'] is True for e in group)
            outcomes.append(dict(family=f['title'], players=f['players'], episodes=len(group), win=won, draw=draw, loss=len(group)-won-draw))
        measurements = []
        for key, label in [('cooperation_rate', 'Cooperation · Prisoner’s Dilemma'),
                           ('defection_rate', 'Defection · Prisoner’s Dilemma'),
                           ('risk_taking_rate', 'Risk-taking · Pig Dice')]:
            values = [e['labels']['behavior'][key] for e in episodes]
            denominator = sum(v['denominator'] for v in values)
            numerator = sum(v['numerator'] or 0 for v in values)
            measurements.append(dict(label=label, numerator=numerator if denominator else None,
                denominator=denominator, value=numerator/denominator if denominator else None))
        partitions = []
        for key, label, units, groups in (
                ('family_id', 'Family holdout', 'families', {g['family_id'] for g in games}),
                ('configuration_id', 'Configuration holdout', 'configurations', ids),
                ('opening_group', 'Opening holdout', 'distinct openings', {i['opening_group'] for i in instances})):
            counts = Counter(self.splits[key][g] for g in groups)
            partitions.append(dict(label=label, unit=units, counts={k:counts[k] for k in ('train','validation','test')}))
        catalog_rows = []
        for g in sorted(games, key=lambda g: (g['family_id'], g['intervention_axis'] is not None, g['configuration_id'])):
            catalog_rows.append(dict(id=g['configuration_id'], family=g['family_id'], title=self.families[g['family_id']]['title'],
                parameters=g['parameters'], axis=g['intervention_axis'], players=g['num_players'],
                episodes=sum(e['inputs']['game_id'] == g['configuration_id'] for e in episodes)))
        return dict(
            counts=dict(families=len(family_rows), configurations=len(games), instances=len(instances),
                distinct_openings=len({i['opening_group'] for i in instances}), episodes=len(episodes), actions=len(actions),
                invalid_actions=sum(not a['valid'] for a in actions)),
            total=dict(families=len(self.families), configurations=len(self.games), instances=len(self.instances), episodes=len(self.episodes)),
            all_families=[dict(id=fid,title=f['title']) for fid,f in self.families.items()], families=family_rows, catalog=catalog_rows,
            parameters={key:distribution(g['parameters'][key] for g in games if key in g['parameters'])
                        for key in sorted({key for g in games for key in g['parameters']})},
            players=distribution(g['num_players'] for g in games),
            information=distribution(g['structured']['information'] for g in games),
            episode_lengths=distribution(e['labels']['focal_actions'] for e in episodes),
            cohorts=cohorts, outcomes=outcomes, measurements=measurements, partitions=partitions,
            audit=dict(status=self.audit['status'], replayed_transitions=self.audit['replayed_transitions'],
                reconciled_calls=self.audit['reconciled_attempt_calls'],reported_cost_usd=self.audit['reported_cost_usd']),
            cohort=cohort,version=self.manifest['version'], textarena_version=self.manifest['environment']['textarena_version'])

    def checks(self):
        path=self.root/'evaluation/results-20260910/summary.json'
        return read(path) if path.exists() else dict(status='pending')

    def game(self, ident):
        game = self.games[ident]
        instances = [i for i in self.instances if i['configuration_id'] == ident]
        episodes = [e for e in self.episodes if e['inputs']['game_id'] == ident]
        return dict(game=game, family=self.families[game['family_id']], seeds=[i['seed'] for i in instances],
            example=dict(seed=instances[0]['seed'], observations=instances[0]['opening_observations']),
            episodes=[dict(id=e['episode_id'], model=e['inputs']['player']['model_id'],
                prompt=e['inputs']['context']['prompt_condition'], seat=e['inputs']['role']['seat_id'],
                source_run=e['source_run'],status=e['status'], actions=e['labels']['focal_actions'], outcome=e['labels']['outcome']) for e in episodes])

    def episode(self, ident):
        item = self.plan[ident]  # Resolve paths only through known episode IDs.
        record = read(self.root/'runs'/self.by_episode[ident]['source_run']/'episodes'/(item['episode_id']+'.json'))
        return dict(id=ident, item=item, status=record['status'], labels=self.by_episode[ident]['labels'],
            steps=[{key:step[key] for key in ('index','actor','is_focal','raw_action','result','before','after','incoming','messages') if key in step}
                   for step in record['steps']],
            retries=sum(len(attempts)-1 for attempts in record['attempts'].values()))

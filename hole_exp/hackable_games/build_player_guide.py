"""Generate the public HTML guide and a readable Markdown copy from UI help."""
from pathlib import Path
import html
import re
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));sys.path.insert(0,str(HERE.parent))
from views.scaleup_help import GUIDES
from engines_scaleup_20260907 import GAMES


def build():
    esc=html.escape
    intro=('Each game is a small, custom scenario with its own rules. You control one player; the other players are scripted. '
           'Choose one action panel, fill its required fields and press that panel’s button. You do not need to fill every panel. '
           'Submitting spends a turn, including requests such as reviews or connection changes. Reading this guide and opening explanations do not spend turns. '
           'An unavailable or malformed action can still use a turn: check the explanation and Last resolution. '
           'Blank optional fields mean you are not making that extra request. After a play, you can stop and choose another game; you do not need to finish all four repeats.')
    md=['# How to play the ten V2 games','',intro,'',
        'These explanations describe the stated rules and control meanings. Start with the goal, the turn structure and one ordinary action. Use the full rules and Last resolution to follow what happened.','']
    parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V2 game guide · Plays</title>',
    '''<style>body{font-family:system-ui,sans-serif;background:#14171c;color:#e5e9ef;max-width:900px;margin:auto;padding:24px;line-height:1.65}a{color:#a9c6ff}h1{font-size:2rem}h2{margin-top:48px}h3{color:#c4cee0}nav{display:flex;flex-wrap:wrap;gap:10px 22px;padding:20px 0}section{border-top:1px solid #36404b;scroll-margin-top:20px}dt{font-weight:650;margin-top:18px}dd{margin:4px 0 18px;color:#c0c9d7}.goal{background:#222934;border-radius:12px;padding:18px}.example{color:#b4c9ed}.back{display:inline-block;margin:12px 0}p{max-width:78ch}strong{color:#f0f3f8}@media(max-width:500px){body{padding:16px}h1{font-size:1.65rem}.goal{padding:14px}}</style>''',
    '<a href="/?version=v2">← Back to the games</a><h1>How to play the ten V2 games</h1>',f'<p>{esc(intro)}</p>',
    '<p>These explanations describe the stated rules and control meanings. Start with the goal, the turn structure and one ordinary action. Use the full rules and Last resolution to follow what happened.</p>',
    '<nav aria-label="Games">'+''.join(f'<a href="#{gid}">{esc(g["title"])}</a>' for gid,g in GUIDES.items())+'</nav>']
    for gid,g in GUIDES.items():
        md += [f'## {g["title"]}','',f'**Goal:** {g["goal"]}','',f'**Your turn:** {g["turn"]}','',f'**Getting started:** {g["start"]}','','### Terms','']
        parts += [f'<section id="{gid}"><h2>{esc(g["title"])}</h2><div class="goal"><p><strong>Goal:</strong> {esc(g["goal"])}</p><p><strong>Your turn:</strong> {esc(g["turn"])}</p><p><strong>Getting started:</strong> {esc(g["start"])}</p></div><h3>Terms</h3><dl>']
        for term,meaning in g['terms'].items():
            md.append(f'- **{term}:** {meaning}');parts.append(f'<dt>{esc(term)}</dt><dd>{esc(meaning)}</dd>')
        md += ['','### Buttons','','| Button | Meaning | What to enter |','|---|---|---|'];parts.append('</dl><h3>Buttons</h3><dl>')
        for a in GAMES[gid].FORMS:
            key=a['fields'][0]['name'] if a['fields'] else re.search(r'\[([^:]+):',a['token'])[1]
            h=g['actions'][key];example=h['example'] or 'No entry needed; press the button.'
            md.append(f'| {a["label"]} | {h["help"]} | {example} |')
            parts.append(f'<dt>{esc(a["label"])}</dt><dd>{esc(h["help"])}<p class="example">{esc(example)}</p></dd>')
        md += [''];parts.append('</dl><a class="back" href="#">Back to the game list ↑</a></section>')
    parts.append('</html>');(HERE/'play/guide.html').write_text('\n'.join(parts)+'\n')
    md += ['## Optional research spoilers','',
      'After playing, compare your observations with the [60-instance research matrix](../benchmark/scaleup/artifacts/MATRIX.md) and [the exact witness sequences](../benchmark/scaleup/artifacts/specs.json). These contain the intended holes and answers. The public guide and in-game help omit that answer key.','']
    target=HERE.parents[1]/'docs/v2-player-guide.md';target.parent.mkdir(exist_ok=True);target.write_text('\n'.join(md))
    print('Built public guide and',target)

if __name__=='__main__':build()

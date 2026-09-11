"""Generate the public V3 guide (HTML) and a Markdown copy from the editions' own rules cards and form help."""
from pathlib import Path
import html
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
from engines_v3_public import EDITIONS


def render():
    esc = html.escape
    intro = ('Each edition is a short game with its own rules card: goal, your turn, scoring and rivals. You control one player; the others are scripted. '
             'Choose one action panel, fill its fields and press its button. Every action, including a request to the clerk, uses your turn. '
             'Editions of the same game share a board, but their rules, scoring and turn limits can differ; read the card for the edition you choose. '
             'Three plays per edition; you may stop after any play.')
    md = ['# How to play the V3 editions', '', intro, '']
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V3 game guide · Plays</title>',
             '''<style>body{font-family:system-ui,sans-serif;background:#14171c;color:#e5e9ef;max-width:900px;margin:auto;padding:24px;line-height:1.65}a{color:#a9c6ff}h1{font-size:2rem}h2{margin-top:48px}h3{color:#c4cee0}nav{display:flex;flex-wrap:wrap;gap:10px 22px;padding:20px 0}section{border-top:1px solid #36404b;scroll-margin-top:20px}dt{font-weight:650;margin-top:18px}dd{margin:4px 0 18px;color:#c0c9d7}.goal{background:#222934;border-radius:12px;padding:18px}.example{color:#b4c9ed}.back{display:inline-block;margin:12px 0}p{max-width:78ch}strong{color:#f0f3f8}@media(max-width:500px){body{padding:16px}h1{font-size:1.65rem}.goal{padding:14px}}</style>''',
             '<a href="/?version=v3">← Back to the games</a><h1>How to play the V3 editions</h1>', f'<p>{esc(intro)}</p>',
             '<nav aria-label="Editions">' + ''.join(f'<a href="#{g.NAME}">{esc(g.TITLE)}</a>' for g in EDITIONS) + '</nav>']
    for g in EDITIONS:
        c = g.CARD
        md += [f'## {g.TITLE}', '', f'**Goal:** {c["goal"]}', '', f'**Your turn:** {c["turn"]}', '', f'**Scoring:** {c["scoring"]}', '', f'**Rivals:** {c["rivals"]}', '', '### Buttons', '', '| Button | Meaning | What to enter |', '|---|---|---|']
        parts.append(f'<section id="{g.NAME}"><h2>{esc(g.TITLE)}</h2><div class="goal"><p><strong>Goal:</strong> {esc(c["goal"])}</p><p><strong>Your turn:</strong> {esc(c["turn"])}</p><p><strong>Scoring:</strong> {esc(c["scoring"])}</p><p><strong>Rivals:</strong> {esc(c["rivals"])}</p></div><h3>Buttons</h3><dl>')
        for a in g.forms():
            fields = '; '.join(f'{f["label"]}: ' + (', '.join((f.get('option_labels') or {}).get(o, o) for o in f['options']) if f['options'] else 'a number' if not f['text'] else 'text') for f in a['fields'])
            entry = a.get('example') or fields or 'No entry needed; press the button.'
            md.append(f'| {a["label"]} | {a.get("help", "")} | {entry} |')
            parts.append(f'<dt>{esc(a["label"])}</dt><dd>{esc(a.get("help", ""))}<p class="example">{esc(entry)}</p></dd>')
        md.append(''); parts.append('</dl><a class="back" href="#">Back to the list ↑</a></section>')
    parts.append('</html>')
    return '\n'.join(parts) + '\n', '\n'.join(md)


def build():
    page, markdown = render()
    (HERE / 'play/guide-v3.html').write_text(page)
    target = HERE.parents[1] / 'docs/v3-player-guide.md'; target.write_text(markdown)
    print('Built play/guide-v3.html and', target)


if __name__ == '__main__': build()

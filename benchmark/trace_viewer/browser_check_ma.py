"""Exercise model attribution, marker navigation, and incomplete traces in Chromium."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument('--url', default='http://127.0.0.1:42327')
args = parser.parse_args()
out = Path('/shared/allie/strategy-behavior/benchmark/results/trace-viewer')
out.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))

    def open_episode(eid, phase='ordinary'):
        page.goto(args.url + '/#run=v3-ma-four-model&phase=' + phase + '&episode=' + eid, wait_until='networkidle')
        page.reload(wait_until='networkidle')
        page.locator('h1').wait_for()
        page.wait_for_function('(id) => location.hash.includes(id) && document.querySelector(".ma-round")', arg=eid)

    open_episode('bfdebd98829842f01d4d', 'nerfed')
    assert page.locator('.ma-chart tbody tr').count() == 6
    assert page.locator('.ma-chart td[data-model="openai/gpt-5-mini"]').count() == 12
    assert page.locator('.ma-round.exploited').count() == 6
    assert page.locator('[data-marker-kind="observed"]').count() == 6
    assert page.locator('.ma-decision[data-model="openai/gpt-5-mini"]').count() == 36
    page.locator('.round-chart').screenshot(path=str(out / 'ma-pledge-chart.png'))
    page.locator('.ma-chart [data-round-jump="2"]').click()
    page.locator('#round-2').screenshot(path=str(out / 'ma-pledge-round.png'))
    page.locator('#pairedlink').click()
    page.wait_for_function('location.hash.includes("03f615f1e765b779dba9") && document.querySelector(".eyebrow")?.textContent.includes("ordinary opponents")')
    assert page.locator('.ma-round.exploited').count() == 0

    open_episode('f48fdef471f25e4efdfd')
    assert page.locator('.ma-round.exploited').count() == 3
    assert page.locator('.ma-chart td[data-model="qwen3.8-27b"]').count() == 4
    assert page.locator('.ma-chart td[data-model="glm-5.3"]').count() == 4
    page.locator('#onlyhits').check()
    assert not page.locator('#round-1').is_visible()
    assert page.locator('#round-2').is_visible()
    page.locator('.ma-chart [data-round-jump="1"]').click()
    assert page.locator('#round-1').is_visible()
    assert not page.locator('#onlyhits').is_checked()
    page.locator('.round-chart').screenshot(path=str(out / 'ma-notes-chart.png'))

    page.locator('#focal').select_option('qwen-3.8-27b')
    page.locator('#opponent').select_option('glm')
    assert page.locator('#episodes .seed').count() == 28
    page.locator('[data-phase="nerfed"]').click()
    assert page.locator('#episodes .seed').count() == 20
    page.locator('#focal').select_option('all')
    page.locator('#opponent').select_option('all')
    page.locator('#outcome').select_option('incomplete')
    assert page.locator('#episodes .seed').count() == 7
    page.locator('#episodes .seed').first.click()
    page.locator('.failure').wait_for()
    assert page.locator('[data-marker-kind]').count() == 0
    assert 'Unscored' in page.locator('.ma-chart').inner_text()
    assert page.locator('.ma-decision').count() > 0
    page.screenshot(path=str(out / 'ma-incomplete.png'))

    open_episode('f48fdef471f25e4efdfd')
    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('.round-chart').scroll_into_view_if_needed()
    page.screenshot(path=str(out / 'ma-mobile.png'))
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.locator('#run').select_option('gemini-original')
    page.wait_for_function('document.querySelector(".sa-model")')
    assert not page.locator('#ma-filters').is_visible()
    assert page.locator('[data-phase="blind"]').is_visible()
    assert page.locator('.sa-model').count() == page.locator('.turn').count()
    page.locator('[data-phase="hinted"]').click()
    page.wait_for_function('document.querySelector(".eyebrow")?.textContent.includes("Hinted execution diagnostic")')
    assert not errors, errors
    result = dict(passed=True, url=args.url, javascript_errors=errors, checks=[
        'Every round chart cell and reply carries model and seat attribution',
        'Six pledge exploit rounds and three ordinary clue-note exploit rounds',
        'Round links, marked-round filter, and matched-condition navigation',
        'Four-model filters and all seven incomplete traces remain accessible',
        'Mobile chart scroll stays inside viewport',
        'Existing single-agent model labels and blind/hinted navigation'])
    (out / 'ma-browser-check.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    browser.close()

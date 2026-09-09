"""Verify the deployed V3 discovery surface in a fresh browser session."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1440, 'height': 1100})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('https://strategy-behavior.flt.build/?version=v3', wait_until='networkidle')
    page.locator('#player').fill('discovery-surface-verification-20260909')
    page.locator('#namebox button').click()
    page.locator('#grid .card').filter(has_text='Commons · Neighbours').click()
    page.get_by_role('button', name='Deposit silt', exact=True).wait_for()
    initial = page.locator('body').inner_text()
    assert 'The habitat officer keeps landings open' in initial
    assert 'three seasons' not in initial
    assert 'each rival loses 6 fish' not in initial
    page.screenshot(path=str(OUT / 'commons-before.png'), full_page=True)
    page.get_by_role('button', name='Deposit silt', exact=True).click()
    page.get_by_text('Rival landings are closed for three seasons.', exact=False).wait_for()
    page.screenshot(path=str(OUT / 'commons-after.png'), full_page=True)
    guide = page.request.get('https://strategy-behavior.flt.build/guide-v3').text()
    assert 'Silt the rival landing sites for three seasons' not in guide
    assert 'Scuttling costs 1 point and blasts' not in guide
    assert 'each rival loses 6 fish' not in guide
    assert not errors, errors
    (OUT / 'public-verification.json').write_text(json.dumps(dict(
        url=page.url, initial_help_no_effect_disclosure=True,
        post_action_effect_visible=True, guide_checked=True, javascript_errors=errors), indent=2)+'\n')
    print('PASS public V3: fresh Commons game hides effects before acting; closure feedback appears after silting; guide matches; no JS errors.')
    browser.close()

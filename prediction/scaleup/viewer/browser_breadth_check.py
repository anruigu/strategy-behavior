"""Exercise family filters, exact trajectories and mobile layout."""
from pathlib import Path
import json,os,sys
HERE=Path(__file__).resolve().parent; STATE=HERE/'state'
os.environ.update(TMPDIR='/shared/allie/home/.codex/tmp',XDG_CACHE_HOME=str(STATE/'browser-cache'),XDG_CONFIG_HOME=str(STATE/'browser-config'),LD_LIBRARY_PATH='/shared/allie/home/.codex/tmp/trace-viewer-libs/root/usr/lib/x86_64-linux-gnu',FONTCONFIG_FILE=str(STATE/'fonts.conf'))
sys.path.insert(0,str(HERE.parents[1]/'dataset_viewer/.deps'))
from playwright.sync_api import sync_playwright,expect

url='http://127.0.0.1:42329'; errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/shared/allie/home/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport=dict(width=1440,height=1000)); page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url+'/general/breadth',wait_until='networkidle')
    expect(page.locator('.family-card')).to_have_count(18); expect(page.locator('[data-role="Holdout"]')).to_have_count(6)
    expect(page.locator('#progress .progress-block')).to_have_count(4)
    page.select_option('#cohort','depth'); expect(page.locator('#metrics')).to_contain_text('288')
    page.select_option('#cohort','breadth'); expect(page.locator('#metrics')).to_contain_text('288')
    page.select_option('#cohort','test'); expect(page.locator('#metrics')).to_contain_text('144')
    page.select_option('#family','gops'); expect(page.locator('.family-card')).to_have_count(1); expect(page.locator('#metrics')).to_contain_text('24')
    page.locator('.family-card').click(); expect(page.locator('#detail')).to_contain_text('GameOfPureStrategy')
    page.select_option('#family','blind_auction'); page.select_option('#cohort','all'); page.locator('.family-card').click()
    expect(page.locator('#episode option')).not_to_have_count(1)
    page.select_option('#episode',index=1); expect(page.locator('#trajectory')).to_contain_text('native transitions'); expect(page.locator('#trajectory')).to_contain_text('Exact actor prompt')
    page.select_option('#family',''); expect(page.locator('.family-card')).to_have_count(18)
    data=page.request.get(url+'/api/general/breadth/summary').json()
    if data['results']:
        expect(page.locator('#results')).to_be_visible(); expect(page.locator('#scores tbody tr')).to_have_count(6)
        page.select_option('#target','native_score'); expect(page.locator('#comparison')).to_contain_text('breadth − depth')
        page.select_option('#target','win'); page.locator('#learning').screenshot(path=str(STATE/'breadth-learning.png'))
    page.screenshot(path=str(STATE/'breadth-overview.png'),full_page=True)
    page.set_viewport_size(dict(width=390,height=844)); page.screenshot(path=str(STATE/'breadth-mobile.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Mobile horizontal overflow'
    assert not errors,errors
    browser.close()
print(json.dumps(dict(status='passed',results_available=bool(data['results']),console_errors=errors)))

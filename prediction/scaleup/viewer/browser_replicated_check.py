"""Exercise live study filters, native samples, and responsive layout."""
from pathlib import Path
import json,os,sys
HERE=Path(__file__).resolve().parent;STATE=HERE/'state'
os.environ.update(TMPDIR='/shared/allie/home/.codex/tmp',XDG_CACHE_HOME=str(STATE/'browser-cache'),XDG_CONFIG_HOME=str(STATE/'browser-config'),LD_LIBRARY_PATH='/shared/allie/home/.codex/tmp/trace-viewer-libs/root/usr/lib/x86_64-linux-gnu',FONTCONFIG_FILE=str(STATE/'fonts.conf'))
sys.path.insert(0,str(HERE.parents[1]/'dataset_viewer/.deps'))
from playwright.sync_api import sync_playwright,expect
url='http://127.0.0.1:42329';errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/shared/allie/home/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport=dict(width=1440,height=1000));page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(url+'/general/replicated',wait_until='networkidle')
    expect(page.locator('.family-tile')).to_have_count(16);expect(page.locator('.new-family')).to_have_count(4)
    expect(page.locator('#progress .progress-item')).to_have_count(5)
    page.select_option('#cohort','legacy');expect(page.locator('#metrics')).to_contain_text('144');expect(page.locator('#metrics')).to_contain_text('779')
    page.select_option('#cohort','training');expect(page.locator('#metrics')).to_contain_text('320');expect(page.locator('#family-chart .distribution-row')).to_have_count(4)
    page.select_option('#family','prisoners_dilemma');expect(page.locator('.family-tile')).to_have_count(1);expect(page.locator('#metrics')).to_contain_text('80')
    page.locator('#game-list button').filter(has_text='"defect_reward":5').first.click()
    expect(page.locator('#sample-detail')).to_contain_text('Actual model episodes');page.select_option('#episode-select',index=1)
    expect(page.locator('#trajectory')).to_contain_text('native transitions');expect(page.locator('.episode-turn').first).to_contain_text('Exact model messages')
    page.select_option('#family','memory');page.locator('#game-list button').first.click();expect(page.locator('#sample-detail')).to_contain_text('MemoryGame')
    page.select_option('#family','');page.select_option('#cohort','all');expect(page.locator('.family-tile')).to_have_count(16)
    results=page.request.get(url+'/api/general/replicated/summary').json().get('results')
    if results:
        expect(page.locator('#result-content')).to_be_visible();expect(page.locator('#score-table tbody tr')).to_have_count(11)
        page.select_option('#suite','family');expect(page.locator('#comparison')).to_contain_text('family-bootstrap')
        page.select_option('#target','offer_share');expect(page.locator('#score-table tbody tr')).to_have_count(9)
        page.select_option('#target','win');page.locator('#learning').screenshot(path=str(STATE/'replicated-learning.png'))
    page.screenshot(path=str(STATE/'replicated-overview.png'),full_page=True)
    page.set_viewport_size(dict(width=390,height=844));page.screenshot(path=str(STATE/'replicated-mobile.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Mobile horizontal overflow'
    assert not errors,errors
    browser.close()
print(json.dumps(dict(status='passed',results_available=bool(results),console_errors=errors)))

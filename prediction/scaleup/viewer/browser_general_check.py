from pathlib import Path
import json
import os
import sys

HERE=Path(__file__).resolve().parent; STATE=HERE/'state'
os.environ['TMPDIR']='/shared/allie/home/.codex/tmp'
os.environ['XDG_CACHE_HOME']=str(STATE/'browser-cache')
os.environ['XDG_CONFIG_HOME']=str(STATE/'browser-config')
os.environ['LD_LIBRARY_PATH']='/shared/allie/home/.codex/tmp/trace-viewer-libs/root/usr/lib/x86_64-linux-gnu'
os.environ['FONTCONFIG_FILE']=str(STATE/'fonts.conf')
sys.path.insert(0,str(HERE.parents[1]/'dataset_viewer/.deps'))
from playwright.sync_api import sync_playwright,expect

url='http://127.0.0.1:42329'
chrome='/shared/allie/home/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell'
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=chrome,headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport=dict(width=1440,height=1000),accept_downloads=True)
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(url+'/general',wait_until='networkidle')
    expect(page.locator('.family-tile')).to_have_count(12)
    expect(page.locator('#metrics')).to_contain_text('477')
    expect(page.locator('#family-chart .distribution-row')).to_have_count(12)
    expect(page.locator('#cohorts tbody tr')).to_have_count(4)
    expect(page.locator('.check-verdict')).to_have_count(5)
    expect(page.locator('#check-forecast tbody tr')).to_have_count(9)
    expect(page.locator('#check-forecast')).to_contain_text('0.1456')
    page.select_option('#check-family','pig_dice')
    expect(page.locator('#check-parameter')).to_contain_text('13.25')
    page.select_option('#check-target','cooperation_rate')
    expect(page.locator('#check-forecast')).to_contain_text('MSE')
    page.select_option('#check-suite','family')
    expect(page.locator('#check-forecast')).to_contain_text('not defined')
    page.select_option('#check-target','win')
    expect(page.locator('#check-forecast')).to_contain_text('0.2056')
    page.locator('#checks').screenshot(path=str(STATE/'general-checks.png'))
    page.select_option('#check-suite','parameter')
    page.screenshot(path=str(STATE/'general-overview.png'),full_page=True)
    page.locator('[data-inspect-family="connect_four"]').click()
    expect(page.locator('#sample-detail h2')).to_have_text('Connect Four')
    expect(page.locator('#native-rules')).to_contain_text('four discs')
    page.locator('#episode').select_option(index=1)
    expect(page.locator('#episode-content')).to_contain_text('focal seat')
    expect(page.locator('#turn-content')).to_contain_text('SUBMITTED ACTION')
    page.get_by_text('Exact model input before this action',exact=True).click()
    expect(page.locator('pre.prompt').first).to_contain_text('primary objective')
    page.locator('#native-turns button').last.click()
    sample_url=page.url
    page.reload(wait_until='networkidle')
    expect(page.locator('#turn-content')).to_contain_text('SUBMITTED ACTION')
    with page.expect_download() as download:
        page.locator('#download-episode').click()
    download.value.save_as(str(STATE/'general-sample.json'))
    page.screenshot(path=str(STATE/'general-sample.png'),full_page=True)
    variant=page.request.get(url+'/api/general/summary?family=connect_four').json()['catalog'][1]['id']
    page.locator(f'[data-game="{variant}"]').click()
    expect(page.locator('#sample-detail')).to_contain_text('No model episodes for this configuration')
    page.locator('#reset').click()
    page.select_option('#players','1')
    expect(page.locator('.family-tile')).to_have_count(3)
    page.select_option('#model','qwen-3.8-27b')
    page.select_option('#prompt','normal')
    expect(page.locator('#cohorts tbody tr')).to_have_count(1)
    expect(page.locator('#cohorts')).to_contain_text('6')
    page.locator('#reset').click()
    expect(page.locator('.family-tile')).to_have_count(12)
    page.select_option('#cohort','parameter-check-20260910')
    expect(page.locator('#metrics')).to_contain_text('302')
    page.locator('[data-inspect-family="prisoners_dilemma"]').click()
    expect(page.locator('#sample-detail h2')).to_contain_text('Dilemma')
    sweep=page.request.get(url+'/api/general/summary?cohort=parameter-check-20260910&family=prisoners_dilemma').json()
    variant=next(g['id'] for g in sweep['catalog'] if g['episodes'])
    page.locator(f'[data-game="{variant}"]').click()
    page.locator('#episode').select_option(index=1)
    expect(page.locator('#turn-content')).to_contain_text('SUBMITTED ACTION')
    page.reload(wait_until='networkidle')
    expect(page.locator('#turn-content')).to_contain_text('SUBMITTED ACTION')
    expect(page.locator('#cohort')).to_have_value('parameter-check-20260910')
    page.locator('#reset').click()
    page.select_option('#cohort','all')
    expect(page.locator('#metrics')).to_contain_text('779')
    page.locator('#reset').click()
    with page.expect_download() as download:
        page.locator('#download-summary').click()
    download.value.save_as(str(STATE/'general-distributions.json'))
    page.set_viewport_size(dict(width=390,height=844))
    page.screenshot(path=str(STATE/'general-mobile.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Mobile horizontal overflow'
    page.locator('[data-inspect-family="wordle"]').click()
    expect(page.locator('#sample-detail h2')).to_have_text('Wordle')
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Mobile sample overflow'
    page.goto(url,wait_until='networkidle')
    expect(page.locator('#metrics')).to_contain_text('6,056')
    expect(page.locator('.dataset-switch a[href="/general"]')).to_be_visible()
    assert not errors,errors
    browser.close()
result=dict(status='passed',errors=errors,sample_url=sample_url,checks=['12 family cards','distribution totals','cohort filters','native rules','trajectory inputs','sample reload','JSON downloads','uncollected variants','mobile layout','dataset switch','five validation verdicts','prediction holdout and target selectors','supported-target missingness','new parameter trajectories','144-episode combined cohort'])
(STATE/'general-browser-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

"""Exercise the live viewer with the existing shared headless Chromium."""
from pathlib import Path
import json
import os
import sys
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parent
STATE=ROOT/'state'
os.environ['TMPDIR']='/shared/allie/home/.codex/tmp'
os.environ['XDG_CACHE_HOME']=str(STATE/'browser-cache')
os.environ['XDG_CONFIG_HOME']=str(STATE/'browser-config')
os.environ['LD_LIBRARY_PATH']='/shared/allie/home/.codex/tmp/trace-viewer-libs/root/usr/lib/x86_64-linux-gnu'
font_config=STATE/'fonts.conf'
font_config.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
    '<dir>/shared/allie/strategy-behavior/benchmark/trace_viewer</dir>'
    f'<cachedir>{STATE}/font-cache</cachedir></fontconfig>')
os.environ['FONTCONFIG_FILE']=str(font_config)
sys.path.insert(0,str(ROOT/'.deps'))
from playwright.sync_api import sync_playwright,expect

meta=json.loads((STATE/'server.json').read_text())
url='http://127.0.0.1:'+str(meta['port'])
chrome=Path('/shared/allie/home/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell')
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=str(chrome),headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1050})
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(url,wait_until='networkidle')
    expect(page.locator('#main h2')).to_contain_text('development-g')
    expect(page.locator('#counts')).to_contain_text('1,488 contexts')
    expect(page.locator('#tab-content pre.prompt')).to_contain_text('Predict behavior before an eight-round')
    page.screenshot(path=str(STATE/'viewer-input.png'),full_page=False)
    page.select_option('#partition','development')
    expect(page.locator('#matches')).to_have_text('336 contexts')
    expect(page.locator('#main h2')).to_contain_text('prospective-g')
    page.get_by_role('tab',name='Targets & forecasts').click()
    expect(page.locator('#fold')).to_have_value('full')
    expect(page.locator('.data-table').first.locator('tbody tr')).to_have_count(11)
    expect(page.locator('#tab-content')).to_contain_text('Kimi few-shot')
    page.screenshot(path=str(STATE/'viewer-targets.png'),full_page=False)
    page.select_option('#model','gpt-oss-20b')
    page.select_option('#opponent','kimi-k3')
    expect(page.locator('#matches')).to_have_text('21 contexts')
    page.get_by_role('tab',name='Player inputs & outputs').click()
    expect(page.locator('.decisions')).to_be_visible()
    expect(page.locator('.response')).to_have_count(2)
    page.get_by_role('button',name='Round 8',exact=True).click()
    expect(page.locator('.round-button.active')).to_have_attribute('data-round','8')
    expect(page.locator('.decision').first.locator('pre.prompt').nth(1)).to_contain_text('This is round 8 of 8')
    assert all(s.strip() in ('A','B') for s in page.locator('.response b').all_text_contents())
    shared=page.url
    page.reload(wait_until='networkidle')
    expect(page.locator('.round-button.active')).to_have_attribute('data-round','8')
    page.screenshot(path=str(STATE/'viewer-traces.png'),full_page=False)
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path=str(STATE/'viewer-mobile.png'),full_page=False)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Mobile horizontal overflow'
    page.locator('#search').fill('no-such-game-xxxxxxxx')
    expect(page.locator('#matches')).to_have_text('0 contexts')
    expect(page.locator('#main')).to_contain_text('No contexts match')
    page.locator('#reset').click()
    expect(page.locator('#matches')).to_have_text('1,488 contexts')
    expect(page.locator('#main h2')).to_be_visible()
    assert not errors,errors
    browser.close()
result=dict(status='passed',port=meta['port'],checks=['initial input','development filter','all10 development methods',
    'ordered player-pair filters','both raw player prompts and outputs','round8 public history','shareable reload',
    'mobile width','empty search and reset','no JavaScript errors'],errors=errors,example_url=shared)
(STATE/'browser-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

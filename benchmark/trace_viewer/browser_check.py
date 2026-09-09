from playwright.sync_api import sync_playwright
from pathlib import Path
out=Path('/shared/allie/strategy-behavior/benchmark/results/trace-viewer')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1000});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto('http://127.0.0.1:42327',wait_until='networkidle')
    page.locator('h1').wait_for();assert page.locator('#run').input_value()=='gemini-original'
    page.locator('[data-phase="hinted"]').click();page.wait_for_function("document.querySelector('.eyebrow')?.textContent.includes('Hinted execution diagnostic')")
    page.goto('http://127.0.0.1:42327/#run=gemini-original&phase=hinted&episode=hinted__v3_gen_seven_seal_certificates.resource_duplication__s19')
    page.reload(wait_until='networkidle');page.locator('h1').wait_for()
    assert page.locator('.annotation').count()>=7
    page.locator('#onlyhits').check();assert not page.locator('#turn-1').is_visible();assert page.locator('#turn-2').is_visible()
    page.locator('#onlyhits').uncheck();page.screenshot(path=str(out/'viewer-desktop.png'),full_page=False)
    page.locator('#blindlink').click();page.wait_for_function("document.querySelector('.eyebrow')?.textContent.includes('Original blind condition')")
    assert page.locator('.seed.selected').count()==1
    page.locator('#run').select_option('gemini-3.7-flash');page.wait_for_function("document.querySelector('.eyebrow')?.textContent.includes('matched / low')")
    page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(out/'viewer-mobile.png'),full_page=False)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert not errors,errors
    print('PASS browser: original Gemini, hinted annotations, exploit filter, blind link, model switching, mobile layout; no JS errors')
    browser.close()

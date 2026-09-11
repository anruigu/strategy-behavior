"""Check the assessment panel and downloads using the existing shared browser."""
import json
import os
from pathlib import Path
import sys

from .data import OUT, PACKAGE, write

state = OUT/"browser"
state.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = "/shared/allie/home/.codex/tmp"
os.environ["XDG_CACHE_HOME"] = str(state/"cache")
os.environ["XDG_CONFIG_HOME"] = str(state/"config")
os.environ["LD_LIBRARY_PATH"] = "/shared/allie/home/.codex/tmp/trace-viewer-libs/root/usr/lib/x86_64-linux-gnu"
os.environ["FONTCONFIG_FILE"] = str(PACKAGE/"viewer/state/fonts.conf")
sys.path.insert(0, str(PACKAGE.parent/"dataset_viewer/.deps"))
from playwright.sync_api import sync_playwright, expect

errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/shared/allie/home/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell", headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport=dict(width=1440, height=1050), accept_downloads=True)
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto("http://127.0.0.1:42329/#assessment-section", wait_until="networkidle")
    expect(page.locator("#assessment-section")).to_be_visible()
    expect(page.locator("#assessment-cards article")).to_have_count(5)
    expect(page.locator("#assessment-scores tbody tr")).to_have_count(10)
    expect(page.locator("#assessment-scope")).to_contain_text("retrospective")
    for img in page.locator("#assessment-section img").all():
        img.scroll_into_view_if_needed()
        expect(img).to_be_visible()
        page.wait_for_function("Array.from(document.querySelectorAll('#assessment-section img')).every(i=>i.complete && i.naturalWidth>0)")
    page.locator("#assessment-section").screenshot(path=str(state/"assessment-desktop.png"))
    with page.expect_download() as download:
        page.get_by_role("link", name="Full assessment").click()
    download.value.save_as(str(state/"downloaded-assessment.md"))
    for route in ("/figures/assessment-behavior.pdf", "/figures/assessment-prediction.pdf"):
        response = page.request.get("http://127.0.0.1:42329"+route)
        assert response.ok and response.body().startswith(b"%PDF")
    page.set_viewport_size(dict(width=390, height=844))
    page.locator("#assessment-section").scroll_into_view_if_needed()
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth"), "Assessment mobile overflow"
    page.screenshot(path=str(state/"assessment-mobile.png"))
    page.select_option("#family", "shared_fishery")
    expect(page.locator("#assessment-section")).to_be_hidden()
    page.select_option("#family", "")
    expect(page.locator("#assessment-section")).to_be_visible()
    assert not errors, errors
    browser.close()
result = dict(status="passed", errors=errors, checks=["five assessment cards", "ten prediction methods", "figure rendering", "report download", "PDF downloads", "mobile layout", "global assessment hidden under family filter"])
write(state/"check.json", result)
print(json.dumps(result, indent=2))

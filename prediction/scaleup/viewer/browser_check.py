"""Check the live viewer in Chromium; all browser state stays in shared storage."""
from pathlib import Path
import json
import os
import sys

HERE = Path(__file__).resolve().parent
STATE = HERE/"state"
STATE.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = "/shared/allie/home/.codex/tmp"
os.environ["XDG_CACHE_HOME"] = str(STATE/"browser-cache")
os.environ["XDG_CONFIG_HOME"] = str(STATE/"browser-config")
os.environ["LD_LIBRARY_PATH"] = "/shared/allie/home/.codex/tmp/trace-viewer-libs/root/usr/lib/x86_64-linux-gnu"
font = STATE/"fonts.conf"
font.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
                '<dir>/shared/allie/strategy-behavior/benchmark/trace_viewer</dir>'
                f'<cachedir>{STATE}/font-cache</cachedir></fontconfig>')
os.environ["FONTCONFIG_FILE"] = str(font)
sys.path.insert(0, str(HERE.parents[1]/"dataset_viewer/.deps"))
from playwright.sync_api import sync_playwright, expect

meta = json.loads((STATE/"server.json").read_text())
url = "http://127.0.0.1:"+str(meta["port"])
chrome = "/shared/allie/home/.cache/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell"
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome, headless=True, args=["--no-sandbox"])
    page = browser.new_page(viewport=dict(width=1440, height=1050), accept_downloads=True)
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(url, wait_until="networkidle")
    expect(page.locator("#metrics")).to_contain_text("6,056")
    expect(page.locator(".family-row")).to_have_count(24)
    expect(page.locator("#dose-chart svg")).to_be_visible()
    expect(page.locator(".split-row")).to_have_count(6)
    page.screenshot(path=str(STATE/"overview.png"), full_page=True)
    page.locator('[data-family="shared_fishery"]').click()
    expect(page.locator("#family")).to_have_value("shared_fishery")
    page.select_option("#parameter", "regeneration")
    expect(page.locator("#dose-chart rect.bar")).to_have_count(5)
    page.get_by_role("button", name="Explore data samples").click()
    expect(page.locator("#sample-detail h2")).to_contain_text("Shared fishery")
    expect(page.locator(".rules")).to_contain_text("quota")
    page.get_by_role("button", name="Trajectory samples", exact=True).click()
    expect(page.locator("#episode-content")).to_contain_text("Focal seat")
    page.locator(".turn-button").last.click()
    expect(page.locator(".action-result")).to_be_visible()
    page.get_by_text("Exact model input before this action", exact=True).click()
    expect(page.locator("pre.prompt").first).to_contain_text("primary objective")
    sample_url = page.url
    page.screenshot(path=str(STATE/"sample.png"), full_page=True)
    with page.expect_download() as download:
        page.get_by_role("button", name="Export sample").click()
    download.value.save_as(str(STATE/"sample-export.json"))
    page.reload(wait_until="networkidle")
    expect(page.locator(".action-result")).to_be_visible()
    expect(page.locator("#family")).to_have_value("shared_fishery")
    page.get_by_role("button", name="Pairs & splits", exact=True).click()
    expect(page.locator(".pair-link").first).to_be_visible()
    page.locator(".pair-link").first.click()
    expect(page.locator("#sample-detail h2")).to_contain_text("Shared fishery")
    page.set_viewport_size(dict(width=390, height=844))
    page.screenshot(path=str(STATE/"mobile.png"), full_page=True)
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Mobile overflow"
    page.locator("#search").fill("unmatched-zzzzzzzzz")
    expect(page.locator("#matches")).to_have_text("0 games")
    expect(page.locator("#sample-detail")).to_contain_text("No samples match")
    # Exercise the continuation route, not just the retained original samples.
    continuation_sample = None
    for offset in range(0, 48, 12):
        listing = page.request.get(url+f"/api/games?offset={offset}").json()
        for row in listing["rows"]:
            game = page.request.get(url+"/api/game?id="+row["game_id"]).json()
            episode = next((e for e in game["episodes"] if "openrouter" in e["model"] and e["status"] == "complete"), None)
            if episode:
                continuation_sample = (row, episode)
                break
        if continuation_sample:
            break
    assert continuation_sample, "No completed OpenRouter sample exposed"
    row, episode = continuation_sample
    page.goto(url+f"/#page=samples&game={row['game_id']}&episode={episode['id']}&tab=trajectory&turn=1", wait_until="networkidle")
    page.reload(wait_until="networkidle")
    expect(page.locator("#episode-content")).to_contain_text("Provider: openrouter")
    payload = page.request.get(url+"/api/episode?id="+episode["id"]).json()
    assert payload["collection_provider"] == "openrouter"
    assert "openrouter-continuation" in payload["source_run"]
    page.set_viewport_size(dict(width=1440, height=1050))
    page.screenshot(path=str(STATE/"openrouter-sample.png"), full_page=True)
    assert not errors, errors
    browser.close()
result = dict(status="passed", errors=errors, sample_url=sample_url,
              checks=["design counts", "24-family chart", "parameter filtering", "six split charts",
                      "sample rules", "trajectory and exact input", "turn selection", "JSON download",
                      "shareable sample reload", "pair navigation", "mobile layout", "empty search", "OpenRouter sample provenance"])
(STATE/"browser-check.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))

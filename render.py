#!/usr/bin/env python3
"""Render a KUYDIGITAL feed post (1080 x 1350, saved at 2x) from a JSON spec.

Usage: python3 render.py spec.json images/YYYY-MM/YYYY-MM-DD-kind-slug.png

spec.json: {"kind": "few-words" | "work" | "build" | "open",
            "kicker": "FEW WORDS",
            "headline": "Text with one [[copper phrase]]",
            "body": "optional caption-sized text inside the image",
            "code": "optional terminal line for build posts"}
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent


def render(spec: dict, out: pathlib.Path) -> None:
    template = (ROOT / "templates" / "post.html").read_text(encoding="utf-8")
    html = template.replace("/*SPEC*/{}", json.dumps(spec, ensure_ascii=False).replace("</", "<\\/"))
    tmp = ROOT / "templates" / "_render.html"
    tmp.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
            page.goto(tmp.as_uri())
            page.wait_for_function("document.title === 'ready'")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            out.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            browser.close()
    finally:
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    render(json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")), pathlib.Path(sys.argv[2]))
    print(sys.argv[2])

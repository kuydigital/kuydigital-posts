#!/usr/bin/env python3
"""Render a KUYDIGITAL feed post (1080 x 1350, saved at 2x) from a JSON spec.

Usage: python3 render.py spec.json images/YYYY-MM/YYYY-MM-DD-kind-slug.png

Fields by kind ([[...]] sets one phrase in copper; \n is a line break):
  work          kicker "Featured project", tag "Web app · Metro Manila", name "CrowdSense"
                (may contain \n), headline (tagline), body (one sentence)
  build         kicker, headline, code (optional terminal line), body
  few-words     kicker, headline
  open          kicker, headline, body
  photo         kicker, headline, photo (repo path, e.g. "library/photos/desk.jpg"), credit
  illustration  kicker, headline, svg (a complete inline <svg> with a viewBox)
  share         kicker "Worth reading", headline (your takeaway), source, title
  funny         kicker, setup, punchline

After rendering it checks that nothing spills out of the frame or into the monogram,
and exits with status 2 (listing the problems) if anything does.
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
            problems = page.evaluate(CHECK)
            out.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            browser.close()
    finally:
        tmp.unlink(missing_ok=True)
    if problems:
        print("LAYOUT PROBLEMS:\n  " + "\n  ".join(problems))
        sys.exit(2)


CHECK = """() => {
  const out = [], post = document.getElementById('post');
  const mark = post.querySelector('.mark').getBoundingClientRect();
  for (const n of post.querySelectorAll('.kicker,.headline,.name,.body,.code,.card,.credit,.art')) {
    const r = n.getBoundingClientRect(), label = (n.className + ': ' + n.textContent.trim()).slice(0, 60);
    if (r.left < 40 || r.top < 40 || r.right > 1040 || r.bottom > 1310) out.push('outside the frame: ' + label);
    if (n.scrollWidth > n.clientWidth + 2) out.push('text wider than its box: ' + label);
    const hit = r.left < mark.right + 16 && r.right > mark.left - 16 && r.top < mark.bottom + 16 && r.bottom > mark.top - 16;
    if (hit && !n.classList.contains('art')) {
      // a block's box may reach into the monogram's corner while its text does not; test the text itself
      const range = document.createRange(); range.selectNodeContents(n);
      for (const t of range.getClientRects()) if (t.right > mark.left - 16 && t.bottom > mark.top - 16 && t.top < mark.bottom) { out.push('overlaps the monogram: ' + label); break; }
    }
  }
  const img = post.querySelector('.photo');
  if (img && !(img.naturalWidth > 0)) out.push('photo did not load');
  if (img && img.naturalWidth < 1080) out.push('photo is smaller than 1080 px wide');
  return out;
}"""


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    render(json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")), pathlib.Path(sys.argv[2]))
    print(sys.argv[2])

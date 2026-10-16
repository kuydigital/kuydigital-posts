#!/usr/bin/env python3
"""Work out what today's post should be, from content/log.jsonl and the photo library.

Usage: python3 next_post.py            (prints one JSON object)

Output fields:
  today, month_posts_in_log, done_today   facts for the checks in CLAUDE.md section 1
  kind                                    the kind to make today
  slot                                    the cycle position to log with this post
  avoid_project                           work/build: the project the last work/build post used
  unused_photos                           photo: library files not used by any post yet
  reason                                  one line on how the kind was chosen

Rules (CLAUDE.md section 2):
  - The first post of a calendar month is `open`.
  - Otherwise the cycle is: work -> wildcard -> build -> wildcard -> few-words, then repeat.
  - A wildcard slot takes the next of: photo -> share -> funny -> illustration, after the last
    wildcard in the log. `photo` is skipped when the library has no unused photo.
  - Log lines with "replaces" (a reposted design) or "outside_cycle" do not move the cycle.
"""
import datetime as dt
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
CYCLE = ["work", "wildcard", "build", "wildcard", "few-words"]
WILD = ["photo", "share", "funny", "illustration"]
SLOT_OF = {"work": 0, "build": 2, "few-words": 4}  # for old log lines written before "slot" existed

today = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date()
log = [json.loads(l) for l in (ROOT / "content/log.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
month = [e for e in log if e["date"][:7] == today.isoformat()[:7]]
cycle_log = [e for e in log if not e.get("replaces") and not e.get("outside_cycle")]

used = {e.get("photo") for e in log if e.get("photo")}
lib = ROOT / "library/photos"
listed = set(re.findall(r"^\|\s*`?([^`|\s]+\.(?:jpe?g|png|webp))`?\s*\|", (lib / "README.md").read_text(encoding="utf-8"), re.M)) if (lib / "README.md").exists() else set()
unused = sorted(f"library/photos/{n}" for n in listed if (lib / n).exists() and f"library/photos/{n}" not in used)

out = {"today": today.isoformat(), "month_posts_in_log": len(month), "done_today": any(e["date"] == today.isoformat() for e in log)}

if not month:
    out.update(kind="open", slot=None, reason="first post of the month")
else:
    last = next((e for e in reversed(cycle_log) if e["kind"] != "open"), None)
    if last is None:
        slot = 0
    else:
        s = last.get("slot")
        if s is None:
            s = SLOT_OF.get(last["kind"], 1)
        slot = (s + 1) % len(CYCLE)
    kind = CYCLE[slot]
    reason = f"cycle position {slot} after the last post ({last['kind'] if last else 'none'})"
    if kind == "wildcard":
        last_w = next((e["kind"] for e in reversed(cycle_log) if e["kind"] in WILD), None)
        i = (WILD.index(last_w) + 1) % len(WILD) if last_w else 0
        for _ in WILD:
            if WILD[i] == "photo" and not unused:
                i = (i + 1) % len(WILD)
                continue
            break
        kind = WILD[i]
        reason += f"; wildcard after {last_w or 'none'}" + ("; photo skipped (no unused photo in the library)" if not unused and "photo" in WILD[:i + 1] else "")
    out.update(kind=kind, slot=slot, reason=reason)

if out["kind"] in ("work", "build"):
    prev = next((e for e in reversed(log) if e["kind"] in ("work", "build") and e.get("project")), None)
    out["avoid_project"] = prev["project"] if prev else None
if out["kind"] == "photo":
    out["unused_photos"] = unused

print(json.dumps(out, ensure_ascii=False, indent=1))

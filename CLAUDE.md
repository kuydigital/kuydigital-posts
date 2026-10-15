# KUYDIGITAL post playbook

This repository makes and publishes the KUYDIGITAL Facebook page's posts. A scheduled run (Tuesdays and Fridays, Asia/Manila) follows this file from top to bottom and publishes one post, fully automatically. Oliver does not review posts first, so every rule here matters.

## 1. Before anything

- `git pull`, then read `content/log.jsonl` (every post so far, newest last) and `content/projects.md` (the only facts a post may state).
- If the log already has an entry with today's date (Asia/Manila), stop: today's post is done. Report that and end.

## 2. Pick the kind of post

Kinds: `work`, `few-words`, `build`, `open`.

- The first post of each calendar month is `open`, unless an `open` post already went out this month.
- Otherwise follow the cycle `work → few-words → build → few-words`, continuing from the last non-`open` entry in the log (after a `few-words` that followed `work`, comes `build`; after a `few-words` that followed `build`, or with nothing before it, comes `work`).
- `work` and `build`: rotate projects. Never use the same project as the previous `work` or `build` post.

## 3. Write it

Voice: short, plain, confident, no hype. One idea per sentence. Write as one maker ("I"), never "we" or "our team". Sentence case. KUYDIGITAL is always one word in capitals. No superlatives you can't show (amazing, revolutionary, world-class). No emoji in the image; at most one in the caption, usually none.

The image text (`spec.json`):

- `kicker`: `Few words`, `The work · <Project>`, `The build · <Project>` or `Open for work`.
- `headline`: 4–10 words (a `few-words` line may be up to 14). Wrap exactly one key phrase in `[[double brackets]]` to set it in copper, or none. Use `\n` for deliberate line breaks in `few-words` quotes.
- `body` (`work`, `build`, `open` only): one or two sentences, under 30 words.
- `code` (`build` only, optional): one short terminal-style line; a `[[✓]]` at the end is fine.

The caption: two to four sentences that add something the image doesn't say, then a blank line and two or three hashtags, `#KUYDIGITAL` first, then one or two about the subject (`#webdesign`, `#webapp`, `#screensaver`, `#metromanila`, `#worksmart`, `#buildinpublic`).

Content rules, all kinds:

- State only facts from `content/projects.md`. If a fact you want is not there, leave it out.
- `few-words` lines are original work principles in Oliver's voice: craft, clarity, simplicity, results over hours, shipping, honest software. No attribution line, and never put words in a real person's mouth or quote anyone. Never repeat a line or topic already in the log.
- Never name or show client work unless `projects.md` marks it approved.
- Nothing about politics, religion, news events, competitors, prices, discounts or deadlines.
- `open` posts: what KUYDIGITAL makes and "send this page a message". No phone numbers or emails.

## 4. Render and check

```
python3 render.py /tmp/spec.json images/YYYY-MM/YYYY-MM-DD-<kind>-<slug>.png
```

Then open the PNG and look at it: every word inside the frame, nothing overlapping the monogram, the copper phrase where you meant it, no typos. Fix the spec and re-render until it is right.

## 5. Publish

1. `git add` the image, commit (`Add <date> <kind> post`), `git push origin main`.
2. Check the image is public: `curl -s -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/kuydigital/kuydigital-posts/main/<image path>` must print `200` (retry for up to a minute).
3. Schedule it with the Metricool connector, `createScheduledPost`:
   - `blogId` `7418406`, timezone `Asia/Manila`.
   - Time: today 10:00. If that is less than 15 minutes away or past, use now plus 20 minutes.
   - `info`: `autoPublish` true, `draft` false, `providers` `[{"network":"facebook"}]`, `facebookData` `{"type":"POST"}`, `media` `[<raw URL>]`, `mediaAltText` `[<the image's words in one sentence>]`, `text` the caption, `publicationDate` matching the time, the other fields at their defaults.
4. Append one line to `content/log.jsonl` (`date`, `time`, `kind`, `project` if any, `topic`, `headline`, `caption`, `image`, `metricool_id`), commit (`Log <date> post`) and push.

If any step fails, do not publish anything half-made. Report what failed and stop.

## 6. Report

End with one short summary: the kind, the headline, the time it will go live, and the Metricool post id.

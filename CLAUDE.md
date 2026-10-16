# KUYDIGITAL post playbook

This repository makes and publishes the KUYDIGITAL Facebook page's posts. A scheduled run (Tuesdays and Fridays, Asia/Manila) follows this file from top to bottom and publishes one post, fully automatically. Oliver does not review posts first, so every rule here matters.

## 1. Before anything

- `git pull`, then read `content/log.jsonl` (every post so far, newest last) and `content/projects.md` (the only facts a post may state).
- If the log already has an entry with today's date (Asia/Manila), stop: today's post is done. Report that and end.
- Monthly limit: Oliver's free Metricool plan allows 10 posts a calendar month. Count this month's posts two ways: entries in the log dated this month, and posts returned by the Metricool connector's `getScheduledPosts` (brandId `7418406`, timezone `Asia/Manila`, from the 1st of this month 00:00 to the last day 23:59). Take the larger count. If it is 10 or more, do not post: report that the month's allowance is used up and end. If it is 9, post only if no other post is already scheduled for later this month.
- Any post made outside this task (for example one Oliver asks for in a chat) also gets a line in the log, so the count stays right. Give it `"outside_cycle": true` so it does not move the rotation, or `"replaces": <metricool id>` when it reposts an earlier post with a new design.

## 2. Pick the kind of post

Run `python3 next_post.py`. It reads the log and the photo library and prints today's `kind`, the cycle `slot` to log, the project to avoid and any unused photos. Use its answer; do not pick a kind by hand. How it decides:

- The first post of each calendar month is `open`.
- Otherwise the cycle is `work → wildcard → build → wildcard → few-words`, then it repeats.
- A wildcard slot takes the next of `photo → share → funny → illustration`. `photo` is skipped while `library/photos/` has no unused photo.
- `work` and `build`: never the same project as the previous `work` or `build` post (`avoid_project`).

If today's kind cannot be done well (no article passes the `share` checks below, say), make the next wildcard kind instead and log the `slot` you were given. Never fall back to posting something weaker just to post.

## 3. Write it

Voice: short, plain, confident, no hype. One idea per sentence. Write as one maker ("I"), never "we" or "our team". Sentence case. KUYDIGITAL is always one word in capitals. No superlatives you can't show (amazing, revolutionary, world-class). No emoji in the image; at most one in the caption, usually none. Use curly quotes and apostrophes in image text (“ ” ’).

Every kind has a `kind` field in `spec.json` (see the top of `render.py`). Headlines are 4–10 words (a `few-words` line or a `funny` post may be up to 14). Wrap at most one key phrase in `[[double brackets]]` to set it in copper.

### `work`: featured project

The project as a portfolio piece, on a dark ground.

- `kicker` `Featured project`; `tag`: what it is and where, from `projects.md` (`Web app · Metro Manila`, `Screensaver · Open source`).
- `name`: the project's name, split over two lines with `\n` when it has two parts (`Crowd\nSense`, `Threat\nMonitor`).
- `headline`: the one-line promise, with the copper phrase on its second line (`Know how crowded it is\n[[before you go.]]`).
- `body`: one sentence, under 25 words.
- No charts, bars, numbers, screenshots or anything that could pass for the project's real data.

### `build`

How something was made. `kicker` `The build · <Project>`, `headline`, optional `code` (one short terminal-style line; `[[✓]]` at the end is fine), `body` (one or two sentences, under 30 words).

### `few-words`

`kicker` `Few words`, `headline`: an original work principle in Oliver's voice (craft, clarity, simplicity, results over hours, shipping, honest software). Use `\n` for deliberate line breaks. No attribution line, never quote anyone. Never repeat a line or topic already in the log.

### `photo`

A royalty-free photo with a short line under it.

- Use only a file from `next_post.py`'s `unused_photos`. Open it first and look at it. Use it only if it fits a line you can write about KUYDIGITAL's work (screens, workspaces, the craft, Metro Manila for CrowdSense). If none fits, make the next wildcard kind.
- `photo`: its path; `credit`: the `credit` column from `library/photos/README.md` (omit it for `-`); `kicker`: `Worth a look`, `On the desk` or `Metro Manila`; `headline`: your line.
- The caption may connect the photo to a project, stating only facts from `projects.md`.
- Log the photo's path in `photo` so it is never used again.

### `illustration`

An original drawing made in code: write a complete `<svg viewBox="0 0 952 720">` into `svg`.

- Flat and geometric, in the brand colours only: ink `#141414`, paper `#f3f0e8`, white `#ffffff`, concrete `#8c8a84`, copper `#d9692b`. Thick even strokes, generous space.
- Subjects: screens, browser windows, wireframes, phones, a monitor showing a screensaver, a Raspberry Pi, a map pin, a calendar, tools, sketches. Draw ideas, not data: no chart that implies real numbers.
- Never draw a real person, a known character, mascot, logo, app icon or someone else's product or interface. No text inside the drawing except one or two short labels if they help.
- `kicker`: `The idea` or `The work · <Project>`; `headline`: the point the drawing makes.

### `share`: worth reading

A good article to share, with Oliver's one-line takeaway.

- Find it with WebSearch, then read the whole article with WebFetch. Share it only if all of these hold: it is useful to small-business owners or makers (web design, building websites and apps, usability, accessibility, speed, honest software, working well with AI coding tools, running a one-person studio, workplace screens and signage); it is from a reputable publisher or a known practitioner's own site; it is free to read (no paywall or sign-up wall); it is not about politics, religion, news events, a competitor studio or agency, or a product launch or sale; you agree with its main point and could say why in one sentence; its link works (WebFetch loads it).
- Never share the same link twice or the same site twice in a row (check the log's `link` field).
- `kicker` `Worth reading`; `headline`: your takeaway in your own words (not a quote from the article); `source`: the site's name; `title`: the article's own title, shortened only with an ellipsis if over 12 words.
- Caption: one or two sentences on why it is worth reading, in your own words, then the link on its own line, then the hashtags. Never copy sentences from the article and never claim KUYDIGITAL wrote it.
- Log the link in `link`.

### `funny`

A light, original joke about the maker's life: clients and feedback, bugs, browsers, Wi-Fi, version names, screensavers, Metro Manila traffic and malls.

- `kicker` `Just saying` (or `Friday` on a Friday); `setup`: the line that sets it up; `punchline`: the turn, shown in copper. Both short.
- Laugh at situations and at yourself, never at clients, users or any group of people. Nothing mean, crude, political, religious or about a real person, brand or competitor. No memes, no borrowed jokes, no copyrighted characters or images.
- If you are not sure it is funny and kind, write the next wildcard kind instead.

### `open`

`kicker` `Open for work`; `headline` and `body`: what KUYDIGITAL makes and "send this page a message". No phone numbers or emails.

### The caption (all kinds)

Two to four sentences that add something the image doesn't say, then a blank line and two or three hashtags, `#KUYDIGITAL` first, then one or two about the subject (`#webdesign`, `#webapp`, `#screensaver`, `#metromanila`, `#worksmart`, `#buildinpublic`, `#smallbusiness`). A `share` caption carries the link before the hashtags.

### Content rules (all kinds)

- Anything said about KUYDIGITAL or its projects comes only from `content/projects.md`. If a fact you want is not there, leave it out.
- Never name or show client work unless `projects.md` marks it approved.
- Nothing about politics, religion, news events, competitors, prices, discounts or deadlines.
- Never repeat a headline, joke, article or topic already in the log.

## 4. Render and check

```
python3 render.py /tmp/spec.json images/YYYY-MM/YYYY-MM-DD-<kind>-<slug>.png
```

`render.py` checks the layout itself and exits with `LAYOUT PROBLEMS` if any text leaves the frame or touches the monogram; fix the spec and re-render. Then open the PNG and look at it: every word readable, the copper phrase where you meant it, no typos, a photo or drawing that looks right. Fix and re-render until it is right.

## 5. Publish

1. `git add` the image, commit (`Add <date> <kind> post`), `git push origin main`.
2. Check the image is public: `curl -s -o /dev/null -w "%{http_code}" https://raw.githubusercontent.com/kuydigital/kuydigital-posts/main/<image path>` must print `200` (retry for up to a minute).
3. Schedule it with the Metricool connector, `createScheduledPost`:
   - `blogId` `7418406`, timezone `Asia/Manila`.
   - Time: today 10:00. If that is less than 15 minutes away or past, use now plus 20 minutes.
   - `info`: `autoPublish` true, `draft` false, `providers` `[{"network":"facebook"}]`, `facebookData` `{"type":"POST"}`, `media` `[<raw URL>]`, `mediaAltText` `[<the image's words in one sentence>]`, `text` the caption, `publicationDate` matching the time, the other fields at their defaults.
4. Append one line to `content/log.jsonl` (`date`, `time`, `kind`, `slot` from `next_post.py`, `project` if any, `topic`, `headline`, `caption`, `image`, `metricool_id`, plus `photo` for a photo post and `link` for a share post), commit (`Log <date> post`) and push.

If any step fails, do not publish anything half-made. Report what failed and stop.

## 6. Report

End with one short summary: the kind, the headline, the time it will go live, and the Metricool post id.

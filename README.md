# kuydigital-posts

Images and the posting playbook for the KUYDIGITAL Facebook page.

A scheduled run designs a post from `content/projects.md`, renders it with `render.py` in the KUYDIGITAL brand (`brand/`, `templates/post.html`), pushes the image under `images/YYYY-MM/`, and publishes it through Metricool, which reads the image from its raw GitHub link. `CLAUDE.md` is the playbook each run follows, and `content/log.jsonl` records every post.

Files here are public by design. Nothing private goes in this repository. To steer the posts, edit `content/projects.md`.

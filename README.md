This is the source code to my public academic website.

## Editing the site

All page content lives in **`site.yml`**. The `index.html` file is **generated**
from it by `build.py` — never edit `index.html` by hand.

Workflow:

1. Edit `site.yml` (add a paper, change a venue, update the bio, …).
2. Drop any new images/videos into `images/`.
3. Run the generator:

   ```bash
   python3 build.py
   ```

4. Commit both `site.yml` and the regenerated `index.html` and push.

Requires Python 3 and PyYAML (`python3 -m pip install pyyaml`).

### Adding a publication

Copy an existing block under `publications:` in `site.yml` and edit it. Fields:

| field       | meaning                                                              |
|-------------|---------------------------------------------------------------------|
| `image`     | thumbnail in `images/`, always shown                                |
| `hover`     | *(optional)* media in `images/` shown on mouse-over — `.mp4` becomes a looping video, `.gif`/`.png`/`.jpg` an image. Omit for a static thumbnail. |
| `highlight` | `true` gives the row the yellow background (used for your own key papers) |
| `award`     | *(optional)* red note after the venue, e.g. `"(Oral Presentation)"` |
| `url`       | link on the paper title                                             |
| `authors`   | raw HTML; wrap your own name in `<strong>…</strong>`                |
| `venue` / `year` | e.g. `ECCV` / `2026`                                           |
| `links`     | ordered list of `{text, href}` shown under the entry               |
| `abstract`  | one-sentence summary                                               |

Papers appear in the same order as in `site.yml` (top = most recent).

The hover fade is handled entirely by CSS (`.one:hover .two` in
`stylesheet.css`), so there is no per-paper JavaScript to copy anymore.

### Other sections

`site.yml` also holds the bio, header links, **News** (currently hidden — set
`show_news: true` to show it), **Supervising**, **Reviewing**, and **Teaching**.

`python3 build.py --check` validates that every referenced image/video exists
without rewriting `index.html`.

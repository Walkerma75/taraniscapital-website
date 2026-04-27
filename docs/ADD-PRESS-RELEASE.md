# Add a Press Release

Workflow for publishing a new press release on `taraniscapital.com/press/<slug>`.

## TL;DR

1. Drop a Markdown file at `content/press/<YYYY-MM-DD-kebab-slug>.md` (format below).
2. Drop the hero image at `images/press/<filename>.jpg` (or `.png`).
3. Run `python tools/add-press-release.py content/press/<slug>.md`.
4. Review the diff with `git status` / `git diff`.
5. Commit the listed files, push, open PR.

That's it. The generator handles template rendering, listing card insertion, sitemap update, placeholder cleanup on first publish, and image dimension detection.

## What the generator does

`tools/add-press-release.py` reads your Markdown source (with YAML frontmatter), then:

- Renders `press/<slug>.html` from `press/_template.html` (strips `noindex` and the template comment block automatically)
- Inserts a card at the top of `.press-grid` in `press.html`
- Adds a URL entry to `sitemap.xml` and bumps `/press` `lastmod` to today
- Removes the placeholder release (file, listing card, sitemap entry) the first time a real release ships
- Auto-detects hero image dimensions (JPEG/PNG) so the browser reserves layout space and avoids CLS
- Idempotent — re-running for the same slug overwrites cleanly

## Source file format

Save at `content/press/<YYYY-MM-DD-kebab-slug>.md`. Frontmatter (YAML between `---` markers), then the body in Markdown:

```markdown
---
slug: 2026-06-12-taranis-launches-biotech-fund        # must match filename
date: 2026-06-12                                       # ISO YYYY-MM-DD
headline: Full headline goes here.
headline_short: Short breadcrumb headline              # optional, falls back to headline
strapline: Optional italic line below the H1.         # optional
dateline_city: "Dubai, UAE"                            # bolded prefix on first paragraph
excerpt: One-line summary for the listing card.
meta_description: ~155-char SEO description.
hero_image: images/press/<filename>.jpg                # optional; relative to repo root
hero_alt: Alt text for the hero image                  # required if hero_image set
boilerplate:                                           # optional; falls back to default "About Taranis Capital"
  - title: About Taranis Capital
    body: |
      First boilerplate text...
  - title: About Partner Org
    body: |
      Their boilerplate...
contacts:                                              # optional; falls back to default Taranis contact
  - title: Taranis Capital Limited
    email: press@taraniscapital.com
  - title: Partner Org
    email: press@example.com
    url: https://example.com/press/                    # optional URL link in contact block
    address: 123 Example Street                        # optional
    phone: +1 555 555 5555                             # optional
---

The first paragraph after the closing --- becomes the dateline paragraph (with the bolded `dateline_city` prefix). Body paragraphs follow normal Markdown rules.

## A subhead

`## Subhead` becomes an `<h2>` for section breaks.

> Pull quotes use Markdown blockquote syntax. Multi-line quotes are fine.
>
> The last quoted paragraph, if it starts with `—` or `--`, is treated as attribution and rendered as `<cite>`.
>
> — Person Name, Title, Organisation

Plain paragraphs become `<p>` elements.
```

HTML entities (`&ldquo;`, `&rdquo;`, `&mdash;`, `&ndash;`, `&rsquo;`, `&amp;`) pass through verbatim — use them for proper typography. UTF-8 punctuation works too.

## After running the generator

The script prints what it generated and the exact `git add` line. Verify with `git status` — you should see:

- new file: `content/press/<slug>.md`
- new file: `press/<slug>.html`
- new file: `images/press/<filename>.<ext>` (if you added a new hero image)
- modified: `press.html`
- modified: `sitemap.xml`
- (first real release only) deleted: `press/2026-05-01-press-section-launch.html`

Commit with the line the script prints:

```
git add content/press/<slug>.md press/<slug>.html press.html sitemap.xml images/press/<filename>.<ext>
git commit -m "Publish press release: <short-title>"
git push
```

Open a PR. CI will run S3 sync + CloudFront invalidation on merge to `main`. Allow 2–3 min, then verify in incognito:

- `https://taraniscapital.com/press` — new card at top, placeholder gone
- `https://taraniscapital.com/press/<slug>` — full release renders, hero loads, no `noindex` in source, canonical URL correct, OG image points at hero, JSON-LD schema present

## Notes

- **Placeholder removal is automatic** — the first time you publish a real release, the placeholder file, its listing card, its sitemap entry, and the stale "placeholder is deliberately omitted" comment in `sitemap.xml` are all cleaned up.
- **No CloudFront republish** is needed for new releases — the `/press/` prefix is already allowlisted in the `url-rewrite` Function.
- **Re-running for the same slug** is safe — overwrites HTML, replaces card cleanly, replaces sitemap entry.
- **Changing a slug post-publish** — the generator only knows about the slug it's currently rendering. If you rename a release, manually delete the old `press/<old-slug>.html`, remove its card from `press.html`, and remove its `<url>` entry from `sitemap.xml`. (Or open an issue and we'll add a `--remove` flag.)
- **Dependencies:** Python 3.7+ and `pyyaml`. Install with `pip install pyyaml` if missing.

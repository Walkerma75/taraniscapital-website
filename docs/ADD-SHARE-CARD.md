# Share cards (link-preview images) for team & board pages

When someone shares a team or board profile URL (LinkedIn, WhatsApp, Slack,
iMessage, X), the preview image is the page's `og:image`. We give **each team and
board member their own 1200×630 share card** (photo + name + title, on-brand) so
the unfurl shows the person, not the bare logo.

Cards live in `images/team/<slug>-share.jpg` and `images/board/<slug>-share.jpg`
(e.g. `images/team/mark-walker-share.jpg`, `images/board/asim-chohan-share.jpg`).
The sitewide default — also used for any member whose headshot is missing — is
`images/share-default.jpg`.

## Adding a new team or board member — do this every time

`<section>` is `team` or `board` below — use whichever folder the profile lives in.

1. Create the profile page as usual: `<section>/<slug>.html` with
   `<h1 class="profile-name">`, `<div class="profile-role">`, and the headshot in
   the `profile-photo` `<img src>`.
2. Generate the card:
   ```
   python tools/generate-share-cards.py
   ```
   With no arguments it creates a card **only** for pages that don't already have
   one — so it just produces the new person's `images/<section>/<slug>-share.jpg`.
   If the headshot file is missing/placeholder it generates **no** card; point
   `og:image` at `images/share-default.jpg` instead (step 3).
3. Point the new page's `og:image` at the card (head section):
   ```html
   <meta property="og:image" content="https://taraniscapital.com/images/<section>/<slug>-share.jpg">
   <meta property="og:image:width" content="1200">
   <meta property="og:image:height" content="630">
   <meta property="og:image:alt" content="<Name> — <Title>, Taranis Capital">
   <meta name="twitter:card" content="summary_large_image">
   <meta name="twitter:image" content="https://taraniscapital.com/images/<section>/<slug>-share.jpg">
   ```
   (Easiest: copy an existing profile page's head block and change the slug/name.)
4. Commit the new `.jpg` together with the HTML, push, deploy.
5. After deploy, re-scrape so caches don't serve a stale/blank preview:
   LinkedIn Post Inspector — https://www.linkedin.com/post-inspector/

## Useful commands

| Command | What it does |
|---|---|
| `python tools/generate-share-cards.py` | Generate cards for pages missing one (safe, idempotent) |
| `python tools/generate-share-cards.py --all` | Regenerate **all** team & board cards (e.g. after a brand/headshot change) |
| `python tools/generate-share-cards.py --default` | Also rebuild `images/share-default.jpg` |
| `python tools/generate-share-cards.py --check` | List pages with no card or whose og:image still points at the logo; exits 1 if any (good for CI) |

## CI guard

The deploy workflow (`.github/workflows/deploy.yml`) runs `--check` before the S3
sync, so the build fails if any team **or board** page lacks a card or still has
`og:image = logo-gold.png` (a transparent PNG that unfurls blank).

## Design / branding

- 1200×630 JPG (Open Graph standard), non-transparent — transparent PNGs are why
  the old logo previews rendered blank on LinkedIn/WhatsApp.
- Colours from `css`: green-dark `#2c3e35` → green-mid `#3a5247` gradient, gold
  `#c9a84c` accent. Name in serif (Georgia on Windows), role/wordmark in sans.
- Long names with credentials (e.g. "Dr. Bijna Kotak Dasani MBE, FRSA") auto-shrink
  to fit. Headshots are centre-cropped slightly high (centering 0.5/0.32) to keep
  faces in frame.

Generator: `tools/generate-share-cards.py`.

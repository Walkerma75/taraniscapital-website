# Press Release Section — Development Plan

**Author:** Mark (via Claude)
**Date:** 2026-04-24
**Target implementer:** Claude Code
**Repo:** `Walkerma75/taraniscapital-website` · branch `main`
**Working directory:** `C:\Users\mark\Claude Cowork\Taranis Capital Website`

---

## 1. Objective

Add a manually curated **Press Releases** section to taraniscapital.com so the firm can publish its own announcements. The existing `/insights` page is an RSS aggregator pulling third-party industry news — it is not suitable for first-party press content. Press releases must sit on their own URL space, follow the Taranis brand system, be SEO-discoverable, and be trivial to add to in future.

## 2. Scope

### In scope

- New listing page at `/press`
- New individual release pages at `/press/<slug>`
- Navigation + footer wiring
- Sitemap + SEO metadata
- CloudFront `url-rewrite` function update (allowlist + catch-all exemption)
- One seed release page (placeholder content) so Claude Code can verify the full flow end-to-end
- QA checklist + deployment steps
- Documented "add a new release" workflow for future use

### Out of scope (for this iteration)

- RSS/Atom feed of press releases (nice-to-have, deferred)
- Share-to-social buttons on individual releases
- Media-kit / downloadable assets page
- CMS or JSON-driven rendering — pages are static HTML, one file per release
- Multi-language support

## 3. Design decision: dedicated `/press` section

Chosen over the two alternatives (single combined page; inline block on Insights) because:

- Clean separation from the RSS Insights feed removes any confusion between first-party and third-party content.
- Per-release URLs (`/press/<slug>`) give stable deep-links suitable for distribution in PR outreach and social posts.
- Matches the existing pattern used for `/team/`, `/board/`, `/partners/` (listing + per-profile page).
- Scales from one release to hundreds without restructuring.

## 4. URL structure

| Purpose | Clean URL | S3 key |
|---|---|---|
| Listing page | `/press` | `press.html` |
| Individual release | `/press/<slug>` | `press/<slug>.html` |

Slug convention: `YYYY-MM-DD-kebab-case-headline` (e.g. `2026-05-01-taranis-capital-launches-biotech-fund`). Date prefix keeps files sorted chronologically in the repo and gives the slug enough length to avoid colliding with the WP legacy catch-all pattern (see §9).

## 5. File inventory

### Files to create

| Path | Purpose |
|---|---|
| `press.html` | Listing page — hero + grid of release cards, newest first |
| `press/<slug>.html` | One file per release — template-driven, easy to duplicate |
| `press/_template.html` | Copy-paste template for future releases (excluded from sitemap; not linked) |
| `css/press.css` *(optional)* | Only if press-specific styles would bloat `styles.css`; otherwise inline in `styles.css` |

### Files to modify

| Path | Change |
|---|---|
| `index.html` | Add "Press" link to nav (between Insights and Contact) and to footer Navigation list |
| `who-we-are.html` | Same nav + footer updates |
| `our-approach.html` | Same nav + footer updates |
| `our-funds.html` | Same nav + footer updates |
| `insights.html` | Same nav + footer updates |
| `contact.html` | Same nav + footer updates |
| `fintech.html` / `datacentres.html` / `biotech.html` / `disruptive-tech.html` / `property.html` | Same nav + footer updates |
| `cookie-policy.html` / `privacy-policy.html` / `404.html` | Footer only (these pages typically don't carry the top nav — verify) |
| `sitemap.xml` | Add `/press` + one entry per release |
| `infra/cloudfront-url-rewrite.js` | Add `/press` and `/press.html` to `EXACT_ALLOW`; add `'/press/'` to `PREFIX_ALLOW` |
| `robots.txt` | Confirm `/press` is crawlable (should be by default; verify no accidental Disallow) |
| `docs/PROJECT-LOG.md` | Append a session entry describing the change |
| `TASKS.md` | Close out the press-release task (if added) |

**Note on bulk nav edits:** every top-level HTML file carries a copy of the `<nav class="nav">` block and a copy of the `<ul class="footer-links">` block. Claude Code should grep for the nav marker (e.g. `<li><a href="/insights"`) and insert the Press link consistently. Consider a one-off script or a careful `replace_all` across files — but verify each file after, since some pages set `class="active"` on their own link.

## 6. Listing page — `press.html`

### Structure

Reuse the existing page scaffolding verbatim (GA tag, meta/OG tags, skip-link, `<nav>`, `<footer>`, cookie banner, scroll-top button, `main.js`). Hero uses the `page-hero` pattern already on `insights.html` and `our-approach.html`.

```
<section class="page-hero" id="main-content">
  <div class="container">
    <div class="page-hero-content">
      <div class="breadcrumb"><a href="/">Home</a> / Press</div>
      <h1>Press Releases</h1>
      <p class="subtitle">Announcements and news from Taranis Capital</p>
    </div>
  </div>
</section>

<section class="press-section">
  <div class="container">
    <div class="press-grid">
      <!-- One <article class="press-card"> per release, newest first -->
    </div>
  </div>
</section>
```

### Card markup (one per release)

```
<article class="press-card">
  <div class="press-card-meta">
    <time datetime="2026-05-01">1 May 2026</time>
    <span class="press-card-tag">Fund Launch</span>
  </div>
  <h2 class="press-card-title">
    <a href="/press/2026-05-01-taranis-capital-launches-biotech-fund">
      Taranis Capital launches Biotech Fund
    </a>
  </h2>
  <p class="press-card-excerpt">One- or two-line summary of the release…</p>
  <a href="/press/2026-05-01-taranis-capital-launches-biotech-fund" class="press-card-link">
    Read release →
  </a>
</article>
```

### Empty state

If the grid has zero releases, render a centred "No releases yet — check back soon" block. Listing page still publishes; just hidden from nav until first release lands (decide at launch).

### Pagination

Not needed for v1. Revisit once >20 releases.

## 7. Individual release page — `press/<slug>.html`

### Required metadata block (top of body or as data attributes)

Every release page carries:

- Headline (`<h1>`)
- Dateline: `<time datetime="YYYY-MM-DD">` formatted human-readable
- Location prefix (e.g. "Dubai, UAE — ")
- Body copy (paragraphs; one `<h2>` sub-heading permitted)
- Optional blockquote for a key quote
- Standard "About Taranis Capital" boilerplate block at the end
- Standard "Media contact" block at the end (pulls from `CLAUDE.md` contact details)

### SEO / social metadata (must match per release)

- `<title>` — `{Headline} | Taranis Capital`
- `<meta name="description">` — first 155 chars of the release summary
- `<link rel="canonical">` — `https://taraniscapital.com/press/<slug>`
- OG tags: `og:title`, `og:description`, `og:type=article`, `og:url`, `og:image` (default `logo-gold.png` if no hero image)
- Twitter card: `summary_large_image`
- JSON-LD structured data: schema.org `NewsArticle` with `headline`, `datePublished`, `author` (Taranis Capital organisation object), `publisher`, `mainEntityOfPage`

### Breadcrumb

`Home / Press / <Headline>` — links back to `/press` for the middle crumb.

### Back-link

Subtle "← All press releases" at the bottom, linking `/press`.

### Accessibility

- Landmark regions via `<nav>`, `<main id="main-content">`, `<article>`, `<footer>`
- Heading hierarchy: one `<h1>`, sub-sections use `<h2>` only
- All links have descriptive text (no bare "Read more" without context for screen readers — use `aria-label` if necessary)
- Skip-link at top as on other pages

## 8. Styling

Follow the established brand system:

- Headings: Playfair Display (600) — the site actually uses Playfair Display for display headings per `insights.html`, not Georgia. Confirm with `styles.css` before picking. CLAUDE.md still references Georgia/Calibri as the brand canon — if there's drift between brand doc and live site, flag it and ask Mark which wins.
- Body: Inter 400/500
- Colours: existing CSS variables (`--tc-off-white`, `--tc-grey-dark`, `--tc-grey-medium`, dark-green heading accent)
- Card hover: subtle lift + border colour shift (match team/board card pattern)
- Mobile: single column below 768px; two columns 768–1199px; three columns ≥1200px (only if we have that many releases — otherwise two max for visual weight)
- No bright yellow / light-blue tables or banners (explicit don't in CLAUDE.md)

All press-specific CSS should go into `css/styles.css` under a clearly marked `/* ==== PRESS ==== */` section, unless the additions exceed ~150 lines, in which case create `css/press.css` and `<link>` it only from press pages.

## 9. CloudFront `url-rewrite` function update

**Critical step — easy to miss.** The function at `infra/cloudfront-url-rewrite.js` will otherwise eat our new URLs alive.

### Changes required

1. **`EXACT_ALLOW`** — add `'/press': 1, '/press.html': 1,`
2. **`PREFIX_ALLOW`** — add `'/press/'` so `/press/<slug>` paths pass the catch-all (line 117 regex matches lowercase-alnum-hyphen ≥20 chars and would otherwise redirect our release slugs to `/insights`)
3. **Last-updated comment** — bump date, note "press section allowlist added"

### Publishing path

Per the file's own header comment: the IAM deploy user has **no CloudFront Function permissions**. Publishing is manual:

1. Push code change to main (GitHub Actions syncs S3 — but the function itself is not deployed from the repo)
2. AWS Console → CloudFront → Functions → `url-rewrite` → paste new code
3. Save → Publish → Attach to distribution `E18AUIFBUGMXSB` (if not already attached)
4. Wait ~5 minutes for propagation
5. Verify with curl:

```
curl -sI https://taraniscapital.com/press | head -1          # expect 200
curl -sI https://taraniscapital.com/press/2026-05-01-... | head -1  # expect 200
curl -sI https://taraniscapital.com/press/                  | head -1  # expect 301 → /press
```

Flag in the PR description that this manual step is required before the live site will resolve `/press/*` correctly.

## 10. Sitemap

Add after the main-pages block in `sitemap.xml`:

```xml
<!-- Press releases -->
<url>
  <loc>https://taraniscapital.com/press</loc>
  <lastmod>2026-05-01</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
<url>
  <loc>https://taraniscapital.com/press/2026-05-01-taranis-capital-launches-biotech-fund</loc>
  <lastmod>2026-05-01</lastmod>
  <changefreq>yearly</changefreq>
  <priority>0.6</priority>
</url>
```

Bump the documented sitemap URL count in `CLAUDE.md` from 49 to 49 + N.

## 11. Navigation wiring

### Top nav (every page)

Insert `<li><a href="/press">Press</a></li>` between the Insights and Contact list items. On `press.html` itself, give it `class="active"`.

### Footer Navigation column (every page)

Insert `<li><a href="/press">Press</a></li>` between Insights and Contact in the footer `<ul class="footer-links">`.

### Mobile menu

The mobile toggle button is driven by `main.js` — no JS changes needed, but verify the new link renders and closes the menu on click. Add a quick manual test to the QA list.

## 12. Seed release (Claude Code deliverable)

To prove the full flow, Claude Code should ship **one** placeholder release alongside the scaffolding:

- Slug: `2026-05-01-press-section-launch` *(placeholder — Mark will replace with real first release)*
- Content: a short, obviously-placeholder body ("This is a placeholder release used to validate the press section layout and should be replaced before launch.")
- Marked with a visible banner at the top: `<div class="dev-banner">Placeholder — not for publication</div>` styled to be impossible to miss
- Excluded from sitemap until real content replaces it

Mark will replace the content before pushing to main; the placeholder exists only to test rendering during the PR review.

## 13. "Add a new release" workflow (document this in the PR)

For future ops — add to `PROJECT-LOG.md` or a new `docs/ADD-PRESS-RELEASE.md`:

1. Copy `press/_template.html` to `press/<YYYY-MM-DD-slug>.html`
2. Fill in: `<title>`, meta description, canonical, OG tags, JSON-LD, `<h1>`, `<time>`, body, quote (optional), contact block
3. Add a `<article class="press-card">` entry at the **top** of the `.press-grid` in `press.html`
4. Add a `<url>` entry in `sitemap.xml` and bump `<lastmod>` on `/press`
5. `git add` the two/three specific files → single-line commit → `git push`
6. GitHub Actions runs S3 sync + CloudFront invalidation
7. Hard-refresh `https://taraniscapital.com/press` to verify

No CloudFront function republish needed for subsequent releases — the `PREFIX_ALLOW` for `/press/` covers all future slugs.

## 14. QA checklist (Claude Code must run before opening the PR)

- [ ] `press.html` renders locally with correct nav, hero, grid, footer
- [ ] Seed release page renders with full metadata block + placeholder banner
- [ ] All ten-plus top-level pages carry the new "Press" nav link
- [ ] All top-level pages carry the new footer "Press" link
- [ ] Sitemap parses as valid XML
- [ ] `infra/cloudfront-url-rewrite.js` diffs cleanly vs. the live version — only additions, no removals
- [ ] No references to `computer://` or absolute Windows paths in any HTML (per CLAUDE.md)
- [ ] No bright yellow / light-blue off-brand colours introduced
- [ ] No files committed from the `.gitignore`'d directories (`Board of Advisors/`, `Documents/`, etc.)
- [ ] `git status` before push is clean of stray files
- [ ] Commit message is single-line, `-m "..."` form (Windows cmd.exe constraint per memory)
- [ ] PR description flags the **manual CloudFront Function republish** as a required post-merge step

## 15. Deployment sequence

1. Implement on a feature branch `feat/press-section` (don't commit directly to `main`)
2. Open PR against `main` with description including:
   - Screenshots of listing page + seed release
   - Diff highlights for the CloudFront function
   - Explicit reminder about the manual CF Function republish
3. Mark reviews, replaces placeholder content with real first release (or merges as-is and replaces in a follow-up commit)
4. Merge to `main` → GitHub Actions runs `aws s3 sync` + `cloudfront create-invalidation`
5. Mark (or whoever has console access) republishes the CloudFront Function via console
6. Verification curl commands from §9
7. Append entry to `docs/PROJECT-LOG.md`
8. Update `CLAUDE.md` sitemap URL count + "Last updated" line

## 16. Risks & watch-outs

| Risk | Mitigation |
|---|---|
| CloudFront catch-all redirects `/press/<slug>` to `/insights` if `PREFIX_ALLOW` isn't updated | §9 is explicit; QA list checks it |
| Nav/footer edits introduce inconsistency (one page missed) | Grep-based insertion; spot-check each modified file in the PR diff |
| Brand font drift — CLAUDE.md says Georgia/Calibri, live `insights.html` uses Playfair Display/Inter | Claude Code should ask Mark which is canonical before styling the new pages; don't silently choose |
| Google indexes the placeholder release if it ships to main | Keep placeholder out of sitemap; add `<meta name="robots" content="noindex">` on the placeholder page |
| Two GitHub accounts on Mark's machine trigger credential prompts | Verify `git config user.email` matches `Walkerma75` before pushing (per memory) |
| Someone commits from an ignored directory | `git add` specific files only — don't `git add .` (per CLAUDE.md) |

## 17. Open questions for Mark (answer before Claude Code starts)

1. **Brand font canon:** Playfair Display/Inter (matches live site) or Georgia/Calibri (matches brand doc)?
2. **Nav placement:** "Press" between Insights and Contact (recommended) or as a sub-item under Insights?
3. **First real release:** do you want the scaffolding to ship with a real first release baked in, or just the placeholder? If real, please provide headline, date, dateline, body, optional quote, media-contact details.
4. **Category tags on cards** (e.g. "Fund Launch", "Partnership", "Leadership", "Corporate"): want these from day one, or skip until we have enough volume to justify filtering?
5. **Subdomain press releases:** do any of the fund subdomains (fintech/datacentre/property/disruptive-tech/biotech) need their own press pages, or is all press centralised under the apex domain? (Recommended: apex only, with subdomains linking back.)

## 18. Acceptance criteria

The feature is "done" when:

- `/press` loads with a grid showing at least one release card
- `/press/<slug>` loads with full SEO metadata, valid JSON-LD, and the boilerplate blocks
- All top-level pages expose the new nav + footer link
- Sitemap is valid and includes the new URLs
- The CloudFront function is updated in the repo (and Mark has been clearly told to republish it)
- A PR is open with the full change set and a written description that matches this plan
- Nothing off-brand, no stray committed files, no broken links, no console errors on any modified page

---

**End of plan.** Hand this file to Claude Code along with a prompt like: *"Implement `PRESS-RELEASE-PLAN.md` exactly. Open a PR on branch `feat/press-section` against `main`. Answer the open questions in §17 first by asking me — don't guess."*

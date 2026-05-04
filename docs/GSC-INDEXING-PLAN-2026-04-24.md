# Google Search Console "Crawled – currently not indexed" — Fix Plan

**Site:** taraniscapital.com
**GSC issue:** Crawled – currently not indexed (66 URLs as of 2026-04-20)
**Report source:** `taraniscapital.com-Coverage-Drilldown-2026-04-24.xlsx`
**Prepared for:** Claude Code in `C:\Users\mark\Claude Cowork\Taranis Capital Website`
**Date:** 2026-04-24

---

## Executive summary

Of the 66 URLs flagged, only **3 are real pages on the current site**:

- `/board/abdulaziz-al-sayyari`
- `/board/ghassan-najmeddin`
- `/partners/jehanzeb-awan`

The other **63 are legacy WordPress URLs** — paginated archives (`/page/32/`), old news-article slugs, WP taxonomy (`/tag/*`, `/author/*`), custom-post-types (`/board_members/*`, `/team_member/*`), truncated LinkedIn paste fragments (`/ryft-raises-`, `/felix-secures-` etc.), and `http://`/`http://www.` variants. Google keeps re-crawling them from external backlinks and its own cached history of the old site, finds nothing, and files them under "Crawled – currently not indexed" (effectively soft-404 purgatory).

**Validation keeps failing because Google finds new legacy URLs each cycle, not because the site has a structural indexing fault.** The robots.txt fix that *did* validate (reported separately) is a good sign — that category is now clear.

The plan has three workstreams:

1. **Emit proper 301 redirects for legacy WP URLs** so Google removes them from the index cleanly instead of parking them. *(Biggest impact — covers 63 of 66.)*
2. **Strengthen the 3 real pages** so Google decides to index them. *(Thin content + weak internal linking is the likely cause.)*
3. **Keep the sitemap and canonical signals tidy** so nothing contradicts.

---

## URL classification from the drilldown

| Category | Count | Action |
|---|---:|---|
| A. Real pages not yet indexed | 3 | Enrich content + internal links + Person JSON-LD |
| B. WP paginated archives (`/page/N/`, `/insights/page/N/`, with/without `?trk=…`) | 19 | 301 → `/insights` |
| C. WP news/article slugs (unmigrated posts) | 27 | 301 → `/insights` |
| D. Truncated LinkedIn-copy fragments (`/ryft-raises-`, `/felix-secures-`, `/belvo-secures-`, `/grain-secures-`, `/leap-finance-`, `/standard-`, `/marshmallow-`, `/mews-secures-`, `/wealthtech-`) | 9 | 301 → `/insights` |
| E. WP taxonomy / custom post types (`/tag/*`, `/author/*`, `/team_member/*`, `/board_members/*`) | 4 | 301 — pattern-based |
| F. WP infra (`/members-area/`, `/embed/`, `*/feed/`) | 3 | 301 → `/` or `/insights` |
| G. `http://` / `http://www.` variants of old article | 2 | Already handled by HTTPS+canonical redirect; verify |
| H. Stale partner slug (`/partners/disrupts/`) | 1 | 301 → `/who-we-are#strategic-partnerships` |

---

## Workstream 1 — Emit 301 redirects for the 63 legacy URLs

**Mechanism:** Extend the existing `url-rewrite` CloudFront Function on distribution `E18AUIFBUGMXSB` (viewer-request event). This already handles clean URLs — add pattern-based 301 logic before the current rewrite logic.

### 1.1 Patterns to add (in this order)

All redirects should return **301 (Moved Permanently)** so Google drops the old URL and consolidates link equity onto the new one.

```
# Pagination archives (covers /page/3/, /page/20/, /page/26/, … and LinkedIn ?trk=... variants)
^/page/\d+/?(\?.*)?$                     → /insights                                    301
^/insights/page/\d+/?(\?.*)?$            → /insights                                    301

# WP taxonomy
^/tag/[^/]+/?$                           → /insights                                    301
^/author/[^/]+/?$                        → /                                            301

# WP custom post types → new profile URLs (slug-preserving)
^/team_member/([^/]+)/?$                 → /team/$1                                     301
^/board_members/([^/]+)/?$               → /board/$1                                    301

# WP infra
^/members-area/?$                        → /                                            301
^/embed/?$                               → /                                            301
^/.*/feed/?$                             → /insights                                    301

# Stale partner slug
^/partners/disrupts/?$                   → /who-we-are#strategic-partnerships           301

# Known legacy news slugs — catch-all: any top-level slug that isn't a known site path
# and looks like an old post (lowercase, hyphenated, ≥20 chars).
# Check $1 against the allowlist below BEFORE firing.
^/([a-z0-9][a-z0-9-]{19,})/?(\?.*)?$     → /insights                                    301

# Strip LinkedIn tracking on anything that falls through
?trk=public_post_main-feed-card-text     strip query, 301 to canonical
```

### 1.2 Allowlist for the catch-all

The catch-all in the final rule is powerful but risky. Before sending a slug to `/insights`, check it isn't one of the current top-level paths:

```
/ (root)
/index.html
/who-we-are
/our-approach
/our-funds
/insights
/contact
/fintech
/datacentres
/biotech
/disruptive-tech
/property
/cookie-policy
/privacy-policy
/board/*        (any slug under /board/)
/partners/*     (any slug under /partners/)
/team/*         (any slug under /team/)
/css/*
/js/*
/images/*
/fonts/*
/docs/*
/robots.txt
/sitemap.xml
/humans.txt
/llms.txt
/security.txt
```

Any request whose path is not in this allowlist AND whose slug looks like a legacy post (≥20 chars, lowercase-hyphen-alnum) → 301 to `/insights`.

### 1.3 http:// and www. normalisation

Confirm the existing CloudFront Function (or bucket policy) already redirects:

- `http://taraniscapital.com/*` → `https://taraniscapital.com/*` (301)
- `http://www.taraniscapital.com/*` → `https://taraniscapital.com/*` (301)
- `https://www.taraniscapital.com/*` → `https://taraniscapital.com/*` (301)

The two `http://` / `http://www.` legacy URLs in the report suggest this might not be fully enforced, or the rules predate Google's last crawl of those URLs. **Test with `curl -I` against all four host variants** before closing.

### 1.4 Deliverable

- Update the CloudFront Function source (commit it into the repo under, say, `infra/cloudfront-url-rewrite.js` so it's version-controlled — currently the function appears to live only in the AWS console).
- Deploy via AWS Console (deploy IAM user does not have CloudFront Function perms per `reference_iam_deploy_user` memory — use console).
- Wait for global propagation (~5 min) and verify with `curl -I` for a representative URL from each category:
  ```
  curl -I https://taraniscapital.com/page/32/
  curl -I https://taraniscapital.com/tag/taraniscapital/
  curl -I https://taraniscapital.com/author/abeeryehia/
  curl -I https://taraniscapital.com/team_member/mohamed-essam/
  curl -I https://taraniscapital.com/board_members/mike-chambers/
  curl -I https://taraniscapital.com/members-area/
  curl -I https://taraniscapital.com/embed/
  curl -I https://taraniscapital.com/binance-officially-launches-in-bahrain/feed/
  curl -I https://taraniscapital.com/partners/disrupts/
  curl -I "https://taraniscapital.com/page/3/?trk=public_post_main-feed-card-text"
  curl -I http://taraniscapital.com/taranis-capital-announces-its-advisory-board-including-fintech-heavyweights/
  curl -I https://taraniscapital.com/aazzur-raises-2m-to-accelerate-fintech-orchestration-platform-growth/
  ```
  All should return **301** with the correct `Location:` header.

### 1.5 Then request re-validation in GSC

Once deploy is confirmed, in Search Console → Pages → "Crawled – currently not indexed" → **Validate Fix**. Google will re-crawl a sample over 2–4 weeks.

---

## Workstream 2 — Help the 3 real pages get indexed

All three pages exist, have canonical tags, meta descriptions, Open Graph tags, and are in the sitemap. The likely reasons Google is declining to index them:

1. **Thin content.** Visible body text is only 328–364 words per page. Google's threshold for single-person bio pages is usually comfortably above 500 words when there's no other authority signal.
2. **Weak internal linking.** Each of the three is linked from just 2 files (likely only `who-we-are.html` and `sitemap.xml`). No sibling-cross-linking.
3. **No structured data.** No `Person` JSON-LD on the profile pages.
4. **No unique outbound signal** (no LinkedIn link, no cited publications, etc.) that would let Google verify "this is a real person worth indexing."

### 2.1 Content enrichment (3 pages)

For each of `/board/abdulaziz-al-sayyari`, `/board/ghassan-najmeddin`, `/partners/jehanzeb-awan`:

- Expand the bio to **≥ 500 words of unique, substantive body copy**. Pull from the Taranis People data file (`Taranis-People-Data-Collection.xlsx`) if there's richer source text than what's on the page today.
- Add a short "Areas of focus" or "Investment thesis contribution" paragraph — unique to each person, tied to Taranis's funds.
- Add a LinkedIn link (from `taranis-people-data.json`) where available.
- If a profile has no LinkedIn in the data file, flag it in `MISSING-PROFILE-INFO.md` (it's already tracked there — 11 people missing LinkedIn per CLAUDE.md).

### 2.2 Add Person JSON-LD to every profile page

Add this block to the `<head>` of each `/board/*.html`, `/partners/*.html`, and `/team/*.html` page. Values populated from `taranis-people-data.json`:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{full name}",
  "jobTitle": "{role}",
  "worksFor": {
    "@type": "Organization",
    "name": "Taranis Capital",
    "url": "https://taraniscapital.com"
  },
  "url": "https://taraniscapital.com{profile path}",
  "image": "https://taraniscapital.com{headshot path}",
  "sameAs": ["{linkedin URL if present}"]
}
</script>
```

This is a template change — apply to all ~40 profile pages in one pass, not just the 3 flagged ones, to uplift indexing across the site.

### 2.3 Add cross-links between profiles

On every `/board/*.html` page, add a "Other Investment Committee members" row at the bottom (5–6 thumbnails linking to siblings in the same fund). Same treatment for `/team/*` and `/partners/*`. This gives each profile 5–6 extra inbound internal links and moves them out of "orphan" territory.

### 2.4 Force re-crawl

After 2.1–2.3 deploy, use **Search Console → URL Inspection → Request Indexing** for the 3 specific URLs. It's a one-off manual nudge per URL; worth doing.

---

## Workstream 3 — Sitemap and signal hygiene

### 3.1 Audit sitemap.xml

The sitemap currently lists 49 URLs. Run through all 49 with a quick 200-check:

```bash
grep -oE 'https://[^<]+' sitemap.xml | xargs -I{} curl -s -o /dev/null -w "%{http_code} {}\n" {}
```

Anything that returns other than 200 should be removed (or fixed). A clean sitemap is a stronger indexing signal than a sitemap with 404s in it.

### 3.2 Confirm no lingering references to dead URLs

```bash
cd "C:\Users\mark\Claude Cowork\Taranis Capital Website"
grep -rE "(page/\d+|/tag/|/author/|/feed/|wp-content|wp-login|xmlrpc)" --include="*.html" .
```

Should return zero hits. If any exist (e.g. a hard-coded old link in a nav or footer), strip them — they leak crawl budget to dead URLs.

---

## Implementation order (recommended)

1. **Workstream 1.1–1.4** first — highest volume, biggest GSC win. Redirects only, no content changes.
2. **Workstream 3.1–3.2** — lightweight audit, catches anything 1 missed.
3. **Workstream 2.1–2.3** — content work, touches ~40 HTML files.
4. Request re-validation in GSC (1) and request indexing for the 3 real URLs (2.4).
5. Wait ~3 weeks. Re-pull the drilldown and compare.

---

## Risk register

| Risk | Mitigation |
|---|---|
| Catch-all regex in 1.1 redirects a legitimate future URL to `/insights` | Maintain the allowlist (1.2). Review the allowlist whenever a new top-level page is added. Consider a hard list of 63 explicit slugs instead of a catch-all if team prefers precision over coverage. |
| CloudFront Function size limit (10 KB) | Patterns as written are well under the cap. If the explicit-slug list grows, move article-slug redirects to S3 routing rules and keep only patterns in the Function. |
| JSON-LD typo → Google rejects structured data | Validate every generated page once with Google's Rich Results Test. |
| Content enrichment reveals missing data | Any person without a usable bio stays as-is; add to `MISSING-PROFILE-INFO.md`. Don't push half-rewritten profiles. |
| Deploy user has no Route 53 / CloudFront perms | Confirmed per `reference_iam_deploy_user` — do all CloudFront Function edits via console, keep source in repo for version control only. |

---

## Files Claude Code will touch

**New / modified infra:**
- `infra/cloudfront-url-rewrite.js` (new — version-controlled source of the CF Function)

**Modified site files:**
- All `board/*.html` (~24 files) — add JSON-LD, add cross-links, expand bio where flagged
- All `partners/*.html` (3 files) — same
- All `team/*.html` (~9 files) — same
- `docs/PROJECT-LOG.md` — append session entry per project convention
- `docs/PROPOSED-REDIRECTS.md` — mark sections as "implemented" once 301s deploy
- `TASKS.md` — cross off the indexing item

**Untouched:**
- `sitemap.xml` (unless 3.1 finds 404s)
- `robots.txt` (last GSC fix already validated)
- Fund pages, index.html (no changes needed)

---

## Hand-off note to Claude Code

Start with Workstream 1. The CloudFront Function change is the single highest-leverage fix and affects 63 of 66 flagged URLs. Don't enrich any bio content until the redirect layer is deployed and verified — otherwise you're re-emitting new canonical signals into a broken index state.

When you write the CloudFront Function file into `infra/`, the deploy workflow currently excludes `docs/*` and `*.md` but will include `infra/*` by default — either (a) exclude it explicitly in `.github/workflows/deploy.yml`, or (b) place it outside the deploy sync path. **Don't let a `.js` file get synced to S3 and served publicly under `/infra/…` — that would defeat the point of having version-controlled infra.**

# Proposed 301 Redirects — Old WordPress URLs → New Static Site

**Date:** 7 April 2026
**Purpose:** Prevent 404 errors in Google Search Console and preserve any link equity from the old WordPress site.

These redirects should be configured as S3 routing rules or CloudFront Functions.

---

## HIGH PRIORITY — Currently indexed by Google

These URLs are confirmed in Google's index right now and will generate 404 errors immediately.

| Old WordPress URL | → New URL | Notes |
|---|---|---|
| `/contact-us/` | `/contact` | Google has this indexed. New page is `/contact.html` |
| `/ai/` | `/disruptive-tech` | Old "AI" fund page → new Disruptive Tech Fund (covers AI/ML) |
| `/biotech/` | `/` | Biotech fund — no standalone page on new site yet (redirect to homepage, or create a biotech page) |
| `/datacentres/` | `/datacentres` | Same name but old URL has trailing slash |
| `/fintech/` | `/fintech` | Same name but old URL has trailing slash |
| `/insights/page/2/` | `/insights` | Old paginated insights page → new insights page |
| `/our-approach/` | `/our-approach` | Same page, trailing slash difference |
| `/who-we-are/` | `/who-we-are` | Same page, trailing slash difference |
| `/insights/` | `/insights` | Same page, trailing slash difference |

## HIGH PRIORITY — Old news/announcement posts

These were WordPress blog posts that likely have external backlinks (shared on LinkedIn, press sites, etc.).

| Old WordPress URL | → New URL | Notes |
|---|---|---|
| `/taranis-capital-receives-in-principle-approval-from-dfsa-to-establish-venture-capital-firm-in-difc-expands-focus-to-saudi-arabia/` | `/insights` | DFSA approval announcement — high-value press coverage |
| `/taranis-capital-appoints-h-e-osama-al-zamil-as-advisory-board-chairman/` | `/board/osama-al-zamil` | Redirect to his board profile |
| `/aazzur-raises-2m-to-accelerate-fintech-orchestration-platform-growth/` | `/insights` | Portfolio news post |

## MEDIUM PRIORITY — Old team/board appointment posts

The old WordPress site had `/appointment-news/person-name/` style URLs for team announcements. These should redirect to the corresponding new profile pages.

| Old WordPress URL (pattern) | → New URL | Notes |
|---|---|---|
| `/appointment-news/nicholas-bingham*/` | `/team/nicholas-bingham` | Founding Partner & CEO |
| `/appointment-news/mark-walker*/` | `/team/mark-walker` | Founding Partner & CTO |
| `/appointment-news/osama-bukhari*/` or `/appointment-news/osama-ben-saleh*/` | `/team/osama-bukhari` | Founding Partner |
| `/appointment-news/bijna-kotak-dasani*/` or `/appointment-news/dr-bijna*/` | `/team/bijna-kotak-dasani` | CIO |
| `/appointment-news/milan-radia*/` | `/team/milan-radia` | Partner |
| `/appointment-news/amit-varma*/` | `/team/amit-varma` | Director |
| `/appointment-news/svitlana-burlakova*/` | `/team/svitlana-burlakova` | VP Legal |
| `/appointment-news/mohamed-essam*/` | `/team/mohamed-essam` | VP Legal |
| `/appointment-news/emad-zowawi*/` | `/team/emad-zowawi` | CLO |
| `/appointment-news/jack-hollander*/` | `/board/jack-hollander` | Board adviser |
| `/appointment-news/joel-blake*/` | `/board/joel-blake` | Board adviser |
| `/appointment-news/david-parker*/` | `/board/david-parker` | Board adviser |
| `/appointment-news/michael-boevink*/` | `/board/michael-boevink` | Board adviser |
| `/appointment-news/bruno-martorano*/` | `/board/bruno-martorano` | Board adviser |
| `/appointment-news/osama-al-zamil*/` | `/board/osama-al-zamil` | Board chairman |
| `/appointment-news/rayan-al-karawi*/` | `/board/rayan-al-karawi` | Board adviser |
| `/appointment-news/ayman-sejiny*/` | `/who-we-are` | Board adviser (no individual page found) |

## LOW PRIORITY — Trailing slash normalisation

All old WordPress URLs had trailing slashes. The new static site uses no trailing slashes. A catch-all rule to strip trailing slashes and 301 redirect would handle all of these automatically.

| Pattern | → | Notes |
|---|---|---|
| Any URL ending in `/` (except root `/`) | Same URL without trailing slash | Prevents duplicate content, fixes all WP URL patterns |

## LOW PRIORITY — WordPress infrastructure URLs

These will 404 naturally and Google will drop them, but redirecting to homepage is cleaner.

| Old WordPress URL | → New URL | Notes |
|---|---|---|
| `/wp-login.php` | `/` | WP admin login |
| `/wp-admin/` | `/` | WP admin panel |
| `/xmlrpc.php` | `/` | WP XML-RPC |
| `/feed/` | `/insights` | Old RSS feed |

---

## Implementation Options

**Option A — CloudFront Function (recommended)**
Create a CloudFront Function on the viewer-request event that handles all redirects. This is the fastest (edge-level) and most flexible approach. Can handle regex patterns for the `/appointment-news/*` catch-all.

**Option B — S3 Routing Rules**
Add redirect rules to the S3 bucket website configuration. Limited to 50 rules and doesn't support regex, so less flexible for pattern matching.

**Option C — Hybrid**
Use a CloudFront Function for the trailing-slash normalisation and pattern-based redirects (appointment-news/*), and S3 routing rules for specific one-to-one URL redirects.

---

## Missing Page: Biotech Fund

The old site had `/biotech/` as a standalone fund page that is currently indexed by Google. The new site has no biotech.html equivalent (there's a biotech.taraniscapital.com subdomain for a different biotech-focused microsite on Replit). Consider creating a biotech.html fund page similar to fintech.html, datacentres.html, property.html, and disruptive-tech.html. This would preserve the SEO value of the old /biotech/ URL.

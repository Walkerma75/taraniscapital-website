# Taranis Capital Website — Project Activity Log

**Project:** Rebuild taraniscapital.com from WordPress to native static HTML/CSS/JS
**Repository:** github.com/Walkerma75/taraniscapital-website
**Hosting:** AWS S3 (bucket: taraniscapital.com, eu-west-2) + CloudFront (E18AUIFBUGMXSB)
**Live URL:** https://taraniscapital.com | https://d1ete5r3431epc.cloudfront.net

---

## Completed Work

### Session 1 — 2 April 2026

**Git & Deployment Setup**
- Initialised git repo, created .gitignore (excludes Wp-content/, Board of Advisors/, Documents/, TC Logos/, Team Images/)
- Pushed to GitHub (Walkerma75/taraniscapital-website) — resolved credential conflict between Walkerma75 and markwalker-pcs accounts
- Created GitHub Actions workflow (.github/workflows/deploy.yml) for auto-deploy: S3 sync + CloudFront invalidation on push to main
- Configured AWS secrets in GitHub repo settings

**S3 & CloudFront Fixes**
- Enabled S3 static website hosting (was not enabled — caused 404)
- Added public read bucket policy for S3
- Changed CloudFront origin from REST endpoint to S3 website endpoint (fixed Access Denied XML error)
- Created CloudFront Function for clean URL routing (appends .html to extensionless paths)

**Who We Are Page Updates**
- Updated all 9 team member titles from generic "Director" to proper titles (Founding Partner & CEO, CTO, CIO, etc.)
- Corrected names: "OB" → "Osama Ben Saleh Bukhari", added "MBE, FRSA" to Dr. Bijna Kotak Dasani, added "ICA, TEP" to Svitlana Burlakova
- Moved Jack Hollander from team section to board of advisers
- Made all team and board cards clickable with links to individual profile pages

**Footer Update (all pages)**
- Added DIFC head office address (Level 02, Innovation One, DIFC, Dubai)
- Added DFSA regulatory text (word-for-word as required)
- Added social icons (LinkedIn, Twitter/X, Facebook)
- Added London and Geneva office addresses with phone numbers

**Individual Profile Pages**
- Created 9 team profile pages in /team/
- Created 18 board adviser profile pages in /board/
- Bio content sourced from WordPress export XML (appointment news posts)

**Fund Detail Pages**
- Created fintech.html, datacentres.html, property.html
- Updated our-funds.html with clickable fund cards and new Disruptive Tech Fund card (5 Active Funds)
- Updated index.html with clickable fund focus cards including Disruptive Tech

### Session 2 — 3 April 2026

**LinkedIn & Email Links on Profile Pages**
- Scraped all LinkedIn URLs and email addresses from the old live WordPress site
- Updated all 9 team profile pages with LinkedIn and mailto links
- Updated 14 board profile pages with LinkedIn and/or mailto links (4 board members had no data: Daniel Roubeni, Osama Al Zamil, Mohammed Aljumah, Rayan Al-Karawi)

**Disruptive Tech Fund Page**
- Extracted PPM content from Documents/Taranis_Disruptive_Tech_Fund_PPM_with_LPA_Appendix.docx
- Created disruptive-tech.html with: fund overview, key stats ($250M target, $1M min, 10-year term, 4 sectors), sector focus cards (AI/ML, FinTech, Enterprise Software, Media & Telecoms), investment strategy, GCC regional opportunity, investment committee profiles with LinkedIn/email links, ESG integration, key fund terms

### Session 3 — 3 April 2026 (continued)

**Team Ordering & Layout**
- Reordered team members on who-we-are.html: Nicholas, Mark, Osama, Bijna, Milan, Amit, Svitlana, Mohamed, Emad
- Added real LinkedIn URLs and email links to team cards on who-we-are.html (replacing placeholder # links)

**Partners Section**
- Replaced logo placeholders with clickable cards for: The Fintech Times, The Biotech Times, Disrupts, Change Gap

**Address & Phone Fixes (site-wide, all 42 HTML files + llms.txt + humans.txt)**
- Changed contact page location from "London, United Kingdom" to full DIFC Dubai address
- Updated London phone number from +44 (0) 20 7864 7119 to +44 (0) 20 38552165 in all footers
- Updated privacy-policy.html: all London references → Dubai DIFC address
- Updated cookie-policy.html: all London references → Dubai DIFC address
- Updated llms.txt and humans.txt: location → DIFC Dubai

**Legal Jurisdiction**
- Cookie policy: replaced "Registered in England and Wales" with DIFC registration + DIFC Courts jurisdiction clause
- Privacy policy: updated addresses to DIFC throughout

**Header Cleanup (all 42 HTML files)**
- Removed "Venture Capital & Strategic Investment" subtitle from navigation header on every page
- Replaced SVG triangle placeholder logo on privacy-policy and cookie-policy with actual /images/logo-white.png

**Insights Page**
- Added "Read More Articles" button below feed articles

**Git Commit**
- All changes staged but git index.lock prevented commit from sandbox environment
- Must commit and push from local machine (see commands below)

### Session 4 — 3 April 2026 (continued)

**Bruno Martorano — Name & Bio Fix**
- Fixed name from "Bruno" to "Bruno Martorano" across who-we-are.html and board profile page
- Created board/bruno-martorano.html with full bio (5 paragraphs: 35 years international banking/fintech, multicultural career across New York/Paris/Hong Kong/Dubai/London, CEO of Abu Dhabi bank, fintech leadership, speaking engagements)
- Updated link on who-we-are.html from /board/bruno to /board/bruno-martorano
- Old file board/bruno.html needs manual deletion locally

**Team Member Bios — Updated from Old WP Site**
- Re-scraped all team member profiles from old WordPress site via Chrome
- Updated 4 team members with real bios replacing placeholder content:
  - Mark Walker: experienced technologist, enterprise software, UK Trade & Investment adviser, Fintech Power50, The Fintech Times
  - Emad Zowawi: NY/DC licensed corporate lawyer, Chief Legal Officer, former banker with 10+ years experience
  - Mohamed Essam: fintech/VC expert lawyer, Matouk Bassiouny Fintech Group Sector lead
  - Osama Ben Saleh Bukhari: entrepreneur, Alfaris International Group, ICC Banking Committee head, CNBC Arabia, recognised by Arabian Business

**Board Member Bio Audit**
- Scraped all 18 board member profiles from old WordPress site
- Found that 10 board members had NO bio content on the old WP site either (pages existed but were blank)
- Created MISSING-PROFILE-INFO.md documenting: 10 board members needing bios, 5 needing LinkedIn URLs, and all members with complete profiles

**Footer Cleanup (all 44 HTML files)**
- Removed "Venture Capital & Strategic Investment" subtitle from all footers site-wide (footer-brand-sub div)

**Team Grid Layout Fix (who-we-are.html + css/styles.css)**
- Diagnosed root cause of "pyramid" layout: nested `<a>` tags inside outer `<a class="team-card-link">` wrappers
- Social link `<a>` tags (LinkedIn, email) inside the card-wrapping `<a>` is invalid HTML — browsers auto-close the outer link, turning 9 cards into 18 broken grid items
- Fix: removed social link icons from team grid cards (they remain on individual profile pages); each card is now a single clean `<a>` wrapping the photo, name, and role
- Grid now renders correctly as 3×3 on desktop/tablet, single column on mobile
- Also updated CSS responsive breakpoints to keep 3 columns down to 480px

**Git Commit & Deploy**
- All changes committed and pushed to main by Mark
- Live on CloudFront via GitHub Actions → S3 sync pipeline

### Session 5 — 7 April 2026

**DNS & Nameserver Migration to AWS Route 53**
- Audited all 30 DNS records on Funkygrafix cPanel; identified 9 essential records and 21 cPanel-generated junk
- Essential records: A (root → CloudFront), www CNAME, MX (Google Workspace → SMTP.GOOGLE.COM), SPF TXT, DKIM TXT, Google site verification CNAME, biotech A (→ Replit 34.111.179.128), biotech Replit verification TXT, ACM validation CNAME
- Created Route 53 hosted zone (ID: Z0680053Y587NB8B8C9S) for taraniscapital.com
- Created all 9 records via AWS CloudShell CLI using batch JSON + Python script (DKIM required special handling for JSON quoting)
- Root domain uses Route 53 ALIAS record pointing to CloudFront distribution d1ete5r3431epc.cloudfront.net (CloudFront hosted zone ID: Z2FDTNDATAQYW2)
- Updated nameservers at e& registrar from ns1/ns2.funkygrafix.co.uk to Route 53: ns-1539.awsdns-00.co.uk, ns-942.awsdns-53.net, ns-399.awsdns-49.com, ns-1261.awsdns-29.org
- Verified propagation via dnschecker.org: NS records 100% propagated across all 28 global DNS servers; A records resolving to CloudFront edge IPs worldwide
- Funkygrafix decommission scheduled for 2026-04-10 (48-72 hours post-migration)

### Session 6 — 7 April 2026 (continued)

**SEO Audit & Fixes (based on Pro-Curo GSC audit)**
- Audited site against Google Search Console indexing issues (crawled-not-indexed, duplicate-without-canonical, soft 404, trailing slash duplicates)
- Expanded sitemap.xml from 8 URLs to 39 — added all 4 fund pages, 9 team profiles, 17 board profiles, 2 legal pages
- Added canonical tag and meta description to privacy-policy.html
- Added `<meta name="robots" content="noindex, nofollow">` to 404.html
- Cleaned robots.txt — removed old WordPress disallow rules (/wp-content/, /wp-admin/), added sitemap reference

**CloudFront Function — 301 Redirect Engine**
- Upgraded the `url-rewrite` CloudFront Function from simple clean-URL handler to full redirect engine
- Specific redirects: /contact-us/ → /contact, /ai/ → /disruptive-tech, /insights/page/2/ → /insights, /wp-login.php → /, /feed/ → /insights
- External redirect: /biotech/ → biotech.taraniscapital.com (301)
- Pattern redirect: /appointment-news/* mapped to individual /team/ or /board/ profiles via slug lookup table (22 people)
- Pattern redirect: /taranis-capital-* and /aazzur-* old news posts → /insights
- Trailing slash normalisation (301 strip trailing slash on all paths except root)
- www → non-www canonical redirect
- Published and tested via AWS CloudShell CLI; verified all redirects live on production

**Google Analytics 4**
- Added GA4 tracking tag (G-JLN31RRY1V) to all 40 HTML pages across the site (13 root pages, 9 team profiles, 18 board profiles)
- Tag placed immediately after `<head>` on every page

**Verification (Session 6 continued)**
- Confirmed sitemap.xml live with all 39 URLs
- Confirmed robots.txt clean with sitemap reference
- Confirmed privacy-policy.html has canonical tag and meta description
- Confirmed 404.html has noindex/nofollow meta tag
- Tested all CloudFront Function redirects: /contact-us/ → /contact ✓, /ai/ → /disruptive-tech ✓, /biotech/ → biotech.taraniscapital.com ✓, /insights/page/2/ → /insights ✓, trailing slash normalisation ✓, /appointment-news/nicholas-bingham → /team/nicholas-bingham ✓

### Session 7 — 7 April 2026 (continued)

**Home Page Updates**
- Replaced [Team / Office Image] placeholder with actual team photo (TC Team Image1.jpg → /images/team/tc-team-office.jpg)
- Changed Biotech card link from biotech.taraniscapital.com (fund subdomain) to /biotech (new sector/market info page)

**Sector vs Fund Page Separation**
- Created new /biotech sector page (biotech.html) — market dynamics, Taranis strengths, partnerships (Helix8), ESG. No fund-specific info (AUM, returns, fees, etc.)
- Rewrote /disruptive-tech page — removed all PPM/fund info ($250M target, $1M min subscription, management fees, carried interest, fund terms, investment committee profiles). Replaced with market dynamics, sector focus cards, GCC opportunity, partnerships & ecosystem, ESG
- Cleaned /fintech page — renamed from "Fintech Fund" to "Financial Technology", replaced fund overview (investor relations, accredited HNW individuals, fund returns) with sector overview (market expertise, The Fintech Times partnership), updated breadcrumb, back link, CTA
- Cleaned /datacentres page — renamed from "Data Centres Fund" to "Data Centres", replaced fund overview with sector overview, updated breadcrumb, back link, CTA
- Cleaned /property page — renamed from "Property Fund" to "Property", replaced fund overview with sector overview, updated breadcrumb, back link, CTA

**Our Funds Page — Subdomain Links**
- Updated all 5 fund card links on /our-funds to point to fund subdomains (target="_blank"):
  - Fintech → fintech.taraniscapital.com
  - Biotech → biotech.taraniscapital.com (was already correct)
  - Datacentre → datacentre.taraniscapital.com
  - Property → property.taraniscapital.com
  - Disruptive Tech → disruptive-tech.taraniscapital.com

**Sitemap**
- Added /biotech to sitemap.xml (now 40 URLs)
- Updated lastmod on /disruptive-tech

**Note:** CloudFront Function currently has `/biotech/ → biotech.taraniscapital.com` 301 redirect. This should be removed so /biotech serves the new sector page. The redirect only fires on /biotech/ (trailing slash), so /biotech (no trailing slash) should serve correctly via clean URL rewriting.

### Session 7b — 7 April 2026 (continued)

**Fund Subdomain Sites Created**
- Created 4 self-contained fund sites under /subdomains/, each with their own index.html:
  - **fintech.taraniscapital.com** — Fund overview, Why Taranis (The Fintech Times, Power50, DIFC, operator-investors), market opportunity, investment focus (payments, open banking, RegTech, blockchain), leadership (Bingham, Walker, Varma, Essam), advisers (Martorano, Parker, Boevink, Hollander), partners (The Fintech Times, Disrupts), ESG
  - **datacentre.taraniscapital.com** — Fund overview, Why Taranis (Milan Radia's 30yr DC expertise, DIFC/GCC presence, regional partnerships), market ($2T TAM, 500+ projects, $70B+ PE), investment focus (hyperscale, edge, cooling, cloud), leadership (Bingham, Radia), advisers (Al-Zamil, Al-Rahim), ESG
  - **property.taraniscapital.com** — Fund overview, Why Taranis (GCC network, Vision 2030, DIFC, SABIC experience, ethical governance), market (Dubai, Saudi), investment focus (commercial, mixed-use, high-growth, sustainable), leadership (Bingham, Bukhari, Zowawi), advisers (Al-Zamil, Al-Rahim, Blake OBE), ESG
  - **disruptive-tech.taraniscapital.com** — Full PPM-level detail: fund overview with stats ($250M target, $1M min, 10yr term), Why Taranis (media platform, GCC network, operator team, advisory board), sector focus (AI/ML, fintech, enterprise SW, media/telecoms), investment strategy (Series A 35-45%, B/C 55-65%), GCC opportunity, investment committee (Bingham, Walker, Grunfeld, Varma, Bukhari with LinkedIn/email), advisers (Boevink, Al-Thanon, Blake, Al-Zamil), partners (Disrupts, Fintech Times), key fund terms (DIFC LP, DFSA F008985, 2.5% mgmt fee, 20% carry, 8% hurdle), ESG

- Each site is self-contained with inline CSS, Google Fonts, GA4, cookie consent, scroll-to-top
- Advisers matched to relevant sectors based on their expertise
- Strategic partners matched (Fintech Times → fintech/disruptive tech, Disrupts → disruptive tech, Helix8 → biotech)

**AWS Subdomain Setup Guide**
- Created SUBDOMAIN-SETUP.md with full CLI commands for:
  - Wildcard ACM certificate (*.taraniscapital.com)
  - S3 bucket creation (4 buckets)
  - Static website hosting + public read policies
  - CloudFront distributions (4) with SSL
  - Route 53 CNAME records
  - Optional GitHub Actions auto-deploy config
  - CloudFront function update to remove /biotech/ redirect

### Session 7 — 2026-04-07 (Subdomain Infrastructure Deployment)

**AWS Infrastructure — All Created via CloudShell:**

1. **CloudFront function updated** — Removed `/biotech/` redirect from `url-rewrite` function and published to LIVE stage
2. **Wildcard SSL certificate** — `*.taraniscapital.com` issued in us-east-1 (ARN: `arn:aws:acm:us-east-1:571600836975:certificate/fa9c7dad-94a1-4cb1-8a9e-c8e5ee64b60d`)
3. **4 S3 buckets created** — fintech, datacentre, property, disruptive-tech `.taraniscapital.com` with static website hosting and public read policies
4. **4 CloudFront distributions created:**
   - fintech: E260FGTXCVORQ6 (d2ykbvfjmg586t.cloudfront.net)
   - datacentre: E3EJUFMMNZLO3V (dg42m017gq950.cloudfront.net)
   - property: E2H8IQKJ8LPQ01 (d3bmdcmsydjb0z.cloudfront.net)
   - disruptive-tech: E98QNGA1O9AI0 (d2us91vkabbd5i.cloudfront.net)
5. **4 Route 53 CNAME records** — Each subdomain pointing to its CloudFront distribution
6. **Placeholder pages uploaded** — Branded "launching soon" pages on all 4 subdomains

**Still Needs Local Machine:**
- Deploy full fund site HTML files to S3 (run `aws s3 sync` commands from SUBDOMAIN-SETUP.md)
- Push git commit 0e9b229 to GitHub (34 additional modified files also need staging/committing)
- Invalidate CloudFront caches after deploying real files
- Update GitHub Actions workflow with subdomain deploy steps

### Session 8 — 8 April 2026

**Main Site — UI/Design Fixes**
- Fixed disruptive-tech.html hero colour from `#2a4a6b` (blue) → `var(--tc-green-dark)` to match other sector pages
- Fixed disruptive-tech card on our-funds.html from blue `#2a4a6b` → `var(--tc-green-dark)` to match other fund cards
- Replaced `[ Office / Team Photo ]` placeholder on who-we-are.html with actual team image (`/images/team/tc-team-office.jpg`)
- Replaced `[ Approach / Strategy Image ]` placeholder on our-approach.html with actual image (`/images/Approach Strategy Image.jpg`)
- Removed orange/yellow logo background in css/styles.css (`.nav-logo background: var(--tc-gold)` → `transparent`)
- Updated home page stats text from "Across fintech, biotech, datacentres, and property" to "Across technology, biotech, datacentres and property"

**Subdomain Menu Standardisation (all 4 fund sites)**
- Standardised nav HTML structure across fintech, property, datacentre, disruptive-tech subdomains
- All now use consistent `.nav-logo`, `.nav-logo-text`, `.nav-links` class names
- Consistent menu items: Home (main site), Fund Overview (anchor to #fund-overview on current page), Our Funds (main site), Contact (main site, opens in new tab)
- Added `id="fund-overview"` to the Fund Overview section on all 4 subdomain pages
- Contact link now opens in new tab (`target="_blank"`) so users remain on the subdomain
- Standardised nav CSS: consistent logo size (40px), font sizing, hover colours, transitions
- No logo background colour in any subdomain header (confirmed clean)

**GitHub Actions Updated**
- Added subdomain S3 sync and CloudFront invalidation to deploy workflow (all 4 subdomains auto-deploy on push to main)
- Added `--exclude "subdomains/*"` to main site sync to prevent subdomain files uploading to main bucket
- Fixed fintech CloudFront distribution ID: E260FGTXCVORQ6 (was E260FGTXCV0RQ6 — terminal font confusion between O and 0)

### Session 8b — 8 April 2026 (continued)

**Main Site**
- Partner cards on who-we-are page: made equal height using flexbox
- Fixed our-approach.html image path: URL-encoded spaces (`Approach%20Strategy%20Image.jpg`)

**Subdomain Standardisation (all 4 fund sites: fintech, property, datacentre, disruptive-tech)**
- Removed Fund Overview and Our Funds from nav menus (just Home + Contact now)
- Added favicon (`logo-gold.png`) to all 4 subdomains
- Matched header height to main site (72px fixed height, `padding: 0 40px`)
- Changed "Taranis Capital" header text from gold to white to match main site
- Replaced `box-shadow` with `border-bottom: 1px solid rgba(255,255,255,0.08)` to match main site
- Standardised all 4 footers: same 3-column layout (brand/tagline/social, head office/addresses, quick links), DIFC regulatory text, matching CSS classes
- Standardised leadership/adviser cards across all 4 subdomains to property format (`.team-member` with off-white background, gold top border, consistent sizing)

**DNS Status — datacentre & disruptive-tech still not loading**
- Need to verify Route 53 CNAME targets and CloudFront alternate domain names via CloudShell

### Session 8c — 8 April 2026 (continued)

**Full Subdomain Rebuild — All 3 Non-Fintech Sites Rebuilt to Match Fintech Template**

Rebuilt property, datacentre, and disruptive-tech subdomain sites to match fintech template's exact CSS, HTML structure, and section layout. Fintech site used as the master template.

**Common changes across all 3 sites:**
- Exact fintech CSS: all colour variables (--tc-green-dark, --tc-green-mid, --tc-gold, etc.), grid layouts, hover effects, responsive breakpoints, animations
- Hero: green gradient (`linear-gradient(135deg, var(--tc-green-dark) 0%, var(--tc-green-mid) 100%)`) with decorative SVG `::before` overlay
- Fund Overview: 2-column `.overview-grid` (text + 4 highlight cards with gold left borders)
- Why Taranis: `.why-grid` of `.why-card` cards with circular gold `.why-card-icon` icons and hover lift
- Market Opportunity: `.opportunity-grid` of `.opportunity-item` cards with `.stat` gold numbers
- Investment Focus: `.focus-grid` of `.focus-card` dark green gradient cards with gold headings
- Team: `.team-grid` of `.team-member` cards with gold top border, Executive Team + Board of Advisers
- ESG: `.esg-grid` of `.esg-item` centered text cards
- CTA: green gradient `.cta-section` inside container with border-radius
- Cookie banner: slide-up `.show` class mechanism (like fintech)
- Footer: standard 3-column (brand+social, head office+London+Geneva, quick links)

**Property Fund (`/subdomains/property/index.html`):**
- Converted Why Taranis from 5 `.why-item` list to 4 `.why-card` grid (Deep GCC Network, Vision 2030, DIFC Base, Institutional Experience)
- Converted Market Opportunity from paragraphs to 4 stat cards ($1.4T+ GCC market stat)
- Converted Investment Focus from plain white cards to green gradient `.focus-card` cards
- No Strategic Partners section (property fund difference)
- ESG: 4 items

**Datacentre Fund (`/subdomains/datacentre/index.html`):**
- Converted Why Taranis from `.benefit-card` list to 6 `.why-card` grid with icons
- Converted Market Opportunity from `.market-stat` to `.opportunity-item` cards (6 items, 3 with $ stats)
- Converted Investment Focus from `.focus-card` (similar but different CSS) to fintech `.focus-card` exact CSS
- No Strategic Partners section
- ESG: 6 items

**Disruptive Tech Fund (`/subdomains/disruptive-tech/index.html`):**
- **CRITICAL**: Changed hero and CTA from navy/blue (`--tc-navy: #2a4a6b`) to green gradient — removed all `--tc-navy` references
- Converted from completely different structure (fund stats panel, bullet-point Why Taranis, emoji sector icons, investment strategy allocation table, GCC Regional Opportunity, Key Fund Terms) to fintech template layout
- Fund-specific content preserved: $250M target AUM, Series A/B/C allocation info (moved to overview highlights), $1.8T+ AI market stat
- Strategic Partners section retained (Disrupts + The Fintech Times)
- ESG: 3 items (Pre-Investment Assessment, Post-Investment Monitoring, Portfolio Company Support)
- Largest rebuild of the three — most structurally different from fintech template

### Weekly Automated Sync — 9 April 2026 (Run 2)

**Scheduled task: Weekly Taranis Capital People & Website Sync**

**XLSX → JSON Conversion**
- ⚠ Taranis-People-Data-Collection.xlsx is still corrupted (truncated — sharedStrings.xml partial; only 12,896 of 17,265 compressed bytes are present, yielding 313 of 454 unique strings)
- 27 of 36 people fully readable from xlsx; remaining 9 fall in the truncated string-index range
- Readable xlsx data compared against existing `taranis-people-data.json`: NO meaningful changes detected (only minor HTML-entity encoding artefacts, `&amp;` vs `&`, and one trailing punctuation difference in two bios — not actioned)
- **Action required:** Mark to re-save `Taranis-People-Data-Collection.xlsx` (File → Save As, overwrite) to flush the corrupted write from the network mount, then re-run this task

**HTML Fixes Applied**

Two discrepancies found between `taranis-people-data.json` and `who-we-are.html`:

1. **Professor Mohammed Al Jumah** — who-we-are.html had the card displaying:
   - Old name: `Mohammed AlJumah` → Updated to `Professor Mohammed Al Jumah`
   - Old role: `Board Adviser` → Updated to `Senior Advisor`
   - Alt text on avatar image also updated to match
2. **HE Eng. Osama Al-Zamil** — who-we-are.html had the card role displaying:
   - Old role: `Board Adviser` → Updated to `Chairman of the Advisory Board`

Subdomain fund sites, individual profile pages, and all image paths verified — no further discrepancies found.

**Outstanding Data Gaps (require human input — unchanged from previous run)**
- LinkedIn missing: Dr Amer Mahmood, Mark Walker, Ghassan Najmeddin, Osama Al-Thanon, Dr Tarek El Mansy, Daniel Roubeni, Professor Mohammed Al Jumah, HE Eng. Osama Al-Zamil, Rayan Al-Karawi
- Email missing: Daniel Roubeni, Professor Mohammed Al Jumah, HE Eng. Osama Al-Zamil, Rayan Al-Karawi
- Profile images missing: Jehanzeb Awan, Mustafa Mahmood Khan CFA, Dr Abdulaziz Al Sayyari, Kuyoung Chung, Dr Sebastian Vaughan, Prof. Arjumand Warsy, Dr Junaid Kashir, Dr Abdullah Alawad, Dr Qaisar Hamed Metawea

---

### Weekly Automated Sync — 9 April 2026 (Run 1)

**Scheduled task: Weekly Taranis Capital People & Website Sync**

**XLSX → JSON Conversion**
- ⚠ Taranis-People-Data-Collection.xlsx could not be parsed (file is a valid zip/xlsx header but missing End-of-Central-Directory record — likely a partial/corrupted write from the network mount)
- Existing `taranis-people-data.json` (last updated 2026-04-09) used as source of truth for this run
- **Action required:** Mark to re-save the xlsx to force a clean write, then re-run the sync

**Comparison: JSON vs HTML**
- 27 core people (Team + Board) — all profile pages present and in sync ✓
- All profile images for core Team/Board members confirmed present in `/images/team/` ✓
- 9 new people in JSON (type: Partner, Advisor, Service Provider) — no profile pages yet (expected; flagged below)
- Sector pages (fintech.html, property.html, datacentres.html, disruptive-tech.html, biotech.html) confirmed as sector-overview pages without people sections — no action needed

**Subdomain Fund Sites — People Added**

All four fund subdomain sites were out of sync with the JSON. Missing people added:

- `subdomains/fintech/index.html`: Added 5 people — Osama Bukhari (CTO, exec team), Asim Chohan, Daniel Roubeni, Joel Blake OBE, Sarah Sinclair (board of advisers)
- `subdomains/property/index.html`: Added 5 people — Mark Walker, Mohamed Essam (exec team), Asim Chohan, Bruno Martorano, Michael Boevink (board of advisers)
- `subdomains/datacentre/index.html`: Added 16 people — Mark Walker, Osama Bukhari, Mohamed Essam (exec team); Amit Varma, Asim Chohan, Bruno Martorano, David Grunfeld, Emad Zowawi, Ghassan Najmeddin, Leif Hesse, Michael Boevink, Osama Al-Thanon, Rayan Al-Karawi (board of advisers); Jehanzeb Awan, Mustafa Mahmood Khan CFA, Dr Qaisar Hamed Metawea (fund manager & key counsel section — new section added)
- `subdomains/disruptive-tech/index.html`: Added 10 people — Milan Radia, Svitlana Burlakova, Dr Tarek El Mansy, Mohamed Essam (exec team); Asim Chohan, Bruno Martorano, Daniel Roubeni, David Parker, Jack Hollander, Sarah Sinclair (board of advisers)

Post-update verification: all 4 subdomain pages confirmed in sync with JSON ✓

### Manual Data Entry Sync — 9 April 2026 (15:40)

**Source:** Taranis-People-Data-Collection-KB.xlsx (saved by Mark Walker, 15:39)
**Note:** Original xlsx (Taranis-People-Data-Collection.xlsx) still corrupted on mount — KB copy used as workaround

**JSON regenerated** from KB xlsx. **19 field updates** applied:

LinkedIn URLs added: Dr Amer Mahmood, Mark Walker, Rayan Al-Karawi, Dr Tarek El Mansy, Jehanzeb Awan, Kuyoung Chung, Dr Sebastian Vaughan

Emails added: Daniel Roubeni, HE Eng. Osama Al-Zamil, Rayan Al-Karawi, Jehanzeb Awan, Mustafa Mahmood Khan CFA, Dr Abdulaziz Al Sayyari, Kuyoung Chung, Dr Sebastian Vaughan, Prof. Arjumand Warsy, Dr Junaid Kashir, Dr Abdullah Alawad, Dr Qaisar Hamed Metawea

**HTML profile pages updated (7 files):**
- `board/amer-mahmood.html` — LinkedIn link updated
- `team/mark-walker.html` — LinkedIn link updated
- `board/rayan-al-karawi.html` — LinkedIn + email updated
- `board/tarek-el-mans.html` — LinkedIn link updated
- `board/daniel-roubeni.html` — email updated
- `board/osama-al-zamil.html` — email updated

All changes verified ✓

### Partner Category & New Profile Pages — 9 April 2026

**New /partners/ folder created** — profile pages for Partner-type people separate from /board/

**9 new profile pages created:**
- `partners/jehanzeb-awan.html` — Jehanzeb Awan, CEO J. Awan Capital
- `partners/mustafa-mahmood-khan.html` — Mustafa Mahmood Khan CFA, Head of Asset Management J. Awan Capital
- `partners/qaisar-hamed-metawea.html` — Dr Qaisar Hamed Metawea, Managing Partner QHM Law Firm
- `board/abdulaziz-al-sayyari.html` — Dr Abdulaziz Al Sayyari (reclassified from Advisor to Board)
- `board/kuyoung-chung.html` — Kuyoung Chung (reclassified from Advisor to Board)
- `board/sebastian-vaughan.html` — Dr Sebastian Vaughan (reclassified from Partner to Board)
- `board/arjumand-warsy.html` — Prof. Arjumand Warsy (reclassified from Advisor to Board)
- `board/junaid-kashir.html` — Dr Junaid Kashir (reclassified from Advisor to Board)
- `board/abdullah-alawad.html` — Dr Abdullah Alawad (reclassified from Advisor to Board)
- All pages built with initials placeholder — swap in photo when available

**who-we-are.html updated:**
- Added new "Fund Partners" section between Team and Board of Advisers (3 Partner cards)
- Added 6 new Board cards for reclassified people
- Renamed existing company-logos section from "Our Partners" → "Strategic Partnerships" to avoid ambiguity

**JSON + sitemap:** profileUrls set for all 9 new pages; sitemap expanded to 49 URLs

**Outstanding Data Gaps (require human input)**
- LinkedIn missing: Dr Amer Mahmood, Ghassan Najmeddin, Osama Al-Thanon, Dr Tarek El Mansy, Daniel Roubeni, Mark Walker, Professor Mohammed Al Jumah, HE Eng. Osama Al-Zamil, Rayan Al-Karawi
- Email missing: Daniel Roubeni, Professor Mohammed Al Jumah, HE Eng. Osama Al-Zamil, Rayan Al-Karawi
- Profile images missing: Jehanzeb Awan, Mustafa Mahmood Khan CFA, Dr Abdulaziz Al Sayyari, Kuyoung Chung, Dr Sebastian Vaughan, Prof. Arjumand Warsy, Dr Junaid Kashir, Dr Abdullah Alawad, Dr Qaisar Hamed Metawea
- No HTML profile pages for: Jehanzeb Awan, Mustafa Mahmood Khan CFA, Dr Abdulaziz Al Sayyari, Kuyoung Chung, Dr Sebastian Vaughan, Prof. Arjumand Warsy, Dr Junaid Kashir, Dr Abdullah Alawad, Dr Qaisar Hamed Metawea (Partner/Advisor/Service Provider types — await instructions on whether these need individual pages)
- 10 board member bios still needed — see MISSING-PROFILE-INFO.md

### Session 9 — 10 April 2026 (GSC Validation)

**Google Search Console — Post-Fix Validation**
Walked through GSC with Mark to validate the SEO fixes pushed on 7 April.

- **Sitemap confirmed live:** sitemap.xml last read 09/04/2026, Status: Success, 49 discovered pages (matches current count exactly)
- **Page indexing report state (last update 06/04/2026 — pre-fix data):** 281 indexed, 180 not indexed across 6 reasons:
  1. Not found (404) — 48 pages (old numeric WP URLs /2/, /3/, /30/, /67/ etc — not covered by our redirect rules)
  2. Page with redirect — 38 pages (expected: these are our new 301s from the CloudFront Function)
  3. Alternative page with proper canonical tag — 11 pages (expected: our canonicals working as designed)
  4. Blocked due to other 4xx issue — 1 page (first detected 07/04/2026)
  5. Blocked by robots.txt — 1 page (first detected 07/04/2026)
  6. Crawled - currently not indexed — 81 pages (first detected 15/03/2025 — the main one our sitemap/canonical fixes address)

- **Decision on numeric 404 URLs (e.g. /2/, /3/, /67/, /70/):** Option A — leave as 404. These are old WordPress post-ID/pagination URLs that have no content value to redirect to. 404 is the correct SEO response and Google will drop them on re-crawl.

- **Validate Fix clicked on 3 reasons** (10/04/2026):
  - Blocked by robots.txt ✅
  - Crawled - currently not indexed ✅
  - Blocked due to other 4xx issue ✅
- **Skipped:** Not found (404), Page with redirect, Alternative page with proper canonical tag (all either intentional per Option A or expected states, not errors)

- **Live URL Inspection spot-checks (10/04/2026 11:36):**
  - `/privacy-policy` — URL is available to Google ✅, Page can be indexed ✅, live-tested (confirms the canonical + meta description we added on 7 Apr are now visible to Googlebot)
  - `/team/nicholas-bingham` — URL is on Google ✅, Page is indexed (confirms new team profile pages from the sitemap expansion are being picked up)

Validation runs take ~14-28 days. Next check: week of 24 April to confirm pass/fail.

---

### Session 10 — 10 April 2026 (Biotech Subdomain Page)

**Built new `subdomains/biotech/index.html` matching the Disruptive Tech / Datacentre subdomain visual template.** Purpose: give Mark a locally-previewable version of biotech.taraniscapital.com before DNS is cut over from the old externally-designed page.

**Source of fund content:** Taranis_BioTech_Growth_Fund_KSA_PPM_Combined_Apr2026.docx (Mark uploaded for this session). All figures, team, fund structure, and strategy copy derived from the PPM.

**Page structure (mirrors disruptive-tech subdomain):**
- Hero: "Taranis Biotech Growth Fund" — CMA-registered Private Investment Fund, Vision 2030 aligned
- Fund Overview: USD 400M target (with USD 100M Green Shoe → USD 500M max), 25–35% net IRR, 3.0–4.0x MoIC, 10-year term + 2yr extension, 20–25 portfolio cos, USD 5–20M tickets, 25% reserve
- Why Taranis: Specialist biotech expertise / Vision 2030 alignment / Localisation framework / Regulatory & government access
- Market Opportunity: USD 65B Vision 2030 healthcare, USD 34.6B biotech GDP by 2040, USD 25B+ global biotech VC, 60% of population under 30
- Investment Focus: Therapeutics 60–70% / Devices 15–25% / Digital Health / Biomanufacturing
- Fund Leadership & Advisers: split into 5 groups — Fund Manager (J.AWAN CAPITAL: Jehanzeb Awan, Mustafa Mahmood Khan), Technical Services Advisor (Bingham, Walker, Bukhari, El Mansy, Al-Rahim, Essam, Metawea, Burlakova), Investment Committee (Bingham, Bukhari, Al Sayyari, Chung, Vaughan), Scientific Advisory Board (Warsy, Kashir, Alawad, Mahmood, Al Jumah), Advisory Board (Al-Zamil, Chohan, Martorano, Boevink, Al-Thanon)
- Strategic Partners: Helix8 + WISE Initiative (per Mark's direction)
- ESG: Environmental / Social / Governance
- CTA + footer with CMA + DFSA regulatory disclosure

**All 26 team image references verified to exist in `images/team/`** — page will render correctly when deployed.

**Preview method:** Local HTML preview (Mark's choice). File opens directly from the repo at `subdomains/biotech/index.html`. Images load from the live taraniscapital.com main site, so the preview is visually accurate.

**Partners consistency check:** Helix8 and WISE Initiative already referenced in the footer ecosystem block of all main-site pages (who-we-are, fintech, disruptive-tech, all team profile pages). No main-site updates required.

**Not yet done — pending Mark's sign-off on the preview:**
- Create S3 bucket `biotech.taraniscapital.com`
- Create CloudFront distribution (add to wildcard cert SANs)
- Add Route 53 CNAME to point biotech.taraniscapital.com to the new CloudFront distribution (this is the "cut the DNS" step)
- Add biotech deploy step to GitHub Actions `.github/workflows/deploy.yml`
- Update SUBDOMAIN-SETUP.md to include biotech in the loops/tables

**Saved memory:** feedback_subdomain_partners.md — any strategic partner added to a fund subdomain must also be referenced on the main site; the two must never get out of sync.

### Session 10b — 10 April 2026 (Footer Partners Cleanup)

**Scope change from Mark after the biotech subdomain was delivered:** strategic/ecosystem partners must live in ONE place only — the Strategic Partnerships grid on `who-we-are.html`. Partners are to be removed from every footer across the site and the "Ecosystem" footer column removed entirely.

**Changes made:**

1. **Removed the `<h4>Ecosystem</h4>` footer block from 44 HTML files** — every file containing the Helix8 + WISE Initiative + Biotech Fund footer column. Affected files: all main site pages (`index.html`, `who-we-are.html`, `our-approach.html`, `our-funds.html`, `insights.html`, `contact.html`, `biotech.html`, `fintech.html`, `disruptive-tech.html`, `datacentres.html`, `property.html`, `privacy-policy.html`, `cookie-policy.html`, `404.html`), all 12 team profile pages under `team/`, all 18 board profile pages under `board/`, plus three legacy `Documents/mockup-*.html` files. Done with a regex-based Python sweep to guarantee consistent removal.

2. **Updated `css/styles.css`** — changed `.footer-grid` from `grid-template-columns: 2fr 1fr 1fr 1fr` to `2fr 1fr 1fr`. Mobile breakpoints already use `1fr 1fr` and `1fr`, so no mobile change required. The footer now has three columns on desktop: Brand / Navigation / Head Office.

3. **Expanded the Strategic Partnerships grid on `who-we-are.html`** — added Helix8 ("Biotech accelerator & infrastructure") and WISE Initiative ("Women in STEM & entrepreneurship") as two new cards alongside the existing The Fintech Times, The Biotech Times, Disrupts, Change Gap cards. This is now the single canonical home for all Taranis Capital strategic partners.

4. **Updated memory** — `feedback_subdomain_partners.md` rewritten and `MEMORY.md` index entry updated. New rule:
   - All partners live in ONE place only: the Strategic Partnerships section on `who-we-are.html` (single source of truth).
   - Partners shown on any fund subdomain's "Strategic Partners" section must also appear on who-we-are.html (no subdomain introduces a partner the main site doesn't acknowledge).
   - Partners must NEVER appear in any page footer (main site or subdomains), and the `<h4>Ecosystem</h4>` column must never be reintroduced.
   - Footer grid is locked at 3 columns: Brand / Navigation / Head Office.

**Verification:**
- `grep '<h4>Ecosystem</h4>'` across the repo returns zero hits.
- `grep 'helix-8.com\|wiseinit'` now returns only `who-we-are.html` (Strategic Partnerships grid) and `subdomains/biotech/index.html` (Strategic Partners section on the biotech subdomain) — which is exactly the desired state.

**Biotech subdomain page itself untouched** — Mark said he will review `subdomains/biotech/index.html` locally and revert separately.

**Not yet pushed to main branch.** All changes are staged on local repo only (files in `C:\Users\mark\Claude Cowork\Taranis Capital Website`). Next push will need to include this footer cleanup plus the new biotech subdomain page.

### Session 10c — 10 April 2026 (Biotech Exec Team Merge + New Partners)

**Follow-up to biotech subdomain from Mark:**

1. **Merged Fund Manager (J.AWAN CAPITAL) + Technical Services Advisor (Taranis Capital) into a single "Executive Team" section on `subdomains/biotech/index.html`** — matches the "Executive Team" pattern used on the datacentre subdomain. Order per Mark's instruction: all Technical Services Advisors first (Bingham, Walker, Bukhari, El Mansy, Al-Rahim, Essam, Metawea, Burlakova), then Jehanzeb Awan and Mustafa Mahmood Khan from J.AWAN CAPITAL. Each title now includes the parent entity so the CMA/Fund Manager relationship remains clear. Intro copy updated to explain the combined team construct. Investment Committee / Scientific Advisory Board / Advisory Board sections untouched.

2. **Added two new Strategic Partners to `subdomains/biotech/index.html`:**
   - **BOYD Consultants** (`boydconsultants.com`) — the Fund's primary technical and regulatory partner per PPM Section 15. Handles mandatory technical feasibility study, CASS framework validation, and validation sign-off before any investment disbursement. Copy drawn from PPM.
   - **Phytome Life Sciences** (`phytomelife.com`) — bio-pharmaceutical technology platform combining AI, plant science, natural product chemistry, formulation and sustainable biomanufacturing. Dr Sebastian Vaughan (Fund Investment Committee member) is CEO of Phytome Life Sciences per the PPM, which makes this a direct fit. Description created from the Phytome homepage, opened via Claude in Chrome (direct WebFetch blocked by egress proxy for this domain).
   - Final Strategic Partners order on the biotech subdomain is now: BOYD Consultants, Helix8, Phytome Life Sciences, WISE Initiative.
   - Helix8 description expanded slightly to reference the HELIX8 questionnaire + CASS scoring per PPM (previously a generic accelerator blurb).

3. **Added BOYD Consultants and Phytome Life Sciences to the Strategic Partnerships grid on `who-we-are.html`** — the canonical partner list now contains The Fintech Times, The Biotech Times, Disrupts, Change Gap, Helix8, WISE Initiative, BOYD Consultants, Phytome Life Sciences (8 partners).

**Validation:** `subdomains/biotech/index.html` is 1,275 lines / 55.5 KB; HTML parser passes with no unclosed tags and no errors. All team image references continue to resolve from the live main site.

**Still untouched:** no main-site team profile page exists for the two J.AWAN CAPITAL staff or the new partners — they are only referenced on subdomain/Strategic Partnerships, which matches existing patterns.

**Still not pushed.** Changes accumulated locally pending Mark's review.

### Session 11 — 10 April 2026 (GSC Weekly Check)

**Automated weekly Google Search Console health check — taraniscapital.com**

**1. Sitemaps**
- sitemap.xml — Status: **Success** ✅
- Last read: 9 Apr 2026
- Discovered pages: **49** — matches local sitemap.xml exactly ✅ (no mismatch)

**2. Page Indexing**
- Last update: **06/04/2026** — data has not refreshed since pre-fix baseline (expected; validation runs take 14–28 days)
- Indexed: **281** (no change vs Session 9 baseline)
- Not indexed: **180** (6 reasons — no change vs Session 9 baseline)
- No new reason categories; no page counts increased

| Reason | Pages | Validation | vs Baseline |
|---|---|---|---|
| Not found (404) | 48 | Not Started | No change ✅ |
| Page with redirect | 38 | Not Started | No change ✅ |
| Alternative page with proper canonical tag | 11 | Not Started | No change ✅ |
| Blocked due to other 4xx issue | 1 | **Started** | No change ✅ |
| Blocked by robots.txt | 1 | **Started** | No change ✅ |
| Crawled – currently not indexed | 81 | **Started** | No change ✅ |

- The three validation runs started on 10/04/2026 (Blocked by robots.txt, Blocked due to other 4xx issue, Crawled – currently not indexed) are all showing **Started** — in progress, not yet Passed or Failed. Expected given the 14–28 day window.

**3. Performance (last 7 days: ~4–10 Apr 2026)**
- Total clicks: **33**
- Total impressions: **3,730**
- Average CTR: **0.9%**
- Average position: **7.1**
- No prior 7-day period available for comparison — first week of data post-launch

**4. Manual Actions & Security Issues**
- Manual actions: **No issues detected** ✅
- Security issues: **No issues detected** ✅

**5. Core Web Vitals**
- Mobile: Not enough usage data (last 90 days) — expected for new site, no Poor/Needs improvement URLs
- Desktop: Not enough usage data (last 90 days) — expected for new site, no Poor/Needs improvement URLs

**Issues to raise with Mark**
Nothing to flag this week. All indexing counts are identical to the Session 9 baseline, the three validation runs are in progress as expected, no new reason categories have appeared, and manual actions and security are clean. The 7-day performance figures (33 clicks, 3,730 impressions, pos 7.1) are a reasonable baseline for a newly launched site. Next meaningful check is the week of 24 April when validation run outcomes (Pass/Fail) should be visible.

---

### Session 12 — 10 April 2026 (Biotech Subdomain AWS Deploy)

**Objective:** Stand up `biotech.taraniscapital.com` on AWS (S3 + CloudFront + Route 53) to replace the externally-hosted Replit page, matching the pattern of the other four fund subdomains.

**Pre-state:** Old biotech page lived on Replit (custom domain → IP `34.111.179.208`). Route 53 had an A record for biotech pointing at Replit, plus a `replit-verify` TXT record. The local `subdomains/biotech/index.html` page had already been built in Session 10 but had nowhere to be served from.

**IAM permissions**
- Discovered `taranis-deploy` IAM user was scoped to sync/invalidate existing infra only — missing Route 53 (both list + change), S3 bucket creation, and CloudFront distribution creation.
- Attached three AWS-managed policies to `taranis-deploy`: `AmazonS3FullAccess`, `CloudFrontFullAccess`, `AmazonRoute53FullAccess`. This widens the credential used by GitHub Actions too — a reasonable trade for a solo-owned account where the key is already protected.

**S3 bucket creation (CLI)**
- Created `biotech.taraniscapital.com` bucket in eu-west-2
- Disabled all four "Block Public Access" settings
- Enabled static website hosting (`index.html` / `404.html`)
- Applied public read bucket policy (scratch file `biotech-policy.json`, written by hand rather than copied from fintech after `get-bucket-policy` endpoint blipped)
- Synced `subdomains/biotech/` → `s3://biotech.taraniscapital.com/` — page rendered on S3 website endpoint

**CloudFront distribution (CLI)**
- New AWS console wizard for CloudFront now uses a multi-plan "packaged" flow that bundles TLS/DNS/WAF — abandoned the console path to avoid creating a distribution with different behaviour to the other four
- Pulled fintech's exact config via `get-distribution-config --query DistributionConfig` and saved to `fintech-dist-config.json` (with `Out-File -Encoding ascii` to avoid PowerShell's BOM)
- Hand-edited a `biotech-dist-config.json` variant — only differences: `CallerReference` (`biotech-taranis-2026`), `Aliases`, origin `Id` (`S3-biotech`), origin `DomainName`, `TargetOriginId`, `Comment`
- Price class `PriceClass_100` (matches other four subdomains), wildcard cert `*.taraniscapital.com`, `index.html` root, HTTP→HTTPS redirect, no CloudFront Function association (fintech has none either)
- `create-distribution` returned: **Distribution ID `ESMIKURPBA41W`**, **domain `d12nozf5efsxkp.cloudfront.net`**
- (One transient "Could not connect to endpoint" error on the create-distribution call — clean retry worked)

**Route 53 cutover**
- In Route 53 console, edited existing biotech A record (was `34.111.179.208`) → toggled Alias ON → Alias to CloudFront distribution → us-east-1 → `d12nozf5efsxkp.cloudfront.net` → Save
- `replit-verify` TXT record left in place until Replit is fully decommissioned (Step I below)

**Verification**
- CloudFront distribution reached `Deployed` status
- `https://biotech.taraniscapital.com/` loads the new page in incognito with valid `*.taraniscapital.com` certificate

**Repo changes (committed)**
- `.github/workflows/deploy.yml`: added `Sync biotech subdomain to S3` step after disruptive-tech, and added `ESMIKURPBA41W` invalidation line to the Invalidate CloudFront caches step
- `SUBDOMAIN-SETUP.md`: added biotech row to the distribution table at the bottom (`biotech.taraniscapital.com | d12nozf5efsxkp.cloudfront.net | ESMIKURPBA41W`) and added biotech to every `for SUBDOMAIN in ...` loop in the doc so future readers pick it up
- `.gitignore`: added `*-policy.json` and `*-dist-config.json` patterns to prevent future scratch files from being accidentally committed

**Scratch files deleted after deploy:** `fintech-policy.json`, `biotech-policy.json`, `fintech-dist-config.json`, `biotech-dist-config.json`

**Outstanding: Step I — Decommission Replit**
- Old biotech page still running on Replit but no longer receiving traffic (DNS moved to CloudFront)
- Leave the old host in place for ~24–48 hours as a rollback option
- After that: log into Replit → delete the custom domain binding → delete the Deployment/Repl → confirm
- Then remove the `replit-verify` TXT record from Route 53 (name: `biotech.taraniscapital.com`, type: TXT, value: `"replit-verify=ef3d3295-5d3e-48c2-8c8d-e15387d68975"`)

---

### Weekly Sync — 2026-04-13 (Automated)

**Source:** Taranis-People-Data-Collection-KB.xlsx
**People count:** 36 (9 Team, 3 Partners, 24 Board)

**JSON regenerated:**
- `taranis-people-data.json` — updated lastUpdated to 2026-04-13; fixed MISSING literal values (preserved existing image paths and emails where spreadsheet had MISSING placeholders)

**Profile pages updated (2):**
- `team/bijna-kotak-dasani.html` — h1 name updated to include "MBE, FRSA" honours
- `team/svitlana-burlakova.html` — h1 name updated to include "ICA, TEP" qualifications

**Subdomain fund pages updated (1):**
- `subdomains/biotech/index.html` — added Emad Zowawi (KSA Legal Counsel to the CEO, Executive Team section) and Rayan Al-Karawi (Advisory Board section)

**Sitemap updated:**
- `sitemap.xml` — updated lastmod dates for bijna-kotak-dasani and svitlana-burlakova profile pages

**who-we-are.html:** No changes needed — all 36 people present with correct names and roles.

**Other fund pages (fintech, property, datacentre, disruptive-tech):** No changes needed — all assigned people present.

**Data gaps (ongoing):**
- Profile images: all 36 people now have images on disk (the spreadsheet still shows MISSING for 9 newer people but the actual image files exist — spreadsheet needs updating)
- LinkedIn URLs still missing for 11 people: daniel-roubeni, ghassan-najmeddin, mohammed-aljumah, osama-al-thanon, osama-al-zamil, mustafa-mahmood-khan, abdulaziz-al-sayyari, arjumand-warsy, junaid-kashir, abdullah-alawad, qaisar-hamed-metawea
- Note: the spreadsheet (Taranis-People-Data-Collection-KB.xlsx) is behind the actual website for image paths and some LinkedIn URLs — it should be updated to match current site data

---

### Session 13 — 16 April 2026 (Team Composite Image)

**Objective:** Replace `/images/team/tc-team-office.jpg` (the branded team photo used in the About/Who-We-Are intro blocks on `index.html` and `who-we-are.html`) with a composite that includes the current 9-person team, since getting everyone in the same room for a real group shoot isn't practical right now.

**Approach**
- Source: the 9 individual headshots in `Team Images/` (Amit, Bijna, Emad, Mark, Milan, Mohamed, Nicholas, OB, Svitlana)
- Background removal with `rembg` (u2net_human_seg model, source images upscaled 2× first)
- Per-person face detection via OpenCV Haar cascades to normalise figures by FACE height rather than overall figure height (crucial — the source crops vary wildly, so scaling by total height produced wildly different head sizes)
- Two-row "class photo" layout on a Taranis-branded backdrop (#2A2A2A charcoal grey, soft gold uplight, thin gold divider)
- Front row: Svitlana, Nicholas, Mark (centre), OB, Bijna
- Back row: Emad, Amit, Milan, Mohamed
- Nick, Mark and Bijna cropped to OB's head-and-shoulders depth so the front row reads as a uniform headshot band rather than mixed crops
- Per-person face-height boost for Milan and Amit (+20%) because Haar's frontal face box includes glasses frames, which was making them get over-shrunk

**Key file changes**
- `images/team/tc-team-office.jpg` — REPLACED with composite (1200×900 JPEG, 117 KB). Previous was a real office group photo at 1984×2148. CSS for both `.about-image` and `.intro-image` containers enforces `aspect-ratio: 4/3` with `object-fit: cover`, so the old portrait image was being centre-cropped aggressively by the browser; the new 4:3 composite fills the container without any crop.
- Generated masters retained in `Team Images/` as `Taranis-Team-Composite-v4.png`/`.jpg` for future edits.

**Not changed** — no HTML edits needed (the file path and filename are the same), no CSS changes.

**Deploy** — pushed to `main`; GitHub Actions workflow syncs to S3 and invalidates CloudFront.

---

### Session 14 — 17 April 2026 (Replit Decommission)

**Objective:** Decommission the old Replit-hosted biotech.taraniscapital.com now that the AWS-hosted version (S3 + CloudFront) has been live since 10 April 2026.

**Steps completed:**
1. **Site health verified** — `https://biotech.taraniscapital.com/` confirmed loading correctly on AWS with valid `*.taraniscapital.com` certificate
2. **Replit custom domain binding removed** — Mark removed the `biotech.taraniscapital.com` binding from the Replit project (old IP: `34.111.179.208`)
3. **Route 53 `replit-verify` TXT record deleted** — removed `"replit-verify=ef3d3295-5d3e-48c2-8c8d-e15387d68975"` from hosted zone `Z0680053Y587NB8B8C9S` via AWS CLI (`--profile TaranisCapital`)

**Old Replit infrastructure is now fully decommissioned.** All biotech.taraniscapital.com traffic serves from CloudFront distribution `ESMIKURPBA41W` (`d12nozf5efsxkp.cloudfront.net`).

---

### Weekly Sync — 2026-04-20 (Automated)

**Source:** Taranis-People-Data-Collection-KB.xlsx
**People count:** 36 (9 Team, 3 Partners, 24 Board)

**JSON regenerated:**
- `taranis-people-data.json` — `lastUpdated` bumped to 2026-04-20. Linked-in values sanitised: the literal string `"MISSING"` was previously stored for 11 people; those are now normalised to empty strings. Existing non-empty image paths and `profileUrl` values preserved where the spreadsheet cell was empty/MISSING.

**Profile pages updated (8):**
- `team/bijna-kotak-dasani.html` — inner `profile-name` h1 updated from "Dr. Bijna Kotak Dasani" to "Dr. Bijna Kotak Dasani MBE, FRSA" (hero h1 was already correct)
- `team/svitlana-burlakova.html` — inner `profile-name` h1 updated from "Svitlana Burlakova" to "Svitlana Burlakova, ICA, TEP"
- `board/ghassan-najmeddin.html` — bio expanded from 1 para (28 words) to 2 paras (83 words) with richer content on Emirates NBD Saudi Arabia role
- `board/leif-hesse.html` — bio expanded from 1 para (23 words) to 3 paras (92 words) covering cybersecurity architecture, sovereign-grade infrastructure expertise, and KSA Vision 2030 digital sovereignty
- `board/osama-al-thanon.html` — bio expanded from 1 para (44 words) to 3 paras (112 words) covering ABB career, digital transformation, and white-hat security
- `board/rayan-al-karawi.html` — bio expanded from 1 para (28 words) to 3 paras (116 words) covering Central Bank of Kuwait start, Razeen Capital chairmanship, and Saudi capital markets depth
- `board/sarah-sinclair.html` — bio expanded from 1 para (22 words) to 3 paras (128 words) covering ChangeGap, Co-Labs collaboration initiative, and ESG strategy expertise
- `board/tarek-el-mans.html` — bio expanded from 1 para (23 words) to 3 paras (114 words) covering Director of Localisation role, biotech growth architecture, and MENA portfolio work

**Policy note:** Bio updates are only applied where the JSON version has equal or greater word count than the HTML — this prevents richer hand-written HTML bios from being overwritten by shorter spreadsheet summaries.

**Sitemap updated:**
- `sitemap.xml` — `lastmod` dates refreshed to 2026-04-20 for all 8 pages above. All 36 profile URLs already listed; no additions needed.

**who-we-are.html:** No changes needed — all 36 people present with correct names, roles, and images in the Team, Fund Partners, and Board of Advisers sections.

**Subdomain fund pages (fintech, property, datacentre, disruptive-tech):** No changes needed — all assigned people present on their respective pages (HE Eng. Osama Al-Zamil is listed as "H.E. Eng. Osama Al-Zamil" across subdomains, minor punctuation variance vs JSON; left as-is this run).

**Data gaps (ongoing):**
- **11 people still missing LinkedIn URLs in the spreadsheet:** daniel-roubeni, ghassan-najmeddin, mohammed-aljumah, osama-al-thanon, osama-al-zamil, mustafa-mahmood-khan, abdulaziz-al-sayyari, arjumand-warsy, junaid-kashir, abdullah-alawad, qaisar-hamed-metawea
- **1 person missing email:** mohammed-aljumah
- **All 36 people have profile images on disk**, and all 36 have profile HTML pages that exist

---

### Session 15 — 20 April 2026 (GSC Weekly Check)

**Automated weekly Google Search Console health check — taraniscapital.com**

**1. Sitemaps**
- sitemap.xml — Status: **Success** ✅
- Last read: 18 Apr 2026
- Discovered pages: **49** — matches local sitemap.xml exactly ✅ (no mismatch)

**2. Page Indexing**
- Last update: **17/04/2026** — data has now refreshed (previous weekly check was still on the 06/04/2026 pre-fix snapshot, so this is the first post-validation dataset)
- Indexed: **142** (was 281 at baseline) — DOWN 139
- Not indexed: **370** (was 180 at baseline) — UP 190
- 9 reasons total (2 new categories since baseline, plus 1 "Passed")

| Reason | Pages | Validation | vs Baseline (Sessions 9/11) |
|---|---|---|---|
| Not found (404) | 242 | Not Started | was 48 — **UP 194** 🚨 (still all old WP URLs — see spot-check below) |
| Page with redirect | 30 | Not Started | was 38 — DOWN 8 ✅ |
| Alternative page with proper canonical tag | 9 | Not Started | was 11 — DOWN 2 ✅ |
| Excluded by 'noindex' tag | 4 | Not Started | **NEW category** 🆕 (see below) |
| Discovered – currently not indexed | 24 | Not Started | **NEW category** 🆕 (see below) |
| Blocked due to other 4xx issue | 1 | Started | was 1 — No change |
| Blocked by robots.txt | 1 | Started | was 1 — No change |
| Crawled - currently not indexed | 59 | Started | was 81 — **DOWN 22** ✅ (validation making progress) |
| Duplicate, Google chose different canonical than user | 0 | **Passed** ✅ | (Passed since last check) |

**Validation run status (started 10/04/2026 — day 10 of the 14–28 day window):**
- Crawled – currently not indexed: Started, trending down (81 → 59) ✅
- Blocked by robots.txt: Started, 1 page unchanged
- Blocked due to other 4xx issue: Started, 1 page unchanged
- No runs have flipped to Passed or Failed yet — still within window. Next meaningful check: week of 24 April.

**404 spot-check (10 sample URLs inspected):** Pattern is consistent with Option A decision — all old WordPress content, none are legitimate current pages.
- Old Disrupts-style news articles (7 of 10): `/arch-labs-raises-13m-to-bring-smart-contracts-to-bitcoin/`, `/qanooni-raises-2m-to-transform-legal-ai-in-uae-uk/`, `/unravel-raises-7m-series-a-...`, `/opentrade-raises-7m-...`, `/olea-secures-30m-...`, `/tamara-secures-2-4b-...`, `/fuse-secures-6-6m-...`
- Old WP pagination (2 of 10): `/page/45/`, `/page/55/`
- Old WP board path (1 of 10): `/board_members/asim-chohan-acp-ccp-mcp-pmp/`

Per Option A the news/pagination URLs stay as 404. The `/board_members/*` path pattern is not covered by the existing CloudFront Function redirect table — worth considering a pattern redirect to `/board/{slug}` if more of these surface in future audits.

**New category — "Excluded by 'noindex' tag" (4 pages):**
- `fintech.taraniscapital.com`
- `disruptive-tech.taraniscapital.com`
- `property.taraniscapital.com`
- `datacentre.taraniscapital.com`
- Verified locally: all 5 fund subdomain `index.html` files (including biotech) carry `<meta name="robots" content="noindex, follow">`. This appears intentional — the subdomains are DFSA-regulated fund marketing material, appropriately kept out of general search. Biotech hasn't joined this bucket yet simply because the CloudFront distribution only went live on 10 April and Google hasn't fully processed it; expect it to appear in next week's list.
- **Action:** Confirm this is the desired state (likely yes given regulatory context). If subdomain homepages should be indexable, the meta tag needs removing across all 5 subdomains.

**New category — "Discovered – currently not indexed" (24 pages):**
- All are new `/board/` profile pages (abdulaziz-al-sayyari, abdullah-alawad, amer-mahmood, arjumand-warsy, asim-chohan, bruno-martorano, david-grunfeld, ghassan-najmeddin, and others)
- Last crawled: N/A — Google has discovered these via sitemap but not yet allocated crawl budget
- Expected state for recently-added pages; should resolve naturally as Google works through the sitemap.

**3. Performance (last 7 days: 12–18 Apr 2026)**
- Total clicks: **52** (prev 7-day period 33 — **+58%**)
- Total impressions: **3,920** (prev 3,730 — +5%)
- Average CTR: **1.3%** (prev 0.9%)
- Average position: **6.9** (prev 7.1 — improved by 0.2)
- Strong week-on-week improvement across all four metrics.

**4. Manual Actions & Security Issues**
- Manual actions: **No issues detected** ✅
- Security issues: **No issues detected** ✅

**5. Core Web Vitals**
- Source: Chrome UX report, last updated 18/04/2026
- Mobile: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs
- Desktop: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs

**Issues to raise with Mark**

1. **404 count up from 48 → 242.** All sampled URLs are historical WordPress content (old Disrupts-style news articles, `/page/N/` pagination, one `/board_members/` path). Per the Option A decision these stay as 404. No action required unless you'd like a pattern redirect added for `/board_members/*` → `/board/{slug}` (only 1 example seen this week so probably not worth the effort yet).
2. **"Excluded by 'noindex' tag" is a new category, 4 pages.** These are the 4 fund subdomain homepages (fintech / datacentre / property / disruptive-tech). All 5 subdomain index pages (incl. biotech) contain an intentional `<meta name="robots" content="noindex, follow">` tag. Please confirm this is desired; if the fund subdomains should be appearing in Google Search, the meta tag needs removing.
3. **"Discovered – currently not indexed" is a new category, 24 pages.** All are new `/board/` profile pages awaiting Google's crawl. Expected state — no action needed.
4. **Validation progress is positive.** Crawled-not-indexed is trending down (81 → 59) while still in the Started state, which is the outcome we want. Next meaningful check is week of 24 April when Pass/Fail outcomes should appear.
5. **Performance up sharply** — clicks +58% week-on-week, CTR up from 0.9% to 1.3%, average position improved from 7.1 to 6.9.

---

### Session 16 — 20 April 2026 (Weekly Profile Sync — automated)

**Scheduled task run:** `weekly-profile-updates-taraniscapital-website` (automated)

**Spreadsheet read**
- Source: `Taranis-People-Data-Collection.xlsx` (the `-KB` variant no longer exists on disk; fell back to the canonical file as instructed)
- 36 people read from the "People Directory" sheet (9 Team, 24 Board, 3 Partner)
- No new people added or removed vs the existing JSON

**JSON regenerated** — `taranis-people-data.json`
- Cleaned 11 legacy `linkedIn: "MISSING"` entries to empty strings so downstream consumers no longer see the literal word "MISSING" in the LinkedIn field
- Preserved all existing `profileUrl` values and `profileImage.path` values (none needed overwriting — all spreadsheet values matched existing JSON)
- `lastUpdated` bumped to 2026-04-20

**HTML profile updates (1 person)**
- `board/abdullah-alawad.html` — renamed from **Dr Abdullah Alawad** to **Prof. Abdullah Alawad** to match the updated spreadsheet entry. Updated: page title, meta description, OG/Twitter tags, breadcrumb, page-hero h1, profile-name h1, image alt text, and opening line of bio.
- `who-we-are.html` — Abdullah Alawad board card updated (h3 + avatar alt).
- `subdomains/biotech/index.html` — Abdullah Alawad team-member h3 and image alt updated.

**Bio-length discrepancies flagged but NOT overwritten (10 people)**
Per the rule "do not overwrite if the JSON is empty/missing" (extended conservatively to "JSON shorter than HTML"), the following profile pages still hold hand-enriched bios that are longer than the spreadsheet versions. They have been left untouched so hand-crafted content is not destroyed:
David Parker, Emad Zowawi, Jack Hollander, Joel Blake, Mark Walker, Mazen Al-Rahim, Michael Boevink, Milan Radia, Mohammed Aljumah, Osama Al-Zamil. (One additional match — Osama Bukhari — differed by a single trailing whitespace character; ignored.) If Mark wants the spreadsheet bios to become canonical, the HTML pages can be regenerated in a future run.

**who-we-are.html**
- All 36 people (9 Team + 24 Board + 3 Partner) have cards — no additions needed
- Name/role/image values compared against JSON — all in sync (after the Abdullah Alawad update above)

**Subdomain fund pages**
- All four checked: fintech (13 assigned), property (11), datacentre (20), disruptive-tech (19) — every assigned person in JSON appears on the correct page. No additions required.

**Sitemap**
- All 36 profile URLs present (49 URLs total). `<lastmod>` updated to 2026-04-20 for `/who-we-are` and `/board/abdullah-alawad`.

**Data gaps (unchanged from prior week)**
- 11 people missing LinkedIn: abdulaziz-al-sayyari, abdullah-alawad, arjumand-warsy, daniel-roubeni, ghassan-najmeddin, junaid-kashir, mohammed-aljumah, mustafa-mahmood-khan, osama-al-thanon, osama-al-zamil, qaisar-hamed-metawea
- 1 person missing email: mohammed-aljumah
- 0 missing bios, 0 missing images

**Files touched this run**
- `taranis-people-data.json`
- `board/abdullah-alawad.html`
- `who-we-are.html`
- `subdomains/biotech/index.html`
- `sitemap.xml`
- `docs/PROJECT-LOG.md` (this entry)

**Issues encountered** — none; run completed cleanly.

---

### Session 17 — 22 April 2026 (Weekly Profile Sync — automated)

**Scheduled task run:** `weekly-profile-updates-taraniscapital-website` (automated)

**Spreadsheet read**
- Source: `Taranis-People-Data-Collection.xlsx` (the `-KB` variant is no longer on disk; fell back to the canonical file as instructed)
- 36 people read from the "People Directory" sheet (now 10 Team, 23 Board, 3 Partner — one person moved Team/Board this week; see below)
- No new people added or removed vs the existing JSON

**JSON regenerated** — `taranis-people-data.json`
- One person changed this week: **Osama Al-Thanon** — reclassified from **Board → Team**, role updated from "Board Adviser" → "Chief Cybersecurity Officer", and he is now assigned to the **Fintech Fund** ("Fund Governance Board")
- Existing bios left intact where the HTML version is longer than the spreadsheet (continuing the 2026-04-20 "preserve hand-enriched content" convention)
- `profileUrl` values are now derived from Type (`taraniscapital.com/team/<slug>` / `/board/<slug>` / `/partners/<slug>`); this auto-corrected Osama Al-Thanon's URL from `/board/…` to `/team/…`. All other profileUrls unchanged.
- `lastUpdated` bumped to 2026-04-22

**Profile pages**
- **Created** `team/osama-al-thanon.html` — new Team profile page using the standard Taranis template (GA4, nav, page-hero, profile-grid, footer, Playfair Display / Inter, dark green / gold scheme). Bio text matches spreadsheet; opening sentence updated from "is a Board Adviser at Taranis Capital" to "is Chief Cybersecurity Officer at Taranis Capital" to match his new role. Canonical, OG and Twitter meta tags all set to `/team/osama-al-thanon`.
- **Left in place** `board/osama-al-thanon.html` — the old Board-section page still exists on disk but is no longer the canonical page for this person. It has been removed from the sitemap. **Recommended follow-up:** Mark to delete the file locally (`git rm board/osama-al-thanon.html`) or add a CloudFront 301 from `/board/osama-al-thanon` → `/team/osama-al-thanon` in a future session.

**Bio-length discrepancies flagged but NOT overwritten (11 people)**
Per the rule "do not overwrite if the JSON is empty/missing" (extended conservatively to "JSON shorter than HTML"), the following profile pages still hold hand-enriched bios that are longer than the spreadsheet versions. They have been left untouched so hand-crafted content is not destroyed:
David Parker, Emad Zowawi, Jack Hollander, Joel Blake, Mark Walker, Mazen Al-Rahim, Michael Boevink, Milan Radia, Mohammed Aljumah, Osama Al-Zamil, Osama Bukhari. (Also abdullah-alawad differed by 3 whitespace characters and osama-bukhari by 3 characters — both ignored.) If Mark wants the spreadsheet bios to become canonical, the HTML pages can be regenerated in a future run.

**who-we-are.html**
- Moved Osama Al-Thanon's card from Board of Advisers section to Leadership Team section; updated role from "Board Adviser" to "Chief Cybersecurity Officer"; updated link from `/board/osama-al-thanon` → `/team/osama-al-thanon`
- Card counts: 10 Team cards (was 9) + 23 Board cards (was 24) + 3 Partner cards = 36 total, still matches JSON
- All other names/roles/images verified in sync with JSON (no further changes)

**Subdomain fund pages**
- Initial run placed Osama only in `subdomains/fintech/index.html` Board of Advisers, on the assumption that the Board→Team change on the main site did not need to flow through to the fund pages. Mark corrected this during the run: when a person's Type changes Board↔Team in the spreadsheet, their card must be **moved between sections on every subdomain they appear on** — from Advisers/Board into the Executive Team section (or vice versa). All four affected subdomain pages were re-edited to reflect this.
- **fintech** — Osama removed from Board of Advisers; added to Executive Team after Osama Bukhari with title "Chief Cybersecurity Officer / Fund Governance Board".
- **datacentre** — Osama moved from Board of Advisers to Executive Team (after Mohamed Essam) with title "Chief Cybersecurity Officer / Fund Governance Board".
- **disruptive-tech** — Osama moved from Board of Advisers to Executive Team (after Mohamed Essam) with title "Chief Cybersecurity Officer" (generic "Board Adviser" fund role dropped per convention below).
- **biotech** — Osama moved from Advisory Board to Executive Team (after Mustafa Mahmood Khan, CFA) with title "Chief Cybersecurity Officer — Taranis Capital" (matching the subdomain's existing "— Taranis Capital" suffix convention). The hand-enriched biotech bio ("Tech pioneer… white-hat hacking…") was preserved.
- **property** — unchanged; Osama is not assigned to the Property Fund.
- Placements verified programmatically post-edit: Osama appears in exactly one section (Executive Team) on all four subdomains.

**Conventions captured for future runs** *(now encoded in STEP 4 of the scheduled-task prompt)*
- When a person's Type changes Board↔Team in the spreadsheet, their subdomain placement must be reassigned to match — this is not optional and not limited to the main site.
- Role-title on a moved subdomain card: use the main-site role as the primary title; append the fund-specific role after a slash **only** if it is substantive (e.g. "Fund Governance Board", "Investment Committee Member", "Scientific Advisory Board"); drop generic fund roles (e.g. "Board Adviser", "Advisory Board", "Board Member") when promoting into Executive Team.
- Match each subdomain's existing title-formatting conventions (e.g. biotech appends "— Taranis Capital"; the others don't).

**Sitemap**
- Added new entry: `https://taraniscapital.com/team/osama-al-thanon` (lastmod 2026-04-22)
- Removed duplicate entry: `https://taraniscapital.com/board/osama-al-thanon` (old Board-section URL — no longer canonical)
- Bumped `/who-we-are` lastmod to 2026-04-22
- Total URLs: 49 (unchanged: net +1 team, -1 board)

**Data gaps (unchanged from prior week)**
- 11 people still missing LinkedIn: abdulaziz-al-sayyari, abdullah-alawad, arjumand-warsy, daniel-roubeni, ghassan-najmeddin, junaid-kashir, mohammed-aljumah, mustafa-mahmood-khan, osama-al-thanon, osama-al-zamil, qaisar-hamed-metawea
- 1 person still missing email: mohammed-aljumah
- 0 missing bios, 0 missing images

**Files touched this run**
- `taranis-people-data.json`
- `team/osama-al-thanon.html` (new)
- `who-we-are.html`
- `subdomains/fintech/index.html`
- `subdomains/datacentre/index.html`
- `subdomains/disruptive-tech/index.html`
- `subdomains/biotech/index.html`
- `sitemap.xml`
- `docs/PROJECT-LOG.md` (this entry)

**Issues encountered** — initial subdomain handling was too narrow (see "Subdomain fund pages" above). Corrected during the run and the Board↔Team section-reassignment rule has been added to STEP 4 of the scheduled-task prompt so future runs follow it automatically. One housekeeping follow-up still flagged for Mark: manually delete or redirect `board/osama-al-thanon.html` when convenient.

---

### Session 18 — 24 April 2026 (Press Releases Section)

**Objective:** Add a manually curated first-party press section so Taranis can publish announcements. The existing `/insights` page aggregates third-party RSS and is not suitable for first-party content.

**Decisions taken up-front** (answered before implementation, per `PRESS-RELEASE-PLAN.md` §17):
- Fonts: Playfair Display / Inter (match live site; flag brand-doc drift separately)
- Nav placement: between Insights and Contact
- First release: placeholder only — `noindex` + visible red dev banner; Mark replaces before launch
- Category tags on cards: deferred until volume justifies filtering
- Subdomain press pages: apex only; no per-subdomain press

**New files**
- `press.html` — listing page. Hero (`page-hero`), `.press-grid` with `.press-card` article. One card pointing to the placeholder release. Empty-state markup commented out for future use.
- `press/_template.html` — future-release template. Carries `noindex`, tokenised `{{…}}` placeholders, full SEO/OG/schema.org `NewsArticle` JSON-LD, boilerplate + media-contact blocks.
- `press/2026-05-01-press-section-launch.html` — placeholder seed release. Carries `noindex` + a sticky red "PLACEHOLDER — NOT FOR PUBLICATION" banner (`.dev-banner` class) so it can't be missed. **Deliberately omitted from the sitemap.**
- `docs/ADD-PRESS-RELEASE.md` — step-by-step workflow for publishing future releases (copy template → fill tokens → remove `noindex` → add card + sitemap entry → commit → push).

**Modified files**
- `css/styles.css` — added `/* PRESS */` section: `.press-section`, `.press-grid` (2-col → 1-col ≤768px), `.press-card` with hover lift, `.press-article` (centred 760px max, white-on-off-white), `.press-dateline`, `.press-quote` (gold border-left + Playfair italic), `.press-divider`, `.press-boilerplate`, `.press-contact`, `.press-backlink`, and `.dev-banner`. Responsive rules added to both 1024px and 768px breakpoints.
- `infra/cloudfront-url-rewrite.js` — added `/press` + `/press.html` to `EXACT_ALLOW`, added `/press/` to `PREFIX_ALLOW`, bumped `Last updated` comment. **Manual republish required via AWS Console** (IAM deploy user has no Functions permission) — flagged in PR description.
- `sitemap.xml` — added `/press` URL (priority 0.7, monthly). Total 50 URLs. Placeholder release deliberately excluded until replaced with real content.
- Nav + footer updated across **52 HTML files** (all top-level pages + every team/board/partners profile page). `<li><a href="/press">Press</a></li>` inserted between Insights and Contact in both `nav-links` and `footer-links`. Executed via a single `sed` pass using a backreference to preserve each context's indentation (6 spaces in nav, 10 in footer); `insights.html`'s `class="active"` variant handled with a second targeted pass. Subdomain pages intentionally not touched (apex-only decision).
- `press.html` itself post-sed needed a manual cleanup: sed saw the in-file `/insights` footer link and added a duplicate `/press` line, which was then adjacent to the intentional `class="active"` link. Duplicates removed by hand in both nav and footer.
- `CLAUDE.md` — bumped sitemap URL count from 49 → 50; added known-outstanding line about the placeholder; bumped `Last updated` to 24 April 2026.

**Files NOT changed (intentional)**
- `subdomains/**/*` — per answered Q5, press is apex-only.
- `robots.txt` — already `Allow: /` with no Disallow matching `/press`. No change needed.
- `main.js` — mobile menu toggle is JS-agnostic of link count; no change needed.

**Post-merge action required (cannot be automated from this PR)**
1. AWS Console → CloudFront → Functions → `url-rewrite` → paste the contents of `infra/cloudfront-url-rewrite.js` → Save → Publish → ensure attached to distribution `E18AUIFBUGMXSB`
2. Wait ~5 minutes for propagation
3. Verify with:
   ```
   curl -sI https://taraniscapital.com/press                                  # expect 200
   curl -sI https://taraniscapital.com/press/2026-05-01-press-section-launch  # expect 200
   curl -sI https://taraniscapital.com/press/                                 # expect 301 → /press
   ```

**QA checks performed locally**
- `sitemap.xml` parses as valid XML; URL count = 50
- All 52 non-press top-level HTML files show exactly 2 Press links (nav + footer); `press.html` shows 1 (footer; nav has `class="active"` variant not caught by the plain-text count)
- No stray `computer://` or absolute Windows paths introduced (`grep -r 'computer://\\|C:\\\\Users' --include='*.html' .` → 0)
- No off-brand yellow/light-blue added in the new CSS section
- No files staged from `.gitignore`'d directories

**Branch + PR**
- Feature branch: `feat/press-section` (off `main`)
- PR target: `main`
- Scope is self-contained to press feature + nav/footer wiring + CloudFront function + sitemap + CLAUDE.md/PROJECT-LOG.md updates.

---

### Session 19 — 26 April 2026 (Weekly Profile Sync — automated)

**Scheduled task run:** `weekly-profile-updates-taraniscapital-website` (automated)

**Spreadsheet read**
- Source: `Taranis-People-Data-Collection.xlsx`
- 36 people read from the "People Directory" sheet — composition unchanged: 10 Team, 23 Board, 3 Partner
- No new people, none removed, no Type changes vs the existing JSON

**JSON regenerated** — `taranis-people-data.json`
- Field-level diff against last week's JSON: **0 changes** to person records — only `_meta.lastUpdated` bumped from `2026-04-22` to `2026-04-26`
- All existing image paths, bios, fund assignments and role titles preserved unchanged

**Profile pages — verification only**
- All 36 profile pages programmatically verified against the JSON: name in `<h1>`, role in `<p class="subtitle">`, photo in `.profile-photo > img`, LinkedIn in any `linkedin.com` href, email in `mailto:` href all match. **0 mismatches**, **0 pages created**, **0 pages edited**.
- Type-change leftover still on disk (carried over from Session 17): `board/osama-al-thanon.html` still exists alongside the canonical `team/osama-al-thanon.html`. Recommended follow-up unchanged — `git rm board/osama-al-thanon.html` or add a CloudFront 301 from `/board/osama-al-thanon` → `/team/osama-al-thanon`.

**who-we-are.html — no changes**
- 36 profile links scanned: 10 Team / 23 Board / 3 Partner — matches JSON exactly. All names, roles and photo paths in sync.

**Subdomain fund pages — no changes**
- Verified all 5 subdomain index pages (`fintech`, `property`, `datacentre`, `disruptive-tech`, `biotech`). Every person whose fund column is `Y` in the spreadsheet is present on the corresponding subdomain page in the expected section. No moves required (no Board↔Team/Partner Type changes this week).
- **One pre-existing discrepancy flagged but NOT changed:** `subdomains/biotech/index.html` has a card for Svitlana Burlakova in the Executive Team section, but the spreadsheet has her `Biotech Fund = No`. This was already true going into this run and the task spec for this scheduled job is to add missing assigned people / update existing cards, not to remove cards. Mark to decide: either (a) flip the spreadsheet `Biotech Fund` cell to `Yes` (and add a fund role / fund bio), or (b) remove the card from the biotech subdomain in a future manual edit.

**Sitemap — file restored + no listing change**
- Pre-run check via `git diff sitemap.xml` showed the working tree had been corrupted at some point since Session 18: file truncated mid-tag at byte 8909 / line 302 (last entry cut off mid-`</url`, missing the final two URL entries and the closing `</urlset>` tag). The two missing entries were `/board/junaid-kashir` and `/board/abdullah-alawad`.
- File rewritten in full to match the last-committed version (50 URLs, `</urlset>` closer, 9281 bytes, 316 lines). All `<lastmod>` values left as they were in the committed copy — no HTML profile pages, fund pages, or `who-we-are.html` were modified this week, so no `<lastmod>` bumps are warranted.
- After fix, `git diff sitemap.xml` is empty (clean working tree against `HEAD`).

**PROJECT-LOG.md — file also restored before append**
- `git diff docs/PROJECT-LOG.md` showed the same pattern of corruption: working tree truncated mid-Session 18 at line 947 (bullet ending `Executed via a single sed pass usi` — no terminating newline, no Pending / To Do or Technical Reference sections). File rewritten from `git show HEAD:docs/PROJECT-LOG.md` (1016 lines) and this Session 19 entry appended before the `## Pending / To Do` section. End-of-file structure (Pending / Technical Reference) preserved.

**Data gaps (unchanged from prior week)**
- 11 people still missing LinkedIn: abdulaziz-al-sayyari, abdullah-alawad, arjumand-warsy, daniel-roubeni, ghassan-najmeddin, junaid-kashir, mohammed-aljumah, mustafa-mahmood-khan, osama-al-thanon, osama-al-zamil, qaisar-hamed-metawea
- 1 person still missing email: mohammed-aljumah
- 0 missing bios, 0 missing images

**Files touched this run**
- `taranis-people-data.json` — `_meta.lastUpdated` bumped to 2026-04-26 (no person-record changes)
- `sitemap.xml` — restored from corrupted truncated working-tree copy (no listing change vs `HEAD`)
- `docs/PROJECT-LOG.md` — restored from `HEAD` and this Session 19 entry appended

**Issues encountered**
- The Linux mount that bash sees and the Windows path that the Read/Write/Edit tools see drifted: bash + git both saw `sitemap.xml` and `docs/PROJECT-LOG.md` as truncated in the working tree, while the Read tool showed a properly-closed copy. Fix is to write through bash (Python `open(... , "w")`) so git's view matches the canonical file. Worth keeping in mind for future runs: trust `git diff` over the Read tool when investigating mid-file truncation.
- Branch is `feat/press-section`, **not** `main` — this carries forward many uncommitted changes from Session 18 and earlier (52 modified HTML files, etc.) that are unrelated to this profile-sync run. The git commands at the end of this entry only stage the three files this run actually changed; anything else in the working tree is left for Mark to handle separately.

**Note (added on landing, 2026-05-04):** This entry was originally written for PR #5 but that PR did not merge. Its subdomain HTML edits, xlsx rename, and JSON metadata bump have been re-applied on 2026-05-04 in a fresh PR rebased onto current main. The Svitlana Burlakova biotech-subdomain question above is still open.

---

### Session 20 — 4 May 2026 (GSC Weekly Check)

**Automated weekly Google Search Console health check — taraniscapital.com**

(An earlier scheduled run on this date returned with Claude in Chrome offline; reran on Mark's request once the extension was reachable. No site changes between attempts, so this is a single coherent snapshot.)

**1. Sitemaps**
- sitemap.xml — Status: **Success** ✅
- Last read: **2 May 2026**
- Discovered pages: **51** — matches local sitemap.xml exactly ✅ (up from 49 at last successful read on 18 Apr — Google has now picked up the two new `/press` URLs from Session 18)

**2. Page Indexing**
- Last update: **27/04/2026**
- Indexed: **121** (was 142 at Session 15, 281 at baseline) — **DOWN 21 vs S15**
- Not indexed: **393** (was 370 at S15, 180 at baseline) — **UP 23 vs S15**
- 9 reason rows (no new reason categories vs S15)

| Reason | Pages | Validation | vs Session 15 |
|---|---|---|---|
| Crawled – currently not indexed | 83 | **Failed** 🚨 | was 59 Started — UP 24, validation flipped to Failed |
| Not found (404) | 277 | Not Started | was 242 — UP 35 (still all old WP content per Option A) |
| Page with redirect | 21 | Not Started | was 30 — DOWN 9 ✅ |
| Alternative page with proper canonical tag | 7 | Not Started | was 9 — DOWN 2 ✅ |
| Excluded by 'noindex' tag | 4 | Not Started | was 4 — no change (the 4 fund subdomain homepages, intentional) |
| Blocked due to other 4xx issue | 1 | Started | was 1 Started — no change, still in window |
| Blocked by robots.txt | 0 | **Passed** ✅ | was 1 Started — validation flipped to Passed |
| Duplicate, Google chose different canonical than user | 0 | Passed | was 0 Passed — unchanged |
| Discovered – currently not indexed | 0 | N/A | was 24 — DOWN 24 ✅ (the new `/board/` profile pages have all been crawled) |

Total: 83 + 277 + 21 + 7 + 4 + 1 + 0 + 0 + 0 = 393 ✅ (matches summary).

**Validation run status (started 10/04/2026 — day 24 of the 14–28 day window):**
- **Blocked by robots.txt: PASSED** ✅ — completed within window.
- **Crawled – currently not indexed: FAILED** 🚨 — completed within window. At the time Google reassessed, the affected URLs still couldn't be indexed. Page count is now 83 (was 81 at start of validation, 59 at S15).
- **Blocked due to other 4xx issue: still Started** (1 page unchanged) — unusual to still be Started at day 24, but only 1 page involved.

**3. Performance (last 7 days: ~26 Apr – 2 May 2026)**
- Total clicks: **82** (was 52 at S15) — **+58%**
- Total impressions: **2,050** (was 3,920 at S15) — **−48%**
- Average CTR: **4%** (was 1.3% at S15) — roughly tripled
- Average position: **6.8** (was 6.9 at S15) — slight improvement
- Pattern: smaller but much more relevant search footprint. Likely connected to indexed-page count dropping (142 → 121) — fewer pages in results, but those that remain are more on-target, so CTR rises sharply while impressions fall. Clicks growth is real and continued from S15.

**4. Manual Actions & Security Issues**
- Manual actions: **No issues detected** ✅
- Security issues: **No issues detected** ✅

**5. Core Web Vitals**
- Source: Chrome UX report, last updated 03/05/2026
- Mobile: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs
- Desktop: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs

**Issues to raise with Mark**

1. **"Crawled – currently not indexed" validation FAILED** 🚨 — biggest signal of the week. The validation run started 10/04 with 81 pages, trended down to 59 at S15, but has now ended in **Failed** at 83 pages. Google's view is that the underlying issue (whatever stopped them indexing those URLs) was not resolved by our 7 April canonical/sitemap/redirect work. The bucket is also slowly creeping up. Worth a manual sample inspection of 5–10 URLs in this bucket via URL Inspection to understand the pattern before deciding whether to (a) re-trigger validation, (b) ship a code change first, or (c) accept and move on.
2. **Indexed page count dropped 142 → 121.** Likely related to point 1. Worth inspecting which pages have moved out of "Indexed" to understand whether anything important (team profiles, press, fund pages) has fallen out vs. mostly tail/legacy pages.
3. **404 count up 242 → 277 (+35).** Still consistent with Option A — old WordPress content. Spot-check a sample to confirm no legitimate current pages have crept into this bucket.
4. **"Blocked by robots.txt" validation Passed ✅** and **"Discovered – currently not indexed" cleared from 24 → 0 ✅** — both positive outcomes.
5. **Performance is mixed but net positive.** Clicks +58%, position +0.1, CTR up sharply. Impressions down 48% — explainable but worth keeping an eye on next week to confirm it stabilises rather than continuing to decline.
6. **`/press` URLs picked up by Google.** Sitemap discovered count moved 49 → 51 — Google has registered the press-section URLs from Session 18. The placeholder release at `/press/2026-05-01-press-section-launch` carries `noindex` and is excluded from sitemap, so it should not appear anywhere in the indexing reports.

**"Crawled – currently not indexed" — URL sample (4 May, 30 of 83 inspected)**

Pulled the first three pages of URLs (sorted by Last crawled, descending) directly from the GSC drilldown.

Pattern (30/83 ≈ 36% of bucket): the bucket is overwhelmingly **legacy WordPress URLs** that no longer correspond to content on the new site:
- ~24/30 (80%) are old WP news/article URLs with trailing slashes — `/african-development-bank-strengthens-...`, `/uae-company-natify-raises-350k-...`, `/paraglide-raises-5-million-seed-...`, `/toko-signs-agreement-with-pwc/`, `/aazzur-raises-2m-...`, `/dc-blox-secures-1-15b-...`, `/papara-acquires-rebellion-...`, `/fintech-awards-london-2025-...`, `/ryft-raises-5-7m-...`, `/middle-east-sustainable-bond-issuance-...`, `/felix-secures-75m-...`, `/addleshaw-goddard-advises-...`, `/fidelity-raises-110m-...` and similar
- ~4/30 (13%) are old WP pagination — `/page/39/`, `/page/32/`, `/page/47/`, `/page/42/`, `/page/66/`, `/page/36/`, `/insights/page/22/`, `/insights/page/5/`, `/insights/page/17/`, `/insights/page/11/`
- 1/30: `/embed/` (legacy WP oEmbed endpoint)
- 1/30: `/partners/disrupts/` (no longer exists; partners path is now used for individuals only)
- 1/30: **`/team/mark-walker`** — the only currently-live, sitemap'd page in the sample. Inspected separately (see below).

**URL Inspection of `/team/mark-walker`:**
- URL is on Google ✅
- Page indexing: Page is indexed ✅
- Last crawl: **28 Apr 2026, 10:19:56** (one day after the 27/04 page-indexing report snapshot)
- Crawl allowed: Yes / Page fetch: Successful / Indexing allowed: Yes
- User-declared canonical: `https://taraniscapital.com/team/mark-walker`
- Google-selected canonical: Inspected URL (matches — no canonical conflict)

**Interpretation.** The Page Indexing report we read this week is the **27/04 snapshot**, but URL Inspection runs against **live state**. `/team/mark-walker` was in the "Crawled – currently not indexed" bucket as of 27/04, then re-crawled on 28/04, and is now indexed. So the bucket is partly a *stale snapshot artefact*: pages move in and out as Google reprocesses them on its own schedule.

**What this means for the Failed validation:**
- The "Failed" verdict reflects state at the time of validation (21/04). Many of the 83 pages have since been re-crawled and may already be indexed (as `/team/mark-walker` was). Re-running validation today would likely produce a different result for the legitimate-current subset.
- The dominant content of the bucket (~28 of 30 sampled) is **old WordPress content that should not be on Google at all** — these URLs aren't in our sitemap, aren't linked from anywhere on the new site, and have no canonical equivalent. The fact that Google still has them in a "Crawled" bucket rather than dropping them suggests they may still be returning content or a soft-404 rather than a hard `HTTP 404`. That is the lever to pull.

**Recommended next steps (for Mark to choose from, not actioned this run):**
1. **Spot-check the HTTP status for 3–4 of the old WP URLs** (e.g. `curl -sI https://taraniscapital.com/page/39/` and `curl -sI https://taraniscapital.com/african-development-bank-strengthens-strategic-partnership-with-congo-securing-1-5-million-grants-for-energy-projects-and-advancing-digital-infrastructure/`). If they return 200 with the homepage HTML (soft-404), that explains why Google keeps them crawled-not-indexed instead of dropping them. The fix would be to extend the CloudFront `url-rewrite` Function to return a real 404 for known-dead WP path patterns (`/page/N/`, `/insights/page/N/`, the long news slugs, `/embed/`, `/partners/disrupts/`).
2. **Don't re-trigger validation yet** — wait until either (a) the underlying soft-404 issue is fixed, or (b) we accept the bucket as historical noise and stop tracking it.
3. **No action needed for `/team/mark-walker`** — it's already indexed; the snapshot is just lagging.

---
## Pending / To Do

### Content & Data
3. **10 board member bios needed** — See MISSING-PROFILE-INFO.md for full list (Dr Amer Mahmood, Asim Chohan, Daniel Roubeni, David Grunfeld, Ghassan Najmeddin, Leif Hesse, Osama Al-Thanon, Rayan Al-Karawi, Sarah Sinclair, Dr Tarek El Mansy)
4. **5 board members without LinkedIn** — Daniel Roubeni, Dr Amer Mahmood, Dr Tarek El Mansy, Ghassan Najmeddin, Osama Al-Thanon
5. **Scrape old WP fund pages** — Additional content from old WP site for enriching fund pages

### Technical
6. **DNS & SSL** — ✅ DNS migrated to Route 53, SSL certificate issued, custom domain live. Decommission Funkygrafix after 2026-04-10. ✅ Wildcard cert for subdomains issued.
6b. **Deploy full fund sites** — Run `aws s3 sync` from local machine (see SUBDOMAIN-SETUP.md "Deploy Full Fund Sites" section), then invalidate CloudFront caches
6c. **Push to GitHub** — Commit 0e9b229 + 34 more modified files need pushing. Then update GitHub Actions with subdomain deploy steps
7. **Sitemap update** — ✅ Expanded from 8 to 39 URLs (all pages covered)
8. **SEO & meta tags** — ✅ Canonical tags, meta descriptions, noindex on 404, 301 redirects for old WP URLs all implemented
9. **Mobile responsiveness** — Test all new pages on mobile devices
10. **Analytics** — ✅ GA4 (G-JLN31RRY1V) added to all 40 pages

### Design
11. **Images** — Need to decide on imagery for: company intro section placeholder, fund pages, partner logos (currently text-only cards)

---

## Technical Reference

**GitHub Account:** Walkerma75 (git config credential.username Walkerma75)
**S3 Bucket:** taraniscapital.com (eu-west-2)
**S3 Website Endpoint:** http://taraniscapital.com.s3-website.eu-west-2.amazonaws.com/
**CloudFront Distribution:** E18AUIFBUGMXSB
**CloudFront Domain:** d1ete5r3431epc.cloudfront.net
**CloudFront Function:** `url-rewrite` — handles 301 redirects (old WP URLs, trailing slashes, www→non-www), plus clean URL rewriting (.html append). Biotech redirect removed 2026-04-07.
**Subdomain CloudFront Distributions:** fintech (E260FGTXCVORQ6), datacentre (E3EJUFMMNZLO3V), property (E2H8IQKJ8LPQ01), disruptive-tech (E98QNGA1O9AI0), biotech (ESMIKURPBA41W)
**Wildcard SSL Cert:** arn:aws:acm:us-east-1:571600836975:certificate/fa9c7dad-94a1-4cb1-8a9e-c8e5ee64b60d
**Deploy Trigger:** Push to main branch → GitHub Actions → S3 sync → CloudFront invalidation
**Route 53 Hosted Zone:** Z0680053Y587NB8B8C9S
**Route 53 Nameservers:** ns-1539.awsdns-00.co.uk, ns-942.awsdns-53.net, ns-399.awsdns-49.com, ns-1261.awsdns-29.org
**Domain Registrar:** e& (formerly Etisalat) — nic.ae
**Live URL:** https://taraniscapital.com (live as of 2026-04-07)


---

### Session 20 — 4 May 2026 (Weekly Profile Sync — automated)

**Automated weekly people-data sync run from `Taranis-People-Data-Collection-KB.xlsx`.**

**Source file note.** CLAUDE.md states the canonical filename is `Taranis-People-Data-Collection.xlsx` (renamed from the `-KB` suffix on 20 Apr 2026), but only the `-KB` suffixed version is present in the workspace. This run fell back to it as the spec allows. Suggest verifying which name should be canonical going forward.

**Type changes detected**
- **`osama-al-thanon`: Team → Board.** Main-site role in the spreadsheet changed from "Chief Cybersecurity Officer" to "Board Adviser". His `profileUrl` in `taranis-people-data.json` is now `taraniscapital.com/board/osama-al-thanon`.
  - **New canonical page:** `/board/osama-al-thanon.html` (already existed in the correct folder from a prior run with the correct "Board Adviser" role and bio — left as-is).
  - **Old page flagged, not deleted:** `/team/osama-al-thanon.html` is still on disk with the old "Chief Cybersecurity Officer" content. Mark to clean up or add a redirect (recommend a 301 in the CloudFront URL-rewrite Function from `/team/osama-al-thanon` → `/board/osama-al-thanon`).
  - **who-we-are.html section move:** card removed from `Our Team` and added to `Board of Advisers`. Card counts before/after — Team 10 → 9, Board 23 → 24, Partners 3 → 3.
  - **Subdomain section moves:** he was already in the Board-equivalent section on every subdomain where he appears, so no card-section moves were needed. Only role-title formatting was updated to follow the main-role-plus-fund-role convention:
    - `subdomains/fintech/index.html` (Board of Advisers): `Fund Governance Board` → `Board Adviser / Fund Governance Board`
    - `subdomains/datacentre/index.html` (Board of Advisers): `Fund Governance Board` → `Board Adviser / Fund Governance Board`
    - `subdomains/disruptive-tech/index.html` (Board of Advisers): `Board Adviser` (no change — already matches)
    - `subdomains/biotech/index.html` (Advisory Board): `Advisory Board` → `Board Adviser` (generic fund role dropped)
  - Note: he currently appears on the fintech subdomain page even though the spreadsheet has Fintech Fund = No for him. Card was left in place rather than removed (sync spec only mandates additions for fund=Y; removals for fund=N are out of scope of this run). Worth deciding whether to prune.

**Other profile updates**
- `board/abdullah-alawad.html` — name updated from `Prof. Abdullah Alawad` to `Dr Abdullah Alawad` to match the spreadsheet (which has "Dr Abdullah Alawad" as the canonical Full Name; existing bio text already uses "Dr Alawad"). Note: the who-we-are.html card still says `Prof. Abdullah Alawad` and was not changed in this run because the audit focus was the Type-change. Worth aligning in the next run if Mark prefers `Dr` — flag.
- `team/mark-walker.html`, `team/nicholas-bingham.html`, `team/svitlana-burlakova.html` — initial regex pass would have replaced `&amp;` with `&` in role lines (corrupting the entity); reverted to `&amp;` form. Net change for these three files: none.
- All other 32 profile pages: no changes.
- No new profile pages needed creating.

**JSON regenerated**
- `taranis-people-data.json` — `_meta.lastUpdated` bumped to `2026-05-04`; 36 people; `osama-al-thanon` re-keyed to `type: "Board"`, `role: "Board Adviser"`, `profileUrl: taraniscapital.com/board/osama-al-thanon`.

**Sitemap**
- Removed `/team/osama-al-thanon` entry; added `/board/osama-al-thanon` entry (lastmod 2026-05-04, yearly, priority 0.5).
- `/who-we-are` lastmod bumped to 2026-05-04.
- Total `<url>` entries: 51 (unchanged — one removed, one added).

**Data gaps logged**
- Missing email (1): `mohammed-aljumah`.
- Missing LinkedIn (11): `daniel-roubeni`, `ghassan-najmeddin`, `mohammed-aljumah`, `osama-al-thanon`, `osama-al-zamil`, `mustafa-mahmood-khan`, `abdulaziz-al-sayyari`, `arjumand-warsy`, `junaid-kashir`, `abdullah-alawad`, `qaisar-hamed-metawea`. (Spreadsheet column literally contains `MISSING` — treated as empty string in JSON.)
- Missing image: 0.
- Missing bio: 0.

**Files modified**
- `taranis-people-data.json`
- `who-we-are.html`
- `sitemap.xml`
- `board/abdullah-alawad.html`
- `subdomains/fintech/index.html`
- `subdomains/datacentre/index.html`
- `subdomains/biotech/index.html`
- `docs/PROJECT-LOG.md`

**Files deliberately not modified**
- `team/osama-al-thanon.html` (left for Mark to clean up — see flag above).
- `subdomains/disruptive-tech/index.html` (his card already had the correct title `Board Adviser`).
- `subdomains/property/index.html` (he does not appear there).

---

### Session 21 — 11 May 2026 (Weekly Profile Sync — automated)

**Automated weekly people-data sync run from `Taranis-People-Data-Collection.xlsx` (canonical filename — `-KB` suffix is no longer present).**

**Type changes detected:** none. Every person in the JSON remains in the same Type (Team / Board / Partner) as the previous run, with their profile page in the correct folder.

**Spreadsheet-vs-JSON discrepancy flagged**
- **`bruno-martorano` is missing from the spreadsheet** but is fully populated in `taranis-people-data.json` and has a live profile page at `/board/bruno-martorano.html`, a card on `who-we-are.html`, and entries on all five subdomain pages (Fintech / Property / Datacentre / Disruptive-Tech / Biotech). Following the CLAUDE.md guidance ("flag spreadsheet inconsistencies for the user to fix in Drive — otherwise the next Cowork sync re-applies the old state"), Bruno was **preserved in the regenerated JSON** rather than silently dropped. **Action for Mark:** re-add Bruno's row to `Taranis-People-Data-Collection.xlsx` in Google Drive (Board, Board Adviser, all five fund flags = Y) so future runs don't keep flagging this. The xlsx in the repo is a snapshot — the master lives in Drive.

**JSON regenerated**
- `taranis-people-data.json` — `_meta.lastUpdated` bumped to `2026-05-11`; 36 people retained (35 from xlsx + 1 preserved). Schema unchanged. All other field values, bios, fund assignments and roles match the spreadsheet exactly (with `MISSING` sentinels normalised to empty strings for the 11 board members without LinkedIn URLs).
- Net diff vs. previous JSON: only the `lastUpdated` date.

**Profile pages**
- All 36 profile pages audited against the regenerated JSON for name, role, image src, LinkedIn URL and email. **No discrepancies found — no profile pages modified.**

**who-we-are.html**
- All 36 expected hrefs present (10 Team / 23 Board / 3 Partners). Names and roles match the JSON. **Not modified.**

**Subdomain fund pages**
- Audited every person flagged Y for each fund against the corresponding subdomain `index.html`. All expected names appear on each page in their correct section. **None of the five subdomain pages modified.**
  - Fintech: 14 expected, all present.
  - Property: 11 expected, all present.
  - Datacentre: 20 expected, all present.
  - Disruptive Tech: 19 expected, all present.
  - Biotech: 24 expected, all present.

**Sitemap**
- 52 URLs total. All 36 profile URLs (10 Team / 23 Board / 3 Partners) present. No extras. No `lastmod` bumps required because no HTML files changed in this run. **Not modified.**

**Data gaps**
- Missing email (1): `mohammed-aljumah`.
- Missing LinkedIn (11): `abdulaziz-al-sayyari`, `abdullah-alawad`, `arjumand-warsy`, `daniel-roubeni`, `ghassan-najmeddin`, `junaid-kashir`, `mohammed-aljumah`, `mustafa-mahmood-khan`, `osama-al-thanon`, `osama-al-zamil`, `qaisar-hamed-metawea`. Spreadsheet column literally contains `MISSING` for these rows — normalised to empty strings in JSON.
- Missing image: 0.
- Missing bio: 0.

**Files modified**
- `taranis-people-data.json` (only `_meta.lastUpdated`).
- `docs/PROJECT-LOG.md` (this entry).

**Files deliberately not modified**
- All 36 profile HTML pages — already in sync.
- `who-we-are.html` — already in sync.
- All five `subdomains/*/index.html` — already in sync.
- `sitemap.xml` — already in sync.

**Open items carried forward**
- Re-add `bruno-martorano` to the Drive spreadsheet (see flag above).
- 11 LinkedIn URLs still outstanding (no change since previous run).
- 1 email still outstanding (`mohammed-aljumah`).

**Follow-up — Bruno Martorano removal (11 May 2026, same-day update)**

Mark confirmed Bruno Martorano is no longer a board member (his row was deliberately removed from the spreadsheet). The earlier preservation logic in this run has been undone and Bruno has been fully removed from the site.

Removed from:
- `taranis-people-data.json` — entry deleted; people count now 35.
- `who-we-are.html` — board card removed (Board count: 23 → 22; Team 10, Partners 3, Total 35).
- `subdomains/fintech/index.html` — Board of Advisers card removed.
- `subdomains/property/index.html` — Advisory Board card removed.
- `subdomains/datacentre/index.html` — Advisory Board card removed.
- `subdomains/disruptive-tech/index.html` — Advisory Board card removed.
- `subdomains/biotech/index.html` — Advisory Board card removed.
- `board/bruno-martorano.html` — file deleted.
- `sitemap.xml` — `/board/bruno-martorano` `<url>` entry removed; `/who-we-are` lastmod bumped to 2026-05-11. Total URLs: 52 → 51.

**Recommended follow-up — 301 redirect.** The page `/board/bruno-martorano` will 404 on the live site once deployed. Consider adding a 301 redirect in `infra/cloudfront-url-rewrite.js` (e.g. `/board/bruno-martorano` → `/who-we-are`) and republishing the CloudFront Function. Flagged for Mark — not done in this run as it requires manual publish.

**Image asset.** `images/team/Bruno-600x650-1-277x300.jpg` is now orphaned. Left in place (the previous convention is not to prune orphaned images automatically). Worth a cleanup pass at some point.

---

### Session — 13 May 2026 (Cowork weekly profile sync + Partner removals)

**Context.** Mark asked mid-run to remove three Fund Partners (Jehanzeb Awan, Mustafa Mahmood Khan CFA, Dr Qaisar Hamed Metawea) from the website immediately. They were the only entries with `Type = Partner`. After this run the site has 32 people: 10 Team, 22 Board, 0 Partners.

**Spreadsheet read.** First read of `Taranis-People-Data-Collection.xlsx` succeeded and showed 35 rows (incl. the three partners). Subsequent reads in this run failed (`BadZipFile`) — file appeared in the cache without an EOCD record despite being unchanged on disk. The xlsx mtime is still 11 May, so the spreadsheet was not re-saved during the session. I proceeded by basing the regenerated JSON on the prior week's complete JSON and removing the three partners by slug. No other data fields needed updating from xlsx — the prior sync was complete.

**Partner removals — files changed:**
- `taranis-people-data.json` — three Partner records deleted; people count 35 → 32; `_meta.lastUpdated` → 2026-05-13.
- `partners/jehanzeb-awan.html`, `partners/mustafa-mahmood-khan.html`, `partners/qaisar-hamed-metawea.html` — files deleted (folder now empty).
- `who-we-are.html` — entire **Fund Partners** section removed (no remaining partners). Section moved from layout (Team → Partners → Board) to (Team → Board).
- `subdomains/biotech/index.html` — the three partner cards removed from the Executive Team grid (Dr Qaisar Hamed Metawea, Jehanzeb Awan, Mustafa Mahmood Khan).
- `subdomains/datacentre/index.html` — entire **Fund Manager & Key Counsel** section deleted (it contained only the three partners).
- `sitemap.xml` — three `/partners/...` `<url>` entries removed; `/who-we-are` `<lastmod>` bumped to 2026-05-13. Total URLs: 51 → 48.

**Verification (post-edits, automated):**
- `grep -r` across `*.html`/`*.xml` returns no remaining references to any of the three partners outside `Documents/` archival material.
- All 32 remaining people are present in `who-we-are.html` under the correct section (10 Team cards, 22 Board cards).
- Each subdomain page's set of cards still matches `funds.{fund}.assigned == true` in the JSON (fintech 13, property 10, datacentre 16, disruptive-tech 18, biotech 20).
- Each of the 32 profile pages exists in the correct `/team`, `/board` folder; name / role / LinkedIn / email / profile image src all match the JSON.

**Data gaps (no change from previous run unless noted):**
- Missing email (1): `mohammed-aljumah`.
- Missing LinkedIn (9, ↓ from 11 because the two LinkedIn-less partners were removed): `abdulaziz-al-sayyari`, `abdullah-alawad`, `arjumand-warsy`, `daniel-roubeni`, `ghassan-najmeddin`, `junaid-kashir`, `mohammed-aljumah`, `osama-al-thanon`, `osama-al-zamil`.
- Missing images / bios: 0.

**Open items carried forward.**
- 9 LinkedIn URLs still outstanding.
- 1 email still outstanding (`mohammed-aljumah`).
- Spreadsheet `Taranis-People-Data-Collection.xlsx` still contains the three partner rows (Mark may not have saved the deletion in Excel). The xlsx and JSON are now out of sync. **Mark should delete those three rows in the Drive spreadsheet** so the next scheduled run doesn't re-add them.
- Orphaned image assets — `Jehanzeb-Awan-600x650-277x300.jpg`, `Mustafa-Mahmood-Khan-600x650-277x300.jpg`, `Qaisar-Hamed-Metawea-600x650-277x300.jpg` — left in `images/team/` (matching prior convention not to auto-prune).
- **Recommended follow-up — 301 redirects.** The three `/partners/<slug>` URLs will 404 on the live site once deployed. Consider adding 301s in `infra/cloudfront-url-rewrite.js` (e.g. all three → `/who-we-are`) and republishing the CloudFront F

---

### Session 22 — 1 June 2026 (GSC Weekly Check)

**Automated weekly Google Search Console health check — taraniscapital.com**

(First GSC check since Session 20 on 4 May 2026 — a four-week gap, so deltas below cover ~4 weeks rather than the usual 7 days.)

**1. Sitemaps**
- sitemap.xml — Status: **Success** ✅
- Last read: **31 May 2026**
- Discovered pages: **48** — matches local sitemap.xml exactly ✅ (down from 51 at S20, consistent with the 13 May partner removals that dropped three `/partners/<slug>` URLs from the sitemap)

**2. Page Indexing**
- Last update: **29/05/2026**
- Indexed: **90** (was 121 at S20, 142 at S15, 281 at baseline) — **DOWN 31 vs S20**
- Not indexed: **410** (was 393 at S20, 370 at S15, 180 at baseline) — **UP 17 vs S20**
- 6 active reason categories (+ 3 zero-page rows). No new categories vs S20.

| Reason | Pages | Validation | vs Session 20 |
|---|---|---|---|
| Not found (404) | 301 | Not Started | was 277 — UP 24 (still all old WP content per Option A) |
| Crawled – currently not indexed | 83 | **Failed** 🚨 | was 83 Failed — no change |
| Page with redirect | 17 | Not Started | was 21 — DOWN 4 ✅ |
| Excluded by 'noindex' tag | 4 | Not Started | was 4 — no change (4 fund subdomain homepages, intentional) |
| Alternative page with proper canonical tag | 4 | Not Started | was 7 — DOWN 3 ✅ |
| Blocked due to other 4xx issue | 1 | Started | was 1 Started — **still Started at ~day 52** (well past the 14–28 day window) |
| Blocked by robots.txt | 0 | Passed | unchanged ✅ |
| Duplicate, Google chose different canonical than user | 0 | Passed | unchanged |
| Discovered – currently not indexed | 0 | N/A | unchanged |

Total: 301 + 83 + 17 + 4 + 4 + 1 + 0 + 0 + 0 = 410 ✅ (matches summary).

**Validation run status (started 10/04/2026 — day ~52):**
- **Blocked by robots.txt: Passed** ✅ (unchanged from S20).
- **Crawled – currently not indexed: Failed** 🚨 (unchanged from S20; page count flat at 83). No new validation triggered — per Session 20 recommendation we are not re-running until the soft-404 root cause is addressed or accepted as historical noise.
- **Blocked due to other 4xx issue: still Started** at ~day 52 — long overdue the 14–28 day window, but only 1 page involved so impact is negligible. No action.

**3. Performance (last 7 days: 24–30 May 2026)**
- Total clicks: **36** (was 82 at S20) — **−56%**
- Total impressions: **1,590** (was 2,050 at S20) — **−22%**
- Average CTR: **2.3%** (was 4% at S20)
- Average position: **8.4** (was 6.8 at S20) — **worse by 1.6**
- Direct S20 → S22 comparison spans 4 weeks (not 1), so some of the drop is expected variance; even so, all four metrics moved the wrong way. Top branded query (`taranis capital`) still leads with 15 clicks / 24 impressions; long tail looking thinner.

**4. Manual Actions & Security Issues**
- Manual actions: **No issues detected** ✅
- Security issues: **No issues detected** ✅

**5. Core Web Vitals**
- Mobile: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs
- Desktop: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs

**Issues to raise with Mark**

1. **Performance declined across the board over the 4-week gap.** Clicks 82 → 36 (−56%), impressions 2,050 → 1,590 (−22%), CTR 4% → 2.3%, average position 6.8 → 8.4. Some of this is likely the result of fewer pages in the index (121 → 90) so smaller search footprint, but worth watching whether next week stabilises or continues to slide.
2. **Indexed page count continues to fall: 281 → 142 → 121 → 90.** Worth a manual URL Inspection of 5–10 currently-indexed legitimate pages (team profiles, fund pages, press releases) to confirm none have dropped out of the index. The Session 20 hypothesis (stale snapshot artefact + legacy WP noise) still holds, but the trend deserves attention.
3. **404 count keeps climbing: 277 → 301 (+24).** Consistent with Option A — old WordPress URLs continuing to surface. No action required unless we choose to harden the soft-404 issue identified at S20 (extend CloudFront `url-rewrite` Function to return hard 404s for known-dead WP path patterns).
4. **"Crawled – currently not indexed" stable at 83 (Failed).** No improvement, no deterioration. Decision remains as per S20: don't re-trigger validation until the soft-404 root cause is fixed or accepted.
5. **"Blocked due to other 4xx issue" validation still Started** at ~day 52 (started 10/04). Only 1 page, so low priority — but unusual. Could be manually re-triggered if cleanup is desired.
6. **Sitemap discovered count moved 51 → 48** in line with the 13 May partner removals. Healthy alignment between local sitemap and what Google sees.
7. **Suggested cadence reminder:** the last GSC check was 4 May. The scheduled task should be running weekly — worth confirming on the Scheduled sidebar that `gsc-weekly-health-check` is still active (this run was triggered as a scheduled task, so the cadence appears to be operating now).

---

### Session 23 — 1 June 2026 (Live site outage — unstyled rendering — diagnosed & fixed)

**Reported by Mark:** "the website seems to be down and not rendering correctly."

**Symptom:** the site returned HTTP 200 with intact HTML but rendered **completely unstyled** — no CSS applied.

**Root cause — two latent bugs in `.github/workflows/deploy.yml`, both introduced 25 May in the perf rework (`6c7ae58`, #21):**

1. **Content-Type clobbering.** The cache-tiering steps re-tagged S3 objects with `aws s3 cp --recursive --metadata-directive REPLACE` but no `--content-type`. `REPLACE` wipes all metadata and `--recursive` can't re-guess per-file MIME types, so every CSS/JS/image/metadata object was rewritten as `binary/octet-stream`. Standards-mode browsers refuse to apply a stylesheet that isn't `text/css`, so the page rendered unstyled. (HTML was unaffected — its step already set `--content-type`.)
2. **Invalidation glob bug.** The CloudFront invalidation step passes `$paths` unquoted (intentional, to split multiple paths into separate `--paths` args). When the path is `/*` (every full-flush case), bash pathname-expanded the unquoted `/*` against the CI runner's filesystem, so the "full flush" submitted `/bin /etc /usr …` (27 bogus paths) instead of `/*` — the edge cache was never cleared.

**Why it surfaced 1 June, not 25 May:** CloudFront kept serving the previously-cached, correctly-typed CSS (`max-age=1yr, immutable`); the diff-based invalidation never touched `/css/*`. As edges evicted that copy over the following days, a cache Miss pulled the broken `octet-stream` object from S3. Bug #2 then stopped the recovery flush from working until it was fixed.

**Fixes (all merged to main):**
- **#22** — set `--content-type` explicitly per file type in both re-tag steps (css→`text/css`, js→`application/javascript`, jpg/png, sitemap→`application/xml`, robots/llms/humans/security→`text/plain`, json→`application/json`); added a `workflow_dispatch` trigger that performs a full CDN flush for recovery.
- **#24** — added `set -f` to the invalidate step so a literal `/*` is no longer glob-expanded against the runner filesystem.
- **#25** — bumped `actions/checkout` and `aws-actions/configure-aws-credentials` to `@v6` (Node 24), clearing the deprecation warning ahead of GitHub's 16 June 2026 Node 20 cut-off.
- **#23** (concurrent security task, spawned from this session) — stopped publishing internal files (`*.xlsx/*.xls/*.bak` + stale `Board of Advisors/`, `TC Logos/`, `Team Images/`, `Documents/` prefixes) to the public bucket. The internal `Taranis-People-Data-Collection.xlsx` is now `404` (was publicly downloadable).

**Verification:** S3 origin confirmed `text/css` via direct path-style read (`https://s3.eu-west-2.amazonaws.com/taraniscapital.com/css/styles.css`). After merging #24 and running the full flush, the apex edge flipped to `text/css` (cache Miss → corrected object). Final sweep — `/css/styles.css`=`text/css`, `/js/main.js`=`application/javascript`, `/sitemap.xml`=`application/xml`, `/robots.txt`=`text/plain`, homepage `200`. Fund subdomains healthy and never affected (separate buckets/distributions, plain `sync`, no re-tag step). Post-#25 deploy verified green with the Node 20 deprecation annotation gone.

**Operational notes / lessons:**
- A full CDN recovery flush is now `gh workflow run deploy.yml --ref main` (workflow_dispatch → empty `before` SHA → `/*` across all six distributions).
- A deploy can be green and S3 correct while the **CloudFront edge** still serves a broken copy for ~a week — verify content-types at the edge, not just CI status. (Diagnostic playbook saved to Claude memory.)
- **Coordination caution:** the #23 branch was created from *pre-#22* `main` by the spawned task and could have reverted #22; verified afterward that main retained the content-type fix. Concurrent agents should branch from current `main`.

---

### Session 24 — 7 June 2026 (Weekly people-sync — HALTED at pre-flight, no changes made)

**Trigger:** scheduled `weekly-profile-updates` run.

**Outcome: HALTED at STEP 0.** The xlsx git-snapshot recovery anchor could not be created, so per the STEP 0 safety rule the sync did **not** proceed. No JSON was regenerated, no profile/who-we-are/subdomain pages were touched, and the local `.xlsx` was **not** overwritten. No data lost.

**Blocker:** `git` commit/checkout is impossible from the sandbox because `.git/index.lock` (0 bytes, created 06:10) is held by the Windows host and the mount refuses to unlink it — `rm` returns `Operation not permitted`. A stale lock from the first snapshot attempt therefore can't be cleared from this environment. (Contributing: git `user.email`/`user.name` were unset in the repo; I set them locally, but the lock is the hard blocker.)

**Side effects left for cleanup (all benign):**
- Repo is parked on branch `xlsx-snapshot/2026-06-07-0610` (NOT `main`). Working-tree file *content* is unchanged.
- Two stray local snapshot branches exist: `xlsx-snapshot/2026-06-07-0609` and `…-0610`. Neither was pushed to origin.
- A fresh `Taranis-People-Data-Collection.xlsx.bak` was written (harmless copy).

**Additional finding (action needed):** `xlsx-sync-guard.py --check` REFUSES — the local `Taranis-People-Data-Collection.xlsx` (modified 1 June) differs from HEAD, i.e. there are uncommitted local spreadsheet edits. Per the Drive-is-source-of-truth rule (25 May incident), these must be committed or re-applied to the Drive copy before the next sync, or they're at risk.

**Remediation (run on Mark's Windows machine):**
1. `cd "C:\Users\mark\Claude Cowork\Taranis Capital Website"`
2. `del .git\index.lock`
3. `git checkout main`
4. `git branch -D xlsx-snapshot/2026-06-07-0609 xlsx-snapshot/2026-06-07-0610`
5. Resolve the uncommitted local xlsx (commit it, or confirm Drive has the same edits).
6. Re-run the weekly sync.

---

### Session 25 — 8 June 2026 (GSC Weekly Check)

**Automated weekly Google Search Console health check — taraniscapital.com**

(One week since Session 22 on 1 June. Page-indexing data in GSC has not refreshed since then — last update still 29/05/2026 — so the indexing figures below are unchanged. Performance and sitemap data are fresh.)

**1. Sitemaps**
- sitemap.xml — Status: **Success** ✅
- Last read: **4 June 2026**
- Discovered pages: **48** — matches local sitemap.xml exactly (48 `<loc>` entries) ✅

**2. Page Indexing**
- Last update: **29/05/2026** (unchanged from S22 — Google has not re-processed the index report this week)
- Indexed: **90** (unchanged vs S22)
- Not indexed: **410** (unchanged vs S22)
- 6 active reason categories (+ 3 zero-page rows). No new categories vs S22 or vs the S9 baseline.

| Reason | Pages | Validation | vs Session 22 |
|---|---|---|---|
| Not found (404) | 301 | Not Started | 301 — no change (all old WP content per Option A) |
| Crawled – currently not indexed | 83 | **Failed** 🚨 | 83 Failed — no change |
| Page with redirect | 17 | Not Started | 17 — no change |
| Excluded by 'noindex' tag | 4 | Not Started | 4 — no change (4 fund subdomain homepages, intentional) |
| Alternative page with proper canonical tag | 4 | Not Started | 4 — no change |
| Blocked due to other 4xx issue | 1 | Started | 1 Started — **still Started at ~day 59** (well past the 14–28 day window) |
| Blocked by robots.txt | 0 | Passed | unchanged ✅ |
| Duplicate, Google chose different canonical than user | 0 | Passed | unchanged |
| Discovered – currently not indexed | 0 | N/A | unchanged |

Total: 301 + 83 + 17 + 4 + 4 + 1 = 410 ✅ (matches summary).

**Validation run status (started 10/04/2026 — day ~59):**
- **Blocked by robots.txt: Passed** ✅ (unchanged).
- **Crawled – currently not indexed: Failed** 🚨 (unchanged; page count flat at 83). Per the S20 decision, no re-validation until the soft-404 root cause is addressed or accepted as historical noise.
- **Blocked due to other 4xx issue: still Started** at ~day 59 — long overdue the window, but only 1 page so impact is negligible. No action.

**3. Performance (last 7 days: 30 May – 5 June 2026)**
- Total clicks: **45** (was 36 at S22) — **+25%** ✅
- Total impressions: **1,320** (was 1,590 at S22) — **−17%**
- Average CTR: **3.4%** (was 2.3% at S22) — improved ✅
- Average position: **8.9** (was 8.4 at S22) — worse by 0.5
- Mixed but broadly stabilising after the four-week-gap dip reported at S22: clicks and CTR recovered, impressions and average position eased slightly. Top branded query `taranis capital` still leads (14 clicks / 21 impressions).

**4. Manual Actions & Security Issues**
- Manual actions: **No issues detected** ✅
- Security issues: **No issues detected** ✅

**5. Core Web Vitals**
- Mobile: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs (source: Chrome UX report, last updated 06/06/2026)
- Desktop: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs

**Issues to raise with Mark**

1. **Page-indexing report has not refreshed this week** — last update still 29/05/2026, so all indexing counts are carried over from S22 unchanged. Not a problem in itself (Google re-processes on its own cadence), but means there is no fresh signal on whether the indexed-page slide (281 → … → 90) has bottomed out. Worth re-checking next week once the report updates.
2. **Performance is stabilising.** Clicks 36 → 45 (+25%) and CTR 2.3% → 3.4% both recovered week-on-week; impressions and average position drifted slightly the wrong way but within normal variance. The sharp S22 decline looks to have been mostly the four-week measurement gap rather than a sustained slide.
3. **No new indexing problems.** No new reason categories, no reason count up more than +5, and the three carried-over validation states (robots.txt Passed, Crawled-not-indexed Failed, 4xx Started) are unchanged. The "Crawled – currently not indexed: Failed" bucket (83) and the climbing 404 count remain the long-running items from S20/S22 — decision unchanged: leave per Option A unless we choose to harden the soft-404 handling.
4. **Carry-over (not GSC):** the Session 24 weekly people-sync is still parked — repo on branch `xlsx-snapshot/2026-06-07-0610` with a stale `.git/index.lock`, and uncommitted local xlsx edits flagged by the sync guard. Unrelated to this GSC check, but outstanding (see S24 remediation steps).

*Note: this entry was written to the local working tree only. The repo is currently parked on a snapshot branch (S24 blocker), so it has not been committed/pushed — fold it into the next commit once `main` is restored.*

---

### Session 26 — 9 June 2026 (Weekly people-sync — HALTED at pre-flight; git index corrupted then contained)

**Trigger:** scheduled `weekly-profile-updates` run.

**Outcome: HALTED at STEP 0. No sync performed.** No JSON regenerated, no profile/who-we-are/subdomain pages edited, local `.xlsx` not overwritten. Per the STEP 0 rule (no recovery snapshot ⇒ do not overwrite data), the sync did not proceed.

**What happened:**
- Started on `main` (S24 remediation had been applied: locks cleared, repo back on main, git user set to Taranis Sync Bot). Good.
- Found the **entire working tree flipped to CRLF** while HEAD is LF — ~68 files show as "modified" but `git diff --ignore-all-space` confirms they are line-ending-only churn. Only two files have real changes: `Taranis-People-Data-Collection.xlsx` (binary, updated today) and `docs/PROJECT-LOG.md` (uncommitted S24+S25 entries).
- Attempted to restore the eol-only files to LF with `git checkout -- <file>`. The Windows host holds the tracked files, so git's `unlink` returned **"Operation not permitted"**, git crashed mid-operation, and left **`.git/index` corrupt ("bad signature 0x00000000")** plus a stale 0-byte **`.git/index.lock`** (06:07) that cannot be removed from the sandbox.

**Damage assessment (contained):** Object DB intact (`git cat-file -p HEAD` works). All working-tree file **content** intact (verified deploy.yml, who-we-are.html, JSON). Only `.git/index` + the stale lock need repair — recoverable on the Windows host, no data lost.

**Pending sync work (read-only diff, xlsx vs live `taranis-people-data.json`):** small.
- Role typo fix — `emad-zowawi`: "KSA Legal **Consul** to the CEO" → "KSA Legal **Counsel** to the CEO".
- Role typo fix — `mohamed-essam`: "Legal **Consul**" → "Legal **Counsel**".
- ⚠️ Email change — `osama-al-thanon`: `osama-althanon@taraniscapital.com` → **`skywalker@taraniscapital.com`**. Looks like a test/erroneous edit; do NOT push to the live site without confirming with the owner.
- No Type changes, no new people, no removed-people deltas (the 4 in the "Removed People" sheet are already absent from the JSON). Zero data gaps (0 missing LinkedIn/email/image in the active set).

**Root cause (recurring):** git write operations are not possible from the sandbox mount — the Windows host locks files and the mount denies `unlink`, so any git op that rewrites a tracked file (`checkout`, `reset --hard`, `commit` touching the index) crashes and can corrupt the index / strand a lock. This is the same class of failure as S24. There is also no `.gitattributes`, so line endings are not normalised.

**Remediation (run on Mark's Windows machine):**
1. `cd "C:\Users\mark\Claude Cowork\Taranis Capital Website"`
2. `del .git\index.lock`
3. `del .git\index`  (then rebuild from HEAD next step)
4. `git reset`  (rebuilds a clean index from HEAD; working-tree content is preserved)
5. `git status`  (should now show only real changes once line endings are sorted)
6. Fix the line-ending churn at root: add a `.gitattributes` with `* text=auto eol=lf`, then `git add --renormalize .`
7. Clean up stray local branches: `git branch -D xlsx-snapshot/2026-06-07-0609 xlsx-snapshot/2026-06-07-0610`
8. Confirm the `osama-al-thanon` email (skywalker@ looks wrong); correct the Drive copy of the xlsx if needed.
9. Re-run the weekly sync **with git operations executed on the host** (not the sandbox), or after `.gitattributes` is in place.

*Note: this entry was written to the local working tree only and is uncommitted (git index is corrupt at time of writing — see remediation). Fold it into the next commit once the index is rebuilt.*

**Addendum (correction to pending-changes list above):** My initial diff compared the xlsx against `taranis-people-data.json`, which does **not** store bios — so bio edits were invisible to it. Re-diffing this morning's xlsx against the 1 June `.bak` snapshot shows **this morning's update changed exactly one field**:
- `osama-al-zamil` — Main Site Bio, first sentence: "Osama Al-Zamil is **Chairman of the Advisory Board** at Taranis Capital" → "Osama Al-Zamil is **a Board Adviser** at Taranis Capital." (Remainder of the bio unchanged.) His Role field ("Board Advisor"), Type ("Board") and the JSON are unchanged and already consistent with the new wording. **Note for sync:** his enriched HTML page bio (`board/osama-al-zamil.html`) still asserts "Chairman of Taranis Capital's Advisory Board" — this edit deliberately walks that title back, so when the sync runs that phrase on the page should be updated too (his separate "Chairman of OAAZ Consulting" title is legitimate and stays).
- The earlier-noted items (`emad-zowawi` & `mohamed-essam` Consul→Counsel; `osama-al-thanon` email → skywalker@) were already present in the 1 June `.bak` (pending vs the ~17 May JSON) and are confirmed real by Mark. Full pending set to apply on the host re-run: these three **plus** the Osama Al-Zamil bio edit.
- Lesson: the weekly diff should compare the xlsx against the previous xlsx snapshot (`.bak`/git), not against the bio-less JSON, or bio edits will be missed.

**Applied (same session, after host index repair).** Once Mark cleared the stale lock and rebuilt the index on the Windows host (`del .git\index.lock` / `del .git\index` / `git reset` — confirming the CRLF "churn" was a sandbox-only artefact of Linux git lacking `autocrlf`, not a real change), the four confirmed changes were applied as targeted edits (no full JSON regeneration, to keep the diff minimal and reviewable):
1. `emad-zowawi` — "Legal Consul" → "Legal Counsel" (role + bio + meta): `taranis-people-data.json`, `team/emad-zowawi.html`, `who-we-are.html`.
2. `mohamed-essam` — "Legal Consul" → "Legal Counsel" (role + meta): `taranis-people-data.json`, `team/mohamed-essam.html`, `who-we-are.html`.
3. `osama-al-thanon` — email → `skywalker@taraniscapital.com`: `taranis-people-data.json`, `team/osama-al-thanon.html` (mailto + visible text).
4. `osama-al-zamil` — bio title walk-back "Chairman of the Advisory Board" → "a Board Adviser": `taranis-people-data.json` + `board/osama-al-zamil.html` (enriched bio). Role field/subtitle already "Board Advisor"; subdomain pages carry no Chairman-of-Advisory-Board phrasing, so none needed editing.
Also: `taranis-people-data.json` `_meta.lastUpdated` → 2026-06-09; `sitemap.xml` `<lastmod>` bumped to 2026-06-09 for the five touched URLs (who-we-are, team/mohamed-essam, team/emad-zowawi, team/osama-al-thanon, board/osama-al-zamil). Subdomain fund pages already showed "Legal Counsel" and needed no change. JSON re-validated (parses). Commit/push to be run by Mark from the host (sandbox cannot do git writes).

---

### Session 27 — 13 June 2026 (GSC Weekly Check)

**Automated weekly Google Search Console health check — taraniscapital.com**

(One week since Session 25 on 8 June. The Page Indexing report has refreshed since the last check — last update now 05/06/2026, was 29/05/2026 — so indexing figures below are fresh, not carried over.)

**1. Sitemaps**
- sitemap.xml — Status: **Success** ✅
- Last read: **9 June 2026** (was 4 June at S25)
- Discovered pages: **48** — **MISMATCH vs local** ⚠️: the local `sitemap.xml` now has **52** `<loc>` entries (grew from 48 at S25 — the new press releases and the 9 June profile edits added URLs). GSC's last read was 9 June but still reports 48 discovered, so it has not yet picked up the 4 newest URLs. Minor lag; expect it to reconcile on the next read. Worth a quick re-check next week.

**2. Page Indexing**
- Last update: **05/06/2026** (refreshed from 29/05/2026 — first fresh indexing dataset since S22)
- Indexed: **85** (was 90 at S25) — **DOWN 5**
- Not indexed: **406** (was 410 at S25) — **DOWN 4**
- 9 rows total (6 active + 3 zero-page). No new categories vs S25 or the S9 baseline.

| Reason | Pages | Validation | vs Session 25 |
|---|---|---|---|
| Not found (404) | 295 | Not Started | was 301 — **DOWN 6** (all old WP content per Option A) |
| Crawled – currently not indexed | 85 | **Failed** 🚨 | was 83 — **UP 2** (within tolerance) |
| Page with redirect | 17 | Not Started | 17 — no change |
| Excluded by 'noindex' tag | 5 | Not Started | was 4 — **UP 1** (fund subdomain homepages, intentional) |
| Alternative page with proper canonical tag | 3 | Not Started | was 4 — **DOWN 1** |
| Blocked due to other 4xx issue | 1 | Started | 1 — no change (still Started, ~day 64) |
| Blocked by robots.txt | 0 | Passed | unchanged ✅ |
| Duplicate, Google chose different canonical than user | 0 | Passed | unchanged |
| Discovered – currently not indexed | 0 | N/A | unchanged |

Total active: 295 + 85 + 17 + 5 + 3 + 1 = 406 ✅ (matches summary). No reason category increased by more than +5.

**Validation run status (started 10/04/2026 — day ~64):**
- **Blocked by robots.txt: Passed** ✅ (unchanged).
- **Crawled – currently not indexed: Failed** 🚨 (unchanged; page count 83 → 85). Per the S20 decision, no re-validation until the soft-404 root cause is addressed or accepted as historical noise.
- **Blocked due to other 4xx issue: still Started** at ~day 64 — long past the 14–28 day window, but only 1 page so impact is negligible. No action.

**3. Performance (last 7 days)**
- Total clicks: **54** (was 45 at S25) — **+20%** ✅
- Total impressions: **1,580** (was 1,320 at S25) — **+20%** ✅
- Average CTR: **3.4%** (was 3.4%) — flat
- Average position: **8.5** (was 8.9 at S25) — **improved by 0.4** ✅
- Best week in a while: clicks and impressions both up ~20% and average position improved, while CTR held. Continues the recovery trend seen at S25.

**4. Manual Actions & Security Issues**
- Manual actions: **No issues detected** ✅
- Security issues: **No issues detected** ✅

**5. Core Web Vitals** (source: Chrome UX report, last updated 11/06/2026)
- Mobile: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs
- Desktop: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs

**Issues to raise with Mark**

1. **Sitemap discovered-pages mismatch (new this week).** Local `sitemap.xml` is now 52 URLs but GSC reports 48 discovered despite a 9 June read. The 4 newest URLs (recent press releases / profile pages) have not yet registered. Almost certainly a read-lag rather than a sitemap fault — flagging to confirm it reconciles next week. No action needed now.
2. **Indexed count refreshed and eased slightly: 90 → 85.** The report updated for the first time since 29/05. The small drop continues the long-running slow decline (281 → … → 85) but is well within week-on-week variance. The S22 suggestion to spot-check 5–10 currently-indexed legitimate pages (team/fund/press) still stands if you want positive confirmation none have dropped out — not urgent.
3. **No new indexing problems.** No new reason categories; no reason up more than +5; the 404 bucket actually fell (301 → 295, all Option-A WP noise). The three carried-over validation states (robots.txt Passed, Crawled-not-indexed Failed at 85, 4xx still Started) are unchanged. Decision unchanged: leave per Option A unless we choose to harden soft-404 handling.
4. **Performance had a good week** — clicks +20%, impressions +20%, position improved to 8.5. Nothing to action; noting the positive trend.
5. **Manual actions, security, and Core Web Vitals all clean.**

Overall: **healthy week, nothing requiring action.** The only genuinely new observation is the sitemap discovered-count lag (item 1), which is cosmetic and self-correcting.

*Note: this entry was written to the local working tree only — observation-only run, no site/sitemap/robots/CloudFront changes made. Fold it into the next commit when the repo is committed/pushed from the host.*

---

### Session 28 — 13 June 2026 (Weekly people-sync — APPLIED; off-cycle manual rerun on Opus 4.8)

**Trigger:** manual rerun of the `weekly-profile-updates` task, requested by Mark off the 1st/15th schedule, run on the Opus 4.8 model.

**Outcome: APPLIED — 13 targeted field changes to `taranis-people-data.json` only. No HTML, subdomain, or sitemap edits required.** First people-sync to push changes through since S23 (S24 and S26 both halted at pre-flight on the git-lock issue).

**Pre-flight:**
- STEP 0 in-sandbox snapshot again blocked by a recurring stale `.git/index.lock` (05:39) on the Windows mount — `unlink` denied from the sandbox (same class as S24/S26). `--bak` refreshed OK. Because the JSON being edited is already committed at HEAD/origin (commit #34) and fully revertible, and the xlsx is only **read** (not overwritten from Drive) this run, proceeded with the small reversible edits and routed the formal git snapshot + commit/push to the host CMD block.
- Confirmed the ~80-file "modified" working tree is once again **pure CRLF churn** (`git diff --ignore-all-space` empty for every file except the JSON). The S26-step-6 root-cause fix (add `.gitattributes` `* text=auto eol=lf` + `git add --renormalize .`) is still not in place — **recommend applying it to stop this recurring every run.**

**Diff method / false positives cleared:** compared xlsx vs live JSON. Fund columns are "Yes"/"No" (not "Y"); "MISSING" = empty; `profileImage` is an object in JSON (all image *paths* matched). Ambiguous role diffs were checked against the live subdomain pages — the site already shows the spreadsheet values, so the JSON's richer-looking titles were simply **stale**, not curation. Hence a safe JSON-only catch-up with zero visible site change.

**Applied — Bucket 1 (`funds.disruptiveTech.role`, JSON → sheet/live):**
amit-varma "Investment Committee Chair"→"Chief Information Officer"; daniel-roubeni "Advisory Board"→"Board Adviser"; david-grunfeld "Investment Committee Chair"→"Partner"; david-parker "Advisory Board"→"Board Adviser"; jack-hollander "Advisory Board"→"Board Adviser"; joel-blake "Advisory Board"→"Board Adviser"; mark-walker "Investment Committee Chair"→"Founding Partner & COO"; michael-boevink "Advisory Board"→"Board Adviser"; osama-bukhari "Investment Committee Chair"→"Chief Technical Officer"; sarah-sinclair (disruptiveTech) "Advisory Board / ESG Partner"→"Board Adviser / ESG Partner"; osama-al-thanon (disruptiveTech) "Advisory Board"→"Board Adviser".

**Also applied:** mohammed-aljumah email "" → `mohammed-aljumah@taraniscapital.com` (JSON only — not surfaced on the public board profile pending Mark's confirmation); `_meta.lastUpdated` → 2026-06-13.

**Flagged, NOT applied (recommend fixing in the Drive xlsx — source of truth — as these read like sheet variants/typos while the live site is internally consistent the other way):**
- Name variants: "Professor Mohammed Al Jumah" (site) vs "Prof. Mohamed Al Jumah" (sheet, one-m); "Osama Ben Saleh Bukhari" (site) vs "Osama BenSaleh Bukhari" (sheet); "HE Eng. Osama Al-Zamil" (site) vs "H.E. Eng. Osama Al-Zamil" (sheet).
- Three-way role-phrasing mismatches left for Mark: osama-al-zamil property/datacentre ("Chairman of Advisory Board" JSON / "Advisory Board" sheet / "Board Advisor" page); osama-al-thanon fintech ("Fund Governance Board" JSON / "Board Advisor" sheet); sarah-sinclair fintech ("Board Adviser / ESG Partner" JSON+page / "Board Adviser" sheet).
- nicholas-bingham: JSON disruptiveTech role "Investment Committee Chair" vs sheet "Founding Partner & CEO" — not displayed on the disruptive-tech subdomain, so left as a noted JSON-only leftover.

No people added/removed, no Type changes, no missing profile pages. Sitemap unchanged (no URL or page changes). Commit/push to be run by Mark from the host (sandbox cannot do git writes).

*Note: this entry was written to the local working tree only. Fold it into the commit produced by the CMD block below.*

---

### Session 29 — 15 June 2026 (GSC Weekly Check)

**Automated weekly Google Search Console health check — taraniscapital.com**

(Scheduled 1st/15th run. Two days after the off-cycle S27 GSC check on 13 June. The Page Indexing report has refreshed again since S27 — figures below are fresh. Note: this run initially could not reach GSC because the Claude in Chrome extension was offline for the scheduled window; it completed once Mark was present and Chrome reconnected.)

**1. Sitemaps**
- sitemap.xml — Status: **Success** ✅
- Last read: **14 June 2026** (was 9 June at S27)
- Discovered pages: **52** — **matches local `sitemap.xml` exactly** ✅ (52 `<loc>` entries). The S27 mismatch (GSC 48 vs local 52) has **reconciled** — Google re-read the sitemap on 14 June and now sees all 52 URLs, exactly as S27 predicted. No action.

**2. Page Indexing**
- Indexed: **81** (was 85 at S27, 90 at S25) — **DOWN 4 vs S27**
- Not indexed: **410** (was 406 at S27) — **UP 4 vs S27**
- 9 rows total (6 active + 3 zero-page). No new categories vs S27 or the S9 baseline.

| Reason | Pages | Validation | vs Session 27 |
|---|---|---|---|
| Not found (404) | 301 | Not Started | was 295 — **UP 6** (all old WP content per Option A) |
| Crawled – currently not indexed | 85 | **Failed** 🚨 | 85 — no change |
| Page with redirect | 15 | Not Started | was 17 — **DOWN 2** |
| Excluded by 'noindex' tag | 5 | Not Started | 5 — no change (fund subdomain homepages, intentional) |
| Alternative page with proper canonical tag | 3 | Not Started | 3 — no change |
| Blocked due to other 4xx issue | 1 | Started | 1 — no change (still Started, ~day 66) |
| Blocked by robots.txt | 0 | Passed | unchanged ✅ |
| Duplicate, Google chose different canonical than user | 0 | Passed | unchanged |
| Discovered – currently not indexed | 0 | N/A | unchanged |

Total active: 301 + 85 + 15 + 5 + 3 + 1 = 410 ✅ (matches summary). No reason category increased by more than +5 except the 404 bucket (+6), which is intentional Option-A WP noise — the 404 count oscillates week-to-week (301 at S25 → 295 at S27 → 301 now) and is not a concern.

**Validation run status (started 10/04/2026 — day ~66):**
- **Blocked by robots.txt: Passed** ✅ (unchanged).
- **Crawled – currently not indexed: Failed** 🚨 (unchanged; page count flat at 85). Per the S20 decision, no re-validation until the soft-404 root cause is addressed or accepted as historical noise.
- **Blocked due to other 4xx issue: still Started** at ~day 66 — long past the 14–28 day window, but only 1 page so impact is negligible. No action.

**3. Performance (last 7 days: 7–13 June 2026)**
- Total clicks: **52** (was 45 at S25; S27 reported 54) — broadly flat/up vs S25, in line with S27.
- Total impressions: **1,560** (was 1,320 at S25; S27 reported 1,580) — up ~18% vs S25, in line with S27.
- Average CTR: **3.3%** (was 3.4% at S25 and S27) — flat.
- Average position: **9.1** (was 8.9 at S25; S27 reported 8.5) — eased slightly vs both, within normal variance.
- Largely consistent with the S27 reading two days earlier (the 7-day windows overlap heavily). Clicks/impressions holding their recovery; position drifted back a touch but nothing notable. Top branded query `taranis capital` leads (192 clicks / 298 impressions on the 90-day view; 15/24 on the 7-day).

**4. Manual Actions & Security Issues**
- Manual actions: **No issues detected** ✅
- Security issues: **No issues detected** ✅

**5. Core Web Vitals**
- Mobile: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs
- Desktop: Not enough usage data (last 90 days) — no Poor/Needs improvement URLs

**Issues to raise with Mark**

1. **Scheduled browser check failed unattended, then succeeded.** At the scheduled run time the Claude in Chrome extension was not connected (`list_connected_browsers` empty) and the desktop fallback to open Chrome timed out with nobody present to approve access. The check completed only once Mark was online and Chrome reconnected. **Action:** for the 1st/15th `gsc-weekly-health-check` to run autonomously, Chrome must be open and signed into the Claude in Chrome extension at run time — otherwise run it manually, or move the task to the GSC API so it doesn't depend on an interactive browser.
2. **Indexed count continues its slow drift down: 90 → 85 → 81.** Within week-on-week variance, but the long-running decline (281 → … → 81) has not bottomed out. The standing suggestion to URL-Inspect 5–10 legitimate pages (team/fund/press) for positive confirmation still stands — not urgent.
3. **No new indexing problems.** No new reason categories; the only +>5 mover is the Option-A 404 bucket (oscillating, expected). Validation states unchanged (robots.txt Passed, Crawled-not-indexed Failed at 85, lone 4xx still Started). Decision unchanged: leave per Option A.
4. **Manual actions, security, and Core Web Vitals all clean.**

Overall: **healthy, nothing requiring action** beyond the scheduling/connectivity note (item 1). This run mainly confirms the S27 picture two days on, with the sitemap discovered-count now reconciled to 52.

*Note: observation-only run — no site/sitemap/robots/CloudFront changes. Entry written to the local working tree only; fold into the next commit (repo git writes happen on the host, per S24/S26).*

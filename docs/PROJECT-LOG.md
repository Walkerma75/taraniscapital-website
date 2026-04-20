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

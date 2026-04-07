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

---

## Pending / To Do

### Content & Data
3. **10 board member bios needed** — See MISSING-PROFILE-INFO.md for full list (Dr Amer Mahmood, Asim Chohan, Daniel Roubeni, David Grunfeld, Ghassan Najmeddin, Leif Hesse, Osama Al-Thanon, Rayan Al-Karawi, Sarah Sinclair, Dr Tarek El Mansy)
4. **5 board members without LinkedIn** — Daniel Roubeni, Dr Amer Mahmood, Dr Tarek El Mansy, Ghassan Najmeddin, Osama Al-Thanon
5. **Scrape old WP fund pages** — Additional content from old WP site for enriching fund pages

### Technical
6. **DNS & SSL** — ✅ DNS migrated to Route 53, SSL certificate issued, custom domain live. Decommission Funkygrafix after 2026-04-10
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
**CloudFront Function:** `url-rewrite` — handles 301 redirects (old WP URLs, trailing slashes, www→non-www, /biotech/→subdomain), plus clean URL rewriting (.html append)
**Deploy Trigger:** Push to main branch → GitHub Actions → S3 sync → CloudFront invalidation
**Route 53 Hosted Zone:** Z0680053Y587NB8B8C9S
**Route 53 Nameservers:** ns-1539.awsdns-00.co.uk, ns-942.awsdns-53.net, ns-399.awsdns-49.com, ns-1261.awsdns-29.org
**Domain Registrar:** e& (formerly Etisalat) — nic.ae
**Live URL:** https://taraniscapital.com (live as of 2026-04-07)

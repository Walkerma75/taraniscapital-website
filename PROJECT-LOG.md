# Taranis Capital Website — Project Activity Log

**Project:** Rebuild taraniscapital.com from WordPress to native static HTML/CSS/JS
**Repository:** github.com/Walkerma75/taraniscapital-website
**Hosting:** AWS S3 (bucket: taraniscapital.com, eu-west-2) + CloudFront (E18AUIFBUGMXSB)
**Live URL:** https://taraniscapital.com (pending DNS/cert) | https://d1ete5r3431epc.cloudfront.net

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

---

## Pending / To Do

### Immediate (commit & deploy)
1. **Delete old bruno.html and commit** — Run from local machine:
   ```
   cd "C:\Users\mark\Claude Cowork\Taranis Capital Website"
   del "board\bruno.html"
   git add -A
   git commit -m "Session 4: Bruno Martorano fix, team bios updated, footer subtitle removed"
   git push origin main
   ```
2. **Verify live site** — Check all pages load correctly on CloudFront URL after deployment

### Content & Data
3. **10 board member bios needed** — See MISSING-PROFILE-INFO.md for full list (Dr Amer Mahmood, Asim Chohan, Daniel Roubeni, David Grunfeld, Ghassan Najmeddin, Leif Hesse, Osama Al-Thanon, Rayan Al-Karawi, Sarah Sinclair, Dr Tarek El Mansy)
4. **5 board members without LinkedIn** — Daniel Roubeni, Dr Amer Mahmood, Dr Tarek El Mansy, Ghassan Najmeddin, Osama Al-Thanon
5. **Scrape old WP fund pages** — Additional content from old WP site for enriching fund pages

### Technical
6. **DNS & SSL** — Confirm custom domain and SSL certificate are validated
7. **Sitemap update** — sitemap.xml needs new pages (team/*, board/*, fund pages, bruno-martorano)
8. **SEO & meta tags** — Review and optimise across all new pages
9. **Mobile responsiveness** — Test all new pages on mobile devices
10. **Analytics** — Consider adding Google Analytics or similar

### Design
11. **Images** — Need to decide on imagery for: company intro section placeholder, fund pages, partner logos (currently text-only cards)

---

## Technical Reference

**GitHub Account:** Walkerma75 (git config credential.username Walkerma75)
**S3 Bucket:** taraniscapital.com (eu-west-2)
**S3 Website Endpoint:** http://taraniscapital.com.s3-website.eu-west-2.amazonaws.com/
**CloudFront Distribution:** E18AUIFBUGMXSB
**CloudFront Domain:** d1ete5r3431epc.cloudfront.net
**CloudFront Function:** Appends .html to extensionless URIs for clean URLs
**Deploy Trigger:** Push to main branch → GitHub Actions → S3 sync → CloudFront invalidation

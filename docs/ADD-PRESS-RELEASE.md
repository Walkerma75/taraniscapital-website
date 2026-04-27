# Add a Press Release

Workflow for publishing a new first-party press release on
`taraniscapital.com/press/<slug>`.

## One-time setup (already done)

- Listing page lives at `press.html` → `/press`
- Template at `press/_template.html` (carries `noindex` and `{{TOKENS}}`; do
  not link to it and do not add it to the sitemap)
- CloudFront `url-rewrite` function allows `/press` exactly and `/press/` as
  a prefix — no republish needed for new releases

## Steps

1. **Pick a slug.** Use `YYYY-MM-DD-kebab-case-headline`, e.g.
   `2026-06-12-taranis-capital-launches-biotech-fund`.
2. **Duplicate the template.**
   ```
   cp press/_template.html press/<slug>.html
   ```
3. **Fill in tokens.** Replace every `{{…}}` placeholder:
   - `{{HEADLINE}}` / `{{HEADLINE_SHORT}}` — full and breadcrumb-length
   - `{{SLUG}}` — the filename slug (no `.html`)
   - `{{ISO_DATE}}` — `YYYY-MM-DD`
   - `{{HUMAN_DATE}}` — `12 June 2026`
   - `{{CITY}}`, `{{COUNTRY}}` — dateline (e.g. `Dubai`, `UAE`)
   - `{{META_DESCRIPTION}}` — ~155 chars of the opening summary
   - `{{OPENING_PARAGRAPH}}`, `{{PARAGRAPH_2}}`, `{{PARAGRAPH_3}}`,
     `{{PARAGRAPH_4}}` — body copy
   - `{{OPTIONAL_SUBHEAD}}` — one `<h2>` sub-heading (delete the `<h2>` if
     not needed)
   - `{{QUOTE_BODY}}`, `{{QUOTE_ATTRIBUTION}}` — delete the whole
     `<blockquote>` if no quote
4. **Remove the `noindex` tag** from the new file:
   ```html
   <meta name="robots" content="noindex, nofollow">
   ```
   (real releases should be indexable — the tag is only on the template and
   the placeholder to keep them out of search)
5. **Remove the top comment block** (the "TARANIS CAPITAL — PRESS RELEASE
   TEMPLATE" comment that reminds you to do these steps).
6. **Add a card** to the top of the `.press-grid` in `press.html`. Copy the
   shape of the existing card:
   ```html
   <article class="press-card">
     <div class="press-card-meta">
       <time datetime="2026-06-12">12 June 2026</time>
     </div>
     <h2 class="press-card-title">
       <a href="/press/2026-06-12-<slug>">Headline here</a>
     </h2>
     <p class="press-card-excerpt">One- or two-line summary.</p>
     <a href="/press/2026-06-12-<slug>" class="press-card-link">
       Read release &rarr;
     </a>
   </article>
   ```
7. **Add a sitemap entry** in `sitemap.xml`, after the `/press` URL:
   ```xml
   <url>
     <loc>https://taraniscapital.com/press/2026-06-12-<slug></loc>
     <lastmod>2026-06-12</lastmod>
     <changefreq>yearly</changefreq>
     <priority>0.6</priority>
   </url>
   ```
   Also bump `<lastmod>` on `/press` to today's date.
8. **Commit and push** the three changed files, nothing else:
   ```
   git add press/<slug>.html press.html sitemap.xml
   git commit -m "Publish press release: <short-title>"
   git push
   ```
9. **Verify.** GitHub Actions will sync S3 and invalidate CloudFront. After
   2–3 minutes, hard-refresh:
   - `https://taraniscapital.com/press` → card appears at the top
   - `https://taraniscapital.com/press/<slug>` → full release renders
   - View-source → confirm `meta robots` is NOT `noindex` and the
     canonical URL matches

## Notes

- The placeholder release at `press/2026-05-01-press-section-launch.html`
  was shipped with the section scaffolding. It carries `noindex` and a red
  "PLACEHOLDER — NOT FOR PUBLICATION" banner. Delete its card from
  `press.html` when you publish the first real release (or sooner).
- No CloudFront Function republish is needed for new releases — the
  `/press/` prefix is already allowlisted.
- Keep `sitemap.xml` to actual indexable URLs. Do not add `_template.html`
  or noindexed placeholders to the sitemap.

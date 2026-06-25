# Sitemap and Indexing Fix: Developer Handover

> ## Status as of 25 June 2026
>
> **Done in this session (committed-ready in the working tree, not yet pushed):**
> - **P2 implemented.** New `tools/generate-sitemap.py` generates the full sitemap deterministically from the page set. Verified: identical 52-URL set, well-formed XML, board hints normalised (the 6 inconsistent board entries are now uniform), `lastmod` sourced from git.
> - **P3 implemented.** `tools/add-press-release.py` no longer string-splices the sitemap; `update_sitemap()` now delegates to the generator, and the call site regenerates *after* placeholder cleanup. `sitemap.xml` regenerated. `.github/workflows/deploy.yml` has a new `Verify sitemap.xml is in sync` step (runs `--check` before any S3 write; `fetch-depth: 0` was already set, so `lastmod` is stable in CI).
> - All four touched files verified null-byte clean, syntax/YAML valid, and the generator's `--check` passes against the committed sitemap.
>
> **Still to do (needs a human or a code session with the right access):**
> 1. **Review and push the working-tree changes** (`git add` + commit + push to `main`). Files: `tools/generate-sitemap.py` (new), `tools/add-press-release.py`, `sitemap.xml`, `.github/workflows/deploy.yml`. Pushing triggers the deploy workflow.
> 2. **P1: publish the CloudFront Function** (section 3 below). This is the single highest-impact item and is a manual AWS console step because the IAM deploy user has no CloudFront Function permissions. Nothing in the repo can do this automatically.
> 3. **P4: re-prompt Google** in Search Console once P1 is live (resubmit sitemap, request indexing on key pages). This is a state-changing GSC action and was deliberately left for you to trigger.
>
> The reference implementation in section 3 P2 below now matches the code that was actually shipped, kept here as documentation.

---


**Site:** taraniscapital.com (static site, S3 + CloudFront)
**Prepared:** 25 June 2026
**Author:** SEO health check follow-up
**Audience:** the developer or Claude Code session that maintains this repo
**Related docs:** `docs/GSC-INDEXING-PLAN-2026-04-24.md`, `docs/PROPOSED-REDIRECTS.md`, `infra/cloudfront-url-rewrite.js`, `.github/workflows/deploy.yml`, `tools/add-press-release.py`

---

## 1. Important correction up front

The 90-day Search Console check raised a flag that the sitemap "only lists 52 URLs while 313 URLs earn impressions, and Search Console reports 0 indexed against the sitemap." On inspecting the actual code, the headline framing was wrong in one key respect, and it matters:

**The sitemap file is not missing any live pages.** `sitemap.xml` contains exactly 52 URLs, and the site has exactly 52 live, publishable HTML pages. It is a clean 1:1 match. Nothing real is absent, and nothing stale is present. The generator inside `tools/add-press-release.py` has kept it in sync.

So this is not a "sitemap is incomplete" job. The real situation is two separate things:

1. **A live-versus-repo drift on the redirect layer.** The 313 ranking URLs are overwhelmingly legacy WordPress URLs (old news-article slugs, `/page/N/` pagination, `/tag/`, `/author/`, `/team_member/`, `/board_members/`) left over from the WordPress to static migration. The repo already contains a CloudFront Function that 301-redirects all of these (`infra/cloudfront-url-rewrite.js`), but that function does not appear to be published to the live distribution. Evidence: `https://taraniscapital.com/page/2/` returns a hard 404, whereas the repo function would 301 it to `/insights`. So the code that fixes this exists but is not live.

2. **The sitemap is maintained by fragile string-splicing,** which works today but will drift the moment the page set changes in a way the regex did not anticipate. That is a latent risk, not a current fault.

"Fix the sitemap situation" therefore breaks down into: get the redirect function live (highest impact), harden how the sitemap is generated (removes future risk), then re-prompt Google. None of the fix involves adding the legacy URLs to the sitemap. You never list a URL you intend to redirect or 404.

---

## 2. Root cause, in one paragraph

The site was migrated from WordPress to a hand-coded static site on S3 and CloudFront. Google still holds hundreds of old WordPress URLs in its index and keeps re-crawling them from backlinks and its own history. The migration plan (`GSC-INDEXING-PLAN-2026-04-24.md`) correctly called for 301 redirects, and those redirects were written into `infra/cloudfront-url-rewrite.js`. Because the IAM deploy user has no CloudFront Function permissions, publishing that function is a manual console step, and it looks like the latest version (the one with the pagination and catch-all blocks) was never published. Until it is, the legacy URLs keep returning 404 or nothing, Google keeps them in limbo, they keep generating impressions with no clicks, and the sitemap's "indexed" count stays misleading.

---

## 3. The fix, in priority order

### P1. Publish the CloudFront Function (highest impact, no code change needed)

The correct code already sits in `infra/cloudfront-url-rewrite.js`. It handles, in order: `/page/N/` and `/insights/page/N/` to `/insights`, `/tag/*` and `/author/*`, `/team_member/*` and `/board_members/*` slug-preserving redirects, WP infra paths, truncated LinkedIn paste fragments via the catch-all, trailing-slash collapsing, and the clean-URL to `.html` rewrite.

What code needs to do: nothing new. What a human needs to do is publish it. The steps are documented in the file header and in `GSC-INDEXING-PLAN-2026-04-24.md`:

1. AWS Console, CloudFront, Functions, `url-rewrite`.
2. Diff the live function body against `infra/cloudfront-url-rewrite.js`. If the live clean-URL rewrite block at the bottom differs, keep the live version of that block and merge in only the redirect block above it.
3. Paste, Save, Publish, attach to distribution `E18AUIFBUGMXSB`.
4. Wait about 5 minutes for propagation.

Verify with curl. These must return `301` with the right `location`, not `404`:

```bash
curl -sI https://taraniscapital.com/page/2/                 | grep -i -E 'HTTP|location'
curl -sI https://taraniscapital.com/insights/page/17/       | grep -i -E 'HTTP|location'
curl -sI https://taraniscapital.com/tag/fintech/            | grep -i -E 'HTTP|location'
curl -sI https://taraniscapital.com/team_member/mark-walker | grep -i -E 'HTTP|location'
```

Expected: `HTTP/2 301` and `location: https://taraniscapital.com/insights` (or the mapped target).

If you prefer to grant automation rights instead of pasting by hand: add `cloudfront:CreateFunction`, `cloudfront:UpdateFunction`, `cloudfront:PublishFunction`, and `cloudfront:DescribeFunction` to the deploy IAM user, then a future workflow step can publish `infra/cloudfront-url-rewrite.js` on push. That is optional and a larger change.

### P2. Replace the string-splice sitemap maintenance with a deterministic generator

Today `tools/add-press-release.py` edits `sitemap.xml` with a chain of regex substitutions (`update_sitemap`, lines 377 to 433). It works, but every edit is a fresh chance to corrupt the file, and only the press tool knows how to touch the sitemap. If a board member or fund page is added by any other route, the sitemap is not updated.

What code needs to do: generate the whole sitemap from the file system on every build, deterministically. Walk the repo, apply exactly the same exclusion rules the deploy already uses, map each `.html` file to its clean URL, and write `sitemap.xml`.

The discovery rules must stay identical to three existing places, or you reintroduce drift:

- the `aws s3 sync` exclude list in `.github/workflows/deploy.yml` (what actually ships),
- the `EXACT_ALLOW` and `PREFIX_ALLOW` lists in `infra/cloudfront-url-rewrite.js` (what is reachable),
- the URL form (extensionless, no trailing slash, `index.html` maps to `/`).

Reference implementation, drop in as `tools/generate-sitemap.py`:

```python
#!/usr/bin/env python3
"""Generate sitemap.xml deterministically from the published page set.

Source of truth for what is "published" mirrors the S3 sync exclude list in
.github/workflows/deploy.yml. Keep the two in sync.
"""
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOST = "https://taraniscapital.com"

# Directories never published to the apex bucket (mirror deploy.yml --exclude).
EXCLUDE_DIRS = {
    ".git", ".github", ".claude", "docs", "infra", "secrets",
    "Wp-content", "Board of Advisors", "Documents", "TC Logos",
    "Team Images", "Tmp Images folder", "subdomains", "content",
    "css", "js", "images", "fonts",
}
EXCLUDE_FILES = {"404.html", "_template.html"}

# Per-section crawl hints. Default applies to anything unlisted.
HINTS = {
    "/":               ("weekly",  "1.0"),
    "_root_page":      ("monthly", "0.8"),
    "/insights":       ("weekly",  "0.8"),
    "/press":          ("weekly",  "0.7"),
    "press/":          ("yearly",  "0.6"),
    "team/":           ("monthly", "0.6"),
    "board/":          ("monthly", "0.6"),
    "partners/":       ("monthly", "0.6"),
    "_default":        ("monthly", "0.5"),
}

def git_lastmod(path: Path) -> str:
    """Last commit date for a file, falling back to mtime, then today."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=REPO, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).date().isoformat()
    except Exception:
        return date.today().isoformat()

def url_for(rel: str) -> str:
    if rel == "index.html":
        return HOST + "/"
    return HOST + "/" + rel[: -len(".html")]

def hints_for(rel: str):
    if rel == "index.html":
        return HINTS["/"]
    clean = "/" + rel[: -len(".html")]
    if clean in HINTS:
        return HINTS[clean]
    if "/" in rel:                       # inside a section folder
        return HINTS.get(rel.split("/")[0] + "/", HINTS["_default"])
    return HINTS["_root_page"]           # top-level page like /who-we-are

def discover():
    pages = []
    for path in REPO.rglob("*.html"):
        rel_parts = path.relative_to(REPO).parts
        if any(part in EXCLUDE_DIRS for part in rel_parts[:-1]):
            continue
        if rel_parts[0] in EXCLUDE_DIRS:
            continue
        if path.name in EXCLUDE_FILES:
            continue
        rel = "/".join(rel_parts)
        pages.append(rel)
    pages.sort(key=lambda r: ("" if r == "index.html" else r))
    return pages

def build():
    rows = []
    for rel in discover():
        cf, pr = hints_for(rel)
        rows.append(
            "  <url>\n"
            f"    <loc>{url_for(rel)}</loc>\n"
            f"    <lastmod>{git_lastmod(REPO / rel)}</lastmod>\n"
            f"    <changefreq>{cf}</changefreq>\n"
            f"    <priority>{pr}</priority>\n"
            "  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    (REPO / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"sitemap.xml written with {len(rows)} URLs")

if __name__ == "__main__":
    build()
```

This makes the sitemap a pure function of the committed page set. No more partial edits, no placeholder leftovers, accurate `lastmod` from git history.

### P3. Wire the generator in, and retire the string-splice

Two edits:

1. In `tools/add-press-release.py`, replace the body of `update_sitemap(meta)` with a single call that shells out to, or imports and runs, `generate-sitemap.py`. The press tool still stages `sitemap.xml` in its git add, it just stops hand-editing it. Delete the regex block once the generator is proven.

2. In `.github/workflows/deploy.yml`, add a step that runs the generator before the `aws s3 sync`, and fail the build if it produces a diff that was not committed. That keeps the committed sitemap honest:

```yaml
      - name: Generate and verify sitemap
        run: |
          python3 tools/generate-sitemap.py
          if ! git diff --quiet -- sitemap.xml; then
            echo "::error::sitemap.xml is stale. Run tools/generate-sitemap.py and commit."
            git --no-pager diff -- sitemap.xml
            exit 1
          fi
```

Put this step before the sync block, after checkout and Python setup.

### P4. Re-prompt Google once redirects are live

Order matters. Do P1 first, confirm the curl checks pass, then:

1. In Search Console, Sitemaps, remove and re-add `https://taraniscapital.com/sitemap.xml` so it is re-fetched. A fresh `lastmod` from P2 helps here.
2. Use URL Inspection, Request Indexing, on the handful of pages you most want re-crawled (homepage, `/insights`, `/our-funds`, any new board or team profiles).
3. Leave the legacy URLs alone. They will fall out of the index on their own once they consistently return 301. Do not use the Removals tool for them; a 301 is the clean signal.

The "0 indexed against this sitemap" number in Search Console is a lagging, often unreliable per-sitemap counter. Judge success by the Pages report and by live curl behaviour, not by that field.

### P5. Stop the drift at the source (optional but recommended)

Right now the published page set is defined in three places that must agree by hand: the deploy exclude list, the CloudFront allowlists, and the sitemap discovery rules. Consider a single `pages.json` or `pages.txt` manifest that all three read from. That is a larger refactor and is not required to fix today's problem, but it is the durable answer to "why did the sitemap drift again."

---

## 4. Acceptance criteria

The job is done when all of the following hold:

- `curl -sI https://taraniscapital.com/page/2/` returns `301` to `/insights`, and the other P1 curl checks pass.
- `python3 tools/generate-sitemap.py` runs clean and produces a `sitemap.xml` byte-identical to the committed one (no diff).
- `tools/add-press-release.py` no longer contains regex string-splicing of the sitemap, and adding a test press release still results in a correct sitemap.
- The deploy workflow fails if `sitemap.xml` is out of date.
- In Search Console, the sitemap shows as successfully fetched with the full live URL count, and over the following weeks the count of legacy URLs in the Pages report trends down.

---

## 5. What not to do

Do not add legacy WordPress URLs, pagination, or the old news slugs to the sitemap to "get them indexed." They are being deliberately retired. Listing a URL you are redirecting sends Google a contradictory signal and slows the cleanup. The sitemap should contain only the 52-or-so live, canonical, 200-status pages, which is exactly what it contains today.

---

*Scope note: this entire analysis used only the taraniscapital.com Search Console property and this repository. No other site or property was touched.*

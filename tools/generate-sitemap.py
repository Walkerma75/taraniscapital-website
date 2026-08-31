#!/usr/bin/env python3
"""Generate sitemap.xml deterministically from the published page set.

The sitemap becomes a pure function of the committed HTML pages, so it can
never drift out of sync with the site. This replaces the old hand-edited /
regex-spliced approach that lived in tools/add-press-release.py.

Discovery rules (which files count as "published") MUST stay in sync with:
  - the `aws s3 sync ... --exclude` list in .github/workflows/deploy.yml
  - the EXACT_ALLOW / PREFIX_ALLOW lists in infra/cloudfront-url-rewrite.js

URL form: clean URLs, no .html, no trailing slash; index.html maps to "/".
lastmod: the file's last git commit date, falling back to mtime, then today.
         A file with uncommitted changes reports today, because that is the
         date it will carry once the commit lands.
         For a stable value in CI, check out with fetch-depth: 0 (full history).

--check compares the committed sitemap against a fresh render. A difference in
<lastmod> values alone warns and passes, since the dates a page carries depend
on when its commit lands and cannot be known before it does. Any other
difference -- a URL added, removed or renamed, or a changed crawl hint --
still fails.

Usage:
  python3 tools/generate-sitemap.py            # write sitemap.xml
  python3 tools/generate-sitemap.py --check     # exit 1 if the URL set is stale
"""
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HOST = "https://taraniscapital.com"
SITEMAP = REPO / "sitemap.xml"

# Directories never published to the apex bucket. Mirror deploy.yml --exclude.
EXCLUDE_DIRS = {
    ".git", ".github", ".claude", "docs", "infra", "secrets",
    "Wp-content", "Board of Advisors", "Documents", "TC Logos",
    "Team Images", "Tmp Images folder", "subdomains", "content",
    "css", "js", "images", "fonts",
}
EXCLUDE_FILES = {"404.html", "_template.html"}

# Per-page crawl hints, by exact clean path.
EXACT_HINTS = {
    "/":                 ("weekly",  "1.0"),
    "/who-we-are":       ("monthly", "0.8"),
    "/our-approach":     ("monthly", "0.8"),
    "/our-funds":        ("monthly", "0.8"),
    "/insights":         ("daily",   "0.7"),
    "/press":            ("monthly", "0.7"),
    "/contact":          ("monthly", "0.6"),
    "/fintech":          ("monthly", "0.7"),
    "/datacentres":      ("monthly", "0.7"),
    "/property":         ("monthly", "0.7"),
    "/disruptive-tech":  ("monthly", "0.7"),
    "/biotech":          ("monthly", "0.7"),
    "/privacy-policy":   ("yearly",  "0.3"),
    "/cookie-policy":    ("yearly",  "0.3"),
}
# Hints by top-level section folder.
SECTION_HINTS = {
    "press":    ("yearly",  "0.6"),
    "team":     ("monthly", "0.6"),
    "board":    ("monthly", "0.6"),
    "partners": ("monthly", "0.6"),
}
DEFAULT_HINT = ("monthly", "0.5")   # any unlisted top-level page

# Deterministic section ordering for a clean, readable file.
SECTION_ORDER = {
    "_root_index": 0, "_root_page": 1,
    "press": 2, "team": 3, "board": 4, "partners": 5,
}


def dirty_paths() -> set:
    """Repo-relative paths with uncommitted changes (modified, staged, untracked).

    Queried once for the whole repo, not once per page: a per-file
    `git status` costs about as much as the per-file `git log` below, and
    would roughly double the generator's runtime for no extra information.

    `-z` gives NUL-separated records with no path quoting, so paths
    containing spaces or non-ASCII need no unescaping.
    """
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "-z"],
            cwd=REPO, capture_output=True, text=True, check=True,
        ).stdout
    except Exception:
        return set()

    paths, fields, i = set(), out.split("\0"), 0
    while i < len(fields):
        entry, i = fields[i], i + 1
        if len(entry) < 4:
            continue
        paths.add(entry[3:])
        # A rename/copy record is followed by its source path in the next field.
        if entry[0] in ("R", "C") and i < len(fields):
            paths.add(fields[i])
            i += 1
    return paths


def git_lastmod(rel: str, dirty: frozenset = frozenset()) -> str:
    # An uncommitted file will carry today's date once the commit lands, so
    # report that rather than the previous commit's date. Writing the stale
    # date is what made every press-release publish fail the --check guard on
    # its first deploy: press.html is always modified-but-uncommitted at the
    # moment the generator runs. See HANDOVER-CW018.
    if rel in dirty:
        return date.today().isoformat()
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=REPO, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    try:
        return datetime.fromtimestamp(
            (REPO / rel).stat().st_mtime, timezone.utc
        ).date().isoformat()
    except Exception:
        return date.today().isoformat()


def clean_url(rel: str) -> str:
    if rel == "index.html":
        return "/"
    return "/" + rel[: -len(".html")]


def hints_for(rel: str):
    path = clean_url(rel)
    if path in EXACT_HINTS:
        return EXACT_HINTS[path]
    if "/" in rel:
        return SECTION_HINTS.get(rel.split("/")[0], DEFAULT_HINT)
    return DEFAULT_HINT


def sort_key(rel: str):
    if rel == "index.html":
        return (SECTION_ORDER["_root_index"], "")
    if "/" in rel:
        sec = rel.split("/")[0]
        return (SECTION_ORDER.get(sec, 9), clean_url(rel))
    return (SECTION_ORDER["_root_page"], clean_url(rel))


def discover():
    pages = []
    for path in REPO.rglob("*.html"):
        parts = path.relative_to(REPO).parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if path.name in EXCLUDE_FILES:
            continue
        pages.append("/".join(parts))
    pages.sort(key=sort_key)
    return pages


def render() -> str:
    rows = []
    dirty = frozenset(dirty_paths())
    for rel in discover():
        cf, pr = hints_for(rel)
        rows.append(
            "  <url>\n"
            f"    <loc>{HOST}{clean_url(rel)}</loc>\n"
            f"    <lastmod>{git_lastmod(rel, dirty)}</lastmod>\n"
            f"    <changefreq>{cf}</changefreq>\n"
            f"    <priority>{pr}</priority>\n"
            "  </url>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )


def blank_lastmod(xml: str) -> str:
    """The sitemap with every <lastmod> value replaced by a fixed placeholder.

    Two sitemaps that match once blanked have the same URL set and the same
    crawl hints, and differ only in dates.
    """
    return re.sub(r"<lastmod>[^<]*</lastmod>", "<lastmod>-</lastmod>", xml)


def lastmod_by_loc(xml: str) -> dict:
    return dict(
        re.findall(
            r"<loc>([^<]*)</loc>\s*<lastmod>([^<]*)</lastmod>", xml
        )
    )


def main():
    xml = render()
    if "--check" in sys.argv:
        current = SITEMAP.read_text(encoding="utf-8") if SITEMAP.exists() else ""
        if current != xml:
            # A <lastmod>-only difference is cosmetic for SEO and cannot be
            # avoided when the committed sitemap is generated before the
            # commit that dates its own pages. Warn, name the URLs, and let
            # the deploy proceed. Anything else -- a URL added, removed or
            # renamed, or a changed changefreq/priority -- still blocks.
            if blank_lastmod(current) == blank_lastmod(xml):
                was, now = lastmod_by_loc(current), lastmod_by_loc(xml)
                drifted = [k for k in now if k in was and was[k] != now[k]]
                sys.stderr.write(
                    f"warning: sitemap.xml has stale <lastmod> dates on "
                    f"{len(drifted)} URL(s). The URL set is correct, so this "
                    f"does not block the deploy. Run "
                    f"`python3 tools/generate-sitemap.py` to refresh them.\n"
                )
                for loc in drifted[:10]:
                    sys.stderr.write(f"  {loc}: {was[loc]} -> {now[loc]}\n")
                if len(drifted) > 10:
                    sys.stderr.write(f"  ... and {len(drifted) - 10} more\n")
                print("sitemap.xml URL set is up to date.")
                return
            sys.stderr.write(
                "sitemap.xml is stale. Run `python3 tools/generate-sitemap.py` "
                "and commit the result.\n"
            )
            sys.exit(1)
        print("sitemap.xml is up to date.")
        return
    SITEMAP.write_text(xml, encoding="utf-8")
    print(f"sitemap.xml written with {xml.count('<loc>')} URLs")


if __name__ == "__main__":
    main()

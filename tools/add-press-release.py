#!/usr/bin/env python3
"""
add-press-release.py - Generate a Taranis Capital press release page.

Usage:
    python tools/add-press-release.py content/press/<slug>.md
    python tools/add-press-release.py --publish-due   # scheduled releases (CI)
    python tools/add-press-release.py --list-due

A source whose `date` is in the future is refused: it goes live by itself at
06:00 Riyadh time (03:00 UTC) on that date via the deploy workflow. Set
PRESS_NOW=YYYY-MM-DD to see what would be published on a given day.

Reads the markdown source (with YAML frontmatter), renders the release HTML
from press/_template.html, inserts a card into press.html, and updates
sitemap.xml. Idempotent - re-running for the same slug overwrites cleanly.
The placeholder release (and its listing card / sitemap entry) is removed
automatically the first time a real release is published.

See docs/ADD-PRESS-RELEASE.md for the source-file format and full workflow.
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import date as date_mod, datetime, time, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("ERROR: pyyaml is required. Run: pip install pyyaml")


def image_dimensions(path):
    """Return (width, height) for a JPEG or PNG file using only stdlib.

    Returns None if the format isn't recognised - script falls back to no
    width/height attrs. Used to set explicit dimensions on the hero image
    so the browser can reserve layout space and avoid CLS.
    """
    try:
        with open(path, "rb") as f:
            head = f.read(24)
            # PNG: signature + IHDR
            if head[:8] == b"\x89PNG\r\n\x1a\n":
                w = int.from_bytes(head[16:20], "big")
                h = int.from_bytes(head[20:24], "big")
                return w, h
            # JPEG: SOI + segments
            if head[:2] == b"\xff\xd8":
                f.seek(2)
                while True:
                    marker = f.read(2)
                    if len(marker) < 2 or marker[0] != 0xFF:
                        return None
                    length_bytes = f.read(2)
                    if len(length_bytes) < 2:
                        return None
                    length = int.from_bytes(length_bytes, "big")
                    # SOF0/1/2/3/5/6/7/9/10/11/13/14/15 - all have dimensions
                    if marker[1] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                        f.read(1)  # bit depth
                        h = int.from_bytes(f.read(2), "big")
                        w = int.from_bytes(f.read(2), "big")
                        return w, h
                    f.seek(length - 2, 1)
    except (OSError, ValueError):
        pass
    return None


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
TEMPLATE = REPO_ROOT / "press" / "_template.html"
PRESS_LISTING = REPO_ROOT / "press.html"
SITEMAP = REPO_ROOT / "sitemap.xml"
RELEASES_DIR = REPO_ROOT / "press"

PLACEHOLDER_SLUG = "2026-05-01-press-section-launch"

DEFAULT_BOILERPLATE = [
    {
        "title": "About Taranis Capital",
        "body": (
            "Taranis Capital is an investment firm deploying disciplined "
            "capital and knowledge leadership across emerging markets and "
            "high-growth sectors including fintech, biotech, datacentres, "
            "disruptive technology, and real estate."
        ),
    }
]

DEFAULT_CONTACTS = [
    {
        "title": "Taranis Capital",
        "email": "info@taraniscapital.com",
    }
]


def parse_source(md_path):
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        sys.exit(f"ERROR: {md_path} must start with a YAML frontmatter block (---)")
    parts = text.split("---", 2)
    if len(parts) < 3:
        sys.exit(f"ERROR: {md_path} frontmatter not closed with ---")
    meta = yaml.safe_load(parts[1]) or {}
    body_md = parts[2].strip()
    return meta, body_md


def human_date(iso_date):
    """Format ISO date as e.g. '27 April 2026' - cross-platform (no %-d)."""
    if isinstance(iso_date, str):
        y, m, d = iso_date.split("-")
        d_obj = date_mod(int(y), int(m), int(d))
    else:
        d_obj = iso_date
    return f"{d_obj.day} {d_obj.strftime('%B')} {d_obj.year}"


def render_body(meta, body_md):
    """Build the inner-<article> HTML from the parsed source."""
    parts = []

    # Hero image (optional)
    hero = meta.get("hero_image")
    if hero:
        alt = (meta.get("hero_alt") or "Press release illustration").strip()
        # Auto-detect dimensions to prevent layout shift on load
        dims = image_dimensions(REPO_ROOT / hero.lstrip("/"))
        size_attrs = ""
        if dims:
            size_attrs = f'\n             width="{dims[0]}" height="{dims[1]}"'
        parts.append(
            f'      <figure class="press-hero-image" style="margin:0 0 32px;">\n'
            f'        <img src="/{hero.lstrip("/")}"\n'
            f'             alt="{alt}"{size_attrs}\n'
            f'             style="width:100%;height:auto;display:block;border-radius:4px;">\n'
            f'      </figure>'
        )

    # Body blocks (paragraphs / h2 / blockquotes)
    parts.extend(render_body_blocks(body_md, (meta.get("dateline_city") or "").strip()))

    # Divider
    parts.append('      <hr class="press-divider">')

    # About boilerplate(s)
    boilerplate = meta.get("boilerplate") or DEFAULT_BOILERPLATE
    for bp in boilerplate:
        parts.append(
            f'      <div class="press-boilerplate">\n'
            f'        <h3>{bp["title"]}</h3>\n'
            f'        <p>{bp["body"].strip()}</p>\n'
            f'      </div>'
        )

    # Media contacts
    contacts = meta.get("contacts") or DEFAULT_CONTACTS
    contact_inner = []
    for c in contacts:
        lines = [f'<strong>{c["title"]}</strong>']
        if c.get("address"):
            lines.append(c["address"])
        if c.get("email"):
            lines.append(f'Email: <a href="mailto:{c["email"]}">{c["email"]}</a>')
        if c.get("phone"):
            lines.append(f'Tel: {c["phone"]}')
        if c.get("url"):
            url_label = c["url"].replace("https://", "").replace("http://", "").rstrip("/")
            lines.append(
                f'Web: <a href="{c["url"]}" target="_blank" rel="noopener noreferrer">{url_label}</a>'
            )
        contact_inner.append("        <p>\n          " + "<br>\n          ".join(lines) + "\n        </p>")
    contacts_heading = "Media Contacts" if len(contacts) > 1 else "Media Contact"
    parts.append(
        f'      <div class="press-contact">\n'
        f'        <h3>{contacts_heading}</h3>\n'
        + "\n".join(contact_inner) + "\n"
        f'      </div>'
    )

    # Backlink
    parts.append('      <p class="press-backlink"><a href="/press">&larr; All press releases</a></p>')

    return "\n\n".join(parts)


INTERNAL_HOSTS = ("taraniscapital.com", "www.taraniscapital.com")

_OL_ITEM = re.compile(r'^\d+\.\s+')
_UL_ITEM = re.compile(r'^[-*]\s+')


def _link(match):
    text, url = match.group(1), match.group(2)
    href = url.replace("&amp;", "&").replace("&", "&amp;")
    host = re.match(r'^https?://([^/?#]+)', url, flags=re.IGNORECASE)
    if host and host.group(1).lower() not in INTERNAL_HOSTS:
        return f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'
    return f'<a href="{href}">{text}</a>'


def render_inline(text):
    """Inline Markdown: **bold**, *italic* and [text](url).

    Links to taraniscapital.com (or site-relative paths) are plain <a href>;
    any other host opens in a new tab with rel="noopener". Text without any
    of these markers is returned unchanged, so older releases render exactly
    as before.
    """
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', _link, text)
    text = re.sub(r'\*\*(?=\S)(.+?)(?<=\S)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<![*\w])\*(?=\S)(.+?)(?<=\S)\*(?![*\w])', r'<em>\1</em>', text)
    return text


def is_list_block(block):
    """True when the block's first line opens a numbered or bulleted list."""
    first = block.lstrip().split("\n", 1)[0]
    return bool(_OL_ITEM.match(first) or _UL_ITEM.match(first))


def render_list(block):
    """Render a '1. ' or '- ' list block as <ol>/<ul>. Indented or unmarked
    lines continue the previous item."""
    lines = [l.strip() for l in block.strip().split("\n") if l.strip()]
    ordered = bool(_OL_ITEM.match(lines[0]))
    marker = _OL_ITEM if ordered else _UL_ITEM
    items = []
    for line in lines:
        if marker.match(line):
            items.append(marker.sub("", line, count=1))
        else:
            items[-1] += " " + line
    tag = "ol" if ordered else "ul"
    inner = "\n".join(f'        <li>{render_inline(item)}</li>' for item in items)
    return f'      <{tag}>\n{inner}\n      </{tag}>'


def render_body_blocks(body_md, dateline_city):
    """Render body markdown to a list of HTML block strings."""
    raw_blocks = re.split(r'\n\s*\n', body_md.strip())
    rendered = []
    is_first_paragraph = True

    for block in raw_blocks:
        block = block.rstrip()
        if not block:
            continue

        if block.startswith("## "):
            heading = block[3:].strip()
            rendered.append(f'      <h2>{heading}</h2>')

        elif block.startswith(">"):
            lines = []
            for line in block.split("\n"):
                if line.startswith("> "):
                    lines.append(line[2:])
                elif line.startswith(">"):
                    lines.append(line[1:].lstrip())
                else:
                    lines.append(line)
            inner = "\n".join(lines).strip()
            sub_blocks = re.split(r'\n\s*\n', inner)
            quote_body = inner
            attribution = None
            if len(sub_blocks) > 1 and re.match(r'^[\u2014\u2013-]', sub_blocks[-1].strip()):
                attribution = re.sub(r'^[\u2014\u2013-]+\s*', '', sub_blocks[-1].strip())
                quote_body = "\n\n".join(sub_blocks[:-1]).strip()
            quote_paras = [
                re.sub(r'\s+', ' ', para).strip()
                for para in re.split(r'\n\s*\n', quote_body)
                if para.strip()
            ]
            quote_paras[0] = f'&ldquo;{quote_paras[0]}'
            quote_paras[-1] = f'{quote_paras[-1]}&rdquo;'
            if len(quote_paras) > 1:
                quote_html = "\n        ".join(f'<p>{para}</p>' for para in quote_paras)
            else:
                quote_html = quote_paras[0]
            if attribution:
                rendered.append(
                    f'      <blockquote class="press-quote">\n'
                    f'        {quote_html}\n'
                    f'        <cite>&mdash; {attribution}</cite>\n'
                    f'      </blockquote>'
                )
            else:
                rendered.append(
                    f'      <blockquote class="press-quote">\n'
                    f'        {quote_html}\n'
                    f'      </blockquote>'
                )

        elif is_list_block(block):
            rendered.append(render_list(block))

        else:
            content = render_inline(re.sub(r'\s+', ' ', block).strip())
            if is_first_paragraph and dateline_city:
                rendered.append(
                    f'      <p class="press-dateline"><strong>{dateline_city}</strong> &mdash; {content}</p>'
                )
            else:
                rendered.append(f'      <p>{content}</p>')
            is_first_paragraph = False

    return rendered


def render_html(meta, body_html, *, is_template=False):
    template = TEMPLATE.read_text(encoding="utf-8")

    if not is_template:
        template = re.sub(
            r'<!--\s*\n  TARANIS CAPITAL.*?-->\n',
            "",
            template,
            count=1,
            flags=re.DOTALL,
        )

    iso_date = meta["date"]
    if not isinstance(iso_date, str):
        iso_date = iso_date.isoformat()
    h_date = human_date(iso_date)

    if meta.get("og_image"):
        og_image = meta["og_image"]
    elif meta.get("hero_image"):
        og_image = "https://taraniscapital.com/" + meta["hero_image"].lstrip("/")
    elif (REPO_ROOT / "images" / "press" / f"{meta['slug']}-share.jpg").exists():
        # Headline card from `generate-share-cards.py --press`
        og_image = f"https://taraniscapital.com/images/press/{meta['slug']}-share.jpg"
    else:
        # Branded default, not the transparent logo (which unfurls blank)
        og_image = "https://taraniscapital.com/images/share-default.jpg"

    strapline = (meta.get("strapline") or "").strip()
    strapline_block = ""
    if strapline:
        strapline_block = (
            f'      <p class="subtitle" style="font-style:italic;max-width:780px;'
            f'margin-bottom:12px;">{strapline}</p>'
        )

    noindex = '<meta name="robots" content="noindex, nofollow">' if is_template else ""

    replacements = {
        "{{HEADLINE}}": meta["headline"],
        "{{HEADLINE_SHORT}}": meta.get("headline_short") or meta["headline"],
        "{{SLUG}}": meta["slug"],
        "{{ISO_DATE}}": iso_date,
        "{{HUMAN_DATE}}": h_date,
        "{{META_DESCRIPTION}}": meta.get("meta_description") or meta.get("excerpt", ""),
        "{{OG_IMAGE}}": og_image,
        "{{STRAPLINE_BLOCK}}": strapline_block,
        "{{NOINDEX_META}}": noindex,
        "{{BODY_HTML}}": body_html,
    }

    out = template
    for token, value in replacements.items():
        out = out.replace(token, str(value))

    # Tidy: collapse blank line left where {{NOINDEX_META}} or {{STRAPLINE_BLOCK}} was empty
    out = re.sub(r'\n  \n  <meta', '\n  <meta', out)
    out = re.sub(r'\n\n      <p class="subtitle"', '\n      <p class="subtitle"', out)

    return out


def update_press_listing(meta):
    html = PRESS_LISTING.read_text(encoding="utf-8")

    # Remove placeholder card if present
    html = re.sub(
        r'\n      <!-- PLACEHOLDER.*?</article>\n',
        "",
        html,
        flags=re.DOTALL,
    )

    # Remove existing card for this slug (idempotent re-runs).
    # Tempered token (?:(?!</article>).)*? prevents the match from spanning
    # across adjacent cards if this slug appears later in the listing.
    slug = meta["slug"]
    html = re.sub(
        r'\n      <article class="press-card">(?:(?!</article>).)*?<a href="/press/'
        + re.escape(slug) + r'"(?:(?!</article>).)*?</article>\n',
        "",
        html,
        flags=re.DOTALL,
    )

    iso_date = meta["date"] if isinstance(meta["date"], str) else meta["date"].isoformat()
    h_date = human_date(iso_date)

    # Optional thumbnail using the hero image
    thumb_block = ""
    hero = meta.get("hero_image")
    if hero:
        alt = (meta.get("hero_alt") or "Press release illustration").strip()
        dims = image_dimensions(REPO_ROOT / hero.lstrip("/"))
        size_attrs = ""
        if dims:
            size_attrs = f' width="{dims[0]}" height="{dims[1]}"'
        thumb_block = (
            f'        <a href="/press/{slug}" class="press-card-thumb" aria-hidden="true" tabindex="-1">\n'
            f'          <img src="/{hero.lstrip("/")}" alt="{alt}" loading="lazy"{size_attrs}>\n'
            f'        </a>\n'
        )

    card = (
        f'      <article class="press-card">\n'
        + thumb_block +
        f'        <div class="press-card-meta">\n'
        f'          <time datetime="{iso_date}">{h_date}</time>\n'
        f'        </div>\n'
        f'        <h2 class="press-card-title">\n'
        f'          <a href="/press/{slug}">\n'
        f'            {meta["headline"]}\n'
        f'          </a>\n'
        f'        </h2>\n'
        f'        <p class="press-card-excerpt">{meta.get("excerpt", "")}</p>\n'
        f'        <a href="/press/{slug}" class="press-card-link">\n'
        f'          Read release &rarr;\n'
        f'        </a>\n'
        f'      </article>\n'
    )

    # Insert in date order (newest first), before the first card dated
    # earlier than this one, so re-rendering an older release leaves its card
    # where it was and scheduled releases slot in correctly whatever order
    # they are published in. Same-date cards keep this one on top.
    insert_at = None
    for m in re.finditer(r'\n      <article class="press-card">', html):
        card_end = html.find("</article>", m.end())
        t = re.search(r'<time datetime="([0-9-]+)"', html[m.end():card_end])
        if t and t.group(1) <= iso_date:
            insert_at = m.start() + 1
            break
    if insert_at is None:
        grid_end = re.search(r'\n    </div>\n', html[html.index('<div class="press-grid">'):])
        insert_at = html.index('<div class="press-grid">') + grid_end.start() + 1
    html = html[:insert_at] + card + "\n" + html[insert_at:]

    PRESS_LISTING.write_text(html, encoding="utf-8")


def update_sitemap(meta=None):
    """Regenerate sitemap.xml from the current published page set.

    Delegates to tools/generate-sitemap.py, which walks the repo and emits a
    complete, deterministic sitemap. This replaced the old regex string-splice
    approach so the sitemap can never drift from the actual pages.

    Call this AFTER all page files have been written or removed (in particular,
    after cleanup_placeholder_release), so the generated sitemap reflects the
    final on-disk state. The `meta` argument is accepted for backwards
    compatibility and is unused.
    """
    generator = SCRIPT_DIR / "generate-sitemap.py"
    subprocess.run([sys.executable, str(generator)], check=True)

def cleanup_placeholder_release():
    placeholder = RELEASES_DIR / f"{PLACEHOLDER_SLUG}.html"
    if placeholder.exists():
        placeholder.unlink()
        return True
    return False


# ---- Scheduled publishing ---------------------------------------------------
# A release goes live at 06:00 Riyadh time (03:00 UTC) on its `date`. Before
# then it is not rendered, listed, put in the sitemap or deployed. The deploy
# workflow runs `--publish-due` on every deploy and on a daily 03:15 UTC
# schedule, so a future-dated source only needs committing and merging.
GO_LIVE_UTC = time(3, 0, tzinfo=timezone.utc)
CONTENT_DIR = REPO_ROOT / "content" / "press"


def now_utc():
    """Current UTC time. PRESS_NOW (YYYY-MM-DD or ISO datetime, UTC) overrides
    it, for testing what the site looks like on a given day."""
    override = os.environ.get("PRESS_NOW")
    if override:
        if len(override) == 10:
            override += "T12:00:00"
        dt = datetime.fromisoformat(override)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def go_live_at(meta):
    d = meta["date"]
    if isinstance(d, str):
        d = date_mod.fromisoformat(d)
    return datetime.combine(d, GO_LIVE_UTC)


def is_due(meta, now=None):
    return (now or now_utc()) >= go_live_at(meta)


def load_source(md_path):
    meta, body_md = parse_source(md_path)
    file_slug = md_path.stem
    if meta.get("slug") and meta["slug"] != file_slug:
        print(f"WARNING: slug in frontmatter ({meta['slug']}) does not match filename ({file_slug}). Using filename.")
    meta["slug"] = file_slug
    return meta, body_md


def write_release(meta, body_md):
    """Render the release page and its listing card. Returns the page path.
    The caller regenerates the sitemap once all pages are written."""
    body_html = render_body(meta, body_md)
    html = render_html(meta, body_html, is_template=False)
    out_path = RELEASES_DIR / f"{meta['slug']}.html"
    out_path.write_text(html, encoding="utf-8")
    update_press_listing(meta)
    return out_path


def tracked_sources():
    """content/press/*.md files committed to git. Untracked drafts are never
    published automatically, even when their date has passed."""
    result = subprocess.run(
        ["git", "ls-files", "--", "content/press/*.md"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    )
    return sorted(REPO_ROOT / p for p in result.stdout.split() if p)


def publish_due():
    """Render every committed source that is due and has no page yet."""
    now = now_utc()
    published = []
    for md_path in tracked_sources():
        if (RELEASES_DIR / f"{md_path.stem}.html").exists():
            continue
        meta, body_md = load_source(md_path)
        if not is_due(meta, now):
            print(f"Scheduled: {meta['slug']} (goes live {go_live_at(meta):%Y-%m-%d %H:%M} UTC)")
            continue
        write_release(meta, body_md)
        published.append(meta["slug"])
        print(f"Published: press/{meta['slug']}.html")
    if published:
        update_sitemap()
    else:
        print("Nothing due to publish.")
    # The deploy workflow reads this list to invalidate the new pages at the CDN.
    out =os.environ.get("PRESS_PUBLISHED_FILE")
    if out:
        Path(out).write_text("".join(s + "\n" for s in published), encoding="utf-8")
    return published


def main():
    parser = argparse.ArgumentParser(description="Generate a Taranis Capital press release.")
    parser.add_argument("source", nargs="?", help="Path to content/press/<slug>.md")
    parser.add_argument(
        "--publish-due", action="store_true",
        help="Render every committed content/press source whose go-live time has "
             "passed and which has no page yet (used by the deploy workflow).",
    )
    parser.add_argument(
        "--list-due", action="store_true",
        help="Print the slug of every committed source whose go-live time has passed.",
    )
    args = parser.parse_args()

    if args.publish_due:
        publish_due()
        return
    if args.list_due:
        now = now_utc()
        for md_path in tracked_sources():
            meta, _ = parse_source(md_path)
            if is_due(meta, now):
                print(md_path.stem)
        return
    if not args.source:
        parser.error("give a source file, or --publish-due")

    md_path = Path(args.source).resolve()
    if not md_path.exists():
        sys.exit(f"ERROR: {md_path} not found")

    meta, body_md = load_source(md_path)

    if not is_due(meta):
        sys.exit(
            f"REFUSED: {meta['slug']} is dated {go_live_at(meta):%Y-%m-%d} and goes live at "
            f"06:00 Riyadh time (03:00 UTC) on that date.\n"
            f"Do not publish it by hand. Commit the source in content/press/ and merge: "
            f"the deploy workflow publishes it automatically when it falls due."
        )

    out_path = write_release(meta, body_md)
    placeholder_removed = cleanup_placeholder_release()
    # Regenerate the sitemap last, so it reflects the final on-disk page set
    # (new release added, placeholder removed).
    update_sitemap(meta)

    print(f"Generated: {out_path.relative_to(REPO_ROOT)}")
    print(f"Updated:   press.html, sitemap.xml")
    if placeholder_removed:
        print(f"Removed:   press/{PLACEHOLDER_SLUG}.html (and its listing card / sitemap entry)")
    print()
    print("Stage with:")
    rel_md = md_path.relative_to(REPO_ROOT) if str(md_path).startswith(str(REPO_ROOT)) else md_path
    files_to_add = [str(out_path.relative_to(REPO_ROOT)), "press.html", "sitemap.xml", str(rel_md)]
    if meta.get("hero_image"):
        files_to_add.append(meta["hero_image"])
    print(f"  git add {' '.join(files_to_add)}")
    if placeholder_removed:
        print(f"  git rm press/{PLACEHOLDER_SLUG}.html")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
add-press-release.py - Generate a Taranis Capital press release page.

Usage:
    python tools/add-press-release.py content/press/<slug>.md

Reads the markdown source (with YAML frontmatter), renders the release HTML
from press/_template.html, inserts a card into press.html, and updates
sitemap.xml. Idempotent - re-running for the same slug overwrites cleanly.
The placeholder release (and its listing card / sitemap entry) is removed
automatically the first time a real release is published.

See docs/ADD-PRESS-RELEASE.md for the source-file format and full workflow.
"""

import argparse
import re
import sys
from datetime import date as date_mod
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
            "Taranis Capital is a Dubai-based investment firm licensed by the "
            "Dubai International Financial Centre (DIFC) and regulated by the "
            "Dubai Financial Services Authority. The firm deploys disciplined "
            "capital and knowledge leadership across emerging markets and "
            "high-growth sectors including fintech, biotech, datacentres, "
            "disruptive technology, and real estate."
        ),
    }
]

DEFAULT_CONTACTS = [
    {
        "title": "Taranis Capital",
        "address": "Level 02, Innovation One, Dubai International Financial Centre (DIFC), Dubai, United Arab Emirates",
        "email": "info@taraniscapital.com",
        "phone": "+971 (0) 44 573232",
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
            quote_html = quote_body.replace("\n\n", "</p>\n        <p>").replace("\n", " ")
            if attribution:
                rendered.append(
                    f'      <blockquote class="press-quote">\n'
                    f'        &ldquo;{quote_html}&rdquo;\n'
                    f'        <cite>&mdash; {attribution}</cite>\n'
                    f'      </blockquote>'
                )
            else:
                rendered.append(
                    f'      <blockquote class="press-quote">\n'
                    f'        &ldquo;{quote_html}&rdquo;\n'
                    f'      </blockquote>'
                )

        else:
            content = re.sub(r'\s+', ' ', block).strip()
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
    else:
        og_image = "https://taraniscapital.com/images/logo-gold.png"

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

    # Remove existing card for this slug (idempotent re-runs)
    slug = meta["slug"]
    html = re.sub(
        r'\n      <article class="press-card">[^<]*<div class="press-card-meta">.*?<a href="/press/'
        + re.escape(slug) + r'".*?</article>\n',
        "",
        html,
        flags=re.DOTALL,
    )

    iso_date = meta["date"] if isinstance(meta["date"], str) else meta["date"].isoformat()
    h_date = human_date(iso_date)
    card = (
        f'      <article class="press-card">\n'
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

    html = re.sub(
        r'(    <div class="press-grid">\n)',
        r'\1\n' + card,
        html,
        count=1,
    )

    PRESS_LISTING.write_text(html, encoding="utf-8")


def update_sitemap(meta):
    sm = SITEMAP.read_text(encoding="utf-8")
    today = date_mod.today().isoformat()
    iso_date = meta["date"] if isinstance(meta["date"], str) else meta["date"].isoformat()
    slug = meta["slug"]
    new_url = f"https://taraniscapital.com/press/{slug}"

    # Remove placeholder URL if present
    sm = re.sub(
        r'  <url>\s*<loc>https://taraniscapital\.com/press/'
        + re.escape(PLACEHOLDER_SLUG) + r'</loc>.*?</url>\n',
        "",
        sm,
        flags=re.DOTALL,
    )

    # Replace stale "press releases" comment that mentioned the placeholder
    sm = re.sub(
        r'  <!-- Press releases \(individual release URLs.*?placeholder.*?\) -->',
        '  <!-- Press releases -->',
        sm,
        flags=re.DOTALL,
    )

    # Bump /press lastmod to today
    sm = re.sub(
        r'(<loc>https://taraniscapital\.com/press</loc>\s*<lastmod>)\d{4}-\d{2}-\d{2}',
        rf'\g<1>{today}',
        sm,
    )

    # Remove existing entry for this slug
    sm = re.sub(
        r'  <url>\s*<loc>' + re.escape(new_url) + r'</loc>.*?</url>\n',
        "",
        sm,
        flags=re.DOTALL,
    )

    new_entry = (
        f'  <url>\n'
        f'    <loc>{new_url}</loc>\n'
        f'    <lastmod>{iso_date}</lastmod>\n'
        f'    <changefreq>yearly</changefreq>\n'
        f'    <priority>0.6</priority>\n'
        f'  </url>\n'
    )

    sm = re.sub(
        r'(<url>\s*<loc>https://taraniscapital\.com/press</loc>.*?</url>\n)',
        r'\1' + new_entry,
        sm,
        count=1,
        flags=re.DOTALL,
    )

    SITEMAP.write_text(sm, encoding="utf-8")


def cleanup_placeholder_release():
    placeholder = RELEASES_DIR / f"{PLACEHOLDER_SLUG}.html"
    if placeholder.exists():
        placeholder.unlink()
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Generate a Taranis Capital press release.")
    parser.add_argument("source", help="Path to content/press/<slug>.md")
    args = parser.parse_args()

    md_path = Path(args.source).resolve()
    if not md_path.exists():
        sys.exit(f"ERROR: {md_path} not found")

    meta, body_md = parse_source(md_path)

    file_slug = md_path.stem
    if meta.get("slug") and meta["slug"] != file_slug:
        print(f"WARNING: slug in frontmatter ({meta['slug']}) does not match filename ({file_slug}). Using filename.")
    meta["slug"] = file_slug

    body_html = render_body(meta, body_md)
    html = render_html(meta, body_html, is_template=False)

    out_path = RELEASES_DIR / f"{meta['slug']}.html"
    out_path.write_text(html, encoding="utf-8")

    update_press_listing(meta)
    update_sitemap(meta)
    placeholder_removed = cleanup_placeholder_release()

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

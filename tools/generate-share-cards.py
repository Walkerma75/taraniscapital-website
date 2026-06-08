#!/usr/bin/env python3
"""
generate-share-cards.py — Open Graph share-card generator for Taranis Capital.

Creates 1200x630 branded share images (used as og:image / twitter:image) so that
sharing a team or board profile link unfurls with that person's photo, name and
title instead of the bare logo.

Run from the website repo root (or anywhere — paths are resolved relative to this
file's parent directory).

Usage:
    python tools/generate-share-cards.py            # generate cards MISSING for any team/board page
    python tools/generate-share-cards.py --all      # (re)generate every team & board card, overwrite
    python tools/generate-share-cards.py --default  # also (re)generate the sitewide default card
    python tools/generate-share-cards.py --check     # list team/board pages with no card / logo og:image (exit 1 if any)

Inputs  : team/*.html and board/*.html  (name from <h1 class="profile-name">, role
          from <div class="profile-role">, headshot from the profile-photo <img src>)
Outputs : images/team/<slug>-share.jpg   per team member
          images/board/<slug>-share.jpg  per board member
          images/share-default.jpg       sitewide default (with --default)

A page whose headshot file is missing/placeholder gets NO card; point its og:image
at images/share-default.jpg instead (a broken per-person card is worse than the
branded default). After generating, commit the new JPGs and point each page's
og:image at its card (see docs/ADD-SHARE-CARD.md). New team/board member => add
their page as usual, then run this script with no args; it produces only the
missing card.

Dependencies: Pillow  (pip install pillow)
"""
import os, re, sys, glob, html

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    sys.exit("Pillow is required: pip install pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1200, 630
GREEN_D = (44, 62, 53)    # --tc-green-dark  #2c3e35
GREEN_M = (58, 82, 71)    # --tc-green-mid   #3a5247
GOLD    = (201, 168, 76)  # --tc-gold        #c9a84c
WHITE   = (245, 245, 242)
GREY    = (185, 194, 189)

# Cross-platform font resolution: prefer Windows brand-ish fonts, fall back to Linux.
SERIF_BOLD_CANDIDATES = [
    "C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/timesbd.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
SERIF_CANDIDATES = [
    "C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/times.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]
SANS_CANDIDATES = [
    "C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/lato/Lato-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
SANS_BOLD_CANDIDATES = [
    "C:/Windows/Fonts/calibrib.ttf", "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/lato/Lato-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

def _first(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    raise SystemExit("No usable font found among: " + ", ".join(paths))

# Resolved lazily (see resolve_fonts) so subcommands that don't render — e.g.
# --check, used as the CI guard — require only Pillow, not installed fonts.
SERIF_BOLD = SERIF = SANS = SANS_BOLD = None

def resolve_fonts():
    """Populate the brand-font path globals on first use (idempotent)."""
    global SERIF_BOLD, SERIF, SANS, SANS_BOLD
    if SERIF_BOLD is None:
        SERIF_BOLD = _first(SERIF_BOLD_CANDIDATES)
        SERIF      = _first(SERIF_CANDIDATES)
        SANS       = _first(SANS_CANDIDATES)
        SANS_BOLD  = _first(SANS_BOLD_CANDIDATES)

def gradient():
    g = Image.new("RGB", (W, H))
    px = g.load()
    for x in range(W):
        t = x / (W - 1)
        f = t / 0.5 if t < 0.5 else (1 - t) / 0.5
        col = tuple(int(GREEN_D[i] + (GREEN_M[i] - GREEN_D[i]) * f) for i in range(3))
        for y in range(H):
            px[x, y] = col
    return g

def fit_font(draw, text, path, max_w, start, min_s):
    s = start
    while s > min_s:
        f = ImageFont.truetype(path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 2
    return ImageFont.truetype(path, min_s)

def logo_img(size):
    logo = Image.open(os.path.join(ROOT, "images/logo-gold.png")).convert("RGBA")
    logo.thumbnail((size, size), Image.LANCZOS)
    return logo

def parse_page(path):
    t = open(path, encoding="utf-8").read()
    n = re.search(r'<h1 class="profile-name">([^<]+)</h1>', t)
    r = re.search(r'<div class="profile-role">([^<]+)</div>', t)
    m = re.search(r'class="profile-photo">\s*<img src="([^"]+)"', t)
    if not (n and r and m):
        return None
    return {
        "name": html.unescape(n.group(1)).strip(),
        "role": html.unescape(r.group(1)).strip(),
        "img":  m.group(1).lstrip("/"),
        "has_og_logo": bool(re.search(r'og:image"\s+content="[^"]*logo-gold\.png"', t)),
        "has_og_default": bool(re.search(r'og:image"\s+content="[^"]*share-default\.jpg"', t)),
    }

def make_person_card(info, out_path):
    resolve_fonts()
    img = gradient()
    d = ImageDraw.Draw(img)
    def ctr(txt, font, y, fill):
        w = d.textlength(txt, font=font)
        d.text(((W - w) // 2, y), txt, font=font, fill=fill)

    # Brand logo in the top-left corner, kept clear of the centred portrait so it
    # doesn't read as an ornament sitting on top of the circle.
    logo = logo_img(48)
    img.paste(logo, (56, 48), logo)

    # Large, CENTRED headshot. The old card put a small photo on the right third,
    # which WhatsApp / iMessage crop to a centred square thumbnail that cut the
    # face off entirely. A big centred face stays recognisable in that square crop
    # and still reads well in the full 1.91:1 banner (LinkedIn, Slack, X).
    D = 410
    photo = Image.open(os.path.join(ROOT, info["img"])).convert("RGB")
    ph = ImageOps.fit(photo, (D, D), Image.LANCZOS, centering=(0.5, 0.30))
    mask = Image.new("L", (D, D), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, D, D), fill=255)
    px, py = (W - D) // 2, 72
    d.ellipse((px - 7, py - 7, px + D + 7, py + D + 7), outline=GOLD, width=6)
    img.paste(ph, (px, py), mask)

    # Name + role, centred below the photo.
    ctr(info["name"], fit_font(d, info["name"], SERIF_BOLD, W - 120, 62, 40), 500, WHITE)
    ctr(info["role"], fit_font(d, info["role"], SANS, W - 300, 30, 22), 570, GOLD)
    img.save(out_path, "JPEG", quality=90)

def make_default_card(out_path):
    resolve_fonts()
    g = gradient()
    d = ImageDraw.Draw(g)
    logo = logo_img(150)
    g.paste(logo, ((W - logo.width) // 2, 150), logo)
    wm = ImageFont.truetype(SANS_BOLD, 58)
    tag = ImageFont.truetype(SERIF, 32)
    def ctr(txt, fnt, y, fill):
        w = d.textlength(txt, font=fnt)
        d.text(((W - w) // 2, y), txt, font=fnt, fill=fill)
    ctr("TARANIS CAPITAL", wm, 330, WHITE)
    d.rectangle((W // 2 - 45, 418, W // 2 + 45, 423), fill=GOLD)
    ctr("Disciplined capital. Knowledge leadership.", tag, 450, GREY)
    g.save(out_path, "JPEG", quality=90)

def slug(page_path):
    return os.path.splitext(os.path.basename(page_path))[0]

# Profile sections that get per-person cards. Each globs <section>/*.html and
# writes images/<section>/<slug>-share.jpg.
SECTIONS = ("team", "board")

def headshot_exists(info):
    """True when the page's referenced headshot file is actually on disk. A
    missing/placeholder headshot => no per-person card; the page should fall back
    to images/share-default.jpg as its og:image (a broken card is worse)."""
    return info is not None and os.path.exists(os.path.join(ROOT, info["img"]))

def main():
    args = set(sys.argv[1:])
    do_all = "--all" in args
    do_default = "--default" in args
    do_check = "--check" in args

    def pages_in(section):
        return sorted(glob.glob(os.path.join(ROOT, section, "*.html")))

    if do_check:
        problems = []
        for section in SECTIONS:
            for p in pages_in(section):
                info = parse_page(p)
                tag = f"{section}/{slug(p)}"
                if info is None:
                    problems.append(f"{tag}: could not parse name/role/photo")
                    continue
                if info["has_og_logo"]:
                    problems.append(f"{tag}: og:image still points at logo-gold.png")
                card = os.path.join(ROOT, "images", section, slug(p) + "-share.jpg")
                if headshot_exists(info):
                    if not os.path.exists(card):
                        problems.append(f"{tag}: no share card (images/{section}/{slug(p)}-share.jpg missing)")
                elif not info["has_og_default"]:
                    # No headshot on disk: the page must fall back to the branded
                    # default rather than point at a per-person card that can't exist.
                    problems.append(f"{tag}: headshot {info['img']} missing/placeholder and og:image is not images/share-default.jpg")
        if problems:
            print("Share-card issues:")
            for x in problems:
                print("  -", x)
            sys.exit(1)
        print("All team & board pages have a card (or default fallback) and a non-logo og:image.")
        return

    made, skipped, defaulted = [], [], []
    for section in SECTIONS:
        out_dir = os.path.join(ROOT, "images", section)
        os.makedirs(out_dir, exist_ok=True)
        for p in pages_in(section):
            info = parse_page(p)
            tag = f"{section}/{slug(p)}"
            if info is None:
                print(f"  ! skipped {tag} (could not parse)")
                continue
            if not headshot_exists(info):
                defaulted.append(tag)
                print(f"  ~ {tag}: headshot missing ({info['img']}) — point og:image at images/share-default.jpg, no card")
                continue
            card = os.path.join(out_dir, slug(p) + "-share.jpg")
            if os.path.exists(card) and not do_all:
                skipped.append(tag)
                continue
            make_person_card(info, card)
            made.append(tag)
            print(f"  + images/{section}/{slug(p)}-share.jpg  ({info['name']})")

    if do_default:
        make_default_card(os.path.join(ROOT, "images", "share-default.jpg"))
        print("  + images/share-default.jpg (sitewide default)")

    print(f"\nGenerated {len(made)} card(s); {len(skipped)} already existed"
          + (" (use --all to overwrite)" if skipped else "")
          + (f"; {len(defaulted)} use the default card (missing headshot)" if defaulted else "") + ".")
    if made:
        print("Remember: set each page's og:image to its card and commit the JPG(s). See docs/ADD-SHARE-CARD.md")

if __name__ == "__main__":
    main()

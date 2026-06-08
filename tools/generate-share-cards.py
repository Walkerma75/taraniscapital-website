#!/usr/bin/env python3
"""
generate-share-cards.py — Open Graph share-card generator for Taranis Capital.

Creates 1200x630 branded share images (used as og:image / twitter:image) so that
sharing a team profile link unfurls with that person's photo, name and title
instead of the bare logo.

Run from the website repo root (or anywhere — paths are resolved relative to this
file's parent directory).

Usage:
    python tools/generate-share-cards.py            # generate cards MISSING for any team page
    python tools/generate-share-cards.py --all      # (re)generate every team card, overwrite
    python tools/generate-share-cards.py --default  # also (re)generate the sitewide default card
    python tools/generate-share-cards.py --check     # list team pages with no card / no og:image (exit 1 if any)

Inputs  : team/*.html  (name from <h1 class="profile-name">, role from
          <div class="profile-role">, headshot from the profile-photo <img src>)
Outputs : images/team/<slug>-share.jpg  per person
          images/share-default.jpg       sitewide default (with --default)

After generating, commit the new JPGs and point each page's og:image at its card
(see docs/ADD-SHARE-CARD.md). New team member => add their page as usual, then run
this script with no args; it will produce only the missing card.

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

def main():
    args = set(sys.argv[1:])
    do_all = "--all" in args
    do_default = "--default" in args
    do_check = "--check" in args

    pages = sorted(glob.glob(os.path.join(ROOT, "team", "*.html")))
    out_dir = os.path.join(ROOT, "images", "team")
    os.makedirs(out_dir, exist_ok=True)

    if do_check:
        problems = []
        for p in pages:
            info = parse_page(p)
            card = os.path.join(out_dir, slug(p) + "-share.jpg")
            if info is None:
                problems.append(f"{slug(p)}: could not parse name/role/photo")
                continue
            if not os.path.exists(card):
                problems.append(f"{slug(p)}: no share card ({slug(p)}-share.jpg missing)")
            if info["has_og_logo"]:
                problems.append(f"{slug(p)}: og:image still points at logo-gold.png")
        if problems:
            print("Share-card issues:")
            for x in problems:
                print("  -", x)
            sys.exit(1)
        print("All team pages have a share card and a non-logo og:image.")
        return

    made, skipped = [], []
    for p in pages:
        info = parse_page(p)
        if info is None:
            print(f"  ! skipped {slug(p)} (could not parse)")
            continue
        card = os.path.join(out_dir, slug(p) + "-share.jpg")
        if os.path.exists(card) and not do_all:
            skipped.append(slug(p))
            continue
        make_person_card(info, card)
        made.append(slug(p))
        print(f"  + {slug(p)}-share.jpg  ({info['name']})")

    if do_default:
        make_default_card(os.path.join(ROOT, "images", "share-default.jpg"))
        print("  + images/share-default.jpg (sitewide default)")

    print(f"\nGenerated {len(made)} card(s); {len(skipped)} already existed"
          + (" (use --all to overwrite)" if skipped else "") + ".")
    if made:
        print("Remember: set each page's og:image to its card and commit the JPG(s). See docs/ADD-SHARE-CARD.md")

if __name__ == "__main__":
    main()

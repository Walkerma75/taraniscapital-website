# Managing strategic partners

Partner cards on the main site (`who-we-are`) and the five fund subdomains are
**data-driven**. You edit one JSON file and run one script — you never hand-edit
the partner HTML. This mirrors the people-data pattern
(`taranis-people-data.json`) and the press pipeline (`docs/ADD-PRESS-RELEASE.md`).

## Files

| File | Role |
|---|---|
| `taranis-partners-data.json` | **Source of truth** — drives every partner card. |
| `Taranis-Partners-Data-Collection.xlsx` | Human-readable monitor/amend copy (Mark's editing surface). |
| `tools/build-partners.py` | Generator — renders the cards into the HTML pages. |

## The model

Every partner has a **main-site identity** (`name`, `url`, `description`) and a
set of **per-fund entries** under `funds`. A partner shows:

- on **who-we-are** when `mainSite.shown` is `true`;
- on a **fund subdomain** when `funds.<fund>.shown` is `true`.

Each fund entry MAY override `brand` (display name), `url` and `description`. A
blank/absent override falls back to the main-site value:

```
title       = funds[fund].brand       or  partner.name
link        = funds[fund].url         or  partner.url
body        = funds[fund].description or  partner.description
```

Fund keys are exactly: `fintech`, `biotech`, `datacentre`, `property`,
`disruptiveTech`. (`disruptiveTech` maps to the `subdomains/disruptive-tech/` page.)

### The Disrupts Media special case

`"isGroup": true` marks the Disrupts Media corporate card. There is **one**
"Disrupts Media" card on the main site, but a **different brand on each
subdomain**, produced purely by the per-fund overrides — no special code:

| Fund | Brand shown | Link |
|---|---|---|
| Fintech | The Fintech Times | thefintechtimes.com |
| Biotech | The Biotech Times | biotech.disruptsmedia.com |
| Datacentre | The Datatech Times | datatech.disruptsmedia.com |
| Property | Disrupts | disrupts.disruptsmedia.com |
| Disruptive Tech | Disrupts | disrupts.disruptsmedia.com |

Invariant: at most **one** Disrupts Media brand card per subdomain.

### Card order

The generator orders cards by a fixed rule (not by any field in the JSON):

> **The Disrupts Media group brand always renders first, then every other
> partner alphabetically by its displayed name/brand.**

(Per Mark's instruction, 9 Jun 2026. The `mainSite.order` values in the JSON are
now informational only.)

## How to make a change

1. Edit `taranis-partners-data.json` (add a partner, flip a `shown`, change a
   description, add a per-fund override, etc.). Keep
   `Taranis-Partners-Data-Collection.xlsx` in step as the readable copy.
2. Regenerate the pages:
   ```
   python tools/build-partners.py
   ```
   It rewrites only the region between the `<!-- PARTNERS:START -->` and
   `<!-- PARTNERS:END -->` markers on each page, prints a per-page card count,
   and ends with a `git add …` line.
3. Commit the JSON **and** every page it changed, push, open a PR, let CI deploy.

### Adding a brand-new partner

Append an object to `partners` with `slug`, `name`, `url`, `description`,
`mainSite` and a `funds` block. Set `shown: true` on whichever surfaces it
belongs to; add `brand`/`url`/`description` only where they differ from the
main-site identity. Run the generator.

### Adding a partner to a fund that has no section yet

Only the five funds above have a Strategic Partners section. If a future
subdomain needs one, add the shared partner CSS (`.partners-grid` /
`.partner-card`) and a `<section class="alt">` containing an empty
`<!-- PARTNERS:START --> … <!-- PARTNERS:END -->` marker pair, then register the
page in `SUBDOMAIN_PAGES` in `tools/build-partners.py`.

## Checking sync (CI)

```
python tools/build-partners.py --check
```

Exits non-zero if any page is out of step with the JSON (e.g. someone edited the
JSON but forgot to regenerate). Writes nothing. Useful as a CI guard.

## Source-of-truth / sync caveat

There is **no Drive copy or scheduled sync** for the partners sheet yet, unlike
people-data. Until one exists (and replicates the `xlsx-sync-guard` safety
pattern), **`taranis-partners-data.json` is hand-edited and is the source of
truth.** Do not wire up an automated partners sync before establishing the Drive
copy — see the Strategic Partners code brief, §7.

# Managing fund team cards

The team-and-adviser cards on the five fund subdomains (`fintech`, `biotech`,
`datacentre`, `property`, `disruptive-tech`) are **data-driven**. You edit one
JSON roster and run one script — you never hand-edit the team-card HTML. This
mirrors the strategic-partners pattern (`tools/build-partners.py`,
`docs/MANAGE-PARTNERS.md`).

> Scope: the **fund subdomains only**. `who-we-are.html` uses a different card
> structure (`<div class="team-role">`), is already in sync with the directory's
> top-level `role`, and is **not** touched by this tool.

## Files

| File | Role |
|---|---|
| `taranis-fund-teams.json` | **Source of truth** for the per-fund cards — which people appear, in which section, in what order, with what curated title. Hand-edited. |
| `taranis-people-data.json` | The person directory (Drive-synced). Owns **identity** — `fullName`, `profileImage.path`, and per-fund `bio` — resolved by `slug`. |
| `tools/build-people.py` | Generator — renders the cards into the subdomain HTML between the `<!-- TEAM:START -->` / `<!-- TEAM:END -->` markers. |

## The model

The roster describes each fund as an ordered list of **sections**, each an
ordered list of **members**:

```json
{
  "funds": {
    "fintech": {
      "page": "subdomains/fintech/index.html",
      "sections": [
        { "title": "Executive Team", "members": [
          { "slug": "nicholas-bingham", "title": "Founding Partner & CEO" }
        ]},
        { "title": "Board of Advisers", "members": [
          { "slug": "david-parker", "title": "Board Adviser" }
        ]}
      ]
    }
  }
}
```

Fund keys are exactly: `fintech`, `biotech`, `datacentre`, `property`,
`disruptiveTech`. (`disruptiveTech` maps to the `subdomains/disruptive-tech/`
page.)

### How a card is resolved

Each member is `{ slug, title }` plus two optional overrides. Identity resolves
from the person directory by `slug`; the roster owns the title:

```
name  = member.name  or  person.fullName
image = person.profileImage.path            (no override; the card <img> prefixes
                                             it with https://taraniscapital.com)
bio   = member.bio   or  person.funds[fund].bio
title = member.title                        (always from the roster)
alt   = the displayed name
```

- **`title`** (required) — the curated role shown on the card. The roster exists
  to own this field, because the directory's per-fund `role` values are stale and
  drive nothing.
- **`name`** (optional) — only where the card must show a name different from the
  directory `fullName`. Prefer fixing the name in the directory (via Drive); use
  an override only as a stopgap.
- **`bio`** (optional) — used where the curated card bio differs from the
  directory's per-fund bio. Two reasons this is common today:
  1. **Recurrence.** In biotech, Nicholas Bingham and Osama Bukhari each appear in
     two sections (Executive Team and Investment Committee) with different bios; a
     single `funds.biotech.bio` cannot represent both, so the second uses a `bio`
     override.
  2. **Drift.** The directory's per-fund bios have drifted from the curated site
     copy on ~31 cards (the bios, like the roles, drive nothing on the live site
     and were never kept in sync). Those cards carry the curated bio as an
     override so the site renders as written. See the source-of-truth note below.

A member whose `slug` is unknown, or who is not `assigned` to that fund in the
directory, or who has an empty `title`, fails `validate()` rather than rendering
a blank card.

## How to make a change

1. Edit `taranis-fund-teams.json` — change a title, add/remove a member, reorder a
   section, add a `name`/`bio` override, etc.
2. Regenerate the pages:
   ```
   python tools/build-people.py
   ```
   It rewrites only the region between the `<!-- TEAM:START -->` and
   `<!-- TEAM:END -->` markers on each subdomain, prints a per-page section/card
   count, and ends with a `git add …` line.
3. Commit the JSON **and** every page it changed, push, open a PR, let CI deploy.
   (Per `CLAUDE.md`, never push straight to `main`.)

### Adding a member to a fund

Append `{ "slug": "...", "title": "..." }` to the relevant section's `members`.
The `slug` must exist in `taranis-people-data.json` and be `assigned: true` for
that fund. Run the generator.

### Adding a section, or a fund that has no team markers yet

Insert a new `{ "title": ..., "members": [...] }` object in roster order. If a
**page** has no `TEAM:START/END` markers yet, add the pair by hand first:
immediately before the first `<div class="team-section-title">` and immediately
after the final team-grid `</div>`, inside the `Fund Leadership & Advisers`
section (the `<h2>` and intro paragraph stay outside the markers). The generator
refuses to run on a page with no markers.

## Checking sync (CI)

```
python tools/build-people.py --check
```

Re-renders every page in memory and exits non-zero if any is out of step with the
roster (e.g. someone edited the JSON but forgot to regenerate). Writes nothing.
This runs in `.github/workflows/deploy.yml` alongside `build-partners.py --check`
and blocks the deploy on drift.

## Source-of-truth / sync caveat

`taranis-fund-teams.json` is **hand-edited and is the source of truth** for the
per-fund cards. Identity (`fullName`, image, and non-overridden bios) still comes
from the Drive-synced `taranis-people-data.json`.

Note that the directory's `funds.<fund>.role` **and** `funds.<fund>.bio` fields
are stale — no page reads them, so they drifted from the curated site copy. This
tool deliberately does **not** read `funds.<fund>.role`, and reads
`funds.<fund>.bio` only as a fallback where the roster has no `bio` override.
Whether to back-fill those directory fields from the roster, or retire them, is a
separate decision (raise a brief); do not wire an automated directory→site sync
for titles or bios.

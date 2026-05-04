# Claude Context — Taranis Capital Website

**Purpose:** Corporate website for Taranis Capital. Static HTML/CSS/JS rebuild of the former WordPress site.
**State:** LIVE
**Owner entity:** Taranis Capital

## Tech stack

- Frontend: HTML, CSS, vanilla JS (no framework, no build step)
- Hosting: AWS S3 static website hosting in `eu-west-2` (bucket `taraniscapital.com`)
- CDN: CloudFront distribution `E18AUIFBUGMXSB` with a `url-rewrite` Function for clean URLs and 301 redirects
- DNS: AWS Route 53 hosted zone `Z0680053Y587NB8B8C9S`
- TLS: ACM certificate in `us-east-1` (wildcard `*.taraniscapital.com`)
- CI/CD: GitHub Actions — `.github/workflows/deploy.yml` runs `aws s3 sync` + `cloudfront create-invalidation` on push to `main`

## Live URL

- Primary: https://taraniscapital.com
- CloudFront direct: https://d1ete5r3431epc.cloudfront.net
- Fund subdomains: fintech / datacentre / property / disruptive-tech / biotech `.taraniscapital.com` — each with its own S3 bucket + CloudFront distribution

## Repository

- GitHub: `Walkerma75/taraniscapital-website`
- Branch: `main`
- IAM user for deploys: `taranis-deploy` (Taranis Capital AWS account)

## Deploy

1. Edit HTML/CSS/JS locally
2. `git add {files}` → `git commit -m "..."` → `git push`
3. GitHub Actions auto-runs: S3 sync + CloudFront invalidation
4. Hard-refresh the live URL

There is no build step — the site deploys as-is.

## Secrets

- AWS credentials: GitHub repo secrets (access key, secret, region)
- No `.env` on disk for this project
- Google Analytics ID `G-JLN31RRY1V` is public (embedded in HTML)

## Project files

- `PROJECT-LOG.md` — human-facing session history (primary reference)
- `TASKS.md` — project-specific task list
- `SUBDOMAIN-SETUP.md` — how to add a new subdomain (S3 + CloudFront + Route 53)
- `PROPOSED-REDIRECTS.md` — URL redirect map for old WordPress paths
- `MISSING-PROFILE-INFO.md` — outstanding team/board data
- `Taranis Website - AWS Infrastructure Summary.md` — infra overview
- `Documents/AWS-Setup-Guide.md`, `GitHub-Setup-Guide.md`, `GitHub-Actions-Setup-Guide.md` — setup references
- Brand guidance lives in `../Taranis Capital Shared/Brand/taranis-brand-SKILL.md` (Georgia headings dark green `#2C3E35`, Calibri body `#374047`)
- `Documents/Taranis-Capital-Overview.md`, `IBEM-Partnership-Overview-DRAFT.md` — content

## Do / don't

- **Do** follow the canonical workflow in `../WORKFLOW.md`
- **Do** stage files specifically (`git add contact.html`), not `git add .`
- **Do** respect the Taranis brand: Georgia for headings (dark green `#2C3E35`), Calibri body (`#374047`)
- **Do** self-merge PRs you opened once the diff is clean, CI is green, and you've verified the work — no need to wait for human review. Use `gh pr merge <n> --squash --delete-branch`. Still go via a PR (not direct push to main) so CI runs and history is reviewable.
  - Exceptions that still warrant a human OK: anything touching secrets, deletes/destructive changes, or work that depends on a manual post-merge step the user must run (e.g. CloudFront Function republish — flag it, don't merge silently). When in doubt, ask.
- **Don't** commit anything from `Board of Advisors/`, `Documents/`, `TC Logos/`, `Team Images/`, `Tmp Images folder` — these are excluded in `.gitignore`
- **Don't** use bold yellow/light-blue tables — they're off-brand
- **Don't** put `computer://` or absolute paths into HTML — use site-relative paths
- **Don't** push directly to `main` — `main` auto-deploys to production. Always go through a PR, even if you're going to merge it yourself.

## Known gotchas

- Two GitHub accounts on this machine (`Walkerma75` + `markwalker-pcs`) — Windows Credential Manager has triggered auth conflicts when pushing. If git prompts for credentials unexpectedly, confirm the git config user email matches the account with repo access.
- `Taranis-People-Data-Collection.xlsx` is **Cowork's** source of truth and is read from Google Drive, not from this repo. The xlsx checked into this repo is a periodic snapshot — never edit it locally. For data corrections, edit `taranis-people-data.json` and the affected HTML directly, and flag spreadsheet inconsistencies for the user to fix in Drive (otherwise the next Cowork sync re-applies the old state).

## Scheduled tasks

- `taranis-people-sync` (Cowork scheduled task) — runs 09:00 local on the 1st and 15th of each month. Reads `Taranis-People-Data-Collection.xlsx`, diffs against `taranis-people-data.json`, and opens a PR on branch `sync/profiles-YYYY-MM-DD` if profile fields have changed. Never commits to `main` directly. Manage from the Scheduled sidebar.

## Known outstanding

- 10 board member bios missing (see `MISSING-PROFILE-INFO.md`)
- 11 people missing LinkedIn URLs
- Sitemap now lists 51 URLs; keep it synchronised when new pages added
- Press section live with first release (Taranis × EEC Saudi data centre partnership, 27 Apr). New releases via `python tools/add-press-release.py content/press/<slug>.md` — see `docs/ADD-PRESS-RELEASE.md`.

## Last updated

4 May 2026 (press card thumbnails + 4-across grid; Cowork profile sync re-landed; xlsx source-of-truth note clarified)

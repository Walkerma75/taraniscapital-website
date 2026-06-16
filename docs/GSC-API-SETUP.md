# GSC API Setup — unattended weekly health check

This replaces the browser-driven weekly Google Search Console check with the
**Search Console API**, so the scheduled task runs unattended (no Chrome needed).

## What the API can and can't do

| Check | API? | How it's covered now |
|---|---|---|
| Sitemaps (status, last read, discovered count) | ✅ Yes | Weekly API run |
| Performance (clicks / impressions / CTR / position) | ✅ Yes | Weekly API run |
| Per-URL index status | ✅ Yes (URL Inspection) | Weekly API run inspects every sitemap URL |
| Aggregate "not indexed by reason" table | ❌ No API | Monthly browser check |
| Validation-run statuses | ❌ No API | Monthly browser check |
| Manual Actions | ❌ No API | Monthly browser check **+ Google auto-emails the owner** |
| Security Issues | ❌ No API | Monthly browser check **+ Google auto-emails the owner** |
| Core Web Vitals | ❌ No API | Monthly browser check (CrUX — no data on this site anyway) |

**Hybrid model:** the API handles the weekly run; a separate **monthly** task
(`gsc-monthly-browser-check`) opens GSC in Chrome to read the things the API
can't. Manual actions and security issues also trigger automatic email alerts
from Google to the property owner, so they're covered between browser checks.

---

## One-time setup (do this once, in your own Google account)

### 1. Create / pick a Google Cloud project and enable the API
1. Go to <https://console.cloud.google.com> and create a project (e.g.
   `taranis-gsc`) or reuse an existing one.
2. Enable the API: **APIs & Services → Library → search "Google Search Console
   API" → Enable**. (This is the *Search Console API*, not the *Indexing API*.)

### 2. Create a service account + JSON key
1. **APIs & Services → Credentials → Create credentials → Service account.**
2. Name it e.g. `gsc-weekly-check`. No project roles are needed (it gets access
   inside Search Console, not via IAM). Click **Done**.
3. Open the new service account → **Keys → Add key → Create new key → JSON →
   Create.** A `.json` file downloads. **This is a secret — treat it like a
   password.**
4. Note the service-account email — it looks like
   `gsc-weekly-check@taranis-gsc.iam.gserviceaccount.com`.

### 3. Grant the service account access in Search Console
1. Open <https://search.google.com/search-console> → select the
   **taraniscapital.com** (domain) property.
2. **Settings → Users and permissions → Add user.**
3. Paste the service-account email. Set permission to **Full**.
   - *Full is required* for the URL Inspection API. Performance + sitemaps alone
     would work with Restricted, but the per-URL index check needs Full.

> Adding a user is a permissions change on your own property — do this yourself
> in the Search Console UI. (Claude won't change access controls for you.)

### 4. Place the key file (kept out of git and S3)
Put the downloaded JSON at:

```
C:\Users\mark\Claude Cowork\Taranis Capital Website\secrets\gsc-service-account.json
```

Create the `secrets\` folder if it doesn't exist. This location is already:
- **git-ignored** — `secrets/` is in `.gitignore`, so it's never committed.
- **excluded from S3** — `deploy.yml` has `--exclude "secrets/*"`, so it can
  never be published to the public bucket even if something tried.

Do **not** rename it elsewhere into the repo root — `.json` files in the root
*are* part of the S3 allowlist and would be publishable.

### 5. (First run only) install the Python deps
The script needs two libraries. The scheduled task installs them at the start of
each run, but to test locally:

```
pip install --break-system-packages google-api-python-client google-auth
```

---

## Run it

```
cd "C:\Users\mark\Claude Cowork\Taranis Capital Website"
python tools/gsc-weekly-check.py
```

It prints the Markdown body of the PROJECT-LOG entry to the screen and also
writes `gsc-check-<date>.md` and `gsc-check-<date>.json` (both git-ignored).

Useful flags:
- `--no-inspect` — skip the per-URL inspection (sitemap + performance only; fast).
- `--key <path>` — use a key somewhere other than the default location.
- `--end-offset-days N` — end the 7-day performance window N days before today
  (default 3, to use Google's finalised data).

---

## How the scheduled tasks use this

- **`gsc-weekly-health-check`** (Mondays) — now runs `tools/gsc-weekly-check.py`,
  takes its stdout, adds the `### Session N — DATE (GSC Weekly Check — API)`
  heading + a one-line comparison to last week, and appends to
  `docs/PROJECT-LOG.md`. Fully unattended. See that task's SKILL.md.
- **`gsc-monthly-browser-check`** (monthly) — opens GSC in Chrome for Manual
  Actions, Security, Core Web Vitals and the aggregate index report. Needs
  Chrome open + the Claude in Chrome extension signed in; degrades gracefully
  and reports if the browser isn't reachable.

## Troubleshooting

- **`service-account key not found`** — the key isn't at the default path and
  `--key` / `$GSC_SA_KEY` weren't set. See step 4.
- **`403 / insufficient permission` on URL inspection** — the service account
  isn't a **Full** user on the property (step 3), or you granted access to the
  wrong property (must be the `sc-domain:` domain property).
- **`The caller does not have permission` on sitemaps/performance** — service
  account not added in Search Console at all (step 3), or wrong project / API
  not enabled (steps 1–2).
- **Performance shows zeros** — normal if the window is too recent; data lags
  2–3 days. The script already ends the window 3 days back.
- **URL Inspection quota** — 2,000/day per property; this site has ~52 URLs, so
  no risk.

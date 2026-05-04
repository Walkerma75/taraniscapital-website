# Migration Brief — Taranis Capital Website

**Project:** Taranis Capital Website
**Repo:** `Walkerma75/taraniscapital-website` (folder: `Claude Cowork/Taranis Capital Website/`)
**Risk tier:** Tier 2 (per `../PROJECTS-REGISTER.md`)
**Purpose of this document:** Instructions for the discovery pass that closes out this project's readiness for a Claude Code-driven workflow. Once complete, it is signed off on the register and the handover is done.
**Owner:** Mark Walker
**Created:** 20 April 2026

---

## Starting position

This project is further along than most — a comprehensive `CLAUDE.md`, a 65 KB `PROJECT-LOG.md`, an AWS infrastructure summary, a subdomain runbook (`SUBDOMAIN-SETUP.md`), a redirects map, and a tasks file all exist. So unlike a cold-start discovery, this brief is mostly about:

1. Pulling the existing knowledge into one inventory document
2. Closing the specific gaps that aren't documented anywhere yet
3. Producing the signed-off `MIGRATION-INVENTORY.md` artefact

We are not rebuilding what's already there. We are formalising it.

---

## What is already known (summary — do not re-document)

- **Tech stack:** static HTML/CSS/JS, no build step
- **AWS account:** `TaranisCapital`, region `eu-west-2`
- **Services:** S3 bucket `taraniscapital.com`, CloudFront distribution `E18AUIFBUGMXSB`, Route 53 zone `Z0680053Y587NB8B8C9S`, ACM cert in `us-east-1` (wildcard `*.taraniscapital.com`), CloudFront Function `url-rewrite`
- **Git:** `Walkerma75/taraniscapital-website`, branch `main`
- **CI/CD:** GitHub Actions `.github/workflows/deploy.yml` — S3 sync + CloudFront invalidation on push to `main`
- **Deploy IAM user:** `taranis-deploy`
- **Secrets:** AWS keys in GitHub repo secrets; no `.env` on disk
- **Domain registrar:** e& (nic.ae), migrated from Funkygrafix 7 Apr 2026
- **Subdomains:** fintech, datacentre, property, disruptive-tech, biotech — each has its own S3 bucket and CloudFront distribution
- **Analytics:** GA4 `G-JLN31RRY1V`
- **Contact form:** MailerLite (external, no AWS involvement)
- **Brand:** Georgia headings `#2C3E35`, Calibri body `#374047`
- **Known gotchas:** two GitHub accounts on the machine cause credential conflicts; weekly auto-sync task currently pointed at the wrong folder

Everything above is already captured in the existing project files. It gets carried forward verbatim into the inventory.

---

## Status update — Bucket A closed in Cowork conversation, 20 April 2026

A pre-flight Q&A with Mark closed every gap that didn't require a console or CLI lookup. Recording the answers here so the Claude Code session picks up only what it can't answer from conversation.

### Confirmed

- Repo `Walkerma75/taraniscapital-website` is **public**
- No collaborators, deploy keys, or GitHub Apps beyond the built-ins — just Mark
- No branch protection on `main` today (will be added — see inline fixes below)
- AWS `TaranisCapital` account: Mark is the only human; `taranis-deploy` is the only other IAM principal
- AWS root MFA: **on**
- Cloudflare is **not** in the DNS path for `taraniscapital.com` or any fund subdomain — all Route 53
- Third-party integrations: **MailerLite** (contact form), **GA4** (`G-JLN31RRY1V`), **RSS feeds** on Insights page (client-side, public, no auth). No other integrations.
- Nothing currently monitoring the site — outage detection is reactive (see inline fixes)

### Inline fixes already completed

Recorded in the inventory's "Changes made during discovery" block at handover.

| Date | Change | Why | How to revert |
|---|---|---|---|
| 2026-04-20 | Enabled MFA on `Walkerma75` GitHub account | Public repo + AWS deploy keys in secrets — credential compromise would grant direct AWS write access | GitHub → Settings → Password and authentication → Two-factor authentication → Disable (not recommended) |
| 2026-04-20 | Enabled MFA on Taranis MailerLite account | Holds GDPR-relevant contact form submissions | MailerLite → Account settings → Two-factor authentication → Disable (not recommended) |

### Inline fixes to perform during the Claude Code session

All three are on the allowed-inline list in `../PROJECTS-REGISTER.md` Discovery policy. Each gets logged in the "Changes made during discovery" block with revert instructions.

1. **Enable branch protection on `main`** for `Walkerma75/taraniscapital-website`: require linear history, disallow force-push, disallow branch deletion. No required reviews (solo repo), no required status checks (no pre-deploy CI yet).
2. **Turn on S3 bucket versioning** on `taraniscapital.com` and on each of the five fund-subdomain buckets, if not already on. Gives a rollback path for a botched `aws s3 sync`.
3. **Add an uptime monitor** for `https://taraniscapital.com`. Preferred: a Route 53 health check with an SNS topic → email to `mark@taraniscapital.com` (keeps monitoring inside AWS, ~£0.40/month). Second choice: free-tier UptimeRobot. Mark to choose during the session.

### Follow-ups — not fixed inline, scheduled with deadlines

Added to this project's `TASKS.md` during handover.

- **Rotate the `taranis-deploy` AWS access key** — deadline **4 May 2026** (two weeks). Sequence: generate new key → update GitHub repo secret → trigger a test deploy → deactivate the old key once confirmed. Not done inline because the rotation ritual needs a clean, unhurried window.

### Still open — Bucket B (quick console checks)

Resolve these during the Claude Code session with AWS Console + AWS CLI access:

- S3 bucket versioning status (before the inline fix is applied — record the current state)
- CloudTrail enabled/disabled in the `TaranisCapital` account; if disabled, evaluate cost vs benefit
- ACM certificate ARN and expiry date for `*.taraniscapital.com` (`us-east-1`), plus any per-subdomain certs
- CloudFront distribution IDs, S3 bucket names, and ACM cert ARNs for each of the five fund subdomains (fintech, datacentre, property, disruptive-tech, biotech)
- `taraniscapital.com` renewal date at e& (nic.ae) and whether auto-renewal is enabled
- Who has access to the GA4 property (`G-JLN31RRY1V`) and any connected services (Search Console, Ads)
- Exact permissions policy (JSON) attached to the `taranis-deploy` IAM user — least-privilege review

### Still open — Bucket C (scripted via CLI)

- Git history grep for leaked secrets: `AKIA`, `aws_access`, `aws_secret`, `BEGIN RSA`, `BEGIN OPENSSH`, `private_key`. Scope is the full history of all branches, not just the working tree.
- Full subdomain resource enumeration via `aws` CLI — build a flat table of bucket → distribution → ACM cert → Route 53 record set

---

## Gaps to close during this pass

These are the items that either aren't documented anywhere yet, or are marked `TBD` in `../ACCOUNTS.md` or `../PROJECTS-REGISTER.md`. Each must be resolved before handover sign-off.

> **Note:** The status update above supersedes the list below where they overlap. The list remains as the full working set for Claude Code to tick off during execution.

### Git and access

These are the items that either aren't documented anywhere yet, or are marked `TBD` in `../ACCOUNTS.md` or `../PROJECTS-REGISTER.md`. Each must be resolved before handover sign-off.

### Git and access

- [ ] Confirm repository visibility: public or private? (`ACCOUNTS.md` has it as "public? — confirm")
- [ ] List every user/team/app with push access to `Walkerma75/taraniscapital-website`
- [ ] Confirm branch protection on `main` (required reviews? required status checks?)
- [ ] Confirm MFA is enforced on the `Walkerma75` GitHub account
- [ ] Note any outside collaborators or deploy keys

### AWS and IAM

- [ ] Document every IAM user with access to the `TaranisCapital` AWS account, not just `taranis-deploy`
- [ ] Confirm the exact permissions policy attached to `taranis-deploy` (least-privilege review)
- [ ] Confirm whether root account MFA is enabled
- [ ] Confirm whether CloudTrail is on in this account (audit trail if something changes)
- [ ] Enumerate the five fund subdomain distributions explicitly: bucket names, CloudFront IDs, ACM cert ARNs, Route 53 record sets. The `SUBDOMAIN-SETUP.md` is a runbook, not an inventory — we need the actual IDs listed

### Secrets

- [ ] Confirm the exact GitHub repo secret names in use (e.g. `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`)
- [ ] Confirm the last rotation date of the AWS deploy key; record the next planned rotation date
- [ ] Confirm no secrets exist elsewhere (search the repo for `aws_access`, `secret`, `key`; confirm `.env` is in `.gitignore` and not committed historically)

### CI/CD and rollback

- [ ] Confirm the exact trigger: push to `main` only? Any manual dispatch?
- [ ] Document the rollback procedure: what does "undo a bad deploy" look like on this stack? (git revert + push? S3 object versioning? CloudFront cache rollback?)
- [ ] Confirm whether S3 bucket versioning is enabled — this is the backstop for a botched sync
- [ ] Confirm who else, if anyone, can approve/trigger a deploy

### DNS and certificates

- [ ] Note the ACM certificate ARN and expiry date for `*.taraniscapital.com` in `us-east-1`
- [ ] Note expiry for any per-subdomain certs (if they're separate)
- [ ] Confirm the domain auto-renewal setting at e& (nic.ae) — is it on, and when does `taraniscapital.com` itself expire?
- [ ] Confirm Cloudflare is NOT in the DNS path for this domain (ACCOUNTS.md flags this as TBD globally)

### Third-party integrations

- [ ] MailerLite: which account holds it, where does the form submission endpoint live in the HTML, where is the API key (if any) stored?
- [ ] Insights RSS feeds: list the source URLs, confirm they're all public and not dependent on any auth
- [ ] Google Analytics: who has access to the GA4 property, any other connected services (Search Console, Ads)?

### Monitoring and alerting

- [ ] Is anything watching the site? (CloudWatch, UptimeRobot, StatusCake, Route 53 health checks, none?) If nothing, flag it as a gap to close *after* handover
- [ ] If something is watching, where do alerts go — email, SMS, Slack?

### Backup and DR

- [ ] S3 versioning: on or off? If off, note it as a risk
- [ ] Where else does the site source live? (It's in git, so git is the authoritative backup — confirm)
- [ ] Restore procedure: what does "rebuild the site from nothing" look like? Rough step list
- [ ] Last time the restore procedure was tested (even dry-run)

### Tribal knowledge

- [ ] Expand the `CLAUDE.md` "Known gotchas" section — add anything that has tripped you up in the last three months that hasn't been written down yet
- [ ] Note any decisions that look odd without context (e.g. why the CloudFront Function exists, why certain URLs are redirected the way they are — some of this is in `PROPOSED-REDIRECTS.md` already)

---

## Expected output

A new file at the repo root:

**`MIGRATION-INVENTORY.md`**

It follows the twelve-section template in `../PROJECTS-REGISTER.md` (Identity, Git, Cloud, Secrets, CI/CD, DNS, Third-party, Database, Monitoring, Backup/DR, Tribal knowledge, Known risks). For this project, the Database section will be "N/A — no database, flat-file static site".

The inventory should be a document that a new engineer could read in 20 minutes and, on its basis, take over the project with no further briefing. If it doesn't pass that test, it isn't done.

---

## Execution plan

Run this in a Claude Code session rooted at this folder. Do each step in order; don't let Claude skip ahead.

1. **Read the existing context.** `CLAUDE.md`, `PROJECT-LOG.md`, `Taranis Website - AWS Infrastructure Summary.md`, `SUBDOMAIN-SETUP.md`, `PROPOSED-REDIRECTS.md`, `TASKS.md`, `MISSING-PROFILE-INFO.md`, and the two Setup Guides under `Documents/`. No changes yet.

2. **Grep for secrets.** Search the repo history (not just the working tree) for obvious leaks: `aws_access`, `secret`, `private_key`, `AKIA`, `BEGIN RSA`. If any hit, stop and escalate to Mark before continuing.

3. **Draft the inventory skeleton.** Create `MIGRATION-INVENTORY.md` with the twelve section headings, pre-populated with the "already known" items above. Mark every unknown as `[CONFIRM]` or `[TBD]`.

4. **Close the gaps.** Work through the checklist in this brief section by section. For each item:
   - If Claude can determine it from the repo or from AWS CLI calls against the existing account, it does so and fills the inventory
   - If the discovery finds something that qualifies as a low-risk fix under the register's Discovery policy (e.g. S3 versioning off, `.gitignore` missing an entry, no branch protection on `main`), Claude fixes it inline and records the change in the "Changes made during discovery" block at the top of `MIGRATION-INVENTORY.md`
   - Anything outside the low-risk list gets logged as a follow-up in `TASKS.md`, not acted on
   - If it requires Mark to look at a console or confirm something externally, it stays `[CONFIRM]` and gets added to a "Questions for Mark" block at the top of the inventory
5. **Review questions with Mark.** Produce a short list of only the unresolved questions. Mark answers them in one pass, Claude updates the inventory.

6. **Cross-check against the register.** Open `../PROJECTS-REGISTER.md` and confirm every relevant "Gaps to resolve" item that touches this project has been closed. Strike them through in that file.

7. **Sign-off.** Mark reviews the finished inventory end-to-end. On approval:
   - Update the Taranis Capital Website row in `../PROJECTS-REGISTER.md`: Discovery status → **Discovery complete**, Inventory doc → link to `MIGRATION-INVENTORY.md`
   - Tick the handover checklist at the bottom of the register for this project
   - Move handover status to **Migrated** (this project is already using a Claude Code workflow; the inventory is confirmation, not a migration)

---

## Constraints

- **Low-risk fixes allowed inline.** Follow the Discovery policy in `../PROJECTS-REGISTER.md` — additive, reversible hygiene items (S3 versioning, `.gitignore` additions, branch protection on an unprotected repo, uptime checks, auto-renewal) get fixed during discovery and recorded. Anything that rotates secrets, changes IAM, touches DNS/CDN, alters CI/CD pipelines, or touches the running site goes into `TASKS.md` as a follow-up.
- **Don't commit secrets.** Everything in this brief is structure and metadata, not credentials. Keep it that way.
- **Respect the existing `.gitignore`.** `Board of Advisors/`, `Documents/`, `TC Logos/`, `Team Images/`, `Tmp Images folder/` remain untouched.
- **Keep the inventory in UK English.** Match the tone of the existing `CLAUDE.md`.

---

## When this is done

The register row reads:

> Discovery status: **Discovery complete** · Inventory doc: `MIGRATION-INVENTORY.md` · Handover status: **Migrated**

And we have a template proven against a real project. The next brief — Pro-curo Website (pro-curo.com) — reuses this structure with the Azure-specific variations.

# Migration Inventory — Taranis Capital Website

**Project:** Taranis Capital Website
**Owner:** Mark Walker
**Risk tier:** Tier 2
**State:** LIVE
**Inventory created:** 20 April 2026
**Signed off:** _pending Mark's review_

This document is the single-read handover for the Taranis Capital Website. A new engineer should be able to read it in 20 minutes and take over the project with no further briefing. Where items below read `[TBD]`, they remain open pending Mark's answer — see "Questions for Mark" block.

---

## Changes made during discovery

Every additive, reversible hygiene fix applied during the discovery pass is logged here. Follow the Discovery policy in `../../PROJECTS-REGISTER.md` — rotations, IAM/DNS/CloudFront/CI changes are follow-ups, not inline.

| Date | Change | Why | How to revert |
|---|---|---|---|
| 2026-04-20 | Enabled MFA on `Walkerma75` GitHub account | Public repo + AWS deploy keys in repo secrets — credential compromise would grant direct AWS write access | GitHub → Settings → Password and authentication → Two-factor authentication → Disable |
| 2026-04-20 | Enabled MFA on Taranis MailerLite account | Holds GDPR-relevant contact form submissions | MailerLite → Account settings → Two-factor authentication → Disable |
| 2026-04-20 | Created branch protection ruleset "main protection" on `Walkerma75/taraniscapital-website` (target narrowed to `main` only; require linear history, block force-pushes, block deletions; no required reviews, no required status checks) | Solo public repo had no branch protection; protects history integrity and prevents accidental main deletion/rewrite | Repo → Settings → Rules → Rulesets → "main protection" → Delete |
| 2026-04-20 | Enabled S3 bucket versioning on all 6 website buckets (`taraniscapital.com`, `fintech.taraniscapital.com`, `datacentre.taraniscapital.com`, `property.taraniscapital.com`, `disruptive-tech.taraniscapital.com`, `biotech.taraniscapital.com`) | Previously off on all six; gives object-level rollback for a botched `aws s3 sync --delete` | `aws s3api put-bucket-versioning --bucket <name> --versioning-configuration Status=Suspended` per bucket |
| 2026-04-20 | Added `Tmp Images folder/` to `.gitignore` | CLAUDE.md claimed the folder was already ignored but it wasn't. Folder exists on disk, is currently untracked — defensive addition to prevent accidental future commits | Revert the single-line edit in `.gitignore` |
| 2026-04-20 | Created Route 53 health check + CloudWatch alarm + SNS uptime alert on `taraniscapital.com` → `mark@taraniscapital.com`. Health check is **HTTP on port 80** (not HTTPS) because Route 53 health checkers max out at TLS 1.2 and the main CloudFront distribution requires TLSv1.3_2025 — TLS handshake fails before SNI. Port 80 returns a 301 redirect to HTTPS which Route 53 treats as healthy (3xx). See TLS alignment follow-up in `TASKS.md`. Health check ID: `31616e98-9cd2-41e1-bcf8-29df51dd1d63` · CloudWatch alarm (`us-east-1`): `taraniscapital-com-uptime` · SNS topic ARN: `arn:aws:sns:us-east-1:571600836975:taraniscapital-uptime-alerts` · Email subscription confirmed by Mark. | No monitoring on the live site; outage detection was previously reactive | Route 53 → Health checks → delete `taraniscapital.com-uptime`; CloudWatch → Alarms (us-east-1) → delete `taraniscapital-com-uptime`; SNS → Topics (us-east-1) → delete `taraniscapital-uptime-alerts` (removes subscription in the same action) |
| 2026-04-20 | **Enabled CloudTrail** — created `taranis-capital-account-trail` (multi-region, home region `us-east-1`, management events only, log file validation on, SSE-KMS disabled to avoid KMS key monthly cost). ARN: `arn:aws:cloudtrail:us-east-1:571600836975:trail/taranis-capital-account-trail`. Log S3 bucket: `aws-cloudtrail-logs-571600836975-f495d2a6`. Cost: £0/month — first management-events trail is free. | Account had no audit trail. Cheap insurance if anything unexpected happens across this account (website + Dataroom + any future project). | CloudTrail → Trails → `taranis-capital-account-trail` → Delete. Also manually delete the logs S3 bucket if no longer needed. |
| 2026-04-20 | **Rollback drill performed** — commit `760ba1a` reverted (`7860865`), pushed, deploy succeeded, site stayed live; then revert-of-revert (`af7f867`) pushed, deploy succeeded, content restored. Rollback procedure verified end-to-end. | Tier 2 Handover checklist requires it; had never been tested before. | Rollback drill is ephemeral — no persistent change to revert. Git log retains the two revert commits as historical record. |
| 2026-04-20 | **Moved all tracked `.md` internal docs from repo root into `docs/` subfolder and added `--exclude "*.md"` + `--exclude "docs/*"` to `.github/workflows/deploy.yml`**. Affected files: `MIGRATION-INVENTORY.md`, `MISSING-PROFILE-INFO.md`, `PROFILE-UPDATE-REPORT-2026-04-09.md`, `PROJECT-LOG.md`, `PROPOSED-REDIRECTS.md`, `SUBDOMAIN-SETUP.md`, `TASKS.md`, `Taranis Website - AWS Infrastructure Summary.md`. | **Active data exposure** discovered mid-discovery: the workflow was syncing the repo root to the public S3 bucket with only specific folder excludes, so all `.md` docs at root were being served publicly at `https://taraniscapital.com/<file>.md`. PROJECT-LOG.md (65 KB) had been publicly readable since whenever it was added; MIGRATION-INVENTORY.md became exposed today when first committed. Fix combines the S3 sync `--delete` flag (which removes the no-longer-present root docs from the bucket on the next push) with structural and belt-and-braces workflow excludes to prevent regression. This is a workflow-file change that the Discovery policy would normally require as a follow-up, but an active public exposure justifies the inline deviation. | `git mv docs/*.md .` to move docs back to root (breaks privacy again — don't do this without first reverting the workflow exclude); then revert the `.github/workflows/deploy.yml` edit to remove the `*.md` and `docs/*` excludes. |
| 2026-04-20 | **Created new IAM user `taranis-website-deploy`** with custom policy `TaranisWebsiteDeployPolicy` scoped to only: `s3:ListBucket`/`GetBucketLocation` on the 6 website buckets, `s3:GetObject`/`PutObject`/`DeleteObject` on their contents, and `cloudfront:CreateInvalidation` on the 6 distribution ARNs. Rotated GitHub repo secrets `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` to the new user's key. Verified with an empty-commit deploy — full workflow passed end-to-end. Old `taranis-deploy` access key deactivated (step in progress; delete scheduled 2026-04-21 after 24h). | Original `taranis-deploy` was substantially over-permissive (S3/Route53/CloudFront FullAccess + ECR + ECS inline) and shared with the Taranis Dataroom project. New user is website-only, least-privilege, and isolates website CI from any Dataroom compromise. Supersedes the 4 May rotation and least-privilege follow-ups. | IAM → Users → `taranis-website-deploy` → delete access key + user; IAM → Policies → `TaranisWebsiteDeployPolicy` → delete; GitHub → repo secrets → revert `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` to the old `taranis-deploy` key values. (Reverting assumes the old key is still active or has been reactivated.) |

---

## Questions for Mark

Items that can't be resolved from the repo, the brief, `../../ACCOUNTS.md`, or CLI calls under `taranis-deploy`'s permission scope. Resolve in one pass, then update the inventory.

1. ~~**Branch protection scope.**~~ — **Answered** (Mark 2026-04-20): ruleset target narrowed to `main` only.
2. ~~**CloudTrail.** Is any trail configured in the `TaranisCapital` account?~~ — **None configured** (Mark confirmed 2026-04-20). Follow-up logged in `TASKS.md` to evaluate enabling a single free trail.
3. ~~**`taranis-deploy` policy JSON.** Paste the full JSON of every attached and inline policy.~~ — **Answered** (Mark confirmed 2026-04-20, via console): 4 AWS-managed policies + 1 customer-inline. See Section 3. Finding: over-permissive. Follow-up logged in `TASKS.md`. The `ECSDeployPolicy` inline JSON still needs capture for full least-privilege review.
4. ~~**Full IAM user list.**~~ — **Answered** (Mark confirmed 2026-04-20): 2 users total, `taranis-deploy` and `github-deploy`. Both without MFA, no console sign-in.
5. ~~**`github-deploy` — what is it?**~~ — **Answered** (Mark 2026-04-20): used by the Taranis Dataroom project. Full workflow mapping to be captured during Dataroom discovery.
6. ~~**Route 53 health check IDs.**~~ — **Answered** (inline, 2026-04-20). See the "Changes made during discovery" table.
7. ~~**e& (nic.ae) renewal.**~~ — **Answered** (Mark 2026-04-20): expires **February 2027**, auto-renewal **ON**.
8. ~~**GA4 access.**~~ — **Answered** (Mark 2026-04-20): `mark@taraniscapital.com` only; Google Search Console linked (same account); Google Ads not linked.
9. ~~**Local deploy key co-tenant.**~~ — **Resolved 2026-04-20**: old `taranis-deploy` access key deactivated today. Local CLI now rejects the old profile (verified end-to-end). Follow-up in `TASKS.md` covers creating a separate `mark-admin` IAM user for local work when Mark wants it.
10. ~~**MailerLite account holder / contract.**~~ — **Answered** (Mark 2026-04-20): owner `mark@taraniscapital.com`. **Free tier** (up to 500 subscribers). Currently 1 subscriber — re-review before crossing the 500 limit.
11. ~~**IAM least-privilege tightening timing.**~~ — **Resolved 2026-04-20**: paired with the rotation, done today. `taranis-website-deploy` created with `TaranisWebsiteDeployPolicy` (6 buckets + 6 distributions, no wildcards). Old `taranis-deploy` still used by Dataroom — cleaned up during Dataroom's own discovery pass.

---

## 1. Identity

- **Project name:** Taranis Capital Website
- **Owner (technical & business):** Mark Walker (`mark@taraniscapital.com`)
- **Live URLs:**
  - Primary: `https://taraniscapital.com` (and `www.taraniscapital.com`)
  - CloudFront direct: `https://d1ete5r3431epc.cloudfront.net`
  - Fund subdomains: `fintech.` · `datacentre.` · `property.` · `disruptive-tech.` · `biotech.taraniscapital.com`
- **State:** LIVE
- **Purpose:** Corporate website for Taranis Capital. Static HTML/CSS/JS rebuild of the former WordPress site.

---

## 2. Git

- **Account / repo:** `Walkerma75/taraniscapital-website` on GitHub (personal account)
- **Visibility:** **public** (confirmed 2026-04-20)
- **Default branch:** `main`
- **Other active branches:** none
- **Submodules / LFS / vendor repos:** none
- **Collaborators / deploy keys / GitHub Apps:** none beyond built-ins (solo — confirmed 2026-04-20)
- **MFA on `Walkerma75`:** ON (enabled 2026-04-20, this discovery pass)
- **Branch protection:** ruleset "main protection" created 2026-04-20. Require linear history · block force-pushes · block deletions · no required reviews (solo repo) · no required status checks (no pre-deploy CI yet). Scope: `[CONFIRM — see Questions for Mark]`.
- **Git config on this machine:**
  - Local (this repo): `user.name = Mark Walker`, `user.email = mark@taraniscapital.com`
  - Global: `user.name = Walkerma75`, `user.email = mark@taraniscapital.com`
  - Remote: `https://github.com/Walkerma75/taraniscapital-website.git`
- **Credential gotcha:** two GitHub accounts on this machine (`Walkerma75` + `markwalker-pcs`). Windows Credential Manager has previously triggered auth prompts on push. If git prompts for credentials, confirm `user.email` matches the account with push access.

---

## 3. Cloud

- **AWS account:** `TaranisCapital`, account ID **571600836975**
- **Primary region:** `eu-west-2` (London) · CloudFront-attached ACM certs in `us-east-1`
- **Root MFA:** ON (confirmed in Bucket A pre-flight, 2026-04-20)
- **IAM users in the account (confirmed by Mark 2026-04-20, via console):** **2 users**, both without MFA and without console sign-in:
  - `taranis-deploy` — CI/CD principal, last activity 2026-04-20
  - `github-deploy` — used by the separate **Taranis Dataroom** project (confirmed by Mark 2026-04-20). Specific workflow/repo mapping to be fully captured during the Dataroom discovery pass. Last activity 2026-04-20.
- **`taranis-deploy` attached policies (confirmed by Mark 2026-04-20, via console):**
  - `AmazonEC2ContainerRegistryPowerUser` (AWS managed)
  - `AmazonRoute53FullAccess` (AWS managed)
  - `AmazonS3FullAccess` (AWS managed)
  - `CloudFrontFullAccess` (AWS managed)
  - `ECSDeployPolicy` (customer inline — JSON `[TBD]`)

  **Finding: substantially over-permissive for a website deployer.** The ECR + ECS policies indicate `taranis-deploy` is also the CI user for the Taranis Dataroom project. `AmazonS3FullAccess` grants write on every bucket in the account (including `taranis-dataroom-documents-prod`). Recommended to split into two per-project users and scope resources — logged as follow-up in `TASKS.md`.
- **CloudTrail:** **enabled during discovery 2026-04-20** — trail `taranis-capital-account-trail` (multi-region, management events, log file validation on, SSE-KMS disabled). Logs to S3 bucket `aws-cloudtrail-logs-571600836975-f495d2a6`. ARN `arn:aws:cloudtrail:us-east-1:571600836975:trail/taranis-capital-account-trail`. Cost £0/month — first trail for management events is free.
- **Scope note:** this account also hosts the separate **Taranis Dataroom** project (bucket `taranis-dataroom-documents-prod`, ALB `taranis-dataroom-alb-…`, DNS `dataroom.taraniscapital.com`, ACM cert `e8bb602c-…` in `eu-west-2`). All of that is out of scope for this inventory — it belongs to its own Tier 3 project.

### 3a. Resource inventory

**S3 buckets** (all `eu-west-2`, all static-website-hosted, all public-read via bucket policy, all versioning **enabled 2026-04-20**):

| Bucket | Created | Website endpoint |
|---|---|---|
| `taraniscapital.com` | 2026-04-03 | `taraniscapital.com.s3-website.eu-west-2.amazonaws.com` |
| `fintech.taraniscapital.com` | 2026-04-07 | `fintech.taraniscapital.com.s3-website.eu-west-2.amazonaws.com` |
| `datacentre.taraniscapital.com` | 2026-04-07 | `datacentre.taraniscapital.com.s3-website.eu-west-2.amazonaws.com` |
| `property.taraniscapital.com` | 2026-04-07 | `property.taraniscapital.com.s3-website.eu-west-2.amazonaws.com` |
| `disruptive-tech.taraniscapital.com` | 2026-04-07 | `disruptive-tech.taraniscapital.com.s3-website.eu-west-2.amazonaws.com` |
| `biotech.taraniscapital.com` | 2026-04-10 | `biotech.taraniscapital.com.s3-website.eu-west-2.amazonaws.com` |

**CloudFront distributions** (all origin = S3 website endpoint, `http-only`):

| Alias | Distribution ID | CloudFront domain | ACM cert | TLS min | Price class | WAF | CloudFront Function | Logging |
|---|---|---|---|---|---|---|---|---|
| `taraniscapital.com` + `www` | `E18AUIFBUGMXSB` | `d1ete5r3431epc.cloudfront.net` | `ea95d60f-…` | TLSv1.3_2025 | All | `CreatedByCloudFront-018b0599` (`90c5ca10-4b11-48fc-850d-b5e0436baf18`) | `url-rewrite` (viewer-request) | off |
| `fintech.` | `E260FGTXCVORQ6` | `d2ykbvfjmg586t.cloudfront.net` | `fa9c7dad-…` | TLSv1.2_2021 | 100 | — | — | off |
| `datacentre.` | `E3EJUFMMNZLO3V` | `dg42m0l7gq950.cloudfront.net` | `fa9c7dad-…` | TLSv1.2_2021 | 100 | — | — | off |
| `property.` | `E2H8IQKJ8LPQ01` | `d3bmdcmsydjb0z.cloudfront.net` | `fa9c7dad-…` | TLSv1.2_2021 | 100 | — | — | off |
| `disruptive-tech.` | `E98QNGA1O9AI0` | `d2us9lvkabbd5i.cloudfront.net` | `fa9c7dad-…` | TLSv1.2_2021 | 100 | — | — | off |
| `biotech.` | `ESMIKURPBA41W` | `d12nozf5efsxkp.cloudfront.net` | `fa9c7dad-…` | TLSv1.2_2021 | 100 | — | — | off |

**CloudFront Function:**
- `url-rewrite` — appends `.html` to extensionless paths, handles old WordPress 301 redirects. Attached only to the main distribution (viewer-request).

**ACM certificates** (both in `us-east-1` for CloudFront attachment, status ISSUED, InUse true):

| ARN (short) | Primary DomainName | SANs | Issued | Expires | Used by |
|---|---|---|---|---|---|
| `ea95d60f-9080-414b-8aa3-d719ea803477` | `taraniscapital.com` | `taraniscapital.com`, `*.taraniscapital.com` | 2026-04-03 | **2026-10-18** | Main distribution |
| `fa9c7dad-94a1-4cb1-8a9e-c8e5ee64b60d` | `*.taraniscapital.com` | `*.taraniscapital.com`, `taraniscapital.com` | 2026-04-07 | **2026-10-22** | All 5 subdomain distributions |

Both certs renew automatically through ACM (RenewalEligibility = ELIGIBLE). The two certs overlap — either could in principle cover both the apex and all subdomains; not clear why two exist (low-priority review item).

**Route 53 hosted zone** `Z0680053Y587NB8B8C9S` (`taraniscapital.com.`, 16 record sets):

| Name | Type | Target | Purpose |
|---|---|---|---|
| `taraniscapital.com.` | A alias | `d1ete5r3431epc.cloudfront.net.` | Main apex |
| `www.taraniscapital.com.` | CNAME | `d1ete5r3431epc.cloudfront.net` | www redirect |
| `biotech.taraniscapital.com.` | A alias | `d12nozf5efsxkp.cloudfront.net.` | Biotech subdomain |
| `datacentre.taraniscapital.com.` | CNAME | `dg42m0l7gq950.cloudfront.net` | Datacentre subdomain |
| `disruptive-tech.taraniscapital.com.` | CNAME | `d2us9lvkabbd5i.cloudfront.net` | Disruptive Tech subdomain |
| `fintech.taraniscapital.com.` | CNAME | `d2ykbvfjmg586t.cloudfront.net` | Fintech subdomain |
| `property.taraniscapital.com.` | CNAME | `d3bmdcmsydjb0z.cloudfront.net` | Property subdomain |
| `taraniscapital.com.` | MX | `1 smtp.google.com` | Google Workspace |
| `taraniscapital.com.` | TXT | `v=spf1 include:_spf.google.com ~all` | Google Workspace SPF |
| `google._domainkey.taraniscapital.com.` | TXT | DKIM key | Google Workspace DKIM |
| `don4dbspoe7p.taraniscapital.com.` | CNAME | `gv-n4ffp6d7utjxrn.dv.googlehosted.com` | Google Workspace domain verification |
| `_181332ddf920a7b0e3d7fe913806e02a.taraniscapital.com.` | CNAME | ACM validation target | ACM cert validation |
| `_4e9c0106bf0bbe7ff6451b774be39d41.dataroom.…` | CNAME | ACM validation target | ACM validation (Dataroom project) |
| `dataroom.taraniscapital.com.` | A alias | `taranis-dataroom-alb-…eu-west-2.elb.amazonaws.com.` | Dataroom project (not in scope) |
| `taraniscapital.com.` | NS, SOA | AWS default NS | Zone administration |

---

## 4. Secrets

- **Storage:** GitHub repo secrets on `Walkerma75/taraniscapital-website`
- **Secret names and purpose:**

  | Name | Purpose |
  |---|---|
  | `AWS_ACCESS_KEY_ID` | Access key ID of `taranis-deploy` |
  | `AWS_SECRET_ACCESS_KEY` | Secret key of `taranis-deploy` |
  | `AWS_REGION` | `eu-west-2` |
  | `S3_BUCKET` | `taraniscapital.com` (main bucket only; subdomain bucket names are hardcoded in the workflow) |
  | `CLOUDFRONT_DISTRIBUTION_ID` | `E18AUIFBUGMXSB` (main only; subdomain IDs are hardcoded) |

- **Rotation:** never rotated since CI/CD was set up. **Next rotation: 2026-05-04** — logged as a follow-up in `TASKS.md`.
- **Who has access:** only Mark (no collaborators; repo is solo).
- **`.env` files on disk:** none (repo has never had one).
- **Git history scan (2026-04-20):** searched all branches/history for `AKIA`, `aws_access`, `aws_secret`, `BEGIN RSA`, `BEGIN OPENSSH`, `private_key` — **zero hits**.
- **Local-machine co-tenant:** the `taranis-deploy` access key is also stored in `~/.aws/credentials` on Mark's working machine (as `[default]`, `[disruptsmedia]`, and `[TaranisCapital]` profiles — all the same credential). This means the CI deploy key has two points of exposure. See Questions for Mark item 8.
- **Other secret stores:** none. No Secrets Manager, no Parameter Store, no Key Vault, no 1Password entry tracked.

---

## 5. CI / CD

- **Pipeline file:** `.github/workflows/deploy.yml`
- **Trigger:** `push` on branch `main` only. No `workflow_dispatch`, no PR triggers, no schedule. (Manual re-deploy = push any commit, or re-run the failed/latest workflow run from the Actions tab.)
- **Runner:** `ubuntu-latest` · `actions/checkout@v4` · `aws-actions/configure-aws-credentials@v4`
- **Steps (in order):**
  1. Checkout code
  2. Configure AWS credentials from repo secrets
  3. `aws s3 sync` main site → `s3://taraniscapital.com/` (excludes `.git/*`, `.github/*`, `.gitignore`, `Wp-content/*`, `Board of Advisors/*`, `Documents/*`, `TC Logos/*`, `Team Images/*`, `subdomains/*`)
  4. `aws s3 sync` each of 5 fund subdomain directories (`subdomains/<name>/`) to its own bucket
  5. `aws cloudfront create-invalidation --paths "/*"` on all 6 distributions
- **Who can approve/trigger:** Mark, as the only user with push access to `main`. Branch protection (2026-04-20) blocks force-push and deletion but doesn't require review (solo repo).
- **Rollback procedure:**
  1. **Preferred:** `git revert <bad-sha>` → `git push origin main` → Actions re-syncs, invalidates
  2. **Object-level:** S3 versioning (enabled 2026-04-20) lets you restore previous file versions via `aws s3api list-object-versions` + `copy-object`
  3. **CloudFront:** no cache rollback — only invalidation. Subsequent push overwrites.
- **Last rollback tested:** **2026-04-20** (discovery pass). `git revert 760ba1a` → pushed → CI deploy succeeded with site still serving (HTTP 200) → `git revert` of that revert → pushed → content restored. Two commits in `git log` (`7860865`, `af7f867`) document the drill. Procedure verified end-to-end.

---

## 6. DNS

- **Hostnames managed:**
  - `taraniscapital.com` (apex) + `www.`
  - `fintech.`, `datacentre.`, `property.`, `disruptive-tech.`, `biotech.taraniscapital.com`
  - Email-support: MX, SPF, DKIM, Google Workspace verification records on apex
  - `dataroom.taraniscapital.com` — **not owned by this project** (separate Taranis Dataroom project)
- **Registrar:** e& (nic.ae), migrated from Funkygrafix on **2026-04-07**
- **DNS provider:** AWS Route 53, zone `Z0680053Y587NB8B8C9S`
- **Cloudflare:** not in the DNS path (confirmed 2026-04-20)
- **Domain expiry:** **February 2027** (confirmed by Mark 2026-04-20) · **Auto-renewal: ON**
- **Certificate issuer:** Amazon ACM (both certs issued by Amazon)
- **Certificate expiry:** main 2026-10-18; subdomain wildcard 2026-10-22. Both renew automatically via ACM DNS validation.

---

## 7. Third-party integrations

- **MailerLite** — contact form handler
  - Form `action`: `https://assets.mailerlite.com/jsonp/2240915/forms/183664557068125464/subscribe`
  - Account ID: `2240915` · Form ID: `183664557068125464`
  - Script: `https://groot.mailerlite.com/js/w/webforms.min.js`
  - Present only on `contact.html`
  - **No API key in HTML** — public form ID, MailerLite validates server-side
  - MFA on account: **ON** (enabled 2026-04-20)
  - Contract/billing: **Free tier** (≤500 subscribers). Currently 1 subscriber. Owner login: `mark@taraniscapital.com`.

- **Google Analytics 4** — traffic analytics
  - Measurement ID: `G-JLN31RRY1V`
  - Embedded via `gtag.js` on every page on the main site and all five fund subdomains
  - Account access: **`mark@taraniscapital.com` only** (confirmed 2026-04-20)
  - Connected services: **Google Search Console** (same account) · Google Ads not linked

- **RSS feeds on the Insights page** (`js/main.js:148-168`) — 14 public feeds, no auth, routed through the free-tier `api.rss2json.com` proxy:

  | Category | Feeds |
  |---|---|
  | Venture Capital | TechCrunch, EU-Startups, Crunchbase News |
  | Fintech | The Fintech Times, Finextra, PYMNTS |
  | Biotech | FierceBiotech, GEN, BioPharma Dive |
  | MENA | Waya Media, Zawya, Gulf News Business |
  | Crypto | CoinDesk, CoinTelegraph |

  Proxy: `https://api.rss2json.com/v1/api.json?rss_url=` (no API key; rate-limited public tier).

- **Google Workspace** — domain email for `mark@taraniscapital.com`. Not integrated with the site itself, but the DNS apex carries its MX/SPF/DKIM/verification records.

---

## 8. Database

**N/A — no database.** Flat-file static site. No engine, no migrations, no persistent server-side state. Contact form submissions are handled entirely by MailerLite (external).

---

## 9. Monitoring / alerting

- **Pre-discovery state:** nothing watching the site. Outage detection was reactive (Mark noticing).
- **Discovery-pass inline fix (2026-04-20):** Route 53 health check on `http://taraniscapital.com:80/` (HTTP on port 80 — see note below, interval 30s, failure threshold 3, 8 checker regions) → CloudWatch alarm `taraniscapital-com-uptime` in `us-east-1` (fires when `HealthCheckStatus < 1` for 1 minute) → SNS topic `arn:aws:sns:us-east-1:571600836975:taraniscapital-uptime-alerts` → email subscription `mark@taraniscapital.com` (confirmed). Cost ~£0.40/month.
  - **Why HTTP not HTTPS:** Route 53 health checkers support up to TLS 1.2 only; the main CloudFront distribution requires TLSv1.3_2025 — HTTPS checks fail with `protocol_version` alert. Port 80 returns `301 → https://` which Route 53 treats as healthy (3xx). This monitors "CloudFront is responding on port 80" — it catches total outages but not HTTPS-specific failures (bad cert, TLS config drift). Follow-up candidate: lower main distribution min TLS to `TLSv1.2_2021` (aligns with subdomains) then switch the check to HTTPS.
- **CloudFront access logs:** disabled on all 6 distributions (no object-level request logs exist). Follow-up candidate.
- **CloudWatch metrics:** CloudFront publishes the standard metrics (Requests, 4xx/5xxErrorRate, BytesDownloaded) automatically; no custom alarms configured.
- **Dashboards:** none.
- **GitHub Actions build status:** visible in Actions tab; no external alerting when a deploy fails.

---

## 10. Backup / DR

- **Authoritative source backup:** the git repository `https://github.com/Walkerma75/taraniscapital-website`. Everything needed to rebuild the site lives there. Subdomain content is in `subdomains/<name>/` in the same repo.
- **Object-level rollback:** S3 versioning enabled on all 6 buckets (2026-04-20). Previous object versions can be restored without redeploy. Lifecycle policy to age out old versions: **not configured** (means versions accumulate indefinitely — consider adding a 30-day expiry on noncurrent versions).
- **Off-site copy:** GitHub is the off-site copy. No additional mirror.
- **Restore procedure (site rebuild from nothing):**
  1. Clone the repo locally
  2. Create S3 buckets + CloudFront distributions + Route 53 records per `SUBDOMAIN-SETUP.md` (or re-use existing if they still exist)
  3. Configure `taranis-deploy` IAM user + GitHub repo secrets
  4. `git push origin main` — Actions workflow syncs everything
- **Last restore test:** never — **scheduled for 2026-04-30** in `TASKS.md`. Tier 2 Handover checklist requires a full restore-from-nothing drill (stand up a scratch S3 bucket + distribution, confirm the pipeline rebuilds the site end-to-end). Rollback (smaller scope) was tested 2026-04-20; the restore-from-nothing is a ~30-minute exercise best done in an unhurried window.

---

## 11. Tribal knowledge

- **Two GitHub accounts on this machine** (`Walkerma75` + `markwalker-pcs`). Windows Credential Manager has previously prompted for creds on push. Keep the git `user.email` matched to the account that owns the repo.
- **Weekly auto-sync scheduled task** points at the wrong Cowork folder (CLAUDE.md flags this). Needs re-pointing; that's an operational fix, not an infra fix.
- **People-data source of truth:** `Taranis-People-Data-Collection.xlsx` (renamed from `-KB` suffix on 2026-04-20 after the earlier corrupted copy was replaced). Don't edit the JSON mirror directly; regenerate from the xlsx.
- **`url-rewrite` CloudFront Function** on the main distribution handles: (a) clean URLs — appends `.html` to extensionless paths so `/contact` serves `contact.html`; (b) 301 redirects from the old WordPress URL structure (see `PROPOSED-REDIRECTS.md`). **Not attached to the subdomains** — they use their own direct S3 paths.
- **Distribution drift.** Main has TLS 1.3_2025, PriceClass_All, a WAF, and the url-rewrite Function. The five subdomains have TLS 1.2_2021, PriceClass_100, no WAF, no Function. Likely intentional at creation (cost, simplicity) but worth flagging if a consistency pass is done later.
- **Two wildcard ACM certs** both cover the same domain space. Main uses cert #1 (`ea95d60f-…`), subdomains use cert #2 (`fa9c7dad-…`). Either could cover everything. Low priority — no harm from the duplication, just clutter.
- **Scope co-tenant:** `dataroom.taraniscapital.com` (DNS alias to ALB), `taranis-dataroom-documents-prod` (S3 bucket), `e8bb602c-…` (ACM cert in `eu-west-2`), and `taranis-dataroom-alb-…` (ALB) all belong to the **Taranis Dataroom** project, not this site. Same AWS account, different Tier-3 project. Leave alone from this repo.
- **`taranis-deploy` is tightly scoped** — no IAM, no CloudTrail, no Route 53 write, no SNS. Good for least-privilege. Downside: local CLI work from Mark's machine currently uses this same key, so several console-level tasks (health check creation, IAM enumeration) need to be done in the AWS console or under a separate admin principal.
- **CloudFront Function runtime** is `cloudfront-js-2.0`. Update procedure is in `SUBDOMAIN-SETUP.md` Step 0 (get → edit → update → publish with ETag handling).

---

## 12. Known risks / open items

| Risk | Severity | Mitigation / owner |
|---|---|---|
| **`taranis-deploy` substantially over-permissive** — `AmazonS3FullAccess`, `AmazonRoute53FullAccess`, `CloudFrontFullAccess`, `AmazonEC2ContainerRegistryPowerUser`, and inline `ECSDeployPolicy`. Single compromise = write access on website + Dataroom documents + DNS + ECS. | **High** | Follow-up in `TASKS.md` — split into per-project users, scope policies to specific ARNs. Pair with the 4 May rotation if possible |
| `taranis-deploy` AWS key never rotated since CI setup | Medium | Rotation scheduled 2026-05-04 (see `TASKS.md`) |
| Both IAM users (`taranis-deploy`, `github-deploy`) have no MFA, no console sign-in | Low–Medium | Access keys are the only credential path; no interactive login to protect. But MFA can be required for CLI calls via an assume-role bastion if desired. Follow-up |
| `github-deploy` purpose unknown — active but not documented | Medium | Follow-up in `TASKS.md` — identify owner, document, or remove |
| Deploy key also lives in `~/.aws/credentials` on Mark's machine (doubles blast radius) | Medium | Follow-up: create separate `mark-admin` IAM user, remove local deploy credential. See Questions for Mark item 9 |
| ~~No CloudTrail / audit trail configured in the account~~ | ~~Medium~~ | **Resolved 2026-04-20** — `taranis-capital-account-trail` created (multi-region, management events, log file validation) |
| No CloudFront access logs on any of the 6 distributions | Low | Follow-up candidate — evaluate cost vs forensic value |
| No lifecycle policy on S3 versioning → old versions accumulate | Low | Follow-up — add 30-day expiry on noncurrent versions once we have confidence in the backup chain |
| Distribution drift between main (TLS 1.3 + WAF + Function) and subdomains (TLS 1.2, no WAF, no Function) | Low | Review if a consistency pass is warranted |
| 10 board bios missing, 11 LinkedIn URLs missing | Low (content, not infra) | Tracked in `MISSING-PROFILE-INFO.md` |
| No restore-from-nothing drill has ever been run | Medium | **Scheduled 2026-04-30** in `TASKS.md`. Rollback drill itself was performed 2026-04-20. |
| **Active data exposure pre-2026-04-20: internal `.md` docs (including 65 KB `PROJECT-LOG.md`) were publicly readable** at `https://taraniscapital.com/<file>.md` because the workflow's S3 sync excluded specific folders but not `.md` files at root | Medium — historical. Resolved 2026-04-20 by moving docs to `docs/` + adding `*.md`/`docs/*` excludes to the workflow. Content that was exposed is now gone from the live bucket, but may have been indexed by search engines — Google cache / Wayback Machine retention is outside our control. | Resolved inline 2026-04-20. Follow-up consideration: Google search `site:taraniscapital.com filetype:md` to see if any pages were indexed, and request removal via Search Console if so |

---

## Sources read during this pass

- `MIGRATION-BRIEF.md`
- `CLAUDE.md`
- `../../PROJECTS-REGISTER.md` (Discovery policy + inventory template)
- `../../ACCOUNTS.md` (Taranis rows, grep only)
- `Taranis Website - AWS Infrastructure Summary.md`
- `SUBDOMAIN-SETUP.md` (skimmed Step 0 re url-rewrite Function)
- `TASKS.md`
- `MISSING-PROFILE-INFO.md` (head)
- `.github/workflows/deploy.yml`
- `.gitignore`
- `contact.html` (MailerLite form)
- `js/main.js` (RSS feed list)
- AWS CLI as `taranis-deploy`: `sts`, `s3 ls`, `s3api get-bucket-versioning`, `s3api put-bucket-versioning`, `cloudfront list-distributions`, `cloudfront get-distribution`, `route53 list-hosted-zones`, `route53 list-resource-record-sets`, `acm list-certificates` (both regions), `sns list-topics`, `route53 list-health-checks`
- `git log --all --full-history -S` across 6 secret patterns

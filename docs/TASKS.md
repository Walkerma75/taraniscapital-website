# Tasks

## Active

### Migration discovery follow-ups (from MIGRATION-BRIEF.md — 2026-04-20)

- [x] **Rotate `taranis-deploy` AWS access key** — **completed 2026-04-20** (earlier than 4 May deadline). Superseded by the creation of `taranis-website-deploy` below.
- [x] **Tighten `taranis-website` IAM to least-privilege** — **completed 2026-04-20**. New IAM user `taranis-website-deploy` created with `TaranisWebsiteDeployPolicy` scoped to exactly the 6 website buckets and the 6 CloudFront distribution ARNs. GitHub secrets rotated. Verified by empty-commit deploy (run succeeded end-to-end). Old `taranis-deploy` access key deactivated 2026-04-20, **scheduled to delete 2026-04-21**.
- [ ] **Delete the deactivated `taranis-deploy` access key** — scheduled **2026-04-21** (24h after deactivation). Only delete if no Dataroom / other CI has failed in the intervening period.
- [ ] **Dataroom cross-project IAM cleanup (follow-up for Dataroom discovery pass)** — the original `taranis-deploy` user (S3/Route53/CloudFront FullAccess + ECR + inline `ECSDeployPolicy`) and the separate `github-deploy` user remain in the account and are used by the Taranis Dataroom project. When Dataroom discovery runs, split those into scoped per-project users and then consider whether `taranis-deploy` can be deleted entirely.
- [ ] **Identify what `github-deploy` IAM user is used for** — deadline **4 May 2026**. Active user (last used 2026-04-20) but not documented. Check which repo/workflow consumes its key; document, consolidate, or remove as appropriate.
- [x] **Enable CloudTrail on the `TaranisCapital` account** — **completed 2026-04-20**. Trail `taranis-capital-account-trail` created (multi-region, management events, log file validation on, SSE-KMS off). Logs to S3 bucket `aws-cloudtrail-logs-571600836975-f495d2a6`. Cost £0/month (first trail is free).
- [ ] **Create a separate `mark-admin` IAM user for local CLI work** — deadline none, convenience task. Attach `AdministratorAccess` + require MFA. Remove `taranis-deploy` credentials from `~/.aws/credentials` on Mark's machine once the new profile is verified. Removes the local exposure of the CI deploy key.
- [ ] **Run a restore-from-nothing drill** — deadline **30 April 2026**. Tier 2 Handover checklist requires it. Clone repo to a scratch directory, point a scratch S3 bucket + distribution at it, confirm the pipeline rebuilds the site end-to-end. Dry-run only, don't touch production buckets. A ~30-minute task when Mark has an unhurried window.
- [ ] **Audit search engine caches for the previously-exposed `.md` docs** — deadline **24 April 2026**. Root cause fixed 2026-04-20 (workflow `*.md`/`docs/*` excludes + docs moved to `docs/`). However content Google / Bing / Wayback Machine indexed while public may still be cached. Run `site:taraniscapital.com filetype:md` in Google and Bing. If any pages appear, use Google Search Console → Removals → Temporary removal to kill the cached copy, and file a Wayback Machine removal request if applicable. No action needed if no hits.
- [ ] **Add S3 versioning lifecycle policy** — once we're confident the backup chain is healthy (say, 30 days after 2026-04-20), add a lifecycle rule on all 6 buckets to expire noncurrent versions after 30 days. Otherwise old versions accumulate indefinitely.
- [ ] **Evaluate distribution consistency** — main distribution has TLS 1.3_2025 + WAF + `url-rewrite` Function; subdomains have TLS 1.2_2021 + no WAF + no Function. Decide whether to bring subdomains into line (raise TLS minimum at minimum — cheap and non-breaking).
- [ ] **Align main distribution's TLS min + switch uptime check to HTTPS** — main currently requires `TLSv1.3_2025`, which Route 53 health checkers can't negotiate (max TLS 1.2). Current uptime check is on HTTP:80 as a workaround, which monitors only basic reachability, not TLS/cert health. Options: (a) lower main distribution min TLS to `TLSv1.2_2021` (aligns with subdomains, minor posture weakening) then recreate the health check on HTTPS:443 with SNI, or (b) keep TLS 1.3 and accept the weaker HTTP-only uptime monitoring, or (c) add UptimeRobot (or similar) as a secondary HTTPS monitor that handles TLS 1.3. No deadline — driven by preference.
- [ ] **Enable CloudFront access logs** — currently disabled on all 6 distributions. Follow-up to decide: enable with a bucket lifecycle for 30/90-day retention, or leave off and accept the trade-off.

### DNS & Nameserver Migration

- [x] **Audit all existing DNS records on Funkygrafix** - Documented all 30 records; identified 9 essential records (A, www CNAME, MX, SPF TXT, DKIM TXT, Google verify CNAME, biotech A, biotech TXT, ACM validation CNAME) and 21 cPanel-generated junk records
- [x] **Decide target DNS provider for migration** - Chose AWS Route 53 over e& built-in DNS. Route 53 supports ALIAS records for CloudFront root domain, integrates natively with AWS hosting, costs $0.50/month
- [x] **Create Route 53 hosted zone** - Created hosted zone Z0680053Y587NB8B8C9S for taraniscapital.com
- [x] **Recreate all DNS records on Route 53** - All 9 essential records created via CloudShell CLI, including ALIAS to CloudFront for root domain, DKIM TXT via Python script. 11 total records (9 migrated + 2 auto NS/SOA)
- [x] **Add AWS ACM CNAME validation record** - Included in the Route 53 batch creation
- [x] **Verify AWS SSL certificate validates successfully** - Certificate was already issued; ACM validation CNAME migrated to Route 53
- [x] **Switch nameservers at e& domain registrar to Route 53** - Updated from ns1/ns2.funkygrafix.co.uk to Route 53 nameservers (ns-1539.awsdns-00.co.uk, ns-942.awsdns-53.net, ns-399.awsdns-49.com, ns-1261.awsdns-29.org). Confirmed by e& registrar on 2026-04-07
- [x] **Monitor DNS propagation and verify all services** - Verified via dnschecker.org on 2026-04-07: NS records 100% propagated across all 28 global DNS servers; A records resolving to CloudFront edge IPs worldwide
- [ ] **Decommission Funkygrafix account** - Wait 48-72 hours after migration (earliest: 2026-04-10), then remove records and close account

## Waiting On

## Someday

## Done


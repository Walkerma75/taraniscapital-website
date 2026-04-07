# Tasks

## Active

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


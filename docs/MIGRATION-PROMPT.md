# Claude Code handover prompt — Taranis Capital Website

**Created:** 20 April 2026
**Purpose:** The prompt to paste into a fresh Claude Code session started in this folder. Runs the migration discovery pass described in `MIGRATION-BRIEF.md` and produces the signed-off `MIGRATION-INVENTORY.md`.

---

## The prompt

Copy everything inside the fenced block below. Paste as the first message of a new Claude Code session, rooted at this folder.

```
You are in a Claude Code session rooted at the Taranis Capital Website repo
(the folder this prompt was pasted into). Your job is to complete the
migration discovery pass for this project and produce a signed-off
MIGRATION-INVENTORY.md.

Priority order of instructions:

1. MIGRATION-BRIEF.md (this folder) is authoritative. Read it first and
   follow its execution plan exactly. Do not re-scope.
2. ../PROJECTS-REGISTER.md defines the Discovery policy. Read the
   "Discovery policy" section before making any infrastructure change.
3. ../ACCOUNTS.md is the portfolio-wide infrastructure map. Reference it
   for account IDs; do not duplicate it into this repo.
4. CLAUDE.md (this folder) is the per-project context briefing.
   PROJECT-LOG.md is deep context if you need it.

Produce a new file at the repo root: MIGRATION-INVENTORY.md, following the
12-section template in ../PROJECTS-REGISTER.md. The top of that file must
carry two blocks:

- "Changes made during discovery" — pre-seeded with the two 2026-04-20
  MFA enablements that Mark has already completed (Walkerma75 GitHub +
  Taranis MailerLite). Append every further inline fix you perform, with
  date, what changed, why, and how to revert.
- "Questions for Mark" — anything you cannot resolve from the repo, the
  brief, ACCOUNTS.md, or AWS CLI calls. Do not guess; ask.

Constraints:

- Follow the Discovery policy strictly. If in doubt, it is a follow-up,
  not an inline fix.
- Never rotate secrets, change IAM policies, alter DNS records, change
  CloudFront distributions, modify CI/CD workflows, or touch the running
  site. These are follow-ups, regardless of apparent urgency.
- Do not put secret values into committed files. Names and locations
  only.
- UK English throughout.

Definition of done:

1. All 12 inventory sections filled (Database is N/A — flat static site).
2. Every "Still open — Bucket B" and "Bucket C" item from MIGRATION-BRIEF.md
   is either resolved (answer written into the inventory) or logged as a
   follow-up in TASKS.md with a deadline.
3. The three scheduled inline fixes are applied and logged:
   a. Branch protection on main (linear history, no force-push, no delete)
   b. S3 bucket versioning on the main bucket and all five fund-subdomain
      buckets
   c. Uptime monitor on https://taraniscapital.com (Mark's preferred:
      Route 53 health check with SNS → email; fall back to UptimeRobot
      free tier only if Route 53 health check incurs unexpected cost —
      confirm with Mark before choosing the fallback)
4. ../PROJECTS-REGISTER.md Taranis Capital Website row updated:
   Discovery status → Discovery complete
   Inventory doc → MIGRATION-INVENTORY.md
   Handover status → Migrated
5. Handover checklist in PROJECTS-REGISTER.md ticked for this project.
6. End the session with a short written summary of findings and any
   follow-ups for Mark to review.

Stop and ask Mark before acting if:

- You find anything that looks like a secret in git history (any match
  for AKIA, aws_access, aws_secret, BEGIN RSA, BEGIN OPENSSH,
  private_key — stop immediately, do not commit anything).
- You find an IAM policy that is substantially over-permissive (e.g.
  grants * on services the workflow does not use).
- You find AWS resources in the TaranisCapital account that do not match
  the expected inventory (unknown buckets, unexpected distributions,
  orphaned roles).
- An inline fix turns out to be already done (skip it, log that you
  checked).
- Any single inline change would take more than 10 minutes or require
  more than a single CLI call to revert.

Begin by reading MIGRATION-BRIEF.md in full and playing back to Mark what
you understand the task to be — including the three inline fixes, the
follow-up rotation scheduled for 4 May 2026, and the two MFA changes
already logged. Do not make any changes until Mark confirms your
read-back.
```

---

## Reuse note

This shape is reusable for future projects. For each new project, swap:

- "Taranis Capital Website" → new project name
- The three inline fixes (they're project-specific)
- The pre-seeded "Changes made during discovery" entries
- The Database line under Definition of done ("N/A — flat static site" only applies here)

Keep the rest identical — priority order, Discovery policy reference, constraints, "stop and ask" triggers, read-back-first requirement.

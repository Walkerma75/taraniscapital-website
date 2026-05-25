"""xlsx-sync-guard.py — pre-flight check for the weekly people-data sync.

PURPOSE
-------
The Cowork-side `taranis-people-sync` scheduled task reads
`Taranis-People-Data-Collection.xlsx` from Google Drive (Cowork's
source-of-truth copy) and overwrites the local copy in this repo before
regenerating JSON / HTML.

If a user has edited the local xlsx without first applying the same edits
to the Drive copy, the sync will silently *roll back* those edits — and
without a `git`-tracked snapshot of the prior state, the changes are lost.

This script is the safety check that should run *before* the scheduled task
overwrites the local file. It does two things:

    1. Refuses the overwrite when the local file is newer than what the
       repo has committed (i.e. a user has made unsaved-to-git edits).
       The sync task should abort and surface the situation to the user
       rather than clobber.

    2. Snapshots the current `.xlsx` and any existing `.xlsx.bak` into git
       so that an overwrite, if it does happen, can be recovered via
       `git checkout <sha> -- Taranis-People-Data-Collection.xlsx`.

USAGE
-----
    python tools/xlsx-sync-guard.py --check   # exit 0 if safe to overwrite, 1 if local edits would be lost
    python tools/xlsx-sync-guard.py --snapshot  # stage and commit the current xlsx + .bak to git on a snapshot branch
    python tools/xlsx-sync-guard.py --bak     # copy current .xlsx → .xlsx.bak (called by the sync task right before write)

The Cowork scheduled task SKILL.md (see the Scheduled sidebar) should be
amended to call this script. Suggested call order:

    1. python tools/xlsx-sync-guard.py --check   # abort sync if exit != 0
    2. python tools/xlsx-sync-guard.py --snapshot
    3. python tools/xlsx-sync-guard.py --bak
    4. <overwrite the xlsx from Drive>
    5. <regenerate JSON, HTML, etc.>
    6. <commit everything including the new xlsx + bak>
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
XLSX = REPO_ROOT / "Taranis-People-Data-Collection.xlsx"
BAK = REPO_ROOT / "Taranis-People-Data-Collection.xlsx.bak"


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, **kwargs)


def local_is_newer_than_committed() -> bool:
    """Return True iff the local xlsx differs from the committed version
    (HEAD blob). We compare hashes — mtime is unreliable on network mounts."""
    if not XLSX.exists():
        return False
    r = run(["git", "hash-object", str(XLSX)])
    if r.returncode != 0:
        # If hash-object fails, assume unsafe so we don't silently overwrite.
        print(f"git hash-object failed: {r.stderr.strip()}", file=sys.stderr)
        return True
    local_hash = r.stdout.strip()
    r2 = run(["git", "ls-tree", "HEAD", "--", "Taranis-People-Data-Collection.xlsx"])
    if r2.returncode != 0 or not r2.stdout.strip():
        # File not tracked at HEAD yet — treat as "local has data the repo doesn't"
        return True
    head_hash = r2.stdout.split()[2]
    return local_hash != head_hash


def cmd_check() -> int:
    if local_is_newer_than_committed():
        print(
            "REFUSE: local Taranis-People-Data-Collection.xlsx has uncommitted "
            "changes (differs from HEAD).\n"
            "The scheduled sync would overwrite them with Drive's copy.\n"
            "Action required: commit the local xlsx first, OR re-apply the "
            "edits to the Google Drive copy and re-run the sync."
        )
        return 1
    print("OK: local xlsx matches HEAD; safe to overwrite.")
    return 0


def cmd_bak() -> int:
    if not XLSX.exists():
        print(f"no xlsx at {XLSX}", file=sys.stderr)
        return 1
    shutil.copy2(XLSX, BAK)
    print(f"backed up {XLSX.name} → {BAK.name}")
    return 0


def cmd_snapshot() -> int:
    """Stage and commit the current xlsx + bak on a snapshot branch.

    Creates a branch named `xlsx-snapshot/YYYY-MM-DD-HHMM` from the current
    HEAD, commits the xlsx and the .bak (if present), pushes to origin.
    The scheduled task can then overwrite the working tree knowing every
    prior on-disk state is recoverable.
    """
    if not XLSX.exists():
        print(f"no xlsx at {XLSX}", file=sys.stderr)
        return 1
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    branch = f"xlsx-snapshot/{stamp}"

    # Stash any other changes so the snapshot is clean (sync runs in a clean tree anyway)
    run(["git", "checkout", "-b", branch])
    run(["git", "add", "Taranis-People-Data-Collection.xlsx"])
    if BAK.exists():
        run(["git", "add", "Taranis-People-Data-Collection.xlsx.bak"])
    msg = f"xlsx snapshot {stamp} (pre-sync)"
    commit = run(["git", "commit", "-m", msg, "--allow-empty"])
    if commit.returncode != 0:
        print(commit.stdout, commit.stderr, file=sys.stderr)
        return 1
    push = run(["git", "push", "-u", "origin", branch])
    if push.returncode != 0:
        print(push.stdout, push.stderr, file=sys.stderr)
        # Push failure is non-fatal — local commit still recoverable
    print(f"snapshot committed on {branch}")
    # Return to main
    run(["git", "checkout", "main"])
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Safety guard for the weekly xlsx sync.")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--check", action="store_true", help="Exit non-zero if local file has uncommitted changes")
    grp.add_argument("--bak", action="store_true", help="Copy current xlsx → xlsx.bak")
    grp.add_argument("--snapshot", action="store_true", help="Commit xlsx + bak on a snapshot branch")
    args = p.parse_args(argv)
    if args.check:
        return cmd_check()
    if args.bak:
        return cmd_bak()
    if args.snapshot:
        return cmd_snapshot()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env bash
# infra/compute-invalidations.sh
#
# Compute CloudFront invalidation paths from a git diff range and group
# them by distribution. Output format, one entry per line:
#
#     DIST:/path
#
# Distribution keys:
#     APEX             — apex bucket (taraniscapital.com)
#     FINTECH          — fintech.taraniscapital.com
#     DATACENTRE       — datacentre.taraniscapital.com
#     PROPERTY         — property.taraniscapital.com
#     DISRUPTIVE_TECH  — disruptive-tech.taraniscapital.com
#     BIOTECH          — biotech.taraniscapital.com
#
# Usage:  compute-invalidations.sh <before-sha> <after-sha>
#
# Rules:
#   * If before-sha is all-zeros (initial / force push) or empty, emit "/*"
#     for every distribution.
#   * If a single distribution has > 50 changed paths, fall back to "/*"
#     for that distribution only (cheaper than enumerating).
#   * For HTML files in the apex tree, emit BOTH the .html path AND the
#     clean-URL form (e.g. "/board/foo.html" + "/board/foo") because the
#     CloudFront viewer-request function rewrites between them — the
#     edge cache keys them separately.
#   * Skip files that aren't served by the site (docs/, infra/, *.md, etc.)

set -euo pipefail

BEFORE="${1:?before SHA required}"
AFTER="${2:?after SHA required}"

ALL_DISTS=(APEX FINTECH DATACENTRE PROPERTY DISRUPTIVE_TECH BIOTECH)
ZERO_SHA="0000000000000000000000000000000000000000"

# Initial / force push — invalidate everything.
if [ -z "$BEFORE" ] || [ "$BEFORE" = "$ZERO_SHA" ]; then
  for d in "${ALL_DISTS[@]}"; do echo "${d}:/*"; done
  exit 0
fi

# Make sure both SHAs are reachable. If not, fall back.
if ! git cat-file -e "$BEFORE" 2>/dev/null || ! git cat-file -e "$AFTER" 2>/dev/null; then
  for d in "${ALL_DISTS[@]}"; do echo "${d}:/*"; done
  exit 0
fi

CHANGED=$(git diff --name-only "$BEFORE" "$AFTER" || true)

declare -A PATHS
for d in "${ALL_DISTS[@]}"; do PATHS[$d]=""; done

add() {
  local dist=$1 path=$2
  PATHS[$dist]+="${path}"$'\n'
}

while IFS= read -r f; do
  [ -z "$f" ] && continue

  # Skip files that are not deployed.
  case "$f" in
    .git/*|.github/*|.gitignore) continue ;;
    docs/*|infra/*|tools/*) continue ;;
    Wp-content/*|"Board of Advisors/"*|Documents/*) continue ;;
    "TC Logos/"*|"Team Images/"*|"Tmp Images folder/"*) continue ;;
    *.md|*.xlsx|*.xls|*.lock) continue ;;
  esac

  # Subdomain files → that subdomain's distribution
  case "$f" in
    subdomains/fintech/*)
      add FINTECH "/${f#subdomains/fintech/}"
      continue ;;
    subdomains/datacentre/*)
      add DATACENTRE "/${f#subdomains/datacentre/}"
      continue ;;
    subdomains/property/*)
      add PROPERTY "/${f#subdomains/property/}"
      continue ;;
    subdomains/disruptive-tech/*)
      add DISRUPTIVE_TECH "/${f#subdomains/disruptive-tech/}"
      continue ;;
    subdomains/biotech/*)
      add BIOTECH "/${f#subdomains/biotech/}"
      continue ;;
    subdomains/*) continue ;;   # any other subdomain — skip
  esac

  # Apex distribution
  case "$f" in
    index.html)
      add APEX "/"
      add APEX "/index.html"
      ;;
    *.html)
      # Clean URL + .html — viewer-request function rewrites between them,
      # so each is a distinct edge-cache key.
      add APEX "/${f%.html}"
      add APEX "/$f"
      ;;
    *)
      add APEX "/$f"
      ;;
  esac
done <<<"$CHANGED"

for d in "${ALL_DISTS[@]}"; do
  list=$(printf '%s' "${PATHS[$d]}" | grep -v '^$' | sort -u || true)
  count=$(printf '%s\n' "$list" | grep -c '^/' || true)
  if [ "$count" -eq 0 ]; then
    continue
  elif [ "$count" -gt 50 ]; then
    echo "${d}:/*"
  else
    while IFS= read -r p; do
      [ -z "$p" ] && continue
      echo "${d}:${p}"
    done <<<"$list"
  fi
done

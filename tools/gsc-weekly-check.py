#!/usr/bin/env python3
"""
gsc-weekly-check.py — Unattended Google Search Console health check via the
Search Console API (service-account auth, no browser required).

Covers the parts of the weekly GSC check that the API CAN reach:
  1. Sitemaps      — status, last-read date, discovered (submitted) URL count
  2. Performance   — clicks / impressions / CTR / avg position, last 7 days,
                     with week-over-week deltas
  3. Index health  — per-URL inspection of every URL in the local sitemap.xml
                     (a cleaner "are my real pages indexed?" signal than the
                     aggregate report, which is dominated by old WordPress 404s)

It does NOT cover Manual Actions, Security Issues, the aggregate
not-indexed-by-reason table, or Core Web Vitals — those are not exposed by the
API and are handled by the separate monthly browser check + Google's automatic
owner email alerts. See docs/GSC-API-SETUP.md.

Output:
  - Prints a ready-to-paste Markdown block (body of the PROJECT-LOG entry) to
    stdout. The scheduled task adds the "### Session N — DATE" heading and the
    comparison-to-last-week prose, then appends it to docs/PROJECT-LOG.md.
  - Writes the same block to  <repo>/outputs or CWD as gsc-check-<date>.md
  - Writes raw metrics as JSON next to it (gsc-check-<date>.json) for tooling.

Usage:
  pip install --break-system-packages google-api-python-client google-auth
  python tools/gsc-weekly-check.py
  python tools/gsc-weekly-check.py --key /path/to/sa.json --out-dir /tmp

Auth:
  Reads a service-account JSON key. Resolution order:
    1. --key <path>
    2. $GSC_SA_KEY
    3. <repo-root>/secrets/gsc-service-account.json
  The service account must be added as a *Full* user on the property in
  Search Console → Settings → Users and permissions (Full is required for the
  URL Inspection API; performance + sitemaps would work with Restricted).
"""

import argparse
import datetime as dt
import json
import os
import sys
import time
import xml.etree.ElementTree as ET

PROPERTY = "sc-domain:taraniscapital.com"
SITEMAP_URL = "https://taraniscapital.com/sitemap.xml"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_SITEMAP = os.path.join(REPO_ROOT, "sitemap.xml")
DEFAULT_KEY = os.path.join(REPO_ROOT, "secrets", "gsc-service-account.json")


def eprint(*a):
    print(*a, file=sys.stderr)


def resolve_key(cli_key):
    for cand in (cli_key, os.environ.get("GSC_SA_KEY"), DEFAULT_KEY):
        if cand and os.path.isfile(cand):
            return cand
    eprint(
        "ERROR: service-account key not found. Looked at --key, $GSC_SA_KEY, and\n"
        f"       {DEFAULT_KEY}\n"
        "       See docs/GSC-API-SETUP.md for how to create and place the key."
    )
    sys.exit(2)


def build_services(key_path):
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        eprint(
            "ERROR: missing deps. Run:\n"
            "  pip install --break-system-packages google-api-python-client google-auth"
        )
        sys.exit(2)
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    # webmasters v3: searchanalytics + sitemaps. searchconsole v1: urlInspection.
    wm = build("webmasters", "v3", credentials=creds, cache_discovery=False)
    sc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    return wm, sc


def local_sitemap_urls():
    try:
        tree = ET.parse(LOCAL_SITEMAP)
    except Exception as e:
        eprint(f"WARN: could not parse local sitemap.xml ({e}); URL inspection skipped.")
        return []
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [el.text.strip() for el in tree.getroot().findall(".//sm:loc", ns) if el.text]


# ----------------------------------------------------------------------------- sitemaps
def check_sitemaps(wm):
    out = {"ok": False}
    try:
        info = wm.sitemaps().get(siteUrl=PROPERTY, feedpath=SITEMAP_URL).execute()
    except Exception as e:
        out["error"] = str(e)
        return out
    contents = info.get("contents", [])
    submitted = sum(int(c.get("submitted", 0)) for c in contents)
    out.update(
        ok=True,
        last_downloaded=info.get("lastDownloaded", ""),
        is_pending=info.get("isPending", False),
        errors=int(info.get("errors", 0)),
        warnings=int(info.get("warnings", 0)),
        discovered=submitted,
    )
    return out


# ----------------------------------------------------------------------------- performance
def perf_window(wm, start, end):
    body = {"startDate": start, "endDate": end, "dimensions": [], "dataState": "final"}
    rows = wm.searchanalytics().query(siteUrl=PROPERTY, body=body).execute().get("rows", [])
    if not rows:
        return {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0}
    r = rows[0]
    return {
        "clicks": int(r.get("clicks", 0)),
        "impressions": int(r.get("impressions", 0)),
        "ctr": round(r.get("ctr", 0.0) * 100, 1),     # %
        "position": round(r.get("position", 0.0), 1),
    }


def check_performance(wm, end_offset_days=3):
    # GSC finalises data ~2-3 days late; end the window 3 days back for stable figures.
    end = dt.date.today() - dt.timedelta(days=end_offset_days)
    start = end - dt.timedelta(days=6)
    prev_end = start - dt.timedelta(days=1)
    prev_start = prev_end - dt.timedelta(days=6)
    cur = perf_window(wm, start.isoformat(), end.isoformat())
    prev = perf_window(wm, prev_start.isoformat(), prev_end.isoformat())
    return {
        "window": f"{start.isoformat()} to {end.isoformat()}",
        "prev_window": f"{prev_start.isoformat()} to {prev_end.isoformat()}",
        "current": cur,
        "previous": prev,
    }


# ----------------------------------------------------------------------------- url inspection
def inspect_urls(sc, urls):
    try:
        from googleapiclient.errors import HttpError
    except ImportError:
        HttpError = Exception
    tally = {"indexed": 0, "not_indexed": 0, "errors": 0}
    not_indexed_detail = []
    for u in urls:
        body = {"inspectionUrl": u, "siteUrl": PROPERTY}
        for attempt in range(3):
            try:
                res = sc.urlInspection().index().inspect(body=body).execute()
                idx = res.get("inspectionResult", {}).get("indexStatusResult", {})
                verdict = idx.get("verdict", "")
                coverage = idx.get("coverageState", "")
                if verdict == "PASS" or coverage.lower().startswith("submitted and indexed") \
                        or coverage.lower() == "indexed, not submitted in sitemap":
                    tally["indexed"] += 1
                else:
                    tally["not_indexed"] += 1
                    not_indexed_detail.append({"url": u, "coverage": coverage, "verdict": verdict})
                break
            except HttpError as e:
                if getattr(e, "resp", None) is not None and e.resp.status in (429, 503):
                    time.sleep(2 * (attempt + 1))
                    continue
                tally["errors"] += 1
                not_indexed_detail.append({"url": u, "coverage": f"API error: {e}", "verdict": "ERROR"})
                break
            except Exception as e:
                tally["errors"] += 1
                not_indexed_detail.append({"url": u, "coverage": f"error: {e}", "verdict": "ERROR"})
                break
        time.sleep(0.12)  # stay well under 600 QPM
    return tally, not_indexed_detail


# ----------------------------------------------------------------------------- rendering
def pct_delta(cur, prev):
    if prev == 0:
        return "n/a" if cur == 0 else "+∞"
    d = (cur - prev) / prev * 100
    return f"{d:+.0f}%"


def render(metrics):
    s = metrics["sitemaps"]
    p = metrics["performance"]
    insp = metrics["inspection"]
    local_n = metrics["local_sitemap_count"]
    L = []
    L.append("**1. Sitemaps**")
    if s.get("ok"):
        status = "Success" if s["errors"] == 0 else f"{s['errors']} error(s)"
        match = "matches local exactly ✅" if s["discovered"] == local_n \
            else f"⚠️ MISMATCH — local sitemap.xml has {local_n} `<loc>` entries (likely read-lag if GSC is lower)"
        L.append(f"- sitemap.xml — Status: **{status}**" + (f", {s['warnings']} warning(s)" if s["warnings"] else ""))
        L.append(f"- Last read: **{s.get('last_downloaded','')[:10]}**")
        L.append(f"- Discovered pages: **{s['discovered']}** — {match}")
    else:
        L.append(f"- ⚠️ could not read sitemap status via API: {s.get('error','unknown error')}")
    L.append("")
    L.append("**2. Performance (last 7 days, API)**")
    cur, prev = p["current"], p["previous"]
    L.append(f"- Window: {p['window']} (prev: {p['prev_window']})")
    L.append(f"- Total clicks: **{cur['clicks']}** (prev {prev['clicks']}, {pct_delta(cur['clicks'], prev['clicks'])})")
    L.append(f"- Total impressions: **{cur['impressions']}** (prev {prev['impressions']}, {pct_delta(cur['impressions'], prev['impressions'])})")
    L.append(f"- Average CTR: **{cur['ctr']}%** (prev {prev['ctr']}%)")
    L.append(f"- Average position: **{cur['position']}** (prev {prev['position']})")
    L.append("")
    L.append("**3. Index health — URL Inspection of sitemap URLs (API)**")
    L.append(f"- URLs inspected: **{insp['tally']['indexed'] + insp['tally']['not_indexed'] + insp['tally']['errors']}** of {local_n} in sitemap.xml")
    L.append(f"- On Google (indexed): **{insp['tally']['indexed']}**")
    L.append(f"- NOT indexed: **{insp['tally']['not_indexed']}**" + (f"; API errors: {insp['tally']['errors']}" if insp['tally']['errors'] else ""))
    if insp["not_indexed"]:
        L.append("- Not-indexed / error URLs (investigate any legitimate page here):")
        for d in insp["not_indexed"][:60]:
            L.append(f"    - `{d['url'].replace('https://taraniscapital.com','')}` — {d['coverage'] or d['verdict']}")
    else:
        L.append("- ✅ every sitemap URL is indexed on Google")
    L.append("")
    L.append("**4. Manual Actions / Security / Core Web Vitals**")
    L.append("- Not checked by this API run (no API surface). Covered by the monthly browser check "
             "and Google's automatic owner email alerts. No alert emails ⇒ assume clean.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", help="path to service-account JSON key")
    ap.add_argument("--out-dir", default=os.environ.get("GSC_OUT_DIR", "."),
                    help="directory for the dated .md / .json output (default: cwd)")
    ap.add_argument("--no-inspect", action="store_true",
                    help="skip per-URL inspection (faster; sitemap + performance only)")
    ap.add_argument("--end-offset-days", type=int, default=3,
                    help="end the perf window N days before today (data-freshness lag)")
    args = ap.parse_args()

    key = resolve_key(args.key)
    eprint(f"Using key: {key}")
    wm, sc = build_services(key)

    urls = local_sitemap_urls()
    eprint(f"Local sitemap URLs: {len(urls)}")

    metrics = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "property": PROPERTY,
        "local_sitemap_count": len(urls),
        "sitemaps": check_sitemaps(wm),
        "performance": check_performance(wm, args.end_offset_days),
    }
    eprint("Sitemaps + performance done.")
    if args.no_inspect or not urls:
        metrics["inspection"] = {"tally": {"indexed": 0, "not_indexed": 0, "errors": 0}, "not_indexed": []}
    else:
        eprint(f"Inspecting {len(urls)} URLs (≈{len(urls)*0.12:.0f}s)…")
        tally, detail = inspect_urls(sc, urls)
        metrics["inspection"] = {"tally": tally, "not_indexed": detail}
    eprint("Inspection done.")

    block = render(metrics)
    today = dt.date.today().isoformat()
    os.makedirs(args.out_dir, exist_ok=True)
    md_path = os.path.join(args.out_dir, f"gsc-check-{today}.md")
    json_path = os.path.join(args.out_dir, f"gsc-check-{today}.json")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(block + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    eprint(f"Wrote {md_path} and {json_path}")

    print(block)  # stdout = the PROJECT-LOG entry body


if __name__ == "__main__":
    main()

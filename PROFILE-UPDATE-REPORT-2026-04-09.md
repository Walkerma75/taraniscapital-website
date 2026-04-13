# Profile Bio Update Report — 9 April 2026

## Summary

The `Taranis-People-Data-Collection.xlsx` spreadsheet was read and compared against all profile pages across the main site and all sub-sites. Bio text was updated wherever the spreadsheet contained newer content.

> **Note:** The spreadsheet file appears to be partially truncated (the compressed `sharedStrings.xml` stream ends at ~14KB of an expected ~50KB). As a result, only the first 9 people's data could be fully extracted. The remaining ~27 rows in the spreadsheet have their string data in the unrecoverable section. Those profiles were left unchanged.

---

## Files Updated

### Main Site — Board Profile Pages

| File | Change |
|------|--------|
| `board/amer-mahmood.html` | Replaced placeholder bio with full 3-paragraph bio covering KSU stem cell research, regenerative medicine, and gene therapy career. Also updated meta/OG descriptions. |
| `board/asim-chohan.html` | Replaced placeholder bio with full 3-paragraph bio covering SVP/COO role, Harvard/MIT/Cambridge qualifications, and AI expertise. Also updated meta/OG descriptions. |
| `board/bruno-martorano.html` | Replaced legacy 5-paragraph bio with updated 5-paragraph bio matching spreadsheet version, emphasising emerging markets, ethical finance, and sustainable growth. |
| `board/daniel-roubeni.html` | Replaced placeholder bio with full 3-paragraph bio covering Bocconi/NYU credentials, multilingual background, and global entrepreneurship. |
| `board/david-grunfeld.html` | Replaced placeholder bio with full 2-paragraph bio covering Prose Solutions, PS NXT, angel investments, and UAE network. Also updated meta/OG descriptions. |
| `board/david-parker.html` | Replaced generic bio with updated bio referencing Co-Founder of Konsentus, Saatchi background, and NED roles (3S Money, Swiipr, Nymcard, Itemize, Curve). Also updated meta/OG descriptions. |

### Main Site — Team Profile Pages

| File | Change |
|------|--------|
| `team/amit-varma.html` | Replaced legacy CIO/fintech products bio with updated 2-paragraph bio focusing on digital assets, DeFi, payments infrastructure, and regulatory expertise. |
| `team/bijna-kotak-dasani.html` | Replaced legacy bio with updated 3-paragraph bio focusing on digital assets, DeFi, MBE, and commitment to ethical investment. |

### Sub-Sites

| File | Change |
|------|--------|
| `subdomains/fintech/index.html` | Updated David Parker's team card bio from generic description to specific Konsentus/Saatchi/NED credentials matching the spreadsheet. |

---

## ⚠️ Flag for Review — Amit Varma Role Title

The spreadsheet's `Main Site Bio (Full Text)` field for Amit Varma opens with **"Amit Varma is Chief Investment Officer at Taranis Capital..."** however his `Role (Main Site)` column is set to **"Chief Information Officer"**. The bio text has been updated as written in the spreadsheet. Please confirm the correct title and update manually if needed.

---

## Profiles Not Updated (Spreadsheet Data Unavailable)

Due to file truncation, the following people's spreadsheet data could not be read. Their profile pages were left unchanged:

- Emad Zowawi
- All remaining Board Advisers (Ghassan Najmeddin, Jack Hollander, Joel Blake, Leif Hesse, Mazen Al-Rahim, Michael Boevink, Mohammed AlJumah, Osama Al-Thanon, Osama Al-Zamil, Rayan Al-Karawi, Sarah Sinclair, Tarek El-Mans)
- All remaining Team Members (Mark Walker, Milan Radia, Mohamed Essam, Nicholas Bingham, Osama Bukhari, Svitlana Burlakova)

**Recommendation:** Re-save the `Taranis-People-Data-Collection.xlsx` file and re-run this task to update the remaining profiles.

---

## GitHub Push Commands

Run the following commands from your local clone of the repository to commit and push these changes.

### 1. Stage all changed files

```bash
cd /path/to/taraniscapital-website

git add board/amer-mahmood.html \
        board/asim-chohan.html \
        board/bruno-martorano.html \
        board/daniel-roubeni.html \
        board/david-grunfeld.html \
        board/david-parker.html \
        team/amit-varma.html \
        team/bijna-kotak-dasani.html \
        subdomains/fintech/index.html
```

### 2. Commit with a descriptive message

```bash
git commit -m "Update profile bios from People Data spreadsheet (9 Apr 2026)

- Dr Amer Mahmood: full KSU stem cell bio replacing placeholder
- Asim Chohan: full SVP/COO bio replacing placeholder
- Bruno Martorano: updated 5-para bio replacing legacy version
- Daniel Roubeni: full Bocconi/NYU bio replacing placeholder
- David Grunfeld: full Prose Solutions/PS NXT bio replacing placeholder
- David Parker: updated Konsentus/Saatchi/NED bio on profile + fintech sub-site
- Amit Varma: updated DeFi/digital assets bio replacing legacy CIO bio
- Bijna Kotak Dasani: updated MBE/digital assets bio replacing legacy version"
```

### 3. Push to GitHub

```bash
git push origin main
```

### 4. Deploy to AWS CloudFront (if applicable)

If you use the AWS CLI to deploy, invalidate the affected paths:

```bash
aws cloudfront create-invalidation \
  --distribution-id <YOUR_DISTRIBUTION_ID> \
  --paths \
    "/board/amer-mahmood.html" \
    "/board/asim-chohan.html" \
    "/board/bruno-martorano.html" \
    "/board/daniel-roubeni.html" \
    "/board/david-grunfeld.html" \
    "/board/david-parker.html" \
    "/team/amit-varma.html" \
    "/team/bijna-kotak-dasani.html" \
    "/fintech/*"
```

> Replace `<YOUR_DISTRIBUTION_ID>` with your CloudFront distribution ID. Based on the project log, the fintech distribution ID is `E260FGTXCVORQ6`. Check the AWS Infrastructure Summary document for IDs for other sub-sites.

---

*Generated automatically by the weekly-profile-updates scheduled task.*

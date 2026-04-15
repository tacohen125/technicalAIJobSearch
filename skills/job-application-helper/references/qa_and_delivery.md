# Quality Assurance & Delivery

## Table of Contents
- [Page Count Verification](#page-count-verification)
- [Page Gap Check](#page-gap-check)
- [Minimum Bullets Rule](#minimum-bullets-rule)
- [Publication Order Rule](#publication-order-rule)
- [Content Reduction Priority](#content-reduction-priority)
- [Verification Checklist](#verification-checklist)
- [Pre-Delivery Checklist](#pre-delivery-checklist)

## Page Count Verification

**NOTE: The baseline resume renders as 3 pages in LibreOffice.** `verify_page_count.sh` will always report 3 pages and is not a reliable gate. Use char count instead:

```bash
python scripts/para_utils.py chars unpacked/word/document.xml
```

**Char count is a rough proxy only — always tell the user to open the docx in Word and confirm exactly 2 pages before submitting.** Do not consider delivery complete until the user has confirmed the page count. A resume at 7400 chars can still render as 3 pages in Word if bullets wrap to 2 lines.

**Target char range: 7200–7350 chars.** Stay away from the 7430 ceiling — layout variance and line wrapping can push a borderline resume to 3 pages.

**Single-line bullet rule**: Keep all experience bullets under ~110 chars. Bullets in the 113–158 char range wrap to 2 lines; each wrap costs ~14pt of vertical space. Four extra wraps ≈ 56pt ≈ enough to push a borderline resume to 3 pages.

`verify_page_count.sh` is still useful for catching gross overflows (e.g., 4+ pages), but a "3 pages" result is expected and not a failure.

## Page Gap Check

**After the user confirms 2 pages, check for excess whitespace at the bottom of page 2.**

If more than ~2 blank lines remain at the bottom of page 2, add content to fill the gap — in this priority order:

1. **Restore a publication**: Add back a previously removed publication from the baseline if it is relevant to the target role. Prefer first-author publications; co-author papers are acceptable if the topic aligns with the job description.
2. **Add an experience bullet**: Add the next most-relevant bullet from `references/user_profile.md` > Complete Experience Bullets for the most relevant role, keeping it under 110 chars.
3. **Expand a trimmed bullet**: Slightly lengthen a bullet that was shortened aggressively, up to but not exceeding 110 chars.

A char count near the bottom of the range (6970–7100) is a signal that a gap likely exists. Target **7200–7350 chars** to use the page fully.

## Minimum Bullets Rule

**Every experience role must have a minimum of 3 bullet points.**

When cutting content to hit the 2-page limit, never reduce any role below 3 bullets. Cut from publications or trim bullet length instead. After all edits, count bullets under each role header before packing — if any role has fewer than 3, add the most relevant bullet from `references/user_profile.md` > Complete Experience Bullets.

## Publication Order Rule

**Publications must be listed in reverse chronological order (newest first).**

When adding, restoring, or reordering publications, sort by year descending. When inserting a restored publication, place it at the position that maintains reverse chronological order — do not simply append or insert at a fixed index. After any publication change, verify the full list is still in reverse year order before packing.

## Content Reduction Priority

If resume exceeds 2 pages, follow the content reduction strategy in `references/xml_editing_guide.md` > Content Reduction Strategy.

## Verification Checklist

Before presenting materials, verify:

1. **LPS optimization**:
   - ✓ Keywords appear in first third of resume
   - ✓ Job title or similar appears in Summary/Branding
   - ✓ Key technologies mentioned in job description appear 2-3 times
   - ✓ Parallel language used throughout

2. **Formatting consistency**:
   - ✓ Matches baseline template exactly (spacing, indents, fonts)
   - ✓ No formatting inconsistencies
   - ✓ Section headers match baseline casing (NOT all caps unless baseline is)
   - ✓ Professional appearance maintained

3. **Content accuracy**:
   - ✓ All claims are truthful and drawn from actual experience
   - ✓ Dates and companies are accurate
   - ✓ Metrics and achievements are verifiable

4. **Readability**:
   - ✓ Natural language flow (not keyword-stuffed)
   - ✓ Clear, concise sentences
   - ✓ Logical progression of ideas

5. **Structure**:
   - ✓ Every experience role has at least 3 bullets
   - ✓ Publications are in reverse chronological order (newest first)
   - ✓ No duplicate content across bullets (especially FAT/SAT, vendor work, specific metrics)

## Pre-Delivery Checklist

Complete this checklist BEFORE delivering files to the user:

- [ ] **PAGE COUNT: Instruct user to open docx in Word and confirm exactly 2 pages**
- [ ] **CHAR COUNT: Total chars in target range 7200–7350 (run `para_utils.py chars`)**
- [ ] **BULLET LENGTH: All experience bullets ≤110 chars (run `para_utils.py list` and check)**
- [ ] **MIN BULLETS: Every experience role has ≥3 bullets**
- [ ] **PAGE GAP: No more than ~2 blank lines at bottom of page 2**
- [ ] **PUB ORDER: Publications in reverse chronological order**
- [ ] **FORMATTING: All spacing, indentation, fonts match baseline exactly**
- [ ] **KEYWORDS: Top 10 job requirement keywords appear in first third of resume**
- [ ] **ACCURACY: All dates, companies, and metrics are correct**
- [ ] **NO DUPLICATES: No bullet point content repeated across sections**
- [ ] **FILE NAMING: Files follow naming convention**
- [ ] **OUTPUT FOLDER: Files are in `assets/outputs/[YYMMDD]-[Company]-[Role]/`**
- [ ] **CLEANUP: All unpacked directories removed**

If any item is unchecked, DO NOT deliver. Fix the issue first.

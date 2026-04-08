# Quality Assurance & Delivery

## Table of Contents
- [Page Count Verification](#page-count-verification)
- [Content Reduction Priority](#content-reduction-priority)
- [Verification Checklist](#verification-checklist)
- [Pre-Delivery Checklist](#pre-delivery-checklist)

## Page Count Verification

**NOTE: The baseline resume renders as 3 pages in LibreOffice.** `verify_page_count.sh` will always report 3 pages and is not a reliable gate. Use char count instead:

```bash
python scripts/para_utils.py chars unpacked/word/document.xml
```

Keep the modified resume within ~200 chars of the baseline (7679 chars). If over budget, follow the Content Reduction Strategy in `references/xml_editing_guide.md` — starting with proactive publication cuts.

`verify_page_count.sh` is still useful for catching gross overflows (e.g., 4+ pages), but a "3 pages" result is expected and not a failure.

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

## Pre-Delivery Checklist

Complete this checklist BEFORE delivering files to the user:

- [ ] **PAGE COUNT: Resume is exactly 2 pages** (verified via PDF conversion)
- [ ] **FORMATTING: All spacing, indentation, fonts match baseline exactly**
- [ ] **KEYWORDS: Top 10 job requirement keywords appear in first third of resume**
- [ ] **ACCURACY: All dates, companies, and metrics are correct**
- [ ] **CONSISTENCY: Section headers match baseline casing**
- [ ] **FILE NAMING: Files follow naming convention**
- [ ] **LOCATION: Files are in /mnt/user-data/outputs/**
- [ ] **CLEANUP: Unpacked directories removed (unless --keep-unpacked for debugging)**

If any item is unchecked, DO NOT deliver. Fix the issue first.

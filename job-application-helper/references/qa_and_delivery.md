# Quality Assurance & Delivery

## Table of Contents
- [Page Count Verification](#page-count-verification)
- [Content Reduction Priority](#content-reduction-priority)
- [Verification Checklist](#verification-checklist)
- [Pre-Delivery Checklist](#pre-delivery-checklist)

## Page Count Verification

**MANDATORY - DO THIS FIRST:**
```bash
bash scripts/verify_page_count.sh [resume_filename].docx
```
This converts to PDF, checks the page count, and exits non-zero if not exactly 2 pages. If it fails, reduce content before proceeding.

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

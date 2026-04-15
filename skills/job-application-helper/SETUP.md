# Setup Guide — job-application-helper

This guide covers everything a new user needs to do before running their first job application.

## Prerequisites

| Tool | Required | Purpose |
|------|----------|---------|
| Python 3.8+ | Yes | XML editing, char counting, pack/unpack |
| `lxml` Python package | Yes | XML parsing (`pip install lxml`) |
| LibreOffice | Optional | Page count verification |
| Poppler (`pdfinfo`) | Optional | Page count verification (used by LibreOffice step) |

LibreOffice and Poppler are only needed for automated page count checks. You can run without them and verify page count manually by opening the `.docx` in Word.

---

## Step 1 — Add Your Baseline Resume

Replace the placeholder baseline with your own resume:

```
assets/Ted_Cohen-RESUME.docx
```

This file is the source that every tailored resume is copied from. It must be a `.docx` file. The skill edits it directly via XML — its formatting, fonts, spacing, and section structure become the template for all output resumes.

**Requirements for your baseline:**
- Must render as **exactly 3 pages** in Microsoft Word (the skill trims to 2 pages per application)
- Should include all experience, publications, and skills you might ever want to draw from
- Use standard fonts (Arial recommended) and no text boxes, tables, or multi-column layouts

> If your baseline is already 2 pages or is 4+ pages, the calibration ratios will still work but the computed char count targets will be approximations. Manual tuning may be needed after your first application.

---

## Step 2 — Run the Baseline Setup Script

After placing your resume, run the calibration script to compute the correct char count targets for your document:

```bash
cd skills/job-application-helper
bash scripts/setup_baseline.sh
```

This script:
1. Unpacks your baseline and counts its total characters
2. Checks its page count with LibreOffice (if installed)
3. Computes calibrated 2-page char count ranges using empirical ratios
4. Automatically updates `references/xml_editing_guide.md` and `references/qa_and_delivery.md` with your values

**Example output:**
```
=== Baseline Resume Setup ===
Baseline: assets/Ted_Cohen-RESUME.docx

Step 1: Measuring baseline char count...
  Baseline char count: 7679

Step 2: Checking baseline page count with LibreOffice...
  Baseline page count: 3
  OK: Baseline is 3 pages as expected.

Step 3: Computing calibrated 2-page char count ranges...
  Baseline chars:      7679
  2-page floor:        6970   (too sparse below this)
  2-page ceiling:      7430   (risk of 3 pages above this)
  Target range:        7200–7350 (recommended sweet spot)

Step 4: Updating reference files...
  Updated: references/xml_editing_guide.md
  Updated: references/qa_and_delivery.md
```

### Options

```bash
# Skip LibreOffice (if not installed)
bash scripts/setup_baseline.sh --no-verify

# Preview computed values without modifying any files
bash scripts/setup_baseline.sh --dry-run

# Use a baseline at a different path
bash scripts/setup_baseline.sh --baseline path/to/MyResume.docx
```

---

## Step 3 — Verify the Calibration

The char count ranges are **estimates** based on empirical ratios from the original baseline. Word and LibreOffice render documents slightly differently, so the ranges may need minor adjustment for your specific resume.

To verify:
1. Run your first tailored application through the full skill workflow
2. Open the output `.docx` in **Microsoft Word** and confirm it is exactly 2 pages
3. Check its char count: `python scripts/para_utils.py chars unpacked/word/document.xml`
4. If the resume is 2 pages and the char count is **outside** the target range, you have two calibration data points — update the ceiling or floor in `references/xml_editing_guide.md` to match what you observed

---

## Step 4 — Update the Skill's Name References (Optional)

The skill files contain "Ted Cohen" in several places. If you want cleaner output for your own name:

- `scripts/prepare_resume.sh` — hardcodes `Ted_Cohen-RESUME.docx` as the baseline filename
- `scripts/prepare_cover_letter.sh` — hardcodes `Ted_Cohen-COVERLETTER.docx`
- `SKILL.md` — references `Ted_Cohen-RESUME.docx` and `Ted_Cohen-COVERLETTER.docx`

These are cosmetic references — the skill works correctly regardless. But if you want output files named after you, update these references and rename the asset files accordingly.

---

## Step 5 — Update User Profile and References

Edit the following files in `references/` to reflect your background:

| File | What to update |
|------|---------------|
| `user_profile.md` | Your role, experience, competencies, and complete experience bullets |
| `list_of_key_accomplishments.md` | Your top 3–5 accomplishments with metrics |
| `list_of_target_companies.md` | Your target companies and roles |

These files are the primary source Claude uses when selecting and writing resume content. The more complete and accurate they are, the better the tailoring.

---

## Troubleshooting

**`verify_page_count.sh` reports 3 pages even after cutting content**
LibreOffice renders documents slightly differently than Word. Use char count as your primary gate and verify in Word manually. See `references/qa_and_delivery.md` for guidance.

**Script can't find Python**
The script looks for `python3` then `python`. Make sure one is in your PATH and has `lxml` installed (`pip install lxml`).

**LibreOffice step fails with a path error**
LibreOffice can fail on paths with spaces. The script copies to a temp directory to avoid this, but if the issue persists, use `--no-verify` and check page count manually in Word.

**Char count is in range but resume is still 3 pages**
Experience bullets longer than ~110 characters wrap to 2 lines in Word. Each extra wrap adds ~14pt of height. Check for long bullets:
```bash
python scripts/para_utils.py list unpacked/word/document.xml
```
Any experience bullet over 110 chars should be shortened.

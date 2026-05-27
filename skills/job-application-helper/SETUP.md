# Setup Guide — job-application-helper

This guide covers everything a new user needs to do before running their first tailored job application.

## Prerequisites

| Tool | Required | Purpose |
|------|----------|---------|
| Python 3.8+ | Yes | Onboarding, XML editing, char counting, pack/unpack |
| `python-docx` | Yes | Resume parsing (`pip install python-docx`) |
| `lxml` | Yes | XML parsing (`pip install lxml`) |
| LibreOffice | Optional | Page count verification |
| Poppler (`pdfinfo`) | Optional | Page count verification (used by LibreOffice step) |

LibreOffice and Poppler are only needed for automated page count checks. You can run without them and verify page count manually by opening the `.docx` in Word.

---

## Step 1 — Run the Onboarding Script

Run `onboard.py` with your baseline resume. This single command handles everything:

```bash
cd skills/job-application-helper
python scripts/onboard.py --resume /path/to/Your_Resume.docx
```

**What it does automatically:**
1. Parses your resume — detects your name, contact info, sections, and experience bullets
2. Copies your resume to `assets/` under a clean `FirstName_LastName-RESUME.docx` filename
3. Writes `config.sh` so all scripts know your filename
4. Scaffolds `references/user_profile.md` pre-populated with your actual bullet text
5. Scaffolds `references/list_of_key_accomplishments.md` from your resume's accomplishments section
6. Creates a blank `references/list_of_target_companies.md`
7. Calibrates char count targets for your specific resume

**Optional flags:**
```bash
# Also set up a cover letter template
python scripts/onboard.py --resume /path/to/resume.docx \
                           --cover-letter /path/to/coverletter.docx

# Override the auto-detected name
python scripts/onboard.py --resume /path/to/resume.docx --name "Jane Doe"

# Preview what would happen without writing any files
python scripts/onboard.py --resume /path/to/resume.docx --dry-run

# Overwrite existing files without prompting (re-onboarding)
python scripts/onboard.py --resume /path/to/resume.docx --force
```

---

## Step 2 — Fill In Your Details

After onboarding, open the scaffolded reference files and complete them:

### `references/user_profile.md`
Most sections are pre-populated from your resume. Review and complete:
- **Basic Information** — verify contact details, add location if missing, add GitHub/portfolio if applicable
- **Professional Summary** — polish the draft pulled from your resume into a 2–3 sentence branding statement
- **Key Competencies** — clean up the skill lines detected from your Skills section
- **Work Experience** — bullets are populated from your resume; add any that are missing or tweak wording
- **Education** — verify institution/degree lines parsed from your resume
- **Target Roles** — fill in the role types, industries, and locations you are targeting

#### Adding extra experience bullets

The onboarding script copies only the bullets on your current resume. Claude selects the most relevant subset per application, so it pays to give it more material to choose from — especially for older roles or accomplishments that didn't make the cut when you last trimmed your resume.

To add more bullets, open `references/user_profile.md`, find the relevant `### Company Name` section under **Work Experience**, and append additional bullet lines:

```markdown
### Acme Corp — Seattle, WA
**Senior Engineer**  |  Jan 2020 – Jun 2022

- (bullet already pulled from resume)
- (bullet already pulled from resume)
- Additional bullet describing an accomplishment not currently on your resume
- Another alternate phrasing or metric-rich version of an existing bullet
```

There is no limit on how many bullets you add per role. Bullets that don't fit the 2-page target are simply not selected for a given application.

#### Adding publications and presentations

If `onboard.py` detected a publications or presentations section in your resume, those entries were auto-populated. If not — or if you want to add entries beyond what the parser found — add the sections manually at the bottom of `user_profile.md`, just before **Target Roles**:

```markdown
## Select Publications

1. Author, A; Author, B; Your Name. "Title of Paper." Journal Name Year, Volume, Page.
2. Your Name; Author, B. "Another Paper Title." Conference Proceedings Year.

---

## Select Presentations

1. Talk Type, Your Name. "Presentation Title." Conference Name: City, State, Month Year.
2. Poster, Your Name; Co-Author. "Poster Title." Symposium Name: City, Country, Month Year.
```

Claude uses these lists when tailoring resumes for roles where publications or presentations add credibility (research scientist, staff engineer, academic-adjacent roles). Add as many entries as you have — the skill selects the most relevant subset per application.

### `references/list_of_key_accomplishments.md`
If your resume had an accomplishments section, entries are pre-populated. For each:
- Verify the metrics are accurate and current
- Add the `[Add metrics]` detail for any entries that lack quantification
- Add tags (e.g., `leadership`, `technical`, `cross-functional`)

### `references/list_of_target_companies.md`
Fill in the companies and roles you are actively targeting. Used during cover letter research.

---

## Step 3 — Verify the Calibration

The char count ranges computed by `onboard.py` are estimates based on empirical ratios. Word and LibreOffice render documents slightly differently, so ranges may need minor adjustment.

To verify:
1. Run your first tailored application through the full skill workflow
2. Open the output `.docx` in **Microsoft Word** and confirm it is exactly the right number of pages
3. Check its char count: `python scripts/para_utils.py chars unpacked/word/document.xml`
4. If the page count in Word doesn't match expectations, re-run with a corrected target:
   ```bash
   bash scripts/setup_baseline.sh --target-pages 2 --no-verify
   ```

---

## Manual Setup (Alternative to onboard.py)

If you prefer to configure manually:

1. **Copy your resume to `assets/`** — use the naming convention `FirstName_LastName-RESUME.docx`

2. **Create `config.sh`** from the template:
   ```bash
   cp config.template.sh config.sh
   # Edit config.sh with your name and TARGET_PAGES
   ```

3. **Run `setup_baseline.sh`** to calibrate char count targets:
   ```bash
   bash scripts/setup_baseline.sh --no-verify
   ```

4. **Fill in reference files** in `references/` — use the blank templates in `templates/` as a starting point, or see Step 2 above for what each file needs.

---

## Troubleshooting

**`onboard.py` can't find my resume sections**
Run `python scripts/parse_resume.py your_resume.docx --verbose` to see which signals fired for each paragraph. If your resume uses unusual formatting (e.g., all section headers are manually bolded with no Word heading styles), the heuristic scoring should still catch them. If not, open an issue with your resume's header formatting pattern.

**`verify_page_count.sh` reports wrong page count**
LibreOffice renders documents slightly differently than Word. Use char count as your primary gate and verify in Word manually. See `references/qa_and_delivery.md` for guidance.

**Script can't find Python**
The script looks for `python3` then `python`. Make sure one is in your PATH and has `lxml` and `python-docx` installed:
```bash
pip install lxml python-docx
```

**LibreOffice step fails with a path error**
LibreOffice can fail on paths with spaces. The script copies to a temp directory to avoid this, but if the issue persists, use `--no-verify` and check page count manually in Word.

**Char count is in range but resume is still the wrong page count**
Experience bullets longer than ~110 characters wrap to 2 lines in Word. Each extra wrap adds ~14pt of height. Check for long bullets:
```bash
python scripts/para_utils.py list unpacked/word/document.xml
```
Any experience bullet over 110 chars should be shortened.

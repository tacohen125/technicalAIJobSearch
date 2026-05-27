# Cover Letter Setup Guide

This guide explains how to set up a cover letter template for use with job-application-helper.

## What the skill expects

The skill expects a `.docx` cover letter at `assets/{COVERLETTER_BASENAME}` (set in `config.sh`).
It edits specific paragraphs via XML to tailor the letter for each application while preserving
your formatting exactly.

## Option A — Use the skill to generate your first cover letter

If you don't have a cover letter yet, you can ask the skill to draft one for you:

```
/job-application-helper
I need a cover letter template for my job search. Please draft one based on my
user_profile.md and save it to assets/ as a .docx file.
```

The skill will create a formatted .docx that becomes your template for future applications.

## Option B — Bring your own cover letter

If you already have a cover letter as a `.docx`:

1. Copy it to `assets/` with the correct filename:
   ```bash
   cp /path/to/your_cover_letter.docx assets/{FirstName_LastName}-COVERLETTER.docx
   ```
   (Use the same `FirstName_LastName` prefix as your resume.)

2. Add it during onboarding:
   ```bash
   python scripts/onboard.py --resume assets/Your_Resume.docx \
                              --cover-letter /path/to/cover_letter.docx
   ```

3. Create a `.md` mirror alongside the `.docx` — a plain-text version of your cover letter
   that Claude references for paragraph-length guidance during XML editing:
   ```
   assets/{FirstName_LastName}-COVERLETTER.md
   ```

## Cover letter structure

The skill edits these paragraph regions in your cover letter XML:

| Paragraph | Content |
|-----------|---------|
| RE line | `RE: [Role Title] – [Company Name]` |
| Date | Today's date |
| Salutation | `Dear [Hiring Manager / Hiring Team],` |
| Opening | Express enthusiasm for the role and company; connect your background |
| Body 1–2 | 2–3 accomplishments matching top job requirements (STAR format, with metrics) |
| Body 3 | Company knowledge — always web-searched for recent news/products |
| Closing | Reiterate enthusiasm, call to action |
| Sign-off | Your name and credentials — **do not edit** |

## Tips

- Keep each paragraph roughly the same length as in your template — this preserves
  the 1-page layout. Claude will reference your `.md` mirror for length guidance.
- Avoid tables, text boxes, or multi-column layouts in your cover letter template —
  these interfere with XML editing.
- The sign-off region should include your full name, credentials, and contact info
  pre-formatted — the skill will never edit this section.

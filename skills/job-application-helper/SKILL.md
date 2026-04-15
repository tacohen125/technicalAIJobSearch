---
name: job-application-helper
description: "Tailors resumes and cover letters for job applications using LinkedIn Parsing System (LPS) optimization. Use this skill when the user requests: (1) Creating or updating a resume for a specific job posting, (2) Writing or customizing a cover letter for a role, (3) Optimizing application materials for ATS/LPS systems, (4) Analyzing job descriptions to identify keyword matches and skill gaps, (5) Formatting resumes or cover letters to maintain professional standards while maximizing keyword density, or (6) Any task involving job application document preparation. This skill specializes in Technical Program Manager, Senior Integration Engineer, and Engineering Program Manager roles in Tech, Aerospace/Defense, and Outdoors industries, but is not limited to these."
---

# Job Application Tailoring

## Source Documents

- **Baseline Resume**: `assets/Ted_Cohen-RESUME.docx` (MUST be edited via XML, never recreated)
- **LinkedIn Profile**: https://www.linkedin.com/in/tacohen/ (for additional experience details)
- **Cover Letter Template**: `assets/Ted_Cohen-COVERLETTER.md` (for formatting structure)
- **Target Companies List**: `references/list_of_target_companies.md`

## Core Principles

### LinkedIn Parsing System (LPS) Optimization

Modern employers use LPS to screen resumes before human review. Your materials must:
- Include targeted keywords from the job description (especially in the first third of the resume)
- Use industry-standard terminology and role-specific language
- Avoid verbose descriptions that dilute keyword density
- Structure content for both machine parsing and human readability
- Quantify achievements with specific metrics
- Align experience descriptions with job requirements using parallel language

**Critical**: If a resume lacks proper formatting, targeted keywords, or alignment with job-specific requirements, it will be rejected before reaching human eyes. Issues like verbose descriptions, weak KSA (Knowledge, Skills, Abilities) responses, or outdated templates render applications invisible.

### Applicant Tracking System (ATS) Optimization

ATS software parses and stores resume data before human review. Ensure materials are ATS-compatible:
- **File format**: Always submit `.docx` for initial applications — PDFs may not parse correctly in all ATS platforms
- **Standard section headers**: Use recognizable headers (e.g., "Experience", "Education", "Technical Skills") so ATS can map content to the correct fields
- **Parseable structure**: Avoid tables, text boxes, multi-column layouts, and content in headers/footers — ATS systems often skip or misparse these elements
- **Simple formatting**: Use standard fonts (Calibri, Arial, Times New Roman) and avoid graphics, icons, or decorative elements that interfere with text extraction
- **Contact info placement**: Place name, email, phone, and LinkedIn URL in the main document body (not in a header/footer) so ATS can extract them into candidate fields

## User Profile

Read `references/user_profile.md` for the user's background, target roles, key competencies, and career goals. Consult this during job description analysis (Step 1) and when mapping experience to job requirements.

## Determining Scope

**CRITICAL: Only work on what the user explicitly requests. Do not assume additional deliverables.**

Before beginning work, identify the user's request:

**Application Materials:**
- **Resume only?** → Complete Steps 1-2 and 4-5 only
- **Cover letter only?** → Complete Steps 1, 3-5 only
- **Both resume and cover letter?** → Complete all Steps 1-5
- **Neither (research/prep only)?** → Skip to Additional Capabilities below

**Other Requests:**
- **Company research?** → Read `references/company_research.md` and perform web search
- **Interview preparation?** → Read `references/interview_preparation.md` and generate questions/responses
- **Skill gap analysis?** → Read `references/skill_gap_analysis.md` and analyze job requirements
- **Networking support?** → Read `references/networking_support.md` and draft outreach messages
- **LinkedIn profile support?** → Read `references/linkedin_profile_optimization.md` to optimize profile sections and content
- **LinkedIn interactions support?** → Read `references/networking_support.md` for connection requests and engagement strategies
- **Something else?** → Address the specific request using relevant references as needed

**If the request is ambiguous, ask for clarification before proceeding. Never assume the user wants more than what they explicitly asked for.**

## Workflow

### Step 1: Job Description Analysis

When provided with a job posting, immediately:

1. **Extract key requirements**:
   - Must-have qualifications vs. preferred qualifications
   - Technical skills and tools mentioned
   - Years of experience required
   - Educational requirements
   - Industry-specific knowledge

2. **Identify keyword clusters**:
   - Job-specific terminology (e.g., "Technical Program Manager", "cross-functional", "stakeholder management")
   - Technical tools and platforms (e.g., "Asana", "Jira", "Google Workspace")
   - Domain expertise (e.g., "AR/VR", "aerospace", "defense systems")
   - Soft skills (e.g., "leadership", "communication", "strategic planning")
   - Action verbs used in the posting (e.g., "led", "managed", "delivered", "coordinated")

3. **Map to user's experience**:
   - Identify direct experience matches
   - Find transferable skills from adjacent domains
   - Note skill gaps that need addressing or de-emphasizing
   - Highlight unique differentiators

### Step 2: Resume Tailoring

**CRITICAL REQUIREMENT: The final resume MUST NOT exceed 2 pages. This is non-negotiable. Plan your edits with this constraint in mind.**

**CRITICAL: Use XML-Based Editing Approach**

The baseline resume must be edited directly using XML manipulation to preserve exact formatting. **Never recreate the resume from scratch using docx-js or similar libraries**, as this inevitably introduces spacing, formatting, and structural inconsistencies.

**Before you begin editing:**
1. Assess which sections are most relevant to the target role
2. Identify which bullets may need to be shortened or removed if length becomes an issue
3. Plan keyword integration into existing bullet points rather than adding new content

#### Required Process:

**Option A: Automated workflow with cleanup (Recommended)**

```bash
bash scripts/create_tailored_resume.sh [output_filename].docx
```

This orchestrator handles preparation, editing, packing, verification, and automatic cleanup. The workflow:
1. Prepares resume (copies baseline and unpacks to timestamped directory)
2. Prompts you to edit XML at `unpacked_[timestamp]/word/document.xml`
3. Packs edited XML back to .docx
4. Verifies page count (2 pages required)
5. Automatically cleans up unpacked directory on success

**Flags:**
- `--keep-unpacked`: Preserve unpacked directory for debugging
- `--unpacked-dir <dir>`: Use custom directory name instead of timestamp
- `--no-verify`: Skip page count verification

**Option B: Manual workflow (for debugging)**

> ⚠️ **Existing output files**: If the file already exists in `assets/outputs/`, do NOT use `prepare_resume.sh` or `create_tailored_resume.sh` — both unconditionally overwrite the target with the baseline, destroying prior edits. Instead, unpack directly:
> ```bash
> python scripts/unpack.py assets/outputs/[FOLDER]/[FILENAME].docx [unpacked_dir]
> ```
> Only use the prepare/create scripts when starting a brand-new tailored resume for the first time.

Use individual scripts for granular control:

1. **Copy and unpack the baseline resume** (new files only — see warning above):
   ```bash
   bash scripts/prepare_resume.sh [output_filename].docx [unpacked_dir]
   ```
   This copies the baseline resume and unpacks it to XML. `unpacked_dir` defaults to `unpacked/`.

2. **Edit the XML directly** using `str_replace` tool on `unpacked/word/document.xml`. Read `references/xml_editing_guide.md` for all formatting rules, protected attributes, and baseline patterns before editing.

3. **Pack the edited XML back to .docx**:
   ```bash
   python3 <pack_script_path> unpacked/ [output_filename].docx --original <skill_dir>/assets/Ted_Cohen-RESUME.docx
   ```

   The `pack_script_path` will be shown by `prepare_resume.sh`. It's searched in order: `scripts/pack.py` (local), `/mnt/skills/public/docx/scripts/office/pack.py` (browser), or `~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/docx/ooxml/scripts/pack.py` (CLI).

4. **Clean up manually** (remember to do this):
   ```bash
   bash scripts/cleanup_unpacked.sh [unpacked_dir] --force
   ```

#### Content Modifications (via XML editing):

> **Note:** For exact XML attributes (bold tags, bullet numbering, spacing, etc.) for each section below, see `references/xml_editing_guide.md` > Section-Specific Formatting.

This requirement takes precedence over all other optimizations. If keyword density and page count conflict, page count wins. A 2-page resume with 70% keyword match is better than a 3-page resume (which is not allowed) with 80% keyword match.

1. **Branding Title** (bold text, no section header):
   - Located immediately after LinkedIn URL
   - Bold text, typically 1-2 lines
   - Tailor to match the job posting's specific role title or focus area
   - Be exact and concise
   - Example: "Senior Technical Program Manager" or "Technical Program Manager - AR/VR Systems"

2. **Branding Statement** (paragraph after branding title):
   - No section header (continues directly after branding title)
   - Keep to 3-4 sentences maximum
   - Regular text (not bold)
   - Lead with role-relevant keywords
   - Include 2-3 keywords from top requirements
   - Highlight years of experience matching requirements
   - Mention specific domains/industries relevant to role

3. **Areas of Expertise section** (if present in baseline):
   - Section header: "Areas of Expertise" (NOT all caps)
   - Format: Up to 4 lines of expertise areas separated by pipes (|)
   - Example: `Strategic Planning & Execution | Cross-functional Collaboration | Technical Program Management | Stakeholder Engagement`
   - Include key competency areas that match target role priorities
   - Reorder items to prioritize job-relevant expertise first
   - May adjust items based on job requirements while staying truthful

4. **Skills section**:
   - Section header: "Skills" (NOT all caps)
   - Format: Up to 4 bullets containing 2 lines each of skill lists
   - The summary category for each bullet should be bolded
   - Example: **Nanofabrication & Process Integration:** Pilot‑scale process development, lithography and advanced patterning, optical materials processing, DFM/DFT, quality control, DOE/SPC, FMEA and root cause analysis.
   - Contains mixed content: technical skills, leadership skills, programming languages
   - Reorder items to prioritize job-relevant skills first
   - Add/remove skills based on job requirements while staying truthful
   - Only use skills from the Key Competency section of `references/user_profile.md`
   - Keep format concise and scannable for ATS parsing
   - **Do not list specific product families** (e.g., "micro-LED", "compound semiconductor") in the skills bullets — these belong in experience bullets and accomplishments. Skills should name capabilities, not products.

5. **Key Accomplishments section**:
   - Section header: "Key Accomplishments" (NOT all caps)
   - Choose the 3 accomplishments that match the job best, from baseline, `references/list_of_key_accomplishments.md`, or rewrite existing ones
   - Reorder by relevance: most relevant first
   - Keep accomplishment titles consistent
   - Each accomplishment has first few, most impactful words in bold, rest regular
   - Avoid including responsibility and excessive details here. That content should be included in the experience section
   - Inject keywords naturally while maintaining truthfulness
   - **No recycling rule**: Each KA must describe a distinct outcome not already covered by an experience bullet. If a KA and an experience bullet describe the same work using the same metrics or phrasing, rewrite one of them. The KA should capture a broader impact or a different angle, not restate the bullet. When in doubt, use an accomplishment from `references/list_of_key_accomplishments.md` rather than constructing a new one from experience bullets.

6. **Experience section**:
   - Section header: "Experience" (NOT all caps)
   - Company line format: **Company Name**[TAB]Location (company name bold, location regular)
   - Title line format: Job Title[TAB]Dates (both regular text, title may be underlined)
   - **Before selecting bullets**: Read ALL bullets under the matching role in `references/user_profile.md` > Complete Experience Bullets. Score each against the job description keywords. If a user_profile.md bullet has a stronger keyword match than the corresponding baseline bullet, replace the baseline bullet with the user_profile.md version. Do not skip bullets in user_profile.md simply because they don't appear in the baseline — they may be more relevant.
   - Bullets use numbering
   - Reorder bullets within each position to prioritize job-relevant experience
   - Take care to not repeat content that is already in the Key Accomplishment section
   - **Deduplication**: After drafting all bullets, do a pass across the full resume (summary, accomplishments, skills, all experience bullets) and flag any specific phrase, clause, or list of items that appears more than once. Rephrase or remove the less prominent instance. Pay special attention to technical lists (e.g., "lithography, etch, wet, films, metrology") — each distinct list should appear at most once. When a bullet already names specific process steps, subsequent bullets should refer to the work by outcome or flow name (e.g., "during grating fabrication flows") rather than re-listing the steps.
   - **Use specific program and product names**: When `references/user_profile.md` or the job description mentions a specific program name (e.g., "Orion", "Project X"), use it in accomplishments and experience bullets rather than generic descriptions. Specificity adds credibility and differentiates the resume.
   - Update bullet text to inject keywords from job posting
   - Use parallel language from job description
   - Quantify all achievements with specific metrics (team sizes, budget amounts, project scales)
   - Mirror the job posting's specific terminology rather than using generic language
   - **Page breaks**: Ensure page breaks fall either mid-bullet-list for a single job, or between jobs — never between a job header and its first bullet. If a page break would orphan a job header, insert a page break paragraph immediately before that header. See `references/xml_editing_guide.md` > Page Breaks for implementation.

7. **Keyword density optimization**:
   - Aim for 60-80% keyword match with job description
   - Place highest-priority keywords in first third (branding + summary + accomplishments)
   - Use keywords in context, not as keyword stuffing
   - Mirror exact phrases from job posting when accurate

If the resume exceeds 2 pages, follow the content reduction strategy in `references/xml_editing_guide.md` > Content Reduction Strategy.

For formatting rules and protected attributes, see `references/xml_editing_guide.md` > Formatting Rules.

#### Publications and Presentations: Mandatory Format Preservation

When adding, restoring, or modifying any publication or presentation entry, you **MUST** reproduce the exact run-level formatting from the original baseline resume. Never use `replace_all_runs()` for these entries — they require mixed formatting across multiple runs.

**Publication format** (each entry is one `ListParagraph` paragraph):
- Author list: plain text, except `Cohen, T. A` which is always **underlined**
- Article/book title: plain text
- Journal/venue name: *italic*
- Year: **bold**
- Volume, issue, page: plain text

**Presentation format** (each entry is two paragraphs):
- Para 1 (`ListParagraph`): citation line with run-level formatting:
  - Presentation type (e.g., "Invited Seminar", "GRC Poster Award"): **bold**
  - `Cohen, T. A`: **underlined**
  - Conference/venue name: *italic*
  - Year: **bold**
  - All other text: plain
- Para 2 (no style / empty `pPr` style): talk title in quotes, all plain text

**To restore a removed entry**: copy the XML paragraph(s) from the baseline `unpacked_baseline_inspect/word/document.xml` directly — do not reconstruct from scratch. Unpack the baseline temporarily if needed (`bash scripts/prepare_resume.sh` or copy + unpack manually), copy the target paragraph's XML verbatim, then clean up.

### Step 3: Cover Letter Tailoring

**CRITICAL: Use XML-Based Editing Approach**

The cover letter template (`assets/Ted_Cohen-COVERLETTER.docx`) must be edited via XML to preserve exact formatting — never recreate from scratch.

#### Required Process:

```bash
bash scripts/prepare_cover_letter.sh [output_filename].docx [unpacked_dir]
```

This copies the template and unpacks it. Then:
1. Edit XML at `unpacked_cl/word/document.xml`
2. Pack: `python scripts/pack.py unpacked_cl/ [output_filename].docx --original assets/Ted_Cohen-COVERLETTER.docx`
3. Verify 1 page: `bash scripts/verify_page_count.sh [output_filename].docx 1`
4. Clean up: `bash scripts/cleanup_unpacked.sh unpacked_cl/ --force`

#### Paragraphs to Edit:

- **P005** — RE line: `RE: [Role Title] – [Company Name]`
- **P007** — Date: e.g., `March 10, 2026`
- **P009** — Salutation: `Dear [Hiring Manager / Hiring Team],`
- **P011** — Opening paragraph
- **P013** — Body paragraph 1 (UW + Meta lithography)
- **P015** — Body paragraph 2 (Meta metrology)
- **P017** — Body paragraph 3 (company knowledge — always use web search)
- **P019** — Closing paragraph
- **P021–P026** — Sign-off and credentials — **DO NOT EDIT**

Aim to maintain the same paragraph lengths as in `assets/Ted_Cohen-COVERLETTER.md`.

**Content strategy**:

1. **Opening paragraph**:
   - Express genuine enthusiasm for the specific role and company
   - Mention how the user learned about the position (if known)
   - Include a compelling hook connecting background to role

2. **Body paragraphs (2-3 paragraphs)**:
   - Paragraph 1-2: Highlight 2-3 accomplishments directly matching top requirements
     - First paragraph focuses on University of Washington and Meta lithography experience.
     - Second paragraph highlights Meta Metrology experience.
     - Use STAR method elements (Situation, Task, Action, Result)
     - Include specific metrics and outcomes.
     - Draw from Meta, HCL Tech, and University of Washington experiences as relevant.
     - Avoid repeating very specific details that are already in my resume.

   - Paragraph 3: Demonstrate company knowledge and cultural fit
     - **Always use web search** to find recent company news, products, or initiatives
     - Reference specific recent developments (partnerships, product launches, expansions)
     - Explain alignment with company mission/values
     - Show how career goals align with company trajectory

   - Optional Paragraph 3: Address unique qualifications or explain career transitions

3. **Closing paragraph**:
   - Reiterate enthusiasm
   - Thank them for consideration
   - Include call to action ("I would welcome the opportunity to discuss...")
   - Keep professional but warm

### Step 4: Quality Assurance

Read `references/qa_and_delivery.md` and complete all verification and pre-delivery checklists before proceeding to delivery. Page count verification is mandatory and must be done first.

**Page gap check (mandatory after page count passes):**
Open the PDF and inspect the bottom of each page. If any page has more than ~3 blank lines of unused space at the bottom:
1. **Preferred fix**: Add a bullet from the relevant role's section in `references/user_profile.md` to fill the gap. Choose the bullet with the strongest keyword match to the job description that is not already represented in the resume.
2. **If adding a bullet would exceed 2 pages**: Shorten an existing verbose bullet in the same role to make room, then add the new one.
3. **If a forced page break caused the gap**: Consider whether removing or repositioning the page break would produce a better layout (e.g., if the following section fits cleanly on page 1 with room to spare).
After any gap fix, re-run `verify_page_count.sh` to confirm the resume is still exactly 2 pages.

### Step 5: Delivery

**Output folder creation (mandatory)**:

Create a dated output folder under `assets/outputs/`:
```bash
FOLDER="assets/outputs/[YYMMDD]-[CompanyName]-[RoleTitle]"
mkdir -p "${FOLDER}"
```

- Use today's date in `YYMMDD` format (e.g., `260310` for March 10, 2026)
- No spaces in folder name — use hyphens throughout (e.g., `260310-Google-ProcessIntegrationEngineer`)

**Files to place in the folder**:
1. Resume: `Ted_Cohen-RESUME-[CompanyName]-[RoleTitle].docx`
2. Cover letter: `Ted_Cohen-COVERLETTER-[CompanyName]-[RoleTitle].docx`
3. Job description: `job_description.md` — a markdown file containing the full job description text provided by the user

**Steps**:
```bash
mkdir -p assets/outputs/[YYMMDD]-[CompanyName]-[RoleTitle]
mv Ted_Cohen-RESUME-[CompanyName]-[RoleTitle].docx assets/outputs/[YYMMDD]-[CompanyName]-[RoleTitle]/
mv Ted_Cohen-COVERLETTER-[CompanyName]-[RoleTitle].docx assets/outputs/[YYMMDD]-[CompanyName]-[RoleTitle]/
# Write job_description.md with the job description text
```

- Provide brief summary of key changes made

## Additional Capabilities

- **Company Research**: Read `references/company_research.md`. Always use web search before writing cover letters.
- **Interview Preparation**: Read `references/interview_preparation.md` for practice questions, STAR response crafting, and format-specific prep.
- **Skill Gap Analysis**: Read `references/skill_gap_analysis.md` to compare user qualifications against job requirements.
- **Networking Support**: Read `references/networking_support.md` for LinkedIn outreach, cold emails, and networking strategy.
- **LinkedIn Profile Optimization**: Read `references/linkedin_profile_optimization.md` for profile sections, headline, about section, skills management, and visibility strategies.
- **LinkedIn Interactions**: Read `references/networking_support.md` for connection requests and engagement best practices.

## Important Notes

- **Always be truthful**: Never fabricate experience or skills
- **Maintain user voice**: Keep professional tone consistent with user's communication style
- **Prioritize impact**: Focus on outcomes and results, not just activities
- **Stay current**: Use web search for company-specific information (especially for cover letters)
- **Be strategic**: Tailor each application specifically; generic applications fail LPS screening
- **Preserve formatting**: Use XML editing for resumes, never recreate from scratch

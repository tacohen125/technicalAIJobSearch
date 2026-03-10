---
name: job-application-helper
description: "Tailors resumes and cover letters for job applications using LinkedIn Parsing System (LPS) optimization. Use this skill when the user requests: (1) Creating or updating a resume for a specific job posting, (2) Writing or customizing a cover letter for a role, (3) Optimizing application materials for ATS/LPS systems, (4) Analyzing job descriptions to identify keyword matches and skill gaps, (5) Formatting resumes or cover letters to maintain professional standards while maximizing keyword density, or (6) Any task involving job application document preparation. This skill specializes in Technical Program Manager, Senior Integration Engineer, and Engineering Program Manager roles in Tech, Aerospace/Defense, and Outdoors industries, but is not limited to these."
---

# Job Application Tailoring

## Source Documents

- **Baseline Resume**: `assets/Jason_J_Garcia-RESUME.docx` (MUST be edited via XML, never recreated)
- **LinkedIn Profile**: https://www.linkedin.com/in/24-jason-j-garcia/ (for additional experience details)
- **Cover Letter Template**: `assets/Jason_J_Garcia-COVERLETTER.md` (for formatting structure)
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

Use individual scripts for granular control:

1. **Copy and unpack the baseline resume**:
   ```bash
   bash scripts/prepare_resume.sh [output_filename].docx [unpacked_dir]
   ```
   This copies the baseline resume and unpacks it to XML. `unpacked_dir` defaults to `unpacked/`.

2. **Edit the XML directly** using `str_replace` tool on `unpacked/word/document.xml`. Read `references/xml_editing_guide.md` for all formatting rules, protected attributes, and baseline patterns before editing.

3. **Pack the edited XML back to .docx**:
   ```bash
   python3 <pack_script_path> unpacked/ [output_filename].docx --original <skill_dir>/assets/Jason_J_Garcia-RESUME.docx
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

3. **Areas of Expertise section** (NEW in current baseline):
   - Section header: "Areas of Expertise" (NOT all caps)
   - Format: Up to 4 lines of expertise areas separated by pipes (|)
   - Example: `Strategic Planning & Execution | Cross-functional Collaboration | Technical Program Management | Stakeholder Engagement`
   - Include key competency areas that match target role priorities
   - Reorder items to prioritize job-relevant expertise first
   - May adjust items based on job requirements while staying truthful

4. **Technical Skills section**:
   - Section header: "Technical Skills" (NOT all caps)
   - Format: Up to 2 lines of pipe-separated skills (NOT bulleted)
   - Example: `Google Workspace | Microsoft Office Suite | Asana | Jira | Python | SQL | HTML/CSS`
   - Contains mixed content: enterprise tools, project management platforms, programming languages
   - Reorder items to prioritize job-relevant skills first
   - Add/remove skills based on job requirements while staying truthful
   - Keep format concise and scannable for ATS parsing

5. **Key Accomplishments section**:
   - Section header: "Key Accomplishments" (NOT all caps)
   - Choose the 3 accomplishments that match the job best, from baseline, `references/list_of_key_accomplishments.md`, or rewrite existing ones
   - Reorder by relevance: most relevant first
   - Each accomplishment has first few, most impactful words in bold, rest regular
   - Use bullet formatting
   - Inject keywords naturally while maintaining truthfulness

5. **Experience section**:
   - Section header: "Experience" (NOT all caps)
   - Company line format: **Company Name**[TAB]Location (company name bold, location regular)
   - Title line format: Job Title[TAB]Dates (both regular text, title may be underlined)
   - Bullets use numbering
   - Reorder bullets within each position to prioritize job-relevant experience
   - Update bullet text to inject keywords from job posting
   - Use parallel language from job description
   - Quantify all achievements with specific metrics (team sizes, budget amounts, project scales)
   - Mirror the job posting's specific terminology rather than using generic language

6. **Keyword density optimization**:
   - Aim for 60-80% keyword match with job description
   - Place highest-priority keywords in first third (branding + summary + accomplishments)
   - Use keywords in context, not as keyword stuffing
   - Mirror exact phrases from job posting when accurate

If the resume exceeds 2 pages, follow the content reduction strategy in `references/xml_editing_guide.md` > Content Reduction Strategy.

For formatting rules and protected attributes, see `references/xml_editing_guide.md` > Formatting Rules.

### Step 3: Cover Letter Tailoring

**Use docx-js for cover letter creation** (cover letters don't need the same formatting precision as resumes).

Refer to `assets/Jason_J_Garcia-COVERLETTER.md` for structure.

**Content strategy**:

1. **Opening paragraph**:
   - Express genuine enthusiasm for the specific role and company
   - Mention how the user learned about the position (if known)
   - Include a compelling hook connecting background to role

2. **Body paragraphs (2-3 paragraphs)**:
   - Paragraph 1: Highlight 2-3 accomplishments directly matching top requirements
     - Use STAR method elements (Situation, Task, Action, Result)
     - Include specific metrics and outcomes
     - Draw from Meta, Raytheon, or Northrop Grumman experiences as relevant
   
   - Paragraph 2: Demonstrate company knowledge and cultural fit
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

### Step 5: Delivery

**File naming and delivery**:
- Resume filename: `Jason_J_Garcia-RESUME-[CompanyName]-[RoleTitle].docx`
- Cover letter filename: `Jason_J_Garcia-COVERLETTER-[CompanyName]-[RoleTitle].docx`
- Copy final files to `/mnt/user-data/outputs/`
- Use `present_files` tool to share with user
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
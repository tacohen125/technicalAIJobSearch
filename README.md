# AI-Assisted Job Search Toolkit

A collection of Claude AI skills for comprehensive job search preparation — from crafting application materials to preparing for behavioral assessments.

## 📦 Available Skills

### 1. [Job Application Helper](./docs/job-application-helper.md)
**Tailors resumes and cover letters for specific job postings with LPS/ATS optimization**

![Resume example](./images/output-baseline-resumes-sidebyside.png)

**Key Features:**
- ✅ XML-based resume editing (preserves exact formatting)
- ✅ 60-80% keyword match targeting
- ✅ Cover letter generation with company research
- ✅ LinkedIn profile optimization and comparison
- ✅ 2-page resume enforcement

**Best For:** Research Scientist, Metrology Engineer, and Integration Engineer roles in photonics, semiconductors, and quantum technology

**Personalization:** ⚠️ **Required** — Must customize with your documents and background

[📖 Full Documentation](./docs/job-application-helper.md) | [📋 SKILL.md](./skills/job-application-helper/SKILL.md) | [⚙️ Setup Guide](./skills/job-application-helper/SETUP.md)

---

### 2. [Interview Study Guide](./docs/interview-study-guide.md)
**Generates comprehensive, role-specific technical interview study guides**

**Key Features:**
- ✅ Deep-dive technical sections on the role's core technologies (physics, process flows, failure modes)
- ✅ Explicit mapping of user's background to each job requirement
- ✅ Interview Q&A frameworks grounded in the user's actual experience
- ✅ Verified references with study-priority ratings (web-researched)
- ✅ Quick-fire facts table and day-before checklist

**Best For:** Research Scientist, Metrology Engineer, and Integration Engineer roles in photonics, semiconductors, and quantum technology

**Personalization:** ✅ **None Required** — Reads from job-application-helper's user_profile.md automatically

[📖 Full Documentation](./docs/interview-study-guide.md) | [📋 SKILL.md](./skills/interview-study-guide/SKILL.md)

---

### 3. [Likert Screening Tutor](./docs/likert-screening-tutor.md)
**Prepares candidates for Likert-scale behavioral screenings (Google Hiring Assessment format)**

**Key Features:**
- ✅ Practice questions across 8 behavioral categories
- ✅ Automated scoring with consistency checks
- ✅ Timed mock assessment sessions
- ✅ Strategic guidance for 85%+ alignment scores
- ✅ Red flag identification and improvement recommendations

**Best For:** Preparing for Google's Hiring Assessment and similar behavioral screenings used in tech hiring

**Personalization:** ✅ **None Required** — Works out of the box

[📖 Full Documentation](./docs/likert-screening-tutor.md) | [📋 SKILL.md](./skills/likert-screening-tutor/SKILL.md)

---

### 4. [Behavioral Story Optimization](./docs/behavioral-story-optimization.md)
**Maintains a STAR-format story library and generates role-tailored top 10 interview reference sheets**

**Key Features:**
- ✅ Incremental story watcher — detects new raw stories and auto-generates compressed STAR summaries
- ✅ Bulk summary regeneration from scratch
- ✅ Role-specific top 10 selector — ranks best stories against the job description from your outputs folder
- ✅ Quick-reference summary table + full story detail blocks for pre-interview study
- ✅ Windows Task Scheduler integration for automatic watcher on login

**Best For:** Preparing behavioral answers for any technical role interview; pairs with the interview-study-guide skill

**Personalization:** ⚠️ **Required** — Must populate `assets/rawStorySummary.md` with your own stories; requires an Anthropic API key for summary generation

[📖 Full Documentation](./docs/behavioral-story-optimization.md) | [📋 SKILL.md](./skills/behavioral-story-optimization/SKILL.md)

---

## 🤖 Agents

### [Resume Updater](./agents/resume-updater.md)
**Keeps the job-application-helper skill synchronized when your baseline resume changes**

This Claude Code subagent automatically reviews and updates all skill documentation, reference materials, scripts, and XML editing guides whenever you modify your baseline resume. It prevents drift between your resume and the skill's knowledge base.

**When to use:** After updating your baseline resume (`assets/Ted_Cohen-RESUME.docx`), run this agent to propagate changes across the entire skill.

**Key Capabilities:**
- Unpacks and analyzes resume XML structure for formatting changes
- Updates `xml_editing_guide.md` with current section patterns and protected attributes
- Synchronizes reference materials (accomplishments, user profile, skills inventory)
- Validates all scripts against the updated baseline
- Performs cross-referential consistency checks across all documentation
- Generates a change log documenting what was updated

**Platform:** Claude Code CLI only (agents are not supported in Claude.ai browser)

**Usage:**
```
I've updated my baseline resume. Run the resume-updater agent to sync all skill docs.
```

---

## 🚀 Quick Start

### Prerequisites

**Required:**
- **Claude Code CLI** installed, OR **Claude.ai** account (browser-based usage)
- **Python 3.x** with `lxml` package: `pip install lxml`

**For resume tailoring (job-application-helper):**
- **Anthropic `docx` example skill** — provides pack/unpack scripts for .docx XML editing
  - Claude.ai: automatically available at `/mnt/skills/public/docx/`
  - Claude Code CLI: install via the example skills marketplace, or copy `pack.py` and `unpack.py` into `skills/job-application-helper/scripts/`
- **`defusedxml`** Python package — required by pack/unpack scripts: `pip install defusedxml`
- **LibreOffice** — optional, for page count verification (headless .docx-to-PDF conversion): `sudo apt install libreoffice` / `brew install --cask libreoffice` / [libreoffice.org](https://www.libreoffice.org/download/)
- **`pdfinfo`** (from poppler-utils) — optional, for page count verification: `sudo apt install poppler-utils` / `brew install poppler`

**For behavioral story optimization:**
- **Anthropic API key** — required by `generate_summaries.py` and `story_watcher.py` for STAR summary generation

### Installation

**Option 1: Claude Code CLI**
```bash
# Copy skills to your skills directory
cp -r skills/job-application-helper ~/.claude/skills/
cp -r skills/interview-study-guide ~/.claude/skills/
cp -r skills/likert-screening-tutor ~/.claude/skills/
cp -r skills/behavioral-story-optimization ~/.claude/skills/

# Copy agents to your agents directory
mkdir -p ~/.claude/agents
cp agents/resume-updater.md ~/.claude/agents/
```

**Option 2: Claude.ai Browser**
```bash
# Package skills into .skill files
python utils/package_skill.py skills/job-application-helper
python utils/package_skill.py skills/interview-study-guide
python utils/package_skill.py skills/likert-screening-tutor
python utils/package_skill.py skills/behavioral-story-optimization

# Then upload to claude.ai:
# Settings → Capabilities → Skills → "+ Add" → "Upload a skill"
```

> **Note:** `behavioral-story-optimization` uses Claude Code CLI scripts — the Claude.ai browser version can invoke the skill but cannot run the Python scripts directly.

### Usage

In a Claude conversation, invoke skills with `/skill-name`:

**Create tailored resume and cover letter:**
```
/job-application-helper
I'm applying to [Company] for [Role]. Here's the job description:
[paste job description]

I need: both resume and cover letter
```

**Generate an interview study guide:**
```
/interview-study-guide
I have an upcoming interview at [Company] for [Role]. Please generate a full study guide.
```
*(If you've already run job-application-helper for this role, the job description is found automatically — no paste needed.)*

**Practice for behavioral assessment:**
```
/likert-screening-tutor
Give me a full 75-question timed mock assessment for Google's Hiring Assessment
```

**Generate a role-tailored behavioral story reference sheet:**
```
/behavioral-story-optimization
Generate my top 10 behavioral stories for my HyperLight interview
```

---

## ⚠️ Personalization Requirements

### Job Application Helper — **MUST CUSTOMIZE**

This skill contains example data and will not work without personalization.

**Quick Checklist:**
- [ ] Replace `skills/job-application-helper/assets/Ted_Cohen-RESUME.docx` with your baseline resume
- [ ] Replace `skills/job-application-helper/assets/Ted_Cohen-COVERLETTER.md` with your cover letter template
- [ ] Run the baseline setup script to calibrate char count targets: `bash skills/job-application-helper/scripts/setup_baseline.sh`
- [ ] Update `skills/job-application-helper/references/user_profile.md` with your background
- [ ] Update `skills/job-application-helper/references/list_of_key_accomplishments.md` with your achievements
- [ ] Update `skills/job-application-helper/references/list_of_target_companies.md` with your target companies
- [ ] Edit `skills/job-application-helper/SKILL.md` (lines 10, 11, 256-257) to use your name and LinkedIn URL
- [ ] If you renamed your resume file, update the `BASELINE=` path in `skills/job-application-helper/scripts/prepare_resume.sh` (line 12)

[See detailed personalization guide →](./docs/job-application-helper.md#️-important-personalization-required) | [See setup guide →](./skills/job-application-helper/SETUP.md)

### Interview Study Guide — **NO CUSTOMIZATION NEEDED**
✅ Automatically reads from `job-application-helper/references/user_profile.md` — works once job-application-helper is personalized

### Likert Screening Tutor — **NO CUSTOMIZATION NEEDED**
✅ Works out of the box

### Behavioral Story Optimization — **MUST CUSTOMIZE**
- [ ] Populate `skills/behavioral-story-optimization/assets/rawStorySummary.md` with your STAR stories (excluded from version control)
- [ ] Set `ANTHROPIC_API_KEY` environment variable for summary generation
- [ ] Run `python scripts/generate_summaries.py` or `python scripts/story_watcher.py --once` to generate `targettedSummaries.md`

[See detailed documentation →](./docs/behavioral-story-optimization.md)

---

## 📁 Repository Structure

```
technicalAIJobSearch/
├── README.md                           # This file - overview of all skills
├── agents/                             # Claude Code subagent definitions
│   └── resume-updater.md              # Syncs skill docs after resume changes
├── changelogs/                         # Change history
├── docs/                               # Detailed documentation (outside skill folders)
│   ├── job-application-helper.md       # Resume/cover letter skill docs
│   ├── interview-study-guide.md        # Interview study guide skill docs
│   ├── likert-screening-tutor.md       # Behavioral screening prep docs
│   └── behavioral-story-optimization.md # Behavioral story library docs
├── skills/                             # All skill definitions
│   ├── job-application-helper/         # Resume/cover letter skill
│   │   ├── SKILL.md                    # Skill definition and workflow
│   │   ├── SETUP.md                    # New user setup guide
│   │   ├── assets/                     # Baseline documents
│   │   │   ├── Ted_Cohen-RESUME.docx
│   │   │   ├── Ted_Cohen-COVERLETTER.md
│   │   │   ├── Ted_Cohen-COVERLETTER.docx
│   │   │   ├── 260316-Linkedin-Profile.pdf
│   │   │   └── LinkedIn_Best_Profile_Guide.pdf
│   │   ├── references/                 # Knowledge base
│   │   │   ├── user_profile.md
│   │   │   ├── xml_editing_guide.md
│   │   │   ├── linkedin_profile_optimization.md
│   │   │   ├── list_of_key_accomplishments.md
│   │   │   ├── list_of_target_companies.md
│   │   │   ├── qa_and_delivery.md
│   │   │   ├── company_research.md
│   │   │   ├── interview_preparation.md
│   │   │   ├── skill_gap_analysis.md
│   │   │   └── networking_support.md
│   │   └── scripts/                    # Automation scripts
│   │       ├── setup_baseline.sh       # Calibrates char count targets for new baseline
│   │       ├── prepare_resume.sh
│   │       ├── prepare_cover_letter.sh
│   │       ├── create_tailored_resume.sh
│   │       ├── cleanup_unpacked.sh
│   │       ├── verify_page_count.sh
│   │       ├── pack.py
│   │       ├── unpack.py
│   │       └── para_utils.py
│   ├── interview-study-guide/          # Technical interview study guide skill
│   │   └── SKILL.md                    # Skill definition and workflow
│   ├── likert-screening-tutor/         # Behavioral screening prep skill
│   │   ├── SKILL.md                    # Skill definition and workflow
│   │   └── references/                 # Question bank & scoring guide
│   │       ├── question_bank.md
│   │       └── scoring_guide.md
│   └── behavioral-story-optimization/  # Behavioral story library & top-10 selector
│       ├── SKILL.md                    # Skill definition and workflow
│       ├── targettedSummaries.md       # Generated STAR summaries (gitignored)
│       ├── assets/
│       │   ├── rawStorySummary.md      # Raw story notes (gitignored)
│       │   └── processed_stories.json  # Watcher state file
│       └── scripts/
│           ├── generate_summaries.py   # Bulk regeneration from raw stories
│           ├── story_watcher.py        # Incremental watcher for new stories
│           └── generate_top10_stories.py # Role-specific top 10 selector
├── utils/                              # Shared utilities
│   ├── package_skill.py                # Creates .skill files for browser upload
│   └── quick_validate.py               # Validates skill structure
└── images/                             # Documentation images
    └── output-baseline-resumes-sidebyside.png
```

---

## 🛠️ Utilities

### `package_skill.py` — Package Skills for Browser Usage

Creates `.skill` files that can be uploaded to Claude.ai:

```bash
# Package a single skill
python utils/package_skill.py skills/job-application-helper

# Package with custom output directory
python utils/package_skill.py skills/likert-screening-tutor ./dist
```

**What it does:**
- Validates skill structure (SKILL.md, YAML frontmatter)
- Bundles entire skill folder into a .zip archive with .skill extension
- Preserves folder structure and file paths
- Shows validation results and confirms successful creation

**Example output:**
```
📦 Packaging skill: job-application-helper

🔍 Validating skill...
✅ Skill validation passed

  Added: job-application-helper/SKILL.md
  Added: job-application-helper/assets/Ted_Cohen-RESUME.docx
  [... more files ...]

✅ Successfully packaged skill to: job-application-helper.skill
```

### `quick_validate.py` — Validate Skill Structure

Checks if a skill meets Claude Code requirements:

```bash
python utils/quick_validate.py skills/job-application-helper
```

---

## 📚 Documentation

Each skill has detailed documentation in the `docs/` folder:

- **[Job Application Helper Documentation](./docs/job-application-helper.md)**
  - Complete workflow walkthrough
  - Personalization guide
  - Advanced customization options
  - Technical details (LPS/ATS optimization, XML editing)

- **[Job Application Helper Setup Guide](./skills/job-application-helper/SETUP.md)**
  - Prerequisites and installation
  - Baseline calibration with `setup_baseline.sh`
  - Verification and troubleshooting

- **[Interview Study Guide Documentation](./docs/interview-study-guide.md)**
  - Study guide structure and section descriptions
  - Automatic job description resolution from outputs folder
  - Shared dependencies with job-application-helper

- **[Likert Screening Tutor Documentation](./docs/likert-screening-tutor.md)**
  - Assessment background and format
  - Practice modes and usage
  - Scoring rubric and strategic principles
  - Common mistakes to avoid

- **[Behavioral Story Optimization Documentation](./docs/behavioral-story-optimization.md)**
  - Raw story format and STAR summary structure
  - `story_watcher.py` incremental watcher setup (including Windows Task Scheduler)
  - `generate_top10_stories.py` usage for role-specific interview prep
  - Troubleshooting

- **[Resume Updater Agent](./agents/resume-updater.md)**
  - Subagent definition for keeping skill docs in sync with baseline resume
  - Execution workflow, responsibilities, and success criteria

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

**For job-application-helper:**
- Additional industry-specific templates
- Enhanced ATS parsing rules
- Multi-language support
- More LinkedIn optimization strategies

**For likert-screening-tutor:**
- Additional practice questions for question bank
- Company-specific scoring patterns (beyond Google)
- More assessment format variations (e.g., Microsoft, Meta)
- Expanded strategic guidance

**For behavioral-story-optimization:**
- Additional behavioral question categories
- Multi-company story ranking (score stories across multiple open roles simultaneously)
- Story gap analysis (identify under-covered behavioral categories)

**New skills:**
- Salary negotiation advisor
- Career transition planner
- Networking outreach templates
- Portfolio/GitHub profile optimizer

---

## 📄 License

MIT License - Feel free to adapt these skills for your own job search needs.

---

## 📊 Reports & Evaluations

- [Job Application Helper Skill Evaluation (2026-02-02)](./skill-creator-reports/skill-evaluation-2026-02-02.md) - Best practices evaluation against Claude Code Skill Creator guidelines

---

## 🎯 Roadmap

**Planned Skills:**
- [x] Technical interview prep → delivered as `interview-study-guide`
- [x] Behavioral story library and top-10 selector → delivered as `behavioral-story-optimization`
- [ ] Salary negotiation coach
- [ ] Career transition planner
- [ ] Networking outreach generator
- [ ] Portfolio review and optimization

**Enhancements:**
- [ ] job-application-helper: Add more industry templates
- [ ] interview-study-guide: Add .docx output generation natively within the skill workflow
- [ ] likert-screening-tutor: Expand question bank to 200+ questions
- [ ] behavioral-story-optimization: Multi-company story ranking across open roles
- [ ] Integration between skills (e.g., use interview prep insights in resume tailoring)

---

**Note:** The job-application-helper and behavioral-story-optimization skills contain data specific to the author. You must personalize them with your own documents and background before use. The interview-study-guide and behavioral-story-optimization (top-10 selector) skills work automatically once job-application-helper is personalized. See the [personalization guide](./docs/job-application-helper.md#️-important-personalization-required) and [setup guide](./skills/job-application-helper/SETUP.md) for details.

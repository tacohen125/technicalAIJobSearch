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

**Best For:** Technical Program Manager, Senior Integration Engineer, and Engineering Program Manager roles in Tech, Aerospace/Defense, and Outdoors industries

**Personalization:** ⚠️ **Required** — Must customize with your documents and background

[📖 Full Documentation](./docs/job-application-helper.md) | [📋 SKILL.md](./job-application-helper/SKILL.md)

---

### 2. [Likert Screening Tutor](./docs/likert-screening-tutor.md)
**Prepares candidates for Likert-scale behavioral screenings (Google Hiring Assessment format)**

**Key Features:**
- ✅ Practice questions across 8 behavioral categories
- ✅ Automated scoring with consistency checks
- ✅ Timed mock assessment sessions
- ✅ Strategic guidance for 85%+ alignment scores
- ✅ Red flag identification and improvement recommendations

**Best For:** Preparing for Google's Hiring Assessment and similar behavioral screenings used in tech hiring

**Personalization:** ✅ **None Required** — Works out of the box

[📖 Full Documentation](./docs/likert-screening-tutor.md) | [📋 SKILL.md](./likert-screening-tutor/SKILL.md)

---

## 🚀 Quick Start

### Prerequisites
- **Claude Code CLI** installed, OR
- **Claude.ai** account (browser-based usage)

### Installation

**Option 1: Claude Code CLI**
```bash
# Copy skills to your skills directory
cp -r job-application-helper ~/.claude/skills/
cp -r likert-screening-tutor ~/.claude/skills/
```

**Option 2: Claude.ai Browser**
```bash
# Package skills into .skill files
python utils/package_skill.py job-application-helper
python utils/package_skill.py likert-screening-tutor

# Then upload to claude.ai:
# Settings → Capabilities → Skills → "+ Add" → "Upload a skill"
```

### Usage

In a Claude conversation, invoke skills with `/skill-name`:

**Create tailored resume and cover letter:**
```
/job-application-helper
I'm applying to [Company] for [Role]. Here's the job description:
[paste job description]

I need: both resume and cover letter
```

**Practice for behavioral assessment:**
```
/likert-screening-tutor
Give me a full 75-question timed mock assessment for Google's Hiring Assessment
```

---

## ⚠️ Personalization Requirements

### Job Application Helper — **MUST CUSTOMIZE**

This skill contains example data and will not work without personalization.

**Quick Checklist:**
- [ ] Replace `job-application-helper/assets/Jason_J_Garcia-RESUME.docx` with your baseline resume
- [ ] Replace `job-application-helper/assets/Jason_J_Garcia-COVERLETTER.md` with your cover letter template
- [ ] Update `job-application-helper/references/user_profile.md` with your background
- [ ] Update `job-application-helper/references/list_of_key_accomplishments.md` with your achievements
- [ ] Update `job-application-helper/references/list_of_target_companies.md` with your target companies
- [ ] Edit `job-application-helper/SKILL.md` (lines 10, 11, 256-257) to use your name and LinkedIn URL

[See detailed personalization guide →](./docs/job-application-helper.md#️-important-personalization-required)

### Likert Screening Tutor — **NO CUSTOMIZATION NEEDED**
✅ Works out of the box

---

## 📁 Repository Structure

```
ai-assisted-job-search/
├── README.md                           # This file - overview of all skills
├── docs/                               # Detailed documentation (outside skill folders)
│   ├── job-application-helper.md       # Resume/cover letter skill docs
│   └── likert-screening-tutor.md       # Behavioral screening prep docs
├── job-application-helper/             # Resume/cover letter skill
│   ├── SKILL.md                        # Skill definition and workflow
│   ├── assets/                         # Baseline documents
│   │   ├── Jason_J_Garcia-RESUME.docx
│   │   ├── Jason_J_Garcia-COVERLETTER.md
│   │   └── LinkedIn_Best_Profile_Guide.pdf
│   ├── references/                     # Knowledge base
│   │   ├── user_profile.md
│   │   ├── xml_editing_guide.md
│   │   ├── linkedin_profile_optimization.md
│   │   ├── list_of_key_accomplishments.md
│   │   ├── list_of_target_companies.md
│   │   ├── qa_and_delivery.md
│   │   ├── company_research.md
│   │   ├── interview_preparation.md
│   │   ├── skill_gap_analysis.md
│   │   └── networking_support.md
│   └── scripts/                        # Automation scripts
│       ├── prepare_resume.sh
│       ├── create_tailored_resume.sh
│       ├── cleanup_unpacked.sh
│       └── verify_page_count.sh
├── likert-screening-tutor/             # Behavioral screening prep skill
│   ├── SKILL.md                        # Skill definition and workflow
│   └── references/                     # Question bank & scoring guide
│       ├── question_bank.md
│       └── scoring_guide.md
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
python utils/package_skill.py job-application-helper

# Package with custom output directory
python utils/package_skill.py likert-screening-tutor ./dist
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
  Added: job-application-helper/assets/Jason_J_Garcia-RESUME.docx
  [... more files ...]

✅ Successfully packaged skill to: job-application-helper.skill
```

### `quick_validate.py` — Validate Skill Structure

Checks if a skill meets Claude Code requirements:

```bash
python utils/quick_validate.py job-application-helper
```

---

## 📚 Documentation

Each skill has detailed documentation in the `docs/` folder:

- **[Job Application Helper Documentation](./docs/job-application-helper.md)**
  - Complete workflow walkthrough
  - Personalization guide
  - Advanced customization options
  - Technical details (LPS/ATS optimization, XML editing)

- **[Likert Screening Tutor Documentation](./docs/likert-screening-tutor.md)**
  - Assessment background and format
  - Practice modes and usage
  - Scoring rubric and strategic principles
  - Common mistakes to avoid

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

**New skills:**
- Technical interview preparation (coding, system design)
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
- [ ] Technical interview prep (LeetCode, system design)
- [ ] Salary negotiation coach
- [ ] Career transition planner
- [ ] Networking outreach generator
- [ ] Portfolio review and optimization

**Enhancements:**
- [ ] job-application-helper: Add more industry templates
- [ ] likert-screening-tutor: Expand question bank to 200+ questions
- [ ] Integration between skills (e.g., use interview prep insights in resume tailoring)

---

**Note:** The job-application-helper skill contains example data specific to the original author. You must personalize it with your own documents and background before use. See the [personalization guide](./docs/job-application-helper.md#️-important-personalization-required) for details.

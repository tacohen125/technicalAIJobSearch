# Interview Study Guide

A Claude AI skill for generating comprehensive, role-specific technical interview study guides for job applications.

## Overview

This skill produces structured interview preparation documents that go beyond generic advice — each guide is tailored to the specific technologies, processes, and context of a target role, and explicitly bridges the user's background to the job's requirements.

### Example Output

The `260331-IonQ-SrResearchScientistTFLN` folder contains the reference example:
`IonQ_TFLN_Interview_Study_Guide.docx` — a study guide for the IonQ Senior Research Scientist (TFLN) role.

### Key Features

- **Technology Deep Dives**: Covers the 2–4 core technical domains of the role with first-principles explanations, key equations, process flows, and failure mode analysis
- **Experience Bridge**: Maps the user's background to each job requirement — identifies strong matches, adjacent skills, and honest study gaps
- **Interview Q&A Frameworks**: Role-specific technical and behavioral questions with structured answer outlines grounded in the user's actual experience
- **Verified References**: Real papers and resources with study-priority ratings, sourced via web search
- **Quick-Fire Facts Table**: Key numbers, benchmarks, and company milestones to know cold
- **Day-Before Checklist**: Specific, actionable prep items for the night before the interview
- **Web Research Integration**: Company roadmap, recent publications, and technology benchmarks are verified via web search

## How It Works

### Scope Determination

The skill only generates what the user explicitly requests:
- Full study guide (all 11 sections)
- Specific sections only (e.g., "just the Q&A frameworks")
- Study gap analysis only

### Step 1: Job & Company Analysis

Extracts core technologies, key processes, differentiating requirements, and external context from the job description. Uses web search to confirm company strategy and recent developments.

### Step 2: User Background Mapping

Reads `job-application-helper/references/user_profile.md` and builds an explicit mapping from each job requirement to the user's relevant experience. Identifies study gaps with recommended actions.

### Step 3: Study Guide Generation

Generates 11 structured sections:

1. **Role Snapshot & Strategic Context** — compact table of mission, team, tech, processes, and differentiators
2–4. **Core Technology Deep Dives** — physics/principles, process details, challenges table (one section per core technology)
5. **Platform / Process Essentials** — material stack, litho, etch, metrology touchpoints
6. **Application Context** — why this technology matters for the company's mission
7. **Key References** — 15–25 priority-starred citations organized by topic
8. **Anticipated Interview Q&A** — technical question frameworks + behavioral question guidance
9. **User Narrative** — through-line career narrative + requirement/experience mapping table + study gap list
10. **Quick-Fire Facts** — key numbers, benchmarks, milestones in table form
11. **Day-Before Checklist** — 6–10 specific, prioritized prep actions

### Step 4: Output Delivery

Saves the guide as `[CompanyName]_[RoleAbbrev]_Interview_Study_Guide.md` in the same output folder used by job-application-helper:

```
skills/job-application-helper/assets/outputs/[YYMMDD]-[CompanyName]-[RoleTitle]/
```

## Using the Skill

### With Claude Code (CLI)

```
/interview-study-guide

I have an upcoming interview at [Company] for [Role]. Here's the job description:
[paste job description]

[Optional: I already have the application folder at assets/outputs/[YYMMDD]-[CompanyName]-[RoleTitle]/]
```

### Partial Guide Requests

```
/interview-study-guide

Generate just the Q&A frameworks and quick-fire facts for my IonQ interview.
Job description: [paste]
```

## Quality Standards

- **Technical accuracy**: All numbers, equations, and process parameters are verified
- **No fabricated citations**: Every reference is a real paper confirmed via web search
- **User-grounded answers**: Every answer framework connects to a specific named experience from user_profile.md
- **Honest gap assessment**: Study gaps are flagged clearly with concrete study plans

## Shared Dependencies

This skill reads reference files from `job-application-helper`:
- `../job-application-helper/references/user_profile.md` — user background and experience
- `../job-application-helper/references/list_of_key_accomplishments.md` — key achievements for behavioral Q&A
- `../job-application-helper/assets/outputs/` — shared output folder

No additional setup is required if job-application-helper is already configured.

---

**[← Back to Main README](../README.md)**

---
name: interview-study-guide
description: "Generates a comprehensive technical interview study guide for a specific job application. Use this skill when the user requests: (1) Interview preparation for a specific role, (2) A study guide for an upcoming technical interview, (3) Deep-dive technical preparation on a role's core technologies, (4) Bridging the user's background to a specific job's requirements, or (5) A summary of key facts, references, and Q&A frameworks for a target role. This skill specializes in Research Scientist, Metrology Engineer, and Integration Engineer roles in photonics, semiconductors, and quantum technology, but is not limited to these."
---

# Interview Study Guide Generator

## Source Documents

- **User Profile**: `../job-application-helper/references/user_profile.md` (background, competencies, experience)
- **Key Accomplishments**: `../job-application-helper/references/list_of_key_accomplishments.md`
- **Job Description**: provided by the user in the conversation, OR located via folder search (see Job Description Resolution below)
- **Outputs Folder**: `../job-application-helper/assets/outputs/`

## Purpose

This skill generates a structured, role-specific interview study guide that:
- Covers the core technical concepts required by the job
- Bridges the user's existing background to the role's requirements
- Provides interview question frameworks with answer outlines
- Surfaces the key numbers, references, and facts to memorize
- Produces a day-before action checklist

The output is written as a markdown file saved to the job's output folder (shared with the job-application-helper outputs).

---

## Job Description Resolution

Before doing anything else, determine the job description source:

### Case 1: User provides the JD directly
Use it. Proceed to Step 1.

### Case 2: User references a company/role but does not paste the JD

1. List all subdirectories under `../job-application-helper/assets/outputs/`
2. Find any folder whose name contains the company name or role keywords the user mentioned (case-insensitive match on folder name)
3. If **exactly one** matching folder is found:
   - Read `job_description.md` from that folder
   - Confirm to the user: "Found job description in `[folder name]` — using that. Proceeding with study guide."
   - Use the resolved output folder for saving the study guide
4. If **multiple** matching folders are found:
   - List them and ask the user which one to use
5. If **no** matching folder is found:
   - Ask the user to paste the job description directly

### Case 3: User provides no company/role reference at all
Ask: "Which role is this study guide for? You can paste the job description or name the company/role and I'll look for it in your outputs folder."

---

## Determining Scope

**CRITICAL: Only work on what the user explicitly requests. Do not assume additional deliverables.**

Before beginning, confirm:
- Has the job description been resolved? (See Job Description Resolution above)
- Is there an existing output folder for this application? If found via folder search, use it. If not, create one.
- Does the user want a full study guide, or a specific section only?

**If the request is ambiguous, ask for clarification before proceeding.**

---

## Workflow

### Step 1: Job & Company Analysis

Read the job description carefully. Extract:

1. **Role summary**: One sentence describing the core mission of the role.
2. **Core technologies**: The 2–4 primary technical domains the role requires deep expertise in (e.g., periodic poling, ICP-RIE etching, scatterometry, MOCVD, etc.).
3. **Key processes**: Fabrication steps, measurement workflows, or system design approaches central to the role.
4. **Required skills**: Technical, software, cross-functional.
5. **Differentiating requirements**: Anything unusual or highly specialized that distinguishes this role from a generic version.
6. **External context**: Foundry relationships, vendor partnerships, regulatory or standards environment.

Then **use web search** to:
- Confirm the company's current technology strategy, products, and roadmap
- Identify recent publications, press releases, or investor materials relevant to the role
- Find the specific team's focus area within the broader company (if identifiable)

### Step 2: User Background Mapping

Read `../job-application-helper/references/user_profile.md` and `../job-application-helper/references/list_of_key_accomplishments.md`.

Build a mapping table:

| Job Requirement | User's Experience Bridge |
|---|---|
| [core requirement 1] | [specific experience, tool, or project] |
| [core requirement 2] | [specific experience, tool, or project] |
| ... | ... |

Identify:
- **Strong matches**: Direct experience the user can lead with
- **Adjacent experience**: Transferable skills from different but related work
- **Study gaps**: Topics where the user must build new knowledge before the interview

Mark study gaps clearly so the user knows where to invest prep time.

### Step 3: Generate Study Guide Content

Generate all 9 sections below. Each section is described in detail.

---

#### Section 1: Role Snapshot & Strategic Context

Open with 2–3 sentences framing the role's mission within the company's broader strategy. Then produce a compact table:

| Dimension | Detail |
|---|---|
| Mission | [one-sentence role mission] |
| Team | [cross-functional team composition and key stakeholders] |
| Core Materials / Tech | [primary materials or technology platform] |
| Key Processes | [3–5 core technical processes] |
| Differentiator | [what makes this role/company's approach distinctive] |
| External | [foundry, vendor, partner, or standards context] |

---

#### Section 2–4: Core Technology Deep Dives

For each of the 2–4 core technologies identified in Step 1, generate a numbered section (e.g., "2. Periodic Poling Deep Dive", "3. Waveguide Fabrication Essentials").

Each deep dive must include:

**2a. What Is [Technology]?**
Plain-language explanation of the phenomenon or process. Suitable for someone with strong physics/engineering background approaching this topic for the first time.

**2b. Core Physics / Principles**
The quantitative fundamentals: key equations, figures of merit, physical limits, and how they relate to device performance. Use real numbers (e.g., χ(2) = 27 pm/V, Vπ·L < 2 V·cm). Do not use vague language where specific values are known.

**2c. Process / Implementation Details**
Step-by-step process flow or implementation approach: tools used, parameters, critical control points, in situ monitoring techniques.

**2d. Challenges & Mitigations**
A table of the 4–6 most common failure modes or technical challenges, each with its implication and the standard mitigation approach:

| Challenge | Implication / Mitigation |
|---|---|
| [challenge 1] | [implication / mitigation] |
| ... | ... |

---

#### Section 5: Platform / Process Essentials

Cover the full material stack, lithography approach, etching, and metrology touchpoints relevant to the role. Structure as subsections (5a, 5b, etc.):

**5a. Material Stack** — table of layers with roles
**5b. Lithography** — resolution requirements, tool types, mask/resist considerations
**5c. Etching** — process type, key parameters, selectivity, surface quality targets
**5d. Metrology Touchpoints** — list the specific measurement techniques the user would use, framed as direct value-add (e.g., "SEM/FIB cross-section: etch profile and sidewall angle")

Tie metrology touchpoints explicitly to the user's background where possible.

---

#### Section 6: Application Context — Why This Technology Matters

2–3 paragraphs explaining:
- What problem the company is solving
- Why this specific technology (the role's focus) is the critical enabling layer
- How the role's outputs connect to the company's commercial or scientific roadmap

This section helps the user give authentic, informed answers to "Why IonQ?" or "Why this role?" questions.

---

#### Section 7: Key References — Study Priority List

Organize references by topic, with priority stars (★★ = essential, ★ = important, no star = useful background). Include:
- Author, year, title, journal/venue
- One-line annotation explaining why it's relevant
- Label FOUNDATIONAL, BENCHMARK, or REVIEW as appropriate

Provide 15–25 references organized into 4–6 topic groupings matching the role's core technologies. Use web search to identify real, current papers — do not fabricate citations.

---

#### Section 8: Anticipated Interview Questions & Answer Frameworks

**Technical Questions (3–5)**

For each question:
```
Q: [specific technical question likely to be asked]
ANSWER FRAMEWORK:
1. [key point to cover]
2. [key point to cover]
3. [key point to cover]
4. [connect to user's direct background]
5. [quantitative fact or specific example to include]
```

Choose questions that:
- Test deep understanding of the core technologies
- Probe process troubleshooting ability
- Assess metrology/characterization judgment
- Explore scale-up or external partner management (if relevant)

**Behavioral / Fit Questions (4–6)**

Format as:
`'[behavioral question stem]' → [which of the user's experiences to draw from + what to quantify]`

Draw from `../job-application-helper/references/user_profile.md` experience bullets. Explicitly name the project or tool the user should reference.

---

#### Section 9: User Narrative — Connecting Your Background

One framing paragraph that articulates the through-line from the user's career history to this specific role. Should be usable nearly verbatim as a 2-minute intro narrative.

Then the mapping table (built in Step 2), formatted as:

| [Company] Requirement | Your Experience Bridge |
|---|---|
| [requirement] | [experience] |
| ... | ... |

Close with a bullet list of **study gaps** the user should address before the interview, each with a recommended action (e.g., "Read Fejer 1992 — covers QPM derivation").

---

#### Section 10: Quick-Fire Facts to Memorize

A table of 8–12 specific numerical facts, product names, or milestones the user should know cold:

| Fact | Value |
|---|---|
| [parameter name] | [value with units] |
| [company milestone] | [number / date] |
| ... | ... |

Include: key material constants, device performance benchmarks, company roadmap milestones, ion/wavelength specifics, or any other role-specific numbers that signal deep familiarity.

---

#### Section 11: Day-Before Checklist

6–10 specific, actionable items. Each should be:
- A concrete action (read, review, prepare, practice)
- Tied to a specific resource or experience
- Ordered by priority

End with a personal logistics note (e.g., travel, arrival time, format of interview if known).

Close the document with: `Prepared for Ted Cohen — [Company] Job ID [ID if known] — [Month Year]`

---

### Step 4: Output Delivery

**Save as markdown file**:

```
FOLDER="../job-application-helper/assets/outputs/[YYMMDD]-[CompanyName]-[RoleTitle]"
```

If the folder already exists (from job-application-helper), save the file there. If not, create it.

Filename: `[CompanyName]_[RoleTitleAbbrev]_Interview_Study_Guide.md`

Example: `IonQ_TFLN_Interview_Study_Guide.md`

**Also save the job description** as `job_description.md` in the same folder if not already present.

After saving, provide the user with:
1. The file path to the saved study guide
2. A brief summary of study gaps identified
3. The top 3 most important references to read first

---

## Quality Standards

- **All technical facts must be accurate** — use web search to verify key numbers, paper titles, and company claims. If uncertain, say so explicitly in the guide.
- **No fabricated citations** — every reference in Section 7 must be a real paper. Use web search to confirm.
- **Specificity over generality** — "ICP-RIE with Cl₂/Ar at < 0.5 nm RMS sidewall roughness" is better than "dry etching techniques."
- **User-grounded answers** — every answer framework in Section 8 must connect to a specific named experience from `user_profile.md`, not generic advice.
- **Bridge gaps honestly** — if the user has no direct experience with a core requirement, say so clearly and provide a concrete study plan, rather than overstating transferability.

## Important Notes

- **Always be truthful**: Never fabricate the user's experience or capabilities
- **Depth over breadth**: A technically deep guide covering 2–3 topics well is better than a shallow guide covering 6 topics poorly
- **Interview-ready framing**: Write frameworks as things the user would say aloud, not as bullet points to memorize verbatim
- **Stay current**: Use web search for company roadmap, recent publications, and technology benchmarks

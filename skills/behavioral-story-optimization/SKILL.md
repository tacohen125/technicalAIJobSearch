---
name: behavioral-story-optimization
description: "Generates a role-tailored top 10 behavioral stories reference sheet for a job interview. Use this skill when the user requests: (1) A top 10 behavioral stories document for an upcoming interview, (2) A behavioral story reference sheet for a specific company or role, (3) Help selecting which stories to highlight in an interview, or (4) Running the generate_top10_stories.py script. This skill reads the user's full story library (targettedSummaries.md) and uses the job description from the application output folder to rank and format the 10 most relevant stories."
---

# Behavioral Story Optimization

Generates a role-specific top 10 behavioral stories reference sheet for a job
interview, containing a quick-reference summary table and full story details.

---

## Source Documents

- **Story Library**: `targettedSummaries.md` (in this skill's root directory)
- **Job Description**: `job_description.md` in the job's output folder (see Job Resolution below)
- **Outputs Folder**: `../job-application-helper/assets/outputs/`
- **Script**: `scripts/generate_top10_stories.py`

---

## Job Description Resolution

Before running, identify which job the user is referring to:

### Case 1: User names a company and/or role
1. List all subdirectories under `../job-application-helper/assets/outputs/`
2. Find folders whose name contains the company name or role keywords (case-insensitive, hyphen-insensitive match)
3. If **exactly one** folder matches:
   - Confirm to the user: "Found `[folder name]` — generating top 10 stories for that role."
   - Proceed to Step 1.
4. If **multiple** folders match:
   - List them and ask the user which one to use. Do not proceed until resolved.
5. If **no** folder matches:
   - Tell the user no output folder was found for that role.
   - Ask them to either paste the job description directly or create the application folder first using the job-application-helper skill.

### Case 2: User provides no company or role reference
Ask: "Which role is this for? You can name the company/role and I'll find it in your outputs folder, or paste the job description directly."

---

## Workflow

The script handles file I/O only. Story selection is done by Claude reading the
context output — no API key required.

### Step 1: Print context

Run the script with just the search term. It prints the job description and full
story library to stdout:

```bash
cd "skills/behavioral-story-optimization"
python scripts/generate_top10_stories.py "<search_term>"
```

Use `--list` to see available folders if the search term is unclear:
```bash
python scripts/generate_top10_stories.py --list
```

Use `--dry-run` to validate the folder and see the story inventory without the
full context dump:
```bash
python scripts/generate_top10_stories.py "<search_term>" --dry-run
```

### Step 2: Select top 10

Read the context output and select the 10 most relevant stories for the role.
Rank them 1–10 (most relevant first) and assign group theme labels for stories
1–4, 5–8, and 9–10.

### Step 3: Write the document

Pass the selection as a JSON string to `--write`:

```bash
python scripts/generate_top10_stories.py "<search_term>" --write '<json>'
```

Or pipe it via stdin:
```bash
echo '<json>' | python scripts/generate_top10_stories.py "<search_term>" --write -
```

**Selection JSON schema:**
```json
{
  "stories": [
    {
      "rank": 1,
      "section": "<behavioral question category>",
      "title": "<exact story title from context, including → part>",
      "short_name": "<4-6 word version for the summary table>",
      "career_stage": "<as shown in story block>",
      "primary_attributes": "<3-6 word phrase: what this story proves>",
      "strong_for": "<short phrase: interview question types it answers>"
    }
  ],
  "group_1_4_label": "<≤8 word theme for stories 1-4>",
  "group_5_8_label": "<≤8 word theme for stories 5-8>",
  "group_9_10_label": "<≤8 word theme for stories 9-10>"
}
```

### Step 4: Confirm and report

After `--write` completes, confirm:
- Output file written: `Ted_Cohen-Top10BehavioralStories-[Company]-[Role].md`
- Saved to the correct job output folder

Report to the user:
1. Which folder the file was saved to
2. The 10 selected stories with ranks
3. The group theme labels (Stories 1–4, 5–8, 9–10)

---

## Output Format

The generated document contains two sections:

**Quick Reference Table** — for use during the interview itself:

| # | Anchor Story | Career Stage | Primary Attributes | Strong For Questions About… |
|---|---|---|---|---|
| 1 | Story short name | Career stage | Key attributes | Topic area |
| ... | | | | |

Followed by group labels:
> **Stories 1–4** → Core [role] fit
> **Stories 5–8** → [Theme]
> **Stories 9–10** → Judgment & leadership

**Story Details** — full STAR blocks for each of the 10 stories, in ranked order,
for pre-interview study.

Output file: `Ted_Cohen-Top10BehavioralStories-[CompanyName]-[RoleTitle].md`
Saved to: `../job-application-helper/assets/outputs/[matched-folder]/`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Multiple folders match the search term | Use a longer, more specific search term or the full folder name |
| `job_description.md` not found in the folder | Create the application materials first with the job-application-helper skill |
| `targettedSummaries.md` is empty or missing | Run `story_watcher.py --once` or `generate_summaries.py` to populate it |
| JSON parse error on `--write` | Check for unescaped quotes in the JSON string; use stdin (`--write -`) for complex payloads |

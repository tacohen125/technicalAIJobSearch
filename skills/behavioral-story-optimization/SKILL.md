---
name: behavioral-story-optimization
description: "Maintains a library of STAR-format behavioral interview stories and keeps them synchronized between a raw notes file and a compressed, interview-ready summaries file. Use this skill when the user requests: (1) Adding a new raw story and generating its STAR summary, (2) Updating targettedSummaries.md with any unprocessed stories, (3) Selecting the top 10 most relevant stories for a specific job interview, (4) Rebuilding all summaries from scratch, or (5) Reviewing or navigating the story library by behavioral question category."
---

# Behavioral Story Optimization

## Key Files

| File | Purpose |
|------|---------|
| `assets/rawStorySummary.md` | Source of truth — raw story notes organized by behavioral question category |
| `targettedSummaries.md` | Output — compressed STAR summaries ready for interview use |
| `assets/processed_stories.json` | State file — tracks which raw stories have already been summarized |
| `scripts/story_watcher.py` | Optional script — calls Claude API to batch-process new stories |

Both `rawStorySummary.md` and `targettedSummaries.md` are excluded from version control (personal content).

---

## Raw Story Format

Stories in `rawStorySummary.md` are organized under `##` section headings that match standard behavioral question categories. Each story has an `*italic title*` line followed by a short prose description:

```markdown
## Category Name

**Describe a situation where...**

*Story title in italics*
Story body text describing what happened, what you did, and what the outcome was.
Keep it concise — 2–5 sentences.

*Another story title*
...
```

The unique state key for each story is `"Section::Title"` (e.g., `"Dealing with conflict::The Grating Spec Debate"`).

---

## Targeted Summary Format

Each summary in `targettedSummaries.md` follows this structure:

```markdown
### Story Title → Outcome

**Career stage:** <Graduate school | Early industry | Industry | Senior IC / informal manager>
**Core proof:** <The single most important thing this story proves>

- **Situation:** One sentence: context and challenge.
- **Action:** One sentence: what Ted specifically did (use "I").
- **Result:** One sentence: outcome, ideally with a metric or business impact.

**Use for:**
- ✔ <behavioral question tag>
- ✔ <behavioral question tag>
- ✔ <behavioral question tag>

**Opening line:** "<Natural, spoken 1-sentence opener for the interview>"
```

### Career stage options
- Graduate school
- Early industry
- Industry
- Senior IC / informal manager

### Common "Use for" tags
Persuasion with data · Dealing with conflict · Above and beyond · Prioritization ·
Split-second decisions · Failure & learning · Mentorship · Delegation ·
Unpopular decisions · Resilience · Taking initiative · Managing up ·
Root cause analysis · Technical depth · Developing others · External communication ·
Standards & alignment · Risk management · Ownership under pressure

---

## Determining Scope

Before beginning work, identify the user's request:

- **Add a new story?** → Mode A, then Mode B for its summary
- **Update summaries for stories already in rawStorySummary.md?** → Mode B
- **Select top 10 for an interview?** → Mode C
- **Rebuild all summaries?** → Mode B with `--rebuild` flag or full re-read
- **Review/find a story by category?** → Read `targettedSummaries.md` and surface the relevant section

**If the request is ambiguous, ask for clarification before proceeding.**

---

## Workflow

### Mode A: Add a New Raw Story

When the user wants to add a new story to the library:

1. Ask for: the behavioral question category (section heading), a story title, and the raw story text (2–5 sentences covering situation, action, result)
2. Read `assets/rawStorySummary.md` to confirm the correct `## Section` heading exists (or determine where to add a new one)
3. Append the story under the correct section using the raw story format:
   - `*italic title*` line
   - Followed by the body text
4. Proceed to Mode B to generate the STAR summary for the new story

---

### Mode B: Summarize New Stories

When the user wants to update `targettedSummaries.md` with stories not yet processed:

1. Read `assets/rawStorySummary.md` and `assets/processed_stories.json`
2. Identify stories whose `"Section::Title"` key is absent from the `"processed"` array in the state file
3. For each new story, generate a STAR summary using the Targeted Summary Format above:
   - Keep each STAR field to 1 sentence
   - Use active voice and first person ("I") for Action and Opening line
   - Opening line must sound natural and spoken, not like a resume bullet
   - Choose 3 "Use for" tags from the common tags list that best match the behavioral category and story content
4. Append each summary to the correct `## Section` in `targettedSummaries.md`:
   - If the section exists, append after the last story in that section (preceded by `---`)
   - If the section doesn't exist yet, create it at the end of the file with a `---` separator before the new `## Heading`
5. Update `assets/processed_stories.json` by adding the new story's key to the `"processed"` array (keep the array sorted)

**Alternatively, run the watcher script** (requires `ANTHROPIC_API_KEY` in environment):

```bash
cd skills/behavioral-story-optimization

# Process any new stories (one pass):
python scripts/story_watcher.py --once

# Rebuild all summaries from scratch (clears state first):
python scripts/story_watcher.py --rebuild --once

# Use a faster model for drafts:
python scripts/story_watcher.py --model claude-haiku-4-5-20251001 --once
```

---

### Mode C: Select Top 10 Stories for an Interview

When the user wants a role-specific behavioral story reference sheet before an interview:

**Step 1: Resolve the target job**

- If the user names a company or role: list folders under `skills/job-application-helper/assets/outputs/` and find the match
- If exactly one folder matches, confirm it and proceed
- If multiple folders match, list them and ask the user to pick one
- If no folder matches, ask the user to paste the job description directly

**Step 2: Load context**

1. Read `targettedSummaries.md` to load the full story library
2. Read `job_description.md` from the matched output folder

**Step 3: Select and rank**

Score each story against:
- Explicit behavioral competencies and values mentioned in the job description
- Role level fit (IC vs. manager, technical depth, scope of influence)
- Variety: ensure coverage across at least 5 different "Use for" tag categories
- Recency and career stage fit for a senior IC / informal manager role

Rank the 10 most relevant stories from most to least relevant. Assign a short theme label for stories 1–4, 5–8, and 9–10.

**Step 4: Write the output file**

Output file name: `Ted_Cohen-Top10BehavioralStories-[CompanyName]-[RoleTitle].docx`
Save to: `skills/job-application-helper/assets/outputs/[matched-folder]/`

```markdown
# Top 10 Behavioral Stories — [Company Name] [Role Title]

## Quick Reference Table

| # | Anchor Story | Career Stage | Primary Attributes | Strong For Questions About… |
|---|---|---|---|---|
| 1 | Short story name | Career stage | Key attributes | Topic area |
...

**Stories 1–4** → [Theme label]
**Stories 5–8** → [Theme label]
**Stories 9–10** → [Theme label]

---

## Story Details

[Full STAR block for each of the 10 stories in ranked order]
```

**Step 5: Confirm**

Report to the user:
- Which folder the file was saved to
- The 10 selected stories with ranks and group labels

---

## Important Notes

- **Never fabricate stories**: Only summarize what the user has written in `rawStorySummary.md`
- **Preserve voice**: Keep first person ("I") and active voice in Action and Opening line fields
- **State integrity**: Always update `processed_stories.json` after generating a summary so it isn't re-processed
- **Section matching**: Section headings in `rawStorySummary.md` must exactly match `## headings` in `targettedSummaries.md` for correct placement

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No new stories found` after adding one | Check that the title uses `*italic*` formatting (single asterisks, not double) |
| Summary appended to wrong section | Section heading in `rawStorySummary.md` must exactly match the `## heading` in `targettedSummaries.md` |
| Want to re-generate one summary | Remove its `"Section::Title"` key from `processed_stories.json`, then run Mode B |
| Want to regenerate everything | Run `python scripts/story_watcher.py --rebuild --once` or re-read all stories and re-generate |
| Job folder not found for Mode C | List `skills/job-application-helper/assets/outputs/` to see available folders |
| `ANTHROPIC_API_KEY not set` | Set the env var, or use the inline Mode B workflow (no script needed) |

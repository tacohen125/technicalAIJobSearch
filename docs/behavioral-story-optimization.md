# Behavioral Story Optimization

Maintains a library of STAR-format behavioral interview stories and keeps them
synchronized between a raw notes file and a compressed, interview-ready summaries file.

---

## Overview

| File | Role |
|------|------|
| `skills/behavioral-story-optimization/assets/rawStorySummary.md` | Source of truth — raw story notes organized by behavioral question category |
| `skills/behavioral-story-optimization/targettedSummaries.md` | Output — compressed STAR summaries ready for interview use |
| `skills/behavioral-story-optimization/assets/processed_stories.json` | State file — tracks which raw stories have already been summarized |
| `skills/behavioral-story-optimization/scripts/generate_summaries.py` | Bulk generator — regenerates all summaries from scratch |
| `skills/behavioral-story-optimization/scripts/story_watcher.py` | Incremental watcher — detects and summarizes new stories automatically |
| `skills/behavioral-story-optimization/scripts/generate_top10_stories.py` | Role-specific selector — picks the top 10 stories for a given job interview |

Both `rawStorySummary.md` and `targettedSummaries.md` are excluded from version
control (personal content). See `.gitignore`.

---

## Raw Story Format (`rawStorySummary.md`)

Stories are organized under `##` headings that match standard behavioral question
categories. Each story has an `*italic title*` line followed by a short prose description:

```markdown
## Category Name

**Describe a situation where...**

*Story title in italics*
Story body text describing what happened, what you did, and what the outcome was.
Keep it concise — 2–5 sentences.

*Another story title*
...
```

The `story_watcher.py` identifies stories by their `*italic title*` line within
each `## section`. The unique key for state tracking is `"Section::Title"`.

---

## Targeted Summary Format (`targettedSummaries.md`)

Each story is compressed into a structured STAR block:

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

**Opening line:** "<Natural, spoken 1-sentence opener for the interview>"
```

---

## Scripts

### `generate_summaries.py` — Bulk Regeneration

Reads all of `rawStorySummary.md`, calls the Claude API for each section, and
writes a fresh `targettedSummaries.md`. Use this when starting fresh or after
significantly editing many raw stories.

```bash
cd skills/behavioral-story-optimization
ANTHROPIC_API_KEY=sk-ant-... python scripts/generate_summaries.py
```

**When to use:** Initial setup, or after bulk edits to raw stories where a full
regeneration is simpler than incremental updates.

---

### `story_watcher.py` — Incremental Watcher

Compares `rawStorySummary.md` against `processed_stories.json` to find new
stories, generates a summary for each, and appends it to the correct section in
`targettedSummaries.md`. State is saved after each story so the process can be
interrupted and resumed.

```bash
# Run once (good for Task Scheduler / cron):
python scripts/story_watcher.py --once

# Poll continuously (default: every 60 seconds):
python scripts/story_watcher.py

# Poll every 5 minutes:
python scripts/story_watcher.py --interval 300

# Rebuild all from scratch (clears state first):
python scripts/story_watcher.py --rebuild --once

# Use a faster/cheaper model for drafts:
python scripts/story_watcher.py --model claude-haiku-4-5-20251001
```

**When to use:** After adding one or a few new stories to `rawStorySummary.md`
without wanting to regenerate everything.

#### Windows Task Scheduler (auto-run on login)

1. Open Task Scheduler → Create Basic Task
2. **Trigger**: At log on
3. **Action**: Start a program
   - Program: `python`
   - Arguments: `"C:\...\skills\behavioral-story-optimization\scripts\story_watcher.py" --once`
   - Start in: `C:\...\skills\behavioral-story-optimization`
4. Add `ANTHROPIC_API_KEY` to user environment variables:
   ```powershell
   [System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
   ```

---

### `generate_top10_stories.py` — Role-Specific Top 10

Reads `targettedSummaries.md`, finds the job's output folder, reads the job
description, and calls Claude to select and rank the 10 most relevant stories
for that interview. Writes a reference document (summary table + full story
details) to the job's output folder.

The script is a two-step process — no API key required. Claude reads the context
and makes the selection; the script handles all file I/O.

```bash
# Step 1 — print job description + story library for Claude to read:
python scripts/generate_top10_stories.py "IonQ"

# Step 2 — Claude selects top 10 and passes JSON back via --write:
python scripts/generate_top10_stories.py "IonQ" --write '<json>'

# Other commands:
python scripts/generate_top10_stories.py --list                  # list folders
python scripts/generate_top10_stories.py "IonQ" --dry-run        # validate + story inventory
echo '<json>' | python scripts/generate_top10_stories.py "IonQ" --write -  # stdin
```

Output file: `Ted_Cohen-Top10BehavioralStories-[CompanyName]-[RoleTitle].md`
Saved to: `skills/job-application-helper/assets/outputs/[matched-folder]/`

**When to use:** Before any job interview to quickly generate a role-tailored
behavioral story reference sheet.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ANTHROPIC_API_KEY not set` | Set env var or prepend to command |
| `No new stories found` after adding one | Check `*italic*` formatting on the title line in rawStorySummary.md |
| Summary appended to wrong section | Section heading in rawStorySummary.md must exactly match `## heading` in targettedSummaries.md |
| Want to re-generate one story | Remove its key from `processed_stories.json`, then run `--once` |
| Want to regenerate everything | Run `--rebuild --once` |
| Job folder not found | Run `--list` to see available folders; use more of the folder name in your search term |

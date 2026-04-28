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
| `skills/behavioral-story-optimization/scripts/story_watcher.py` | Optional script — calls Claude API to batch-process new stories |
| `skills/behavioral-story-optimization/SKILL.md` | Skill definition — Claude handles all workflows (summarize, top 10) directly |

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

## Usage

### Skill Invocation (Recommended)

All workflows are available directly via the Claude skill — no API key or script required:

```
/behavioral-story-optimization
Add a new story about [topic] to my library and generate its summary.
```

```
/behavioral-story-optimization
Update my summaries with any new stories I've added to rawStorySummary.md.
```

```
/behavioral-story-optimization
Generate my top 10 behavioral stories for my IonQ interview.
```

See `SKILL.md` for full workflow details.

---

### `story_watcher.py` — Optional Batch Script

Compares `rawStorySummary.md` against `processed_stories.json` to find new
stories, generates a summary for each via the Claude API, and appends it to the
correct section in `targettedSummaries.md`. State is saved after each story so
the process can be interrupted and resumed.

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

**When to use:** When you prefer a fully automated batch run over invoking the skill.
Requires `ANTHROPIC_API_KEY` in your environment.

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

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ANTHROPIC_API_KEY not set` | Set env var or use the skill directly (no API key needed) |
| `No new stories found` after adding one | Check `*italic*` formatting on the title line in rawStorySummary.md |
| Summary appended to wrong section | Section heading in rawStorySummary.md must exactly match `## heading` in targettedSummaries.md |
| Want to re-generate one story | Remove its key from `processed_stories.json`, then run Mode B via the skill or `--once` |
| Want to regenerate everything | Ask the skill to rebuild, or run `python scripts/story_watcher.py --rebuild --once` |
| Job folder not found for top 10 | List `skills/job-application-helper/assets/outputs/` to see available folders |

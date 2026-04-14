---
name: story-summary-updater
description: "Use this agent when the user adds new raw stories to rawStorySummary.md and wants targettedSummaries.md updated, or when they want to start the background watcher that automatically detects and summarises new stories as they are added."
tools: Glob, Grep, Read, Edit, Write, Bash
model: inherit
color: purple
skills: behavioral-story-optimization
---

# Story Summary Updater — Agent Description

## Purpose

This agent keeps `targettedSummaries.md` in sync with `rawStorySummary.md`.
It detects new stories that have not yet been summarised, calls the Claude API
to generate a targeted STAR-format summary for each one, and appends the result
to the correct section in `targettedSummaries.md`.

Summaries follow the Top 10 Anchor Stories format:
- Story title → Outcome
- Career stage + Core proof
- Situation / Action / Result (one sentence each)
- "Use for" behavioral question tags
- A natural spoken Opening line

---

## Key Files

| File | Purpose |
|------|---------|
| `skills/behavioral-story-optimization/assets/rawStorySummary.md` | Source of truth for all raw stories |
| `skills/behavioral-story-optimization/targettedSummaries.md` | Output — targeted STAR summaries |
| `skills/behavioral-story-optimization/assets/processed_stories.json` | State file — tracks which stories have been summarised |
| `skills/behavioral-story-optimization/scripts/story_watcher.py` | The watcher/agent script |

---

## How Stories Are Detected

`rawStorySummary.md` is organised as:

```
## Section Name (behavioral question category)

*Story title*
Story body text...

*Another story title*
Story body text...
```

The watcher identifies stories by their `*italic title*` lines within each
`## section`. A story is "new" if its `"Section::Title"` key is absent from
`processed_stories.json`.

---

## Usage

### One-time check (run manually or via Task Scheduler)

```bash
cd "skills/behavioral-story-optimization"
ANTHROPIC_API_KEY=sk-ant-... python scripts/story_watcher.py --once
```

### Continuous background watcher (polls every 60 seconds)

```bash
ANTHROPIC_API_KEY=sk-ant-... python scripts/story_watcher.py
```

### Custom polling interval (e.g., every 5 minutes)

```bash
ANTHROPIC_API_KEY=sk-ant-... python scripts/story_watcher.py --interval 300
```

### Rebuild all summaries from scratch

```bash
ANTHROPIC_API_KEY=sk-ant-... python scripts/story_watcher.py --rebuild --once
```

This clears the state file and regenerates summaries for every story,
including ones already in `targettedSummaries.md`. Use this after editing
the system prompt or switching models.

### Use a faster/cheaper model for drafts

```bash
ANTHROPIC_API_KEY=sk-ant-... python scripts/story_watcher.py --model claude-haiku-4-5-20251001
```

---

## Workflow When This Agent Is Invoked by Claude Code

When a user asks to add new stories or update summaries, this agent should:

1. **Read** `rawStorySummary.md` to understand the current story inventory.
2. **Read** `processed_stories.json` to identify which stories are already done.
3. **Identify** any stories in rawStorySummary.md not present in state.
4. **For each new story**: generate a STAR summary in the Top 10 Anchor Stories
   format (Career stage, Core proof, Situation, Action, Result, Use for, Opening line).
5. **Append** the summary to the correct `## Section` in `targettedSummaries.md`.
   - If the section already exists, append after the last story in that section.
   - If the section doesn't exist yet, create it at the end of the file.
6. **Update** `processed_stories.json` with the new story key.
7. **Report** what was added.

### Adding a new story manually (without running the script)

If the user adds a story to `rawStorySummary.md` and asks you to update the
summaries file directly (no API key available), generate the summary inline
using the format below and append it to the correct section yourself.

---

## Summary Format Reference

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

## Running as a Scheduled Task (Windows Task Scheduler)

To have the watcher run automatically whenever you log in:

1. Open **Task Scheduler** → Create Basic Task
2. **Trigger**: At log on (or on a schedule)
3. **Action**: Start a program
   - Program: `python`
   - Arguments: `"C:\...\skills\behavioral-story-optimization\scripts\story_watcher.py" --once`
   - Start in: `C:\...\skills\behavioral-story-optimization`
4. Add `ANTHROPIC_API_KEY` to your user environment variables
   (System Properties → Environment Variables → User variables → New)

Or add an environment variable once in PowerShell (persists across sessions):
```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ANTHROPIC_API_KEY not set` | Set the env var (see above) or prepend to command |
| `No new stories found` but you added one | Check the `*italic*` formatting of the title in rawStorySummary.md |
| Summary appended to wrong section | Section name in rawStorySummary.md must exactly match the `## heading` in targettedSummaries.md |
| Want to re-generate a specific summary | Remove its key from `processed_stories.json`, then run `--once` |
| Want to regenerate everything | Run with `--rebuild --once` |

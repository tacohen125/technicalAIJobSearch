"""
Behavioral Story Watcher — incremental summary agent.

Polls rawStorySummary.md for new stories that haven't been summarized yet.
For each new story found, calls the Claude API to generate a targeted
STAR-format summary and appends it to targettedSummaries.md under the
correct section heading.

State is persisted in assets/processed_stories.json so the agent picks up
where it left off across restarts.

Usage:
    # Run once (good for Task Scheduler / cron):
    python scripts/story_watcher.py --once

    # Poll continuously (default interval: 60 seconds):
    python scripts/story_watcher.py

    # Poll every 5 minutes:
    python scripts/story_watcher.py --interval 300

    # Use a custom model:
    python scripts/story_watcher.py --model claude-haiku-4-5-20251001

Requires:
    pip install anthropic
    ANTHROPIC_API_KEY environment variable set
"""

import argparse
import json
import os
import re
import sys
import time
import textwrap
from datetime import datetime

import anthropic

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
RAW_STORIES_PATH = os.path.join(SKILL_DIR, "assets", "rawStorySummary.md")
SUMMARIES_PATH = os.path.join(SKILL_DIR, "targettedSummaries.md")
STATE_PATH = os.path.join(SKILL_DIR, "assets", "processed_stories.json")

DEFAULT_MODEL = "claude-opus-4-6"
DEFAULT_INTERVAL = 60  # seconds

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """\
You are a behavioral interview coach helping a senior optical/photonic engineer \
named Ted prepare STAR-format story summaries for job interviews.

For the raw story provided, produce a targeted summary using EXACTLY this format \
(no preamble, no commentary — output only the block below):

### Story Title → Outcome

**Career stage:** <Graduate school | Early industry | Industry | Senior IC / informal manager>
**Core proof:** <The single most important thing this story proves about the candidate>

- **Situation:** One sentence: context and challenge.
- **Action:** One sentence: what Ted specifically did (use "I").
- **Result:** One sentence: outcome, ideally with a metric or business impact.

**Use for:**
- ✔ <behavioral question tag>
- ✔ <behavioral question tag>
- ✔ <behavioral question tag>

**Opening line:** "<A natural, spoken 1-sentence opener Ted can use to launch this story in an interview>"

Rules:
- Keep each field to 1–2 sentences maximum.
- Use active voice and first person for Action and Opening line.
- "Use for" tags should match standard behavioral categories \
  (e.g., Persuasion with data, Dealing with conflict, Above and beyond, \
  Prioritization, Split-second decisions, Failure & learning, Mentorship, \
  Delegation, Unpopular decisions, Resilience, Taking initiative, etc.)
- Opening line must sound natural and spoken, not like a resume bullet.
- Output ONLY the formatted block — nothing else.
"""


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def parse_raw_stories(md_text: str) -> list[dict]:
    """
    Parse rawStorySummary.md into a flat list of story dicts:
        {section, title, body, key}

    Sections are ## headings.
    Stories within a section are identified by *italic title* lines.
    """
    stories = []

    # Split into sections on ## headings
    section_pattern = re.compile(r"^## (.+)$", re.MULTILINE)
    section_matches = list(section_pattern.finditer(md_text))

    for i, sec_match in enumerate(section_matches):
        section = sec_match.group(1).strip()
        sec_start = sec_match.end()
        sec_end = section_matches[i + 1].start() if i + 1 < len(section_matches) else len(md_text)
        sec_body = md_text[sec_start:sec_end]

        # Find individual stories by *italic title* lines.
        # Explicitly exclude **bold** question-prompt lines (which start with **).
        story_pattern = re.compile(r"^(?!\*\*)\*([^*].+?[^*])\*\s*$", re.MULTILINE)
        story_matches = list(story_pattern.finditer(sec_body))

        for j, story_match in enumerate(story_matches):
            title = story_match.group(1).strip()
            body_start = story_match.end()
            body_end = story_matches[j + 1].start() if j + 1 < len(story_matches) else len(sec_body)
            body = sec_body[body_start:body_end].strip()
            # Strip trailing separators
            body = re.sub(r"\n---\s*$", "", body).strip()

            if body:
                key = f"{section}::{title}"
                stories.append({
                    "section": section,
                    "title": title,
                    "body": body,
                    "key": key,
                })

    return stories


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------
def load_state() -> set[str]:
    if not os.path.isfile(STATE_PATH):
        return set()
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("processed", []))


def save_state(processed: set[str]) -> None:
    data = {"processed": sorted(processed)}
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ---------------------------------------------------------------------------
# Summary generation
# ---------------------------------------------------------------------------
def generate_summary(client: anthropic.Anthropic, story: dict, model: str) -> str:
    """Call Claude API to produce a targeted summary for a single story."""
    user_content = (
        f"Behavioral question section: {story['section']}\n\n"
        f"Story title: {story['title']}\n\n"
        f"Raw story:\n{story['body']}"
    )
    message = client.messages.create(
        model=model,
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    return message.content[0].text.strip()


# ---------------------------------------------------------------------------
# Appending to targettedSummaries.md
# ---------------------------------------------------------------------------
def section_heading_in_summaries(section: str) -> str:
    """Return the ## heading as it should appear in targettedSummaries.md."""
    return f"## {section}"


def append_summary_to_file(section: str, summary_block: str) -> None:
    """
    Append summary_block under the correct ## section in targettedSummaries.md.
    If the section doesn't exist yet, create it at the end of the file.
    """
    with open(SUMMARIES_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    heading = section_heading_in_summaries(section)
    section_idx = content.find(f"\n{heading}\n")
    if section_idx == -1:
        # Also try at start of file
        section_idx = content.find(f"{heading}\n")

    block_with_separator = f"\n---\n\n{summary_block}\n"

    if section_idx == -1:
        # Section doesn't exist — append a new one at the end
        addition = f"\n---\n\n{heading}\n{block_with_separator}"
        content = content.rstrip() + addition
    else:
        # Find the end of this section (next ## heading or EOF)
        # Look for next ## heading after section_idx
        next_section = re.search(r"\n## ", content[section_idx + 1:])
        if next_section:
            insert_at = section_idx + 1 + next_section.start()
        else:
            insert_at = len(content)

        # Insert before the next section
        content = content[:insert_at].rstrip() + "\n" + block_with_separator + content[insert_at:]

    with open(SUMMARIES_PATH, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Core update loop
# ---------------------------------------------------------------------------
def run_once(client: anthropic.Anthropic, model: str) -> int:
    """
    Check for new stories and generate summaries for any found.
    Returns the number of new stories processed.
    """
    if not os.path.isfile(RAW_STORIES_PATH):
        print(f"[WARN] Raw stories file not found: {RAW_STORIES_PATH}", flush=True)
        return 0

    with open(RAW_STORIES_PATH, "r", encoding="utf-8") as f:
        raw_md = f.read()

    all_stories = parse_raw_stories(raw_md)
    processed = load_state()
    new_stories = [s for s in all_stories if s["key"] not in processed]

    if not new_stories:
        print(f"[{_ts()}] No new stories found ({len(all_stories)} total, all processed).", flush=True)
        return 0

    print(f"[{_ts()}] Found {len(new_stories)} new story/stories to summarise.", flush=True)

    for story in new_stories:
        print(f"  → Generating summary: [{story['section']}] {story['title']} ...", flush=True)
        try:
            summary = generate_summary(client, story, model)
            append_summary_to_file(story["section"], summary)
            processed.add(story["key"])
            save_state(processed)
            print(f"    ✔ Appended to targettedSummaries.md", flush=True)
        except Exception as e:
            print(f"    ✘ Error: {e}", flush=True)

    return len(new_stories)


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Watch rawStorySummary.md for new stories and auto-generate summaries."
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single check and exit (good for cron / Task Scheduler).",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL,
        metavar="SECONDS",
        help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL}). Ignored with --once.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Clear processed state and regenerate summaries for ALL stories.",
    )
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(SUMMARIES_PATH):
        print(f"ERROR: targettedSummaries.md not found at {SUMMARIES_PATH}", file=sys.stderr)
        sys.exit(1)

    if args.rebuild:
        if os.path.isfile(STATE_PATH):
            os.remove(STATE_PATH)
        print(f"[{_ts()}] State cleared — will regenerate all summaries.", flush=True)

    client = anthropic.Anthropic(api_key=api_key)

    if args.once:
        run_once(client, args.model)
        return

    print(
        f"[{_ts()}] Watcher started. Polling every {args.interval}s. Press Ctrl+C to stop.",
        flush=True,
    )
    try:
        while True:
            run_once(client, args.model)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print(f"\n[{_ts()}] Watcher stopped.", flush=True)


if __name__ == "__main__":
    main()

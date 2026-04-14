"""
Generate a top 10 behavioral stories reference sheet for a specific job interview.

This script handles file I/O only — no API calls. Story selection is done by
Claude Code reading the context output and passing a JSON selection back via
--write.

Workflow:
    # Step 1 — print job description + story library for Claude to read:
    python scripts/generate_top10_stories.py "IonQ"

    # Step 2 — Claude selects top 10 and calls --write with the JSON:
    python scripts/generate_top10_stories.py "IonQ" --write '<json>'

    # Read selection JSON from stdin instead of inline arg:
    python scripts/generate_top10_stories.py "IonQ" --write -

Other commands:
    # List available job output folders:
    python scripts/generate_top10_stories.py --list

    # Validate folder + show story count without full context dump:
    python scripts/generate_top10_stories.py "IonQ" --dry-run

Output:
    Ted_Cohen-Top10BehavioralStories-[CompanyName]-[RoleTitle].md
    Saved to: skills/job-application-helper/assets/outputs/[matched-folder]/

Selection JSON schema (pass to --write):
    {
      "stories": [
        {
          "rank": 1,
          "section": "<behavioral question category>",
          "title": "<exact story title from context output, including → part>",
          "short_name": "<4-6 word version for the summary table>",
          "career_stage": "<as shown in story block>",
          "primary_attributes": "<3-6 word phrase: what this story proves>",
          "strong_for": "<short phrase: interview question types it answers>"
        },
        ... (10 total, ranked 1-10)
      ],
      "group_1_4_label": "<≤8 word theme for stories 1-4>",
      "group_5_8_label": "<≤8 word theme for stories 5-8>",
      "group_9_10_label": "<≤8 word theme for stories 9-10>"
    }
"""

import argparse
import json
import os
import re
import sys

# Ensure UTF-8 output on Windows terminals that default to cp1252
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
SUMMARIES_PATH = os.path.join(SKILL_DIR, "targettedSummaries.md")
OUTPUTS_DIR = os.path.normpath(
    os.path.join(SKILL_DIR, "..", "job-application-helper", "assets", "outputs")
)

# ---------------------------------------------------------------------------
# Folder resolution
# ---------------------------------------------------------------------------

def list_job_folders() -> list[str]:
    """Return sorted list of job output folder names."""
    if not os.path.isdir(OUTPUTS_DIR):
        return []
    return sorted(
        d for d in os.listdir(OUTPUTS_DIR)
        if os.path.isdir(os.path.join(OUTPUTS_DIR, d))
    )


def find_job_folder(search_term: str) -> list[str]:
    """
    Return folder names whose name contains search_term (case-insensitive).
    Strips hyphens and spaces from both sides for a forgiving match.
    """
    needle = re.sub(r"[-\s]+", "", search_term).lower()
    matches = []
    for folder in list_job_folders():
        haystack = re.sub(r"[-\s]+", "", folder).lower()
        if needle in haystack:
            matches.append(folder)
    return matches


def parse_folder_name(folder: str) -> tuple[str, str]:
    """
    Extract (CompanyName, RoleTitle) from a folder named YYMMDD-Company-Role.
    Returns the raw parts after stripping the date prefix if present.
    """
    parts = folder.split("-", 1)
    if re.match(r"^\d{6}$", parts[0]) and len(parts) > 1:
        rest = parts[1]
    else:
        rest = folder
    halves = rest.split("-", 1)
    company = halves[0] if halves else rest
    role = halves[1].replace("-", " ") if len(halves) > 1 else ""
    return company, role


# ---------------------------------------------------------------------------
# Story parsing
# ---------------------------------------------------------------------------

def parse_story_blocks(summaries_md: str) -> list[dict]:
    """
    Parse targettedSummaries.md into a flat list of story dicts:
        {section, title, full_block}

    Stories are ### headings within ## sections.
    """
    stories = []

    section_pattern = re.compile(r"^## (.+)$", re.MULTILINE)
    story_pattern = re.compile(r"^### (.+)$", re.MULTILINE)

    section_matches = list(section_pattern.finditer(summaries_md))

    for i, sec_match in enumerate(section_matches):
        section = sec_match.group(1).strip()
        sec_start = sec_match.end()
        sec_end = section_matches[i + 1].start() if i + 1 < len(section_matches) else len(summaries_md)
        sec_body = summaries_md[sec_start:sec_end]

        story_matches = list(story_pattern.finditer(sec_body))
        for j, story_match in enumerate(story_matches):
            title = story_match.group(1).strip()
            block_start = story_match.start()
            block_end = story_matches[j + 1].start() if j + 1 < len(story_matches) else len(sec_body)
            full_block = sec_body[block_start:block_end].strip()
            full_block = re.sub(r"\n---\s*$", "", full_block).strip()
            stories.append({
                "section": section,
                "title": title,
                "full_block": full_block,
            })

    return stories


# ---------------------------------------------------------------------------
# Context output (for Claude to read)
# ---------------------------------------------------------------------------

def print_context(job_description: str, stories: list[dict], folder_name: str) -> None:
    """
    Print job description and full story library to stdout so Claude can
    read the context and make a selection.
    """
    print(f"=== JOB FOLDER: {folder_name} ===")
    print()
    print("=== JOB DESCRIPTION ===")
    print(job_description)
    print()
    print(f"=== STORY LIBRARY ({len(stories)} stories) ===")
    print()
    for s in stories:
        print(f"[Section: {s['section']}]")
        print(s["full_block"])
        print()
        print("---")
        print()
    print("=== END OF CONTEXT ===")
    print()
    print("Select the top 10 stories for this role and call:")
    print(f'  python scripts/generate_top10_stories.py "{folder_name}" --write \'<json>\'')
    print()
    print("JSON schema: see module docstring or README.")


# ---------------------------------------------------------------------------
# Document generation
# ---------------------------------------------------------------------------

def build_document(
    selection: dict,
    stories_by_title: dict[str, dict],
    company: str,
    role: str,
    folder_name: str,
) -> str:
    """Assemble the full markdown reference document."""
    selected = sorted(selection["stories"], key=lambda s: s["rank"])
    g14 = selection.get("group_1_4_label", "Core role fit")
    g58 = selection.get("group_5_8_label", "Technical rigor & problem solving")
    g910 = selection.get("group_9_10_label", "Judgment & leadership")

    role_display = role.replace("-", " ") if role else folder_name
    today = _today_str()

    lines = [
        f"# {company} — Top 10 Behavioral Anchor Stories",
        f"## {role_display} | Interview Reference Sheet",
        f"### Prepared {today}",
        "",
        "---",
        "",
        "## Quick Reference Table",
        "",
        "| # | Anchor Story | Career Stage | Primary Attributes | Strong For Questions About… |",
        "|---|---|---|---|---|",
    ]

    for s in selected:
        lines.append(
            f"| {s['rank']} | {s['short_name']} "
            f"| {s['career_stage']} "
            f"| {s['primary_attributes']} "
            f"| {s['strong_for']} |"
        )

    lines += [
        "",
        f"**Stories 1–4** → {g14}  ",
        f"**Stories 5–8** → {g58}  ",
        f"**Stories 9–10** → {g910}",
        "",
        "---",
        "",
        "## Story Details",
        "",
    ]

    for s in selected:
        title = s["title"]
        story = stories_by_title.get(title)
        if story:
            block = re.sub(r"^### ", f"### {s['rank']}. ", story["full_block"], count=1)
            lines.append(block)
        else:
            lines.append(f"### {s['rank']}. {title}")
            lines.append("*(Story block not found — check targettedSummaries.md)*")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _today_str() -> str:
    from datetime import date
    d = date.today()
    return d.strftime("%B %d, %Y").replace(" 0", " ")


# ---------------------------------------------------------------------------
# Shared: resolve folder and load files
# ---------------------------------------------------------------------------

def resolve(job: str) -> tuple[str, str, str, list[dict]]:
    """
    Resolve job search term to (folder_name, folder_path, job_description, stories).
    Exits with an error message if resolution fails.
    """
    matches = find_job_folder(job)
    if not matches:
        print(f"ERROR: No job folder found matching '{job}'.", file=sys.stderr)
        print("Run with --list to see available folders.", file=sys.stderr)
        sys.exit(1)
    if len(matches) > 1:
        print(f"Multiple folders match '{job}':", file=sys.stderr)
        for m in matches:
            print(f"  {m}", file=sys.stderr)
        print("Refine your search term to match exactly one folder.", file=sys.stderr)
        sys.exit(1)

    folder_name = matches[0]
    folder_path = os.path.join(OUTPUTS_DIR, folder_name)
    jd_path = os.path.join(folder_path, "job_description.md")

    if not os.path.isfile(jd_path):
        print(f"ERROR: job_description.md not found in {folder_path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(SUMMARIES_PATH):
        print(f"ERROR: targettedSummaries.md not found at {SUMMARIES_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(jd_path, "r", encoding="utf-8") as f:
        job_description = f.read()

    with open(SUMMARIES_PATH, "r", encoding="utf-8") as f:
        summaries_md = f.read()

    stories = parse_story_blocks(summaries_md)
    if not stories:
        print("ERROR: No story blocks found in targettedSummaries.md.", file=sys.stderr)
        sys.exit(1)

    return folder_name, folder_path, job_description, stories


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a top 10 behavioral stories doc for a job interview.\n\n"
            "Default (no flags): print context for Claude to read and select from.\n"
            "--write '<json>': write the document using Claude's selection."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "job",
        nargs="?",
        help="Company name, role title, or output folder name to search for.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available job output folders and exit.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate folder and show story count without printing full context.",
    )
    parser.add_argument(
        "--write",
        metavar="JSON",
        help=(
            "Selection JSON string (or '-' to read from stdin). "
            "Writes the output document to the job's output folder."
        ),
    )
    args = parser.parse_args()

    # --list
    if args.list:
        folders = list_job_folders()
        if not folders:
            print("No job output folders found.")
        else:
            print(f"Available job folders ({len(folders)}):")
            for f in folders:
                print(f"  {f}")
        return

    if not args.job:
        parser.error("Provide a job search term or use --list to see available folders.")

    # --dry-run: just validate and report
    if args.dry_run:
        folder_name, folder_path, job_description, stories = resolve(args.job)
        print(f"Folder   : {folder_name}")
        print(f"JD chars : {len(job_description)}")
        print(f"Stories  : {len(stories)}")
        print()
        print("Story inventory:")
        for s in stories:
            print(f"  [{s['section']}] {s['title']}")
        return

    # --write: accept selection JSON and write document
    if args.write is not None:
        folder_name, folder_path, _, stories = resolve(args.job)

        if args.write == "-":
            raw_json = sys.stdin.read()
        else:
            raw_json = args.write

        # Strip accidental markdown fences
        raw_json = re.sub(r"^```(?:json)?\s*", "", raw_json.strip())
        raw_json = re.sub(r"\s*```$", "", raw_json)

        try:
            selection = json.loads(raw_json)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON passed to --write: {e}", file=sys.stderr)
            sys.exit(1)

        if "stories" not in selection or len(selection["stories"]) == 0:
            print("ERROR: JSON must contain a non-empty 'stories' array.", file=sys.stderr)
            sys.exit(1)

        stories_by_title = {s["title"]: s for s in stories}
        company, role = parse_folder_name(folder_name)
        document = build_document(selection, stories_by_title, company, role, folder_name)

        out_filename = f"Ted_Cohen-Top10BehavioralStories-{company}"
        if role:
            role_slug = re.sub(r"\s+", "", role)
            out_filename += f"-{role_slug}"
        out_filename += ".md"
        out_path = os.path.join(folder_path, out_filename)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(document)

        selected = sorted(selection["stories"], key=lambda s: s["rank"])
        print(f"Written: {out_path}")
        print()
        print("Selected stories:")
        for s in selected:
            print(f"  {s['rank']:2}. {s['short_name']}")
        return

    # Default: print context for Claude to read
    folder_name, folder_path, job_description, stories = resolve(args.job)
    print_context(job_description, stories, folder_name)


if __name__ == "__main__":
    main()

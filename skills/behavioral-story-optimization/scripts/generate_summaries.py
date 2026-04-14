"""
Generate targeted behavioral story summaries from rawStorySummary.md.

Reads the raw stories asset, calls the Claude API to compress each story into
the Top 10 Anchor Stories format, and writes the result to targettedSummaries.md
in the skill root.

Usage:
    python scripts/generate_summaries.py

Requires:
    pip install anthropic
    ANTHROPIC_API_KEY environment variable set
"""

import os
import re
import sys
import anthropic

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
RAW_STORIES_PATH = os.path.join(SKILL_DIR, "assets", "rawStorySummary.md")
OUTPUT_PATH = os.path.join(SKILL_DIR, "targettedSummaries.md")

FORMAT_EXAMPLE = """\
### Story Title → Outcome

**Career stage:** Early industry
**Core proof:** Technical rigor → business impact

- **Situation:** One sentence describing the context and challenge.
- **Action:** One sentence describing what you specifically did.
- **Result:** One sentence describing the measurable or meaningful outcome.

**Use for:**
- ✔ Persuasion with data
- ✔ Good judgment / logic
- ✔ Influencing decisions without authority

**Opening line:** "A good example is when I discovered that our absorption measurements were systematically inflated — I traced it to film non-uniformity, found software that corrected for it, and the new numbers directly justified a major VBG research investment."
"""

SYSTEM_PROMPT = """\
You are a behavioral interview coach helping a senior optical/photonic engineer \
named Ted prepare STAR-format story summaries for job interviews.

For each raw story provided, produce a targeted summary using EXACTLY this format:

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
- "Use for" tags should match standard behavioral question categories \
  (e.g., Persuasion with data, Dealing with conflict, Above and beyond, \
  Prioritization, Split-second decisions, Failure & learning, Mentorship, \
  Delegation, Unpopular decisions, Resilience, Taking initiative, etc.)
- Opening line must sound natural and spoken, not like a resume bullet.
- Do NOT add commentary or preamble — output only the formatted summary block.
"""


def parse_sections(md_text: str) -> list[dict]:
    """
    Split rawStorySummary.md into sections by H2 heading (## Question prompt).
    Returns list of dicts with 'question' and 'body'.
    """
    sections = []
    pattern = re.compile(r"^## (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(md_text))
    for i, match in enumerate(matches):
        question = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        body = md_text[start:end].strip()
        if body:
            sections.append({"question": question, "raw": body})
    return sections


def summarise_section(client: anthropic.Anthropic, section: dict) -> str:
    """Call Claude to compress one raw story section into targeted summaries."""
    user_content = (
        f"Behavioral question prompt: {section['question']}\n\n"
        f"Raw story content:\n{section['raw']}\n\n"
        "Produce a targeted summary for EACH distinct story in the raw content above. "
        "If there are two stories, output two summary blocks separated by a blank line."
    )
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    return message.content[0].text.strip()


def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(RAW_STORIES_PATH):
        print(f"ERROR: Raw stories file not found at {RAW_STORIES_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(RAW_STORIES_PATH, "r", encoding="utf-8") as f:
        raw_md = f.read()

    sections = parse_sections(raw_md)
    if not sections:
        print("ERROR: No sections found in rawStorySummary.md.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(sections)} sections. Generating summaries via Claude API...")

    client = anthropic.Anthropic(api_key=api_key)

    output_parts = [
        "# Targeted Behavioral Story Summaries\n",
        "Compressed STAR-format summaries ready for use as interview responses.\n",
        "Format reference: Top 10 Anchor Stories — Interview Reference Sheet.\n",
        "---\n",
    ]

    for i, section in enumerate(sections, 1):
        print(f"  [{i}/{len(sections)}] {section['question'][:70]}...")
        summary = summarise_section(client, section)
        output_parts.append(f"## {section['question']}\n")
        output_parts.append(summary)
        output_parts.append("\n\n---\n")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(output_parts))

    print(f"\nDone. Summaries written to:\n  {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

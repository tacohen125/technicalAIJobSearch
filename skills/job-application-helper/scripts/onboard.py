#!/usr/bin/env python3
"""
onboard.py — First-time setup for job-application-helper.

Parses your baseline resume, detects your name and experience sections,
scaffolds reference documents pre-populated with your background,
copies your resume into assets/, and writes config.sh so all scripts
know your filename.

Usage:
  python scripts/onboard.py --resume /path/to/Your_Name-RESUME.docx
  python scripts/onboard.py --resume /path/to/resume.docx [OPTIONS]

Options:
  --resume <path>       Path to your baseline .docx resume (REQUIRED)
  --cover-letter <path> Path to your cover letter .docx (optional)
  --name "First Last"   Override auto-detected name
  --upstream-url <url>  GitHub URL to set as git upstream remote
  --no-setup-baseline   Skip running setup_baseline.sh after setup
  --dry-run             Print what would happen without writing files
  --force               Overwrite existing files without prompting
"""
from __future__ import annotations

import argparse
import io
import re
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

# Use UTF-8 stdout on Windows to avoid cp1252 encoding errors
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Locate parse_resume so it can be imported regardless of CWD
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))
from parse_resume import parse_resume  # noqa: E402  (after sys.path tweak)


# ---------------------------------------------------------------------------
# Name parsing
# ---------------------------------------------------------------------------

def parse_name(raw: str) -> tuple[str, str, str]:
    """
    Extract (first, last, filename_base) from a raw name string.

    Strips:
      • parenthetical nicknames: "Theodore (Ted) Cohen" -> first="Theodore", last="Cohen"
      • post-nominal titles: "Jane Doe PhD" / "Jane Doe, PhD" -> "Jane Doe"
      • leading/trailing whitespace and punctuation

    Returns:
      first         — first name (Theodore)
      last          — last name (Cohen)
      filename_base — "First_Last" safe for filenames (Theodore_Cohen)
    """
    POSTNOMINAL = re.compile(
        r",?\s+(?:PhD|Ph\.D\.?|MD|M\.D\.?|MS|M\.S\.?|MBA|JD|J\.D\.?|"
        r"PE|PMP|CPA|CFA|CPA|Esq\.?|Jr\.?|Sr\.?|II|III|IV)\.?$",
        re.IGNORECASE,
    )
    # Strip trailing titles
    cleaned = POSTNOMINAL.sub("", raw).strip()
    # Strip parenthetical nickname
    cleaned = re.sub(r'\s*\([^)]*\)\s*', ' ', cleaned).strip()
    # Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    parts = cleaned.split()
    first = parts[0] if parts else "User"
    last  = parts[-1] if len(parts) > 1 else ""
    filename_base = f"{first}_{last}" if last else first
    # Sanitise: keep only alphanumerics, underscores, hyphens
    filename_base = re.sub(r'[^\w\-]', '_', filename_base)

    return first, last, filename_base


# ---------------------------------------------------------------------------
# Scaffolding helpers
# ---------------------------------------------------------------------------

def _section(result: dict, sec_type: str) -> dict | None:
    """Return the first detected section of the given type, or None."""
    for s in result["sections"]:
        if s["type"] == sec_type:
            return s
    return None


def _fill(detected: str, placeholder: str) -> str:
    """Return detected value if present, else placeholder."""
    return detected if detected else placeholder


def scaffold_user_profile(result: dict, first: str, last: str) -> str:
    """
    Build a user_profile.md pre-populated with detected resume content.

    • Basic info block with [FILL IN] placeholders
    • Key Competencies as a <!-- draft --> comment from detected skills text
    • One ### subsection per job with role, dates, and actual bullet text
    • Education, Publications, Presentations sections if detected
    """
    lines = []
    ci = result.get("contact_info", {})

    # ── Header ──────────────────────────────────────────────────────────────
    lines.append(f"# User Profile: {first} {last}\n")

    # ── Basic info ──────────────────────────────────────────────────────────
    lines.append("## Basic Information\n")
    lines.append(f"- **Name:** {first} {last}\n")
    lines.append(f"- **Location:** {_fill(ci.get('location', ''), '[FILL IN city, state]')}\n")
    lines.append(f"- **Email:** {_fill(ci.get('email', ''), '[FILL IN]')}\n")
    lines.append(f"- **Phone:** {_fill(ci.get('phone', ''), '[FILL IN]')}\n")
    lines.append(f"- **LinkedIn:** {_fill(ci.get('linkedin', ''), '[FILL IN URL]')}\n")
    lines.append("- **GitHub / Portfolio:** [FILL IN or remove]\n")
    lines.append("\n---\n")

    # ── Summary / Branding Statement ────────────────────────────────────────
    lines.append("## Professional Summary\n")
    summary_sec = _section(result, "SUMMARY")
    if summary_sec and summary_sec.get("summary_text"):
        lines.append("<!-- Branding statement draft detected from resume:\n")
        lines.append(f"{summary_sec['summary_text']}\n")
        lines.append("-->\n")
        lines.append("[FILL IN your polished 2-3 sentence professional summary]\n")
    else:
        lines.append("[FILL IN your 2-3 sentence professional summary]\n")
    lines.append("\n---\n")

    # ── Key Competencies ────────────────────────────────────────────────────
    lines.append("## Key Competencies\n")
    skills_sec = _section(result, "SKILLS") or _section(result, "EXPERTISE")
    if skills_sec and skills_sec.get("skills_lines"):
        lines.append("<!-- Draft from resume Skills section:\n")
        for ln in skills_sec["skills_lines"]:
            lines.append(f"  {ln}\n")
        lines.append("-->\n\n")
        lines.append("**[Review the draft above and clean up below]**\n\n")
        # Add them as plain text too for easy editing
        for ln in skills_sec["skills_lines"]:
            lines.append(f"- {ln}\n")
    else:
        lines.append("- [FILL IN core technical skill 1]\n")
        lines.append("- [FILL IN core technical skill 2]\n")
        lines.append("- [FILL IN core technical skill 3]\n")
    lines.append("\n---\n")

    # ── Experience ──────────────────────────────────────────────────────────
    lines.append("## Work Experience\n")
    exp_sec = _section(result, "EXPERIENCE")
    if exp_sec and exp_sec.get("jobs"):
        for job in exp_sec["jobs"]:
            company = job.get("company", "[Company]")
            location = job.get("location", "")
            title    = job.get("title", "[Title]")
            dates    = job.get("dates", "[Dates]")

            heading = f"### {company}"
            if location:
                heading += f" — {location}"
            lines.append(f"{heading}\n")
            # Only emit title/dates line if at least one is populated
            if title or dates:
                title_str = f"**{title}**" if title else ""
                dates_str = f"  |  {dates}" if dates else ""
                lines.append(f"{title_str}{dates_str}")
                lines.append("\n\n")
            else:
                lines.append("\n")

            bullet_texts = job.get("bullet_texts", [])
            if bullet_texts:
                for bt in bullet_texts:
                    lines.append(f"- {bt}\n")
            else:
                for _ in range(max(job.get("bullet_count", 3), 1)):
                    lines.append("- [FILL IN accomplishment with metric]\n")
            lines.append("\n")
    else:
        lines.append("### [Company Name] — [City, State]\n")
        lines.append("**[Job Title]**  |  [Start Date – End Date]\n\n")
        lines.append("- [FILL IN accomplishment with metric]\n")
        lines.append("- [FILL IN accomplishment with metric]\n\n")
    lines.append("---\n")

    # ── Education ───────────────────────────────────────────────────────────
    lines.append("\n## Education\n")
    edu_sec = _section(result, "EDUCATION")
    edu_lines = edu_sec.get("content_lines", []) if edu_sec else []
    if edu_lines:
        # Render each line; tab-delimited lines (Institution\t\tGraduated) become bold headers
        for ln in edu_lines:
            if '\t' in ln:
                # Split on first tab cluster: "University: City, State  Graduated: Date"
                parts = [p.strip() for p in ln.split('\t') if p.strip()]
                lines.append(f"**{parts[0]}**")
                if len(parts) > 1:
                    lines.append(f"  —  {parts[-1]}")
                lines.append("\n")
            else:
                lines.append(f"{ln}\n")
        lines.append("\n")
    else:
        lines.append("**[Degree]**, [Major]  \n")
        lines.append("[University Name], [City, State] — [Year]\n\n")
    lines.append("---\n")

    # ── Publications (only if detected) ─────────────────────────────────────
    pub_sec = _section(result, "PUBLICATIONS")
    if pub_sec:
        lines.append("\n## Select Publications\n")
        pub_lines = pub_sec.get("content_lines", [])
        if pub_lines:
            for i, ln in enumerate(pub_lines, 1):
                # First non-bulleted line is often an intro sentence, not a citation
                lines.append(f"{i}. {ln}\n")
        else:
            lines.append("1. [FILL IN citation]\n")
        lines.append("\n---\n")

    # ── Presentations (only if detected) ────────────────────────────────────
    pres_sec = _section(result, "PRESENTATIONS")
    if pres_sec:
        lines.append("\n## Select Presentations\n")
        pres_lines = pres_sec.get("content_lines", [])
        if pres_lines:
            for i, ln in enumerate(pres_lines, 1):
                lines.append(f"{i}. {ln}\n")
        else:
            lines.append("1. [FILL IN presentation title, venue, year]\n")
        lines.append("\n---\n")

    # ── Target roles ────────────────────────────────────────────────────────
    lines.append("\n## Target Roles\n")
    lines.append("- **Role type:** [FILL IN, e.g. Senior Engineer, Research Scientist]\n")
    lines.append("- **Industries:** [FILL IN]\n")
    lines.append("- **Preferred locations:** [FILL IN]\n")
    lines.append("- **Open to remote:** [Yes / No / Hybrid only]\n")

    return "".join(lines)


def scaffold_accomplishments(result: dict) -> str:
    """
    Build list_of_key_accomplishments.md.

    If ACCOMPLISHMENTS section detected: uses real entries with
    [Add metrics: ...] prompts. Otherwise: 3 blank templates.
    """
    lines = []
    lines.append("# Key Accomplishments\n\n")
    lines.append(
        "Use this list as a quick-reference during resume tailoring and cover letter writing.\n"
        "Keep entries focused on outcomes and metrics.\n\n"
    )
    lines.append("---\n\n")

    acc_sec = _section(result, "ACCOMPLISHMENTS")
    if acc_sec and acc_sec.get("accomplishments"):
        for i, entry in enumerate(acc_sec["accomplishments"], 1):
            lines.append(f"## {i}. {entry[:80]}{'...' if len(entry) > 80 else ''}\n\n")
            lines.append(f"**Full text:**\n{entry}\n\n")
            lines.append("**[Add metrics: quantify the impact — %, $, time saved, scale, etc.]**\n\n")
            lines.append("**Tags:** [FILL IN — e.g. leadership, technical, cross-functional]\n\n")
            lines.append("---\n\n")
    else:
        for i in range(1, 4):
            lines.append(f"## {i}. [Title of Accomplishment]\n\n")
            lines.append("**Full text:**\n[Describe the accomplishment in 1-3 sentences]\n\n")
            lines.append("**Metrics:** [Quantify impact — %, $, headcount, time, scale]\n\n")
            lines.append("**Tags:** [e.g. leadership, technical, cross-functional, cost-savings]\n\n")
            lines.append("---\n\n")

    return "".join(lines)


def scaffold_target_companies() -> str:
    """Blank list_of_target_companies.md template."""
    return dedent("""\
        # Target Companies

        List companies you are actively targeting. The job-application-helper skill
        uses this to tailor cover letters and research company-specific talking points.

        ---

        ## Tier 1 — Most Interested

        | Company | Role(s) | Why Interested | Status |
        |---------|---------|----------------|--------|
        | [Company Name] | [Role] | [One-line reason] | Researching |

        ---

        ## Tier 2 — Strong Interest

        | Company | Role(s) | Why Interested | Status |
        |---------|---------|----------------|--------|
        | [Company Name] | [Role] | [One-line reason] | Not yet applied |

        ---

        ## Notes

        - [Any general notes about your search strategy]
    """)


# ---------------------------------------------------------------------------
# File write helpers (respect --dry-run and --force)
# ---------------------------------------------------------------------------

class Writer:
    def __init__(self, dry_run: bool, force: bool):
        self.dry_run = dry_run
        self.force   = force
        self._actions: list[str] = []

    def write_text(self, path: Path, content: str, label: str = "") -> None:
        tag = label or str(path)
        if self.dry_run:
            self._actions.append(f"  [DRY RUN] would write: {tag}")
            return
        if path.exists() and not self.force:
            resp = input(f"  {tag} already exists. Overwrite? [y/N] ").strip().lower()
            if resp not in ("y", "yes"):
                print(f"  Skipped: {tag}")
                return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  Wrote: {tag}")

    def copy_file(self, src: Path, dst: Path, label: str = "") -> bool:
        """Copy src -> dst. Returns True if copy happened."""
        tag = label or f"{src.name} -> {dst}"
        if self.dry_run:
            self._actions.append(f"  [DRY RUN] would copy: {tag}")
            return False
        if dst.exists() and not self.force:
            if src.resolve() == dst.resolve():
                print(f"  Already in place: {dst.name}")
                return True
            resp = input(f"  {dst.name} already exists. Overwrite? [y/N] ").strip().lower()
            if resp not in ("y", "yes"):
                print(f"  Skipped: {dst.name}")
                return False
        if src.resolve() == dst.resolve():
            print(f"  Already in place: {dst.name}")
            return True
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        print(f"  Copied: {tag}")
        return True

    def summary(self) -> None:
        if self.dry_run and self._actions:
            print("\nDRY RUN — nothing was written. Planned actions:")
            for a in self._actions:
                print(a)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Onboard a new user to job-application-helper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--resume",         required=True,  help="Path to your baseline .docx resume")
    ap.add_argument("--cover-letter",   default=None,   help="Path to your cover letter .docx (optional)")
    ap.add_argument("--name",           default=None,   help="Override auto-detected name (e.g. 'Jane Doe')")
    ap.add_argument("--upstream-url",   default=None,   help="GitHub URL to set as git upstream remote")
    ap.add_argument("--no-setup-baseline", action="store_true",
                    help="Skip running setup_baseline.sh after writing files")
    ap.add_argument("--dry-run",        action="store_true", help="Print actions without writing")
    ap.add_argument("--force",          action="store_true", help="Overwrite existing files without prompting")
    args = ap.parse_args()

    resume_path = Path(args.resume).resolve()
    if not resume_path.exists():
        print(f"ERROR: Resume file not found: {resume_path}", file=sys.stderr)
        sys.exit(1)
    if resume_path.suffix.lower() != ".docx":
        print(f"ERROR: Expected a .docx file, got: {resume_path.name}", file=sys.stderr)
        sys.exit(1)

    cover_letter_path = Path(args.cover_letter).resolve() if args.cover_letter else None
    if cover_letter_path and not cover_letter_path.exists():
        print(f"ERROR: Cover letter not found: {cover_letter_path}", file=sys.stderr)
        sys.exit(1)

    skill_dir  = _SCRIPT_DIR.parent            # skills/job-application-helper/
    assets_dir = skill_dir / "assets"
    refs_dir   = skill_dir / "references"

    writer = Writer(dry_run=args.dry_run, force=args.force)

    # ── Step 1: Parse resume ────────────────────────────────────────────────
    print("\n=== Step 1: Parsing resume ===")
    try:
        result = parse_resume(str(resume_path))
    except Exception as e:
        print(f"ERROR: Could not parse resume: {e}", file=sys.stderr)
        sys.exit(1)

    raw_name   = result["name"]
    page_count = result.get("detected_page_count")
    n_sections = len(result["sections"])

    print(f"  Detected name     : {raw_name}")
    print(f"  Page count        : {page_count if page_count else 'unknown (open in Word and save)'}")
    print(f"  Sections detected : {n_sections}")
    for sec in result["sections"]:
        print(f"    • {sec['type']:16s}  \"{sec['header']}\"")

    # ── Step 2: Confirm / override name ─────────────────────────────────────
    print("\n=== Step 2: Confirm name ===")
    if args.name:
        confirmed_name = args.name
        print(f"  Using name from --name flag: {confirmed_name}")
    elif args.dry_run or args.force:
        confirmed_name = raw_name
        print(f"  Using detected name (non-interactive mode): {confirmed_name}")
    else:
        prompt = f"  Detected name: \"{raw_name}\"\n  Press Enter to accept, or type a correction: "
        override = input(prompt).strip()
        confirmed_name = override if override else raw_name
    print(f"  Name: {confirmed_name}")

    first, last, filename_base = parse_name(confirmed_name)
    print(f"  File prefix: {filename_base}")

    # ── Step 3: Copy resume to assets/ ──────────────────────────────────────
    print("\n=== Step 3: Copying resume to assets/ ===")
    resume_dest = assets_dir / f"{filename_base}-RESUME.docx"
    writer.copy_file(resume_path, resume_dest)

    cover_letter_dest: Path | None = None
    if cover_letter_path:
        cover_letter_dest = assets_dir / f"{filename_base}-COVERLETTER.docx"
        writer.copy_file(cover_letter_path, cover_letter_dest)

    # ── Step 4: Write config.sh ─────────────────────────────────────────────
    print("\n=== Step 4: Writing config.sh ===")
    target_pages = page_count if page_count else 2
    config_content = dedent(f"""\
        #!/usr/bin/env bash
        # config.sh — auto-generated by onboard.py on {__import__('datetime').date.today()}
        # DO NOT commit this file (it is gitignored).
        # Re-run: python scripts/onboard.py --resume /path/to/resume.docx
        USER_FIRST_NAME="{first}"
        USER_LAST_NAME="{last}"
        RESUME_BASENAME="{filename_base}-RESUME.docx"
        COVERLETTER_BASENAME="{filename_base}-COVERLETTER.docx"
        TARGET_PAGES={target_pages}
    """)
    writer.write_text(skill_dir / "config.sh", config_content, label="config.sh")

    # ── Step 5: Scaffold user_profile.md ────────────────────────────────────
    print("\n=== Step 5: Scaffolding references/user_profile.md ===")
    profile_content = scaffold_user_profile(result, first, last)
    writer.write_text(refs_dir / "user_profile.md", profile_content, label="references/user_profile.md")

    # ── Step 6: Scaffold list_of_key_accomplishments.md ─────────────────────
    print("\n=== Step 6: Scaffolding references/list_of_key_accomplishments.md ===")
    acc_content = scaffold_accomplishments(result)
    writer.write_text(
        refs_dir / "list_of_key_accomplishments.md",
        acc_content,
        label="references/list_of_key_accomplishments.md",
    )

    # ── Step 7: Scaffold list_of_target_companies.md ────────────────────────
    print("\n=== Step 7: Writing blank references/list_of_target_companies.md ===")
    companies_path = refs_dir / "list_of_target_companies.md"
    if not companies_path.exists() or args.force:
        writer.write_text(companies_path, scaffold_target_companies(),
                          label="references/list_of_target_companies.md")
    else:
        print("  Already exists; skipping (use --force to overwrite).")

    # ── Step 8: Run setup_baseline.sh ───────────────────────────────────────
    if not args.no_setup_baseline and not args.dry_run:
        print("\n=== Step 8: Running setup_baseline.sh ===")
        sys.stdout.flush()
        setup_sh = _SCRIPT_DIR / "setup_baseline.sh"
        cmd = [
            "bash", str(setup_sh),
            "--baseline", str(resume_dest),
            "--target-pages", str(target_pages),
            "--no-verify",
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"  WARNING: setup_baseline.sh exited with code {e.returncode}.", file=sys.stderr)
            print("  Reference files (xml_editing_guide.md, qa_and_delivery.md) may not be updated.")
            print("  Run manually: bash scripts/setup_baseline.sh --no-verify")
        except FileNotFoundError:
            print("  WARNING: bash not found; skipping setup_baseline.sh.", file=sys.stderr)
            print("  Run manually: bash scripts/setup_baseline.sh --no-verify")
    elif args.no_setup_baseline:
        print("\n=== Step 8: Skipped (--no-setup-baseline) ===")
    else:
        print("\n=== Step 8: Skipped (dry-run) ===")

    # ── Step 9: Git upstream remote ─────────────────────────────────────────
    if args.upstream_url and not args.dry_run:
        print("\n=== Step 9: Setting git upstream remote ===")
        try:
            subprocess.run(
                ["git", "remote", "add", "upstream", args.upstream_url],
                cwd=str(skill_dir.parent.parent),  # repo root
                check=True,
                capture_output=True,
            )
            print(f"  Set upstream -> {args.upstream_url}")
        except subprocess.CalledProcessError:
            print("  upstream remote already exists; run: git remote set-url upstream <url>")

    # ── Summary ─────────────────────────────────────────────────────────────
    writer.summary()

    print(f"""
=== Onboarding complete ===

Next steps:
  1. Fill in your details in references/user_profile.md
       (experience bullets are pre-populated from your resume)

  2. Review references/list_of_key_accomplishments.md
       (entries from your resume's accomplishments section, or blank templates)

  3. Add target companies to references/list_of_target_companies.md

  4. If you have a cover letter template, copy it to:
       assets/{filename_base}-COVERLETTER.docx
     or re-run:  python scripts/onboard.py --resume ... --cover-letter /path/to/cl.docx

  5. Review the git diff to see what changed in the reference files:
       git diff references/

  6. To tailor your first resume, invoke the skill in a Claude conversation:
       /job-application-helper
     (Claude Code CLI) or upload the packaged skill on claude.ai.
""")


if __name__ == "__main__":
    main()

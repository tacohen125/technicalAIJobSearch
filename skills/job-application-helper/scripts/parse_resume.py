#!/usr/bin/env python3
"""
parse_resume.py — Two-layer DOCX resume section detector.

Detection approach:
  Layer 1 — Word paragraph styles (Heading 1-9, Title, etc.)
             Catches any resume built with proper Word heading styles.

  Layer 2 — Multi-signal heuristic scoring (6 signals per paragraph):
               bold       +2   all content runs are bold
               allcaps    +2   text is ALL CAPS, or w:caps/w:allCaps flag set
               no_tab     +1   no tab character (rejects Company[TAB]Location lines)
               no_bullet  +1   not a list/bullet paragraph
               short_text +1   text < 50 chars (section labels are concise)
               font_bump  +1   font size ≥ 10% above document baseline
               keyword    +3   text matches a known section keyword

             Decision thresholds:
               keyword path    — keyword fired AND total ≥ 4
               no-keyword path — total ≥ 7  (strong formatting, unusual keyword)

  Approach derived from OpenResume's validated heuristics (open-resume.com),
  adapted for DOCX (they are PDF-based). Both projects' core insight:
  section titles are the only content on their line AND carry double emphasis.

Usage:
  python scripts/parse_resume.py resume.docx              # human-readable
  python scripts/parse_resume.py resume.docx --json       # JSON output
  python scripts/parse_resume.py resume.docx --verbose    # show signal breakdown
"""

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Optional

try:
    from docx import Document
except ImportError:
    print("ERROR: python-docx is required.  pip install python-docx", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Section keyword map
# ---------------------------------------------------------------------------

SECTION_KEYWORDS: dict[str, list[str]] = {
    "SUMMARY":        ["summary", "profile", "objective", "about", "overview",
                       "professional summary", "career summary", "professional profile"],
    "EXPERTISE":      ["areas of expertise", "core competencies", "competencies",
                       "areas of focus", "key competencies"],
    "SKILLS":         ["skills", "technical skills", "tools", "technologies",
                       "capabilities", "technical proficiencies", "technical expertise"],
    "ACCOMPLISHMENTS":["key accomplishments", "accomplishments", "achievements",
                       "highlights", "selected achievements", "career highlights",
                       "key technical achievements", "technical achievements",
                       "key achievements"],
    "EXPERIENCE":     ["experience", "work experience", "employment history",
                       "professional experience", "career history", "work history",
                       "employment"],
    "EDUCATION":      ["education", "academic background", "academics",
                       "educational background", "degrees", "academic credentials"],
    "PUBLICATIONS":   ["publications", "research", "peer-reviewed publications",
                       "papers", "articles", "journal articles",
                       "select publications", "selected publications",
                       "publications and patents", "select publications and patents",
                       "refereed publications", "conference papers"],
    "PRESENTATIONS":  ["presentations", "talks", "conference presentations",
                       "invited talks", "speaking",
                       "select presentations", "selected presentations",
                       "invited presentations", "poster presentations"],
    "PROJECTS":       ["projects", "side projects", "personal projects",
                       "selected projects", "key projects"],
    "CERTIFICATIONS": ["certifications", "licenses", "credentials",
                       "professional certifications", "certificates"],
    "AWARDS":         ["awards", "honors", "recognitions",
                       "awards & honors", "awards and honors", "honors & awards"],
    "VOLUNTEER":      ["volunteer", "volunteering", "community service",
                       "civic engagement", "community involvement"],
    "LANGUAGES":      ["languages", "language skills"],
    "INTERESTS":      ["interests", "hobbies", "activities"],
}

# Flat lookup: normalized keyword → section type
_KEYWORD_LOOKUP: dict[str, str] = {}
for _sec_type, _keywords in SECTION_KEYWORDS.items():
    for _kw in _keywords:
        _KEYWORD_LOOKUP[_kw.lower().strip()] = _sec_type

# Word paragraph style names that identify headings
_HEADING_STYLE_NAMES = {
    "heading 1", "heading 2", "heading 3", "heading 4",
    "heading 5", "heading 6", "title", "subtitle",
}


# ---------------------------------------------------------------------------
# Signal extraction helpers
# ---------------------------------------------------------------------------

def _text(para) -> str:
    """All visible text in a paragraph, stripped."""
    return para.text.strip()


def _any_bold(para) -> bool:
    """
    True if the paragraph contains any explicitly-bold run.
    Checks both run-level rPr and paragraph-level rPr (pPr/w:rPr).
    Uses XML inspection to handle the tri-state (True/False/None=inherit)
    behaviour of python-docx's run.font.bold.
    """
    xml = para._p.xml
    # Find every <w:b> or <w:b/> occurrence
    for m in re.finditer(r'<w:b(?:\s[^>]*)?\s*/?>|<w:b(?:\s[^>]*)?>(?:</w:b>)?', xml):
        tag = m.group(0)
        # Ignore explicit bold-off (w:val="0" or w:val="false")
        if 'w:val="0"' not in tag and 'w:val="false"' not in tag:
            return True
    return False


def _all_runs_bold(para) -> bool:
    """
    True if every non-whitespace content run is explicitly bold.
    Used as a stronger signal than _any_bold when we need higher confidence.
    """
    content_runs = [r for r in para.runs if r.text.strip()]
    if not content_runs:
        return False
    for run in content_runs:
        xml = run._r.xml
        has_b = bool(re.search(r'<w:b(?:\s[^>]*)?\s*/?>', xml))
        is_off = bool(re.search(r'<w:b[^>]*w:val="(?:0|false)"', xml))
        if not has_b or is_off:
            return False
    return True


def _text_is_allcaps(text: str) -> bool:
    """True if the text (letters only) is all uppercase."""
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)


def _any_caps_flag(para) -> bool:
    """
    True if the paragraph text is ALL CAPS, OR any run carries w:caps/w:allCaps.
    Handles both explicit formatting and text convention.
    """
    if _text_is_allcaps(_text(para)):
        return True
    xml = para._p.xml
    return bool(re.search(r'<w:(?:caps|allCaps)(?:\s[^/]*)?\s*/?>', xml))


def _has_tab(para) -> bool:
    """
    True if the paragraph contains a tab element or tab character.
    Key anti-false-positive signal: company/title lines use tabs for
    right-aligned dates/locations; section headers never do.
    """
    return '<w:tab' in para._p.xml or '\t' in para.text


def _has_numbering(para) -> bool:
    """True if the paragraph is a bullet or numbered list item."""
    return '<w:numPr>' in para._p.xml


def _get_font_size_pt(para) -> Optional[float]:
    """
    Return the font size in points from the first content run with an
    explicit w:sz value. Returns None if no explicit size is found.
    Half-point units: sz val="20" → 10pt.
    """
    for run in para.runs:
        if not run.text.strip():
            continue
        m = re.search(r'<w:sz w:val="(\d+)"', run._r.xml)
        if m:
            return int(m.group(1)) / 2.0
    return None


def _detect_baseline_font_size(doc) -> float:
    """
    Estimate body font size (in points) as the most common explicit w:sz
    value across all runs in the document. Falls back to 10pt.
    """
    sizes = []
    for para in doc.paragraphs:
        for run in para.runs:
            if not run.text.strip():
                continue
            m = re.search(r'<w:sz w:val="(\d+)"', run._r.xml)
            if m:
                sizes.append(int(m.group(1)) / 2.0)
    if sizes:
        return Counter(sizes).most_common(1)[0][0]
    return 10.0


def _detect_page_count(path: str) -> Optional[int]:
    """
    Try to read the page count from docProps/app.xml inside the .docx ZIP.
    Word writes this after a save; returns None if missing or unreadable.
    """
    try:
        with zipfile.ZipFile(path, 'r') as z:
            if 'docProps/app.xml' in z.namelist():
                xml = z.read('docProps/app.xml').decode('utf-8')
                m = re.search(r'<Pages>(\d+)</Pages>', xml)
                if m:
                    return int(m.group(1))
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Section keyword classification
# ---------------------------------------------------------------------------

def _classify_text(text: str) -> Optional[str]:
    """
    Return the SECTION_KEYWORDS type for a header text, or None.

    Matching rules (in order):
    1. Exact match after normalisation (lowercase, strip, strip trailing colon)
    2. Strip common decorative prefixes ("select", "selected", "key",
       "additional") and retry exact match — catches "Select Publications",
       "Key Achievements", etc. without enumerating every variant.
    3. Starts-with match within 30% length tolerance — catches minor extensions
       like "Technical Skills & Tools" matching "technical skills".
    """
    normalized = text.lower().strip().rstrip(':').strip()

    # Rule 1: exact match
    if normalized in _KEYWORD_LOOKUP:
        return _KEYWORD_LOOKUP[normalized]

    # Rule 2: strip decorative prefix and retry
    for prefix in ("select ", "selected ", "key ", "additional ", "relevant "):
        if normalized.startswith(prefix):
            stripped = normalized[len(prefix):]
            if stripped in _KEYWORD_LOOKUP:
                return _KEYWORD_LOOKUP[stripped]

    # Rule 3: starts-with with length tolerance
    for kw, sec_type in _KEYWORD_LOOKUP.items():
        if normalized.startswith(kw) and len(normalized) <= len(kw) * 1.3:
            return sec_type

    return None


# ---------------------------------------------------------------------------
# Layer 1: Word paragraph style detection
# ---------------------------------------------------------------------------

def _get_style_chain(para) -> list[str]:
    """Return style names in inheritance order (most specific first)."""
    chain = []
    style = para.style
    seen = set()
    while style and len(chain) < 10:
        name = style.name.lower()
        if name in seen:
            break
        seen.add(name)
        chain.append(name)
        style = style.base_style
    return chain


def _layer1_is_heading(para) -> bool:
    """
    True if the paragraph's style (or any ancestor) is a recognised heading style.
    Traverses the inheritance chain so custom styles derived from Heading 1 are caught.
    """
    for name in _get_style_chain(para):
        if name in _HEADING_STYLE_NAMES:
            return True
        if re.match(r'heading\s*\d', name):
            return True
    return False


# ---------------------------------------------------------------------------
# Layer 2: Multi-signal heuristic scoring
# ---------------------------------------------------------------------------

_SIGNAL_POINTS = {
    "bold":       2,
    "allcaps":    2,
    "no_tab":     1,
    "no_bullet":  1,
    "short_text": 1,
    "font_bump":  1,
    "keyword":    3,
}


def _compute_signals(para, baseline_pt: float) -> dict[str, bool]:
    """
    Compute all seven heuristic signals for a paragraph.
    Returns dict of signal_name → bool (fired or not).
    """
    text = _text(para)
    sz = _get_font_size_pt(para)
    sec_type = _classify_text(text)

    return {
        "bold":       _all_runs_bold(para),
        "allcaps":    _any_caps_flag(para),
        "no_tab":     not _has_tab(para),
        "no_bullet":  not _has_numbering(para),
        "short_text": 0 < len(text) < 50,
        "font_bump":  (sz is not None) and (sz > baseline_pt * 1.10),
        "keyword":    sec_type is not None,
    }


def _signal_score(signals: dict[str, bool]) -> int:
    return sum(_SIGNAL_POINTS[k] for k, fired in signals.items() if fired)


def _layer2_is_heading(signals: dict[str, bool]) -> bool:
    """
    Two-path decision (see module docstring for rationale):
      keyword path    — keyword fired  AND  total ≥ 4
      no-keyword path — total ≥ 7 (requires strong multi-signal formatting)
    """
    total = _signal_score(signals)
    if signals["keyword"]:
        return total >= 4
    return total >= 7


# ---------------------------------------------------------------------------
# Name and contact info detection
# ---------------------------------------------------------------------------

_CONTACT_PATTERN = re.compile(
    r'[@|]|linkedin|github|http|www\.|'
    r'\d{3}[\s.\-]\d{3}[\s.\-]\d{4}|'  # phone
    r'\b\d{5}\b',                        # ZIP
    re.IGNORECASE,
)

_EMAIL_RE    = re.compile(r'[\w.+\-]+@[\w.\-]+\.\w+')
_PHONE_RE    = re.compile(r'\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}')
_LINKEDIN_RE = re.compile(r'linkedin\.com/in/[\w\-]+', re.IGNORECASE)
_LOCATION_RE = re.compile(r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*,\s+[A-Z]{2}\b')


def detect_contact_info(doc, first_header_idx: int) -> dict:
    """
    Extract contact fields from the pre-header area of the resume.

    Scans the same window as detect_name() and looks for:
      email    — user@domain.tld
      phone    — (NNN) NNN-NNNN or variants
      linkedin — linkedin.com/in/handle
      location — City, ST pattern (not always present)

    Returns a dict with whichever fields were found (keys absent if not found).
    """
    limit = min(first_header_idx, 7) if first_header_idx > 0 else 7
    info: dict = {}
    for para in doc.paragraphs[:limit]:
        text = _text(para)
        if not text:
            continue
        if not info.get("email"):
            m = _EMAIL_RE.search(text)
            if m:
                info["email"] = m.group(0)
        if not info.get("phone"):
            m = _PHONE_RE.search(text)
            if m:
                info["phone"] = m.group(0)
        if not info.get("linkedin"):
            m = _LINKEDIN_RE.search(text)
            if m:
                val = m.group(0)
                info["linkedin"] = val if val.startswith("http") else "https://" + val
        if not info.get("location"):
            m = _LOCATION_RE.search(text)
            if m:
                info["location"] = m.group(0)
    return info


def detect_name(doc, first_header_idx: int) -> str:
    """
    Detect the candidate name from the top of the resume (before first header).

    Priority:
    1. Paragraph with the largest explicit font size in the first 7 lines
    2. First centred paragraph
    3. First non-empty, non-contact-info paragraph
    """
    limit = min(first_header_idx, 7) if first_header_idx > 0 else 7
    candidates = []

    for i, para in enumerate(doc.paragraphs[:limit]):
        text = _text(para)
        if not text or _CONTACT_PATTERN.search(text):
            continue
        # Skip pipe-delimited contact bars  (e.g. "Seattle, WA | 555-1234 | …")
        if text.count('|') >= 2:
            continue

        sz = _get_font_size_pt(para)
        is_centered = '<w:jc w:val="center"' in para._p.xml

        candidates.append({"text": text, "sz": sz or 0.0, "centered": is_centered})

    if not candidates:
        return "Unknown"

    max_sz = max(c["sz"] for c in candidates)
    if max_sz > 0:
        large = [c for c in candidates if c["sz"] == max_sz]
        return large[0]["text"]

    centered = [c for c in candidates if c["centered"]]
    if centered:
        return centered[0]["text"]

    return candidates[0]["text"]


# ---------------------------------------------------------------------------
# Section content extraction
# ---------------------------------------------------------------------------

def _extract_bullets(paras) -> list[str]:
    """Return text of all bulleted/numbered paragraphs."""
    return [_text(p) for p in paras if _has_numbering(p) and _text(p)]


def _extract_skills_text(paras) -> str:
    """Concatenate non-empty paragraph text from a skills section."""
    parts = [_text(p) for p in paras if _text(p)]
    return " | ".join(parts) if parts else ""


def _detect_jobs(paras) -> list[dict]:
    """
    Detect job entries within an Experience section.

    Primary strategy (used when any tab+non-bullet lines are found):
      Resumes commonly use TWO consecutive tab-delimited lines per role:
        Line 1 — Company[TAB]Location      (bold company name)
        Line 2 — Job Title[TAB]Dates       (title, possibly underlined)
      The parser pairs these: the FIRST tab line opens a new job entry;
      the SECOND consecutive tab line (while awaiting a title) sets the title.
      Bold non-bullet lines with no tab are treated as secondary-role entries
      within the same company block (e.g. a role change mid-contract).

    Fallback (no tab lines): bold non-bullet paragraphs under ~80 chars are
    used as job separators (handles simpler single-line-per-role templates).
    """
    jobs: list[dict] = []
    current: Optional[dict] = None
    bullet_count = 0
    awaiting_title = False   # True after a company line, before the title line

    has_tab_pattern = any(
        _has_tab(p) and not _has_numbering(p) and _text(p)
        for p in paras
    )

    def _flush():
        nonlocal current, bullet_count, awaiting_title
        if current is not None:
            current["bullet_count"] = bullet_count
            jobs.append(current)
        current = None
        bullet_count = 0
        awaiting_title = False

    for para in paras:
        text = _text(para)
        if not text:
            continue

        is_bullet = _has_numbering(para)
        has_tab   = _has_tab(para)

        if has_tab_pattern:
            if has_tab and not is_bullet:
                if awaiting_title and current is not None:
                    # Second tab line = Title[TAB]Dates for the current company.
                    # Do NOT flush — this belongs to the entry we just opened.
                    parts = text.split('\t', 1)
                    current["title"] = parts[0].strip()
                    current["dates"] = parts[1].strip() if len(parts) > 1 else ""
                    awaiting_title = False
                else:
                    # First tab line = new Company[TAB]Location entry.
                    _flush()
                    parts = text.split('\t', 1)
                    current = {
                        "company":      parts[0].strip(),
                        "location":     parts[1].strip() if len(parts) > 1 else "",
                        "title":        "",
                        "dates":        "",
                        "bullet_count": 0,
                        "bullet_texts": [],
                    }
                    awaiting_title = True

            elif not has_tab and not is_bullet and _any_bold(para) and len(text) < 100:
                # Bold non-tab non-bullet line: secondary role at the same company
                # (e.g. "Lithography Process Engineer: Sep 2022 – Feb 2024").
                # Flush the current role and open a new entry using this line as the name.
                _flush()
                current = {
                    "company":      text,
                    "location":     "",
                    "title":        "",
                    "dates":        "",
                    "bullet_count": 0,
                    "bullet_texts": [],
                }
                awaiting_title = False

            elif is_bullet:
                bullet_count += 1
                if current is not None:
                    current["bullet_texts"].append(text)
                awaiting_title = False   # bullets started; title line window closed

        else:
            # Fallback: bold, non-bullet, short line = job separator
            if _any_bold(para) and not is_bullet and len(text) < 80:
                _flush()
                current = {
                    "company":      text,
                    "location":     "",
                    "title":        "",
                    "dates":        "",
                    "bullet_count": 0,
                    "bullet_texts": [],
                }
            elif current and is_bullet:
                bullet_count += 1
                current["bullet_texts"].append(text)

    _flush()
    return jobs


# ---------------------------------------------------------------------------
# Main parse function
# ---------------------------------------------------------------------------

def parse_resume(path: str) -> dict:
    """
    Parse a .docx resume and return structured section data.

    Returns a dict with keys:
      name, source_file, baseline_font_pt, sections, warnings

    Each section dict contains:
      header, type, detection, style_name, paragraph_count, bullet_count
      _signal_score, _signals   (prefixed _ = diagnostic, stripped from --json)
      + type-specific keys: jobs (EXPERIENCE), skills_text (SKILLS/EXPERTISE),
        accomplishments (ACCOMPLISHMENTS), count (PUBLICATIONS/PRESENTATIONS)
    """
    doc = Document(path)
    baseline_pt = _detect_baseline_font_size(doc)
    page_count  = _detect_page_count(path)
    paragraphs  = doc.paragraphs
    warnings: list[str] = []

    # ------------------------------------------------------------------
    # Pass 1 — identify all section headers
    # ------------------------------------------------------------------
    header_records: list[tuple[int, object, str, dict]] = []
    # (paragraph_index, para, layer_label, signals)

    for i, para in enumerate(paragraphs):
        text = _text(para)
        if not text:
            continue

        signals = _compute_signals(para, baseline_pt)

        if _layer1_is_heading(para):
            header_records.append((i, para, "layer1_style", signals))
        elif _layer2_is_heading(signals):
            header_records.append((i, para, "layer2_heuristic", signals))

    # ------------------------------------------------------------------
    # Pass 2 — detect name (paragraphs before first header)
    # ------------------------------------------------------------------
    first_header_idx = header_records[0][0] if header_records else len(paragraphs)
    name         = detect_name(doc, first_header_idx)
    contact_info = detect_contact_info(doc, first_header_idx)

    # ------------------------------------------------------------------
    # Pass 3 — slice content per section and extract structured data
    # ------------------------------------------------------------------
    sections = []

    for j, (idx, para, layer, signals) in enumerate(header_records):
        header_text = _text(para)
        sec_type    = _classify_text(header_text) or "UNKNOWN"
        style_name  = para.style.name

        next_idx      = header_records[j + 1][0] if j + 1 < len(header_records) else len(paragraphs)
        section_paras = paragraphs[idx + 1 : next_idx]

        content_paras = [p for p in section_paras if _text(p)]
        bullet_paras  = [p for p in section_paras if _has_numbering(p) and _text(p)]

        entry: dict = {
            "header":          header_text,
            "type":            sec_type,
            "detection":       layer,
            "style_name":      style_name,
            "paragraph_count": len(content_paras),
            "bullet_count":    len(bullet_paras),
            "_signal_score":   _signal_score(signals),
            "_signals":        {k: v for k, v in signals.items()},
        }

        # Type-specific extraction
        if sec_type == "SUMMARY":
            entry["summary_text"] = " ".join(_text(p) for p in content_paras)
        elif sec_type == "EXPERIENCE":
            entry["jobs"] = _detect_jobs(section_paras)
        elif sec_type in ("SKILLS", "EXPERTISE"):
            entry["skills_text"] = _extract_skills_text(content_paras)
            entry["skills_lines"] = [_text(p) for p in content_paras if _text(p)]
        elif sec_type == "ACCOMPLISHMENTS":
            # Accomplishments can use mixed styles (ListBullet, normal+bold+tab,
            # etc.). Capture ALL content paragraphs — not just list items — so
            # formats like Ted's resume (2× normal+BT, 1× ListBullet) are handled.
            entry["accomplishments"] = [_text(p) for p in content_paras]
            entry["bullet_count"] = len(content_paras)
        elif sec_type == "EDUCATION":
            entry["content_lines"] = [_text(p) for p in content_paras if _text(p)]
        elif sec_type in ("PUBLICATIONS", "PRESENTATIONS"):
            entry["count"] = len(content_paras)
            entry["content_lines"] = [_text(p) for p in content_paras if _text(p)]

        sections.append(entry)

    if not sections:
        warnings.append(
            "No section headers detected. The resume may use unusual formatting. "
            "Run with --verbose to inspect paragraph-level signal scores."
        )

    return {
        "name":                name,
        "contact_info":        contact_info,
        "source_file":         str(Path(path).name),
        "baseline_font_pt":    baseline_pt,
        "detected_page_count": page_count,
        "sections":            sections,
        "warnings":            warnings,
    }


# ---------------------------------------------------------------------------
# Human-readable output
# ---------------------------------------------------------------------------

def _out(s: str = "") -> None:
    sys.stdout.buffer.write((s + "\n").encode("utf-8", errors="replace"))


def _print_human(result: dict, verbose: bool = False) -> None:
    pc = result.get("detected_page_count")
    pc_str = f"{pc} page{'s' if pc != 1 else ''}" if pc else "unknown (save in Word to embed)"
    _out()
    _out("=== Resume Parse Results " + "=" * 40)
    _out(f"  File            : {result['source_file']}")
    _out(f"  Name            : {result['name']}")
    _out(f"  Page count      : {pc_str}")
    _out(f"  Body font size  : {result['baseline_font_pt']}pt")
    _out(f"  Sections found  : {len(result['sections'])}")
    _out()

    if not result["sections"]:
        _out("  ⚠  No sections detected.")
    else:
        for sec in result["sections"]:
            layer_tag = (
                "[L1-style]"
                if sec["detection"] == "layer1_style"
                else f"[L2-score:{sec['_signal_score']}]"
            )
            _out("  " + "─" * 62)
            _out(f"  Header   : \"{sec['header']}\"")
            _out(f"  Type     : {sec['type']}  {layer_tag}  (style: {sec['style_name']})")
            _out(f"  Content  : {sec['paragraph_count']} paragraphs, "
                 f"{sec['bullet_count']} bullets")

            if verbose:
                sigs     = sec["_signals"]
                fired    = [f"{k}(+{_SIGNAL_POINTS[k]})" for k, v in sigs.items() if v]
                notfired = [k for k, v in sigs.items() if not v]
                _out(f"  Signals  : ✓ {', '.join(fired) if fired else 'none'}")
                if notfired:
                    _out(f"           : ✗ {', '.join(notfired)}")

            if "jobs" in sec:
                _out(f"  Jobs ({len(sec['jobs'])}):")
                for job in sec["jobs"]:
                    loc   = f" — {job['location']}" if job["location"] else ""
                    title = f"\n              title: {job['title']}" if job["title"] else ""
                    _out(f"    • {job['company']}{loc}  [{job['bullet_count']} bullets]{title}")

            if "skills_text" in sec and sec["skills_text"]:
                preview = sec["skills_text"][:120]
                suffix  = "..." if len(sec["skills_text"]) > 120 else ""
                _out(f"  Skills   : {preview}{suffix}")

            if "accomplishments" in sec:
                _out(f"  Accomplishments ({len(sec['accomplishments'])}):")
                for acc in sec["accomplishments"]:
                    _out(f"    • {acc[:100]}{'...' if len(acc) > 100 else ''}")

            if sec["type"] in ("PUBLICATIONS", "PRESENTATIONS") and "count" in sec:
                _out(f"  Entries  : {sec['count']}")

        _out("  " + "─" * 62)

    _out()
    if result["warnings"]:
        for w in result["warnings"]:
            _out(f"  ⚠  {w}")
        _out()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Parse a .docx resume and detect section structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("resume",        help="Path to .docx resume file")
    ap.add_argument("--json",        action="store_true", help="Output JSON")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="Show per-section signal breakdown")
    args = ap.parse_args()

    path = args.resume
    if not Path(path).exists():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    if not path.lower().endswith(".docx"):
        print(f"ERROR: Expected a .docx file, got: {path}", file=sys.stderr)
        sys.exit(1)

    result = parse_resume(path)

    if args.json:
        # Strip internal diagnostic keys from JSON output
        clean_sections = []
        for sec in result["sections"]:
            clean_sections.append({k: v for k, v in sec.items() if not k.startswith("_")})
        print(json.dumps({**result, "sections": clean_sections}, indent=2))
    else:
        _print_human(result, verbose=args.verbose)


if __name__ == "__main__":
    main()

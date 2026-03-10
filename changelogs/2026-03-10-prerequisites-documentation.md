# Changelog: Prerequisites & Portability Documentation

**Date:** 2026-03-10
**Trigger:** External user cloned the repo on a Windows machine and had to make several undocumented fixes to get the job-application-helper skill working.

## Context

A user cloned the repo and encountered the following issues:
1. Scripts couldn't find `pack.py`/`unpack.py` (only searched Claude.ai sandbox and Claude Code marketplace paths)
2. LibreOffice and pdfinfo were required but not documented
3. `defusedxml` Python package dependency was not documented
4. The baseline resume filename is hardcoded in scripts but the personalization guide didn't mention updating them
5. Python's stdlib `xml.etree.ElementTree` corrupts .docx XML when used for writing (strips namespaces, changes encoding)

## Analysis of User's Fixes

| Fix from User | Adopted? | Rationale |
|---|---|---|
| Added `${SCRIPT_DIR}/` as first search path for pack/unpack | **Yes** | Legitimate portability fix — scripts now check locally first |
| Created local `scripts/unpack.py` and `scripts/pack.py` | **No** | These depend on `defusedxml` and are maintained by Anthropic's docx example skill; better to document the dependency than bundle copies |
| Added `lxml` warning to Common Pitfalls | **Yes** | Stdlib `ET.write()` corrupts .docx XML; documented as pitfall #7 |
| Changed hardcoded baseline filename | **No** (code change) / **Yes** (documentation) | This is a personalization step; added scripts to personalization checklist instead |

## Changes Made

### Scripts (code fix — local fallback for pack/unpack)

**`job-application-helper/scripts/prepare_resume.sh`**
- Added `${SCRIPT_DIR}/unpack.py` as first search path (before Claude.ai and Claude Code marketplace paths)
- Added `${SCRIPT_DIR}/pack.py` as first search path
- Improved error messages to list all searched locations with labels and suggest remediation

**`job-application-helper/scripts/create_tailored_resume.sh`**
- Added `${SCRIPT_DIR}/pack.py` as first search path
- Added remediation hint to error message

### Documentation (prerequisites & personalization)

**`README.md`**
- Expanded Prerequisites section with:
  - Anthropic `docx` example skill (with instructions for Claude.ai vs. Claude Code CLI)
  - `defusedxml` Python package
  - LibreOffice (with install commands for Linux, macOS, Windows)
  - `pdfinfo` / poppler-utils
- Added `scripts/prepare_resume.sh` to personalization checklist (for renamed resume files)

**`docs/job-application-helper.md`**
- Replaced vague Dependencies section with detailed subsections:
  - **System Tools** table: LibreOffice, pdfinfo with package names and install commands
  - **Python Dependencies** table: defusedxml
  - **Claude Code Dependencies** table: docx example skill, web search, file system
  - Note documenting the pack/unpack search order
- Added script to Quick Start personalization checklist

**`job-application-helper/SKILL.md`**
- Updated pack_script_path documentation to reflect new search order (local first)

### Reference (pitfall warning)

**`job-application-helper/references/xml_editing_guide.md`**
- Added Common Pitfall #7: Warning against using stdlib `xml.etree.ElementTree` for writing .docx XML
  - Root cause: `ET.write()` changes encoding declaration and strips namespace prefixes (`w:`, `r:`)
  - Recommendation: Use `defusedxml.minidom` or `lxml` instead

## Files Changed

| File | Type | Summary |
|------|------|---------|
| `job-application-helper/scripts/prepare_resume.sh` | Code | Local fallback + better errors |
| `job-application-helper/scripts/create_tailored_resume.sh` | Code | Local fallback + better errors |
| `README.md` | Docs | Prerequisites, personalization checklist |
| `docs/job-application-helper.md` | Docs | Dependencies section, personalization checklist |
| `job-application-helper/SKILL.md` | Docs | Pack script search order |
| `job-application-helper/references/xml_editing_guide.md` | Ref | ET.write() pitfall warning |

> **Note:** The `.claude/skills/` copies were also updated to stay in sync but are not tracked by git.

#!/usr/bin/env bash
set -eu
# pipefail is bash-specific and not available in all POSIX shells (e.g. dash).
# Test in a subshell before enabling so the script works in any environment.
if (set -o pipefail) 2>/dev/null; then set -o pipefail; fi

# setup_baseline.sh — Calibrate char count targets for a new baseline resume
#
# When you add your baseline resume (via onboard.py or manually), run this
# script to calculate same-page char count targets and update the reference
# documentation automatically.
#
# Usage:
#   bash scripts/setup_baseline.sh [OPTIONS]
#
# Options:
#   --baseline <path>     Path to baseline .docx (default: from config.sh, or
#                         assets/Ted_Cohen-RESUME.docx for legacy users)
#   --target-pages N      Target page count for tailored resumes (default: from
#                         config.sh TARGET_PAGES, or auto-detected from baseline)
#   --no-verify           Skip LibreOffice page count check
#   --dry-run             Print computed values without modifying any files
#   --help                Show this help message
#
# What it does:
#   1. Unpacks the baseline resume to a temp directory
#   2. Counts total characters with para_utils.py
#   3. Checks baseline page count with LibreOffice (unless --no-verify)
#   4. Computes calibrated same-page char count ranges from empirical ratios
#   5. Updates references/xml_editing_guide.md and references/qa_and_delivery.md
#      with the new values
#   6. Cleans up temp files
#
# After running:
#   - Review the diff with: git diff references/
#   - Produce one tailored resume and confirm the char count falls in
#     the target range when it looks correct in Word
#   - Commit the updated reference files

# ---------------------------------------------------------------------------
# Empirical calibration ratios for same-page targeting.
# These describe how much the content can shrink relative to the baseline while
# staying on the same number of pages (e.g., baseline is 2 pages → output is 2 pages).
#
#   RATIO_CEILING    — absolute max (above this risks adding a page)
#   RATIO_FLOOR      — minimum viable content density
#   RATIO_TARGET_MAX — recommended upper bound (sweet spot)
#   RATIO_TARGET_MIN — recommended lower bound (sweet spot)
# ---------------------------------------------------------------------------
RATIO_CEILING=0.985
RATIO_FLOOR=0.870
RATIO_TARGET_MAX=0.970
RATIO_TARGET_MIN=0.920

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
BASELINE=""
TARGET_PAGES=""
VERIFY=true
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --baseline)     BASELINE="$2"; shift 2 ;;
        --target-pages) TARGET_PAGES="$2"; shift 2 ;;
        --no-verify)    VERIFY=false; shift ;;
        --dry-run)      DRY_RUN=true; shift ;;
        --help)
            sed -n '/^# setup_baseline/,/^[^#]/p' "$0" | grep '^#' | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

# ---------------------------------------------------------------------------
# Locate skill root and scripts; source config.sh for defaults
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "${SCRIPT_DIR}")"

CONFIG_FILE="${SKILL_DIR}/config.sh"
if [[ -f "${CONFIG_FILE}" ]]; then
    # shellcheck source=/dev/null
    source "${CONFIG_FILE}"
fi

# Apply defaults after config sourcing
if [[ -z "${BASELINE}" ]]; then
    if [[ -n "${RESUME_BASENAME:-}" ]]; then
        BASELINE="${SKILL_DIR}/assets/${RESUME_BASENAME}"
    else
        BASELINE="${SKILL_DIR}/assets/Ted_Cohen-RESUME.docx"
    fi
fi

if [[ ! -f "${BASELINE}" ]]; then
    echo "ERROR: Baseline resume not found: ${BASELINE}" >&2
    echo "Run:  python scripts/onboard.py --resume /path/to/resume.docx" >&2
    echo "  or: bash scripts/setup_baseline.sh --baseline /path/to/resume.docx" >&2
    exit 1
fi

XML_GUIDE="${SKILL_DIR}/references/xml_editing_guide.md"
QA_GUIDE="${SKILL_DIR}/references/qa_and_delivery.md"

for f in "${XML_GUIDE}" "${QA_GUIDE}"; do
    if [[ ! -f "${f}" ]]; then
        echo "ERROR: Reference file not found: ${f}" >&2
        exit 1
    fi
done

# ---------------------------------------------------------------------------
# Find Python
# ---------------------------------------------------------------------------
PYTHON=""
for candidate in python3 python; do
    if command -v "${candidate}" >/dev/null 2>&1 && "${candidate}" -c "import sys; sys.exit(0)" 2>/dev/null; then
        PYTHON="${candidate}"
        break
    fi
done
if [[ -z "${PYTHON}" ]]; then
    echo "ERROR: No working Python interpreter found in PATH" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Step 1: Unpack baseline to temp directory and count chars
# ---------------------------------------------------------------------------
TMPDIR_UNPACK="$(mktemp -d)"
trap 'rm -rf "${TMPDIR_UNPACK}"' EXIT

echo ""
echo "=== Baseline Resume Setup ==="
echo "Baseline: ${BASELINE}"
echo ""
echo "Step 1: Measuring baseline char count..."

"${PYTHON}" "${SCRIPT_DIR}/unpack.py" "${BASELINE}" "${TMPDIR_UNPACK}" >/dev/null 2>&1

BASELINE_CHARS=$(
    "${PYTHON}" "${SCRIPT_DIR}/para_utils.py" chars "${TMPDIR_UNPACK}/word/document.xml" \
    | grep "^Total chars" | awk '{print $NF}'
)

if [[ -z "${BASELINE_CHARS}" || ! "${BASELINE_CHARS}" =~ ^[0-9]+$ ]]; then
    echo "ERROR: Could not read char count from baseline resume." >&2
    exit 1
fi

echo "  Baseline char count: ${BASELINE_CHARS}"

# ---------------------------------------------------------------------------
# Step 2: Check baseline page count (optional)
# ---------------------------------------------------------------------------
BASELINE_PAGES="unknown"

if [[ "${VERIFY}" == true ]]; then
    echo ""
    echo "Step 2: Checking baseline page count with LibreOffice..."

    # Pass a sentinel (99) so verify_page_count.sh always prints "Pages: N" before
    # exiting non-zero; the || true prevents set -e from aborting.
    VERIFY_OUT=$("${SCRIPT_DIR}/verify_page_count.sh" "${BASELINE}" 99 2>&1 || true)
    PAGES_LINE=$(echo "${VERIFY_OUT}" | grep "^Pages:" | head -1)
    BASELINE_PAGES=$(echo "${PAGES_LINE}" | awk '{print $2}')

    if [[ -z "${BASELINE_PAGES}" || ! "${BASELINE_PAGES}" =~ ^[0-9]+$ ]]; then
        echo "  WARNING: Could not determine page count (LibreOffice or pdfinfo may not be installed)."
        echo "           Skipping page count verification. Use --no-verify to suppress this warning."
        BASELINE_PAGES="unknown"
    else
        echo "  Baseline page count: ${BASELINE_PAGES} page(s)"
    fi
else
    echo ""
    echo "Step 2: Skipping LibreOffice page count check (--no-verify)."
fi

# ---------------------------------------------------------------------------
# Determine TARGET_PAGES
# ---------------------------------------------------------------------------
# Priority: --target-pages flag > config.sh TARGET_PAGES > detected BASELINE_PAGES > 2
if [[ -z "${TARGET_PAGES}" ]]; then
    if [[ "${BASELINE_PAGES}" =~ ^[0-9]+$ ]]; then
        TARGET_PAGES="${BASELINE_PAGES}"
    else
        TARGET_PAGES="${TARGET_PAGES_CONFIG:-2}"
    fi
fi

# When page count is unknown (--no-verify), use TARGET_PAGES as the best estimate
# so reference-file comments say "3 pages" instead of "baseline"
if [[ "${BASELINE_PAGES}" == "unknown" && -n "${TARGET_PAGES}" ]]; then
    BASELINE_PAGES="${TARGET_PAGES}"
fi

echo "  Target page count: ${TARGET_PAGES} page(s) (tailored resumes will target this)"

# ---------------------------------------------------------------------------
# Step 3: Compute calibrated char count ranges
# ---------------------------------------------------------------------------
echo ""
echo "Step 3: Computing calibrated char count ranges..."

compute_range() {
    # Args: base_chars ratio  →  prints integer (rounds to nearest 10)
    local base=$1
    local ratio=$2
    "${PYTHON}" -c "print(round(${base} * ${ratio} / 10) * 10)"
}

NEW_CEILING=$(compute_range "${BASELINE_CHARS}" "${RATIO_CEILING}")
NEW_FLOOR=$(compute_range "${BASELINE_CHARS}" "${RATIO_FLOOR}")
NEW_TARGET_MAX=$(compute_range "${BASELINE_CHARS}" "${RATIO_TARGET_MAX}")
NEW_TARGET_MIN=$(compute_range "${BASELINE_CHARS}" "${RATIO_TARGET_MIN}")
# Hard ceiling for the inline code comment (ceiling - ~30, rounded to 10)
NEW_HARD_CEILING=$(compute_range "${BASELINE_CHARS}" "$(echo "${RATIO_CEILING} - 0.004" | "${PYTHON}" -c "import sys; print(eval(sys.stdin.read()))")")

echo ""
echo "  Baseline chars:  ${BASELINE_CHARS}"
echo "  Floor:           ${NEW_FLOOR}   (too sparse below this)"
echo "  Ceiling:         ${NEW_CEILING} (risk of overflow above this)"
echo "  Target range:    ${NEW_TARGET_MIN}–${NEW_TARGET_MAX} (recommended sweet spot)"
echo ""

# ---------------------------------------------------------------------------
# Step 4: Update reference files
# ---------------------------------------------------------------------------
if [[ "${DRY_RUN}" == true ]]; then
    echo "Step 4: DRY RUN — files not modified. Values that would be written:"
    echo "  xml_editing_guide.md:"
    echo "    Verified ${TARGET_PAGES}-page char range: ${NEW_FLOOR}–${NEW_CEILING} chars"
    echo "    Baseline = ${BASELINE_CHARS} chars (${BASELINE_PAGES} pages). Target: ≤${NEW_HARD_CEILING} chars for ${TARGET_PAGES} pages."
    echo "  qa_and_delivery.md:"
    echo "    Target char range: ${NEW_TARGET_MIN}–${NEW_TARGET_MAX} chars"
    echo "    Range bottom reference: ${NEW_FLOOR}–$(( NEW_FLOOR + 130 ))"
    echo ""
    echo "Run without --dry-run to apply these changes."
    exit 0
fi

echo "Step 4: Updating reference files..."

# Pass all values as argv to avoid Windows bash-path expansion issues inside heredocs
"${PYTHON}" - "${XML_GUIDE}" "${QA_GUIDE}" "${TARGET_PAGES}" "${BASELINE_PAGES}" <<PYEOF
import re, sys

xml_guide_path  = sys.argv[1]
qa_guide_path   = sys.argv[2]
target_pages    = sys.argv[3]          # e.g. "2"
baseline_pages  = sys.argv[4]          # e.g. "3" or "unknown"

baseline = ${BASELINE_CHARS}
ceiling  = ${NEW_CEILING}
floor    = ${NEW_FLOOR}
t_min    = ${NEW_TARGET_MIN}
t_max    = ${NEW_TARGET_MAX}
hard_c   = ${NEW_HARD_CEILING}
low_sig  = floor + 130   # "near the bottom" signal threshold

page_label = f"{target_pages}-page"
base_label = (f"{baseline_pages} pages" if baseline_pages.isdigit() else "baseline")

# ---- xml_editing_guide.md ----
with open(xml_guide_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Update "Verified N-page char range: NNNN–NNNN chars."
text = re.sub(
    r'\*\*Verified \d+-page char range: \d+–\d+ chars\.',
    f'**Verified {page_label} char range: {floor}–{ceiling} chars.',
    text
)

# Update inline comment "# Baseline = NNNN chars (N pages). Target: ≤NNNN chars for N pages."
text = re.sub(
    r'# Baseline = \d+ chars \([^)]+\)\. Target: ≤\d+ chars for \d+ pages?\.',
    f'# Baseline = {baseline} chars ({base_label}). Target: ≤{hard_c} chars for {target_pages} pages.',
    text
)

with open(xml_guide_path, 'w', encoding='utf-8') as f:
    f.write(text)
print("  Updated: references/xml_editing_guide.md")

# ---- qa_and_delivery.md ----
with open(qa_guide_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Update "**Target char range: NNNN–NNNN chars.**"
text = re.sub(
    r'\*\*Target char range: \d+–\d+ chars\.\*\*',
    f'**Target char range: {t_min}–{t_max} chars.**',
    text
)

# Update "A char count near the bottom of the range (NNNN–NNNN)"
text = re.sub(
    r'A char count near the bottom of the range \(\d+–\d+\)',
    f'A char count near the bottom of the range ({floor}–{low_sig})',
    text
)

# Update "Target **NNNN–NNNN chars** to use the page fully."
text = re.sub(
    r'Target \*\*\d+–\d+ chars\*\* to use the page fully\.',
    f'Target **{t_min}–{t_max} chars** to use the page fully.',
    text
)

# Update pre-delivery checklist char count line
text = re.sub(
    r'Total chars in target range \d+–\d+',
    f'Total chars in target range {t_min}–{t_max}',
    text
)

with open(qa_guide_path, 'w', encoding='utf-8') as f:
    f.write(text)
print("  Updated: references/qa_and_delivery.md")
PYEOF

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo "=== Setup complete ==="
echo ""
echo "New calibration values:"
echo "  Baseline chars:   ${BASELINE_CHARS}"
echo "  Target pages:     ${TARGET_PAGES}"
echo "  Char count range: ${NEW_FLOOR}–${NEW_CEILING} chars"
echo "  Sweet spot:       ${NEW_TARGET_MIN}–${NEW_TARGET_MAX} chars"
echo ""
echo "Next steps:"
echo "  1. Review changes:  git diff references/"
echo "  2. Produce one tailored resume and confirm it is exactly ${TARGET_PAGES} page(s) in Word"
echo "     with a char count in the target range (${NEW_TARGET_MIN}–${NEW_TARGET_MAX})."
echo "  3. If the page count in Word doesn't match, re-run with --target-pages to adjust."
echo "  4. Commit the updated reference files."

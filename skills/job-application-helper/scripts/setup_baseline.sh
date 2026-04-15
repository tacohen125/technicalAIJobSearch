#!/usr/bin/env bash
set -euo pipefail

# setup_baseline.sh — Calibrate char count targets for a new baseline resume
#
# When you replace assets/Ted_Cohen-RESUME.docx with a new baseline resume,
# run this script to recalculate the 2-page char count targets and update the
# reference documentation automatically.
#
# Usage:
#   bash scripts/setup_baseline.sh [OPTIONS]
#
# Options:
#   --baseline <path>   Path to baseline .docx (default: assets/Ted_Cohen-RESUME.docx)
#   --no-verify         Skip LibreOffice page count check (useful if LibreOffice not installed)
#   --dry-run           Print computed values without modifying any files
#   --help              Show this help message
#
# What it does:
#   1. Unpacks the baseline resume to a temp directory
#   2. Counts total characters with para_utils.py
#   3. Checks baseline page count with LibreOffice (unless --no-verify)
#   4. Computes calibrated 2-page char count ranges from empirical ratios
#   5. Updates references/xml_editing_guide.md and references/qa_and_delivery.md
#      with the new values
#   6. Cleans up temp files
#
# After running:
#   - Review the diff with: git diff references/
#   - Produce one tailored 2-page resume and confirm the char count falls in
#     the new target range when it looks correct in Word
#   - Commit the updated reference files

# ---------------------------------------------------------------------------
# Empirical calibration ratios derived from original baseline (7679 chars, 3 pages).
# These describe where a 2-page Word document falls relative to the 3-page baseline.
# Scaling these ratios to a new baseline gives a good first approximation.
#
#   RATIO_CEILING  = 7430 / 7679 = 0.9676   (absolute max before 3-page risk)
#   RATIO_FLOOR    = 6968 / 7679 = 0.9076   (too sparse below this)
#   RATIO_TARGET_MAX = 7350 / 7679 = 0.9571 (recommended upper target)
#   RATIO_TARGET_MIN = 7200 / 7679 = 0.9376 (recommended lower target)
# ---------------------------------------------------------------------------
RATIO_CEILING=0.9676
RATIO_FLOOR=0.9076
RATIO_TARGET_MAX=0.9571
RATIO_TARGET_MIN=0.9376

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------
BASELINE=""
VERIFY=true
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --baseline)   BASELINE="$2"; shift 2 ;;
        --no-verify)  VERIFY=false; shift ;;
        --dry-run)    DRY_RUN=true; shift ;;
        --help)
            sed -n '/^# setup_baseline/,/^[^#]/p' "$0" | grep '^#' | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

# ---------------------------------------------------------------------------
# Locate skill root and scripts
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "${SCRIPT_DIR}")"

if [[ -z "${BASELINE}" ]]; then
    BASELINE="${SKILL_DIR}/assets/Ted_Cohen-RESUME.docx"
fi

if [[ ! -f "${BASELINE}" ]]; then
    echo "ERROR: Baseline resume not found: ${BASELINE}" >&2
    echo "Place your baseline resume at assets/Ted_Cohen-RESUME.docx or pass --baseline <path>" >&2
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

    # Run verify_page_count.sh; capture output regardless of exit code
    VERIFY_OUT=$("${SCRIPT_DIR}/verify_page_count.sh" "${BASELINE}" 3 2>&1 || true)
    PAGES_LINE=$(echo "${VERIFY_OUT}" | grep "^Pages:" | head -1)
    BASELINE_PAGES=$(echo "${PAGES_LINE}" | awk '{print $2}')

    if [[ -z "${BASELINE_PAGES}" || ! "${BASELINE_PAGES}" =~ ^[0-9]+$ ]]; then
        echo "  WARNING: Could not determine page count (LibreOffice or pdfinfo may not be installed)."
        echo "           Skipping page count verification. Use --no-verify to suppress this warning."
        BASELINE_PAGES="unknown"
    else
        echo "  Baseline page count: ${BASELINE_PAGES}"
        if [[ "${BASELINE_PAGES}" -eq 3 ]]; then
            echo "  OK: Baseline is 3 pages as expected."
        elif [[ "${BASELINE_PAGES}" -eq 2 ]]; then
            echo "  NOTE: Baseline is already 2 pages. The calibration ratios assume a 3-page baseline."
            echo "        Computed ranges may be conservative. Manual tuning is recommended."
        elif [[ "${BASELINE_PAGES}" -gt 3 ]]; then
            echo "  NOTE: Baseline is ${BASELINE_PAGES} pages. Significant cuts will be needed."
        fi
    fi
else
    echo ""
    echo "Step 2: Skipping LibreOffice page count check (--no-verify)."
fi

# ---------------------------------------------------------------------------
# Step 3: Compute calibrated char count ranges
# ---------------------------------------------------------------------------
echo ""
echo "Step 3: Computing calibrated 2-page char count ranges..."

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
# Hard ceiling for the inline code comment (ceiling - 30, rounded to 10)
NEW_HARD_CEILING=$(compute_range "${BASELINE_CHARS}" "$(echo "${RATIO_CEILING} - 0.004" | "${PYTHON}" -c "import sys; print(eval(sys.stdin.read()))")")

echo ""
echo "  Baseline chars:      ${BASELINE_CHARS}"
echo "  2-page floor:        ${NEW_FLOOR}   (too sparse below this)"
echo "  2-page ceiling:      ${NEW_CEILING} (risk of 3 pages above this)"
echo "  Target range:        ${NEW_TARGET_MIN}–${NEW_TARGET_MAX} (recommended sweet spot)"
echo ""

# ---------------------------------------------------------------------------
# Step 4: Update reference files
# ---------------------------------------------------------------------------
if [[ "${DRY_RUN}" == true ]]; then
    echo "Step 4: DRY RUN — files not modified. Values that would be written:"
    echo "  xml_editing_guide.md:"
    echo "    Verified 2-page char range: ${NEW_FLOOR}–${NEW_CEILING} chars"
    echo "    Baseline = ${BASELINE_CHARS} chars (3 pages). Target: ≤${NEW_HARD_CEILING} chars for 2 pages."
    echo "  qa_and_delivery.md:"
    echo "    Target char range: ${NEW_TARGET_MIN}–${NEW_TARGET_MAX} chars"
    echo "    Range bottom reference: ${NEW_FLOOR}–$(( NEW_FLOOR + 130 ))"
    echo ""
    echo "Run without --dry-run to apply these changes."
    exit 0
fi

echo "Step 4: Updating reference files..."

# Pass paths as argv to avoid Windows bash-path expansion issues inside heredocs
"${PYTHON}" - "${XML_GUIDE}" "${QA_GUIDE}" <<PYEOF
import re, sys

# Paths passed as arguments so the shell handles quoting/expansion correctly
xml_guide_path = sys.argv[1]
qa_guide_path  = sys.argv[2]

baseline = ${BASELINE_CHARS}
ceiling  = ${NEW_CEILING}
floor    = ${NEW_FLOOR}
t_min    = ${NEW_TARGET_MIN}
t_max    = ${NEW_TARGET_MAX}
hard_c   = ${NEW_HARD_CEILING}
low_sig  = floor + 130   # "near the bottom" signal threshold

# ---- xml_editing_guide.md ----
with open(xml_guide_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Update "Verified 2-page char range: NNNN–NNNN chars."
text = re.sub(
    r'\*\*Verified 2-page char range: \d+–\d+ chars\.',
    f'**Verified 2-page char range: {floor}–{ceiling} chars.',
    text
)

# Update inline comment "# Baseline = NNNN chars (3 pages). Target: ≤NNNN chars for 2 pages."
text = re.sub(
    r'# Baseline = \d+ chars \(3 pages\)\. Target: ≤\d+ chars for 2 pages\.',
    f'# Baseline = {baseline} chars (3 pages). Target: ≤{hard_c} chars for 2 pages.',
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
echo "  Baseline chars:  ${BASELINE_CHARS}"
echo "  2-page range:    ${NEW_FLOOR}–${NEW_CEILING} chars"
echo "  Target sweet spot: ${NEW_TARGET_MIN}–${NEW_TARGET_MAX} chars"
echo ""
echo "Next steps:"
echo "  1. Review changes:  git diff references/"
echo "  2. Produce one tailored resume and confirm it is exactly 2 pages in Word"
echo "     with a char count in the target range (${NEW_TARGET_MIN}–${NEW_TARGET_MAX})."
echo "  3. If the page count in Word doesn't match, adjust the ratios by passing"
echo "     the char count of a known 2-page resume to re-derive the ceiling."
echo "  4. Commit the updated reference files."

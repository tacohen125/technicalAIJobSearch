#!/usr/bin/env bash
# test_page_count_rules.sh
# Validates that:
#   1. The baseline is 3 pages (verify correctly fails)
#   2. Long bullets (>110c) overflow to 3 pages (rule violation detected)
#   3. Short bullets (≤110c) + pub cuts produce 2 pages (rule compliance confirmed)
#   4. Delivered Applied Materials resume is 2 pages (regression check)
# Run from the skill root directory.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/scripts" && pwd)"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON=python

PASS=0
FAIL=0

pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

get_pages() {
    # Pass 99 as expected so verify always "fails" but still prints "Pages: N".
    # Suppress exit code so set -e doesn't kill the test script.
    local docx="$1"
    bash "${SCRIPT_DIR}/verify_page_count.sh" "$docx" 99 2>&1 | grep "^Pages:" | awk '{print $2}' || true
}

TMPDIR_TEST=$(mktemp -d)
trap 'rm -rf "$TMPDIR_TEST"' EXIT
cd "$SKILL_DIR"

# ── Test 1: Baseline is 3 pages ───────────────────────────────────────────
echo ""
echo "=== Test 1: Baseline is 3 pages ==="
pages=$(get_pages "assets/Ted_Cohen-RESUME.docx")
if [ "$pages" = "3" ]; then
    pass "Baseline correctly detected as 3 pages (verify always fails baseline)"
else
    fail "Expected baseline=3 pages, got: $pages"
fi

# ── Test 2: Long bullets cause overflow ───────────────────────────────────
echo ""
echo "=== Test 2: Long bullets (>130c) overflow to 3 pages ==="
LONG_OUT="${TMPDIR_TEST}/long_bullets.docx"
LONG_UNPACKED="${TMPDIR_TEST}/long_unpacked"
bash "${SCRIPT_DIR}/prepare_resume.sh" "$LONG_OUT" "$LONG_UNPACKED" >/dev/null 2>&1
echo "  Applying long bullets..."
$PYTHON tests/edit_long_bullets.py "${LONG_UNPACKED}/word/document.xml"
$PYTHON "${SCRIPT_DIR}/pack.py" "$LONG_UNPACKED" "$LONG_OUT" \
    --original "assets/Ted_Cohen-RESUME.docx" >/dev/null 2>&1
pages=$(get_pages "$LONG_OUT")
if [ "$pages" = "3" ]; then
    pass "Long bullets overflow to 3 pages (overflow detection confirmed)"
else
    fail "Expected 3 pages with long bullets, got: $pages"
fi

# ── Test 3: Short bullets + cuts = 2 pages ────────────────────────────────
echo ""
echo "=== Test 3: Short bullets (≤110c) + pub cuts produce 2 pages ==="
SHORT_OUT="${TMPDIR_TEST}/short_bullets.docx"
SHORT_UNPACKED="${TMPDIR_TEST}/short_unpacked"
bash "${SCRIPT_DIR}/prepare_resume.sh" "$SHORT_OUT" "$SHORT_UNPACKED" >/dev/null 2>&1
echo "  Applying short bullets + cuts..."
$PYTHON tests/edit_short_bullets.py "${SHORT_UNPACKED}/word/document.xml"
$PYTHON "${SCRIPT_DIR}/pack.py" "$SHORT_UNPACKED" "$SHORT_OUT" \
    --original "assets/Ted_Cohen-RESUME.docx" >/dev/null 2>&1
pages=$(get_pages "$SHORT_OUT")
if [ "$pages" = "2" ]; then
    pass "Short bullets + pub cuts produce 2 pages (rule compliance confirmed)"
else
    fail "Expected 2 pages with short bullets, got: $pages"
fi

# ── Test 4: Delivered Applied Materials resume ────────────────────────────
echo ""
echo "=== Test 4: Delivered Applied Materials resume is 2 pages ==="
AMAT_DOCX="assets/outputs/260413-AppliedMaterials-PhotonicsTestEngineer/Ted_Cohen-RESUME-AppliedMaterials-PhotonicsTestEngineer.docx"
if [ -f "$AMAT_DOCX" ]; then
    pages=$(get_pages "$AMAT_DOCX")
    if [ "$pages" = "2" ]; then
        pass "Applied Materials resume is exactly 2 pages (regression check)"
    else
        fail "Applied Materials resume is $pages pages (expected 2)"
    fi
else
    fail "Applied Materials resume not found: $AMAT_DOCX"
fi

# ── Summary ───────────────────────────────────────────────────────────────
echo ""
echo "========================================="
echo "Results: $PASS passed, $FAIL failed"
echo "========================================="
[ $FAIL -eq 0 ]

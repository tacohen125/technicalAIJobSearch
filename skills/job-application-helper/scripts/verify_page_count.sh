#!/usr/bin/env bash
set -euo pipefail

# Converts a .docx to PDF and verifies the page count is exactly 2.
#
# Usage: verify_page_count.sh <resume.docx> [expected_pages]
#   resume.docx     - The .docx file to verify
#   expected_pages  - Expected page count (default: 2)
#
# Exit codes: 0 = page count matches, 1 = mismatch or error

for cmd in libreoffice pdfinfo; do
    command -v "$cmd" >/dev/null 2>&1 || { echo "ERROR: $cmd is required but not installed." >&2; exit 1; }
done

if [ $# -lt 1 ]; then
    echo "Usage: verify_page_count.sh <resume.docx> [expected_pages]" >&2
    exit 1
fi

DOCX_FILE="$1"

if [ ! -f "${DOCX_FILE}" ]; then
    echo "ERROR: File not found: ${DOCX_FILE}" >&2
    exit 1
fi
EXPECTED="${2:-2}"

if ! [[ "${EXPECTED}" =~ ^[1-9][0-9]*$ ]]; then
    echo "ERROR: Expected page count must be a positive integer, got: '${EXPECTED}'" >&2
    exit 1
fi
TMPDIR=$(mktemp -d)

trap 'rm -rf "${TMPDIR}"' EXIT

echo "Converting ${DOCX_FILE} to PDF..."
libreoffice --headless --convert-to pdf --outdir "${TMPDIR}" "${DOCX_FILE}" >/dev/null 2>&1

PDF_FILE="${TMPDIR}/$(basename "${DOCX_FILE}" .docx).pdf"

if [ ! -f "${PDF_FILE}" ]; then
    echo "FAIL: PDF conversion failed." >&2
    exit 1
fi

PAGES=$(pdfinfo "${PDF_FILE}" | grep -i "^Pages:" | awk '{print $2}')

echo "Pages: ${PAGES}"

if [ "${PAGES}" -eq "${EXPECTED}" ]; then
    echo "PASS: Resume is exactly ${EXPECTED} pages."
    exit 0
else
    echo "FAIL: Resume is ${PAGES} pages (expected ${EXPECTED})." >&2
    exit 1
fi

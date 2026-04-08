#!/usr/bin/env bash
set -euo pipefail

# Converts a .docx to PDF and verifies the page count is exactly 2.
#
# Usage: verify_page_count.sh <resume.docx> [expected_pages]
#   resume.docx     - The .docx file to verify
#   expected_pages  - Expected page count (default: 2)
#
# Exit codes: 0 = page count matches, 1 = mismatch or error

# --- Find LibreOffice ---
# On Windows, LibreOffice installs as soffice.exe, not libreoffice.
SOFFICE=""
for candidate in \
    libreoffice \
    soffice \
    "/c/Program Files/LibreOffice/program/soffice.exe" \
    "/c/Program Files (x86)/LibreOffice/program/soffice.exe"
do
    if command -v "$candidate" >/dev/null 2>&1; then
        SOFFICE="$candidate"
        break
    elif [ -f "$candidate" ]; then
        SOFFICE="$candidate"
        break
    fi
done

if [ -z "$SOFFICE" ]; then
    echo "ERROR: LibreOffice (soffice) not found. Install it or add its program/ directory to PATH." >&2
    exit 1
fi

# --- Find pdfinfo ---
# Winget installs Poppler into a versioned path that isn't added to PATH automatically.
PDFINFO=""
for candidate in \
    pdfinfo \
    "/c/Users/${USERNAME}/AppData/Local/Microsoft/WinGet/Packages/oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe/poppler-25.07.0/Library/bin/pdfinfo.exe"
do
    if command -v "$candidate" >/dev/null 2>&1; then
        PDFINFO="$candidate"
        break
    elif [ -f "$candidate" ]; then
        PDFINFO="$candidate"
        break
    fi
done

# Fallback: glob search in the WinGet Poppler directory for any version
if [ -z "$PDFINFO" ]; then
    for f in "/c/Users/${USERNAME}/AppData/Local/Microsoft/WinGet/Packages/oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe"/*/Library/bin/pdfinfo.exe; do
        if [ -f "$f" ]; then
            PDFINFO="$f"
            break
        fi
    done
fi

if [ -z "$PDFINFO" ]; then
    echo "ERROR: pdfinfo not found. Install Poppler or add its bin/ directory to PATH." >&2
    exit 1
fi

# --- Validate arguments ---
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

# LibreOffice fails on paths with spaces. Copy to a temp location with a simple name.
SAFE_DOCX="${TMPDIR}/resume.docx"
cp "${DOCX_FILE}" "${SAFE_DOCX}"

echo "Converting ${DOCX_FILE} to PDF..."
"${SOFFICE}" --headless --convert-to pdf --outdir "${TMPDIR}" "${SAFE_DOCX}" >/dev/null 2>&1

PDF_FILE="${TMPDIR}/resume.pdf"

if [ ! -f "${PDF_FILE}" ]; then
    echo "FAIL: PDF conversion failed." >&2
    exit 1
fi

PAGES=$("${PDFINFO}" "${PDF_FILE}" | grep -i "^Pages:" | awk '{print $2}')

echo "Pages: ${PAGES}"

if [ "${PAGES}" -eq "${EXPECTED}" ]; then
    echo "PASS: Resume is exactly ${EXPECTED} pages."
    exit 0
else
    echo "FAIL: Resume is ${PAGES} pages (expected ${EXPECTED})." >&2
    exit 1
fi

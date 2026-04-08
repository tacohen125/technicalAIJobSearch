#!/usr/bin/env bash
set -euo pipefail

# Copies the cover letter template and unpacks it to XML for editing.
#
# Usage: prepare_cover_letter.sh <output_filename.docx> [unpacked_dir]
#   output_filename  - Target .docx filename (e.g., Ted_Cohen-COVERLETTER-Google-PIE.docx)
#   unpacked_dir     - Directory to unpack XML into (default: unpacked_cl/)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "${SCRIPT_DIR}")"
TEMPLATE="${SKILL_DIR}/assets/Ted_Cohen-COVERLETTER.docx"

# Find Python executable
if command -v python3 >/dev/null 2>&1 && python3 -c "import sys; sys.exit(0)" 2>/dev/null; then
    PYTHON="python3"
elif command -v python >/dev/null 2>&1 && python -c "import sys; sys.exit(0)" 2>/dev/null; then
    PYTHON="python"
else
    echo "ERROR: No working Python interpreter found in PATH" >&2
    exit 1
fi

# Find unpack script
if [ -f "${SCRIPT_DIR}/unpack.py" ]; then
    UNPACK_SCRIPT="${SCRIPT_DIR}/unpack.py"
elif [ -f "/mnt/skills/public/docx/scripts/office/unpack.py" ]; then
    UNPACK_SCRIPT="/mnt/skills/public/docx/scripts/office/unpack.py"
elif [ -f "${HOME}/.claude/plugins/marketplaces/anthropic-agent-skills/skills/docx/ooxml/scripts/unpack.py" ]; then
    UNPACK_SCRIPT="${HOME}/.claude/plugins/marketplaces/anthropic-agent-skills/skills/docx/ooxml/scripts/unpack.py"
else
    echo "ERROR: Could not find unpack.py script" >&2
    exit 1
fi

if [ ! -f "${TEMPLATE}" ]; then
    echo "ERROR: Cover letter template not found at ${TEMPLATE}" >&2
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Usage: prepare_cover_letter.sh <output_filename.docx> [unpacked_dir]" >&2
    exit 1
fi

OUTPUT_FILE="$1"
UNPACKED_DIR="${2:-unpacked_cl/}"

echo "Copying cover letter template to ${OUTPUT_FILE}..."
cp "${TEMPLATE}" "${OUTPUT_FILE}"

echo "Unpacking to ${UNPACKED_DIR}..."
"${PYTHON}" "${UNPACK_SCRIPT}" "${OUTPUT_FILE}" "${UNPACKED_DIR}"

# Find pack script
if [ -f "${SCRIPT_DIR}/pack.py" ]; then
    PACK_SCRIPT="${SCRIPT_DIR}/pack.py"
elif [ -f "/mnt/skills/public/docx/scripts/office/pack.py" ]; then
    PACK_SCRIPT="/mnt/skills/public/docx/scripts/office/pack.py"
elif [ -f "${HOME}/.claude/plugins/marketplaces/anthropic-agent-skills/skills/docx/ooxml/scripts/pack.py" ]; then
    PACK_SCRIPT="${HOME}/.claude/plugins/marketplaces/anthropic-agent-skills/skills/docx/ooxml/scripts/pack.py"
else
    PACK_SCRIPT="pack.py"
fi

echo "Ready. Edit XML at ${UNPACKED_DIR}word/document.xml"
echo "Paragraphs to edit:"
echo "  P005 - RE: line (role and company)"
echo "  P007 - Date"
echo "  P009 - Salutation"
echo "  P011 - Opening paragraph"
echo "  P013 - Body paragraph 1 (UW + Meta lithography)"
echo "  P015 - Body paragraph 2 (Meta metrology)"
echo "  P017 - Body paragraph 3 (company knowledge)"
echo "  P019 - Closing paragraph"
echo "  P021-P026 - Sign-off and credentials (DO NOT EDIT)"
echo ""
echo "Then pack with:"
echo "  ${PYTHON} ${PACK_SCRIPT} ${UNPACKED_DIR} ${OUTPUT_FILE} --original ${TEMPLATE}"
echo ""
echo "Then verify page count (must be 1 page):"
echo "  bash ${SCRIPT_DIR}/verify_page_count.sh ${OUTPUT_FILE} 1"

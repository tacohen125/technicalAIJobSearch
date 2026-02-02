#!/usr/bin/env bash
set -euo pipefail

# Copies the baseline resume and unpacks it to XML for editing.
#
# Usage: prepare_resume.sh <output_filename.docx> [unpacked_dir]
#   output_filename  - Target .docx filename (e.g., Jason_Garcia_RESUME-Acme-TPM.docx)
#   unpacked_dir     - Directory to unpack XML into (default: unpacked/)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "${SCRIPT_DIR}")"
BASELINE="${SKILL_DIR}/assets/Jason_J_Garcia-RESUME.docx"
UNPACK_SCRIPT="/mnt/skills/public/docx/scripts/office/unpack.py"

if [ ! -f "${BASELINE}" ]; then
    echo "ERROR: Baseline resume not found at ${BASELINE}" >&2
    exit 1
fi

if [ ! -f "${UNPACK_SCRIPT}" ]; then
    echo "ERROR: Unpack script not found at ${UNPACK_SCRIPT}" >&2
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Usage: prepare_resume.sh <output_filename.docx> [unpacked_dir]" >&2
    exit 1
fi

OUTPUT_FILE="$1"
UNPACKED_DIR="${2:-unpacked/}"

echo "Copying baseline resume to ${OUTPUT_FILE}..."
cp "${BASELINE}" "${OUTPUT_FILE}"

echo "Unpacking ${OUTPUT_FILE} to ${UNPACKED_DIR}..."
python3 "${UNPACK_SCRIPT}" "${OUTPUT_FILE}" "${UNPACKED_DIR}"

echo "Ready. Edit XML at ${UNPACKED_DIR}word/document.xml, then pack with:"
PACK_SCRIPT="/mnt/skills/public/docx/scripts/office/pack.py"
echo "  python3 ${PACK_SCRIPT} ${UNPACKED_DIR} ${OUTPUT_FILE} --original ${BASELINE}"

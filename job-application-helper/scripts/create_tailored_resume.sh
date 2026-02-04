#!/usr/bin/env bash
set -euo pipefail

# Orchestrates resume creation workflow with automatic cleanup
# Usage: create_tailored_resume.sh <output_file.docx> [--keep-unpacked] [--unpacked-dir <dir>] [--no-verify]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "${SCRIPT_DIR}")"

# Parse arguments
OUTPUT_FILE=""
KEEP_UNPACKED=0
UNPACKED_DIR=""
NO_VERIFY=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --keep-unpacked)
            KEEP_UNPACKED=1
            shift
            ;;
        --unpacked-dir)
            UNPACKED_DIR="$2"
            shift 2
            ;;
        --no-verify)
            NO_VERIFY=1
            shift
            ;;
        *)
            if [ -z "$OUTPUT_FILE" ]; then
                OUTPUT_FILE="$1"
            else
                echo "ERROR: Unknown argument: $1" >&2
                exit 1
            fi
            shift
            ;;
    esac
done

if [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: create_tailored_resume.sh <output_file.docx> [--keep-unpacked] [--unpacked-dir <dir>] [--no-verify]" >&2
    exit 1
fi

# Set default unpacked directory if not specified
if [ -z "$UNPACKED_DIR" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    UNPACKED_DIR="unpacked_${TIMESTAMP}"
fi

SUCCESS=0

# Cleanup handler
cleanup() {
    local exit_code=$?

    if [ $KEEP_UNPACKED -eq 1 ]; then
        echo "Keeping unpacked directory: ${UNPACKED_DIR}"
        return
    fi

    if [ $SUCCESS -eq 1 ] && [ -d "${SKILL_DIR}/${UNPACKED_DIR}" ]; then
        echo "Cleaning up ${UNPACKED_DIR}..."
        rm -rf "${SKILL_DIR}/${UNPACKED_DIR}"
        echo "Cleanup complete"
    elif [ $exit_code -ne 0 ] && [ -d "${SKILL_DIR}/${UNPACKED_DIR}" ]; then
        echo "Workflow failed. Keeping ${UNPACKED_DIR} for debugging." >&2
    fi
}

trap cleanup EXIT

# Step 1: Prepare resume
echo "=== Step 1: Preparing resume ==="
cd "${SKILL_DIR}"
bash "${SCRIPT_DIR}/prepare_resume.sh" "${OUTPUT_FILE}" "${UNPACKED_DIR}"

# Step 2: Wait for user to complete edits
echo ""
echo "=== Step 2: Edit XML ==="
echo "Edit the XML at: ${UNPACKED_DIR}/word/document.xml"
echo "Press Enter when edits are complete..."
read -r

# Step 3: Pack resume
echo ""
echo "=== Step 3: Packing resume ==="

# Find pack script
if [ -f "/mnt/skills/public/docx/scripts/office/pack.py" ]; then
    PACK_SCRIPT="/mnt/skills/public/docx/scripts/office/pack.py"
elif [ -f "${HOME}/.claude/plugins/marketplaces/anthropic-agent-skills/skills/docx/ooxml/scripts/pack.py" ]; then
    PACK_SCRIPT="${HOME}/.claude/plugins/marketplaces/anthropic-agent-skills/skills/docx/ooxml/scripts/pack.py"
else
    echo "ERROR: Could not find pack.py script" >&2
    exit 1
fi

python3 "${PACK_SCRIPT}" "${UNPACKED_DIR}" "${OUTPUT_FILE}"

# Step 4: Verify page count (unless skipped)
if [ $NO_VERIFY -eq 0 ]; then
    echo ""
    echo "=== Step 4: Verifying page count ==="
    bash "${SCRIPT_DIR}/verify_page_count.sh" "${OUTPUT_FILE}"
else
    echo ""
    echo "=== Skipping verification (--no-verify) ==="
fi

SUCCESS=1
echo ""
echo "=== Resume creation complete ==="
echo "Output: ${OUTPUT_FILE}"

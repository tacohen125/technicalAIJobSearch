#!/usr/bin/env bash
set -euo pipefail

# Cleanup unpacked directories safely with validation
# Usage: cleanup_unpacked.sh [pattern] [--force]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "${SCRIPT_DIR}")"
PATTERN="${1:-unpacked*}"
FORCE=0

# Parse --force flag
if [ "${2:-}" = "--force" ] || [ "${1:-}" = "--force" ]; then
    FORCE=1
    [ "${1}" = "--force" ] && PATTERN="unpacked*"
fi

cd "${SKILL_DIR}"

# Find and validate directories
VALID_DIRS=()
for dir in $(find . -maxdepth 1 -type d -name "${PATTERN}" 2>/dev/null); do
    if [ -f "${dir}/word/document.xml" ] && [ -d "${dir}/_rels" ]; then
        VALID_DIRS+=("$dir")
    fi
done

if [ ${#VALID_DIRS[@]} -eq 0 ]; then
    echo "No valid unpacked directories found matching pattern: ${PATTERN}"
    exit 0
fi

# List directories
echo "Found ${#VALID_DIRS[@]} unpacked directory/directories:"
for dir in "${VALID_DIRS[@]}"; do
    SIZE=$(du -sh "$dir" 2>/dev/null | cut -f1)
    echo "  - $dir ($SIZE)"
done

# Confirm unless --force
if [ $FORCE -eq 0 ]; then
    read -p "Delete these directories? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        exit 0
    fi
fi

# Delete directories
for dir in "${VALID_DIRS[@]}"; do
    echo "Removing $dir..."
    rm -rf "$dir"
done

echo "Cleanup complete"

#!/usr/bin/env bash
# Copies the root lottie.html into every test_website*/ folder
# so each one can serve the tester via a local web server, without storing
# duplicate copies in git (see .gitignore).
#
# Usage: ./copy_lottie_to_test_folders.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

SRC="lottie.html"

if [[ ! -f "$SRC" ]]; then
  echo "Error: $SRC not found in $SCRIPT_DIR" >&2
  echo "Place lottie.html in the project root before running this script." >&2
  exit 1
fi

shopt -s nullglob
dirs=(test_website*/)
if [[ ${#dirs[@]} -eq 0 ]]; then
  echo "No test_website*/ folders found in $SCRIPT_DIR." >&2
  exit 1
fi

for dir in "${dirs[@]}"; do
  cp -v "$SRC" "$dir"
done

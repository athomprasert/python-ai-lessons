#!/usr/bin/env bash
# Sync lessons + reference docs from the teaching workspace into this public repo,
# then commit and push to GitHub Pages.
#
# Usage:
#   ./sync.sh "Add L27 — ADK Tools"
#   ./sync.sh                                  # prompts for a commit message

set -euo pipefail

# --- Config ---
SOURCE_DIR="$HOME/ai/claude/projects/python"
PUBLIC_DIR="$HOME/ai/claude/projects/python-lessons-public"

# --- Sanity checks ---
if [[ ! -d "$SOURCE_DIR/lessons" ]]; then
  echo "ERROR: source lessons directory not found: $SOURCE_DIR/lessons"
  exit 1
fi
if [[ ! -d "$PUBLIC_DIR/lessons" ]]; then
  echo "ERROR: public lessons directory not found: $PUBLIC_DIR/lessons"
  exit 1
fi

cd "$PUBLIC_DIR"

# --- Copy files (only .html, never .env or other stray files) ---
echo "Copying lessons..."
cp "$SOURCE_DIR/lessons/"*.html "$PUBLIC_DIR/lessons/"

echo "Copying reference docs..."
cp "$SOURCE_DIR/reference/"*.html "$PUBLIC_DIR/reference/"

# --- Show what changed ---
echo ""
echo "Changes:"
git status --short

# --- Bail if nothing changed ---
if [[ -z "$(git status --porcelain)" ]]; then
  echo ""
  echo "No changes to commit. Done."
  exit 0
fi

# --- Commit message ---
if [[ $# -ge 1 ]]; then
  MSG="$1"
else
  read -r -p "Commit message: " MSG
fi

if [[ -z "$MSG" ]]; then
  echo "ERROR: empty commit message"
  exit 1
fi

# --- Commit + push ---
git add lessons/ reference/ index.html
git commit -m "$MSG"
git push

echo ""
echo "Done. Pages will rebuild in ~30s."
echo "Live URL: https://athomprasert.github.io/python-ai-lessons/"

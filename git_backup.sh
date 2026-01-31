#!/bin/bash

# Navigate to your project directory
TARGET_DIR="/home/john/antigravity-mcp"
cd "$TARGET_DIR" || exit

# Check if there are actually any changes to commit
if [ -z "$(git status --porcelain)" ]; then
    echo "$(date): No changes detected. Skipping backup."
    exit 0
fi

# Add all changes (respecting your .gitignore)
git add .

# Commit with a timestamped message
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Automated backup: $TIMESTAMP"

# Push to GitHub
# We use 'gh auth token' logic to ensure it uses your verified PAT
git push origin main

echo "$(date): Backup successfully pushed to GitHub."

#!/bin/bash

# Navigate to the project directory
cd ~/antigravity-mcp-setup

# Add all changes
git add .

# Create a commit message with the current date and time
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "Daily update: $TIMESTAMP"

# Push to your repository
# We use 'master' here because that is what your local machine is tracking
git push origin master

echo "---------------------------------------"
echo "Antigravity MCP Backup Complete: $TIMESTAMP"
echo "---------------------------------------"

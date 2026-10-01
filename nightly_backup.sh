#!/bin/bash
# Move to the project directory
cd /home/john/antigravity-mcp-setup

# Run the MCP server in "one-shot" mode using Python to trigger the backup
# This uses the venv python to ensure all Google libraries are present
/home/john/antigravity-mcp-setup/venv/bin/python3 -c "
from server import backup_to_cloud
print(backup_to_cloud.fn('johnnuc_backup_all'))
" >> /home/john/antigravity-mcp-setup/backup_log.txt 2>&1

# ... existing backup code ...

# Add this line at the very end
/home/john/antigravity-mcp-setup/venv/bin/python3 -c "from server import rotate_backup_logs; print(rotate_backup_logs.fn(50))" >> /home/john/antigravity-mcp-setup/backup_log.txt 2>&1

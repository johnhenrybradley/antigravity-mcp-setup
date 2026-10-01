import os
import zipfile
import io
from datetime import datetime
from fastmcp import FastMCP
from google.cloud import storage

# Initialize FastMCP
mcp = FastMCP("antigravity")

# Initialize Google Cloud Storage Client
# Ensure your GOOGLE_APPLICATION_CREDENTIALS env var is set if needed
storage_client = storage.Client()

@mcp.tool()
def list_project_files() -> str:
    """Lists files in the current project directory."""
    files = os.listdir(".")
    return f"Project files: {', '.join(files)}"

@mcp.tool()
def list_my_buckets() -> list:
    """Lists all Google Cloud Storage buckets in the project."""
    buckets = list(storage_client.list_buckets())
    return [b.name for b in buckets]

@mcp.tool()
def backup_to_cloud(bucket_name: str) -> str:
    """Zips the current directory and uploads it to a specified GCS bucket."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"backup_{timestamp}.zip"
    
    # Create zip in memory to avoid local clutter
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for root, dirs, files in os.walk("."):
            for file in files:
                # Skip the venv folder to keep backup small
                if "venv" in root:
                    continue
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, "."))

    # Upload to GCS
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f"backups/{zip_filename}")
        zip_buffer.seek(0)
        blob.upload_from_file(zip_buffer, content_type="application/zip")
        return f"Successfully backed up project to {bucket_name}/backups/{zip_filename}"
    except Exception as e:
        return f"Backup failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()

import psutil # Add this at the top with other imports

@mcp.tool()
def get_system_health() -> str:
    """Returns CPU usage, RAM availability, and disk space for the NUC."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Try to get temperature (might require 'lm-sensors' installed on Ubuntu)
    temps = "N/A"
    try:
        t = psutil.sensors_temperatures()
        if 'coretemp' in t:
            temps = f"{t['coretemp'][0].current}°C"
    except:
        pass

    return (
        f"NUC Health Report:\n"
        f"- CPU Usage: {cpu}%\n"
        f"- RAM: {ram.percent}% used ({ram.available // (1024**2)}MB free)\n"
        f"- Disk: {disk.percent}% used ({disk.free // (1024**3)}GB free)\n"
        f"- CPU Temp: {temps}"
    )

from google.cloud import billing_v1 # Add at top

@mcp.tool()
def check_billing_status(project_id: str) -> str:
    """Checks if billing is enabled for the specified Google Cloud project."""
    try:
        client = billing_v1.CloudBillingClient()
        name = f"projects/{project_id}"
        billing_info = client.get_project_billing_info(name=name)
        
        status = "ENABLED" if billing_info.billing_enabled else "DISABLED"
        return f"Billing Status for {project_id}: {status}\nBilling Account: {billing_info.billing_account_name}"
    except Exception as e:
        return f"Could not retrieve billing info: {str(e)}"
import os
import time

@mcp.tool()
def rotate_backup_logs(max_entries: int = 50) -> str:
    """Keeps only the last X lines of the backup log to prevent file bloat."""
    log_path = "/home/john/antigravity-mcp-setup/backup_log.txt"
    
    if not os.path.exists(log_path):
        return "No log file found to rotate."

    try:
        with open(log_path, "r") as f:
            lines = f.readlines()
        
        if len(lines) <= max_entries:
            return f"Log is healthy ({len(lines)} lines). No rotation needed."
        
        # Keep only the most recent entries
        with open(log_path, "w") as f:
            f.writelines(lines[-max_entries:])
            
        return f"Rotated log. Kept the latest {max_entries} entries."
    except Exception as e:
        return f"Rotation failed: {str(e)}"

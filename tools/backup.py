import os
import subprocess
from agent.tools import tool

@tool
def backup_check_disk():
    """show disk usage of the filesystem holding the backups."""
    backup_path = os.environ.get("BACKUP_PATH", "/backup")
    p = subprocess.run(["df", "-h", backup_path], capture_output=True, text=True)
    return "disk usage:\n" + (p.stdout.strip() or p.stderr.strip())

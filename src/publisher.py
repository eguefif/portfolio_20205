"""
Publisher module to copy and publish index.html to personal website.
"""

import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def publish_to_website(source_file: str, target_dir: str):
    """
    Copy index.html to personal website directory and commit/push changes.

    Args:
        source_file: Path to the source index.html file
        target_dir: Path to the target personal website directory
    """
    source_path = Path(source_file)
    target_path = Path(target_dir)

    # Verify source file exists
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    # Verify target directory exists
    if not target_path.exists():
        raise FileNotFoundError(f"Target directory not found: {target_dir}")

    # Copy index.html to target directory
    target_file = target_path / "index.html"
    shutil.copy2(source_path, target_file)
    print(f"Copied {source_file} to {target_file}")

    # Generate timestamp for commit message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Update website - {timestamp}"

    # Git operations
    try:
        # Change to target directory
        subprocess.run(
            ["git", "add", "-A"],
            cwd=target_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print("Git add completed")

        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=target_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Git commit completed: {commit_message}")

        #subprocess.run(
        #    ["git", "push"],
        #    cwd=target_dir,
        #    check=True,
        #    capture_output=True,
        #    text=True
        #)
        #print("Git push completed successfully")

    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e.stderr}")
        raise

import os
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def clone_btiq_repo():
    repo_path = Path("/app/btiq")

    if (repo_path / ".git").exists():
        logger.info("BTIQ repository already exists, skipping clone")
        return

    username = os.getenv("GIT_USERNAME")
    password = os.getenv("GIT_PASSWORD")

    if not username or not password:
        raise ValueError(
            "GIT_USERNAME and GIT_PASSWORD environment variables must be set"
        )

    repo_url = (
        f"https://{username}:{password}@bigtime.visualstudio.com/BigTime/_git/BTIQ"
    )

    try:
        logger.info("Cloning BTIQ repository...")
        subprocess.run(
            ["git", "clone", repo_url, str(repo_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info("BTIQ repository cloned successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clone repository: {e.stderr}")
        raise

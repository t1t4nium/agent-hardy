"""Configuration loading.
Importing this module loads the root .env file into os.environ, so the
rest of the code can read settings with os.environ.get(...).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Repo root: one directory up from this file (agent/).
ROOT = Path(__file__).resolve().parent.parent

# Without override=True, a variable already exported in the shell wins over .env.
load_dotenv(os.path.join(ROOT, ".env"))

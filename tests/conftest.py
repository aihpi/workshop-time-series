"""Shared test setup.

The notebooks import `nb_config` directly, because it sits next to them in
`notebooks/`. The tests import it the same way, so that they exercise the import
path the course actually uses.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"

for path in (REPO_ROOT, NOTEBOOKS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import os
from pathlib import Path

# Repository root; tests use this to locate source and data files instead of
# paths relative to the test file itself.
REPO_ROOT = Path(os.path.abspath(__file__)).parent.parent

import sys
from pathlib import Path

# Insert project root (one level up) into sys.path for pytest
proj_root = Path(__file__).parent.parent.resolve()
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))

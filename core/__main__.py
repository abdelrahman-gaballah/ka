import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))
from core.cli import main

main()

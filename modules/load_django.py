import os
import sys
from pathlib import Path

import django


PROJECT_ROOT = Path(__file__).resolve().parent.parent
project_root = str(PROJECT_ROOT)

if project_root not in sys.path:
    sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "braincomua_project.settings")
django.setup()

__all__ = []

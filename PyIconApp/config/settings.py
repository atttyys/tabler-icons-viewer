import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIRS = [
    os.path.join(BASE_DIR, "data", "icons", "filled"),
    os.path.join(BASE_DIR, "data", "icons", "outline"),
]

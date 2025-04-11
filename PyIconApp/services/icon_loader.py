import os

def load_icons_from_dirs(directories):
    icons = []
    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith(".svg"):
                icons.append({
                    "path": os.path.join(directory, filename),
                    "name": filename
                })
    return icons

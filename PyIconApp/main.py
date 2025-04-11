import sys
from PySide6.QtWidgets import QApplication
from config.settings import ICON_DIRS
from layouts.icon_gallery import IconGallery

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IconGallery(ICON_DIRS)
    window.show()
    sys.exit(app.exec())

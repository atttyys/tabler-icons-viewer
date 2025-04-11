from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, QScrollArea,
    QGridLayout, QPushButton, QHBoxLayout, QLabel, QComboBox,
)
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QAction  # ✅ เพิ่มบรรทัดนี้
from PySide6.QtCore import Qt
from components.icon_card import IconCard
from services.icon_loader import load_icons_from_dirs


class IconGallery(QMainWindow):
    def __init__(self, icon_dirs):
        super().__init__()
        self.setWindowTitle("SVG Icon Viewer")
        self.resize(800, 600)

        self.icon_dirs = icon_dirs
        self.all_icons = load_icons_from_dirs(self.icon_dirs)
        self.filtered_icons = self.all_icons.copy()
        self.page_size = 25
        self.current_page = 1

        # 🧱 Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # ✅ Menu Bar
        menu_bar = self.menuBar()
        # file_menu = menu_bar.addMenu("File")
        # view_menu = menu_bar.addMenu("View")
        help_menu = menu_bar.addMenu("Help")

        # ตัวอย่าง Action
        # view_menu.addAction(QAction("รีเฟรช", self, triggered=self.render_icons))
        about_action = QAction("เกี่ยวกับ", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # 🔍 Search + Dropdown
        top_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 ค้นหาชื่อไอคอน...")
        self.search.textChanged.connect(self.update_filter)

        self.category_filter = QComboBox()
        self.category_filter.addItems(["ทั้งหมด", "filled", "outline"])
        self.category_filter.currentTextChanged.connect(self.update_filter)

        top_row.addWidget(self.search)
        top_row.addWidget(self.category_filter)
        self.layout.addLayout(top_row)

        # 📜 Icon Grid Scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.grid = QGridLayout(self.content)
        self.scroll.setWidget(self.content)
        self.layout.addWidget(self.scroll)

        # 🧭 Navigation
        self.nav_container = QWidget()
        self.nav_layout = QHBoxLayout(self.nav_container)
        self.nav_layout.setAlignment(Qt.AlignCenter)

        self.prev_btn = QPushButton("⬅ ก่อนหน้า")
        self.page_label = QLabel("หน้า 1 / 1")
        self.next_btn = QPushButton("ถัดไป ➡")

        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)

        self.nav_layout.addWidget(self.prev_btn)
        self.nav_layout.addWidget(self.page_label)
        self.nav_layout.addWidget(self.next_btn)

        self.layout.addWidget(self.nav_container)

        # 🔄 Initial render
        self.render_icons()


    def update_filter(self, _=None):
        text = self.search.text().lower()
        selected = self.category_filter.currentText()

        if selected == "filled":
            filtered = [icon for icon in self.all_icons if "filled" in icon["path"].lower()]
        elif selected == "outline":
            filtered = [icon for icon in self.all_icons if "outline" in icon["path"].lower()]
        else:
            filtered = self.all_icons

        self.filtered_icons = [
            icon for icon in filtered if text in icon["name"].lower()
        ]

        self.current_page = 1
        self.render_icons()

    def render_icons(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        page_icons = self.filtered_icons[start:end]

        cols = 5
        for i, icon in enumerate(page_icons):
            card = IconCard(icon["path"], icon["name"])
            row, col = divmod(i, cols)
            self.grid.addWidget(card, row, col)

        # update page label
        total_pages = max(1, (len(self.filtered_icons) + self.page_size - 1) // self.page_size)
        self.page_label.setText(f"หน้า {self.current_page} / {total_pages}")

        # toggle button enabled
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)

    def next_page(self):
        total_pages = max(1, (len(self.filtered_icons) + self.page_size - 1) // self.page_size)
        if self.current_page < total_pages:
            self.current_page += 1
            self.render_icons()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.render_icons()

    def show_about(self):
        QMessageBox.about(
            self,
            "เกี่ยวกับ SVG Icon Viewer",
            (
                "<b>SVG Icon Viewer</b><br><br>"
                "แอปพลิเคชันนี้ใช้สำหรับดูและค้นหาไฟล์ไอคอน SVG<br>"
                "ไอคอนทั้งหมดในแอปนี้นำมาจากชุดไอคอนโอเพนซอร์ส <b>Tabler Icons</b><br>"
                "<a href='https://github.com/tabler/tabler-icons'>https://github.com/tabler/tabler-icons</a><br><br>"
                "พัฒนาเพื่อการเรียนรู้และใช้งานส่วนตัวเท่านั้น"
            )
        )

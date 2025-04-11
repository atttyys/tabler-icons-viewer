import os
import subprocess

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame,
    QHBoxLayout, QToolButton, QDialog, QDialogButtonBox
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QClipboard, QGuiApplication
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QFileDialog

class IconCard(QFrame):
    def __init__(self, path, name):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignHCenter)
        layout.setSpacing(6)

        self.path = path
        self.name = name

        svg = QSvgWidget(path)
        svg.setFixedSize(QSize(64, 64))
        svg.setStyleSheet("background: transparent;")

        # Horizontal layout for name + buttons
        name_row = QHBoxLayout()
        name_row.setAlignment(Qt.AlignCenter)

        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 10px;")

        # 📋 Copy button
        self.copy_btn = QToolButton()
        self.copy_btn.setText("📋")
        self.copy_btn.setToolTip("คัดลอก path")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setFixedSize(20, 20)
        self.copy_btn.setStyleSheet("QToolButton { border: none; padding: 0px; }")

        # 🔍 Preview button
        preview_btn = QToolButton()
        preview_btn.setText("🔍")
        preview_btn.setToolTip("ดูภาพขนาดใหญ่")
        preview_btn.clicked.connect(self.show_preview)
        preview_btn.setFixedSize(20, 20)
        preview_btn.setStyleSheet("QToolButton { border: none; padding: 0px; }")

        # 📂 Open folder button
        open_btn = QToolButton()
        open_btn.setText("📂")
        open_btn.setToolTip("เปิดโฟลเดอร์ของไฟล์นี้")
        open_btn.clicked.connect(self.open_folder)
        open_btn.setFixedSize(20, 20)
        open_btn.setStyleSheet("QToolButton { border: none; padding: 0px; }")

        # 💾 Export button
        export_btn = QToolButton()
        export_btn.setText("💾")
        export_btn.setToolTip("ส่งออกเป็น PNG")
        export_btn.clicked.connect(self.export_icon)
        export_btn.setFixedSize(20, 20)
        export_btn.setStyleSheet("QToolButton { border: none; padding: 0px; }")

        name_row.addWidget(label)
        name_row.addWidget(self.copy_btn)
        name_row.addWidget(preview_btn)
        name_row.addWidget(open_btn)
        name_row.addWidget(export_btn)

        layout.addWidget(svg, alignment=Qt.AlignCenter)
        layout.addLayout(name_row)

    def copy_to_clipboard(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.path)
        self.copy_btn.setText("✅")
        self.copy_btn.setToolTip("คัดลอกแล้ว!")

        QTimer.singleShot(1200, self.reset_copy_btn)

    def reset_copy_btn(self):
        self.copy_btn.setText("📋")
        self.copy_btn.setToolTip("คัดลอก path")

    def show_preview(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"ดูไอคอน: {self.name}")
        dialog.setMinimumSize(300, 300)

        dlg_layout = QVBoxLayout(dialog)

        svg = QSvgWidget(self.path)
        svg.setFixedSize(QSize(200, 200))
        svg.setStyleSheet("background: transparent;")

        name = QLabel(self.name)
        name.setAlignment(Qt.AlignCenter)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)

        dlg_layout.addWidget(svg, alignment=Qt.AlignCenter)
        dlg_layout.addWidget(name)
        dlg_layout.addWidget(buttons)

        dialog.exec()

    def open_folder(self):
        try:
            subprocess.Popen(f'explorer /select,"{self.path}"')
        except Exception as e:
            print("ไม่สามารถเปิดโฟลเดอร์ได้:", e)

    def export_icon(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("ส่งออกไอคอน")
        dialog.setMinimumSize(300, 350)
        layout = QVBoxLayout(dialog)

        # Preview icon
        preview = QSvgWidget(self.path)
        preview.setFixedSize(QSize(128, 128))
        preview.setStyleSheet("background: transparent;")
        layout.addWidget(preview, alignment=Qt.AlignCenter)

        # Dropdown ขนาด
        size_label = QLabel("เลือกขนาด:")
        size_label.setAlignment(Qt.AlignCenter)

        from PySide6.QtWidgets import QComboBox
        size_combo = QComboBox()
        sizes = ["16", "32", "64", "128", "256", "512", "1024"]
        size_combo.addItems(sizes)
        size_combo.setCurrentText("128")

        layout.addWidget(size_label)
        layout.addWidget(size_combo, alignment=Qt.AlignCenter)

        # ปุ่ม OK / Cancel
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec():
            size = int(size_combo.currentText())

            renderer = QSvgRenderer(self.path)
            export_size = QSize(size, size)

            pixmap = QPixmap(export_size)
            pixmap.fill(Qt.transparent)

            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()

            save_path, _ = QFileDialog.getSaveFileName(
                self,
                f"บันทึกเป็น PNG ({size}x{size})",
                self.name.replace(".svg", f"_{size}px.png"),
                "PNG Files (*.png)"
            )
            if save_path:
                pixmap.save(save_path, "PNG")